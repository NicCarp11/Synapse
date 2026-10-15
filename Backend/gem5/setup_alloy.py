"""The alloy-gem5 configuration Synapse writes next to the controllers of a system.

Synapse fills SYSTEM below with the system its topology resolves to and writes the result as
<name>_gem5.py. alloy-gem5 (gem5 v20, Python 2) builds its systems with its own script,
configs/brg/sc3.py, and network, TwoMeshXY: this file gives sc3.py the options of the system and
the Ruby configuration of the generated controllers, then runs it.
"""

from __future__ import print_function

# The system, from the topology: quantities in bytes, picoseconds and hertz; every controller
# with the machine of its generated SLICC.
SYSTEM = {}

import math
import os
import sys
import types

# Settings of the Synapse artifact's S4 runs that are not part of the system: alloy's warm-up
# before the region of interest, and Garnet buffers that never fill.
FIXED_OPTIONS = ["--ruby", "--network", "garnet2.0", "--topology", "TwoMeshXY", "--brg-fast-forward",
                 "--buffer-size", "0", "--vcs-per-vnet", "64", "--buffers-per-data-vc", "65536",
                 "--buffers-per-ctrl-vc", "1024", "--garnet-deadlock-threshold", "100000"]
# the message buffers of a controller that are not connected to the network
LOCAL_BUFFERS = ("mandatoryQueue", "responseFromMemory")


# ----------------------------------------------------------------------------------------------
# The options of sc3.py
# ----------------------------------------------------------------------------------------------

def walk(node, parent=None):
    """(node, the cluster around it) for every node of the tree."""
    yield node, parent
    for child in node.get("nodes", []):
        for item in walk(child, node):
            yield item


def cycles(picoseconds):
    return picoseconds * SYSTEM["clock_hz"] // 10 ** 12


def size(nbytes):
    for unit, factor in (("GB", 2 ** 30), ("MB", 2 ** 20), ("kB", 2 ** 10)):
        if nbytes % factor == 0:
            return "%d%s" % (nbytes // factor, unit)
    return "%dB" % nbytes


def system_options(cores):
    """sc3.py's options for SYSTEM with `cores` cores."""
    nodes = dict((node["name"], node) for node, _ in walk(SYSTEM["root"]))
    parents = dict((node["name"], parent) for node, parent in walk(SYSTEM["root"]))

    def instances(node):
        parent = parents[node["name"]]
        return 1 if parent is None else parent["count"] * instances(parent)

    l1, llc, directory = [nodes[name] for name in SYSTEM["hierarchy"]]
    memory = [node for node in nodes.values() if node["kind"] == "memory"][0]
    core = [node for node in nodes.values() if node["kind"] == "core"][0]
    chiplet = nodes[llc["placement"]]
    fabric = parents[chiplet["name"]]
    while "interconnect" not in fabric:
        fabric = parents[fabric["name"]]
    if cores % llc["slices"]:
        raise SystemExit("error: %d cores do not fill the %d %s instances evenly"
                         % (cores, llc["slices"], chiplet["name"]))
    clock = "%gGHz" % (SYSTEM["clock_hz"] / 1e9)
    options = [
        "--num-cpus", cores, "--cpu-type", core["type"], "--cpu-clock", clock, "--ruby-clock", clock,
        "--l1d_size", size(l1["capacity_bytes"]), "--l1i_size", size(l1["capacity_bytes"]),
        "--l1d_assoc", l1["associativity"], "--l1i_assoc", l1["associativity"],
        "--l2_size", size(llc["capacity_bytes"]), "--l2_assoc", llc["associativity"],
        "--num-l2caches", llc["slices"], "--num-dirs", directory["slices"],
        "--mem-size", size(memory["capacity_bytes"] * instances(memory)), "--mem-type", memory["type"],
        "--link-latency", cycles(chiplet["interconnect"]["latency_ps"]),
        "--CG_link_latency", cycles(fabric["interconnect"]["latency_ps"]),
        "--link-width-bits", SYSTEM["flit_size_bytes"] * 8,
    ]
    if "transitions_per_cycle" in l1:
        options += ["--num-l1-cache-ports", l1["transitions_per_cycle"]]
    if "transitions_per_cycle" in llc:
        options += ["--ports", llc["transitions_per_cycle"]]
    return [str(option) for option in options]


# ----------------------------------------------------------------------------------------------
# The Ruby configuration of the generated controllers (configs/ruby/<protocol>.py for sc3.py)
# ----------------------------------------------------------------------------------------------

def define_options(parser):
    return


def connect_network(controller, ruby_system):
    """Connects every network buffer of the machine. The machines name their buffers after the
    direction towards the directory: an L1 or an LLC sends on `<net>To` and receives on
    `<net>From`, the directory the other way round."""
    import m5
    from m5.objects import MessageBuffer
    for name, param in sorted(controller._params.items()):
        if name in LOCAL_BUFFERS or not isinstance(param, m5.params.ParamDesc) or \
                param.ptype_str != "MessageBuffer":
            continue
        buffer = MessageBuffer()
        setattr(controller, name, buffer)
        sends = name.endswith("From") if controller.type == "Directory_Controller" else name.endswith("To")
        if sends:
            buffer.master = ruby_system.network.slave
        else:
            buffer.slave = ruby_system.network.master


def create_system(options, full_system, system, dma_ports, bootmem, ruby_system):
    """The L1s, the LLC slices (slice i owns the i-th contiguous range of the addresses) and the
    directory slices, as the Synapse artifact's configs/ruby/MESIRC_*.py."""
    import m5
    from m5.objects import (DerivedClockDomain, DOSequencer, L1Cache_Controller, L2Cache_Controller,
                            MessageBuffer, RubyCache)
    from ruby.Ruby import create_directories, create_topology, send_evicts

    assert not dma_ports and not full_system, "SE mode without DMA only"
    cpu_sequencers, l1_controllers, l2_controllers = [], [], []
    l2_bits = int(math.log(options.num_l2caches, 2))
    block_size_bits = int(math.log(options.cacheline_size, 2))

    for i in range(options.num_cpus):
        cache = RubyCache(size=options.l1d_size, assoc=options.l1d_assoc, start_index_bit=block_size_bits,
                          is_icache=False)
        clk_domain = system.cpu[0].clk_domain if len(system.cpu) == 1 else system.cpu[i].clk_domain
        sequencer = DOSequencer(version=i, icache=cache, dcache=cache, clk_domain=clk_domain,
                                ruby_system=ruby_system)
        controller = L1Cache_Controller(version=i, sequencer=sequencer, cache=cache, cache_instruction=cache,
                                        L2Cache_id=0, cluster_id=0, l2_select_num_bits=l2_bits,
                                        send_evictions=send_evicts(options), ruby_system=ruby_system,
                                        clk_domain=clk_domain, transitions_per_cycle=options.num_l1_cache_ports)
        setattr(ruby_system, "l1_cntrl%d" % i, controller)
        controller.mandatoryQueue = MessageBuffer()
        connect_network(controller, ruby_system)
        cpu_sequencers.append(sequencer)
        l1_controllers.append(controller)

    for i in range(options.num_l2caches):
        # the set index starts above the slice bits, as in the artifact
        cache = RubyCache(size=options.l2_size, assoc=options.l2_assoc, start_index_bit=block_size_bits + l2_bits)
        controller = L2Cache_Controller(version=i, cache=cache, transitions_per_cycle=options.ports,
                                        ruby_system=ruby_system)
        setattr(ruby_system, "l2_cntrl%d" % i, controller)
        connect_network(controller, ruby_system)
        l2_controllers.append(controller)

    ruby_system.memctrl_clk_domain = DerivedClockDomain(clk_domain=ruby_system.clk_domain, clk_divider=3)
    directories, rom_directory = create_directories(options, bootmem, ruby_system, system)
    all_directories = directories + ([rom_directory] if rom_directory is not None else [])
    for controller in all_directories:
        controller.responseFromMemory = MessageBuffer()
        connect_network(controller, ruby_system)

    controllers = l1_controllers + l2_controllers + all_directories
    # one virtual network per network the protocol declares (`<net>To`/`<net>From`)
    networks = set()
    for controller in controllers:
        for name, param in controller._params.items():
            if isinstance(param, m5.params.ParamDesc) and param.ptype_str == "MessageBuffer" \
                    and name not in LOCAL_BUFFERS:
                for suffix in ("To", "From"):
                    if name.endswith(suffix):
                        networks.add(name[:-len(suffix)])
    ruby_system.network.number_of_virtual_networks = len(networks)
    return cpu_sequencers, directories, create_topology(controllers, options)


# ----------------------------------------------------------------------------------------------
# Running sc3.py
# ----------------------------------------------------------------------------------------------

USAGE = """gem5.opt [GEM5 OPTIONS] %s [--cores N] [--alloy DIR] [SC3 OPTIONS] -c PROGRAM -o "ARGUMENTS"

Runs PROGRAM on %s with alloy-gem5's configs/brg/sc3.py. --cores sets the number of cores (default
%d, a multiple of the chiplets); --alloy is the alloy-gem5 tree (default: the one gem5.opt was built
in); the other options go to sc3.py after those of the system and can override them."""


def parse_arguments(argv):
    cores, alloy, rest = SYSTEM["cores"], None, []
    arguments = list(argv[1:])
    while arguments:
        argument = arguments.pop(0)
        name, _, value = argument.partition("=")
        if name in ("--cores", "--alloy"):
            if not value:
                if not arguments:
                    raise SystemExit("error: %s needs a value" % name)
                value = arguments.pop(0)
            if name == "--cores":
                cores = int(value)
            else:
                alloy = value
        elif argument in ("-h", "--help"):
            print(USAGE % (os.path.basename(argv[0]), SYSTEM["name"], SYSTEM["cores"]))
            raise SystemExit(0)
        else:
            rest.append(argument)
    if alloy is None:
        # build/<variant>/gem5.opt in the alloy-gem5 tree
        alloy = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath("/proc/self/exe"))))
    return cores, alloy, rest


def main():
    from m5.defines import buildEnv
    cores, alloy, rest = parse_arguments(sys.argv)
    sc3 = os.path.join(alloy, "configs", "brg", "sc3.py")
    if not os.path.isfile(sc3):
        raise SystemExit("error: no %s: give the alloy-gem5 tree with --alloy" % sc3)
    # sc3.py's Ruby.create_system imports the configuration named after the protocol from the
    # package ruby (configs/ruby): this one takes its place
    module = types.ModuleType(buildEnv["PROTOCOL"])
    module.define_options = define_options
    module.create_system = create_system
    sys.modules[buildEnv["PROTOCOL"]] = sys.modules["ruby." + buildEnv["PROTOCOL"]] = module
    sys.argv = [sc3] + system_options(cores) + FIXED_OPTIONS + rest
    sys.path[0] = os.path.dirname(sc3)
    print("%s: %d cores, sc3.py %s" % (SYSTEM["name"], cores, " ".join(sys.argv[1:])))
    exec(compile(open(sc3).read(), sc3, "exec"), {"__file__": sc3, "__name__": "__m5_main__"})


if __name__ == "__m5_main__":
    main()
