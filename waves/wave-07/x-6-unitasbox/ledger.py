#!/usr/bin/env python3
"""ledger.py [x-6-unitasbox, 2026-10-11]  The volume ledger (s-cross hybrid 3, Morgenstern's count) on ONE invocation of a
published certificate, read only.  Exact: whole numbers and fractions; the only floats are the final logarithms.
Reading: helpers start empty (the certificate checker's reading), CONTENT coordinates (h-7's dictionary, as u-5 used it):
  a wire = (content vector over the 2v data registers) x (row a of the frame of its label).
Every gate is written between primitive forms as  w = (A u + B v) / g ; budget of the gate = log2((|A|+|B|)/|g|).
  move up   (one direction, 2^h gates): the two parents sit on disjoint cosets with the same content -> (1,1)/1, budget 1.
  move down (2^h gates): the two parents sit on the same coset, the result on half of it; over the Gaussian integers the
            common factor is 1+i, of size sqrt 2 -> budget 1/2.          [derived from the dictionary, not replayed on wires]
  addition  t += c*s at a common label (2^h gates, all alike): A, B, g come from the CONTENT vectors alone -> computed here.
usage: python3 -I -B ledger.py <certificate.json.gz>"""
import sys, json, gzip, math
from fractions import Fraction as Fr
from math import gcd
from functools import reduce
from collections import Counter
c = json.load(gzip.open(sys.argv[1])); h, v, R = c["h"], c["v"], c["R"]; nreg = 2 * v + R
reg = [({r: Fr(1)} if r < 2 * v else {}) for r in range(nreg)]
def prim(w):
    """w = s * p, p whole numbers without common factor, s > 0"""
    den = reduce(lambda a, b: a * b // gcd(a, b), (q.denominator for q in w.values()), 1)
    g = reduce(gcd, (abs(int(q * den)) for q in w.values()), 0)
    return Fr(g, den)
kinds = Counter(); bud = Counter(); ngate = Counter(); big = 1; bigwhere = None; qn = Counter(); zero = 0; copies = 0
maxent = 1
def axpy(t, src, co, ph):
    global big, bigwhere, zero, copies, maxent
    d = reg[t]
    if not d:
        for k, u in src.items(): d[k] = co * u
        copies += 1; return
    st = prim(d); ss = prim(src)
    for k, u in src.items():
        w = d.get(k, 0) + co * u
        if w: d[k] = w
        else: d.pop(k, None)
    if not d: zero += 1; return
    sn = prim(d)
    al, be = st / sn, co * ss / sn
    den = al.denominator * be.denominator // gcd(al.denominator, be.denominator)
    A, B = abs(int(al * den)), abs(int(be * den)); assert gcd(A, B) == 1 or gcd(gcd(A, B), den) == 1
    gg = gcd(A, B); assert gg == 1, (A, B, den)
    b = math.log2(Fr(A + B, den)); bud[ph] += b; ngate[ph] += 1
    kinds[(ph, "(%d,%d)/%d" % (min(A, B), max(A, B), den))] += 1
    if den > 1: qn[ph] += 1
    if max(A, B) > big: big = max(A, B); bigwhere = (ph, t, A, B, den)
    maxent = max(maxent, max(abs(int(q / sn)) for q in d.values()))
def run(G, ph):
    for g in G:
        if g[0] == "neg": reg[g[2]] = {k: -u for k, u in reg[g[2]].items()}
        elif g[0] == "out":
            src = dict(reg[g[2]])
            for t, a, b in g[3]: axpy(t, src, Fr(a, b), ph)
        else:
            for s, a, b in g[3]: axpy(g[2], dict(reg[s]), Fr(a, b), ph)
run(c["A"], "A")
tot = {k: dict(reg[s]) for k, s, f in c["ret"]}
def scat_row(t):
    sc = c["scat"]
    if "table" in sc: return [(k, Fr(a, b)) for k, a, b in sc["table"][t]]
    sin, sout = Fr(*sc["inside"]), Fr(*sc["outside"])
    return [(k, sin if c["ports"][t] >> k & 1 else sout) for k in range(h)]
for t in range(v):
    for k, co in scat_row(t):
        if co and k in tot: axpy(v + t, tot[k], co, "scatter")
run(c["B"], "B")
ok = all(reg[t] == {t: 1} for t in range(v)) and all(reg[v + t] == {t: 1, v + t: 1} for t in range(v))
NA = 1 << h
up_inv = c["N"] - c["cst"]; up = up_inv + v; down = c["cst"]
nadd = sum(ngate.values()); badd = sum(bud.values())
print("certificate h=%d v=%d R=%d cst=%d moves=%d ; replay ends with x_t alone and y_t + x_t: %s" % (h, v, R, c["cst"], c["N"], ok))
print("additions that are gates: %d (free copies into an empty register: %d; results that are zero: %d)" % (nadd, copies, zero))
for ph in ("A", "scatter", "B"):
    print("  phase %-7s additions %5d  budget %9.2f  per addition %.3f  with g > 1 (quotient): %d" % (ph, ngate[ph], bud[ph], bud[ph] / max(1, ngate[ph]), qn[ph]))
print("  kinds (A,B)/g of the additions, all phases:")
allk = Counter()
for (ph, kd), q in kinds.items(): allk[kd] += q
for kd, q in allk.most_common(40): print("     %-14s %5d   budget each %.3f" % (kd, q, math.log2(Fr(*[sum(map(int, kd[1:kd.index(')')].split(',')))], int(kd.split('/')[1])))))
print("  largest coefficient in any addition: %d at %s ; largest entry of any primitive content vector: %d" % (big, bigwhere, maxent))
print("moves: up %d (of which %d the prologue of the sources' port moves), down %d" % (up, v, down))
G_inv = (up + down + nadd) * NA; B_inv = (up * 1.0 + down * 0.5 + badd) * NA
need = v * (h * NA // 2) + v * ((h - 1) * NA // 2)
print("ONE INVOCATION as one gate list (G), %d points: gates %d ; budget %.0f ; per gate %.4f" % (2 * v * NA, G_inv, B_inv, B_inv / G_inv))
print("   quotient gates (g of size > 1): %d = (%d moves down + %d additions) x 2^%d ; they bring %0.f of the budget" % ((down + sum(qn.values())) * NA, down, sum(qn.values()), h, down * 0.5 * NA + 0))
print("   needed for the 2v data outputs (log2 of the determinant of their primitive forms): %d ; budget / needed = %.2f" % (need, B_inv / need))
print("   the same with the helpers' own moves left out (data registers and copies only): gates %d budget %.0f per gate %.4f"
      % ((up - R * h + down + nadd) * NA, ((up - R * h) + 0.5 * down + badd) * NA, ((up - R * h) + 0.5 * down + badd) / (up - R * h + down + nadd)))
# plain schedule for the same job: each source makes its port move (prologue), a copy of it comes down one direction (one move down),
# is added to the target (one addition (1,1)/1), then both arrays make their moves; helpers make their h moves as before.
pg = (v + v + v + v * (h - 1) * 2 + R * h) * NA; pb = (v + 0.5 * v + v + v * (h - 1) * 2 + R * h) * NA
print("PLAIN schedule for the same job (one copy move down and one addition per pair): gates %d ; budget %.0f ; per gate %.4f ; budget / needed = %.2f" % (pg, pb, pb / pg, pb / need))
print("   without the helpers' moves: gates %d budget %.0f per gate %.4f" % (pg - R * h * NA, pb - R * h * NA, (pb - R * h * NA) / (pg - R * h * NA)))
