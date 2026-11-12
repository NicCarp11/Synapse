# CMurphi, laid out as the tree `synapse.py verify --murphi` expects: $out/src/mu and
# $out/include (the model's Makefile compiles with MURPHIPATH=$out). $out/bin/mu is the same
# compiler for use on the command line.
{
  lib,
  stdenv,
  flex,
  byacc,
  src,
}:

stdenv.mkDerivation {
  pname = "cmurphi";
  version = "5.4.9.1";
  inherit src;

  nativeBuildInputs = [
    flex
    byacc
  ];

  makeFlags = [
    "-C"
    "src"
    "CPLUSPLUS=${stdenv.cc.targetPrefix}c++"
  ];
  # src/Makefile runs byacc once per output of `y.tab.c + y.tab.h: mu.y`
  enableParallelBuilding = false;

  installPhase = ''
    runHook preInstall
    mkdir -p $out/src $out/bin
    cp -r include ex LGPL-2.1 README.md MURPHI.md $out/
    install -m755 src/mu $out/src/mu
    ln -s ../src/mu $out/bin/mu
    runHook postInstall
  '';

  meta = {
    description = "Explicit-state model checker for Murphi (HeteroGen's fork)";
    homepage = "https://github.com/Errare-humanum-est/CMurphi";
    license = lib.licenses.lgpl21Plus;
    mainProgram = "mu";
    platforms = lib.platforms.unix;
  };
}
