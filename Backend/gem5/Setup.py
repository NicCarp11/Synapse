"""The gem5 simulation setup of a topology.

write_setup() writes <name>_gem5.py next to the generated controllers, a gem5 configuration that
runs a program on the system of the topology with them: for gem5 v23, setup_v23.py, which builds
the whole system (cores, caches, directory, memory and network); for alloy-gem5 (gem5 v20),
setup_alloy.py, which runs alloy's own configuration script with the options of the system and the
Ruby configuration of the controllers. Either is the template with SYSTEM filled in.
"""

import re
import textwrap
from pathlib import Path
from typing import Any, Dict, List

from Algorithms.Synapse.Topology import CACHE, CLUSTER, CORE, MEMORY, Node, Topology

TEMPLATES = {"gem5-v23": Path(__file__).resolve().parent / "setup_v23.py",
             "alloy-gem5-v20": Path(__file__).resolve().parent / "setup_alloy.py"}
_VIRTUAL_NETWORK = re.compile(r'virtual_network="(\d+)"')
WIDTH = 120          # of the lines of SYSTEM


def setup_name(topology: Topology) -> str:
    return f"{topology.name}_gem5.py"


def write_setup(topology: Topology, out: Path, slicc_files: List[str]) -> str:
    """Writes the setup of `topology` to `out`, where its SLICC files are; returns its name."""
    networks = [int(number) for name in slicc_files if name.endswith(".sm")
                for number in _VIRTUAL_NETWORK.findall((out / name).read_text())]
    system = describe(topology, virtual_networks=max(networks) + 1)
    template = TEMPLATES[topology.simulator].read_text()
    docstring = '"""' + template.split('"""')[1] + '"""'
    text = template.replace(docstring, header(topology), 1)
    text = text.replace("\nSYSTEM = {}\n", f"\nSYSTEM = {literal(system, 'SYSTEM = ')}\n", 1)
    (out / setup_name(topology)).write_text(text)
    return setup_name(topology)


def header(topology: Topology) -> str:
    built = f"gem5 must be built with the protocol {topology.name} ({topology.name}.slicc)."
    if topology.simulator == "alloy-gem5-v20":
        simulator = "alloy-gem5 (gem5 v20)"
        usage = '[--cores N] [--alloy DIR] [SC3 OPTIONS] -c PROGRAM -o "ARGUMENTS"'
        text = (f"Runs alloy-gem5's configs/brg/sc3.py with the options of the system of the topology and the "
                f"Ruby configuration of the controllers generated with this file: {built} --help lists the options.")
    else:
        simulator = "gem5 v23"
        usage = "[--cores N] [OPTIONS] -- PROGRAM [ARGUMENTS]"
        text = (f"Builds the system of the topology around the controllers generated with this file: {built} "
                "PROGRAM runs in syscall-emulation mode; --help lists the options.")
    return (f'"""{topology.name} in {simulator}, written by Synapse from {topology.source.name}.\n\n'
            f"    gem5.opt [GEM5 OPTIONS] {setup_name(topology)} {usage}\n\n"
            + textwrap.fill(text, 100, break_on_hyphens=False) + '\n"""')


def literal(value: Any, prefix: str = "", indent: int = 0) -> str:
    """`value` as Python source: on one line if it fits, else one item per line."""
    flat = repr(value)
    if len(prefix) + indent + len(flat) <= WIDTH or not isinstance(value, (dict, list)):
        return flat
    inner = " " * (indent + 4)
    if isinstance(value, dict):
        items = [f"{inner}{key!r}: {literal(item, f'{key!r}: ', indent + 4)}" for key, item in value.items()]
        return "{\n" + ",\n".join(items) + ",\n" + " " * indent + "}"
    items = [f"{inner}{literal(item, '', indent + 4)}" for item in value]
    return "[\n" + ",\n".join(items) + ",\n" + " " * indent + "]"


def describe(topology: Topology, virtual_networks: int) -> Dict[str, Any]:
    """The system as the setup reads it."""
    core = next(node for node in topology.root.walk() if node.kind == CORE)
    return {
        "name": topology.name,
        "cores": topology.cores,
        "clock_hz": core.params["clock"],
        "virtual_networks": virtual_networks,
        "flit_size_bytes": topology.root.params["interconnect"]["flit_size"],
        "hierarchy": [controller.name for controller in topology.hierarchy],
        "root": _node(topology, topology.root),
    }


def _node(topology: Topology, node: Node) -> Dict[str, Any]:
    params = node.params
    body: Dict[str, Any] = {"kind": node.kind, "name": node.name}
    if node.kind == CLUSTER:
        body["count"] = params.get("count", 1)
        if "interconnect" in params:
            body["interconnect"] = {"type": params["interconnect"]["type"],
                                    "latency_ps": params["interconnect"]["latency"]}
        body["nodes"] = [_node(topology, child) for child in node.children]
    elif node.kind == MEMORY:
        body.update(type=params["type"], capacity_bytes=params["capacity"], channels=params["channels"])
    elif node.kind == CORE:
        body.update({key: value for key, value in params.items() if key != "clock"})
    else:
        body["machine"] = topology.machine(node)
        if node.kind == CACHE:
            hierarchy = topology.hierarchy
            body.update(manager=hierarchy[hierarchy.index(node) + 1].name, capacity_bytes=params["capacity"],
                        associativity=params["associativity"])
        body.update(slices=node.slices, link_latency_ps=params["link_latency"])
        if node.placement is not None:
            body["placement"] = node.placement.name
        if "transitions_per_cycle" in params:
            body["transitions_per_cycle"] = params["transitions_per_cycle"]
    return body
