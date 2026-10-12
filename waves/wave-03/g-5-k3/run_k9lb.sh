#!/bin/bash
L() { python3 -B not-in-this-repository/wht35/bin/light.py g-5-k3 "$@" 2>/dev/null; }
echo "## K9 = K3 (x) K3 (9 wires, 9 targets): exhaustive lower bound, gates = 9 + m"
for m in 0 1 2 3 4 5; do echo "p=3 m=$m"; L 400 ./mincirc_odd 3 9 $m rows_k9.txt | grep -E "RESULT|skipped|visited"; done
