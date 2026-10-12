#!/usr/bin/env python3
"""e-4-passes / four_signs.py  exact.  The two 8-point arrangements with 23 non-zeros (exhaustive minimum), with
every choice of signs on rows and columns (a sign is the same as a coefficient -1 in an outer pass): does the
two-sided difference E factor as two differences (word P B B P)?  Uses four.factor."""
import sys, itertools
sys.path.insert(0, ".")
from pbp import had, emat
sys.argv = ["four.py", "8", "-1"]          # cap -1: the import runs no arrangement
import four
d = 8; H = had(d); ones = [1] * d
arrs = [((0,6,2,4,7,3,5,1), tuple(range(8)))]
tested = found = small = 0; hist = {}
for pi, sig in arrs:
    for sr in itertools.product((1, -1), repeat=d - 1):
        for sc in itertools.product((1, -1), repeat=d - 1):
            srr = (1,) + sr; scc = (1,) + sc
            M = [[H[pi[i]][sig[j]] * srr[i] * scc[j] for j in range(d)] for i in range(d)]
            R = [M[0][:]] + [[M[i][j] - M[i-1][j] for j in range(d)] for i in range(1, d)]
            E = [[R[i][0]] + [R[i][j] - R[i][j-1] for j in range(1, d)] for i in range(d)]
            n = sum(1 for r in E for v in r if v); hist[n] = hist.get(n, 0) + 1
            tested += 1
            if n <= 30:
                small += 1
                if four.factor(E):
                    found += 1
                    if found == 1: print("FOUND", pi, sig, srr, scc, E)
print("sign patterns tested:", tested, " with at most 30 non-zeros:", small, " factor as two differences:", found)
print("histogram of non-zeros (lowest):", sorted(hist.items())[:8])
