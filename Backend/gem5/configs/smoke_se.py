#  Syscall-emulation run of a real multi-threaded binary on the synthesized
#  two-level system. Mirrors Synapse `setup-real_UMA.py` (same Garnet network,
#  same controller sizes) but does not depend on the protocol name.
#
#  Usage: gem5.opt smoke_se.py -c 8 [--cpu-type O3CPU] -- <binary> [args...]

import argparse
import os
import sys

import m5
from m5.objects import *

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smoke_system import build_ruby

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cores", type=int, default=4)
parser.add_argument("--llc-slices", type=int, default=1,
                    help="LLC slices per cluster, interleaved by address")
parser.add_argument("--clusters", type=int, default=1,
                    help="number of L2s, each with its share of the cores")
parser.add_argument("--cpu-type", default="O3CPU",
                    choices=["O3CPU", "TimingSimpleCPU"])
parser.add_argument("--deadlock-threshold", type=int, default=None,
                    help="RubySequencer deadlock threshold (cycles)")
parser.add_argument("--env", action="append", default=[],
                    help="extra KEY=VALUE environment entries")
parser.add_argument("cmd", nargs=argparse.REMAINDER)
args = parser.parse_args()

if args.cmd and args.cmd[0] == "--":
    args.cmd = args.cmd[1:]
if not args.cmd:
    fatal("No workload specified. Expected: -- <binary> [args...]")

print(f"PROTOCOL: {buildEnv['PROTOCOL']}")

system = System()
system.clk_domain = SrcClockDomain(clock="2GHz",
                                   voltage_domain=VoltageDomain())
system.mem_mode = "timing"
mem_range = AddrRange("8GB")
system.mem_ranges = [mem_range]

cpu_cls = O3CPU if args.cpu_type == "O3CPU" else TimingSimpleCPU
cpus = [cpu_cls(cpu_id=i) for i in range(args.cores)]
for cpu in cpus:
    cpu.createInterruptController()
system.cpu = cpus

ruby_system, sequencers = build_ruby(
    system, args.cores, mem_range, [cpu.clk_domain for cpu in cpus],
    deadlock_threshold=args.deadlock_threshold, num_clusters=args.clusters,
    llc_slices=args.llc_slices)
for cpu, seq in zip(cpus, sequencers):
    seq.connectCpuPorts(cpu)

binary = os.path.abspath(args.cmd[0])
system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cwd = os.getcwd()
process.cmd = [binary] + args.cmd[1:]
process.output = "program.out"
process.errout = "program.err"
process.env = [f"MAPRED_NPROCESSORS={len(cpus) - 1}"] + args.env

for cpu in cpus:
    cpu.workload = process
    cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()
exit_event = m5.simulate()
cause = exit_event.getCause()
print(f"Exiting @ tick {m5.curTick()} because {cause}")
sys.exit(0 if cause == "exiting with last active thread context" else 1)
