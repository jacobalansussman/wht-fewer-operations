#!/bin/bash
# the class of K3 (x) H2: S_tau (x) K_tau over GF(5); gates = 6 + m; tau = 4 is the transform (control: g-5 found 12 = 6 + 6)
cd "$(dirname "$0")"
M=../g-5-k3/mincirc_odd
for t in 4 2 3; do for m in 5 6; do
  echo "p=5 tau=$t m=$m gates=$((6+m))"
  python3 -B not-in-this-repository/wht35/bin/light.py p0-sym 590 $M 5 6 $m rows_sym_p5_t$t.txt 2>&1 | grep -E "RESULT|visited|LIGHT|no free" | cut -c1-200
done; done
