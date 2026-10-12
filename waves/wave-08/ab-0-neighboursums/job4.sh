#!/bin/sh
cd waves/wave-08/ab-0-neighboursums || exit 1
NB_CHAIN=15 timeout 660 nice -n 19 python3 -B nb.py B4 15 630 12 out2 seed
echo done > job4.done
