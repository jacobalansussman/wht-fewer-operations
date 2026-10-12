#!/bin/sh
# calibration (mode 1: two children, textbook reachable with 0) and the one-child question (mode 0)
cd waves/wave-02/e-7-halftouch || exit 1
for k in 2 3 4; do ./anneal $k 1 3 99 99 3 2000000 6 1 1 2>/dev/null | head -1; done
for k in 2 3 4; do ./anneal $k 0 3 99 99 3 3000000 8 1 1 2>/dev/null | head -1; done
for k in 2 3 4; do ./anneal $k 0 3 99 99 3 3000000 8 2 0 2>/dev/null | head -1; done
