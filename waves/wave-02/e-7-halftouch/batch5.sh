#!/bin/sh
# batch 5 on the Linux machine: the remainder is a free DIAGONAL (its entries are not counted), children of total length 3N/4
cd waves/wave-02/e-7-halftouch || exit 1
run(){ out=$1; shift; nice -n 15 ./altmin "$@" > $out.txt 2> $out.err & }
run f16m3a 4 3 3 3 200 51 0 1
run f16m3b 4 3 3 3 200 52 0 1
run f16m4a 4 4 3 3 200 53 0 1
run f16m4b 4 4 3 3 200 54 0 1
run f16m0a 4 0 3 3 200 55 0 1
run f16m0b 4 0 3 3 200 56 0 1
run f16m1 4 1 3 3 200 57 0 1
run f32m3 5 3 3 3 200 58 30 1
wait
echo done > batch5.done
