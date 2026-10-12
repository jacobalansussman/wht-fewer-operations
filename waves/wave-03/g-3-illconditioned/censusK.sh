#!/bin/bash
# censusK.sh p : the family K_t = [[1,t],[t,1]] x [[1,t],[t,1]] at 4 points (entries t^(Hamming distance)); this is
# d-5's G(u) = u^W at k = 2 with t = (1-u)/(1+u).  t = a square root of -1: the transform up to scalings.  t = 1, -1: rank one.
# For every t in GF(p): is there a circuit with 6 gates, with 7 gates, in count (G) (d-0's mincirc, exhaustive for each t).
cd "$(dirname "$0")"
p=$1; y6=""; y7=""
for ((t=2; t<p-1; t++)); do
  t2=$(( t*t % p ))
  printf "1 %d %d %d\n%d 1 %d %d\n%d %d 1 %d\n%d %d %d 1\n" $t $t $t2 $t $t2 $t $t $t2 $t $t2 $t $t > K_p${p}_t$t.txt
  if ../d-0-zeta/mincirc $p 4 2 K_p${p}_t$t.txt | grep -q "YES"; then y6="$y6 $t"; fi
  if ../d-0-zeta/mincirc $p 4 3 K_p${p}_t$t.txt | grep -q "YES"; then y7="$y7 $t"; fi
done
echo "GF($p), t from 2 to p-2: t with a 6-gate circuit:${y6:- none}"
echo "GF($p), t from 2 to p-2: t with a 7-gate circuit:${y7:- none}"
rm -f K_p${p}_t*.txt
