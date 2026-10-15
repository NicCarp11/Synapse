#  Protocol-agnostic Ruby system for the gem5 smoke tests.
#
#  Topology: N x L1 (client) -> 1 x L2 (proxy / LLC) -> 1 x Directory, i.e. the
#  two-level layout of Synapse's `MESI_MESI_WB_INCL_SMP`.
#  With K clusters (`num_clusters`), the L1s are split into K groups of
#  consecutive cores, each with its own L2, all sharing the directory, as in
#  Synapse `setup-real_NUMA.py` (4 clusters there, with one directory slice
#  each). Only then the off-core protocol (between the L2s and the directory)
#  sees more than one cache: sharing, forwarding and invalidations between L2s.
#  With S LLC slices per cluster (`llc_slices`, a power of 2) the L2 of a cluster is split into S
#  slices interleaved by address, as in Synapse `setup_cluster_real.py` (multi-host, 8 slices): the
#  L1 must then select the slice itself (`l2_select_num_bits`, generated for a topology whose LLC
#  has slices). Slice i of cluster c is L2 controller c * S + i, the numbering of gem5's
#  mapAddressToRange().
#  Three levels: if the protocol has an L3Cache machine (a topology with three cache levels),
#  every core gets an L1 and a private L2 (L2 controller i, the L1's `L2Cache_id`), every cluster
#  an L3 (the L2s' `L3Cache_id`), all sharing the directory, as in Synapse
#  `setup-real_UMA_three_level.py`.
#  Controller classes follow Synapse `setup/protocols/synth_two_level.py`; the
#  only difference is that sizes are parameters (the random tester needs tiny
#  caches to force evictions) and optional SLICC parameters are only set when the
#  machine actually declares them.

import math

from m5.objects import *
from m5.util import panic


def _block_bits(system):
    bits = int(math.log(system.cache_line_size, 2))
    if 2**bits != system.cache_line_size.value:
        panic("Cache line size not a power of 2!")
    return bits


def _has_param(sim_object_cls, name):
    return name in sim_object_cls._params


# m5.objects only has the controllers of the machines the protocol declares
L3Cache_Controller = globals().get("L3Cache_Controller")


_LOCAL_BUFFERS = ("mandatoryQueue", "requestToMemory", "responseFromMemory")


def _connect_dynamic_queues(cntrl, ruby_system):
    # Every network of the machine has a "To" and a "From" buffer (fwd, resp, req for the
    # MESI-like protocols; a machine of a CXL level also has the CXL.mem channels bisnp, birsp,
    # ndr, drs, req2, rwd). The machine declares only the networks it uses.
    names = [name for name, param in type(cntrl)._params.items()
             if param.ptype_str == "MessageBuffer" and name not in _LOCAL_BUFFERS]
    for name in names:
        buf = MessageBuffer(ordered=True)
        if name.endswith("To"):
            buf.in_port = ruby_system.network.out_port
        else:
            buf.out_port = ruby_system.network.in_port
        setattr(cntrl, name, buf)


class SmokeL1Cache(L1Cache_Controller):
    _version = 0

    @classmethod
    def versionCount(cls):
        cls._version += 1
        return cls._version - 1

    def __init__(self, system, ruby_system, clk_domain, cluster_id, size,
                 assoc, send_evictions, llc_slices=1, l2_id=None):
        super().__init__()
        self.version = self.versionCount()
        bits = _block_bits(system)
        self.cache = RubyCache(size=size, assoc=assoc, start_index_bit=bits,
                               is_icache=False)
        if _has_param(L1Cache_Controller, "cache_instruction"):
            self.cache_instruction = RubyCache(size=size, assoc=assoc,
                                               start_index_bit=bits,
                                               is_icache=True)
        if _has_param(L1Cache_Controller, "L2Cache_id"):
            # the cluster's LLC, or the core's private L2 with three levels
            self.L2Cache_id = cluster_id if l2_id is None else l2_id
        if _has_param(L1Cache_Controller, "l2_select_num_bits"):
            self.l2_select_num_bits = int(math.log(llc_slices, 2))
        if _has_param(L1Cache_Controller, "cluster_id"):
            self.cluster_id = cluster_id
        if _has_param(L1Cache_Controller, "send_evictions"):
            self.send_evictions = send_evictions
        self.clk_domain = clk_domain
        self.ruby_system = ruby_system
        self.mandatoryQueue = MessageBuffer()
        _connect_dynamic_queues(self, ruby_system)


class SmokeL2Cache(L2Cache_Controller):
    _version = 0

    @classmethod
    def versionCount(cls):
        cls._version += 1
        return cls._version - 1

    def __init__(self, system, ruby_system, size, assoc, l3_id=0):
        super().__init__()
        self.version = self.versionCount()
        self.cache = RubyCache(size=size, assoc=assoc,
                               start_index_bit=_block_bits(system),
                               is_icache=False)
        if _has_param(L2Cache_Controller, "L3Cache_id"):
            self.L3Cache_id = l3_id
        self.ruby_system = ruby_system
        _connect_dynamic_queues(self, ruby_system)


if L3Cache_Controller is not None:
    class SmokeL3Cache(L3Cache_Controller):
        _version = 0

        @classmethod
        def versionCount(cls):
            cls._version += 1
            return cls._version - 1

        def __init__(self, system, ruby_system, size, assoc):
            super().__init__()
            self.version = self.versionCount()
            self.cache = RubyCache(size=size, assoc=assoc,
                                   start_index_bit=_block_bits(system),
                                   is_icache=False)
            self.ruby_system = ruby_system
            _connect_dynamic_queues(self, ruby_system)


class SmokeDirectory(Directory_Controller):
    _version = 0

    @classmethod
    def versionCount(cls):
        cls._version += 1
        return cls._version - 1

    def __init__(self, ruby_system, ranges, mem_ctrl):
        super().__init__()
        self.version = self.versionCount()
        self.addr_ranges = ranges
        self.ruby_system = ruby_system
        self.directory = RubyDirectoryMemory()
        self.memory_out_port = mem_ctrl.port
        self.requestToMemory = MessageBuffer()
        self.responseFromMemory = MessageBuffer()
        _connect_dynamic_queues(self, ruby_system)


class SmokeNetwork(GarnetNetwork):
    """Same Garnet network as Synapse `setup-real_UMA.py`."""

    def __init__(self, ruby_system):
        super().__init__()
        self.netifs = []
        self.routers = []
        self.ext_links = []
        self.int_links = []
        self.ruby_system = ruby_system
        self.ni_flit_size = 256

    def create_router(self):
        router = GarnetRouter(router_id=len(self.routers))
        self.routers.append(router)
        return router

    def connect_controller(self, router, controller, latency=8):
        self.ext_links.append(GarnetExtLink(link_id=len(self.ext_links),
                                            ext_node=controller,
                                            int_node=router,
                                            latency=latency))

    def connect_routers(self, routers, latency=8, weight=1):
        for ri in routers:
            for rj in routers:
                if ri == rj:
                    continue
                self.int_links.append(GarnetIntLink(
                    link_id=len(self.int_links), src_node=ri, dst_node=rj,
                    latency=latency, weight=weight))

    def setup_buffers(self):
        self.netifs = [GarnetNetworkInterface(id=i)
                       for (i, _) in enumerate(self.ext_links)]


def _split_clusters(num_l1, num_clusters):
    """Consecutive core ids of each cluster, as even as possible."""
    if not 1 <= num_clusters <= num_l1:
        panic(f"cannot split {num_l1} cores into {num_clusters} clusters")
    base, extra = divmod(num_l1, num_clusters)
    clusters, start = [], 0
    for c in range(num_clusters):
        size = base + (1 if c < extra else 0)
        clusters.append(list(range(start, start + size)))
        start += size
    return clusters


def build_ruby(system, num_l1, mem_range, clk_domains, l1_size="64kB",
               l1_assoc=8, l2_size="2MB", l2_assoc=8, send_evictions=True,
               component_latency=10, local_latency=10, dir_latency=10,
               deadlock_threshold=None, num_clusters=1, llc_slices=1,
               l3_size="8MB", l3_assoc=8):
    """Builds the Ruby system and returns the list of L1 sequencers.

    `clk_domains[i]` is the clock domain used by the i-th L1 and sequencer.
    With three levels, `l2_size` is the private L2 and `l3_size` the L3.
    """
    three_level = L3Cache_Controller is not None
    ruby_system = RubySystem()
    system.caches = ruby_system
    network = SmokeNetwork(ruby_system)
    ruby_system.network = network
    ruby_system.number_of_virtual_networks = 9
    network.number_of_virtual_networks = 9

    mem_ctrl = MemCtrl()
    mem_ctrl.dram = DDR4_2400_8x8()
    mem_ctrl.dram.range = mem_range
    system.mem_ctrl = mem_ctrl

    directory = SmokeDirectory(ruby_system, [mem_range], mem_ctrl)
    ruby_system.dir_cntrl = directory
    dir_router = network.create_router()
    network.connect_controller(dir_router, directory)

    if llc_slices < 1 or llc_slices & (llc_slices - 1):
        panic(f"llc_slices must be a power of 2, not {llc_slices}")
    if llc_slices > 1 and not _has_param(L1Cache_Controller, "l2_select_num_bits"):
        panic("this protocol's L1 cannot select an LLC slice (no l2_select_num_bits)")
    if llc_slices > 1 and three_level:
        panic("LLC slices are not supported with three levels")

    sequencers = []
    for cluster_id, cores in enumerate(_split_clusters(num_l1, num_clusters)):
        # The clusters talk to each other (e.g. forwarded data between L2s)
        # through the directory router
        cluster_router = network.create_router()
        network.connect_routers([dir_router, cluster_router], dir_latency)
        local_routers = [cluster_router]

        if three_level:
            l3 = SmokeL3Cache(system, ruby_system, l3_size, l3_assoc)
            setattr(ruby_system, f"l3_cntrl{cluster_id}", l3)
            l3_router = network.create_router()
            network.connect_controller(l3_router, l3, component_latency)
            local_routers.append(l3_router)
        else:
            for s in range(llc_slices):
                l2 = SmokeL2Cache(system, ruby_system, l2_size, l2_assoc)
                setattr(ruby_system, f"l2_cntrl{cluster_id * llc_slices + s}", l2)
                l2_router = network.create_router()
                network.connect_controller(l2_router, l2, component_latency)
                local_routers.append(l2_router)

        for i in cores:
            l1 = SmokeL1Cache(system, ruby_system, clk_domains[i], cluster_id,
                              l1_size, l1_assoc, send_evictions, llc_slices,
                              l2_id=i if three_level else None)
            setattr(ruby_system, f"l1_cntrl{i}", l1)
            router = network.create_router()
            network.connect_controller(router, l1, component_latency)
            local_routers.append(router)
            if three_level:
                # private L2 of core i: L2 controller i
                l2 = SmokeL2Cache(system, ruby_system, l2_size, l2_assoc, l3_id=cluster_id)
                setattr(ruby_system, f"l2_cntrl{i}", l2)
                l2_router = network.create_router()
                network.connect_controller(l2_router, l2, component_latency)
                local_routers.append(l2_router)

            seq_args = dict(version=i, dcache=l1.cache,
                            clk_domain=clk_domains[i], ruby_system=ruby_system)
            if deadlock_threshold is not None:
                seq_args["deadlock_threshold"] = deadlock_threshold
            sequencer = RubySequencer(**seq_args)
            l1.sequencer = sequencer
            sequencers.append(sequencer)

        network.connect_routers(local_routers, local_latency)

    ruby_system.num_of_sequencers = len(sequencers)
    network.setup_buffers()

    ruby_system.sys_port_proxy = RubyPortProxy()
    system.system_port = ruby_system.sys_port_proxy.in_ports
    return ruby_system, sequencers
