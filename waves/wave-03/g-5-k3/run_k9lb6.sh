#!/bin/bash
L() { python3 -B not-in-this-repository/wht35/bin/light.py g-5-k3 "$@" 2>/dev/null; }
echo "## K9, m = 6 (15 gates), GF(3), time limit 590 s (no RESULT line below = not finished)"
L 590 ./mincirc_odd 3 9 6 rows_k9.txt | grep -E "RESULT|skipped|visited"
echo "exit ${PIPESTATUS[0]}"
