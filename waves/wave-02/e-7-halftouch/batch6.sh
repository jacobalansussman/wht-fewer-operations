#!/bin/sh
# batch 6 on the Linux machine: free diagonal remainder, children of total length 3N/4, 16 points, eight more seeds
cd waves/wave-02/e-7-halftouch || exit 1
run(){ out=$1; shift; nice -n 15 ./altmin "$@" > $out.txt 2> $out.err & }
run g16m3a 4 3 3 3 200 61 0 1
run g16m3b 4 3 3 3 200 62 0 1
run g16m3c 4 3 3 3 200 63 0 1
run g16m3d 4 3 3 3 200 64 0 1
run g16m4a 4 4 3 3 200 65 0 1
run g16m4b 4 4 3 3 200 66 0 1
run g16m4c 4 4 3 3 200 67 0 1
run g16m4d 4 4 3 3 200 68 0 1
wait
echo done > batch6.done
