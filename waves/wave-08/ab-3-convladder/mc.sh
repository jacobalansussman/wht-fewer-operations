#!/bin/sh
# exact minimum circuits at 8 points over small fields ("none modulo p" is not "none")
cd waves/wave-08/ab-3-convladder || exit 1
L=not-in-this-repository/wht35/bin/light.py
M=waves/wave-01/d-0-zeta/mincirc
for spec in "ball1 2" "ball1 3" "mid 3" "mid 5" "lp1 3" "lp1 5" "lp1id 3"; do
  set -- $spec; name=$1; p=$2
  for m in 0 1 2 3 4 5 6; do
    out=mc_${name}_p${p}_m${m}.out
    python3 -B $L ab3-mc 300 $M $p 8 $m rows_${name}_k3.txt > $out 2>&1
    if grep -q "RESULT.*NO" $out; then continue; else break; fi
  done
done
touch mc.done
