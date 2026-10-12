#!/bin/sh
# usage: runpart.sh <part suffix>
cd waves/wave-06/u-3-zletter || exit 1
./dwz 3 3 < in8z_part_$1 > out8z_$1.txt
