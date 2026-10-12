#!/usr/bin/env python3
"""lp.py [ab-1-fewerblocks]  THE CHARACTER FLOOR OF THE SUB-GAME (no address maps, no phase letters), as a linear program.
[derived tonight, checked by nobody]  In the sub-game the paid letters and the shifts generate a commutative group; modulo
shifts a product of moves along z_1..z_k is the symmetric bit matrix B = sum z_j z_j^T, the kernel is the identity matrix I.
Every quadratic form Q on the m address bits is a character: move z -> (-1)^Q(z), block -> (-1)^<Q,B>, kernel -> (-1)^<Q,I>.
For a character with <Q,I> = 1 the unit must negate all W live arrays and each block negates one array, so
        for every Q with <Q,I> = 1 :   number of blocks with <Q,B_j> = 1   >=   W.
A block of rank k (k independent directions, 1 <= k <= m-1) has a form B of rank k that is not alternating.
LP: minimise sum_B x_B cost(B) subject to those inequalities (W = 1).  cost = rank (moves) or (rank/m)^z (the engine's price).
A value >= m for moves means: no unit of the sub-game saves a move.  A price >= 1 at exponent z means: no unit of the sub-game
certifies that z.  FLOATS (HiGHS); the m = 3 answer is checked by hand in the report."""
import sys, itertools, numpy as np
from scipy.optimize import linprog
m = int(sys.argv[1])
idx = [(i, j) for i in range(m) for j in range(i, m)]; nb = len(idx)
def rank2(M):
    M = [r[:] for r in M]; rk = 0
    for c in range(m):
        pv = next((i for i in range(rk, m) if M[i][c]), None)
        if pv is None: continue
        M[rk], M[pv] = M[pv], M[rk]
        for i in range(m):
            if i != rk and M[i][c]: M[i] = [a ^ b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
Bs = []; rk = []
for code in range(1, 1 << nb):
    M = [[0] * m for _ in range(m)]
    for t, (i, j) in enumerate(idx):
        if code >> t & 1: M[i][j] = M[j][i] = 1
    if not any(M[i][i] for i in range(m)): continue          # alternating: not the form of one block
    r = rank2(M)
    if r <= m - 1: Bs.append(code); rk.append(r)
Icode = sum(1 << t for t, (i, j) in enumerate(idx) if i == j)
par = np.array([bin(x).count("1") & 1 for x in range(1 << nb)], dtype=np.int8)
Qs = [q for q in range(1 << nb) if par[q & Icode]]
A = np.array([[par[q & b] for b in Bs] for q in Qs], dtype=float)
rk = np.array(rk, dtype=float)
print("m = %d : %d block forms (not alternating, rank 1..%d), by rank %s ; %d characters with <Q,I> = 1" % (m, len(Bs), m - 1, {int(k): int((rk == k).sum()) for k in sorted(set(rk))}, len(Qs)))
def solve(cost):
    res = linprog(cost, A_ub=-A, b_ub=-np.ones(len(Qs)), bounds=(0, None), method="highs")
    return res
r1 = solve(rk)
print("   least moves per live array (LP):            %.6f   (plain schedule: %d)" % (r1.fun, m))
r0 = solve(np.ones(len(Bs)))
print("   least blocks per live array (LP):           %.6f   (plain schedule: 2)" % r0.fun)
print("   exponent z : least price per live array (LP)   [a unit certifies z only if its price is below 1]")
lo, hi = 0.0, 1.0
for z in (1.0, 0.95, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1):
    r = solve((rk / m) ** z); print("      z = %.2f : %.6f" % (z, r.fun))
for _ in range(40):
    mid = (lo + hi) / 2
    if solve((rk / m) ** mid).fun < 1: hi = mid
    else: lo = mid
print("   the LP price reaches 1 at z = %.6f : the character inequalities alone allow no saving above %.6f in the sub-game at block size %d" % (hi, 1 - hi, m))
r = solve((rk / m) ** (hi + 1e-6)); x = r.x
sup = [(Bs[i], int(rk[i]), x[i]) for i in range(len(Bs)) if x[i] > 1e-9]
print("   the minimising 'fractional unit' just above that z: %d forms used, total weight by rank: %s ; blocks per array %.4f ; moves per array %.4f"
      % (len(sup), {k: round(sum(w for b, kk, w in sup if kk == k), 4) for k in sorted(set(kk for b, kk, w in sup))}, sum(w for b, kk, w in sup), sum(kk * w for b, kk, w in sup)))
