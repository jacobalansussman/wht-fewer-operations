#!/bin/sh
cd waves/wave-08/ab-0-neighboursums || exit 1
NB_CHAIN=16 timeout 330 nice -n 19 python3 -B nb.py B4 16 300 11 out2 seed
NB_CHAIN=15 timeout 330 nice -n 19 python3 -B nb.py A3c1 15 300 11 out2 seed
echo done > job3.done
