#!/bin/bash
# setup_tools.sh (ax-k1, wave 16): the open FPGA tools on a fresh Ubuntu x86-64 runtime (Colab), the SAME builds as the Mac.
#
#   1. YosysHQ oss-cad-suite, tag 2026-10-11, linux-x64: the very release the Mac runs (darwin-arm64 of the same tag):
#      Yosys 0.69+274 (7513f8df8), nextpnr 0.11.1-59-g837d0eed (ice40, ecp5, nexus, himbaechel/gowin), icestorm,
#      iverilog, verilator, sby, eqy, z3, boolector, yices, bitwuzla.
#   2. openXC7 (Xilinx 7-series place and route without Vivado), release 2026-10-19 of
#      cavearr/toolchain-openxc7-releases (the build apio packages as "openxc7"; a stable, not nightly, release):
#      nextpnr-xilinx = openXC7/nextpnr e7a6fb0e (himbaechel, uarch xilinx), prjxray-db 6a6debcd, prjxray 317fdc13,
#      chipdbs prebuilt for xc7a50t/100t/200t, xc7s25/50/100, xc7z010/020/030/045/100 (no Kintex in this release).
#      The same release for darwin-arm64 runs on the Mac (on an external drive).
# Both archives are checked against the SHA-256 digests GitHub lists for them (read 21 Oct 2026 from the release API).
# Installs into $TOOLS (default /content/fpga-tools), which survives between jobs of one runtime; a second run only
# checks.  Nothing is installed system-wide.
# Prints DONE-TOOLS at the end only if every tool started and printed its version.
set -u
TOOLS=${TOOLS:-/content/fpga-tools}
mkdir -p "$TOOLS/dl"
cd "$TOOLS"

OCS_TAG=2026-10-11; OCS_FILE=oss-cad-suite-linux-x64-20261011.tgz
OCS_SHA=fc29330a392eecd0d60d220d3d10294ccbcf72fb2860d2b6dcc2054ad2444d75
OCS_URL=https://github.com/YosysHQ/oss-cad-suite-build/releases/download/$OCS_TAG/$OCS_FILE
OXC_TAG=2026-10-19; OXC_FILE=openxc7-toolchain-linux-x86-64-20261019.tgz
OXC_SHA=383785f4af92809671f08ebd7c97660c5d01f0145167538bb10667d9b929656c
OXC_URL=https://github.com/cavearr/toolchain-openxc7-releases/releases/download/$OXC_TAG/$OXC_FILE

fetch() {  # url file sha
  local url=$1 f=$2 sha=$3
  if [ -f "dl/$f" ] && [ "$(sha256sum "dl/$f" | cut -d' ' -f1)" = "$sha" ]; then echo "have $f"; return 0; fi
  echo "download $f"; curl -sSfL --retry 3 -o "dl/$f.part" "$url" || { echo "FAIL download $f"; return 1; }
  local got; got=$(sha256sum "dl/$f.part" | cut -d' ' -f1)
  [ "$got" = "$sha" ] || { echo "FAIL checksum $f: $got != $sha"; rm -f "dl/$f.part"; return 1; }
  mv "dl/$f.part" "dl/$f"
}

# ay-k1: the apt step (time, python3-venv, numactl) was removed: nothing in this kit uses them, and apt-get install
# without apt-get update can fail or wait on a dpkg lock held by the runtime's own setup.

fetch "$OCS_URL" "$OCS_FILE" "$OCS_SHA" || exit 1
fetch "$OXC_URL" "$OXC_FILE" "$OXC_SHA" || exit 1
[ -x oss-cad-suite/bin/yosys ] || { echo "unpack oss-cad-suite"; tar xzf "dl/$OCS_FILE" || exit 1; }
[ -x openxc7/bin/nextpnr-xilinx ] || { echo "unpack openxc7"; mkdir -p openxc7 && tar xzf "dl/$OXC_FILE" -C openxc7 || exit 1; }

cat > "$TOOLS/env.sh" <<EOF
export OSS_CAD_SUITE=$TOOLS/oss-cad-suite
export OPENXC7=$TOOLS/openxc7
export PATH=$TOOLS/oss-cad-suite/bin:\$PATH
EOF
. "$TOOLS/env.sh"
ok=1
v() { local o; o=$("$@" 2>&1 | head -1); echo "  $* -> $o"; [ -n "$o" ] || ok=0; }
echo "== versions"
v yosys -V
v nextpnr-ice40 --version
v nextpnr-ecp5 --version
v nextpnr-nexus --version
v nextpnr-himbaechel --version
v "$OPENXC7/bin/nextpnr-xilinx" --version
v iverilog -V
v verilator --version
v sby --help
yosys -V | grep -q '0.69+274' || { echo "FAIL: yosys is not 0.69+274"; ok=0; }
nextpnr-ecp5 --version 2>&1 | grep -q 'nextpnr-0.11.1-59-g837d0eed' || { echo "FAIL: nextpnr is not 0.11.1-59-g837d0eed"; ok=0; }
"$OPENXC7/bin/nextpnr-xilinx" --version 2>&1 | grep -q e7a6fb0e || { echo "FAIL: nextpnr-xilinx is not e7a6fb0e"; ok=0; }
ls "$OPENXC7/share/nextpnr/himbaechel/xilinx/"chipdb-*.bin | sed 's/^/  chipdb /'
[ $ok = 1 ] && echo DONE-TOOLS || { echo "TOOLS NOT READY"; exit 1; }
