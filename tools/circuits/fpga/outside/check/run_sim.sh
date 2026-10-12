#!/bin/sh
# Simulate every wrapper against the definition (Icarus Verilog from the oss-cad-suite).
# Usage: sh run_sim.sh            Output: one PASS or FAIL line per wrapper, also kept in sim_results.txt
export PATH="${OSS_CAD_SUITE:-/opt/oss-cad-suite}/bin:$PATH"
HERE=$(cd "$(dirname "$0")" && pwd)
STD=$(dirname "$HERE")
C=$STD/cores
WR=$STD/wrappers
OUT=${TMPDIR:-/tmp}/wht_standards_sim.$$
mkdir -p "$OUT"
: > "$HERE/sim_results.txt"
run() {  # module  N  W  latency  include-dir  core-file
    iverilog -g2012 -DDUT=$1 -DDUTNAME="\"$1\"" -DN=$2 -DW=$3 -DLAT=$4 -I "$5" -o "$OUT/$1.vvp" \
        "$HERE/tb_def.v" "$WR/${1#wht_}.v" "$6" || { echo "FAIL dut=$1 (did not compile)" | tee -a "$HERE/sim_results.txt"; return; }
    vvp -n "$OUT/$1.vvp" | grep -E "PASS|FAIL|MISMATCH" | tee -a "$HERE/sim_results.txt"
}
for w in 8 9 12 16; do
    run wht_8_xk265_c_w$w 8 $w 0 "$C/openasic-org_xk265/rtl" "$C/openasic-org_xk265/rtl/fme/fme_satd_8x8.v"
    run wht_8_xk265_r_w$w 8 $w 2 "$C/openasic-org_xk265/rtl" "$C/openasic-org_xk265/rtl/fme/fme_satd_8x8.v"
done
run wht_16_xk264_c_w9 16 9 0 "$C/openasic-org_xk264/rtl" "$C/openasic-org_xk264/rtl/intra/intra_hadamard4x4.v"
run wht_16_xk264_r_w9 16 9 2 "$C/openasic-org_xk264/rtl" "$C/openasic-org_xk264/rtl/intra/intra_hadamard4x4.v"
rm -rf "$OUT"
