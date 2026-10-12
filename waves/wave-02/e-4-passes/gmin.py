#!/usr/bin/env python3
"""e-4-passes / gmin.py  exhaustive at d=8 (d=4): minimum over all row orders and all column orders (columns up
to GL(m,2), rows all) of G = number of odd 2x2 windows = #{(i,j): (pi_i+pi_(i-1)).(sig_j+sig_(j-1)) = 1},
and the joint minimum of corners + crossings.  Claim to test: G_min = (d/2) log2 d."""
import sys, itertools
sys.path.insert(0, ".")
from pbp import reduced_orders
d = int(sys.argv[1]); m = d.bit_length() - 1
par = [[bin(a & b).count("1") & 1 for b in range(d)] for a in range(d)]
sigs = reduced_orders(d); hist = {}
for sig in sigs:
    dl = [sig[j] ^ sig[j-1] for j in range(1, d)]
    for rest in itertools.permutations(range(1, d)):
        pi = (0,) + rest
        G = 0
        for i in range(1, d):
            row = par[pi[i] ^ pi[i-1]]
            for x in dl: G += row[x]
        hist[G] = hist.get(G, 0) + 1
print("d =", d, " (d/2) log2 d =", d * m // 2, "  histogram of G over all arrangements (columns up to GL):", sorted(hist.items())[:6], "... max", max(hist))
