#!/bin/bash
L() { python3 -B not-in-this-repository/wht35/bin/light.py g-5-k3 "$@" 2>/dev/null; }
echo "## symmetric square S6 of K3: more budget"
for m in 5 6 7; do echo "p=3 m=$m"; L 300 ./mincirc_odd 3 6 $m rows_s6.txt | grep -E "RESULT|skipped|visited| g[0-9]"; done
for m in 5 6; do echo "p=5 m=$m"; L 400 ./mincirc_odd 5 6 $m rows_s6.txt | grep -E "RESULT|skipped|visited| g[0-9]"; done
