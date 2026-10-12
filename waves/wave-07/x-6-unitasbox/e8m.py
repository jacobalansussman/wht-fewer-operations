#!/usr/bin/env python3
"""e8m.py [x-6-unitasbox]  Exact.  The scatter matrix M of the published E8 certificate (read only): M[t][s] = how much of source s
target t holds right after the scatter.  Checks: diagonal 1; off-diagonal entries; 'knows' = even overlap of the ports;
rank; M M = kappa M; and two counts for the port family: the largest set of ports no two of which know each other (the rank
of ANY scatter for these ports is at least that), the largest set that all know each other."""
import sys, json, gzip
from fractions import Fraction as Fr
from collections import Counter
c = json.load(gzip.open(sys.argv[1])); h, v, R = c["h"], c["v"], c["R"]; nreg = 2 * v + R
reg = [({r: Fr(1)} if r < 2 * v else {}) for r in range(nreg)]
def axpy(t, src, co):
    d = reg[t]
    for k, u in src.items():
        w = d.get(k, 0) + co * u
        if w: d[k] = w
        else: d.pop(k, None)
for g in c["A"]:
    if g[0] == "neg": reg[g[2]] = {k: -u for k, u in reg[g[2]].items()}
    elif g[0] == "out":
        src = dict(reg[g[2]])
        for t, a, b in g[3]: axpy(t, src, Fr(a, b))
    else:
        for s, a, b in g[3]: axpy(g[2], dict(reg[s]), Fr(a, b))
tot = {k: dict(reg[s]) for k, s, f in c["ret"]}
P = c["ports"]; par = lambda x: bin(x).count("1") & 1
M = [[Fr(0)] * v for _ in range(v)]
for t in range(v):
    for k, a, b in c["scat"]["table"][t]:
        for s, u in tot[k].items():
            assert s < v
            M[t][s] += Fr(a, b) * u
print("ports: %d, weights %s, all distinct: %s" % (v, dict(Counter(bin(p).count('1') for p in P)), len(set(P)) == v))
print("diagonal of M all 1:", all(M[t][t] == 1 for t in range(v)), "; off-diagonal entries:", dict(Counter(str(M[t][s]) for t in range(v) for s in range(v) if s != t)))
print("M[t][s] != 0 exactly when the ports of t and s overlap evenly (t knows s), s != t:", all((M[t][s] != 0) == (par(P[t] & P[s]) == 0) for t in range(v) for s in range(v) if s != t))
print("each target knows:", dict(Counter(sum(1 for s in range(v) if s != t and par(P[t] & P[s]) == 0) for t in range(v))))
def rank(A):
    A = [r[:] for r in A]; rk = 0
    for col in range(len(A[0])):
        pv = next((i for i in range(rk, len(A)) if A[i][col]), None)
        if pv is None: continue
        A[rk], A[pv] = A[pv], A[rk]
        for i in range(rk + 1, len(A)):
            if A[i][col]:
                q = A[i][col] / A[rk][col]; A[i] = [x - q * y for x, y in zip(A[i], A[rk])]
        rk += 1
    return rk
MM = [[sum(M[i][k] * M[k][j] for k in range(v)) for j in range(v)] for i in range(v)]
kap = MM[0][0] / M[0][0]
print("rank of M over the rationals: %d ; M M = %s M: %s ; symmetric: %s ; sources per total kappa = v / rank = %s" % (rank(M), kap, MM == [[kap * x for x in r] for r in M], all(M[i][j] == M[j][i] for i in range(v) for j in range(v)), Fr(v, rank(M))))
# largest clique by simple branch and bound on bitsets
def maxclique(adj):
    best = [0]
    def rec(cand, size):
        if size + bin(cand).count("1") <= best[0]: return
        if not cand:
            best[0] = max(best[0], size); return
        while cand:
            if size + bin(cand).count("1") <= best[0]: return
            i = cand.bit_length() - 1; cand &= ~(1 << i)
            rec(cand & adj[i], size + 1)
    rec((1 << len(adj)) - 1, 0); return best[0]
non = [sum(1 << s for s in range(v) if s != t and par(P[t] & P[s]) == 1) for t in range(v)]
kn = [sum(1 << s for s in range(v) if s != t and par(P[t] & P[s]) == 0) for t in range(v)]
print("largest set of ports no two of which know each other: %d  (so every scatter matrix for these ports and these hyperplanes has rank >= that)" % maxclique(non))
print("largest set of ports that all know each other (an orthonormal set): %d  (h = %d)" % (maxclique(kn), h))
print("the design gains when kappa > 5h/4 = %.2f (five-stage word); with only the %d coordinate directions as ports kappa <= %d" % (5 * h / 4, h, h))
