#!/bin/sh
# usage: an.sh K seed iters T0   -> an_K_seed.out
cd waves/wave-06/u-3-zletter || exit 1
./zmst $1 $2 $3 $4 > an_$1_$2.out 2> an_$1_$2.err
