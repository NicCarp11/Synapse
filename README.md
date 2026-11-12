<p align="center"><img src=".github/synapse-lockup.svg" alt="Synapse" width="360"></p>

Synapse synthesizes the cache coherence controllers of a system from three specifications and
writes them as SLICC state machines for gem5, together with a gem5 setup of the system:

- **protocols**: one stable-state specification per coherence domain (`specs/protocols/*.pcc`);
- **policies**: the caching policy of each controller between two domains (`specs/policies/caching.pol`);
- **topology**: the clusters, cores, memory and controllers of the system (`specs/topologies/*.yaml`).

It implements *Decoupling Protocol, Topology, and Policy for Automated Synthesis of Coherence
Controllers* (MICRO 2026). Project page: https://synapse-coherence.github.io.

## Credits and provenance

Synapse builds on **ProtoGen/HieraGen/HeteroGen** (Nicolai Oswald et al., University of Edinburgh) and **vCXLGen** (Anatole Lefort et al., Technical University of Munich); this repository is directly derived from their code. It is a fork of [HeteroGen](https://github.com/Errare-humanum-est/HeteroGen), and its history keeps the author of every change.

<details>
<summary><b>What is inherited from them, and how to cite</b></summary>

<br>

**ProtoGen / HieraGen / HeteroGen (\*Gen tools)**: Nicolai Oswald, Vijay Nagarajan, Daniel J. Sorin et al.,
The University of Edinburgh ([ProtoGen](https://github.com/Errare-humanum-est/ProtoGen),
[HieraGen](https://github.com/Errare-humanum-est/HieraGen), [HeteroGen](https://github.com/Errare-humanum-est/HeteroGen)).
The ProtoCC language and parser (`Parser/`, `ProtoCC.g`), the protocol data model (`DataObjects/`),
the concurrency algorithm of ProtoGen (`Algorithms/ProtoDirectory`,
HieraGen's proxy cache (`Algorithms/ProtoDirectory`),
the Murphi backend and model-checking flow (`Backend/Murphi`,
`MurphiLitmusTests/`) originate from these tools. Files derived from them keep their original copyright headers.

**vCXLGen**: Systems Research Group, TUM ([TUM-DSE/vCXLGen](https://github.com/TUM-DSE/vCXLGen)).
vCXLGen extended HeteroGen to synthesize and verify CXL bridges. Synapse starts from vCXLGen's code base and reuses or modifies most of its core for (hierarchical) controller generation.

**SLICC back end** (`Backend/SLICC/`): developed by Nicolai Oswald, Theo Olausson, Nicolò Carpentieri,
Anatole Lefort, David Schall, Julian Pritzi and Simon Dittrich. It was first released on the
[`slicc` branch of HeteroGen](https://github.com/Errare-humanum-est/HeteroGen/tree/slicc). If you use it,
please cite HeteroGen and Synapse.

**New in Synapse:** the decoupled protocol / topology / policy specification (`specs/`) and the synthesis
built on it (`Algorithms/Synapse/`), the extensions of the SLICC back end that it needs, the gem5 setup
(`Backend/gem5/`), the `synapse.py` frontend, and the changes to the inherited modules that these need.

If you use Synapse, please also cite the work it builds on:

```bibtex
@inproceedings{oswald2018protogen,
  author    = {Oswald, Nicolai and Nagarajan, Vijay and Sorin, Daniel J.},
  title     = {{ProtoGen}: Automatically Generating Directory Cache Coherence Protocols from Atomic Specifications},
  booktitle = {Proceedings of the 45th Annual International Symposium on Computer Architecture (ISCA)},
  pages     = {247--260},
  year      = {2018},
  doi       = {10.1109/ISCA.2018.00030}
}

@inproceedings{oswald2020hieragen,
  author    = {Oswald, Nicolai and Nagarajan, Vijay and Sorin, Daniel J.},
  title     = {{HieraGen}: Automated Generation of Concurrent, Hierarchical Cache Coherence Protocols},
  booktitle = {Proceedings of the 47th Annual International Symposium on Computer Architecture (ISCA)},
  year      = {2020}
}

@inproceedings{oswald2022heterogen,
  author    = {Oswald, Nicolai and Nagarajan, Vijay and Sorin, Daniel J. and Gavrielatos, Vasilis and Olausson, Theo and Carr, Reece},
  title     = {{HeteroGen}: Automatic Synthesis of Heterogeneous Cache Coherence Protocols},
  booktitle = {IEEE International Symposium on High-Performance Computer Architecture (HPCA)},
  pages     = {756--771},
  year      = {2022},
  doi       = {10.1109/HPCA53966.2022.00061}
}

@inproceedings{lefort2026vcxlgen,
  author    = {Lefort, Anatole and Pritzi, Julian and Carpentieri, Nicol{\`o} and Schall, David and Dittrich, Simon and Chakraborty, Soham and Oswald, Nicolai and Bhatotia, Pramod},
  title     = {{vCXLGen}: Automated Synthesis and Verification of {CXL} Bridges for Heterogeneous Architectures},
  booktitle = {Proceedings of the 31st ACM International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS)},
  pages     = {2177--2196},
  year      = {2026},
  doi       = {10.1145/3779212.3790245}
}
```

</details>


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

### With Nix

`nix develop` opens a shell with what `verify` and the gem5 tools need, without docker: Python
with the packages of `requirements.txt`, CMurphi (`$CMURPHI`, the default of `verify --murphi`),
the toolchain gem5 v23.1 builds with (GCC 13, Python 3.11, SCons 4.8, mold) and Phoenix's kmeans
(`$KMEANS_DIR`).

```bash
nix develop
python synapse.py verify specs/topologies/smp.yaml --out out/smp-murphi --no-docker
gem5-tree gem5     # a writable gem5 v23.1 tree, $GEM5_DIR in later shells
python Backend/gem5/gem5_smoke.py --no-docker --gem5 gem5 --protocol MESI_MESI_WB_INCL_SMP=out/smp \
    --kmeans-dir $KMEANS_DIR
```

`nix run . -- generate ...` runs a copy of `synapse.py` that reads protocols and policies from its
own copy of `specs/`, which holds only the files git tracks; `nix build .#cmurphi`, `.#phoenix` and
`.#gem5-tree` build the tools alone.

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
| `rocketchip.yaml` | RocketChip with SiFive's inclusive L2 (Chipyard's `RocketConfig`), TileLink TL-C (`TileLink.pcc`) at both levels |

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
| `Backend/SLICC/` | SLICC back end |
| `Backend/gem5/` | gem5 setups and build-and-test tool |
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
