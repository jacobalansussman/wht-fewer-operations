#!/bin/sh
# usage: angs.sh K seed iters T0 seedfile   -> angs_K_seed.out   (gate objective, seeded start)
cd waves/wave-06/u-3-zletter || exit 1
GATES=1 ./zmst $1 $2 $3 $4 $5 > angs_$1_$2.out 2> angs_$1_$2.err
