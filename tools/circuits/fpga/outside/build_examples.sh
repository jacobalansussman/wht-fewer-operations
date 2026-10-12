#!/bin/sh
# How to build the two outside cores with the open tools.
# It synthesises each wrapper for the iCE40 with Yosys and prints the cell counts.
# It does not place and route, and it does not touch the board.
# Usage: sh build_examples.sh [outdir]       (default outdir: a temporary folder; logs and counts go there)
# Tools: the oss-cad-suite, release 2026-10-11; set OSS_CAD_SUITE to its unpacked folder.
# The two cores are not in this repository: clone them into cores/ first (see ../README.md).
export PATH="${OSS_CAD_SUITE:-/opt/oss-cad-suite}/bin:$PATH"
STD=$(cd "$(dirname "$0")" && pwd)
C=$STD/cores
WR=$STD/wrappers
RTL=$(dirname "$STD")/rtl/v          # the designs written by gen_rtl.py (read only)
G9=$STD/gen_w9                       # 9-bit designs written here with the same gen_rtl.py (see REPORT.md)
find_v() { if [ -f "$RTL/$1.v" ]; then echo "$RTL/$1.v"; elif [ -f "$G9/$1.v" ]; then echo "$G9/$1.v"; fi; }
OUT=${1:-${TMPDIR:-/tmp}/wht_standards_build}
mkdir -p "$OUT"
synth() {  # top-module  files...   (an -I<dir> argument may come first)
    top=$1; shift
    inc=""
    case "$1" in -I*) inc="$1"; shift ;; esac
    yosys -q -l "$OUT/$top.log" -p "read_verilog $inc $*; synth_ice40 -top $top; tee -o $OUT/$top.stat stat" >/dev/null 2>&1 \
        || { echo "$top: yosys failed, see $OUT/$top.log"; return; }
    python3 -I - "$OUT/$top.stat" "$top" <<'PY'
import re, sys
t = open(sys.argv[1]).read()
def n(cell):
    m = re.search(r"^\s*(\d+)\s+" + cell + r"\s*$", t, re.M) or re.search(r"^\s*" + cell + r"\s+(\d+)\s*$", t, re.M)
    return int(m.group(1)) if m else 0
lut, carry = n("SB_LUT4"), n("SB_CARRY")
dff = sum(int(a or b) for a, b in re.findall(r"^\s*(?:(\d+)\s+SB_DFF\w*|SB_DFF\w*\s+(\d+))\s*$", t, re.M))
print(f"{sys.argv[2]:28s} SB_LUT4 {lut:5d}  SB_CARRY {carry:5d}  flip-flops {dff:5d}")
PY
}
for w in 8 9 12 16; do
    synth wht_8_xk265_c_w$w -I$C/openasic-org_xk265/rtl $C/openasic-org_xk265/rtl/fme/fme_satd_8x8.v $WR/8_xk265_c_w$w.v
    for d in textbook ours; do f=$(find_v 8_${d}_c_w$w); [ -n "$f" ] && synth wht_8_${d}_c_w$w "$f"; done
done
synth wht_16_xk264_c_w9 -I$C/openasic-org_xk264/rtl $C/openasic-org_xk264/rtl/intra/intra_hadamard4x4.v $WR/16_xk264_c_w9.v
for d in textbook ours; do f=$(find_v 16_${d}_c_w9); [ -n "$f" ] && synth wht_16_${d}_c_w9 "$f"; done
echo "logs and stat files: $OUT"
