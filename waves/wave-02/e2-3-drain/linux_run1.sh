#!/bin/sh
# one job: 16 points (40 seeds), 32 points (3 seeds), 64 points (1 seed); nice 15
cd waves/wave-02/e2-3-drain || exit 1 && gcc -O2 -fopenmp -o drain_omp drain.c && mkdir -p r16 r32 r64
for s in $(seq 1 40); do ./drain_omp 16 $s 3000 2 120 20 r16/r_H16_c2_s$s.jsonl H 400000 0; done > r16/log.txt 2>&1
for s in 1 2 3; do ./drain_omp 32 $s 400 2 400 60 r32/r_H32_c2_s$s.jsonl H 300000 1; done > r32/log.txt 2>&1
./drain_omp 64 1 120 2 600 240 r64/r_H64_c2_s1.jsonl H 300000 1 > r64/log.txt 2>&1
echo done > DONE1
