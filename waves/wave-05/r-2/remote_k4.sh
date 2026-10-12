#!/bin/bash
# r-2: weight-only block at k = 4 (5 x 5), p = 11, m = 5 helpers (10 gates), one tau per job; exhaustive over GF(11) (g-5-k3/mincirc_odd.c unchanged)
cd waves/wave-05/r-2 || exit 1
tau=$1
python3 -c "
from math import comb
p=11;t=$tau;k=4
for i in range(k+1): print(' '.join(str(sum(comb(i,m)*comb(k-i,j-m)*pow(t,m,p) for m in range(0,min(i,j)+1) if j-m<=k-i)%p) for j in range(k+1)))" > rows_k4_$tau.txt
echo "k=4 p=11 tau=$tau m=5 gates=10 start $(date)"
timeout 1170 nice -n 19 ./mincirc_odd 11 5 5 rows_k4_$tau.txt | grep -E "RESULT|visited"
echo "exit=$? end $(date)"
