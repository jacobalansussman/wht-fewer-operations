#!/usr/bin/env python3
"""twist.py -- structured batch: the transform of a sign-twisted copy is one 4-point brick on the transform.  Exact integers.
Claim: for u != v non-zero and D = diag((-1)^((u.a)(v.a))):   2 H D = (1 + X_u + X_v - X_(u+v)) H,   X_c = shift by c.
Checked for all pairs u, v at N = 4, 16, 64.  [e2-2-ladder]"""
import itertools
def dot(a, b): return bin(a & b).count("1") & 1
for k in (2, 4, 6):
    N = 1 << k
    H = [[-1 if dot(w, a) else 1 for a in range(N)] for w in range(N)]
    bad = 0; n = 0
    for u, v in itertools.combinations(range(1, N), 2):
        n += 1
        d = [-1 if (dot(u, a) and dot(v, a)) else 1 for a in range(N)]
        for w in range(N):
            for a in range(N):
                lhs = 2 * H[w][a] * d[a]
                rhs = H[w][a] + H[w ^ u][a] + H[w ^ v][a] - H[w ^ u ^ v][a]
                if lhs != rhs: bad += 1
    print("N = %d: %d pairs (u, v) checked, entries that differ: %d" % (N, n, bad))
