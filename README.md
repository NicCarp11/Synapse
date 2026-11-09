<p align="center"><img src=".github/synapse-lockup.svg" alt="Synapse" width="360"></p>

Synapse synthesizes the cache coherence controllers of a system from three specifications and
writes them as SLICC state machines for gem5, together with a gem5 setup of the system:

- **protocols**: one stable-state specification per coherence domain (`specs/protocols/*.pcc`);
- **policies**: the caching policy of each controller between two domains (`specs/policies/caching.pol`);
- **topology**: the clusters, cores, memory and controllers of the system (`specs/topologies/*.yaml`).

It implements *Decoupling Protocol, Topology, and Policy for Automated Synthesis of Coherence
Controllers* (MICRO 2026). Project page: https://synapse-coherence.github.io.

## Quick start

Python 3.10 or newer:

```bash
pip install -r requirements.txt
python synapse.py generate specs/topologies/smp.yaml --out out/smp
python synapse.py generate specs/topologies/smp.yaml --out out/smp-moesi --set directory.protocol=MOESI
python synapse.py show specs/topologies/numa.yaml       # the resolved system, nothing generated
```

`generate` writes, for a system `<name>`:

| File | Content |
|---|---|
| `<name>_client_L1.sm` | the first-level cache |
| `<name>_client_manager_<cache>.sm` | each synthesized controller |
| `<name>_manager_directory.sm` | the directory |
| `<name>_msg.sm`, `<name>.slicc` | the messages and the file list gem5 builds the protocol from |
| `<name>_gem5.py` | the gem5 setup of the system |
| `system.json`, `synapse.log` | the resolved system and the generator's trace |

The name follows from the topology: `<protocols from the L1 up>_<policies>_<scenario>`, e.g.
`MESI_CXL_WB_INCL_MN`.

## Topologies

`specs/topologies/multi_host.yaml`:

```yaml
system: MN

rack:
  nodes:
    - cxl_memory_pool:
        nodes:
          - memory: {capacity: 8GiB}
          - directory: {protocol: CXL}
    - compute_node:
        count: 2
        nodes:
          - LLC: {protocol: MESI, policy: WB_INCL, capacity: 8MiB}
          - core:
              count: 9
              nodes:
                - L1: {capacity: 256KiB}
        interconnect: {connects: [LLC, core], type: direct, latency: 5ns}
  interconnect: {connects: [cxl_memory_pool, compute_node], type: direct, latency: 70ns, flit_size: 72B}
```

- The root is a cluster called by its name. Nodes are listed from the memory to the cores; the
  controllers on the way to the core form the hierarchy (directory, LLC, L1).
- A node is the `memory`, the `directory`, a `core`, a cluster (a name with `nodes`) or a cache
  (any other name). `count` replicates a cluster or the core; the `nodes` of a core are its
  private caches.
- Each controller but the L1 manages the caches below it with its `protocol`. A controller
  between two protocols also has a `policy` (`WB_INCL`, `WB_EXCL`, `WT_INCL`) and is synthesized.
- `interconnect` links the nodes of its cluster; `connects` names them and is checked. A
  cluster without count and interconnect only groups nodes (here the memory pool).
- `shared: true` makes a cache in a replicated cluster one cache for all its instances, with a
  slice of `capacity` in each (`chiplets.yaml`). A directory in a replicated cluster that does
  not hold the memory is sliced the same way.

A private L2 is one more line under `core`: `- L2: {protocol: MESI, policy: WB_INCL, capacity: 1MiB}`.

Parameters (defaults in brackets):

| Node | Parameters |
|---|---|
| document | `system`, `name`, `simulator` [`gem5-v23`; `alloy-gem5-v20`] |
| cluster | `count` [1], `interconnect`: `connects`, `type` (`direct`, `star`, `crossbar`, `ring`), `latency`, `flit_size` [256B] |
| core | `count` [1], `type` [`O3CPU`; `TimingSimpleCPU`], `clock` [2GHz], O3 sizes: `rob_entries`, `load_queue_entries`, `store_queue_entries`, `issue_queue_entries`, `branch_predictor`, `btb_entries` |
| cache | `capacity`, `protocol`, `policy`, `associativity` [8], `shared` [false], `slices` [1], `slice_select` [`interleaved`; `range`], `stalled_requests` [`recycle`; `park`], `transitions_per_cycle`, `link_latency` [5ns] |
| directory | `protocol`, `slices` [1], `link_latency` [5ns] |
| memory | `capacity`, `type` [`DDR5_4400_4x8`], `channels` [1, one per directory slice] |

`--set NODE.PARAMETER=VALUE` edits a topology from the command line, e.g. `--set core.count=16`,
`--set LLC.policy=WB_EXCL`.

| Topology | System |
|---|---|
| `smp.yaml` | S1: one socket, shared LLC |
| `smp_3level.yaml` | S1 with a private L2 per core |
| `numa.yaml` | S2: four sockets in a ring |
| `multi_host.yaml` | S3: two compute nodes and a CXL memory pool |
| `chiplets.yaml` | S4: eight chiplets on a fabric (alloy-gem5) |

## Verification

`verify` model-checks the synthesized controllers with CMurphi: one address, two first-level
caches, every synthesized controller, one more cache of the top protocol and the directory. It
checks that no state deadlocks and that a cache with write permission is the only one holding the
block (single writer, multiple readers).

```bash
git clone https://github.com/Errare-humanum-est/CMurphi && make -C CMurphi/src     # flex, bison, g++
python synapse.py verify specs/topologies/smp.yaml --out out/smp-murphi --murphi CMurphi
```

The model is compiled and run in docker (`--image`), or with the local `make` and `g++`
(`--no-docker`). `--memory` sizes CMurphi's state table in MB; `--caches` and `--top-caches` size
the model. `--deadlock-only` skips the single-writer check, which does not apply to the
release-consistent MESI-RC caches (their non-temporal stores write without ownership).

## gem5

The setup `<name>_gem5.py` runs a program on the system with gem5 built for the protocol `<name>`.

```bash
python Backend/gem5/gem5_smoke.py --gem5 <gem5 v23> --protocol MESI_MESI_WB_INCL_SMP=out/smp --steps slicc,build
<gem5 v23>/build/X86_MESI_MESI_WB_INCL_SMP/gem5.opt out/smp/MESI_MESI_WB_INCL_SMP_gem5.py --cores 8 -- <program>
```

`gem5_smoke.py` also runs the Ruby random tester and a multithreaded program on generated
controllers (`--help`). For `alloy-gem5-v20` the setup runs alloy's `configs/brg/sc3.py`; build
the protocol as any alloy protocol (write-through protocols with `DOSequencer_WT.cc`).

## Layout

| Path | Content |
|---|---|
| `synapse.py` | command line |
| `specs/` | protocols, policies, topologies |
| `Algorithms/Synapse/` | labels, policies, topology, synthesis (Alg. 1) |
| `Backend/SLICC/`, `Backend/gem5/` | SLICC generator; gem5 setups and build-and-test tool |
| `Backend/Murphi/` | Murphi model generator (`verify`) |
| `Algorithms/`, `DataObjects/`, `Parser/`, `Debug/`, `Backend/Common/`, `MurphiLitmusTests/` | protocol parser, the ProtoGen/HieraGen/HeteroGen passes the synthesis builds on, and their support code |
| `third_party/` | ANTLR 3 Python runtime |

## Citation

```bibtex
@inproceedings{carpentieri2026synapse,
  title     = {Decoupling Protocol, Topology, and Policy for
               Automated Synthesis of Coherence Controllers},
  author    = {Carpentieri, Nicolo and Lefort, Anatole and Schall, David
               and Pritzi, Julian and Bhatotia, Pramod},
  booktitle = {Proceedings of the 59th IEEE/ACM International
               Symposium on Microarchitecture (MICRO)},
  year      = {2026},
  address   = {Athens, Greece}
}
```

## License

MIT (`LICENSE`). `third_party/antlr3` is under the BSD license in its files.
