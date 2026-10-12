#!/bin/bash
L() { python3 -B not-in-this-repository/wht35/bin/light.py g-5-k3 "$@" 2>/dev/null; }
echo "## layer A of K3 (x) K3 alone (4-point transform, two butterflies, one idle wire; 9 wires): 11 known; gates = 8 + m"
for p in 3 5; do for m in 2 3; do echo -n "p=$p m=$m: "; L 100 ./mincirc_odd $p 9 $m rows_layerA9.txt | grep -E "RESULT"; done; done
