#!/bin/sh
# usage: rung.sh <part suffix>   exact gate-mode census of one quarter of the 8-point input trees, modulo 3
cd waves/wave-06/u-3-zletter || exit 1
./dwzg 3 3 g < in8z_part_$1 > out8zg_$1.txt
