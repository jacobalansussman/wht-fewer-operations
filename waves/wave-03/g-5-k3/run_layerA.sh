#!/bin/bash
L() { python3 -B not-in-this-repository/wht35/bin/light.py g-5-k3 "$@" 2>/dev/null; }
echo "## layer A of K3 (x) H2 alone (4-point transform and a butterfly on disjoint data, 6 wires): 9 known; gates = 6 + m"
for p in 3 5 7; do for m in 2 3; do echo -n "p=$p m=$m: "; L 200 ./mincirc_odd $p 6 $m rows_layerA6.txt | grep -E "RESULT"; done; done
