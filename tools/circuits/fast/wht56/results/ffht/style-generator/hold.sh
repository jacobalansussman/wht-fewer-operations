#!/bin/sh
# hold.sh -- several timing steps of this job under ONE taking of the shared lock.
#
#   python3 -B lockwait.py sh harness/locked_run.sh out/hold-X.txt sh hold.sh STEP [STEP ...]
#
# Four jobs share the lock by now and each wait for it is long, so the steps are grouped.  They
# run one after the other (never two at once), all pinned to the processor that locked_run.sh
# chose (the harness moves itself to a quieter core when its hyper-thread sibling gets busy and
# says so in its output).  Each step writes its own file in out/, which starts with the time,
# the load and the busy processes at that moment; locked_run.sh's .watch file has the load and
# the busy processes every 10 seconds for the whole hold.
#
# Steps:
#   kloop    one 8-register pass alone, every kernel             -> out/kloop-1.txt
#   redo     the sizes of run 1 kept with a busy sibling, again  -> out/time-redo-run1.txt
#   wheref   the new kernel only in the larger passes, floats    -> out/time-float-where.txt
#   whered   the same, doubles                                   -> out/time-double-where.txt
#   ownf     FFHT's own program, variants taking turns, floats   -> out/own-rounds-float.txt
#   ownd     the same, doubles                                   -> out/own-rounds-double.txt
#   alt      the other plan at 7 sizes                           -> out/time-alt.txt
here=$(cd "$(dirname "$0")" && pwd)
cd "$here"
snapshot() {
    echo "## step $1: $(date -u '+%Y-%m-%d %H:%M:%S UTC'); uptime:$(uptime); pinned to: $(taskset -pc $$ | sed 's/.*: //')"
    echo "## step $1: processes above 5 % of a processor (pid, %cpu, processor, nice, command):"
    ps -eo pid,pcpu,psr,ni,args --sort=-pcpu | awk 'NR > 1 && $2 > 5 {print "##    " substr($0, 1, 150)}'
}
WHERE_VARS=ffht,g20s,p20s,p19f,d20s,d19f
for step in "$@"; do
    echo "hold.sh: step $step starts $(date -u +%H:%M:%S)"
    case $step in
    kloop)  { snapshot kloop; kloop/kloop 15; snapshot kloop-end; } > out/kloop-1.txt 2>&1 ;;
    redo)   { snapshot redo; sh redo.sh run1 9 20; snapshot redo-end; } > out/time-redo-run1.txt 2>&1 ;;
    wheref) { snapshot wheref; ( cd harness && build-where/harness time -t float -k 12 26 -r 9 -v $WHERE_VARS ); snapshot wheref-end; } > out/time-float-where.txt 2>&1 ;;
    whered) { snapshot whered; ( cd harness && build-where/harness time -t double -k 11 26 -r 9 -v $WHERE_VARS ); snapshot whered-end; } > out/time-double-where.txt 2>&1 ;;
    ownf)   { snapshot ownf; sh own_rounds.sh 3 3 26 "ffht g20x g20s" float; snapshot ownf-end; } > out/own-rounds-float.txt 2>&1 ;;
    ownd)   { snapshot ownd; sh own_rounds.sh 3 3 26 "ffht g20x g20s" double; snapshot ownd-end; } > out/own-rounds-double.txt 2>&1 ;;
    alt)    { snapshot alt; sh alt_run.sh 9; snapshot alt-end; } > out/time-alt.txt 2>&1 ;;
    *)      echo "hold.sh: unknown step $step" ;;
    esac
    echo "hold.sh: step $step ends $(date -u +%H:%M:%S)"
done
