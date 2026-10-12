#!/bin/bash
L() { python3 -B not-in-this-repository/wht35/bin/light.py g-5-k3 "$@" 2>/dev/null; }
echo "## symmetric square S6 of K3 (6 wires, 6 targets); tie value 8 gates = m 2"
for p in 3 5 7; do for m in 0 1 2 3 4; do echo "p=$p m=$m"; L 280 ./mincirc_odd $p 6 $m rows_s6.txt | grep -E "RESULT|skipped|visited| g[0-9]"; done; done
