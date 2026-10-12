#!/usr/bin/env python3
"""ag-9 scan4.py: 4 points, the family K_t (x) K_s, K_t = [[1,1],[1,t]] (every 2 x 2 kernel with non-zero entries is one K_t up to
free scalings; the transform is t = s = -1).  For every t, s modulo p (not 0; 1 = rank one is listed apart) ask mincirc
(exhaustive modulo p) for the least number of helpers m.  Count (G).  usage: scan4.py p [diag]"""
import sys, subprocess
p = int(sys.argv[1]); diag = len(sys.argv) > 2
MC = "waves/wave-01/d-0-zeta/mincirc"
def least(rows):
    txt = "\n".join(" ".join(str(x % p) for x in r) for r in rows) + "\n"
    for m in range(0, 4):
        out = subprocess.run([MC, str(p), "4", str(m)], input=txt, capture_output=True, text=True).stdout
        if "YES" in out:
            ng = [l for l in out.splitlines() if "non-input distinct targets" in l][0]
            nt = int(ng.split("targets=")[1].split()[0])
            return nt + m
    return None
res = {}
for t in range(2, p):
    for s in ([t] if diag else range(t, p)):
        rows = [(1, 1, 1, 1), (1, t, 1, t), (1, 1, s, s), (1, t, s, t * s)]
        res[(t, s)] = least(rows)
from collections import Counter
print("p =", p, "least gates over all (t, s), t <= s, t, s not 0 or 1:", sorted(Counter(res.values()).items()))
low = sorted(k for k, v in res.items() if v is not None and v < 7)
print("pairs below 7 gates:", [(k, res[k]) for k in low])
print("the transform t = s = -1:", res.get((p - 1, p - 1)))
