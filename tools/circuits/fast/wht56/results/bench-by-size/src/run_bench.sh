#!/bin/sh
# run_bench.sh -- build bench_size twice (scalar, vectorised) and run each build once.
#   sh run_bench.sh <output directory> <machine label> [runs]
# One benchmark process at a time.  Before and after each run: the date, the load average and
# the list of other processes using more than 50% of a processor.
set -e
here=$(cd "$(dirname "$0")" && pwd)
out=$1
label=$2
runs=${3:-9}
mkdir -p "$out"
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
busy() {
    echo "load: $(uptime)"
    echo "other processes above 50% of a processor:"
    ps -eo pcpu,pid,comm | awk 'NR > 1 && $1 > 50 && $3 !~ /bench_size/ { n++; print "   " $0 } END { print "   count: " n + 0 }'
}
for b in scalar vec; do
    case $b in
        scalar) flags="-O2 $NOVEC" ;;
        vec)    flags="-O3 $NATIVE" ;;
    esac
    log="$out/$label-$b.txt"
    {
        echo "machine: $label; $(uname -srm)"
        echo "compiler: $($CC --version | head -1)"
        echo "build $b: $CC -std=c11 $flags -o bench_size_$b bench_size.c wht56.c -lm"
        $CC -std=c11 $flags -o "$out/bench_size_$b" "$here/bench_size.c" "$here/wht56.c" -lm
        echo "start: $(date)"
        echo "BEFORE"; busy
        "$out/bench_size_$b" "$runs"
        echo "end: $(date)"
        echo "AFTER"; busy
    } > "$log" 2>&1
done
echo ALLDONE > "$out/$label-done.txt"
