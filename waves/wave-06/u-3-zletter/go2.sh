#!/bin/sh
# go-around 2: (a) every sign centre (input scalings +1/-1) on 14 of the best 8-point trees, modulo 3, gate mode;
#              (b) the plain centre modulo 5 (numbers 1..4 allowed on steps and rows) on 16 of the best trees, gate mode
cd waves/wave-06/u-3-zletter || exit 1
if [ "$1" = a ]; then ./dwzg 3 3 g < in8_signs.txt > out8_signs.txt; else ./dwzg 5 3 g < in8_p5_plain.txt > out8_p5_plain.txt; fi
