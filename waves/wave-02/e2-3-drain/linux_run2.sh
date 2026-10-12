#!/bin/sh
# one job: 32 points (2 seeds) and 64 points (1 seed), stop when no gate drains 2 or more; nice 15
cd waves/wave-02/e2-3-drain || exit 1 && mkdir -p r32 r64
./drain_omp 64 1 60 2 600 270 r64/r_H64_c2_s1.jsonl H 150000 1 > r64/log.txt 2>&1
for s in 1 2; do ./drain_omp 32 $s 300 2 400 120 r32/r_H32_c2_s$s.jsonl H 200000 1; done > r32/log.txt 2>&1
echo done > DONE2
