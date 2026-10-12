#!/bin/sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
P="nice -n 19 python3 holegame.py"
$P 3 4 2 seq 12,12,0 20 4
$P 5 2 1 seq 1,1,1,1,0 30 4
$P 5 2 2 seq 1,1,2,2,0 30 4
$P 4 2 2 seq 1,1,2,2 25 4
$P 6 2 1 seq 1,1,1,1,0,0 15 4
$P 6 2 1 seq 1,1,1,1,1,1 20 4
$P 4 3 1 seq 1,1,1,1 15 4
$P 5 3 1 seq 1,1,1,1,0 15 4
$P 6 3 1 seq 1,1,1,1,1,1 15 4
$P 5 4 1 seq 1,1,1,1,0 15 4
