#!/bin/sh
# build_and_bench.sh -- compile the C version three times and run the benchmark of each build.
#
#   sh c/build_and_bench.sh [output directory [runs [k1 k2 ...]]]
#
# Build "novec": -O3 with the compiler's vectorisers switched off (scalar code).
# Build "plain": -O3 and nothing else (the compiler vectorises for its default instruction set).
# Build "vec":   -O3 with the vectorisers on and the instruction set of this machine allowed.
# The compiler is $CC, or cc.  kernels.h is written again from the circuit files first if
# python3 is there (the file in this folder is the same text).
set -e
here=$(cd "$(dirname "$0")" && pwd)
out=${1:-$here/build}
runs=${2:-9}
[ $# -ge 2 ] && shift 2 || shift $#
mkdir -p "$out"
CC=${CC:-cc}

if command -v python3 >/dev/null 2>&1; then
    (cd "$here/../.." && python3 -B -m wht56 --gen kernels) > "$out/kernels.h.new"
    if cmp -s "$out/kernels.h.new" "$here/kernels.h"; then
        echo "kernels.h: the same as what codegen.py writes now"
    else
        echo "kernels.h DIFFERS from what codegen.py writes now" >&2
        exit 1
    fi
fi

if $CC --version 2>/dev/null | grep -qi clang; then
    NOVEC="-fno-vectorize -fno-slp-vectorize"
else
    NOVEC="-fno-tree-vectorize"
fi
case "$(uname -m)" in
    arm64|aarch64) NATIVE="-mcpu=native" ;;
    *)             NATIVE="-march=native" ;;
esac

echo "machine: $(uname -srm)"
echo "compiler: $($CC --version | head -1)"
echo "date: $(date)"
for b in novec plain vec; do
    case $b in
        novec) flags="-O3 $NOVEC" ;;
        plain) flags="-O3" ;;
        vec)   flags="-O3 $NATIVE" ;;
    esac
    echo
    echo "== build $b: $CC -std=c11 $flags"
    $CC -std=c11 $flags -o "$out/bench_$b" "$here/bench.c" "$here/wht56.c" -lm
    "$out/bench_$b" "$runs" "$@"
done
