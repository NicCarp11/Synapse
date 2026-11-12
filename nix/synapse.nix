# The Synapse command line: synapse.py with its Python dependencies. `verify --no-docker`
# compiles the CMurphi model with the make and g++ on its PATH.
#
# It reads the protocols and policies next to the topology first and then from its own copy of
# specs/, the one committed with the flake: to work on specs/, run `python synapse.py` from the
# checkout in `nix develop` instead.
{
  lib,
  stdenvNoCC,
  stdenv,
  python3,
  makeWrapper,
  gnumake,
  src,
  version,
}:

let
  python = python3.withPackages (
    ps: with ps; [
      colorama
      graphviz
      networkx
      pyyaml
      tabulate
    ]
  );
in
stdenvNoCC.mkDerivation {
  pname = "synapse";
  inherit version src;

  nativeBuildInputs = [ makeWrapper ];

  dontConfigure = true;
  dontBuild = true;

  installPhase = ''
    runHook preInstall
    mkdir -p $out/share/synapse
    cp -r . $out/share/synapse
    ${python.interpreter} -m compileall -q $out/share/synapse > /dev/null
    # synapse.py re-executes itself with PYTHONHASHSEED=0 unless it is set already.
    makeWrapper ${python.interpreter} $out/bin/synapse \
      --add-flags $out/share/synapse/synapse.py \
      --set PYTHONHASHSEED 0 \
      --prefix PATH : ${
        lib.makeBinPath [
          gnumake
          stdenv.cc
        ]
      }
    runHook postInstall
  '';

  passthru = { inherit python; };

  meta = {
    description = "Synthesis of cache coherence controllers from protocol, topology and policy specifications";
    homepage = "https://synapse-coherence.github.io";
    license = lib.licenses.mit;
    mainProgram = "synapse";
    platforms = lib.platforms.unix;
  };
}
