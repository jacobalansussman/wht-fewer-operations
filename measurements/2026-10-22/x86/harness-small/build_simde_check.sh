#!/bin/bash
# build_simde_check.sh -- a non-x86 machine (written on an arm64 Mac): compile bench_small.c with SIMDe emulating AVX2 / AVX-512, run the
# exactness gate natively (every program, every size 2^1..2^12 with a batch of 3, every timed size with its timing batch,
# broken copies), then compare the hyb plans with FFHT's fht_avx.c (check_plan.py, through the forwarded `trace` mode).
# Correctness of the SOURCE only: FFHT itself is x86 asm and is gated on the Colab (run.sh); never time these binaries.
# (Rosetta was hung on the Mac on 21-22 Oct 2026, so no x86 binary runs here.)
set -u
cd "$(dirname "$0")"
SIMDE=${SIMDE:?set SIMDE to a SIMDe checkout, v0.8.2}
B=${B:-${TMPDIR:-/tmp}/simde-hyb-small}; mkdir -p "$B"
FFHT=${FFHT:?set FFHT to a checkout of FALCONN-LIB/FFHT at fba727a3}
SIZES=${SIZES:-"6 7 8 9 10 12"}
rc=0
for cfg in "avx2_f32:0" "avx2_f64:2" "avx512_f32:1" "avx512_f64:3"; do
  nm=${cfg%%:*}; xt=${cfg#*:}
  clang -O1 -w -DUSE_SIMDE -DXT=$xt -I"$SIMDE" bench_small.c -o "$B/$nm" -lm || { echo "BUILD FAILED $nm"; exit 1; }
  BATCH_KB=${BATCH_KB:-512} "$B/$nm" check 12 $SIZES > "$B/check_$nm.txt" 2>&1
  echo "$nm: $(grep -c 'FAIL (caught, good)' "$B/check_$nm.txt") broken-copy runs caught, $(grep -c 'PASS' "$B/check_$nm.txt") PASS lines, $(grep -v 'caught, good' "$B/check_$nm.txt" | grep -c 'FAIL') other FAIL lines / $(tail -1 "$B/check_$nm.txt")"
  grep -q "^ALL PASS" "$B/check_$nm.txt" || rc=1
  "$B/$nm" list $SIZES > "$B/list_$nm.txt" 2>&1
done
python3 -I check_plan.py "$FFHT/fht_avx.c" float "$B/avx2_f32" 1 20 > "$B/plan_check_float.txt" 2>&1 || rc=1
tail -2 "$B/plan_check_float.txt"
python3 -I check_plan.py "$FFHT/fht_avx.c" double "$B/avx2_f64" 1 20 > "$B/plan_check_double.txt" 2>&1 || rc=1
tail -2 "$B/plan_check_double.txt"
exit $rc
