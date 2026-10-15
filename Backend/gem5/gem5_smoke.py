#!/usr/bin/env python3
#  gem5 smoke-test backend.
#
#  Takes one or more SLICC protocols (a directory of .sm files each, e.g. the
#  output of Backend/SLICC), injects them into a
#  gem5 v23 tree, builds one gem5.opt per protocol and runs the same smoke tests
#  on all of them:
#
#    slicc   standalone SLICC parse + C++ generation (seconds; catches syntax
#            and type errors before the long scons build)
#    build   scons build/X86_<NAME>/gem5.opt
#    random  Ruby random tester (racing loads/stores/ifetches, value checks,
#            deadlock detection), several seeds / core counts
#    kmeans  Phoenix kmeans in SE mode, output compared with a native run
#            (same check as Synapse `run-functional.sh`)
#
#  Everything runs inside the Synapse docker image by default, which is the
#  environment gem5 v23 was built with for the paper (Ubuntu 22.04).
#
#  Example (from the repository root):
#    python synapse.py generate specs/topologies/smp.yaml --out out/smp
#    python3 Backend/gem5/gem5_smoke.py \
#        --gem5 <gem5 v23 tree> \
#        --protocol MESI_MESI_WB_INCL_SMP=out/smp \
#        --kmeans-dir <phoenix-2.0>/tests/kmeans

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import uuid
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
CONFIG_DIR = HERE / "configs"

DEFAULT_IMAGE = "carpeniem/synapse-artifact-s1_2_3:base"
STAGE_SUBDIR = Path("src") / "custom" / "smoke"
ALL_STEPS = ["slicc", "build", "random", "kmeans"]

# Paths inside the container
C_GEM5 = "/gem5"
C_CONFIGS = "/smoke/configs"
C_OUT = "/smoke/out"
C_KMEANS = "/smoke/kmeans"

KMEANS_ARGS = "-d 250 -c 6 -p 50 -s 50"  # Synapse functional test

# Order in which machines are included in the generated .slicc manifest
MACHINE_ORDER = ["Directory", "L3Cache", "L2Cache", "L1Cache"]
ROLE_NAME = {"Directory": "dir", "L3Cache": "l3", "L2Cache": "l2", "L1Cache": "l1"}

# Patterns used to classify a failed gem5 run
FAILURE_PATTERNS = [
    ("deadlock", r"Deadlock detected|Possible Deadlock detected"),
    ("check-failure", r"Action/check failure"),
    ("invalid-transition", r"Invalid transition"),
    ("panic", r"panic:"),
    ("fatal", r"fatal:"),
    ("assert", r"Assertion .* failed"),
    ("segfault", r"Segmentation fault|SIGSEGV"),
    ("config-error", r"^\w*(Error|Exception): "),
]


@dataclass
class Protocol:
    name: str
    src: Optional[Path]              # directory with the .sm files
    prebuilt: Optional[Path] = None  # or an existing gem5.opt built with the protocol


@dataclass
class StepResult:
    protocol: str
    step: str
    status: str  # PASS / FAIL / SKIP
    detail: str = ""
    seconds: float = 0.0
    log: str = ""


@dataclass
class Runner:
    gem5: Path
    out: Path
    image: Optional[str]
    kmeans_dir: Optional[Path]
    verbose: bool = False
    mounts: List[Tuple[Path, str, bool]] = field(default_factory=list)

    def __post_init__(self):
        self.mounts = [(self.gem5, C_GEM5, False),
                       (CONFIG_DIR, C_CONFIGS, True),
                       (self.out, C_OUT, False)]
        if self.kmeans_dir is not None:
            self.mounts.append((self.kmeans_dir, C_KMEANS, True))

    def path(self, host: Path) -> str:
        """Translates a host path into the path seen by the command."""
        if self.image is None:
            return str(host)
        host = host.resolve()
        for h, c, _ in self.mounts:
            h = h.resolve()
            if host == h or h in host.parents:
                return str(Path(c) / host.relative_to(h))
        raise ValueError(f"{host} is not visible inside the container")

    def run(self, cmd: str, log: Path, cwd: Path, timeout: Optional[int]) -> Tuple[int, bool]:
        """Runs `cmd` (bash) and writes its output to `log`.
        Returns (exit code, timed out)."""
        log.parent.mkdir(parents=True, exist_ok=True)
        container = None
        if self.image is None:
            argv = ["bash", "-c", cmd]
            run_cwd = cwd
        else:
            container = f"gem5-smoke-{uuid.uuid4().hex[:12]}"
            argv = ["docker", "run", "--rm", "--init", "--name", container,
                    "--user", f"{os.getuid()}:{os.getgid()}",
                    "-e", "HOME=/tmp", "-w", self.path(cwd)]
            for h, c, ro in self.mounts:
                argv += ["-v", f"{h.resolve()}:{c}" + (":ro" if ro else "")]
            argv += [self.image, "bash", "-c", cmd]
            run_cwd = None
        if self.verbose:
            print("    $ " + cmd)
        with open(log, "w") as f:
            f.write(f"# {cmd}\n")
            f.flush()
            proc = subprocess.Popen(argv, stdout=f, stderr=subprocess.STDOUT, cwd=run_cwd,
                                    start_new_session=True)
            try:
                return proc.wait(timeout=timeout), False
            except subprocess.TimeoutExpired:
                if container is not None:
                    # Killing the docker client does not stop the container.
                    subprocess.run(["docker", "kill", container], capture_output=True)
                proc.kill()
                proc.wait()
                return -1, True


# --------------------------------------------------------------------------- #
# Staging
# --------------------------------------------------------------------------- #

def machine_type(sm_text: str) -> Optional[str]:
    m = re.search(r"^\s*machine\s*\(\s*MachineType\s*:\s*(\w+)", sm_text, re.M)
    return m.group(1) if m else None


def stage_protocol(proto: Protocol, gem5: Path) -> Path:
    """Copies the .sm files of `proto` into src/custom/smoke/<name>/, renaming
    them to <name>_<role>.sm (SLICC resolves includes over *all* protocol
    directories, so file names must be unique), and writes the .slicc manifest
    and SConsopts."""
    sm_files = sorted(proto.src.glob("*.sm"))
    if not sm_files:
        raise SystemExit(f"error: no .sm files in {proto.src}")

    dest = gem5 / STAGE_SUBDIR / proto.name
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    plain: List[Tuple[str, Path]] = []
    machines: Dict[str, List[Path]] = {}
    for sm in sm_files:
        mtype = machine_type(sm.read_text())
        if mtype is None:
            plain.append(("msg", sm))
        else:
            machines.setdefault(mtype, []).append(sm)

    ordered: List[Tuple[str, Path]] = list(plain)
    for mtype in MACHINE_ORDER + sorted(set(machines) - set(MACHINE_ORDER)):
        for sm in machines.get(mtype, []):
            ordered.append((ROLE_NAME.get(mtype, mtype.lower()), sm))

    includes = []
    used = set()
    for role, sm in ordered:
        new_name = f"{proto.name}_{role}.sm"
        i = 1
        while new_name in used:
            i += 1
            new_name = f"{proto.name}_{role}{i}.sm"
        used.add(new_name)
        shutil.copy2(sm, dest / new_name)
        includes.append(new_name)

    manifest = [f'protocol "{proto.name}";', "",
                'include "RubySlicc_interfaces.slicc";']
    manifest += [f'include "{inc}";' for inc in includes]
    (dest / f"{proto.name}.slicc").write_text("\n".join(manifest) + "\n")
    (dest / "SConsopts").write_text("Import('*')\nmain.Append(PROTOCOL_DIRS=[Dir('.')])\n")
    (dest / "SOURCES.txt").write_text(
        f"source: {proto.src.resolve()}\n" +
        "".join(f"{inc} <- {sm.name}\n" for inc, (_, sm) in zip(includes, ordered)))
    return dest


def write_kconfig(gem5: Path):
    """Regenerates src/custom/smoke/Kconfig for every staged protocol and hooks
    it into src/Kconfig."""
    stage_root = gem5 / STAGE_SUBDIR
    names = sorted(p.name for p in stage_root.iterdir()
                   if p.is_dir() and (p / f"{p.name}.slicc").exists())
    lines = ["config PROTOCOL"]
    lines += [f'    default "{n}" if {kconfig_symbol(n)}' for n in names]
    lines += ["", 'cont_choice "Ruby protocol"']
    for n in names:
        lines += [f"    config {kconfig_symbol(n)}", f'        bool "{n} (smoke test)"']
    lines += ["endchoice", ""]
    (stage_root / "Kconfig").write_text("\n".join(lines))

    top = gem5 / "src" / "Kconfig"
    text = top.read_text()
    hook = 'rsource "custom/smoke/Kconfig"'
    if hook not in text:
        top.write_text(text.rstrip("\n") + "\n" + hook + "\n")

    # Synapse's gem5 sources custom/slicc/Kconfig unconditionally; a fresh
    # tarball does not ship it, which makes every Kconfig step fail.
    synapse_kconfig = gem5 / "src" / "custom" / "slicc" / "Kconfig"
    if 'rsource "custom/slicc/Kconfig"' in text and not synapse_kconfig.exists():
        synapse_kconfig.parent.mkdir(parents=True, exist_ok=True)
        synapse_kconfig.write_text("# placeholder created by gem5_smoke.py\n")


def kconfig_symbol(name: str) -> str:
    return f"RUBY_SMOKE_{name}"


def stage_hash(stage_dir: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(stage_dir.iterdir()):
        if f.is_file():
            h.update(f.name.encode())
            h.update(f.read_bytes())
    return h.hexdigest()[:16]


# --------------------------------------------------------------------------- #
# Steps
# --------------------------------------------------------------------------- #

def tail(path: Path, pattern: Optional[str] = None, n: int = 6) -> str:
    try:
        lines = path.read_text(errors="replace").splitlines()
    except FileNotFoundError:
        return ""
    if pattern:
        rx = re.compile(pattern)
        lines = [line for line in lines if rx.search(line)]
    return "\n".join(lines[-n:])


def classify_failure(*logs: Path) -> str:
    text = ""
    for log in logs:
        if log.exists():
            text += log.read_text(errors="replace")
    for kind, rx in FAILURE_PATTERNS:
        m = re.search(rf"^.*(?:{rx}).*$", text, re.M)
        if m:
            return f"{kind}: {m.group(0).strip()[:300]}"
    return ""


def step_slicc(r: Runner, proto: Protocol, args) -> StepResult:
    stage = r.gem5 / STAGE_SUBDIR / proto.name
    out = r.out / proto.name / "slicc"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    log = r.out / proto.name / "slicc.log"
    cmd = (f"cd {r.path(r.gem5)} && PYTHONPATH=src/mem:ext/ply:build_tools "
           f"python3 -m slicc.main --tb -C {r.path(out / 'generated')} "
           f"-H {r.path(out / 'html')} {r.path(stage / (proto.name + '.slicc'))}")
    t = time.time()
    rc, to = r.run(cmd, log, r.gem5, timeout=600)
    ok = rc == 0 and "SLICC is Done" in log.read_text(errors="replace")
    detail = "" if ok else tail(log, r"Error:", 3) or tail(log)
    warnings = len(re.findall(r"Warning", log.read_text(errors="replace")))
    if ok and warnings:
        detail = f"{warnings} SLICC warnings"
    return StepResult(proto.name, "slicc", "PASS" if ok else "FAIL", detail,
                      time.time() - t, str(log))


def build_dir(proto: Protocol, args) -> str:
    return f"build/{args.build_dir}" if args.build_dir else f"build/X86_{proto.name}"


def step_build(r: Runner, proto: Protocol, args) -> StepResult:
    bdir = build_dir(proto, args)
    log = r.out / proto.name / "build.log"
    sym = kconfig_symbol(proto.name)
    linker = "" if args.no_mold else "--linker=mold"
    cmd = (f"set -e; cd {r.path(r.gem5)}; "
           f"if [ ! -f {bdir}/gem5.build/config ]; then scons defconfig {bdir} build_opts/X86; fi; "
           f"scons setconfig {bdir} RUBY=y {sym}=y; "
           f"grep -q '^PROTOCOL=\"{proto.name}\"' {bdir}/gem5.build/config || "
           f"{{ echo 'protocol not selected in {bdir}/gem5.build/config'; exit 3; }}; "
           f"scons {bdir}/gem5.opt -j {args.jobs} {linker}")
    t = time.time()
    rc, to = r.run(cmd, log, r.gem5, timeout=args.build_timeout)
    binary = r.gem5 / bdir / "gem5.opt"
    ok = rc == 0 and binary.exists()
    detail = ""
    if ok:
        stage = r.gem5 / STAGE_SUBDIR / proto.name
        (r.out / proto.name / "build.hash").write_text(stage_hash(stage) + "\n")
        if args.build_dir:
            # The shared build directory is rebuilt for the next protocol: keep this binary.
            shutil.copy2(binary, gem5_binary(r, proto, args))
    else:
        detail = "timeout" if to else (tail(log, r"(error|Error|\.sm:\d+)", 8) or tail(log))
    return StepResult(proto.name, "build", "PASS" if ok else "FAIL", detail,
                      time.time() - t, str(log))


def gem5_binary(r: Runner, proto: Protocol, args) -> Path:
    if args.build_dir or proto.prebuilt:
        return r.out / proto.name / "gem5.opt"
    return r.gem5 / build_dir(proto, args) / "gem5.opt"


def random_tag(cpus: int, seed: int, clusters: int, slices: int = 1) -> str:
    return f"random-c{cpus}-s{seed}" + (f"-k{clusters}" if clusters > 1 else "") + \
        (f"-b{slices}" if slices > 1 else "")


def kmeans_tag(args) -> str:
    return f"kmeans-c{args.kmeans_cores}" + \
        (f"-k{args.kmeans_clusters}" if args.kmeans_clusters > 1 else "") + \
        (f"-b{args.kmeans_llc_slices}" if args.kmeans_llc_slices > 1 else "")


def step_random(r: Runner, proto: Protocol, args) -> List[StepResult]:
    results = []
    binary = gem5_binary(r, proto, args)
    for cpus, seed, clusters, slices in args.random_runs:
        tag = random_tag(cpus, seed, clusters, slices)
        rdir = r.out / proto.name / tag
        if rdir.exists():
            shutil.rmtree(rdir)
        rdir.mkdir(parents=True)
        log = rdir / "run.log"
        extra = " --no-ifetch" if args.no_ifetch else ""
        cmd = (f"{r.path(binary)} --outdir={r.path(rdir)} "
               f"{C_CONFIGS if r.image else CONFIG_DIR}/smoke_random.py "
               f"--num-cpus {cpus} --clusters {clusters} --llc-slices {slices} --seed {seed} "
               f"--checks {args.random_checks}{extra}")
        t = time.time()
        rc, to = r.run(cmd, log, rdir, timeout=args.random_timeout)
        ok = rc == 0 and "Ruby Tester completed" in log.read_text(errors="replace")
        detail = ""
        if not ok:
            detail = "timeout (no progress / livelock?)" if to else \
                (classify_failure(log) or tail(log, n=3))
        results.append(StepResult(proto.name, tag, "PASS" if ok else "FAIL", detail,
                                  time.time() - t, str(log)))
    return results


def final_means(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    lines = path.read_text(errors="replace").splitlines()
    for i, line in enumerate(lines):
        if "Final means:" in line:
            return " ".join(re.findall(r"-?\d+", " ".join(lines[i + 1:])))
    return None


def kmeans_expected(r: Runner, args) -> Optional[str]:
    ref = r.out / "kmeans-native.txt"
    if not ref.exists() or final_means(ref) is None:
        kdir = r.path(args.kmeans_dir) if r.image is None else C_KMEANS
        cmd = f"cd {kdir} && ./kmeans {KMEANS_ARGS}"
        r.run(cmd, ref, r.out, timeout=600)
    return final_means(ref)


def step_kmeans(r: Runner, proto: Protocol, args) -> StepResult:
    expected = kmeans_expected(r, args)
    if not expected:
        return StepResult(proto.name, "kmeans", "FAIL",
                          f"native reference run failed, see {r.out / 'kmeans-native.txt'}")
    binary = gem5_binary(r, proto, args)
    kdir = r.path(args.kmeans_dir) if r.image is None else C_KMEANS
    rdir = r.out / proto.name / kmeans_tag(args)
    if rdir.exists():
        shutil.rmtree(rdir)
    rdir.mkdir(parents=True)
    log = rdir / "run.log"
    cmd = (f"cd {kdir} && {r.path(binary)} --outdir={r.path(rdir)} "
           f"{C_CONFIGS if r.image else CONFIG_DIR}/smoke_se.py -c {args.kmeans_cores} "
           f"--clusters {args.kmeans_clusters} --llc-slices {args.kmeans_llc_slices} "
           f"--cpu-type {args.cpu_type} -- ./kmeans {KMEANS_ARGS}")
    t = time.time()
    rc, to = r.run(cmd, log, rdir, timeout=args.kmeans_timeout)
    actual = final_means(rdir / "program.out")
    ok = rc == 0 and actual == expected
    detail = ""
    if not ok:
        if to:
            detail = "timeout"
        elif actual is None:
            detail = classify_failure(log, rdir / "program.err") or "no 'Final means' in output"
        else:
            detail = "output differs from native run"
    return StepResult(proto.name, kmeans_tag(args), "PASS" if ok else "FAIL",
                      detail, time.time() - t, str(log))


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #

def print_result(res: StepResult):
    mark = {"PASS": " OK ", "FAIL": "FAIL", "SKIP": "SKIP"}[res.status]
    print(f"  [{mark}] {res.protocol:<24} {res.step:<18} {res.seconds:7.0f}s  "
          f"{res.detail.splitlines()[0] if res.detail else ''}")
    if res.status == "FAIL" and res.detail.count("\n"):
        for line in res.detail.splitlines()[1:]:
            print(f"         {line}")


def write_report(out: Path, results: List[StepResult], protocols: List[Protocol]):
    steps = []
    for res in results:
        if res.step not in steps:
            steps.append(res.step)
    by = {(res.protocol, res.step): res for res in results}

    md = ["# gem5 smoke test", "", f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}", "",
          "| protocol | " + " | ".join(steps) + " |",
          "|---|" + "---|" * len(steps)]
    for p in protocols:
        row = [by[(p.name, s)].status if (p.name, s) in by else "-" for s in steps]
        md.append(f"| {p.name} | " + " | ".join(row) + " |")
    md += ["", "## Protocols", ""]
    md += [f"- `{p.name}`: `{p.src.resolve() if p.src else p.prebuilt}`" for p in protocols]
    fails = [res for res in results if res.status == "FAIL"]
    if fails:
        md += ["", "## Failures", ""]
        for res in fails:
            md += [f"### {res.protocol} / {res.step}", "", f"log: `{res.log}`", "",
                   "```", res.detail, "```", ""]
    (out / "summary.md").write_text("\n".join(md) + "\n")
    (out / "summary.json").write_text(json.dumps([res.__dict__ for res in results], indent=2))


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def parse_protocol(spec: str) -> Protocol:
    if "=" not in spec:
        raise argparse.ArgumentTypeError("expected NAME=DIR")
    name, src = spec.split("=", 1)
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", name):
        raise argparse.ArgumentTypeError(f"invalid protocol name '{name}'")
    src_path = Path(src).expanduser()
    if not src_path.is_dir():
        raise argparse.ArgumentTypeError(f"{src} is not a directory")
    return Protocol(name, src_path)


def parse_prebuilt(spec: str) -> Protocol:
    if "=" not in spec:
        raise argparse.ArgumentTypeError("expected NAME=PATH/TO/gem5.opt")
    name, binary = spec.split("=", 1)
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", name):
        raise argparse.ArgumentTypeError(f"invalid protocol name '{name}'")
    path = Path(binary).expanduser()
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"{binary} is not a file")
    return Protocol(name, None, path)


def run_protocol(r: Runner, p: Protocol, steps: List[str], args, lock: threading.Lock,
                 results: List[StepResult], protocols: List[Protocol]):
    """All steps of one protocol. Build failures skip the later steps (or only the tests with
    --keep-going); a prebuilt binary skips slicc and build."""
    def record(step_results: List[StepResult]):
        with lock:
            results.extend(step_results)
            for res in step_results:
                print_result(res)
            write_report(r.out, results, protocols)

    if p.prebuilt:
        (r.out / p.name).mkdir(parents=True, exist_ok=True)
        shutil.copy2(p.prebuilt, gem5_binary(r, p, args))
    failed = False
    for s in steps:
        if p.prebuilt and s in ("slicc", "build"):
            record([StepResult(p.name, s, "SKIP", f"prebuilt {p.prebuilt}")])
            continue
        no_binary = s in ("random", "kmeans") and not gem5_binary(r, p, args).exists()
        if (failed and not args.keep_going) or no_binary:
            reason = "no gem5 binary" if no_binary else "earlier step failed"
            if s == "random":
                record([StepResult(p.name, random_tag(*run), "SKIP", reason)
                        for run in args.random_runs])
            else:
                name = kmeans_tag(args) if s == "kmeans" else s
                record([StepResult(p.name, name, "SKIP", reason)])
            continue
        if s == "random":
            step_results = step_random(r, p, args)
        else:
            fn = {"slicc": step_slicc, "build": step_build, "kmeans": step_kmeans}[s]
            step_results = [fn(r, p, args)]
        record(step_results)
        if any(x.status == "FAIL" for x in step_results) and s in ("slicc", "build"):
            failed = True


def parse_random_runs(spec: str) -> List[Tuple[int, int, int, int]]:
    """CPUS:SEED[:CLUSTERS[:SLICES]] items, comma separated."""
    runs = []
    for item in spec.split(","):
        fields = [int(x) for x in item.split(":")]
        if len(fields) not in (2, 3, 4):
            raise argparse.ArgumentTypeError(f"bad random run '{item}' (CPUS:SEED[:CLUSTERS[:SLICES]])")
        cpus, seed, clusters, slices = (fields + [1, 1])[:4]
        runs.append((cpus, seed, clusters, slices))
    return runs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gem5", type=Path, default=os.environ.get("GEM5_DIR"), required=
                    "GEM5_DIR" not in os.environ, help="gem5 v23 source tree (Synapse gem5-S1_2_3)")
    ap.add_argument("--protocol", "-p", type=parse_protocol, action="append", default=[],
                    help="NAME=DIR with the protocol's .sm files (repeatable)")
    ap.add_argument("--prebuilt", type=parse_prebuilt, action="append", default=[],
                    help="NAME=PATH of a gem5.opt already built with a protocol, e.g. the Synapse "
                         "artifact's build/X86_<protocol>/gem5.opt: only the tests run (repeatable)")
    ap.add_argument("--parallel", type=int, default=1,
                    help="protocols processed at the same time (each builds with -j JOBS)")
    ap.add_argument("--out", type=Path, default=Path("gem5_smoke_out"))
    ap.add_argument("--steps", default=",".join(ALL_STEPS),
                    help=f"comma separated subset of {ALL_STEPS}")
    ap.add_argument("--image", default=DEFAULT_IMAGE)
    ap.add_argument("--no-docker", action="store_true", help="run on the host")
    ap.add_argument("-j", "--jobs", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--no-mold", action="store_true", help="use the default linker")
    ap.add_argument("--build-dir", metavar="NAME",
                    help="build every protocol in gem5/build/NAME, one after the other (saves disk, "
                         "not time: switching protocol recompiles almost everything); binaries are "
                         "copied to <out>/<protocol>/gem5.opt. Default: one build/X86_<protocol> "
                         "each, rebuilt incrementally when the protocol is regenerated")
    ap.add_argument("--build-timeout", type=int, default=4 * 3600)
    ap.add_argument("--random-runs", type=parse_random_runs, default="2:1,4:2,4:3,8:4",
                    help="CPUS:SEED[:CLUSTERS[:SLICES]] runs of the random tester; CLUSTERS L2s "
                         "(default 1) share the L1s, each split into SLICES slices interleaved by "
                         "address (default 1; needs an L1 generated for an LLC with slices) "
                         "(default: %(default)s)")
    ap.add_argument("--random-checks", type=int, default=20000)
    ap.add_argument("--random-timeout", type=int, default=1800)
    ap.add_argument("--no-ifetch", action="store_true",
                    help="random tester issues no instruction fetches")
    ap.add_argument("--kmeans-dir", type=Path,
                    help="Phoenix tests/kmeans directory with the built binary")
    ap.add_argument("--kmeans-cores", type=int, default=8)
    ap.add_argument("--kmeans-clusters", type=int, default=1,
                    help="number of L2s for kmeans (the artifact's NUMA system has 4)")
    ap.add_argument("--kmeans-llc-slices", type=int, default=1,
                    help="LLC slices per cluster for kmeans (the artifact's multi-host system has 8)")
    ap.add_argument("--kmeans-timeout", type=int, default=3600)
    ap.add_argument("--cpu-type", default="O3CPU", choices=["O3CPU", "TimingSimpleCPU"])
    ap.add_argument("--keep-going", action="store_true",
                    help="run later steps of a protocol even if an earlier one failed")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)
    if isinstance(args.random_runs, str):
        args.random_runs = parse_random_runs(args.random_runs)

    steps = [s.strip() for s in args.steps.split(",") if s.strip()]
    for s in steps:
        if s not in ALL_STEPS:
            ap.error(f"unknown step '{s}'")
    if "kmeans" in steps and args.kmeans_dir is None:
        print("note: --kmeans-dir not given, skipping the kmeans step")
        steps.remove("kmeans")
    protocols: List[Protocol] = args.protocol + args.prebuilt
    if not protocols:
        ap.error("give at least one --protocol or --prebuilt")
    names = [p.name for p in protocols]
    if len(set(names)) != len(names):
        ap.error("protocol names must be unique")

    gem5 = args.gem5.resolve()
    if not (gem5 / "SConstruct").exists():
        ap.error(f"{gem5} is not a gem5 source tree")
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    if args.kmeans_dir is not None:
        args.kmeans_dir = args.kmeans_dir.resolve()
    image = None if args.no_docker else args.image
    r = Runner(gem5, out, image, args.kmeans_dir, args.verbose)

    print(f"gem5:   {gem5}\noutput: {out}\nrunner: {'host' if image is None else image}")
    for p in args.protocol:
        dest = stage_protocol(p, gem5)
        print(f"staged {p.name:<24} {p.src} -> {dest.relative_to(gem5)}")
    if args.protocol:
        write_kconfig(gem5)
    if args.parallel > 1 and args.build_dir:
        ap.error("--parallel needs one build directory per protocol (drop --build-dir)")
    if "kmeans" in steps:
        kmeans_expected(r, args)  # native reference, once

    results: List[StepResult] = []
    lock = threading.Lock()
    with ThreadPoolExecutor(max_workers=max(1, args.parallel)) as pool:
        for future in [pool.submit(run_protocol, r, p, steps, args, lock, results, protocols)
                       for p in protocols]:
            future.result()
    write_report(out, results, protocols)

    print(f"\nreport: {out / 'summary.md'}")
    # SKIP: steps not run for a prebuilt binary (slicc, build)
    return 0 if all(res.status in ("PASS", "SKIP") for res in results) else 1


if __name__ == "__main__":
    sys.exit(main())
