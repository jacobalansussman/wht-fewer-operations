#!/bin/bash
# weight-only block at k = 4 (5 x 5), p = 11: tau = 10 (the transform, Krawtchouk matrix) and tau = 3 (generic); gates = 5 + m
cd waves/wave-05/p-0-classtest || exit 1
gcc -O2 -w -o mincirc_odd mincirc_odd.c
for tau in 10 3; do
  python3 -c "
from math import comb
p=11;t=$tau;k=4
for i in range(k+1): print(' '.join(str(sum(comb(i,m)*comb(k-i,j-m)*pow(t,m,p) for m in range(0,min(i,j)+1) if j-m<=k-i)%p) for j in range(k+1)))" > rows_k4_$tau.txt
done
for m in 4 5 6 7; do for tau in 10 3; do
  echo "k=4 p=11 tau=$tau m=$m gates=$((5+m))"; ./mincirc_odd 11 5 $m rows_k4_$tau.txt | grep -E "RESULT|visited"
done; done
