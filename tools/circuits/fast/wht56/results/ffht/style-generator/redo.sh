#!/bin/sh
# redo.sh -- time again the sizes of a run that were kept although the hyper-thread sibling of the
# timed processor was busy (the harness keeps the 4th attempt whatever happened).
#
#   sh harness/locked_run.sh out/time-redo-TAG.txt sh redo.sh TAG [REPEATS] [LIMIT]   (after lockwait.py)
#
# It reads out/time-float-TAG.txt and out/time-double-TAG.txt, takes every size whose line A shows
# the sibling busy for more than LIMIT per cent (default 20), and runs the harness for that one
# size again, with the same variants.  The harness inherits the processor of this script.
here=$(cd "$(dirname "$0")" && pwd)
tag=${1:?usage}
r=${2:-15}
limit=${3:-20}
vars=${VARS:-ffht,gT,g20x,g20s,g19f}
cd "$here/harness"
for t in float double; do
    f=../out/time-$t-$tag.txt
    [ -f "$f" ] || continue
    for k in $(awk -v lim="$limit" '$1 == "A" { for (i = 2; i <= NF; i++) { split($i, a, "="); v[a[1]] = a[2] } if (v["sibling_busy_pct"] + 0 > lim) print v["k"] }' "$f"); do
        build/harness time -t "$t" -k "$k" "$k" -r "$r" -v "$vars"
    done
done
