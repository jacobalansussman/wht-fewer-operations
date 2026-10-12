#!/bin/sh
# batch 1 on the Linux machine: calibration (mode 1, zero reachable) and the one-child question (mode 0)
cd waves/wave-02/e-7-halftouch || exit 1
run(){ out=$1; shift; timeout 280 nice -n 15 ./anneal "$@" > $out.txt 2> $out.err & }
run c8a  3 1 3 99 99 3 100000000 4 5 1 0.8 0.15
run c8b  3 1 3 99 99 3 100000000 4 5 0 0.8 0.15
run o8a  3 0 3 99 99 3 100000000 6 7 1 0.8 0.15
run o8b  3 0 3 99 99 3 100000000 6 7 2 0.8 0.15
run o16a 4 0 3 99 99 3 1000000000 3 9 1 0.8 0.15
run o16b 4 0 3 99 99 3 1000000000 3 10 1 0.5 0.2
run o16c 4 0 3 99 99 3 1000000000 3 11 0 0.6 0.15
run c16  4 1 3 99 99 3 1000000000 3 12 0 0.6 0.15
wait
echo done > batch1.done
