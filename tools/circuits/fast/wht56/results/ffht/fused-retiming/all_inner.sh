#!/bin/sh
# all_inner.sh -- every timing of this folder in ONE hold of the lock (started by mylock.py).
cd "$(dirname "$0")" || exit 1
snap() {
    echo "## $1: $(date -u '+%Y-%m-%d %H:%M:%S UTC'); load $(cat /proc/loadavg)"
    ps -eo pid,pcpu,psr,ni,comm --sort=-pcpu | awk 'NR > 1 && $2 > 5 {print "##    pid " $1 " " $2 "% cpu" $3 " nice" $4 " " $5}'
}
sibof() { tr ',' ' ' < /sys/devices/system/cpu/cpu$1/topology/thread_siblings_list | awk -v c=$1 '{for (i = 1; i <= NF; i++) if ($i != c) print $i}'; }
one() {  # tag cpu sizes variants [MBUF]
    out=out/$1.txt; cpu=$2; sib=$(sibof $cpu)
    { echo "## waited ${WAITED:-0} s for the lock (one hold for all runs)"; echo "## MBUF=${5:-1} taskset -c $cpu b/reftime $sib $3 $4"; snap before
      MBUF=${5:-1} taskset -c $cpu b/reftime $sib "$3" "$4"; echo "## exit $?"; snap after; } > $out 2>&1
    echo "$(date -u +%H:%M:%S) written $out"
}
small() {  # tag cpu
    one small-$1-chained $2 6,9 T,G19
    one small-$1-separate64 $2 6 T,G19 64
    one small-$1-separate8 $2 9 T,G19 8
}
core() { out=out/core-cpu$1.txt; { echo "## taskset -c $1 b/core"; snap before; taskset -c $1 b/core; echo "## exit $?"; snap after; } > $out 2>&1; echo "$(date -u +%H:%M:%S) written $out"; }
echo "$(date -u +%H:%M:%S) lock held, start"
one main-m1-cpu1 1 12,15,26 ffht,T,G19; one main-m1-cpu3 3 12,15,26 ffht,T,G19
one flags-cpu1 1 6,12,15 T,G19,T_O2,G19_O2,T_gen,G19_gen
one main-m2-cpu1 1 12,15,26 ffht,T,G19; one main-m2-cpu3 3 12,15,26 ffht,T,G19
small a 1
one main-m3-cpu1 1 12,15,26 ffht,T,G19; one main-m3-cpu3 3 12,15,26 ffht,T,G19
one flags-cpu3 3 6,12,15 T,G19,T_O2,G19_O2,T_gen,G19_gen
one main-m4-cpu1 1 12,15,26 ffht,T,G19; one main-m4-cpu3 3 12,15,26 ffht,T,G19
small b 3
one int-cpu1 1 12,18 iT,iG19s,sT,sG19
one main-m5-cpu1 1 12,15,26 ffht,T,G19; one main-m5-cpu3 3 12,15,26 ffht,T,G19
one int-cpu3 3 12,18 iT,iG19s,sT,sG19
core 1
echo "$(date -u +%H:%M:%S) done"; date -u > out/all.done
