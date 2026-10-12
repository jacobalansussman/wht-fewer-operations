#!/usr/bin/env python3
"""scatter.py [h-7-unitmeter]  The scatter of the published unit as a 120 x 120 matrix, exact rationals.
Replays phase A of the certificate (x-content), reads the 8 retained totals T_k (vectors over the 120 sources) and the
scatter table C (120 x 8), and forms M = C T: row S = what target S holds right after the scatter.
Reports: entries, rank, whether M is a multiple of a projector, the 'knows' graph, the frames used and how many are oblique.
usage: python3 -I -B scatter.py <certificate.json.gz>"""
import sys, json, gzip
from fractions import Fraction as Fr
from collections import Counter
c = json.load(gzip.open(sys.argv[1])); h, v, R = c["h"], c["v"], c["R"]; nreg = 2*v+R
reg = [({r: Fr(1)} if r < v else {}) for r in range(nreg)]
def axpy(t, src, co):
    d = reg[t]
    for k, u in src.items():
        w = d.get(k, 0) + co*u
        if w: d[k] = w
        else: d.pop(k, None)
for g in c["A"]:
    if g[0] == "neg": reg[g[2]] = {k: -u for k, u in reg[g[2]].items()}
    elif g[0] == "out":
        src = dict(reg[g[2]])
        for t, a, b in g[3]: axpy(t, src, Fr(a, b))
    else:
        for s, a, b in g[3]: axpy(g[2], reg[s], Fr(a, b))
T = [[reg[s].get(j, Fr(0)) for j in range(v)] for k, s, f in sorted(c["ret"])]
C = [[Fr(0)]*len(T) for _ in range(v)]
for S in range(v):
    for k, a, b in c["scat"]["table"][S]: C[S][k] += Fr(a, b)
M = [[sum(C[S][k]*T[k][j] for k in range(len(T))) for j in range(v)] for S in range(v)]
def rank(A):
    A = [r[:] for r in A]; rk = 0
    for col in range(len(A[0])):
        p = next((i for i in range(rk, len(A)) if A[i][col]), None)
        if p is None: continue
        A[rk], A[p] = A[p], A[rk]
        for i in range(len(A)):
            if i != rk and A[i][col]:
                q = A[i][col]/A[rk][col]
                A[i] = [x - q*y for x, y in zip(A[i], A[rk])]
        rk += 1
    return rk
print("entries of the totals T (8 x 120):", sorted(Counter(x for r in T for x in r).items()))
print("entries of the scatter table C (120 x 8):", sorted(Counter(x for r in C for x in r).items()))
print("M = C T (120 x 120): diagonal entries", sorted(Counter(M[i][i] for i in range(v)).items()),
      "; off-diagonal", sorted(Counter(M[i][j] for i in range(v) for j in range(v) if i != j).items()))
print("rank T =", rank(T), " rank C =", rank(C), " rank M =", rank(M), " rank (M - I) =", rank([[M[i][j]-(i==j) for j in range(v)] for i in range(v)]))
print("M symmetric:", all(M[i][j] == M[j][i] for i in range(v) for j in range(v)))
M2 = [[sum(M[i][k]*M[k][j] for k in range(v)) for j in range(v)] for i in range(v)]
lam = M2[0][0]/M[0][0]
print("M*M = lambda*M with lambda =", lam, ":", all(M2[i][j] == lam*M[i][j] for i in range(v) for j in range(v)))
ports = c["ports"]; par = lambda x: bin(x).count("1") & 1
print("non-zero off-diagonal entry <=> the two port words overlap in an even number of places:",
      all((M[i][j] != 0) == (par(ports[i] & ports[j]) == 0) for i in range(v) for j in range(v) if i != j))
print("port weights:", sorted(Counter(bin(q).count("1") for q in ports).items()))
# common neighbours (strongly regular?)
adj = [[1 if i != j and M[i][j] != 0 else 0 for j in range(v)] for i in range(v)]
cn_adj = Counter(sum(adj[i][k]*adj[j][k] for k in range(v)) for i in range(v) for j in range(i) if adj[i][j])
cn_non = Counter(sum(adj[i][k]*adj[j][k] for k in range(v)) for i in range(v) for j in range(i) if not adj[i][j])
print("the 'knows' graph: degree", sorted(Counter(sum(r) for r in adj).items()), "; common neighbours of a knowing pair", dict(cn_adj), ", of a non-knowing pair", dict(cn_non))
fr = [tuple(f) for f in c["frames"]]
used = set(c["start"]) | set(c["final"]) | {g[1] for g in c["A"]+c["B"]}
ob = sum(1 for i in used if any(bin(b).count("1") > 1 for b in fr[i]))
print("frames (subspaces of F_2^%d) in the table: %d; used: %d; of the used ones, not spanned by coordinate vectors in the stored basis: %d; by dimension:" % (h, len(fr), len(used), ob),
      sorted(Counter(len(fr[i]) for i in used).items()))
