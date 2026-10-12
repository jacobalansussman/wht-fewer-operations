#!/bin/sh
cd waves/wave-10/ag-8-bestbadcircuit || exit 1
for f in ../e2-0-pieces/slp_4.txt ../e2-0-pieces/slp_8.txt ../g-1-tightwires/h8_19gates.txt ../e2-0-pieces/slp_16.txt ../e2-0-pieces/slp_32.txt ../e2-0-pieces/slp_64.txt; do python3 -B wsolve.py $f id; done
python3 -B wsolve.py ../e2-0-pieces/slp_4.txt frames
