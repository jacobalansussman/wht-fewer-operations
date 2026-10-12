#!/bin/sh
# all closed sets of alt forms: a quad needs its two cherries, the half both quads, the root the half
for ex in "" x1x3; do
for cfg in 0 1 3 4 12 15 5 7 13 19 23 27 31 44 46 45 47 63 127 255 79 207; do
  r=$(python3 -B branch3x.py $cfg $ex | ./dwg)
  e=$(python3 -c "print(bin($cfg).count('1'))")
  echo "centre x0x3${ex:++$ex}  cfg $cfg  alt forms $e  steps from origin $r  branch cost $((r-1+e))"
done; done
