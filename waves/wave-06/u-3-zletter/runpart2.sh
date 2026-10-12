#!/bin/sh
# usage: runpart2.sh <part suffix>   (second local copy of a part that is also running on the Linux machine)
cd waves/wave-06/u-3-zletter || exit 1
./dwz 3 3 < in8z_part_$1 > out8z_$1.txt
