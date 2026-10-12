#!/bin/bash
# census37.sh: the same family over GF(37), which contains both a square root of -1 (6, 31) and the sixth roots of unity (10, 26, 27, 11)
cd "$(dirname "$0")"
p=37
for a in 1 36 10 26 27 11 6 31 2 3 5 7; do
  printf "1 1 1 1\n1 1 -1 -1\n1 -1 %d %d\n1 -1 %d %d\n" $a $((p-a)) $((p-a)) $a > fam_p${p}_a$a.txt
  g3=$(../d-0-zeta/mincirc $p 4 3 fam_p${p}_a$a.txt | grep RESULT)
  echo "a=$a | $g3"
done
