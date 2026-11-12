# gem5 is built once per generated protocol, inside its own source tree: gem5_smoke.py copies the
# .sm files into src/custom/smoke/ and builds there. `gem5-tree DIR` makes that writable tree from
# the pinned gem5 source.
{
  writeShellApplication,
  coreutils,
  src,
  version,
}:

writeShellApplication {
  name = "gem5-tree";
  runtimeInputs = [ coreutils ];
  text = ''
    case "''${1:-}" in
      -h | --help)
        echo "usage: gem5-tree [DIR]"
        echo "Copies the gem5 ${version} source to DIR (default: ./gem5), writable, for"
        echo "Backend/gem5/gem5_smoke.py --gem5 DIR (or GEM5_DIR=DIR)."
        exit 0
        ;;
    esac
    dest=''${1:-gem5}
    if [ -e "$dest" ]; then
      echo "gem5-tree: $dest exists" >&2
      exit 1
    fi
    cp -r ${src} "$dest"
    chmod -R u+w "$dest"
    echo "gem5 ${version} is in $dest. For gem5_smoke.py:"
    echo "  export GEM5_DIR=$(realpath "$dest")"
  '';
}
