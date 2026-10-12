#!/usr/bin/env python3
"""g-1 replay8.py: independent exact replay of a circuit printed by sa8.py.  Count (G).
Reads the wire list (vectors in order), and for each wire finds two EARLIER wires u, v and exact rationals a, b with
wire = a*u + b*v (solved in Fractions, checked on every coordinate).  Then checks that the 8 rows of the Sylvester matrix
H_8 (up to sign) are all present.  No code shared with sa8.py / pool.py."""
import sys, re
from fractions import Fraction as F
def solve(u, v, w):
    n = len(w)
    for i in range(n):
        for j in range(i + 1, n):
            det = u[i] * v[j] - u[j] * v[i]
            if det != 0:
                a = F(w[i] * v[j] - w[j] * v[i], det); b = F(u[i] * w[j] - u[j] * w[i], det)
                if all(a * u[t] + b * v[t] == w[t] for t in range(n)): return a, b
                return None
    return None
wires = [[1 if i == j else 0 for i in range(8)] for j in range(8)]; names = ["x%d" % i for i in range(8)]
gates = 0; ok = True
for line in open(sys.argv[1]):
    m = re.match(r"\s+(help|OUT)\s+\(\d+,\d+\)\s+\[(.*)\]", line)
    if not m: continue
    w = [int(x) for x in m.group(2).split(",")]; found = None
    for i in range(len(wires)):
        for j in range(i):
            r = solve(wires[i], wires[j], w)
            if r and r[0] != 0 and r[1] != 0: found = (i, j, r); break
        if found: break
    gates += 1
    if not found: ok = False; print("NO JUSTIFICATION for", w); 
    else:
        i, j, (a, b) = found; print("g%-2d %s = (%s)*%s + (%s)*%s   %s" % (gates, m.group(1), a, names[i], b, names[j], w))
    wires.append(w); names.append("g%d" % gates)
H = [[(-1) ** bin(i & j).count("1") for j in range(8)] for i in range(8)]
have = {tuple(w) for w in wires} | {tuple(-x for x in w) for w in wires}
print("gates: %d; every gate justified exactly: %s; all 8 rows of H_8 present up to sign: %s" % (gates, ok, all(tuple(r) in have for r in H)))
