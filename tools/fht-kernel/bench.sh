#!/bin/sh
# bench.sh -- time this kernel against FFHT:  sh tools/fht-kernel/bench.sh
#
# x86-64 Linux with AVX2 and FMA only.  NOT RUN for revision 2 of this repository (22 October 2026): there was no
# x86 machine for it in that step.  The figures of measurements/2026-10-22/ come from the timing program there, of
# which this kernel is a cut-down copy (check_same_as_harness.py), not from this script.
#
# Needs: gcc (or CC), git, the internet (it fetches FFHT at commit fba727a3 into build/FFHT), taskset.
# Builds this library three times (8-point steps g20, tb8balS and tb8) and FFHT, all with the same compiler and
# flags (CFLAGS, default -O3 -mavx2 -mfma), into one program per precision; pins it to one core (CORE, default the
# last CPU) and times the four programs taking turns.  Leave the machine idle while it runs.
# Sizes: same array 2^6 to 2^20 (even), separate arrays (64 MiB in all, so the data comes from memory) 2^12, 2^16,
# 2^20.  About 10 minutes in all [estimate: 4 programs x 2.3 s per program and size x 11 sizes x 2 precisions].
# Output: build/bench_float.txt and build/bench_double.txt (RESULT and RATIO lines).
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
B=${WHTC_BUILD:-$HERE/build}
CC=${CC:-gcc}
CFLAGS=${CFLAGS:--O3 -mavx2 -mfma}
HARNESS=$HERE/../../measurements/2026-10-22/x86/harness-hybrid
[ "$(uname -s)" = Linux ] && [ "$(uname -m)" = x86_64 ] || { echo "bench.sh: x86-64 Linux only"; exit 2; }
grep -qw avx2 /proc/cpuinfo && grep -qw fma /proc/cpuinfo || { echo "bench.sh: this CPU lacks AVX2 or FMA"; exit 2; }
mkdir -p "$B"
cd "$HERE"
if [ ! -d "$B/FFHT" ]; then git clone -q https://github.com/FALCONN-LIB/FFHT.git "$B/FFHT"; fi
(cd "$B/FFHT" && git checkout -q fba727a3ff72c862260460631ae1cc8e3e44e861)
echo "== machine"; grep -m1 'model name' /proc/cpuinfo; $CC --version | head -1
for s in G20 TB8BALS TB8; do
  $CC $CFLAGS -DWHTC_STEP=$s -Dwhtc_fht_float=${s}_fht_float -Dwhtc_fht_double=${s}_fht_double \
      -c whtc_avx2.c -o "$B/bench_whtc_$s.o"
done
CORE=${CORE:-$(($(nproc) - 1))}
for p in float double; do
  d=""; [ $p = double ] && d="-DPREC_DOUBLE"
  $CC $CFLAGS $d -I"$B/FFHT" -I"$HARNESS" tests/bench_whtc.c "$B"/bench_whtc_G20.o "$B"/bench_whtc_TB8BALS.o \
      "$B"/bench_whtc_TB8.o "$B/FFHT/fht.c" "$B/FFHT/fast_copy.c" -o "$B/bench_whtc_$p" -lm
  # each run writes its file first, so that a crash stops the script (a pipe would hide it)
  taskset -c "$CORE" "$B/bench_whtc_$p" same 6 8 10 12 14 16 18 20 > "$B/bench_$p.txt" || { echo "bench.sh: $p same-array run failed"; exit 1; }
  taskset -c "$CORE" "$B/bench_whtc_$p" separate 12 16 20 >> "$B/bench_$p.txt" || { echo "bench.sh: $p separate-array run failed"; exit 1; }
  grep '^RATIO' "$B/bench_$p.txt" || { echo "bench.sh: no RATIO line in $B/bench_$p.txt"; exit 1; }
done
echo "done: $B/bench_float.txt, $B/bench_double.txt"
