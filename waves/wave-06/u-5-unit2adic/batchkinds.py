#!/usr/bin/env python3
"""batchkinds.py [u-5]  The batch side only, fast: for every addition term of one invocation, the kind of gate modulo 2
(J disjoint / J nested / J cross / S / Q / E) from the classes of the target before, the source, and the target after.
Class of a content vector = the set of registers on which it has its least power of 2.  Reading: helpers start empty,
every x and y register holds its own value.  Also: where the Q additions are, and how deep under its row the wanted
term sits right after the scatter.   usage: python3 -I -B batchkinds.py <certificate.json.gz>"""
import sys, json, gzip
from fractions import Fraction as Fr
from collections import Counter
c = json.load(gzip.open(sys.argv[1])); h, v, R = c["h"], c["v"], c["R"]; nreg = 2 * v + R
reg = [({r: Fr(1)} if r < 2 * v else {}) for r in range(nreg)]
def v2(q):
    n, d = q.numerator, q.denominator
    return ((n & -n).bit_length() - 1) - ((d & -d).bit_length() - 1)
def cls(w):
    if not w: return frozenset()
    vals = {k: v2(q) for k, q in w.items()}; m = min(vals.values())
    return frozenset(k for k, e in vals.items() if e == m)
C = [cls(w) for w in reg]
kinds = Counter(); qlist = []; last = {}; nterm = 0
def axpy(t, src, Bs, co, ph):
    global nterm
    d = reg[t]; Bt = C[t]; empty = not d
    for k, u in src.items():
        w = d.get(k, 0) + co * u
        if w: d[k] = w
        else: d.pop(k, None)
    Bn = C[t] = cls(d)
    nterm += 1; last[t] = nterm
    if empty: kinds[(ph, "copy")] += 1; return
    if Bt == Bs == Bn: kd = "E"
    elif Bt == Bs: kd = "Q"; qlist.append((nterm, t, ph, len(Bt), len(Bn)))
    elif Bn == Bt or Bn == Bs: kd = "S"
    elif not (Bt & Bs): kd = "J disjoint"
    elif Bt <= Bs or Bs <= Bt: kd = "J nested"
    else: kd = "J cross"
    kinds[(ph, kd)] += 1
def run(G, ph):
    for g in G:
        if g[0] == "neg": reg[g[2]] = {k: -u for k, u in reg[g[2]].items()}
        elif g[0] == "out":
            src = dict(reg[g[2]]); Bs = C[g[2]]
            for t, a, b in g[3]: axpy(t, src, Bs, Fr(a, b), ph)
        else:
            for s, a, b in g[3]: axpy(g[2], reg[s], C[s], Fr(a, b), ph)
run(c["A"], "A")
tot = {k: (dict(reg[s]), C[s]) for k, s, f in c["ret"]}
def scat_row(t):
    sc = c["scat"]
    if "table" in sc: return [(k, Fr(a, b)) for k, a, b in sc["table"][t]]
    sin, sout = Fr(*sc["inside"]), Fr(*sc["outside"])
    return [(k, sin if c["ports"][t] >> k & 1 else sout) for k in range(h)]
for t in range(v):
    for k, co in scat_row(t):
        if co and k in tot: axpy(v + t, tot[k][0], tot[k][1], co, "scatter")
depth = Counter(); sizes = Counter()
for t in range(v):
    w = reg[v + t]; m = min(v2(q) for q in w.values())
    depth[v2(w[t]) - m] += 1; sizes[len(C[v + t])] += 1
SB = [C[v + t] for t in range(v)]
def rank2(sets):
    rows = [sum(1 << k for k in S) for S in sets]; piv = {}
    for x in rows:
        while x:
            l = x.bit_length() - 1
            if l in piv: x ^= piv[l]
            else: piv[l] = x; break
    return len(piv)
r2_targets = rank2(SB)
r2_tot = rank2([cls(tot[k][0]) for k in tot])
after = [dict(reg[v + t]) for t in range(v)]
def qrank(rows, cols):
    A = [[w.get(j, Fr(0)) for j in cols] for w in rows]; rk = 0
    for col in range(len(cols)):
        pv = next((i for i in range(rk, len(A)) if A[i][col]), None)
        if pv is None: continue
        A[rk], A[pv] = A[pv], A[rk]
        for i in range(rk + 1, len(A)):
            if A[i][col]:
                q = A[i][col] / A[rk][col]; A[i] = [x - q * y for x, y in zip(A[i], A[rk])]
        rk += 1
    return rk
rq_tot = qrank([tot[k][0] for k in sorted(tot)], range(v))
run(c["B"], "B")
ok = all(reg[t] == {t: 1} for t in range(v)) and all(reg[v + t] == {t: 1, v + t: 1} for t in range(v))
print("certificate h=%d v=%d R=%d cst=%d; totals %d; replay ends with x_t alone and y_t + x_t: %s" % (h, v, R, c["cst"], len(c["ret"]), ok))
tab = {}
for (ph, kd), q in kinds.items(): tab.setdefault(kd, {})[ph] = q
for kd in ("copy", "J disjoint", "J nested", "J cross", "S", "Q", "E"):
    r = tab.get(kd, {}); print("  %-11s A %6d  scatter %6d  B %6d   total %6d" % (kd, r.get("A", 0), r.get("scatter", 0), r.get("B", 0), sum(r.values())))
qy = [q for q in qlist if v <= q[1] < 2 * v]; qs = [q for q in qlist if q[1] >= 2 * v]
print("  Q additions: %d, all in phase %s; into targets: %d (distinct targets %d; each is the last addition into its target: %s; class sizes before -> after: %s)"
      % (len(qlist), sorted({q[2] for q in qlist}), len(qy), len({q[1] for q in qy}), all(last[q[1]] == q[0] for q in qy), Counter((q[3], q[4]) for q in qy).most_common(4)))
print("               into helpers: %d (class sizes before -> after: %s); into sources: %d" % (len(qs), Counter((q[3], q[4]) for q in qs).most_common(4), len(qlist) - len(qy) - len(qs)))
print("  Q gates per invocation at one digit column = (cst + Q additions) * 2^h = (%d + %d) * 2^%d; cst / v = %.3f; Q additions / v = %.3f" % (c["cst"], len(qlist), h, c["cst"] / v, len(qlist) / v))
print("  right after the scatter: wanted term x_t sits this many powers of 2 above the least power in its row: %s; class sizes %s" % (dict(depth), dict(sorted(sizes.items()))))
print("  rank: the %d totals over the rationals %d; the classes of the totals modulo 2: %d; the %d target classes right after the scatter modulo 2: %d"
      % (len(tot), rq_tot, r2_tot, v, r2_targets))
if v <= 200:
    cr = sum(1 for i in range(v) for j in range(i) if SB[i] & SB[j] and not SB[i] <= SB[j] and not SB[j] <= SB[i])
    print("  pairs of target classes that overlap without nesting right after the scatter: %d of %d" % (cr, v * (v - 1) // 2))
else:
    import random
    random.seed(1); S = 0; T = 20000
    for _ in range(T):
        i, j = random.sample(range(v), 2)
        S += bool(SB[i] & SB[j]) and not SB[i] <= SB[j] and not SB[j] <= SB[i]
    print("  pairs of target classes that overlap without nesting right after the scatter: %d of %d sampled pairs" % (S, T))
