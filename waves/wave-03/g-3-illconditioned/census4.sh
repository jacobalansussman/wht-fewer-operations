#!/bin/bash
# census4.sh p : the one-parameter family of 4 x 4 matrices that are "flat on both sides" (type II)
#   rows (1,1,1,1), (1,1,-1,-1), (1,-1,a,-a), (1,-1,-a,a)   (a = 1 or -1: the Walsh-Hadamard matrix; a = a square root of -1: the 4-point Fourier matrix)
# over GF(p), for every a: count (G) by d-0's mincirc (2 helpers = 6 gates, 3 helpers = 7 gates), and for p <= 7 the in-place count by inplace.
cd "$(dirname "$0")"
p=$1
for ((a=1; a<p; a++)); do
  printf "1 1 1 1\n1 1 -1 -1\n1 -1 %d %d\n1 -1 %d %d\n" $a $((p-a)) $((p-a)) $a > fam_p${p}_a$a.txt
  g2=$(../d-0-zeta/mincirc $p 4 2 fam_p${p}_a$a.txt | grep RESULT)
  g3=$(../d-0-zeta/mincirc $p 4 3 fam_p${p}_a$a.txt | grep RESULT)
  ip="-"
  if [ $p -le 7 ]; then ip=$(./inplace $p 0 4 4 0 23 fam_p${p}_a$a.txt | grep RESULT); fi
  echo "a=$a | $g2 | $g3 | in place: $ip"
done
