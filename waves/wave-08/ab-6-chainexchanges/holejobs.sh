#!/bin/sh
# controls first: the exchange (must hit), two stages (must not)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
P="nice -n 19 python3 holegame.py"
$P 2 3 1 seq 1,1 20 1
$P 2 2 1 seq 1,1 20 1
$P 3 2 1 seq 1,1,0 30 1
$P 3 2 1 seq 1,1,1 30 1
$P 4 2 1 seq 1,1,1,1 30 1
$P 3 3 1 seq 1,1,1 30 1
$P 2 3 2 seq 12,12 30 1
$P 3 3 2 seq 12,12,12 40 1
$P 3 3 2 seq 12,12,0 40 1
$P 3 3 2 seq 1,2,12 40 1
$P 3 3 2 seq 1,2,0 40 1
$P 4 3 2 seq 12,12,12,12 40 1
$P 4 3 2 seq 1,1,2,2 40 1
$P 4 3 3 seq 123,123,123,123 40 1
$P 3 3 3 seq 123,123,123 40 1
$P 2 4 2 seq 12,12 30 1
$P 3 4 2 seq 12,12,12 40 1
$P 4 4 2 seq 12,12,12,12 40 1
$P 2 5 2 seq 12,12 30 1
$P 3 5 2 seq 12,12,12 30 1
$P 4 5 2 seq 12,12,12,12 30 1
$P 4 4 2 seq 1,1,2,2 30 1
$P 3 4 3 seq 12,13,23 30 1
$P 3 3 3 seq 1,2,3 40 1
$P 4 5 4 seq 1,2,3,4 20 1
