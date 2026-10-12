#!/bin/sh
# locked_run.sh -- run one timing command under the rules of this job.
#
#   sh locked_run.sh OUTFILE command [arguments]
#
# The command is run as:  taskset -c CPU command arguments   with its output in OUTFILE.
# run_time.sh is this script with the command "build/harness time".
#
# What it does, in this order:
#   1. waits until nobody else's benchmark runs (the tmux sessions named in OTHERS below, and any
#      process whose name contains "bench");
#   2. takes the lock /tmp/ffht-timing.LOCK (a directory; only one timing run of this job at a
#      time), waits if somebody holds it, says so if it takes over a lock older than 30 minutes
#      whose owner is gone;
#   3. picks the processor core whose two hyper-threads were the least busy over 3 seconds, and
#      pins the command to the first thread of that core (CPU=n in the environment overrides);
#   4. writes the date, the load and the busiest processes before and after into OUTFILE,
#      around the output of the command, and every 10 seconds while it runs into OUTFILE.watch;
#   5. removes the lock.
#
# It never changes another process.
out=$1
[ -n "$out" ] && [ $# -ge 2 ] || { echo "usage: sh locked_run.sh OUTFILE command [arguments]" >&2; exit 2; }
shift
LOCK=${LOCK:-/tmp/ffht-timing.LOCK}
OTHERS="bench bench3 passes"

others_running() {
    for s in $OTHERS; do
        if tmux -L "$s" ls >/dev/null 2>&1; then echo "tmux server $s"; return 0; fi
    done
    p=$(ps -eo pid,comm,args | awk 'NR > 1 && tolower($0) ~ /bench/ && $2 != "awk" && $2 != "ps"' | head -3)
    if [ -n "$p" ]; then echo "$p"; return 0; fi
    return 1
}

n=0
while w=$(others_running); do
    [ $((n % 20)) -eq 0 ] && echo "$(date -u +%H:%M:%S) waiting: another benchmark runs: $w" >&2
    n=$((n + 1))
    sleep 15
done

# LOCK_HELD=1: lockwait.py has already taken the lock for this command (it looks 50 times a second;
# the loop below looks every 2 seconds and never wins against the other jobs' waiters)
while [ -z "$LOCK_HELD" ] && ! mkdir "$LOCK" 2>/dev/null; do
    age=$(( $(date +%s) - $(stat -c %Y "$LOCK" 2>/dev/null || date +%s) ))
    owner=$(cat "$LOCK/owner" 2>/dev/null)
    opid=$(echo "$owner" | sed -n 's/.*pid=\([0-9]*\).*/\1/p')
    if [ "$age" -gt 1800 ] && { [ -z "$opid" ] || ! kill -0 "$opid" 2>/dev/null; }; then
        echo "$(date -u +%H:%M:%S) the lock is $age s old and its owner ($owner) is gone: taking it" >&2
        rm -rf "$LOCK"
        continue
    fi
    echo "$(date -u +%H:%M:%S) waiting for the lock ($owner, $age s old)" >&2
    sleep 2
done
echo "label=${LABEL:-style-intrinsics} pid=$$ since=$(date -u +%Y-%m-%dT%H:%M:%SZ) out=$out" > "$LOCK/owner"
trap 'rm -rf "$LOCK"' EXIT INT TERM

# a second look, now that we hold the lock
while w=$(others_running); do
    echo "$(date -u +%H:%M:%S) holding the lock, waiting: another benchmark runs: $w" >&2
    sleep 15
done

snapshot() {
    echo "## $1: $(date -u '+%Y-%m-%d %H:%M:%S UTC'); uptime:$(uptime)"
    echo "## $1: processes above 5 % of a processor (pid, %cpu, processor, nice, command):"
    ps -eo pid,pcpu,psr,ni,args --sort=-pcpu | awk 'NR > 1 && $2 > 5 {print "##    " substr($0, 1, 150)}'
}

if [ -z "$CPU" ]; then
    grep '^cpu[0-9]' /proc/stat > /tmp/ffht_stat_a.$$
    sleep 3
    grep '^cpu[0-9]' /proc/stat > /tmp/ffht_stat_b.$$
    CPU=$(awk 'NR == FNR { t = 0; for (i = 2; i <= 9; i++) t += $i; tot[$1] = t; idle[$1] = $5 + $6; next }
               { t = 0; for (i = 2; i <= 9; i++) t += $i; d = t - tot[$1]; b = d - ($5 + $6 - idle[$1]);
                 c = substr($1, 4) + 0; busy[c] = (d > 0) ? b / d : 0; n = c }
               END { half = (n + 1) / 2; best = 0; bv = 9;
                     for (c = 0; c < half; c++) { v = busy[c] + busy[c + half]; if (v < bv) { bv = v; best = c } }
                     print best }' /tmp/ffht_stat_a.$$ /tmp/ffht_stat_b.$$)
    rm -f /tmp/ffht_stat_a.$$ /tmp/ffht_stat_b.$$
fi

# While the command runs, a watcher writes one line every 10 seconds into OUTFILE.watch: the time,
# whether another benchmark was seen, and every other process above 20 % of a processor with the
# processor it was on.  The lines say afterwards which sizes were timed next to what.  The watcher
# itself is kept off the core of the timed command (off processor CPU and its hyper-thread).
sibs=$(tr ',-' '  ' < /sys/devices/system/cpu/cpu$CPU/topology/thread_siblings_list)
REST=$(awk -v n="$(getconf _NPROCESSORS_ONLN)" -v s="$sibs" 'BEGIN { m = split(s, a, " "); for (i = 1; i <= m; i++) no[a[i] + 0] = 1;
       for (c = 0; c < n; c++) if (!(c in no)) r = r (r == "" ? "" : ",") c; print r }')
(
    [ -n "$REST" ] && taskset -pc "$REST" "$(sh -c 'echo $PPID')" > /dev/null 2>&1
    while :; do
        w=$(others_running) && w="OTHER BENCHMARK: $w" || w="no other benchmark"
        b=$(ps -eo pid,pcpu,psr,ni,comm --sort=-pcpu | awk 'NR > 1 && $2 > 20 {printf " [pid %s %s%% cpu%s nice%s %s]", $1, $2, $3, $4, $5}')
        echo "$(date -u +%H:%M:%S) load $(cut -d" " -f1-3 /proc/loadavg); $w; busy:$b"
        sleep 10
    done
) > "$out.watch" 2>&1 &
watcher=$!
trap 'kill $watcher 2>/dev/null; rm -rf "$LOCK"' EXIT INT TERM

{
    echo "## locked_run.sh: taskset -c $CPU $*"
    echo "## pinned to processor $CPU (siblings: $(cat /sys/devices/system/cpu/cpu$CPU/topology/thread_siblings_list))"
    echo "## transparent huge pages: $(cat /sys/kernel/mm/transparent_hugepage/enabled)"
    snapshot before
    taskset -c "$CPU" "$@"
    echo "## exit code $?"
    snapshot after
} > "$out" 2>&1
kill $watcher 2>/dev/null
echo "written: $out (and $out.watch)"
