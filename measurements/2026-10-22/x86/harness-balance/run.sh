#!/bin/bash
# ax-h0 wave 16, Colab CPU job (x86): (1) does issuing half of the textbook's additions as FMA-by-+-1.0 ("port
# balancing") speed up an add-only Walsh-Hadamard pass on this CPU, and (2) against that balanced textbook, do the
# 19-line (5/6) and 52/56/60-line (3/4 family, depth-limited) circuits win?  llvm-mca 23 predicts: balancing -28 to
# -50 % on Haswell/Broadwell, Zen 2-5, Sapphire Rapids (0 on Skylake / Ice Lake); circuits win only on Sapphire Rapids
# AVX2 (G52 0.84) and Ice Lake AVX-512 (G19 0.81, G52 0.83).  This job measures it.
# Any CPU runtime; ~3-5 min.  Prefer AMD EPYC (Zen 2/3/4) and Intel Sapphire Rapids (model 143) / Ice Lake (106).
# Shared preamble (22 Oct 2026): machine and compilers first (az_pre.sh, out/machine.txt); binaries OUTSIDE this folder
#   ($AZ_BUILD = /content/build/x86-balance); every binary's exact check (CHECK_ONLY=1) must pass and the machine must
#   be quiet (az_quiet on CPU 1 and its SMT sibling) before any timing (ay-k0 fix 14: this job had no gate; the
#   binary's own check already stopped it before timing, but a failure was hidden behind tee). Original: run.sh.orig.
set -u; cd "$(dirname "$0")"; mkdir -p out; exec > >(tee out/log.txt) 2>&1
. ./az_pre.sh x86-balance
az_machine
command -v gcc >/dev/null || { apt-get update -qq && apt-get install -y -qq build-essential >/dev/null; }
command -v taskset >/dev/null || apt-get install -y -qq util-linux >/dev/null 2>&1
date; gcc --version | head -1
B=$AZ_BUILD; SIBS=$(cat /sys/devices/system/cpu/cpu1/topology/thread_siblings_list 2>/dev/null || echo 1)
grep -m1 -o 'avx512f' /proc/cpuinfo && HAVE512=1 || HAVE512=0
python3 make_bench.py avx2 && python3 make_bench.py avx512 || exit 1
gcc -O3 -march=native -o $B/bal_avx2 bench_avx2.c || exit 1
[ $HAVE512 = 1 ] && { gcc -O3 -march=native -mprefer-vector-width=512 -o $B/bal_avx512 bench_avx512.c || exit 1; }
# assembly evidence: one vector instruction per line, spills
objdump -d --no-show-raw-insn $B/bal_avx2 > out/bal_avx2.dis
BINS=bal_avx2; [ $HAVE512 = 1 ] && BINS="$BINS bal_avx512"
for b in $BINS; do CHECK_ONLY=1 $B/$b > out/check_$b.txt 2>&1; rc=$?; grep -c "PASS (exact)" out/check_$b.txt | sed "s/^/$b: exact kernels: /"
  { [ $rc = 0 ] && ! grep -q FAIL out/check_$b.txt; } || az_stop "$b check failed (out/check_$b.txt)"; done
for r in 1 2; do for b in $BINS; do
  az_quiet "$b round $r" "$SIBS"; taskset -c 1 $B/$b > out/res_${b#bal_}_r$r.txt 2>&1; cat out/res_${b#bal_}_r$r.txt
done; done
date
