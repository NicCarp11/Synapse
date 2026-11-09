"""Topology specifications: the third input of Synapse, next to the protocols and the policies.

A topology is a YAML document that describes the system as a tree of clusters (Sec. VI-A of the
paper). This is specs/topologies/smp.yaml:

    system: SMP                         # the scenario, the last part of the system's name

    socket:                             # the root cluster, called by its name
      nodes:                            # listed from the memory to the cores
        - memory: {capacity: 8GiB}
        - directory: {protocol: MESI}
        - LLC: {protocol: MESI, policy: WB_INCL, capacity: 2MiB}
        - core:
            count: 8
            nodes:                      # the private caches of each core
              - L1: {capacity: 64KiB}
      interconnect: {connects: [directory, LLC, core], type: crossbar, latency: 5ns}

A node is the `memory`, the `directory`, a `core`, a cluster (a name with `nodes`) or a cache (any
other name). `count` replicates a cluster or the core, so a node exists once per instance of every
cluster around it. A cluster without count and interconnect only groups nodes (a memory pool). A
cache with `shared: true` is one cache for all the instances of its cluster, a slice of
`capacity` in each; so is a directory in a replicated cluster that does not hold the memory.

The cache controllers, read from the root to the core, form the hierarchy: the directory, then
every cache managed by the controller listed before it. Each controller but the first-level
cache manages the caches below it with its `protocol` (specs/protocols/<protocol>.pcc); the
caches between the first-level cache and the directory are synthesized from the protocol they
manage, the protocol of their parent and their `policy` (Alg. 1).

The system is named after its protocols, from the first-level cache up, its policies and its
scenario (MESI_MESI_WB_INCL_SMP), unless the topology gives a `name`.
"""

import re
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple

import yaml

SIMULATORS = ("gem5-v23", "alloy-gem5-v20")
CORE_TYPES = ("O3CPU", "TimingSimpleCPU")     # the x86 cores of gem5 that work with Ruby
_O3_KNOBS = ("rob_entries", "load_queue_entries", "store_queue_entries", "issue_queue_entries",
             "branch_predictor", "btb_entries")
INTERCONNECT_TYPES = ("crossbar", "star", "direct", "ring")
SLICES_INTERLEAVED = "interleaved"
SLICES_RANGE = "range"
STALL_RECYCLE = "recycle"
STALL_PARK = "park"
CORE, MEMORY, DIRECTORY, CACHE, CLUSTER = "core", "memory", "directory", "cache", "cluster"

_SIZE_UNITS = {"B": 1, "KiB": 2 ** 10, "MiB": 2 ** 20, "GiB": 2 ** 30}
_TIME_UNITS = {"ps": 1, "ns": 10 ** 3, "us": 10 ** 6}
_FREQUENCY_UNITS = {"Hz": 1, "kHz": 10 ** 3, "MHz": 10 ** 6, "GHz": 10 ** 9}

# Parameters of each kind of node: name -> how its value is checked. A unit table means a
# quantity (stored in the table's base unit: bytes, picoseconds, hertz), a tuple the allowed
# words, a type a plain value.
_SCHEMAS = {
    CORE: {
        "type": CORE_TYPES,
        "clock": _FREQUENCY_UNITS,     # of the whole system: cores, caches and network
        # of an out-of-order core (gem5's defaults if not given)
        "rob_entries": int,
        "load_queue_entries": int,
        "store_queue_entries": int,
        "issue_queue_entries": int,
        "branch_predictor": str,       # a branch predictor of gem5 (LTAGE, TournamentBP, ...)
        "btb_entries": int,            # of the branch predictor's target buffer
    },
    MEMORY: {"type": str, "capacity": _SIZE_UNITS, "channels": int},
    DIRECTORY: {
        "protocol": str,            # the protocol the directory manages the caches below it with
        "slices": int,              # the directory is split into this many slices by address
        "link_latency": _TIME_UNITS,    # of the link between the controller and the network
    },
    CACHE: {
        "protocol": str,            # the protocol the cache manages the caches below it with
        "policy": str,              # of a cache between two protocols
        "capacity": _SIZE_UNITS,    # of the cache (a first-level cache: of each of its two caches)
        "associativity": int,
        "slices": int,
        "slice_select": (SLICES_INTERLEAVED, SLICES_RANGE),
        "shared": bool,             # one cache for all the instances of its cluster, a slice in each
        "stalled_requests": (STALL_RECYCLE, STALL_PARK),
        "transitions_per_cycle": int,
        "link_latency": _TIME_UNITS,
    },
}
_DEFAULTS = {
    CORE: {"type": "O3CPU", "clock": "2GHz"},
    MEMORY: {"type": "DDR5_4400_4x8", "channels": 1},
    DIRECTORY: {"slices": 1, "link_latency": "5ns"},
    CACHE: {"associativity": 8, "slices": 1, "slice_select": SLICES_INTERLEAVED,
            "stalled_requests": STALL_RECYCLE, "link_latency": "5ns"},
}
_REQUIRED = {MEMORY: ("capacity",), DIRECTORY: ("protocol",), CACHE: ("capacity",)}
_INTERCONNECT = {"type": INTERCONNECT_TYPES, "latency": _TIME_UNITS, "flit_size": _SIZE_UNITS}
_FLIT_SIZE = "256B"     # of the root interconnect; an interconnect inside takes the one around it
_CLUSTER_KEYS = ("count", "interconnect", "nodes")
_TOP_KEYS = ("name", "system", "simulator")
# quantities carry their base unit in the resolved description (Topology.resolved)
_RESOLVED_NAMES = {"capacity": "capacity_bytes", "flit_size": "flit_size_bytes", "latency": "latency_ps",
                   "link_latency": "link_latency_ps", "clock": "clock_hz"}
_NAME = re.compile(r"[A-Za-z][A-Za-z0-9_]*")
_POLICY_DECLARATION = re.compile(r"^\s*Policy\s+(\w+)\s*\{", re.MULTILINE)


class TopologyError(Exception):
    """The topology is malformed, or describes a system the generator cannot build."""


class Node:
    """A node of the cluster tree: a core, the memory, the directory, a cache or a cluster."""

    def __init__(self, kind: str, name: str, params: Dict[str, Any], parent: Optional["Node"]):
        self.kind = kind
        self.name = name
        self.params = params
        self.parent = parent
        self.children: List["Node"] = []    # of a cluster
        self.given: set = set()             # the parameters the topology writes (not defaults)
        self.protocol: Optional[Path] = None    # of a controller: the protocol it manages
        self.policy: Optional[Tuple[Path, str]] = None  # of a synthesized controller: (file, name)

    def __repr__(self):
        return f"{self.kind} {self.name}"

    @property
    def is_controller(self) -> bool:
        return self.kind in (DIRECTORY, CACHE)

    @property
    def instances(self) -> int:
        """How many times the node exists in the system (slices not counted)."""
        count = self.params.get("count", 1) if self.kind == CLUSTER else 1
        return count * (self.parent.instances if self.parent else 1)

    def walk(self) -> Iterator["Node"]:
        yield self
        for child in self.children:
            yield from child.walk()

    # --- controllers ---
    @property
    def slices(self) -> int:
        return self.params.get("slices", 1)

    @property
    def slice_select(self) -> str:
        return self.params.get("slice_select", SLICES_INTERLEAVED)

    @property
    def stalled_requests(self) -> str:
        return self.params.get("stalled_requests", STALL_RECYCLE)

    @property
    def placement(self) -> Optional["Node"]:
        """The cluster whose instances hold the slices, one each (resolved by Topology)."""
        return getattr(self, "_placement", None)


class Topology:
    """A validated topology with its coherence hierarchy resolved.

    hierarchy   the cache controllers from the first-level cache to the directory
    """

    def __init__(self, document: Any, source: Path, protocol_dirs: Sequence[Path] = (),
                 policy_dirs: Sequence[Path] = ()):
        self.source = source
        self._protocol_dirs = [source.parent, *protocol_dirs]
        self._policy_dirs = [source.parent, *policy_dirs]
        if not isinstance(document, dict):
            raise TopologyError(f"{source}: a topology is a mapping: {', '.join(_TOP_KEYS)} and the root cluster")
        roots = [key for key in document if key not in _TOP_KEYS]
        if len(roots) != 1:
            raise TopologyError(f"a topology has one root cluster next to {', '.join(_TOP_KEYS)}; found "
                                f"{', '.join(map(str, roots)) or 'none'}")
        self.system: Optional[str] = None
        if "system" in document:
            self.system = _check_name(_check_value(document["system"], str, "system"), "system")
        self.simulator: str = _check_value(document.get("simulator", SIMULATORS[0]), SIMULATORS, "simulator")
        self._names: Dict[str, Node] = {}
        root_name, root_body = roots[0], document[roots[0]]
        if not isinstance(root_body, dict) or "nodes" not in root_body:
            raise TopologyError(f"{root_name}: the root cluster is a mapping with nodes")
        self.root = self._build_cluster(str(root_name), root_body, None)
        self._regroup()
        if "interconnect" not in self.root.params:
            raise TopologyError(f"{self.root.name}: the root cluster needs an interconnect")
        self.hierarchy: List[Node] = self._resolve_hierarchy()
        self._resolve_protocols()
        self._resolve_placements()
        self._check_generator_limits()
        self._check_simulation()
        if "name" in document:
            self.name = _check_name(_check_value(document["name"], str, "name"), "name")
        else:
            self.name = "_".join([path.stem for path in self.protocol_chain()]
                                 + list(dict.fromkeys(name for _, name in self.policy_chain()))
                                 + ([self.system] if self.system else []))
            _check_name(self.name, "the name made of the protocols, the policies and system")

    # --- construction ---
    def _build_cluster(self, name: str, body: Dict[str, Any], parent: Optional[Node]) -> Node:
        _check_keys(body, _CLUSTER_KEYS, name, required=("nodes",))
        params: Dict[str, Any] = {}
        if "count" in body:
            params["count"] = _check_value(body["count"], int, f"{name}: count")
        connects = None
        if "interconnect" in body:
            written = dict(_mapping(body["interconnect"], f"{name}: interconnect"))
            connects = written.pop("connects", None)
            interconnect = _check_params(written, _INTERCONNECT, f"{name}: interconnect",
                                         required=("type", "latency"))
            outer = _enclosing_interconnect(parent)
            interconnect.setdefault("flit_size", outer["flit_size"] if outer else
                                    _check_value(_FLIT_SIZE, _SIZE_UNITS, "flit_size"))
            params["interconnect"] = interconnect
        cluster = self._add_node(CLUSTER, name, params, parent)
        if not isinstance(body["nodes"], list) or not body["nodes"]:
            raise TopologyError(f"{name}: nodes is a non-empty list")
        for item in body["nodes"]:
            if isinstance(item, str):
                node_name, node_body = item, None
            elif isinstance(item, dict) and len(item) == 1:
                (node_name, node_body), = item.items()
                node_name = str(node_name)
            else:
                raise TopologyError(f"{name}: every node is written `- NAME: {{parameters}}` "
                                    f"(or `- core`), not {item!r}")
            if node_name == CORE and isinstance(node_body, dict) and \
                    any(key in node_body for key in _CLUSTER_KEYS):
                self._build_core_cluster(node_body, cluster)
                continue
            if node_name in (CORE, MEMORY, DIRECTORY):
                kind = node_name
            elif isinstance(node_body, dict) and "nodes" in node_body:
                self._build_cluster(node_name, node_body, cluster)
                continue
            else:
                kind = CACHE
            if node_body is None and kind == CACHE:
                raise TopologyError(f"{name}: `- {node_name}` is a cache: give it its parameters "
                                    f"(`- {node_name}: {{capacity: ...}}`), or nodes if it is a cluster")
            where = f"{name}: {node_name}"
            params = _check_params(node_body or {}, _SCHEMAS[kind], where, required=_REQUIRED.get(kind, ()))
            given = set(params)
            for key, value in _DEFAULTS[kind].items():
                params.setdefault(key, _check_value(value, _SCHEMAS[kind][key], f"{where}: {key}"))
            self._add_node(kind, node_name, params, cluster).given = given
        if connects is not None:
            # what the interconnect links, as the topology names it: every node of the cluster that
            # reaches the network (a controller or a cluster)
            linked = [getattr(child, "written_name", child.name) for child in cluster.children
                      if child.kind in (CLUSTER, DIRECTORY, CACHE)]
            if not isinstance(connects, list) or sorted(map(str, connects)) != sorted(linked):
                raise TopologyError(f"{name}: the interconnect connects the nodes of {name}: "
                                    f"connects: [{', '.join(linked)}]")
        return cluster

    def _build_core_cluster(self, body: Dict[str, Any], parent: Node):
        """`- core: {count: N, nodes: [private caches]}`: the cluster `cores` of N cores, each
        with its private caches; the other keys are the core's parameters."""
        cluster_body = {key: body[key] for key in _CLUSTER_KEYS if key in body}
        if len(cluster_body.get("nodes", [])) > 1 and "interconnect" not in cluster_body:
            cluster_body["interconnect"] = {"type": "direct", "latency": "0ns"}    # private caches: linked directly
        core_params = {key: value for key, value in body.items() if key not in _CLUSTER_KEYS}
        cluster_body["nodes"] = [*cluster_body.get("nodes", []), {CORE: core_params} if core_params else CORE]
        self._build_cluster(f"{CORE}s", cluster_body, parent).written_name = CORE

    def _regroup(self):
        """The written tree in the shape the generator works on: a group gives its nodes to the
        cluster around it; a shared cache, and a directory replicated away from the memory, become
        one controller of the cluster around theirs with a slice in each instance (`placement`)."""
        on_the_way = set(_ancestors(self._names[CORE])) if CORE in self._names else set()
        for group in [node for node in self.root.walk() if node.kind == CLUSTER and node is not self.root
                      and node not in on_the_way and not {"count", "interconnect"} & set(node.params)]:
            siblings = group.parent.children
            index = siblings.index(group)
            for child in group.children:
                child.parent = group.parent
            siblings[index:index + 1] = group.children
            del self._names[group.name]
        memory = self._names.get(MEMORY)
        for node in list(self.root.walk()):
            cluster = node.parent
            if node.kind == CACHE and node.params.pop("shared", False):
                if cluster.params.get("count", 1) < 2:
                    raise TopologyError(f"{node.name}: shared by the instances of {cluster.name}, which has no count")
            elif not (node.kind == DIRECTORY and memory is not None and memory.parent is not cluster
                      and cluster.params.get("count", 1) > 1):
                continue
            if "slices" in node.given:
                raise TopologyError(f"{node.name}: one slice in each {cluster.name}: no slices")
            count = cluster.params["count"]
            node.params.update(slices=count, placement=cluster.name)
            if "capacity" in node.params:
                node.params["capacity"] *= count
            cluster.children.remove(node)
            outer = cluster.parent.children
            outer.insert(outer.index(cluster), node)
            node.parent = cluster.parent

    def _add_node(self, kind: str, name: str, params: Dict[str, Any], parent: Optional[Node]) -> Node:
        _check_name(name, "a node")
        if name in self._names:
            raise TopologyError(f"two nodes are called '{name}': names identify the nodes (--set NAME.KEY=VALUE); "
                                "a topology has one core, one memory and one directory, replicated with count")
        node = Node(kind, name, params, parent)
        self._names[name] = node
        if parent is not None:
            parent.children.append(node)
        return node

    def _resolve_hierarchy(self) -> List[Node]:
        """The controllers on the way from the root to the core, read in the order of the nodes."""
        for kind in (CORE, MEMORY, DIRECTORY):
            if kind not in self._names:
                raise TopologyError(f"the topology has no {kind}")
        core = self._names[CORE]
        path = []
        node = core
        while node.parent is not None:
            path.insert(0, node)
            node = node.parent
        chain: List[Node] = []
        cluster = self.root
        for step in path:
            position = cluster.children.index(step)
            for child in cluster.children[:position]:
                if child.kind == CLUSTER:
                    if child.params.get("count", 1) != 1:
                        raise TopologyError(f"{child.name} is beside the way to the core: it takes no count")
                    chain += [node for node in child.walk() if node.is_controller]
                elif child.is_controller:
                    chain.append(child)
            later = cluster.children[position + 1:]
            if later:
                raise TopologyError(f"{cluster.name}: list the nodes from the memory to the cores; "
                                    f"{', '.join(child.name for child in later)} comes after {step.name}")
            cluster = step
        outside = [node.name for node in self.root.walk() if node.is_controller and node not in chain]
        if outside:
            raise TopologyError(f"not on the way from the root to the core: {', '.join(outside)} (the hierarchy "
                                "is one chain of controllers, each in a cluster around the core)")
        if chain[0].kind != DIRECTORY:
            raise TopologyError(f"the first controller from the root must be the directory, not {chain[0].name}")
        memory, directory = self._names[MEMORY], self._names[DIRECTORY]
        if memory.parent is not directory.parent:
            raise TopologyError(f"the memory must be in the cluster of the directory ({directory.parent.name})")
        return chain[::-1]

    def _resolve_protocols(self):
        first, directory = self.hierarchy[0], self.hierarchy[-1]
        for controller in self.hierarchy:
            given = controller.params.get("protocol")
            if controller is first:
                if given is not None or "policy" in controller.params:
                    raise TopologyError(
                        f"{first.name} is the first-level cache: it manages no cache, so it has no protocol "
                        f"and no policy; it speaks the protocol of {self.hierarchy[1].name}")
                continue
            if given is None:
                raise TopologyError(f"{controller.name} manages {self._below(controller).name}: give the "
                                    "protocol it manages it with (protocol: MESI)")
            controller.protocol = _find_file(given if Path(given).suffix else f"{given}.pcc",
                                             self._protocol_dirs, f"{controller.name}: protocol")
            if controller is directory:
                continue
            if "policy" not in controller.params:
                raise TopologyError(f"{controller.name} is between two protocols: give its policy (policy: WB_INCL)")
            controller.policy = _find_policy(controller.params["policy"], self._policy_dirs,
                                             f"{controller.name}: policy")

    def _resolve_placements(self):
        for controller in self.hierarchy:
            name = controller.params.get("placement")
            if name is None:
                continue
            cluster = self._names.get(name)
            inside = [node for node in controller.parent.walk() if node.kind == CLUSTER][1:]
            if cluster not in inside:
                raise TopologyError(f"{controller.name}: placement: {name} is not a cluster inside "
                                    f"{controller.parent.name}")
            instances = cluster.instances // controller.parent.instances
            if controller.slices != instances:
                raise TopologyError(f"{controller.name}: placement: {name} has {instances} instances in each "
                                    f"{controller.parent.name}, one per slice: give slices: {instances}")
            controller._placement = cluster

    def _below(self, controller: Node) -> Node:
        return self.hierarchy[self.hierarchy.index(controller) - 1]

    def _check_generator_limits(self):
        """What the synthesis and the SLICC back end support today, reported before they run."""
        first, intermediates = self.hierarchy[0], self.intermediates
        if not intermediates:
            raise TopologyError("the hierarchy has no cache between the first-level cache and the directory: "
                                "there is nothing to synthesize (they are the input protocol itself)")
        if first.parent is not self._names[CORE].parent:
            raise TopologyError(f"the first-level cache {first.name} must be in the cluster of the core")
        if first.slices != 1:
            raise TopologyError(f"the first-level cache {first.name} cannot be split into slices")
        for controller in intermediates[1:]:
            if controller.slices != 1:
                raise TopologyError(f"{controller.name}: only the parent of the first-level cache can be split "
                                    "into slices")
        if intermediates[0].slice_select == SLICES_RANGE and self.simulator != "alloy-gem5-v20":
            raise TopologyError(f"{intermediates[0].name}: slices that own address ranges need "
                                "simulator: alloy-gem5-v20")
        for controller in self.hierarchy:
            if controller.slices & (controller.slices - 1):
                raise TopologyError(f"{controller.name}: slices must be a power of two")
        if len({controller.stalled_requests for controller in intermediates}) > 1:
            raise TopologyError("stalled_requests must be the same for all the synthesized controllers")
        for cluster in self.root.walk():
            if cluster.kind == CLUSTER and cluster.params.get("interconnect", {}).get("type") == "ring":
                for child in cluster.children:
                    if child.kind != CLUSTER or \
                            child.params.get("interconnect", {}).get("type") not in ("crossbar", "star"):
                        raise TopologyError(f"{cluster.name}: a ring links the switches of its clusters: "
                                            f"{child.name} must be a cluster with a crossbar or a star")

    def _check_simulation(self):
        """What the simulation setup of the topology's simulator can build."""
        core = self._names[CORE]
        knobs = [key for key in _O3_KNOBS if key in core.params]
        if knobs and core.params["type"] != "O3CPU":
            raise TopologyError(f"core: {', '.join(knobs)} " + ("is a parameter" if len(knobs) == 1 else "are parameters")
                                + " of an O3CPU core")
        if "btb_entries" in core.params and "branch_predictor" not in core.params:
            raise TopologyError("core: btb_entries is a parameter of the branch_predictor: give it too")
        clock = core.params["clock"]
        interconnects = [(node, node.params["interconnect"]) for node in self.root.walk()
                         if node.kind == CLUSTER and "interconnect" in node.params]
        latencies = [(f"{node.name}: interconnect latency", interconnect["latency"])
                     for node, interconnect in interconnects]
        latencies += [(f"{node.name}: link_latency", node.params["link_latency"])
                      for node in self.hierarchy]
        for where, latency in latencies:
            if latency * clock % 10 ** 12:
                raise TopologyError(f"{where}: {latency / 1000:g}ns is not a whole number of cycles at "
                                    f"{clock / 10 ** 9:g}GHz, the clock of the system")
        for node, interconnect in interconnects:
            if interconnect["flit_size"] != self.root.params["interconnect"]["flit_size"]:
                raise TopologyError(f"{node.name}: gem5 has one flit size for the whole network: the "
                                    f"one of {self.root.name}")
        memory, directory = self._names[MEMORY], self._names[DIRECTORY]
        if directory.slices != memory.params["channels"]:
            raise TopologyError(f"the directory has {directory.slices} slices and the memory "
                                f"{memory.params['channels']} channels: each slice manages one channel")
        if self.simulator == "alloy-gem5-v20":
            self._check_alloy()

    def _check_alloy(self):
        """alloy-gem5 runs the system with its own configuration (sc3.py) and network (TwoMeshXY):
        two cache levels; the slices of the LLC and of the directory placed one per instance of a
        cluster (the chiplets) whose star links the L1s inside it; a star linking the chiplets."""
        def refuse(reason: str):
            raise TopologyError(f"alloy-gem5 (sc3.py, TwoMeshXY): {reason}")

        if len(self.hierarchy) != 3:
            refuse("the hierarchy has two cache levels, an L1 and an LLC")
        first, last_level, directory = self.hierarchy
        knobs = [key for key in _O3_KNOBS if key in self._names[CORE].params]
        if knobs:
            refuse(f"no core parameter {', '.join(knobs)}")
        if last_level.slice_select != SLICES_RANGE or last_level.slices < 2:
            refuse(f"{last_level.name} is shared by the chiplets, a slice in each that owns an address range "
                   "(shared: true, slice_select: range)")
        chiplet = last_level.placement
        if chiplet is None or directory.placement is not chiplet or directory.slices != last_level.slices:
            refuse(f"{last_level.name} and {directory.name} have a slice in each chiplet: write both in the "
                   f"chiplet cluster, {last_level.name} with shared: true, and the memory outside it")
        outer = _enclosing_interconnect(chiplet.parent)
        if chiplet.params.get("interconnect", {}).get("type") != "star" or outer is None or outer["type"] != "star":
            refuse(f"{chiplet.name} and the cluster around it have a star interconnect")
        if chiplet not in self._clusters_of_core() or any(
                "interconnect" in node.params for node in self._clusters_of_core()
                if node is not chiplet and chiplet in _ancestors(node)):
            refuse(f"the cores are inside {chiplet.name}, in clusters without an interconnect of their own")
        latency = chiplet.params["interconnect"]["latency"]
        for controller in self.hierarchy:
            if "link_latency" in controller.given and controller.params["link_latency"] != latency:
                refuse(f"{controller.name}: every controller is linked with the latency of {chiplet.name}'s "
                       f"interconnect ({latency / 1000:g}ns)")

    # --- the resolved system ---
    @property
    def intermediates(self) -> List[Node]:
        """The controllers that are synthesized: managers of one protocol and clients of the next."""
        return self.hierarchy[1:-1]

    def machine(self, controller: Node) -> str:
        """Name of the controller's machine in the generated SLICC."""
        index = self.hierarchy.index(controller)
        return "Directory" if index == len(self.hierarchy) - 1 else f"L{index + 1}Cache"

    def protocol_chain(self) -> List[Path]:
        """The protocol files from the first-level cache's to the directory's."""
        return [controller.protocol for controller in self.hierarchy[1:]]

    def policy_chain(self) -> List[Tuple[Path, str]]:
        """(file, policy name) of each synthesized controller, from the lowest."""
        return [controller.policy for controller in self.intermediates]

    @property
    def cores(self) -> int:
        return self._names[CORE].instances

    def describe(self) -> List[str]:
        """The resolved system in a few lines, for the command line."""
        levels = []
        for index, controller in enumerate(self.hierarchy):
            above = self.hierarchy[index + 1].protocol.stem if controller is not self.hierarchy[-1] else None
            if controller in self.intermediates:
                roles = f"{controller.protocol.stem} x {above}, policy {controller.policy[1]}"
            else:
                roles = above or controller.protocol.stem
            count = controller.instances * controller.slices
            sliced = ""
            if controller.slices > 1:
                how = "interleaved by address" if controller.slice_select == SLICES_INTERLEAVED else \
                    "by address range"
                sliced = f", {controller.slices} slices {how}"
                if controller.placement is not None:
                    sliced += f", one in each {controller.placement.name}"
            parked = ", parks stalled requests" if controller in self.intermediates and \
                controller.stalled_requests == STALL_PARK else ""
            levels.append(f"{self.machine(controller):<11} {controller.name:<10} x{count:<4} {roles}{sliced}{parked}")
        shape = " x ".join(f"{node.params['count']} {node.name}" for node in self._clusters_of_core()
                           if node.params.get("count", 1) > 1)
        return [f"system      {self.name} ({self.source.name}), {self.simulator}",
                f"cores       {self.cores}" + (f" ({shape})" if shape else ""),
                *levels]

    def _clusters_of_core(self) -> List[Node]:
        """The clusters around the core, from the root."""
        node, path = self._names[CORE].parent, []
        while node is not None:
            path.insert(0, node)
            node = node.parent
        return path

    def resolved(self) -> Dict[str, Any]:
        """The system as plain data (written next to the generated controllers): every quantity in
        its base unit, the hierarchy with the machine names of the generated SLICC."""
        def hierarchy_entry(index: int, controller: Node) -> Dict[str, Any]:
            parent = self.hierarchy[index + 1] if controller is not self.hierarchy[-1] else None
            return {"controller": controller.name, "machine": self.machine(controller),
                    "manages_with": _shown(controller.protocol) if controller.protocol else None,
                    "client_of": _shown(parent.protocol) if parent else None,
                    "policy": {"file": _shown(controller.policy[0]), "policy": controller.policy[1]}
                    if controller.policy else None,
                    "instances": controller.instances, "slices": controller.slices}

        return {
            "name": self.name,
            "system": self.system,
            "simulator": self.simulator,
            "source": _shown(self.source),
            "cores": self.cores,
            "hierarchy": [hierarchy_entry(index, controller) for index, controller in enumerate(self.hierarchy)],
            "root": self._resolved_node(self.root),
        }

    def _resolved_node(self, node: Node) -> Dict[str, Any]:
        def with_units(params: Dict[str, Any]) -> Dict[str, Any]:
            return {_RESOLVED_NAMES.get(key, key): with_units(value) if isinstance(value, dict) else value
                    for key, value in params.items()}

        body: Dict[str, Any] = {"kind": node.kind, "name": node.name, **with_units(node.params)}
        if node.kind == CLUSTER:
            body["nodes"] = [self._resolved_node(child) for child in node.children]
        return body


def load_topology(path: Path, overrides: Sequence[str] = (), protocol_dirs: Sequence[Path] = (),
                  policy_dirs: Sequence[Path] = ()) -> Topology:
    """Reads a topology file. `overrides` are `KEY=VALUE` assignments applied to the document
    first: KEY is `name`, `system`, `simulator`, or `NODE.PARAMETER` with the name of a node (e.g.
    `directory.protocol=MOESI`, `LLC.policy=WB_EXCL`, `core.count=16`,
    `socket.interconnect.latency=10ns`). Protocols and policies are looked up next to the topology,
    then in `protocol_dirs` / `policy_dirs`."""
    path = Path(path).resolve()
    try:
        document = yaml.safe_load(path.read_text())
    except (OSError, yaml.YAMLError) as error:
        raise TopologyError(f"cannot read {path}: {error}") from error
    for assignment in overrides:
        _apply_override(document, assignment)
    return Topology(document, path, protocol_dirs, policy_dirs)


def _apply_override(document: Any, assignment: str):
    key, separator, text = assignment.partition("=")
    if not separator or not key:
        raise TopologyError(f"--set {assignment}: expected KEY=VALUE")
    try:
        value = yaml.safe_load(text)
    except yaml.YAMLError as error:
        raise TopologyError(f"--set {assignment}: {error}") from error
    if not isinstance(document, dict):
        raise TopologyError(f"--set {assignment}: the topology is not a mapping")
    if key in _TOP_KEYS:
        document[key] = value
        return
    head, *path = key.split(".")
    target = _node_body(document, head)
    if target is None:
        raise TopologyError(f"--set {assignment}: '{head}' is neither {', '.join(_TOP_KEYS)} nor the name of a node")
    if not path:
        raise TopologyError(f"--set {assignment}: which parameter of {head}?")
    for step in path[:-1]:
        target = target.setdefault(step, {})
        if not isinstance(target, dict):
            raise TopologyError(f"--set {assignment}: {step} is not a mapping")
    target[path[-1]] = value


def _node_body(document: Dict[str, Any], name: str) -> Optional[Dict[str, Any]]:
    """The mapping of the node called `name` in the raw document, created if the node is written
    without parameters (`- core`)."""
    def search(container: Any, key: Any) -> Optional[Dict[str, Any]]:
        body = container[key]
        if isinstance(body, str):                   # `- core` in a list of nodes
            if body != name:
                return None
            container[key] = {name: {}}
            return container[key][name]
        if isinstance(body, dict) and len(body) == 1 and container is not document:
            (node_name, node_body), = body.items()
            if node_name == name:
                if node_body is None:
                    body[node_name] = node_body = {}
                return node_body if isinstance(node_body, dict) else None
            body = node_body
        if isinstance(body, dict) and isinstance(body.get("nodes"), list):
            for index in range(len(body["nodes"])):
                found = search(body["nodes"], index)
                if found is not None:
                    return found
        return None

    for key in document:
        if key in _TOP_KEYS:
            continue
        if key == name:
            return document[key] if isinstance(document[key], dict) else None
        found = search(document, key)
        if found is not None:
            return found
    return None


def _ancestors(node: Node) -> List[Node]:
    result = []
    while node.parent is not None:
        node = node.parent
        result.append(node)
    return result


def _shown(path: Path) -> str:
    """A path as the user gave it: relative to the working directory when it is inside it."""
    try:
        return str(Path(path).relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def _enclosing_interconnect(cluster: Optional[Node]) -> Optional[Dict[str, Any]]:
    while cluster is not None:
        if "interconnect" in cluster.params:
            return cluster.params["interconnect"]
        cluster = cluster.parent
    return None


def _check_name(name: str, what: str) -> str:
    if not _NAME.fullmatch(name):
        raise TopologyError(f"{what}: '{name}' names generated files and gem5 objects: letters, digits and "
                            "underscores only")
    return name


def _mapping(value: Any, where: str) -> Dict[str, Any]:
    if not isinstance(value, dict):
        raise TopologyError(f"{where}: expected a mapping, not {value!r}")
    return value


def _check_keys(body: Dict[str, Any], allowed: Sequence[str], where: str, required: Sequence[str] = ()):
    unknown = [key for key in body if key not in allowed]
    if unknown:
        raise TopologyError(f"{where}: unknown key {', '.join(map(str, unknown))} (known: {', '.join(allowed)})")
    missing = [key for key in required if key not in body]
    if missing:
        raise TopologyError(f"{where}: missing {', '.join(missing)}")


def _check_params(body: Any, schema: Dict[str, Any], where: str, required: Sequence[str] = ()) -> Dict[str, Any]:
    _check_keys(_mapping(body, where), tuple(schema), where, required)
    return {key: _check_value(value, schema[key], f"{where}: {key}") for key, value in body.items()}


def _check_value(value: Any, expected: Any, where: str) -> Any:
    if isinstance(expected, dict):      # a quantity with a unit
        match = re.fullmatch(r"(\d+(?:\.\d+)?)\s*([A-Za-z]+)", str(value).strip())
        if not match or match.group(2) not in expected:
            raise TopologyError(f"{where}: '{value}' is not a number with a unit ({', '.join(expected)})")
        amount = float(match.group(1)) * expected[match.group(2)]
        if amount != int(amount):
            raise TopologyError(f"{where}: '{value}' is not a whole number of {next(iter(expected))}")
        return int(amount)
    if isinstance(expected, tuple):     # one of a few words
        if value not in expected:
            raise TopologyError(f"{where}: '{value}' is not one of {', '.join(expected)}")
        return value
    if expected is bool:
        if not isinstance(value, bool):
            raise TopologyError(f"{where}: expected true or false, not {value!r}")
        return value
    if expected is int:
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise TopologyError(f"{where}: '{value}' is not a positive integer")
        return value
    if not isinstance(value, str) or not value:
        raise TopologyError(f"{where}: expected a name, not {value!r}")
    return value


def _find_file(filename: str, directories: Sequence[Path], where: str) -> Path:
    candidates = [Path(filename)] if Path(filename).is_absolute() else \
        [Path(directory) / filename for directory in directories]
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise TopologyError(f"{where}: {filename} not found in {', '.join(str(c.parent) for c in candidates)}")


def _find_policy(reference: str, directories: Sequence[Path], where: str) -> Tuple[Path, str]:
    """A policy by name (WB_INCL: the policy files are searched for it), by file and name
    (caching.pol:WB_INCL), or by file (the only policy of the file)."""
    filename, separator, name = reference.partition(":")
    if separator or filename.endswith(".pol"):
        path = _find_file(filename, directories, where)
        declared = _POLICY_DECLARATION.findall(path.read_text())
        if not name:
            if len(declared) != 1:
                raise TopologyError(f"{where}: {path.name} defines {', '.join(declared)}: write {filename}:NAME")
            name = declared[0]
        if name not in declared:
            raise TopologyError(f"{where}: {path.name} has no policy {name} ({', '.join(declared)})")
        return path, name
    for directory in directories:
        found = [path for path in sorted(Path(directory).glob("*.pol"))
                 if reference in _POLICY_DECLARATION.findall(path.read_text())]
        if len(found) > 1:
            raise TopologyError(f"{where}: {', '.join(path.name for path in found)} all define {reference}: "
                                f"write FILE:{reference}")
        if found:
            return found[0].resolve(), reference
    raise TopologyError(f"{where}: no policy file defines {reference} (in {', '.join(map(str, directories))})")
