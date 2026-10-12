#!/bin/sh
# usage: ang.sh K seed iters T0   -> ang_K_seed.out   (gate objective)
cd waves/wave-06/u-3-zletter || exit 1
GATES=1 ./zmst $1 $2 $3 $4 > ang_$1_$2.out 2> ang_$1_$2.err
