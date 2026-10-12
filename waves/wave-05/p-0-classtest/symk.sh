#!/bin/bash
# symk.sh: exact minimum (count G) of the (k+1) x (k+1) block "k-th kernel power on data that depend only on the number of 1-bits":
# entry (i, j) = sum_m C(i,m) C(k-i,j-m) tau^m  (at tau = -1 this is the Krawtchouk matrix).  gates = (k+1) + m.
# usage: symk.sh k mmax p...     tool: g-5-k3/mincirc_odd, exhaustive over GF(p)
cd "$(dirname "$0")"
M=../g-5-k3/mincirc_odd; k=$1; mmax=$2; shift; shift
for p in $*; do
  for tau in $(seq 2 $((p-1))); do
    f=rows_symk_tmp_$k.txt
    python3 -c "
from math import comb
p=$p;t=$tau;k=$k
for i in range(k+1): print(' '.join(str(sum(comb(i,m)*comb(k-i,j-m)*pow(t,m,p) for m in range(0,min(i,j)+1) if j-m<=k-i)%p) for j in range(k+1)))" > $f
    res="more than $((k+1+mmax))"
    for m in $(seq 0 $mmax); do
      r=$($M $p $((k+1)) $m $f 2>/dev/null | grep RESULT | head -1)
      case "$r" in *YES*) res="$((k+1+m))"; break;; esac
    done
    echo "k=$k p=$p tau=$tau (1/tau=$(python3 -c "print(pow($tau,-1,$p))")): $res gates"
  done
done
rm -f rows_symk_tmp_$k.txt
