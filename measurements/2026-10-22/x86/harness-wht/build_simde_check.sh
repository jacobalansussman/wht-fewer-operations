#!/bin/bash
# build_simde_check.sh: compile bench_k0.c for a non-x86 (here: arm64) machine with SIMDe emulating AVX2 / AVX-512 and run the check.
# Correctness of the source only (kernels, passes, interleave, in-lane stages, plans); FFHT is x86 asm and is checked
# on the Colab. Used on 21 Oct 2026 because Rosetta was hung on the Mac (every x86 process stuck in state U).
set -u
cd "$(dirname "$0")"
SIMDE=${SIMDE:?set SIMDE to a SIMDe checkout, v0.8.2}; B=${B:-${TMPDIR:-/tmp}/simde-wht}; mkdir -p $B
rc=0
for cfg in "avx2_f32:0" "avx2_f64:2" "avx512_f32:1" "avx512_f64:3"; do
  nm=${cfg%%:*}; xt=${cfg#*:}
  clang -O1 -w -DUSE_SIMDE -DXT=$xt -I$SIMDE bench_k0.c -o $B/$nm -lm || { echo "BUILD FAILED $nm"; exit 1; }
  $B/$nm check ${MAXL:-16} > $B/check_$nm.txt 2>&1; echo "$nm: $(tail -1 $B/check_$nm.txt)"
  grep -q "^ALL PASS" $B/check_$nm.txt || rc=1
done
exit $rc
