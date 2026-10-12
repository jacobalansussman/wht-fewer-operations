#!/bin/sh
# batch 3 on the Linux machine: 32 points (fits by 40 sampled position sets per support), one more 16-point run
cd waves/wave-02/e-7-halftouch || exit 1
run(){ out=$1; shift; nice -n 15 ./altmin "$@" > $out.txt 2> $out.err & }
run p32a 5 0 3 3 235 21 40
run p32b 5 0 3 3 235 22 40
run p32c 5 0 3 3 235 23 100
run p32m8 5 8 3 3 235 24 40
run p32w4 5 0 4 4 235 25 30
run p16w2 4 0 2 2 235 26 0
run p32m3 5 3 3 3 235 27 30
run p32w2 5 0 2 2 235 28 60
wait
echo done > batch3.done
