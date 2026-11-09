"""Model checking of a synthesized hierarchy with CMurphi.

The model holds one address and, from the bottom up: `caches` first-level caches, every
synthesized controller, `top_caches` plain caches of the top protocol (the other agents of the
top domain) and the directory. CMurphi explores every interleaving of their messages and checks
that no state deadlocks and, unless only deadlocks are checked, that a store permission held by a
leaf cache (a first-level cache or a plain top cache) excludes any other load, ifetch or store
permission.

Bound of the model: an access that sends a request and completes at once, without waiting for
an answer (MESI-RC's ntload and ntstore: a stable state to a stable state), can be issued by a
cache only while none of its earlier ones is in flight, its request or the answer to it. Without
this a cache issues any number of them and the model's network overflows; the simulator bounds
them as well (the sequencer's outstanding requests).
"""

import os
import re
import subprocess
from pathlib import Path
from typing import List, Optional, Set, Tuple

from Backend.Murphi.ModularMurphi import ModularMurphi
from DataObjects.ClassCluster import Cluster
from DataObjects.ClassLevel import Level
from DataObjects.ClassMachine import Machine
from DataObjects.FlowDataTypes.ClassBaseAccess import BaseAccess

# Ubuntu 22.04 with make and g++ (the image the gem5 tools use)
DEFAULT_IMAGE = "carpeniem/synapse-artifact-s1_2_3:base"


def write_model(managers: List[Level], clients: List[Optional[Level]], name: str, caches: int,
                top_caches: int, swmr: bool = True) -> Path:
    """Writes <name>.m and its Makefile to the current directory."""
    machines = [Machine(managers[0].cache) for _ in range(caches)]
    machines += [Machine(manager.directory) for manager in managers]
    machines += [Machine(clients[-1].cache) for _ in range(top_caches)] + [Machine(clients[-1].directory)]
    archs = list(dict.fromkeys(machine.arch for machine in machines))
    ModularMurphi([Cluster(tuple(machines), "C1", False)], name, False, None).gen_make()
    model = Path(f"{name}.m").resolve()
    text = model.read_text()
    # A synthesized controller is also a requestor of the domain it manages (it takes the block
    # from its children), so that domain's sets hold one machine more than its caches.
    for level in range(1, len(managers) + 1):
        text = re.sub(rf"^(\s*NrCachesL{level}: )(\d+);", lambda m: f"{m.group(1)}{int(m.group(2)) + 1};", text,
                      count=1, flags=re.M)
    text = _bound_fire_and_forget(text, archs)
    if not swmr:
        model.write_text(text)
        return model
    leaves = [f"OBJSET_{managers[0].cache}"] + ([f"OBJSET_{clients[-1].cache}"] if top_caches else [])
    leaf = lambda m: "(" + " | ".join(f"IsMember({m}, {objset})" for objset in leaves) + ")"
    holds = lambda m, perm: f"MultiSetCount(i:g_perm[{m}][a], g_perm[{m}][a][i] = {perm}) > 0"
    model.write_text(text + f"""
invariant "SWMR among the leaf caches"
    forall a:Address do
        forall m1:Machines do
        forall m2:Machines do
        (m1 != m2 & {leaf("m1")} & {leaf("m2")} & {holds("m1", "store")})
        ->
          !({holds("m2", "store")} | {holds("m2", "load")} | {holds("m2", "ifetch")})
        endforall
        endforall
    endforall;
""")
    return model


def _fire_and_forget(archs) -> Tuple[Set[str], Set[str], Set[str]]:
    """The access rules that send a request and complete at once, the types of those requests and
    of the answers to them: messages sent to `<request>.src` by a handler of a request, or of a
    forward that carries the requester (`src` = `<request>.src`, e.g. MESI-RC's Fwd_GetNT)."""
    rules, requests = set(), set()
    for arch in archs:
        for transition in arch.get_architecture_transitions():
            if isinstance(transition.guard, BaseAccess.Access) and transition.out_msg and \
                    transition.start_state.stable and transition.final_state.stable:
                rules.add(f"{arch}_{transition.start_state}_{transition.guard}")
                requests |= {str(message) for message in transition.out_msg}
    base = lambda name: re.sub(r"L\d+$", "", name)
    carriers, answers = set(requests), set()
    while True:
        before = len(carriers)
        for arch in archs:
            for transition in arch.get_architecture_transitions():
                guard = str(transition.guard)
                if guard not in carriers:
                    continue
                for message in transition.out_msg:
                    if message.msg_routing.src == base(guard):
                        carriers.add(str(message))
                    if message.msg_routing.dest == base(guard):
                        answers.add(str(message))
        if len(carriers) == before:
            return rules, requests, answers


def _bound_fire_and_forget(text: str, archs) -> str:
    """Guards the fire-and-forget access rules with `!ff_in_flight(m)` (module docstring)."""
    rules, requests, answers = _fire_and_forget(archs)
    if not rules:
        return text
    def matches(message: str, types: Set[str]) -> str:
        return " | ".join(f"{message}.mtype = {name}" for name in sorted(types)) or "false"
    checks = []
    for net in re.findall(r"^\s*(\w+): NET_Ordered;", text, re.M):
        element = f"{net}[dst][i]"
        checks.append(f"""      for i: 0..O_NET_MAX-1 do
        if i < cnt_{net}[dst] then
          if ({element}.src = m & ({matches(element, requests)})) | (dst = m & ({matches(element, answers)})) then
            return true;
          endif;
        endif;
      endfor;""")
    for net in re.findall(r"^\s*(\w+): NET_Unordered;", text, re.M):
        element = f"{net}[dst][i]"
        checks.append(f"""      if MultiSetCount(i:{net}[dst], ({element}.src = m & ({matches(element, requests)})) |
                                    (dst = m & ({matches(element, answers)}))) > 0 then
        return true;
      endif;""")
    function = "\n".join(["function ff_in_flight(m: Machines): boolean;", "begin", "  for dst: Machines do",
                          *checks, "  endfor;", "  return false;", "end;", "", ""])
    first_ruleset = re.search(r"^\s*ruleset ", text, re.M)
    text = text[:first_ruleset.start()] + "\n" + function + text[first_ruleset.start():]
    for rule in sorted(rules):
        text, found = re.subn(rf'(rule "{re.escape(rule)}"\n\s*cbe\.State = [^\n]*?)(\s*\n)',
                              r"\1 & !ff_in_flight(m)\2", text, count=1)
        assert found, f"no access rule {rule} in the model"
    return text


def check(model: Path, cmurphi: Path, memory_mb: int, image: Optional[str]) -> Tuple[str, str]:
    """Compiles the model with CMurphi (`cmurphi`: a CMurphi tree with src/mu built) and explores
    it; in `image` with docker, or with the local make and g++ if None. Returns the verdict and the
    report, which is also written next to the model (results.txt)."""
    name, folder = model.stem, model.parent
    script = f"make MURPHIPATH={{murphi}} > compile.txt 2>&1 && ./{name} -tv -pr -m {memory_mb} > results.txt 2>&1"
    if image:
        command = ["docker", "run", "--rm", "--init", "--name", f"synapse-verify-{name}-{os.getpid()}",
                   "--user", f"{os.getuid()}:{os.getgid()}", "-v", f"{cmurphi.resolve()}:/cmurphi:ro",
                   "-v", f"{folder}:/model", "-w", "/model", image, "bash", "-c", script.format(murphi="/cmurphi")]
    else:
        command = ["bash", "-c", script.format(murphi=cmurphi.resolve())]
    subprocess.run(command, cwd=folder)
    report = (folder / "results.txt").read_text(errors="replace") if (folder / "results.txt").is_file() else ""
    if "No error found" in report:
        states = re.search(r"(\d+) states, \d+ rules fired in ([\d.]+)s", report)
        verdict = "verified" + (f": {int(states.group(1)):,} states in {float(states.group(2)):.0f} s" if states else "")
    elif "Deadlocked state found" in report:
        verdict = "deadlock (trace in results.txt)"
    elif re.search(r"Invariant .* failed", report):
        verdict = "a leaf cache writes while another one holds the block (trace in results.txt)"
    elif "Too many messages" in report:
        verdict = "a queue of the model's network overflowed (trace in results.txt)"
    elif "Too many active states" in report or "Closed hash table full" in report:
        verdict = f"the state table is full: give more --memory than {memory_mb} MB"
    elif not report:
        verdict = "the model did not compile (compile.txt)"
    else:
        verdict = "CMurphi stopped (results.txt)"
    return verdict, report
