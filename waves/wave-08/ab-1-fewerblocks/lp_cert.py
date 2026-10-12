#!/usr/bin/env python3
"""lp_cert.py [ab-1-fewerblocks]  EXACT certificate for the moves bound of lp.py at block size m (3 or 4).
Takes the dual solution of the float program, rounds it to fractions, and checks in exact arithmetic:
   weights w_Q >= 0 on the characters Q with <Q,I> = 1 ;  for EVERY block form B:  sum of w_Q over Q with <Q,B> = 1  <=  rank(B).
Then every unit of the sub-game for W arrays has at least W x (sum of the w_Q) moves (add the inequalities of section 4.2)."""
import sys, numpy as np
from fractions import Fraction as Fr
from scipy.optimize import linprog
m = int(sys.argv[1])
idx = [(i, j) for i in range(m) for j in range(i, m)]; nb = len(idx)
def rank2(code):
    M = [[0] * m for _ in range(m)]
    for t, (i, j) in enumerate(idx):
        if code >> t & 1: M[i][j] = M[j][i] = 1
    alt = not any(M[i][i] for i in range(m)); rk = 0
    for c in range(m):
        pv = next((i for i in range(rk, m) if M[i][c]), None)
        if pv is None: continue
        M[rk], M[pv] = M[pv], M[rk]
        for i in range(m):
            if i != rk and M[i][c]: M[i] = [a ^ b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk, alt
Bs = []; rk = []
for code in range(1, 1 << nb):
    r, alt = rank2(code)
    if not alt and r <= m - 1: Bs.append(code); rk.append(r)
Icode = sum(1 << t for t, (i, j) in enumerate(idx) if i == j)
par = [bin(x).count("1") & 1 for x in range(1 << nb)]
Qs = [q for q in range(1 << nb) if par[q & Icode]]
A = np.array([[par[q & b] for b in Bs] for q in Qs], dtype=float)
res = linprog(np.array(rk, float), A_ub=-A, b_ub=-np.ones(len(Qs)), bounds=(0, None), method="highs")
w = -res.ineqlin.marginals
wf = [Fr(float(x)).limit_denominator(960) for x in w]
assert all(x >= 0 for x in wf)
worst = max(Fr(sum((wf[a] for a, q in enumerate(Qs) if par[q & b]), Fr(0)), r) for b, r in zip(Bs, rk))
tot = sum(wf, Fr(0))
print("m = %d : float optimum %.6f ; rounded dual weights: %d characters used, denominators %s, total %s = %.6f" % (m, res.fun, sum(1 for x in wf if x), sorted(set(x.denominator for x in wf if x)), tot, float(tot)))
print("   exact check over all %d block forms: largest (load / rank) = %s  -> certified: at least %s = %.6f moves per live array" % (len(Bs), worst, tot / worst, float(tot / worst)))
ones = lambda q: sum(1 for z in range(1, 1 << m) if sum((q >> t & 1) & (z >> i & 1) & (z >> j & 1) for t, (i, j) in enumerate(idx)) & 1)
print("   number of active directions of the characters used:", sorted(set(ones(q) for q, x in zip(Qs, wf) if x)))
