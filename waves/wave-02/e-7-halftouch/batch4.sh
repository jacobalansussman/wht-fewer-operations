#!/bin/sh
# batch 4 on the Linux machine: start from the tensored 16-point identity (60 entries at 32 points, 240 at 64) and try to improve
cd waves/wave-02/e-7-halftouch || exit 1
gcc -O2 -o altmin altmin.c -lm || exit 1
run(){ out=$1; shift; nice -n 15 ./altmin "$@" > $out.txt 2> $out.err & }
run s32a 5 0 3 3 225 41 40 0 seed32.txt
run s32b 5 0 3 3 225 42 40 0 seed32.txt
run s32c 5 0 3 3 225 43 120 0 seed32.txt
run s32w4 5 0 4 4 225 44 30 0 seed32.txt
run s64a 6 0 3 3 225 45 16 0 seed64.txt
run s16a 4 0 3 3 225 46 0 0 p16a.txt
run s16b 4 0 3 3 225 47 0 0 p16b.txt
run r16 4 0 3 3 225 48 0
wait
echo done > batch4.done
