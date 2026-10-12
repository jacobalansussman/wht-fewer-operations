#!/bin/sh
# ring targets: content i gets the holes of its two neighbouring pairs; every hole is filled for exactly two contents
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
P="nice -n 19 python3 holegame.py"
$P 3 3 3 seq 12,23,13 60 2
$P 4 3 2 seq 12,12,12,12 60 2
$P 4 3 4 seq 12,23,34,14 40 2
$P 3 4 3 seq 12,23,13 40 2
$P 4 4 4 seq 12,23,34,14 30 2
$P 4 4 2 seq 12,12,12,12 40 2
$P 3 5 3 seq 12,23,13 30 2
$P 4 5 2 seq 12,12,12,12 30 2
$P 4 5 4 seq 12,23,34,14 20 2
$P 4 6 2 seq 12,12,12,12 20 2
$P 3 6 3 seq 12,23,13 20 2
$P 2 6 2 seq 12,12 20 2
$P 2 5 2 seq 12,12 30 2
$P 4 3 2 sim 12,12,12,12 40 2
$P 4 4 2 sim 12,12,12,12 40 2
