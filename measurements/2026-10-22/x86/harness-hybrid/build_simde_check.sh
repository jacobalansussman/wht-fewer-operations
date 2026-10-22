#!/bin/bash
# build_simde_check.sh -- a non-x86 machine (written on an arm64 Mac): compile bench_hyb.c with SIMDe emulating AVX2 / AVX-512 and run the
# exactness gate natively, then compare the hybrid's step sequence with FFHT's fht_avx.c (check_plan.py).
# Correctness of the SOURCE only: FFHT itself is x86 asm and is gated on the Colab (run.sh); never time these binaries.
# (Rosetta was hung on the Mac on 21-22 Oct 2026, so no x86 binary runs here.)
set -u
cd "$(dirname "$0")"
SIMDE=${SIMDE:?set SIMDE to a SIMDe checkout, v0.8.2}
B=${B:-${TMPDIR:-/tmp}/simde-hyb}; mkdir -p "$B"
FFHT=${FFHT:?set FFHT to a checkout of FALCONN-LIB/FFHT at fba727a3}
rc=0
for cfg in "avx2_f32:0" "avx2_f64:2" "avx512_f32:1" "avx512_f64:3"; do
  nm=${cfg%%:*}; xt=${cfg#*:}
  clang -O1 -w -DUSE_SIMDE -DXT=$xt -I"$SIMDE" bench_hyb.c -o "$B/$nm" -lm || { echo "BUILD FAILED $nm"; exit 1; }
  "$B/$nm" check ${MAXL:-20} > "$B/check_$nm.txt" 2>&1; echo "$nm: $(tail -1 "$B/check_$nm.txt")"
  grep -q "^ALL PASS" "$B/check_$nm.txt" || rc=1
  "$B/$nm" plan 10 11 12 13 14 15 16 17 18 19 20 > "$B/plan_$nm.txt" 2>&1
done
python3 -I check_plan.py "$FFHT/fht_avx.c" float "$B/avx2_f32" 1 20 > "$B/plan_check_float.txt" 2>&1 || rc=1
tail -2 "$B/plan_check_float.txt"
python3 -I check_plan.py "$FFHT/fht_avx.c" double "$B/avx2_f64" 1 20 > "$B/plan_check_double.txt" 2>&1 || rc=1
tail -2 "$B/plan_check_double.txt"
exit $rc
