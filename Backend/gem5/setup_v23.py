"""The gem5 v23 configuration Synapse writes next to the controllers of a system.

Synapse fills SYSTEM below with the system its topology resolves to and writes the result as
<name>_gem5.py; the rest of this file builds that system in gem5 around the generated controllers
and runs a program on it in syscall-emulation mode.
"""

# The system, from the topology: quantities in bytes, picoseconds and hertz; every controller
# with the machine of its generated SLICC and the controller that manages it.
SYSTEM = {}

import argparse
import math
import os
import sys

BLOCK_BYTES = 64                    # gem5's cache line
# the message buffers of a controller that are not connected to the network
LOCAL_BUFFERS = ("mandatoryQueue", "requestToMemory", "responseFromMemory")
SWITCHED = ("crossbar", "star")     # the interconnects with a switch of their own


# ----------------------------------------------------------------------------------------------
# The plan: every instance of every node, the routers and the links, without gem5 objects
# ----------------------------------------------------------------------------------------------

class Instance:
    """One instance of a node: of a cluster, of the memory, of a core or of a controller."""

    def __init__(self, node, cluster, index):
        self.node = node                # the node of SYSTEM
        self.cluster = cluster          # the instance of the cluster around it (None: the root)
        self.index = index              # among the instances of the node, in the order of the tree
        self.children = []              # of a cluster
        self.switch = None              # of a cluster with a crossbar or a star: its router
        self.endpoints = []             # of a controller: one per slice

    @property
    def kind(self):
        return self.node["kind"]

    @property
    def interconnect(self):
        return self.node.get("interconnect") if self.kind == "cluster" else None

    def ancestors(self):
        """The cluster instances around this one, from the nearest."""
        cluster = self.cluster
        while cluster is not None:
            yield cluster
            cluster = cluster.cluster

    def network(self):
        """The nearest cluster instance around this one with an interconnect."""
        return next((cluster for cluster in self.ancestors() if cluster.interconnect), None)

    def walk(self):
        yield self
        for child in self.children:
            yield from child.walk()


class Endpoint:
    """A slice of a controller instance: one controller in gem5, with its router."""

    def __init__(self, instance, slice_index, version):
        self.instance = instance
        self.slice = slice_index
        self.version = version          # among the controllers of its machine
        self.site = None                # with a placement: the cluster instance the slice sits in
        self.router = None
        self.managers = []              # the endpoints of its manager that it talks to
        # the blocks it can hold: line number = residue (modulo modulus); the slices and the
        # memory units are interleaved by cache line
        self.modulus, self.residue = instance.node["slices"], slice_index

    @property
    def node(self):
        return self.instance.node

    def ancestors(self):
        """The cluster instances around the slice, from the nearest: those of its site, if placed."""
        if self.site is None:
            return self.instance.ancestors()
        return [self.site] + list(self.site.ancestors())

    def network(self):
        return next((cluster for cluster in self.ancestors() if cluster.interconnect), None)

    def shares_blocks_with(self, other):
        common = min(self.modulus, other.modulus)
        return self.residue % common == other.residue % common

    def __str__(self):
        name = f"{self.node['name']} {self.instance.index}"
        return name + (f" slice {self.slice}" if self.node["slices"] > 1 else "")


class Plan:
    """The instances, routers and links of SYSTEM with `cores` cores."""

    def __init__(self, system, cores):
        self.system = system
        self.core_path = self._core_path(system["root"])
        self.counters = {}              # node name -> instances so far
        self.versions = {}              # machine -> controllers so far
        self.root = self._instantiate(system["root"], None, cores)
        self.instances = list(self.root.walk())
        self.endpoints = [endpoint for instance in self.instances for endpoint in instance.endpoints]
        self.cores = [instance for instance in self.instances if instance.kind == "core"]

        memories = [instance for instance in self.instances if instance.kind == "memory"]
        self.memory = memories[0].node
        self.memory_units = len(memories) * self.memory["channels"]
        self.memory_bytes = len(memories) * self.memory["capacity_bytes"]
        directories = [endpoint for endpoint in self.endpoints if endpoint.node["kind"] == "directory"]
        if len(directories) != self.memory_units:
            raise SystemExit(f"error: {len(directories)} directory slices for {self.memory_units} memory channels")
        for directory in directories:
            directory.modulus, directory.residue = len(directories), directory.version
        for instance in self.instances:
            if instance.node.get("placement"):
                sites = [site for site in instance.cluster.walk() if site.node["name"] == instance.node["placement"]]
                for endpoint, site in zip(instance.endpoints, sites):
                    endpoint.site = site

        self._find_managers()
        self.routers = []               # what each router serves: an Endpoint or a cluster Instance
        self._create_routers()
        self.links = []                 # (router, router, latency in ps), each used both ways
        self._create_links()
        self._check_routes()

    # --- instances ---
    @staticmethod
    def _core_path(root):
        """The names of the clusters from the root to the one around the core."""
        def search(node, path):
            path = path + [node["name"]]
            for child in node["nodes"]:
                if child["kind"] == "core":
                    return path
                if child["kind"] == "cluster":
                    found = search(child, path)
                    if found:
                        return found
            return None
        return search(root, [])

    def _instantiate(self, node, cluster, cores):
        """The instance of the cluster `node` inside `cluster`, holding `cores` cores."""
        instance = self._new(node, cluster)
        for child in node["nodes"]:
            if child["kind"] == "cluster":
                for share in self._split(child, cores):
                    instance.children.append(self._instantiate(child, instance, share))
                continue
            if child["kind"] == "core" and cores != 1:
                raise SystemExit(f"error: {node['name']} holds one core, not {cores}")
            member = self._new(child, instance)
            if child["kind"] in ("directory", "cache"):
                for slice_index in range(child["slices"]):
                    version = self.versions.get(child["machine"], 0)
                    self.versions[child["machine"]] = version + 1
                    member.endpoints.append(Endpoint(member, slice_index, version))
            instance.children.append(member)
        return instance

    def _new(self, node, cluster):
        index = self.counters.get(node["name"], 0)
        self.counters[node["name"]] = index + 1
        return Instance(node, cluster, index)

    def _split(self, cluster, cores):
        """The cores of each instance of `cluster` inside an instance that holds `cores`: one
        each in the cluster of the core; else consecutive blocks of the same size, the last
        instance taking the rest."""
        if cluster["name"] == self.core_path[-1]:
            return [1] * cores
        if cluster["name"] not in self.core_path:
            return [0] * cluster["count"]
        share = cores // cluster["count"]
        return [share] * (cluster["count"] - 1) + [cores - share * (cluster["count"] - 1)]

    def _find_managers(self):
        """The endpoints each cache talks to: the slices of its manager that can hold its blocks,
        in the instance of the manager's cluster around it (in every instance, for the directory,
        whose instances share the memory)."""
        by_node = {}
        for instance in self.instances:
            by_node.setdefault(instance.node["name"], []).append(instance)
        for endpoint in self.endpoints:
            manager = endpoint.node.get("manager")
            if manager is None:
                continue
            candidates = by_node[manager]
            if manager != self.system["hierarchy"][-1]:
                around = [id(cluster) for cluster in endpoint.instance.ancestors()]
                candidates = [instance for instance in candidates if id(instance.cluster) in around]
            endpoint.managers = [other for instance in candidates for other in instance.endpoints
                                 if endpoint.shares_blocks_with(other)]

    # --- network ---
    def _create_routers(self):
        """One router per endpoint and per switch: the directory's first, then the others in the
        order of the tree, each cluster's switch before its nodes (and the slices placed in it)."""
        for endpoint in self.endpoints:
            if endpoint.node["kind"] == "directory":
                endpoint.router = self._router(endpoint)
        for instance in self.instances:
            if instance.interconnect and instance.interconnect["type"] in SWITCHED:
                instance.switch = self._router(instance)
            placed = [endpoint for endpoint in self.endpoints if endpoint.site is instance]
            for endpoint in placed + [e for e in instance.endpoints if e.site is None]:
                if endpoint.router is None:
                    endpoint.router = self._router(endpoint)

    def _router(self, owner):
        self.routers.append(owner)
        return len(self.routers) - 1

    def _create_links(self):
        """The links each interconnect makes in each instance of its cluster:
            direct    every cache with the slices of its manager that hold its blocks
            star      a switch with every controller and with the clusters inside
            crossbar  a star whose caches are also linked with each other
            ring      the switches of the clusters inside, in a ring
        A cache and its manager are linked by the interconnect of the nearest cluster around both;
        a cluster inside reaches the network around it through its switch, or through the caches
        that talk to controllers outside it."""
        pairs = [(cache, manager) for cache in self.endpoints for manager in cache.managers]
        seen = set()

        def link(a, b, latency):
            if a != b and (min(a, b), max(a, b)) not in seen:
                seen.add((min(a, b), max(a, b)))
                self.links.append((a, b, latency))

        for network in self.instances:
            if not network.interconnect:
                continue
            kind, latency = network.interconnect["type"], network.interconnect["latency_ps"]
            members = [endpoint for endpoint in self.endpoints if endpoint.network() is network]
            gateways = [router for inner in self.instances
                        if inner.interconnect and inner.network() is network
                        for router in self._gateways(inner, pairs)]
            if kind == "direct":
                for cache, manager in pairs:
                    if self._common_network(cache, manager) is network:
                        link(cache.router, manager.router, latency)
            elif kind in SWITCHED:
                if kind == "crossbar":
                    ports = [network.switch] + [e.router for e in members if e.node["kind"] == "cache"]
                    for a in ports:
                        for b in ports:
                            link(a, b, latency)
                for router in [endpoint.router for endpoint in members] + gateways:
                    link(network.switch, router, latency)
            elif kind == "ring":
                for a, b in zip(gateways, gateways[1:] + gateways[:1]):
                    link(a, b, latency)
            else:
                raise SystemExit(f"error: {network.node['name']}: gem5 v23 has no {kind} interconnect")

    @staticmethod
    def _gateways(cluster, pairs):
        """The routers through which the network of `cluster` reaches the one around it."""
        if cluster.switch is not None:
            return [cluster.switch]
        return list(dict.fromkeys(cache.router for cache, manager in pairs
                                  if cluster in cache.ancestors() and cluster not in manager.ancestors()))

    @staticmethod
    def _common_network(a, b):
        around_b = set(id(cluster) for cluster in b.ancestors())
        return next(cluster for cluster in a.ancestors() if cluster.interconnect and id(cluster) in around_b)

    def _check_routes(self):
        neighbours = {router: set() for router in range(len(self.routers))}
        for a, b, _ in self.links:
            neighbours[a].add(b)
            neighbours[b].add(a)
        for cache in self.endpoints:
            reached, frontier = {cache.router}, [cache.router]
            while frontier:
                frontier = [n for router in frontier for n in neighbours[router] if n not in reached]
                reached.update(frontier)
            for manager in cache.managers:
                if manager.router not in reached:
                    raise SystemExit(f"error: no route from {cache} to {manager}: the interconnects do not link them")


# ----------------------------------------------------------------------------------------------
# The gem5 objects
# ----------------------------------------------------------------------------------------------

def cycles(picoseconds):
    return picoseconds * SYSTEM["clock_hz"] // 10 ** 12


def memory_range(plan, unit):
    """The addresses of a memory unit (a channel of an instance of the memory) and of the
    directory slice that manages it: interleaved by cache line when there are several."""
    from m5.objects import AddrRange
    if plan.memory_units == 1:
        return AddrRange(f"{plan.memory_bytes}B")
    bits = int(math.log2(plan.memory_units))
    low = int(math.log2(BLOCK_BYTES))
    return AddrRange(start=0, size=plan.memory_bytes, intlvHighBit=low + bits - 1, intlvBits=bits,
                     intlvMatch=unit)


def make_memory(plan, unit):
    import m5.objects
    cls = getattr(m5.objects, plan.memory["type"], None)
    if cls is None:
        raise SystemExit(f"error: this gem5 has no memory {plan.memory['type']}")
    if issubclass(cls, m5.objects.DRAMInterface):
        controller = m5.objects.MemCtrl()
        controller.dram = cls()
        controller.dram.range = memory_range(plan, unit)
        return controller
    return cls(range=memory_range(plan, unit))


def make_cache(node, is_icache=False):
    from m5.objects import RubyCache
    return RubyCache(size=f"{node['capacity_bytes']}B", assoc=node["associativity"],
                     start_index_bit=int(math.log2(BLOCK_BYTES)), is_icache=is_icache)


def declared(cls):
    """The parameters the machine declares in its SLICC (not those of every Ruby controller)."""
    return cls._params.local


def make_controller(plan, endpoint, ruby, memories):
    import m5.objects
    from m5.objects import MessageBuffer, RubyDirectoryMemory
    node = endpoint.node
    cls = getattr(m5.objects, f"{node['machine']}_Controller", None)
    if cls is None:
        raise SystemExit(f"error: this gem5 has no {node['machine']}: build it with the protocol "
                         f"{SYSTEM['name']} ({SYSTEM['name']}.slicc)")
    params = declared(cls)
    controller = cls(version=endpoint.version, ruby_system=ruby)
    if node["kind"] == "directory":
        controller.addr_ranges = [memory_range(plan, endpoint.version)]
        controller.directory = RubyDirectoryMemory()
        controller.memory_out_port = memories[endpoint.version].port
        for name in ("requestToMemory", "responseFromMemory"):
            if name in params:
                setattr(controller, name, MessageBuffer())
    else:
        controller.cache = make_cache(node)
    if endpoint.managers:
        # the machine finds its manager by instance (<machine>_id, cluster_id) and slice
        manager = endpoint.managers[0]
        for name in params:
            if name in (f"{manager.node['machine']}_id", "cluster_id"):
                setattr(controller, name, manager.instance.index)
            elif name.endswith("_select_num_bits"):
                setattr(controller, name, int(math.log2(manager.node["slices"])))
    if "transitions_per_cycle" in node:
        controller.transitions_per_cycle = node["transitions_per_cycle"]
    for name, param in params.items():
        if param.ptype_str == "MessageBuffer" and name not in LOCAL_BUFFERS:
            buffer = MessageBuffer(ordered=True)
            if name.endswith("To"):
                buffer.in_port = ruby.network.out_port
            else:
                buffer.out_port = ruby.network.in_port
            setattr(controller, name, buffer)
    return controller


def make_core(node, cpu_id):
    import m5.objects
    core = getattr(m5.objects, node["type"])(cpu_id=cpu_id)
    for key, param in (("rob_entries", "numROBEntries"), ("load_queue_entries", "LQEntries"),
                       ("store_queue_entries", "SQEntries"), ("issue_queue_entries", "numIQEntries")):
        if key in node:
            setattr(core, param, node[key])
    if "branch_predictor" in node:
        core.branchPred = getattr(m5.objects, node["branch_predictor"])()
        if "btb_entries" in node:
            core.branchPred.btb = m5.objects.SimpleBTB(numEntries=node["btb_entries"])
    core.createInterruptController()
    return core


def build(plan):
    """The gem5 system of the plan, and its cores."""
    from m5.objects import (AddrRange, GarnetExtLink, GarnetIntLink, GarnetNetwork,
                            GarnetNetworkInterface, GarnetRouter, MessageBuffer, RubyPortProxy,
                            RubySequencer, RubySystem, SrcClockDomain, System, VoltageDomain)

    system = System()
    system.clk_domain = SrcClockDomain(clock=f"{SYSTEM['clock_hz']}Hz", voltage_domain=VoltageDomain())
    system.mem_mode = "timing"
    system.mem_ranges = [AddrRange(f"{plan.memory_bytes}B")]

    ruby = RubySystem(number_of_virtual_networks=SYSTEM["virtual_networks"])
    system.caches = ruby
    network = GarnetNetwork(ruby_system=ruby, ni_flit_size=SYSTEM["flit_size_bytes"],
                            number_of_virtual_networks=SYSTEM["virtual_networks"])
    ruby.network = network
    network.routers = [GarnetRouter(router_id=index) for index in range(len(plan.routers))]

    # one memory unit per directory slice, in the order of the slices
    memories = [make_memory(plan, unit) for unit in range(plan.memory_units)]
    if len(memories) == 1:
        system.mem_ctrl = memories[0]
    else:
        system.mem_ctrls = memories

    controllers, ext_links = {}, []
    for endpoint in sorted(plan.endpoints, key=lambda endpoint: endpoint.router):
        controller = make_controller(plan, endpoint, ruby, memories)
        machine = endpoint.node["machine"]
        prefix = "dir" if machine == "Directory" else machine[:2].lower()
        setattr(ruby, f"{prefix}_cntrl{endpoint.version}", controller)
        controllers[endpoint] = controller
        ext_links.append(GarnetExtLink(link_id=len(ext_links), ext_node=controller,
                                       int_node=network.routers[endpoint.router],
                                       latency=cycles(endpoint.node["link_latency_ps"])))
    int_links = []
    for a, b, latency in plan.links:
        for source, destination in ((a, b), (b, a)):
            int_links.append(GarnetIntLink(link_id=len(int_links), src_node=network.routers[source],
                                           dst_node=network.routers[destination],
                                           latency=cycles(latency), weight=1))
    network.ext_links = ext_links
    network.int_links = int_links
    network.netifs = [GarnetNetworkInterface(id=index) for index in range(len(ext_links))]

    # every core with the first-level cache of its cluster, which serves its accesses
    cores = []
    for instance in plan.cores:
        core = make_core(instance.node, len(cores))
        endpoint = next(endpoint for endpoint in plan.endpoints if endpoint.node["name"] == SYSTEM["hierarchy"][0]
                        and endpoint.instance.cluster is instance.cluster)
        controller = controllers[endpoint]
        controller.clk_domain = core.clk_domain
        params = declared(type(controller))
        if "cache_instruction" in params:
            controller.cache_instruction = make_cache(endpoint.node, is_icache=True)
        if "send_evictions" in params:
            controller.send_evictions = True        # x86 needs them (the O3 load queue, mwait)
        controller.mandatoryQueue = MessageBuffer()
        controller.sequencer = RubySequencer(version=len(cores), dcache=controller.cache,
                                             clk_domain=controller.clk_domain, ruby_system=ruby)
        controller.sequencer.connectCpuPorts(core)
        cores.append(core)
    system.cpu = cores
    ruby.num_of_sequencers = len(cores)
    ruby.sys_port_proxy = RubyPortProxy()
    system.system_port = ruby.sys_port_proxy.in_ports
    return system, cores


# ----------------------------------------------------------------------------------------------
# Running a program
# ----------------------------------------------------------------------------------------------

def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        prog=os.path.basename(argv[0]),
        usage="gem5.opt [GEM5 OPTIONS] %(prog)s [OPTIONS] -- PROGRAM [ARGUMENTS]",
        description=f"Runs PROGRAM on {SYSTEM['name']} in syscall-emulation mode, a thread on every "
                    "core (a multithreaded program spreads its threads over the cores).")
    parser.add_argument("--cores", type=int, default=SYSTEM["cores"],
                        help="number of cores (default %(default)s): the clusters around the cores get "
                             "the same number each, the last one the rest")
    parser.add_argument("--cwd", default=os.getcwd(), help="working directory of the program")
    parser.add_argument("--env", action="append", default=[], metavar="VAR=VALUE",
                        help="an environment variable of the program (repeatable)")
    parser.add_argument("--input", help="file read as the program's standard input")
    parser.add_argument("--output", help="file of the program's standard output, in gem5's output directory")
    parser.add_argument("--errout", help="file of the program's standard error, in gem5's output directory")
    parser.add_argument("--redirect", action="append", default=[], metavar="GUEST=HOST",
                        help="the program finds the host directory HOST at GUEST, e.g. /etc=guest-etc "
                             "(repeatable)")
    arguments, program = argv[1:], []
    if "--" in arguments:
        separator = arguments.index("--")
        arguments, program = arguments[:separator], arguments[separator + 1:]
    args = parser.parse_args(arguments)
    if not program:
        parser.error("give the program to run after --")
    if args.cores < 1:
        parser.error("--cores must be at least 1")
    args.program = program
    return args


def main():
    import m5
    from m5.objects import Process, RedirectPath, Root, SEWorkload

    args = parse_arguments(sys.argv)
    plan = Plan(SYSTEM, args.cores)
    print(f"{SYSTEM['name']}: {len(plan.cores)} cores, {len(plan.endpoints)} controllers, "
          f"{len(plan.routers)} routers, {len(plan.links)} links")
    system, cores = build(plan)

    process = Process(cmd=args.program, cwd=args.cwd, env=args.env)
    for name in ("input", "output", "errout"):
        if getattr(args, name):
            setattr(process, name, getattr(args, name))
    if args.redirect:
        system.redirect_paths = [RedirectPath(app_path=guest, host_paths=[os.path.abspath(host)])
                                 for guest, _, host in (item.partition("=") for item in args.redirect)]
    system.workload = SEWorkload.init_compatible(args.program[0])
    for core in cores:
        core.workload = process
        core.createThreads()

    Root(full_system=False, system=system)
    m5.instantiate()
    event = m5.simulate()
    print(f"Exiting @ tick {m5.curTick()} because {event.getCause()}")


if __name__ == "__m5_main__":
    main()
