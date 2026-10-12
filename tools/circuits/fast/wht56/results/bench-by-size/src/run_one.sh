#!/bin/sh
# run_one.sh -- one build of bench_size with the flags given, one run.  A control beside run_bench.sh.
#   sh run_one.sh <output directory> <label> <runs> <compiler flags ...>
set -e
here=$(cd "$(dirname "$0")" && pwd)
out=$1
label=$2
runs=$3
shift 3
CC=${CC:-cc}
busy() {
    echo "load: $(uptime)"
    echo "other processes above 50% of a processor:"
    ps -eo pcpu,pid,comm | awk 'NR > 1 && $1 > 50 && $3 !~ /bench_size/ { n++; print "   " $0 } END { print "   count: " n + 0 }'
}
{
    echo "machine: $label; $(uname -srm)"
    echo "compiler: $($CC --version | head -1)"
    echo "build $label: $CC -std=c11 $* -o bench_size_$label bench_size.c wht56.c -lm"
    $CC -std=c11 "$@" -o "$out/bench_size_$label" "$here/bench_size.c" "$here/wht56.c" -lm
    echo "start: $(date)"
    echo "BEFORE"; busy
    "$out/bench_size_$label" "$runs"
    echo "end: $(date)"
    echo "AFTER"; busy
} > "$out/$label.txt" 2>&1
echo ALLDONE > "$out/$label-done.txt"
