#!/bin/sh
# batch 2 on the Linux machine: alternating best fits at 16 points
cd waves/wave-02/e-7-halftouch || exit 1
gcc -O2 -o altmin altmin.c -lm || exit 1
run(){ out=$1; shift; nice -n 15 ./altmin "$@" > $out.txt 2> $out.err & }
run p16a 4 0 3 3 230 1 0
run p16b 4 0 3 3 230 2 0
run q16cal 4 1 3 3 230 3 0
run p16w4 4 0 4 4 230 4 0
run p16m3 4 3 3 3 230 5 0
run p16m4 4 4 3 3 230 6 0
run p16m8 4 8 3 3 230 7 0
run p16m2 4 2 3 3 230 8 0
wait
echo done > batch2.done
