#!/bin/sh
# run_harness.sh -- one full timing run of the harness for this job, floats then doubles.
#
#   sh run_harness.sh TAG [REPEATS] [KMIN KMAX] [VARIANTS]
#
# Each type is one call of locked_run.sh, after lockwait.py has taken the lock
# /tmp/ffht-timing.LOCK: it waits for other benchmarks to end, pins the harness to the quietest
# core, records the load and the busy processes before and after, and releases the lock.  The
# lock is free for 25 seconds between the two types, so that another job can take its turn.
# HARNESS_BIN (default build/harness) and TYPES (default "float double") can be set.
# Output: out/time-float-TAG.txt, out/time-double-TAG.txt and their .watch files.
here=$(cd "$(dirname "$0")" && pwd)
tag=${1:?usage: sh run_harness.sh TAG [REPEATS] [KMIN KMAX] [VARIANTS]}
r=${2:-15}
kmin=${3:-3}
kmax=${4:-26}
vars=${5:-ffht,gT,g20x,g20s,g19f,g19r}
export LABEL=style-generator
cd "$here/harness"
mkdir -p ../out
bin=${HARNESS_BIN:-build/harness}
for t in ${TYPES:-float double}; do
    python3 -B ../lockwait.py sh locked_run.sh "../out/time-$t-$tag.txt" "$bin" time -t "$t" -k "$kmin" "$kmax" -r "$r" -v "$vars"
    sleep 25        # the other job's waiter looks every 20 seconds: let it have its turn
done
echo "run $tag finished: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
