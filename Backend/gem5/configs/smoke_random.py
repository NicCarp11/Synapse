#  Ruby random tester on the synthesized two-level system.
#
#  The RubyTester issues racing loads/stores/ifetches to a small set of
#  addresses from every L1 and checks every value read against the last value
#  written, so it catches both coherence violations ("Action/check failed") and
#  deadlocks ("Deadlock detected"). Caches are tiny on purpose, to force
#  evictions and replacement races.

import argparse
import os
import sys

import m5
from m5.objects import *

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smoke_system import build_ruby

parser = argparse.ArgumentParser()
parser.add_argument("--num-cpus", type=int, default=4)
parser.add_argument("--llc-slices", type=int, default=1,
                    help="LLC slices per cluster, interleaved by address")
parser.add_argument("--clusters", type=int, default=1,
                    help="number of L2s, each with its share of the L1s")
parser.add_argument("--checks", type=int, default=10000,
                    help="RubyTester checks_to_complete")
parser.add_argument("--wakeup-freq", type=int, default=10)
parser.add_argument("--deadlock-threshold", type=int, default=50000,
                    help="RubyTester deadlock threshold (cycles)")
parser.add_argument("--l1-size", default="256B")
parser.add_argument("--l1-assoc", type=int, default=2)
parser.add_argument("--l2-size", default="1kB")
parser.add_argument("--l2-assoc", type=int, default=2)
parser.add_argument("--l3-size", default="2kB",
                    help="L3 of each cluster, with three levels (the L2s are then private)")
parser.add_argument("--l3-assoc", type=int, default=2)
parser.add_argument("--no-ifetch", action="store_true",
                    help="only data loads/stores (for L1s without an icache)")
parser.add_argument("--seed", type=int, default=0,
                    help="seed for gem5's random_mt (0: gem5 default)")
parser.add_argument("--max-tick", type=int, default=0,
                    help="abort after this many ticks (0: no limit)")
args = parser.parse_args()

print(f"PROTOCOL: {buildEnv['PROTOCOL']}")

tester = RubyTester(check_flush=False, checks_to_complete=args.checks,
                    wakeup_frequency=args.wakeup_freq,
                    deadlock_threshold=args.deadlock_threshold)

mem_range = AddrRange("512MB")
system = System(cpu=tester, mem_ranges=[mem_range])
system.voltage_domain = VoltageDomain()
system.clk_domain = SrcClockDomain(clock="1GHz",
                                   voltage_domain=system.voltage_domain)
system.mem_mode = "timing"

ruby_system, sequencers = build_ruby(
    system, args.num_cpus, mem_range,
    [system.clk_domain] * args.num_cpus,
    l1_size=args.l1_size, l1_assoc=args.l1_assoc,
    l2_size=args.l2_size, l2_assoc=args.l2_assoc,
    send_evictions=False, num_clusters=args.clusters,
    llc_slices=args.llc_slices, l3_size=args.l3_size, l3_assoc=args.l3_assoc)
ruby_system.clk_domain = system.clk_domain
ruby_system.randomization = True

tester.num_cpus = len(sequencers)
for seq in sequencers:
    if args.no_ifetch:
        seq.support_inst_reqs = False
        tester.cpuDataPort = seq.in_ports
    else:
        tester.cpuInstDataPort = seq.in_ports
    seq.no_retry_on_stall = True
    seq.using_ruby_tester = True

root = Root(full_system=False, system=system)
m5.ticks.setGlobalFrequency("1ns")
if args.seed:
    from _m5.core import seedRandom
    seedRandom(args.seed)
m5.instantiate()

if args.max_tick > 0:
    exit_event = m5.simulate(args.max_tick)
else:
    exit_event = m5.simulate()
cause = exit_event.getCause()
print(f"Exiting @ tick {m5.curTick()} because {cause}")
# RubyTester exits with "Ruby Tester completed" once all checks are done.
sys.exit(0 if "Ruby Tester completed" in cause else 1)
