# Phoenix 2.0, the shared-memory MapReduce benchmarks. gem5_smoke.py runs kmeans in gem5 and on
# the host and compares their outputs: --kmeans-dir $out/tests/kmeans.
{
  lib,
  stdenv,
  src,
}:

stdenv.mkDerivation {
  pname = "phoenix";
  version = "2.0";
  src = "${src}/phoenix-2.0";

  makeFlags = [
    "CC=${stdenv.cc.targetPrefix}cc"
    "AR=${stdenv.cc.targetPrefix}ar"
    "RANLIB=${stdenv.cc.targetPrefix}ranlib"
  ];

  installPhase = ''
    runHook preInstall
    mkdir -p $out/bin $out/lib
    cp -r include $out/
    cp lib/libphoenix.a $out/lib/
    for test in tests/*/; do
      name=$(basename "$test")
      mkdir -p "$out/tests/$name"
      for program in "$test"*; do
        if [ -f "$program" ] && [ -x "$program" ]; then
          install -m755 "$program" "$out/tests/$name/"
          ln -s "../tests/$name/$(basename "$program")" "$out/bin/"
        fi
      done
    done
    runHook postInstall
  '';

  meta = {
    description = "Shared-memory MapReduce benchmarks (Phoenix 2.0)";
    homepage = "https://github.com/kozyraki/phoenix";
    license = lib.licenses.bsd3;
    platforms = lib.platforms.linux;
  };
}
