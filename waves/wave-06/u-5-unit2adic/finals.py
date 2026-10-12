# u-5: what one invocation leaves in every register when FULL contents are tracked (every register starts with its own value).
import sys, json, gzip
from fractions import Fraction as Fr
from collections import Counter
c = json.load(gzip.open(sys.argv[1])); h, v, R = c["h"], c["v"], c["R"]; nreg = 2*v+R
reg = [{r: Fr(1)} for r in range(nreg)]
k = lambda r: "x" if r < v else "y" if r < 2*v else "s"
def axpy(t, src, co):
    d = reg[t]
    for q, u in src.items():
        w = d.get(q, 0) + co*u
        if w: d[q] = w
        else: d.pop(q, None)
def run(G):
    for g in G:
        if g[0] == "neg": reg[g[2]] = {q: -u for q, u in reg[g[2]].items()}
        elif g[0] == "out":
            src = dict(reg[g[2]])
            for t, a, b in g[3]: axpy(t, src, Fr(a, b))
        else:
            for s, a, b in g[3]: axpy(g[2], reg[s], Fr(a, b))
run(c["A"])
tot = {kk: dict(reg[s]) for kk, s, f in c["ret"]}
print("the totals: kinds of contents", [dict(Counter(k(q) for q in tot[kk])) for kk in sorted(tot)][:3])
for t in range(v):
    for kk, a, b in c["scat"]["table"][t]:
        if a: axpy(v+t, tot[kk], Fr(a, b))
print("y right after the scatter: kinds of contents", dict(Counter(tuple(sorted(Counter(k(q) for q in reg[v+t]).items())) for t in range(v))))
run(c["B"])
print("x final:", dict(Counter(tuple(sorted(Counter(k(q) for q in reg[t]).items())) for t in range(v))))
print("y final:", dict(Counter(tuple(sorted(Counter(k(q) for q in reg[v+t]).items())) for t in range(v))))
print("   y_t final contains x_t with coefficient", Counter(reg[v+t].get(t) for t in range(v)), "and y_t with", Counter(reg[v+t].get(v+t) for t in range(v)))
print("   y_t final minus (x_t + y_t): number of helper values left:", sorted(Counter(len(reg[v+t]) - 2 for t in range(v)).items()))
hs = Counter(); hx = 0; hy = 0
for r in range(2*v, nreg):
    hs[len(reg[r])] += 1; hx += sum(1 for q in reg[r] if q < v); hy += sum(1 for q in reg[r] if v <= q < 2*v)
print("helpers final: x values left in helpers:", hx, "; y values:", hy, "; number of helper values held, histogram:", sorted(hs.items()))
# the helper-to-helper map L and the helper-to-y map
import itertools
idx = {r: i for i, r in enumerate(range(2*v, nreg))}
L = [[reg[r].get(q, Fr(0)) for q in range(2*v, nreg)] for r in range(2*v, nreg)]
def rank(A):
    A = [r[:] for r in A]; rk = 0
    for col in range(len(A[0])):
        p = next((i for i in range(rk, len(A)) if A[i][col]), None)
        if p is None: continue
        A[rk], A[p] = A[p], A[rk]
        for i in range(len(A)):
            if i != rk and A[i][col]:
                q = A[i][col]/A[rk][col]; A[i] = [x - q*y for x, y in zip(A[i], A[rk])]
        rk += 1
    return rk
print("helper-to-helper matrix L (%d x %d): rank" % (R, R), rank(L), "; entries", sorted(Counter(x for row in L for x in row).items())[:12])
Y = [[reg[v+t].get(q, Fr(0)) for q in range(2*v, nreg)] for t in range(v)]
print("helper values inside the targets (120 x %d): rank" % R, rank(Y), "; non-zeros", sum(1 for row in Y for x in row if x))
