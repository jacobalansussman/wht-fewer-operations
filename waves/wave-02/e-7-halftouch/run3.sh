#!/bin/sh
# 8 points: every child variant, 6 seconds each, a = b = 3 (and 2), exhaustive fits
cd waves/wave-02/e-7-halftouch || exit 1
for mode in 0 8 2 3 4 6 7; do ./altmin 3 $mode 3 3 6 11 0 2>/dev/null > v8_m$mode.txt; head -1 v8_m$mode.txt; done
./altmin 3 0 2 2 6 12 0 2>/dev/null > v8_m0_w2.txt; head -1 v8_m0_w2.txt
./altmin 3 0 2 3 6 12 0 2>/dev/null > v8_m0_w23.txt; head -1 v8_m0_w23.txt
./altmin 3 0 3 3 6 13 0 1 2>/dev/null > v8_m0_fd.txt; head -1 v8_m0_fd.txt
