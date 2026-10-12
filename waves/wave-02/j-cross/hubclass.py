#!/usr/bin/env python3
# j-cross / hubclass.py : does the 4-point "hub" (the shape behind the 7-gate brick) exist anywhere else in the class of
# 2 x 2 kernels?  Shape tested: (kernel tensor kernel) = (rank-one matrix) + (matrix with one non-zero per row and column),
# i.e. one wire that is one gate from all four outputs with single inputs as partners (3 + 4 = 7 gates instead of 8).
# Kernels [[1, a], [b, c]] with a, b, c in a small set of rationals, no zero entry, invertible; invariant tau = c / (a*b)
# (unchanged by scaling rows and columns; the Walsh-Hadamard kernel has tau = -1).  Exact Fractions.
from fractions import Fraction as F
import itertools
vals = [F(x) for x in (1, -1, 2, -2, 3, -3)] + [F(1, 2), F(-1, 2), F(1, 3), F(-1, 3)]
def hub(M):
    n = len(M); hits = []
    for pi in itertools.permutations(range(n)):
        # is M equal to a rank-one matrix off the positions (i, pi[i])?  all entries of M are non-zero here.
        u = [None] * n; v = [None] * n; u[0] = F(1); ok = True; changed = True
        while changed and ok:
            changed = False
            for i in range(n):
                for j in range(n):
                    if j == pi[i]: continue
                    if u[i] is not None and v[j] is None: v[j] = M[i][j] / u[i]; changed = True
                    elif u[i] is None and v[j] is not None: u[i] = M[i][j] / v[j]; changed = True
                    elif u[i] is not None and v[j] is not None and u[i] * v[j] != M[i][j]: ok = False
        if ok and all(x is not None for x in u + v):
            # the remainder on the monomial positions must be non-zero everywhere (else M itself is closer to rank one)
            if all(M[i][pi[i]] - u[i] * v[pi[i]] != 0 for i in range(n)): hits.append(pi)
    return hits
taus = {}; n = 0
for a, b, c in itertools.product(vals, repeat=3):
    if c == a * b: continue
    n += 1; K = [[F(1), a], [b, c]]
    M = [[K[i >> 1][j >> 1] * K[i & 1][j & 1] for j in range(4)] for i in range(4)]
    tau = c / (a * b); h = hub(M)
    t = taus.setdefault(tau, [0, 0]); t[0] += 1; t[1] += 1 if h else 0
print('kernels tried:', n, '| distinct tau:', len(taus))
print('tau with a hub (kernels with a hub / kernels with that tau):', {str(t): '%d/%d' % (v[1], v[0]) for t, v in sorted(taus.items()) if v[1]})
print('tau without a hub:', sorted(str(t) for t, v in taus.items() if not v[1]))
