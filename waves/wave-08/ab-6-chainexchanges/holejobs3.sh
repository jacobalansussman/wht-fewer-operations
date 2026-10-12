#!/bin/sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
P="nice -n 19 python3 holegame.py"
$P 3 3 3 seq 12,23,13 25 3
$P 4 3 2 seq 12,12,0,0 25 3
$P 3 3 2 seq 12,12,0 25 3
$P 4 3 4 seq 12,23,34,14 20 3
$P 4 4 2 seq 12,12,12,12 20 3
$P 4 6 2 seq 12,12,12,12 10 3
$P 3 5 2 seq 12,12,0 20 3
$P 4 5 2 seq 12,12,12,12 15 3
