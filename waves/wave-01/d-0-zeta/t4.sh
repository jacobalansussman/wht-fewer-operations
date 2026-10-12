#!/bin/bash
# t4.sh: known 4-point cases as a test of mincirc
cd "$(dirname "$0")"
L=not-in-this-repository/wht35/bin/light.py
while read kind k p m; do
  python3 -B rows.py $kind $k > rows_$kind$k.txt
  python3 -B $L d0-test 60 sh -c "./mincirc $p 4 $m < rows_$kind$k.txt" 2>/dev/null | grep -E "RESULT" | sed "s/^/$kind $k m=$m: /"
done <<EOT
zeta 2 5 0
zeta 2 5 1
had 2 5 2
had 2 5 3
had 2 7 2
had 2 7 3
jmi 4 5 1
jmi 4 5 2
jmi 4 7 1
jmi 4 3 1
EOT
