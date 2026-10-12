#!/bin/bash
# r-2: weight-only block (k+1) x (k+1), entry (i,j) = sum_m C(i,m) C(k-i,j-m) tau^m, by r2_brute: number of helper sets with m helpers.
# usage: run_weight.sh k m B p tau...    (tau = "all" for 2..p-1)      gates = (k+1) + m
cd "$(dirname "$0")"
k=$1; m=$2; B=$3; p=$4; shift; shift; shift; shift
taus="$*"; [ "$taus" = "all" ] && taus=$(seq 2 $((p-1)))
for tau in $taus; do
  printf "k=%s tau=%s (1/tau=%s): " $k $tau $(python3 -c "print(pow($tau,-1,$p))")
  python3 -c "
from math import comb
p=$p;t=$tau;k=$k
for i in range(k+1): print(' '.join(str(sum(comb(i,mm)*comb(k-i,j-mm)*pow(t,mm,p) for mm in range(0,min(i,j)+1) if j-mm<=k-i)%p) for j in range(k+1)))" | ./r2_brute $p $((k+1)) $m $B
done
