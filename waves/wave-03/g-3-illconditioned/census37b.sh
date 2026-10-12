#!/bin/bash
# census37b.sh: the whole family over GF(37): which a have a 7-gate circuit in count (G)
cd "$(dirname "$0")"
p=37; yes=""
for ((a=1; a<p; a++)); do
  printf "1 1 1 1\n1 1 -1 -1\n1 -1 %d %d\n1 -1 %d %d\n" $a $((p-a)) $((p-a)) $a > fam_p${p}_a$a.txt
  if ../d-0-zeta/mincirc $p 4 3 fam_p${p}_a$a.txt | grep -q "RESULT p=37: YES"; then yes="$yes $a"; fi
done
echo "GF(37): values of a with a 7-gate circuit (exhaustive for each a):$yes"
echo "for comparison: 1/3 = 25, -1/3 = 12, -3 = 34, square roots of -1: 6 31, sixth roots of unity: 10 26 27 11"
