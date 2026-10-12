#!/bin/sh
# run_pass.sh -- build bench_pass twice (scalar, vectorised; the flags of run_bench.sh) and run each.
#   sh run_pass.sh <output directory> <machine label> [rounds]
set -e
here=$(cd "$(dirname "$0")" && pwd)
out=$1
label=$2
rounds=${3:-9}
CC=${CC:-cc}
if $CC --version 2>/dev/null | grep -qi clang; then
    NOVEC="-fno-vectorize -fno-slp-vectorize"
else
    NOVEC="-fno-tree-vectorize"
fi
case "$(uname -m)" in
    arm64|aarch64) NATIVE="-mcpu=native" ;;
    *)             NATIVE="-march=native" ;;
esac
for b in scalar vec; do
    case $b in
        scalar) flags="-O2 $NOVEC" ;;
        vec)    flags="-O3 $NATIVE" ;;
    esac
    {
        echo "machine: $label; $(uname -srm)"
        echo "compiler: $($CC --version | head -1)"
        echo "build $b: $CC -std=c11 $flags -o bench_pass_$b bench_pass.c -lm"
        $CC -std=c11 $flags -o "$out/bench_pass_$b" "$here/bench_pass.c" -lm
        echo "start: $(date)"
        echo "load: $(uptime)"
        "$out/bench_pass_$b" "$rounds"
        echo "end: $(date)"
        echo "load: $(uptime)"
    } > "$out/$label-pass-$b.txt" 2>&1
done
echo ALLDONE > "$out/$label-pass-done.txt"
