#!/bin/bash
# weight-only block at k = 4 (5 x 5) over GF(11): tau = 10 (the transform: Krawtchouk matrix) and tau = 3 (generic).  gates = 5 + m.
cd "$(dirname "$0")"
for tau in 10 3; do
  python3 -c "
from math import comb
p=11;t=$tau;k=4
for i in range(k+1): print(' '.join(str(sum(comb(i,m)*comb(k-i,j-m)*pow(t,m,p) for m in range(0,min(i,j)+1) if j-m<=k-i)%p) for j in range(k+1)))" > rows_k4_$tau.txt
done
for m in 4 5 6; do for tau in 10 3; do
  echo "k=4 p=11 tau=$tau m=$m gates=$((5+m))"
  python3 -B not-in-this-repository/wht35/bin/light.py p0-k4 420 ../g-5-k3/mincirc_odd 11 5 $m rows_k4_$tau.txt 2>&1 | grep -E "RESULT|visited|LIGHT|no free" | cut -c1-170
done; done
