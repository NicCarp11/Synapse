#!/usr/bin/env python3
"""Synapse: synthesis of cache coherence controllers from three specifications.

The topology describes the clusters of a system and the protocol and policy of each cache
controller; Synapse synthesizes every controller of the hierarchy and writes it as a SLICC state
machine for gem5. The files are named after the system and the role of each controller:

    <name>_client_<L1>.sm            the first-level cache, a client of its protocol
    <name>_client_manager_<LLC>.sm   a synthesized controller: manager below, client above
    <name>_manager_<directory>.sm    the directory, the manager of its protocol
    <name>_msg.sm, <name>.slicc      the messages, and the list of files gem5 builds the protocol from
    <name>_gem5.py                   the gem5 setup: runs a program on the system with them

    python synapse.py generate specs/topologies/smp.yaml --out out/smp
    python synapse.py generate specs/topologies/smp.yaml --out out/moesi --set directory.protocol=MOESI
    python synapse.py show specs/topologies/numa.yaml       # the resolved system only
    python synapse.py labels specs/topologies/smp.yaml      # the labels the synthesis works on
    python synapse.py verify specs/topologies/smp.yaml --out out/smp-murphi --murphi <CMurphi>
"""

import argparse
import contextlib
import json
import os
import re
import shutil
import sys
import tempfile
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Tuple

if __name__ == "__main__" and os.environ.get("PYTHONHASHSEED") != "0":
    # The synthesis passes iterate over sets, so the names of a few generated states depend on
    # Python's string hashing. A fixed seed makes the output the same, byte for byte, on every run.
    os.environ["PYTHONHASHSEED"] = "0"
    os.execv(sys.executable, [sys.executable, *sys.argv])

from tabulate import tabulate

ROOT = Path(__file__).resolve().parent
# The ANTLR 3 runtime of the protocol parser is shipped with the tool (third_party/README.md).
# It predates the compiler's warning about unknown escapes in string literals.
sys.path.insert(0, str(ROOT / "third_party"))
warnings.filterwarnings("ignore", category=SyntaxWarning, module=r".*[/\\]antlr3[/\\]")

from Algorithms.Synapse.Labeling import ProtocolLabels
from Algorithms.Synapse.LocalWrite import LocalWriteError, derive
from Algorithms.Synapse.Policy import Policy, load_policy
from Algorithms.Synapse.Synthesis import SynapseDirArchitecture, SynthesisError
from Algorithms.Synapse.Topology import SLICES_INTERLEAVED, STALL_PARK, Topology, TopologyError, load_topology
from Backend.SLICC.ModularSLICC.BackendOptions import GEM5_V20, GEM5_V23, LLC_BANKED, LLC_CLUSTER, LLC_RANGE, \
    BackendOptions
from Backend.Murphi.Verify import DEFAULT_IMAGE, check, write_model
from Backend.SLICC.RunSLICCModular import RunSLICCModular
from Backend.gem5.Setup import write_setup
from DataObjects.ClassCluster import Cluster
from DataObjects.ClassLevel import Level
from DataObjects.ClassMachine import Machine
from DataObjects.FlowDataTypes.ClassBaseAccess import Access
from DataObjects.FlowDataTypes.ClassEvent import Event
from Parser.NetworkxParser.ClassProtoParser import ProtoParser

PROTOCOL_DIR = ROOT / "specs" / "protocols"
POLICY_DIR = ROOT / "specs" / "policies"
LOG_NAME = "synapse.log"


class UnsupportedError(Exception):
    """The controllers are synthesized, but the SLICC back end cannot write them."""

SYSTEM_NAME = "system.json"


def load_level(protocol: Path, index: int, text: Optional[str] = None) -> Level:
    """Parses a protocol (or `text`, a version of it) as level `index` of the hierarchy (its
    messages get the suffix L<index + 1>). The parser writes its debug graphs to the working
    directory."""
    return Level(ProtoParser(text or protocol.read_text(), protocol.name, False, True), f"L{index + 1}")


def load_levels(protocols: List[Path], texts: Dict[int, str] = None) -> Tuple[List[Level], List[Optional[Level]]]:
    """(managers, clients): managers[i] is protocol i seen from below (its caches and the manager
    of synthesis i), clients[i] is protocol i seen from above (the client of synthesis i - 1 and,
    for the last one, the directory). Every synthesis transforms the levels it is given (ProtoGen
    concurrency, proxy cache), so a protocol in the middle of the chain is parsed twice, with the
    same level id: both instances have the same messages and machine names. `texts` replaces the
    text of some protocols (by index)."""
    texts = texts or {}
    managers = [load_level(protocol, i, texts.get(i)) for i, protocol in enumerate(protocols[:-1])]
    clients = [None] + [load_level(protocol, i, texts.get(i)) for i, protocol in enumerate(protocols) if i > 0]
    return managers, clients


def local_protocols(topology: Topology, policies: List[Policy]) -> Dict[int, str]:
    """The protocols rewritten for the Local rules of the policies (LocalWrite.py): the parent of a
    controller with such rules takes the child's write accesses locally."""
    protocols = topology.protocol_chain()
    texts: Dict[int, str] = {}
    for i, policy in enumerate(policies):
        if not policy.local_rules:
            continue
        controller = topology.intermediates[i]
        if controller.instances != 1:
            raise TopologyError(f"{controller.name}: policy {policy.name} takes write permission without the parent "
                                f"(Local), which needs a single {controller.name} for every block; it has "
                                f"{controller.instances} instances")
        child = load_level(protocols[i], i)
        child_labels = ProtocolLabels(child)
        requests = {name for name, label in child_labels.msg_labels.items()
                    if any(rule.msg.matches(label) for rule in policy.local_rules)}
        accesses = list(dict.fromkeys(str(t.guard) for t in child.cache.get_architecture_transitions()
                                      if isinstance(t.guard, Access) and any(str(m) in requests for m in t.out_msg)))
        if not accesses:
            raise SynthesisError(f"policy {policy.name}: no access of {protocols[i].stem} sends a request that its "
                                 "Local rules match")
        parent = protocols[i + 1]
        text = texts.get(i + 1, parent.read_text())
        try:
            texts[i + 1] = derive(text, load_level(parent, i + 1, text), accesses)
        except LocalWriteError as error:
            raise SynthesisError(f"policy {policy.name}: {parent.stem} cannot take {', '.join(accesses)} "
                                 f"locally: {error}") from error
    return texts


def merge_global_architectures(levels: List[Level]):
    """One message and access space for the whole hierarchy (the back end writes one message
    file). Each synthesis merges the two levels it composes; this merges the syntheses. The two
    instances of a protocol in the middle of the chain declare the same messages: they are kept
    once."""
    ref = levels[0].directory.global_arch
    for level in levels[1:]:
        other = level.directory.global_arch if level.directory else level.cache.global_arch
        if other is ref:
            continue
        for name in list(other.network.base_message_dict):
            if name in ref.network.base_message_dict:
                other.network.base_message_dict.pop(name)
        ref.merge_base_architecture(other)
    for level in levels:
        for arch in level.get_architectures():
            arch.global_arch = ref


def backend_options(topology: Topology) -> BackendOptions:
    """The choices of the SLICC back end that follow from the topology."""
    parent_of_l1 = topology.intermediates[0]
    if parent_of_l1.slices == 1:
        llc_mapping = LLC_CLUSTER
    else:
        llc_mapping = LLC_BANKED if parent_of_l1.slice_select == SLICES_INTERLEAVED else LLC_RANGE
    return BackendOptions(llc_mapping=llc_mapping,
                          gem5=GEM5_V20 if topology.simulator == "alloy-gem5-v20" else GEM5_V23,
                          park_requests=parent_of_l1.stalled_requests == STALL_PARK)


def load_policies(topology: Topology) -> List[Policy]:
    return [load_policy(path, name) for path, name in topology.policy_chain()]


STATE_ORDER = "ISFEOM"


def state_order(state: str):
    """I, S, F, E, O, M; a synthesized controller's states by its own state, then its children's."""
    return [STATE_ORDER.index(part) if part in STATE_ORDER else len(STATE_ORDER)
            for part in reversed(state.split("__C__"))], state


def show_states(states: List[str]) -> str:
    """A synthesized controller's states as <children>/<own>, grouped by its own state."""
    if not any("__C__" in state for state in states):
        return " ".join(states)
    groups = {}
    for state in states:
        groups.setdefault(state.split("__C__")[-1], []).append(state.replace("__C__", "/"))
    return "  ".join(" ".join(group) for group in groups.values())


def compose(topology: Topology) -> Tuple[List[Level], List[Optional[Level]], List[str]]:
    """Synthesizes the controllers of the topology: the levels of its protocols (load_levels),
    each synthesized controller being the directory of a manager level, and the warnings."""
    policies = load_policies(topology)
    managers, clients = load_levels(topology.protocol_chain(), local_protocols(topology, policies))
    warnings: List[str] = []
    for i, policy in enumerate(policies):
        warnings += SynapseDirArchitecture(managers[i], clients[i + 1], policy).warnings
    return managers, clients, list(dict.fromkeys(warnings))


def merge_levels(managers: List[Level], clients: List[Optional[Level]]):
    merge_global_architectures([level for i in range(len(clients))
                                for level in (managers[i] if i < len(managers) else None, clients[i])
                                if level is not None])


def synthesize(topology: Topology) -> Tuple[List[Path], List[str], List[Tuple[List[str], int, int]]]:
    """Synthesizes the controllers of the topology in the current directory, which also receives
    the intermediate files of the parser and of the back end. Returns the SLICC files, the
    warnings of the synthesis and, for each controller of the hierarchy, its state machine: (stable
    states, number of states, number of transitions)."""
    managers, clients, warnings = compose(topology)
    controllers = [managers[0].cache, *(manager.directory for manager in managers), clients[-1].directory]
    sizes = [(sorted(map(str, controller.stable_states), key=state_order), len(controller.get_architecture_states()),
              len(controller.get_architecture_transitions())) for controller in controllers]
    events = sorted({str(t.guard) for controller in controllers for t in controller.get_architecture_transitions()
                     if isinstance(t.guard, Event)})
    if events:
        raise UnsupportedError(f"the controllers raise events ({', '.join(events)}), which the SLICC back end does "
                               "not translate yet; `verify` model-checks them")
    merge_levels(managers, clients)
    machines = [Machine(managers[0].cache), Machine(clients[-1].directory),
                *(Machine(manager.directory) for manager in managers)]
    system_name = "_".join(protocol.stem for protocol in topology.protocol_chain())
    RunSLICCModular(Cluster(tuple(machines), 'C1', False), system_name, backend_options(topology))
    return sorted(Path("SLICC").resolve().glob("*.sm")), warnings, sizes


@contextlib.contextmanager
def output_to(log: Path):
    """Sends what is written to stdout and stderr, also by child processes, to a file: the
    parser, the synthesis passes and the back end trace their work there."""
    sys.stdout.flush()
    sys.stderr.flush()
    saved = os.dup(1), os.dup(2)
    with open(log, "w") as file:
        os.dup2(file.fileno(), 1)
        os.dup2(file.fileno(), 2)
        try:
            yield
        finally:
            sys.stdout.flush()
            sys.stderr.flush()
            os.dup2(saved[0], 1)
            os.dup2(saved[1], 2)
            os.close(saved[0])
            os.close(saved[1])


@contextlib.contextmanager
def working_directory(keep: Optional[Path]):
    """Runs in a scratch directory (`keep`, or a temporary one that is removed afterwards)."""
    start = Path.cwd()
    with contextlib.ExitStack() as stack:
        if keep is None:
            work = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="synapse-")))
        else:
            work = keep.resolve()
            work.mkdir(parents=True, exist_ok=True)
        os.chdir(work)
        try:
            yield work
        finally:
            os.chdir(start)


def cmd_generate(args) -> int:
    topology = read_topology(args)
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    log = out / LOG_NAME
    print("\n".join(topology.describe()))
    with working_directory(args.work):
        try:
            with output_to(log) if not args.verbose else contextlib.nullcontext():
                slicc_files, warnings, sizes = synthesize(topology)
        except SynthesisError as error:
            print(f"synthesis failed: {error}", file=sys.stderr)
            return 2
        except UnsupportedError as error:
            print(f"cannot write SLICC: {error}", file=sys.stderr)
            return 2
        except Exception:
            if not args.verbose:
                print(f"generation failed, the trace is in {args.out / LOG_NAME}", file=sys.stderr)
            raise
        remove_previous_output(out)
        written = write_slicc(topology, slicc_files, out)
    setup = write_setup(topology, out, written)
    written.append(setup)
    system = topology.resolved()
    system["files"] = written
    (out / SYSTEM_NAME).write_text(json.dumps(system, indent=2) + "\n")

    print()
    print(tabulate([(controller.name, show_states(stable), states, transitions)
                    for controller, (stable, states, transitions) in zip(topology.hierarchy, sizes)],
                   headers=["controller", "stable states", "states", "transitions"]))
    for warning in warnings:
        print(f"warning: {warning}")
    machines = [name for name in written if name.endswith(".sm")]
    lines = sum(len((out / name).read_text().splitlines()) for name in machines)
    print(f"wrote {len(machines)} SLICC files ({lines} lines), {topology.name}.slicc, {setup} and {SYSTEM_NAME} "
          f"to {args.out}")
    return 0


def write_slicc(topology: Topology, slicc_files: List[Path], out: Path) -> List[str]:
    """Copies the back end's files to `out` under the names of the system (module docstring) and
    writes <name>.slicc. Returns the names, in the order gem5 includes them."""
    by_machine = {}
    for slicc_file in slicc_files:
        declared = re.search(r"machine\(MachineType:(\w+)", slicc_file.read_text())
        by_machine[declared.group(1) if declared else None] = slicc_file

    def role(controller) -> str:
        if controller in topology.intermediates:
            return "client_manager"
        return "client" if controller is topology.hierarchy[0] else "manager"

    # the messages first, then the machines from the directory down to the first-level cache
    order = [topology.hierarchy[-1], *topology.intermediates, topology.hierarchy[0]]
    names = {None: f"{topology.name}_msg.sm"}
    names.update({topology.machine(controller): f"{topology.name}_{role(controller)}_{controller.name}.sm"
                  for controller in order})
    written = []
    for machine in [None, *(topology.machine(controller) for controller in order)]:
        shutil.copy2(by_machine[machine], out / names[machine])
        written.append(names[machine])
    manifest = [f'protocol "{topology.name}";', "", 'include "RubySlicc_interfaces.slicc";',
                *(f'include "{name}";' for name in written)]
    (out / f"{topology.name}.slicc").write_text("\n".join(manifest) + "\n")
    return [*written, f"{topology.name}.slicc"]


def remove_previous_output(out: Path):
    """Removes the files a previous run wrote to `out` (those its system.json lists), so that the
    directory holds one system only."""
    previous = out / SYSTEM_NAME
    if previous.is_file():
        for name in json.loads(previous.read_text()).get("files", []):
            (out / Path(name).name).unlink(missing_ok=True)


def cmd_verify(args) -> int:
    topology = read_topology(args)
    # a Local rule assumes one cache per block at its level: no other cache of the top protocol
    top_caches = args.top_caches if args.top_caches is not None else \
        (0 if any(policy.local_rules for policy in load_policies(topology)) else 1)
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    print("\n".join(topology.describe()))
    with working_directory(None):
        try:
            with output_to(out / LOG_NAME):
                managers, clients, _ = compose(topology)
                merge_levels(managers, clients)
                model = write_model(managers, clients, topology.name, args.caches, top_caches,
                                    swmr=not args.deadlock_only)
        except SynthesisError as error:
            print(f"synthesis failed: {error}", file=sys.stderr)
            return 2
        for name in (model.name, "Makefile"):
            shutil.copy2(model.parent / name, out / name)
    print(f"\nmodel: {args.out / model.name} ({args.caches} first-level caches, every synthesized controller, "
          f"{top_caches} other {topology.hierarchy[-1].protocol.stem} caches, the directory; one address)")
    if args.murphi is None:
        print("give --murphi to check it")
        return 0
    verdict, report = check(out / model.name, args.murphi, args.memory, None if args.no_docker else args.image)
    print(f"{'deadlock freedom' if args.deadlock_only else 'deadlock freedom and single writer'}: {verdict}")
    return 0 if "No error found" in report else 1


def cmd_show(args) -> int:
    print("\n".join(read_topology(args).describe()))
    return 0


def cmd_labels(args) -> int:
    topology = read_topology(args)
    protocols = list(dict.fromkeys(topology.protocol_chain()))
    with working_directory(None), tempfile.NamedTemporaryFile(suffix=".log") as log:
        with output_to(Path(log.name)):
            labels = [ProtocolLabels(load_level(protocol, i)) for i, protocol in enumerate(protocols)]
    for protocol, protocol_labels in zip(protocols, labels):
        print(f"\nLabels of {protocol.name}")
        print(tabulate(protocol_labels.table(), headers=["Controller", "Kind", "Name", "Label"]))
    for policy in load_policies(topology):
        print(f"\n{policy}")
    return 0


def read_topology(args) -> Topology:
    return load_topology(args.topology, args.set or (), [PROTOCOL_DIR], [POLICY_DIR])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)

    def add_command(name: str, function, description: str) -> argparse.ArgumentParser:
        command = commands.add_parser(name, help=description, description=description)
        command.add_argument("topology", type=Path, help="topology specification (YAML)")
        command.add_argument("--set", action="append", metavar="KEY=VALUE",
                             help="change the topology before it is read: NODE.PARAMETER=VALUE with the name "
                                  "of a node (directory.protocol=MOESI, LLC.policy=WB_EXCL, core.count=16), "
                                  "or name=..., system=..., simulator=... (repeatable)")
        command.set_defaults(function=function)
        return command

    generate = add_command("generate", cmd_generate,
                           "synthesize the controllers of a topology and write them as SLICC")
    generate.add_argument("--out", type=Path, required=True,
                          help=f"directory of the SLICC files, <name>.slicc, the gem5 setup <name>_gem5.py, "
                               f"{SYSTEM_NAME} (the resolved system) and {LOG_NAME} (the trace of the run)")
    generate.add_argument("--work", type=Path,
                          help="keep the intermediate files (parser graphs, back-end output) in this "
                               "directory instead of a temporary one")
    generate.add_argument("--verbose", action="store_true",
                          help=f"print the trace instead of writing it to {LOG_NAME}")
    verify = add_command("verify", cmd_verify,
                         "model-check the synthesized controllers with CMurphi: no deadlock, a single "
                         "writer or several readers")
    verify.add_argument("--out", type=Path, required=True, help="directory of the model and of CMurphi's report")
    verify.add_argument("--murphi", type=Path, help="a CMurphi tree with src/mu built; without it the model is "
                                                     "only written")
    verify.add_argument("--caches", type=int, default=2, help="first-level caches in the model (2)")
    verify.add_argument("--top-caches", type=int,
                        help="other caches of the top protocol, beside the synthesized controller (1; 0 "
                             "with a Local policy rule)")
    verify.add_argument("--deadlock-only", action="store_true",
                        help="check deadlock freedom only, not the single writer (e.g. release-consistent caches)")
    verify.add_argument("--memory", type=int, default=16384, help="memory of CMurphi's state table, in MB (16384)")
    verify.add_argument("--image", default=DEFAULT_IMAGE, help=f"docker image with make and g++ ({DEFAULT_IMAGE})")
    verify.add_argument("--no-docker", action="store_true", help="compile and run with the local make and g++")
    add_command("show", cmd_show, "print the system a topology resolves to")
    add_command("labels", cmd_labels, "print the labels of the topology's protocols and its policies")

    args = parser.parse_args()
    try:
        return args.function(args)
    except TopologyError as error:
        print(f"topology error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
