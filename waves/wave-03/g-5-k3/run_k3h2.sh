#!/bin/bash
L() { python3 -B not-in-this-repository/wht35/bin/light.py g-5-k3 "$@" 2>/dev/null; }
echo "## K3 (x) H2 on 6 wires, 6 targets: textbook 14, inherited (7-gate brick) 13; gates = 6 + m"
for p in 3 5 7; do for m in 4 5 6 7; do echo "p=$p m=$m"; L 500 ./mincirc_odd $p 6 $m rows_k3h2.txt | grep -E "RESULT|skipped|visited| g[0-9]"; done; done
