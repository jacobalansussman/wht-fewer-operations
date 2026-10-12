#!/bin/sh
cd waves/wave-02/e-7-halftouch || exit 1
# calibration at 8 points with slower cooling and three temperature ranges
./anneal 3 1 3 99 99 3 30000000 4 5 1 1.5 0.08 2>/dev/null | head -1
./anneal 3 1 3 99 99 3 30000000 4 5 1 0.8 0.15 2>/dev/null | head -1
./anneal 3 1 3 99 99 3 30000000 4 5 0 0.8 0.15 2>/dev/null | head -1
# one child, 8 points, can 6 be beaten?
./anneal 3 0 3 99 99 3 30000000 6 7 1 0.8 0.15 2>/dev/null | head -1
./anneal 3 0 3 99 99 3 30000000 6 7 2 0.8 0.15 2>/dev/null | head -1
# one child, 16 points
./anneal 4 0 3 99 99 3 60000000 3 9 1 0.8 0.15 2>&1 | grep -v "^[-0-9 ]*$" | grep -v "^[AB]$"
./anneal 4 0 3 99 99 3 60000000 3 9 1 0.5 0.2 2>&1 | grep -v "^[-0-9 ]*$" | grep -v "^[AB]$"
