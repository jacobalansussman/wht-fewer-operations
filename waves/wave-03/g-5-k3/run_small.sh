#!/bin/bash
L() { python3 -B not-in-this-repository/wht35/bin/light.py g-5-k3 "$@" 2>/dev/null; }
echo "## controls (known: 4-point transform needs exactly 7 gates, count G)"
for p in 3 5; do for m in 2 3; do echo -n "n=4 "; L 60 ./mincirc_odd $p 4 $m rows_h4.txt | grep RESULT; echo -n "n=5 (dummy wire) "; L 60 ./mincirc_odd $p 5 $m rows_h4pad.txt | grep RESULT; done; done
echo "## K3 (3 wires)"
for p in 3 5 7 11; do for m in 0 1; do L 60 ./mincirc_odd $p 3 $m rows_k3.txt | grep -E "RESULT|skipped"; done; done
echo "## two copies of K3 on disjoint data (6 wires)"
for p in 3 5 7; do for m in 1 2; do L 120 ./mincirc_odd $p 6 $m rows_k3x2.txt | grep -E "RESULT|skipped"; done; done
echo "## antisymmetric square A3 = -2 K3^T (3 wires)"
for p in 3 5 7; do for m in 0 1; do L 60 ./mincirc_odd $p 3 $m rows_a3.txt | grep -E "RESULT|skipped"; done; done
