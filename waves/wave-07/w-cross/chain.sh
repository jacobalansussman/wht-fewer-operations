#!/bin/sh
cd waves/wave-07/w-cross || exit 1
L=not-in-this-repository/wht35/bin/light.py
M=waves/wave-01/d-0-zeta/mincirc
for spec in "2 4" "3 3" "2 5" "3 4" "5 3" "2 6" "3 5"; do
  set -- $spec
  python3 -B $L wcross-nbr4-p$1-m$2 110 $M $1 8 $2 rows_nbr4half.txt > nbr4_p$1_m$2.out 2>&1
done
echo done > chain.done
