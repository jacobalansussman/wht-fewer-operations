#!/bin/sh
cd waves/wave-07/w-cross || exit 1
L=not-in-this-repository/wht35/bin/light.py
M=waves/wave-01/d-0-zeta/mincirc
python3 -B $L wcross-nbr4-p5-m5 420 $M 5 8 5 rows_nbr4half.txt > nbr4_p5_m5.out 2>&1
echo done > chain2.done
