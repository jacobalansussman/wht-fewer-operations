#!/bin/sh
# test.sh -- build the kernel and run its tests:  sh tools/fht-kernel/test.sh
#
# Needs a C compiler (CC, default cc) and the C library's libm; Python 3 for the comparison with the timed code;
# a C++ compiler (CXX, default c++) only for the C++ overloads test.  Builds into tools/fht-kernel/build/.
#   - On x86-64 with AVX2 and FMA it builds and tests the AVX2 code (and the portable code beside it).
#   - Elsewhere it builds and tests the portable code.
#   - With SIMDE_DIR pointing at a checkout of SIMDe (https://github.com/simd-everywhere/simde, v0.8.2 was used), it
#     also builds the AVX2 code through SIMDe and tests it, on any machine.  WHTC_FETCH_SIMDE=1 fetches SIMDe v0.8.2
#     into build/simde first (needs git and the internet).
# For each build: the exactness test (tests/test_exact.c) for each of the three steps; the rounding table
# (tests/test_rounding.c); the deliberately broken copy (-DWHTC_BREAK: one line of g20 changed), which must fail;
# code written for FFHT linked against the library under FFHT's names.  Any failure stops the script with exit 1.
# The last line is printed only when everything passed.
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
B=${WHTC_BUILD:-$HERE/build}
CC=${CC:-cc}
CXX=${CXX:-c++}
CFLAGS=${CFLAGS:--O2}
mkdir -p "$B"
cd "$HERE"

echo "== machine: $(uname -s) $(uname -m); compiler: $($CC --version 2>&1 | head -1)"

# ---- which code can run natively here
NATIVE="-DWHTC_PLAIN"; NATIVE_NAME="portable C"
if [ "$(uname -m)" = x86_64 ] || [ "$(uname -m)" = amd64 ]; then
  if [ -r /proc/cpuinfo ] && grep -qw avx2 /proc/cpuinfo && grep -qw fma /proc/cpuinfo; then
    NATIVE="-mavx2 -mfma"; NATIVE_NAME="AVX2 and FMA"
  elif sysctl -n machdep.cpu.leaf7_features 2>/dev/null | grep -qw AVX2 && sysctl -n machdep.cpu.features 2>/dev/null | grep -qw FMA; then
    NATIVE="-mavx2 -mfma"; NATIVE_NAME="AVX2 and FMA"
  fi
fi
CONFIGS="native"
if [ "${WHTC_FETCH_SIMDE:-0}" = 1 ] && [ -z "${SIMDE_DIR:-}" ]; then
  if [ ! -d "$B/simde" ]; then git clone -q https://github.com/simd-everywhere/simde.git "$B/simde"; fi
  (cd "$B/simde" && git checkout -q 71fd833d9666141edcd1d3c109a80e228303d8d7)
  SIMDE_DIR=$B/simde
fi
if [ -n "${SIMDE_DIR:-}" ]; then
  [ -f "$SIMDE_DIR/simde/x86/avx2.h" ] || { echo "SIMDE_DIR=$SIMDE_DIR has no simde/x86/avx2.h"; exit 1; }
  CONFIGS="native simde"
fi

flags_of() { # config -> compiler flags
  if [ "$1" = native ]; then echo "$NATIVE"; else echo "-DWHTC_SIMDE -I$SIMDE_DIR"; fi
}
name_of() {
  if [ "$1" = native ]; then echo "$NATIVE_NAME"; else echo "AVX2 and FMA through SIMDe"; fi
}
build() { # config extra-flags output test-source
  # shellcheck disable=SC2046
  $CC $CFLAGS $(flags_of "$1") $2 whtc_avx2.c whtc_plain.c "$4" -o "$3" -lm
}

for cfg in $CONFIGS; do
  echo
  echo "== build: $(name_of $cfg)   ($CC $CFLAGS $(flags_of $cfg))"
  for step in G20 TB8BALS TB8; do
    build $cfg "-DWHTC_STEP=$step" "$B/test_exact_${cfg}_$step" tests/test_exact.c
    out=$("$B/test_exact_${cfg}_$step") || { echo "$out"; echo "FAIL: test_exact, step $step, $(name_of $cfg)"; exit 1; }
    if [ $step = G20 ]; then echo "$out"; else echo "$out" | grep -E '^# |every 2\^0|portable code gives|^ALL'; fi
  done
  build $cfg "-DWHTC_STEP=G20" "$B/test_rounding_$cfg" tests/test_rounding.c
  "$B/test_rounding_$cfg"
  for step in TB8BALS TB8; do
    build $cfg "-DWHTC_STEP=$step" "$B/test_rounding_${cfg}_$step" tests/test_rounding.c
    "$B/test_rounding_${cfg}_$step" | grep -E '^# test_rounding|^  worst'
  done
  # the broken copy must fail
  build $cfg "-DWHTC_BREAK" "$B/test_exact_${cfg}_broken" tests/test_exact.c
  if out=$("$B/test_exact_${cfg}_broken"); then
    echo "$out"; echo "FAIL: the broken copy (-DWHTC_BREAK) passed the exactness test: the test is blind"; exit 1
  fi
  echo "$out" | grep -E '^# |every 2\^0|^FAIL' | sed 's/^/  broken copy: /'
  echo "CHECK the broken copy (one line of g20 changed) fails the exactness test: CAUGHT (good)"
  # code written for FFHT, linked under FFHT's names
  build $cfg "-DWHTC_FFHT_NAMES" "$B/ffht_names_$cfg" tests/ffht_names.c
  "$B/ffht_names_$cfg"
  if command -v "$CXX" >/dev/null 2>&1; then
    # shellcheck disable=SC2046
    $CC $CFLAGS $(flags_of $cfg) -DWHTC_FFHT_NAMES -c whtc_avx2.c -o "$B/a_$cfg.o"
    # shellcheck disable=SC2046
    $CC $CFLAGS $(flags_of $cfg) -DWHTC_FFHT_NAMES -c whtc_plain.c -o "$B/p_$cfg.o"
    $CXX $CFLAGS tests/ffht_overloads.cpp "$B/a_$cfg.o" "$B/p_$cfg.o" -o "$B/ffht_overloads_$cfg" -lm
    "$B/ffht_overloads_$cfg"
  else
    echo "(no C++ compiler: FFHT's C++ overloads not tested)"
  fi
done

echo
if command -v python3 >/dev/null 2>&1; then
  out=$(python3 -B check_same_as_harness.py) || { echo "$out"; echo "FAIL: the kernel's code is not the timed code (check_same_as_harness.py)"; exit 1; }
  echo "$out" | tail -1
else
  echo "(no python3: the comparison with the timed code, check_same_as_harness.py, was not run)"
fi
echo "OK: exact on integer inputs at every size 2^0 to 2^20 in float and double, FFHT's return codes, broken copy caught."
