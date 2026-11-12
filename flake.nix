{
  description = "Synapse: synthesis of cache coherence controllers, with CMurphi and gem5 v23.1";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
    # HeteroGen's CMurphi, the model checker of `synapse.py verify`.
    cmurphi = {
      url = "github:Errare-humanum-est/CMurphi/1.0.0";
      flake = false;
    };
    # The gem5 the SLICC back end and Backend/gem5 are written for ("gem5 v23"): its build is
    # configured with Kconfig (gem5_smoke.py's `scons defconfig`/`setconfig`) and it has
    # SimpleBTB (setup_v23.py), both new in v23.1.
    gem5 = {
      url = "github:gem5/gem5/v23.1.0.0";
      flake = false;
    };
    # Phoenix 2.0, whose kmeans gem5_smoke.py runs on the generated controllers.
    phoenix = {
      url = "github:kozyraki/phoenix";
      flake = false;
    };
  };

  outputs =
    { self, nixpkgs, ... }@inputs:
    let
      inherit (nixpkgs) lib;
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];
      forAllSystems = f: lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});

      gem5Version = "v23.1.0.0";

      synapseSource = lib.fileset.toSource {
        root = ./.;
        fileset = lib.fileset.unions [
          ./synapse.py
          ./Algorithms
          ./Backend
          ./DataObjects
          ./Debug
          ./MurphiLitmusTests
          ./Parser
          ./specs
          ./third_party
          ./LICENSE
        ];
      };
    in
    {
      packages = forAllSystems (pkgs: rec {
        cmurphi = pkgs.callPackage ./nix/cmurphi.nix { src = inputs.cmurphi; };
        synapse = pkgs.callPackage ./nix/synapse.nix {
          src = synapseSource;
          version = "0-unstable-${builtins.substring 0 8 self.lastModifiedDate}";
        };
        gem5-tree = pkgs.callPackage ./nix/gem5-tree.nix {
          src = inputs.gem5;
          version = gem5Version;
        };
        phoenix = pkgs.callPackage ./nix/phoenix.nix { src = inputs.phoenix; };
        default = synapse;
      });

      devShells = forAllSystems (
        pkgs:
        let
          packages = self.packages.${pkgs.stdenv.hostPlatform.system};
          # gem5 v23.1 embeds Python through its bundled pybind11 2.10, which supports Python up
          # to 3.11, and was released for GCC up to 13.
          gem5Python = pkgs.python311;
          gem5Stdenv = pkgs.gcc13Stdenv;
          # gem5 v23.1 calls CheckLibWithHeader(libs, header, language, call) positionally, and
          # SCons 4.9 added an argument before `call`: its configure checks (zlib) then fail.
          gem5Scons = pkgs.scons.overridePythonAttrs (_: rec {
            version = "4.8.1";
            src = pkgs.fetchFromGitHub {
              owner = "SCons";
              repo = "scons";
              tag = version;
              hash = "sha256-3B7DrWfHVJBs19mWAlm4/EGbu6FqppIq3Q1vH2Xsj6U=";
            };
          });
        in
        {
          default = (pkgs.mkShell.override { stdenv = gem5Stdenv; }) {
            packages = [
              # synapse.py (generate, show, labels, verify)
              packages.synapse.python
              pkgs.graphviz
              # verify: the model is compiled with CMurphi, make and g++ (--no-docker)
              packages.cmurphi
              pkgs.gnumake
              # gem5: a writable source tree, and what gem5_smoke.py --no-docker builds it with
              packages.gem5-tree
              gem5Scons
              pkgs.m4
              pkgs.pkg-config
              pkgs.mold
            ];
            buildInputs = [
              pkgs.zlib
              pkgs.libpng
              pkgs.gperftools
            ];

            # verify --murphi $CMURPHI
            CMURPHI = packages.cmurphi;
            # gem5_smoke.py --kmeans-dir $KMEANS_DIR
            KMEANS_DIR = "${packages.phoenix}/tests/kmeans";
            # gem5's SConstruct links the interpreter python-config names into gem5.
            PYTHON_CONFIG = "${gem5Python}/bin/python3.11-config";

            shellHook = ''
              if [ -z "''${GEM5_DIR:-}" ] && [ -d "$PWD/gem5/src/mem/ruby" ]; then
                export GEM5_DIR="$PWD/gem5"
              fi
            '';
          };
        }
      );

      formatter = forAllSystems (pkgs: pkgs.nixfmt);
    };
}
