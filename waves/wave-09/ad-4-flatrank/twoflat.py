#!/usr/bin/env python3
"""twoflat.py [ad-4-flatrank]  Machine check, at 4 bits, of the hand classification used in ad-4.md section 7b (case A):
if c1 f1 + c2 f2 (f1, f2 signed flats with different supports F1, F2, both coefficients non-zero) takes only the values 0 and 1,
then its support E is  a flat,  or F1 + F2 with F1, F2 disjoint,  or F1 minus F2 with F2 inside F1,  or F1 xor F2 with the
intersection equal to half of F1 or of F2.   Exhaustive over all pairs of the 1,072 signed flats; Fractions."""
from fractions import Fraction
K = 4; N = 16
def wt(x): return bin(x).count("1")
subs = {(0,)}; front = [(0,)]
while front:
    new = []
    for S in front:
        for v in range(1, N):
            if v not in S:
                T = tuple(sorted(set(S) | {s ^ v for s in S}))
                if T not in subs: subs.add(T); new.append(T)
    front = new
flatmasks = set()
sf = []
for S in subs:
    for a in range(N):
        pts = sorted(s ^ a for s in S)
        if pts[0] != a: continue
        m = sum(1 << p for p in pts); flatmasks.add(m); seen = set()
        for b in range(N):
            vec = tuple((-1) ** wt(b & (p ^ a)) if (m >> p) & 1 else 0 for p in range(N))
            if vec in seen: continue
            seen.add(vec); sf.append((m, vec))
print(len(flatmasks), "flats,", len(sf), "signed flats")
types = {}; bad = 0; total = 0
for i in range(len(sf)):
    F1, f1 = sf[i]
    for j in range(len(sf)):
        F2, f2 = sf[j]
        if F1 == F2 or i == j: continue
        if i > j and not (F1 & ~F2 == 0 or F2 & ~F1 == 0): continue      # unordered unless nested (the code below is symmetric otherwise)
        only1 = [z for z in range(N) if (F1 >> z) & 1 and not (F2 >> z) & 1]; only2 = [z for z in range(N) if (F2 >> z) & 1 and not (F1 >> z) & 1]
        cands = []
        if only1 and only2: cands = [(Fraction(1, f1[only1[0]]), Fraction(1, f2[only2[0]]))]
        elif only1:      # F2 inside F1
            c1 = Fraction(1, f1[only1[0]]); z = next(z for z in range(N) if (F2 >> z) & 1)
            cands = [(c1, (t - c1 * f1[z]) / f2[z]) for t in (0, 1)]
        elif only2:
            if i > j: pass
            c2 = Fraction(1, f2[only2[0]]); z = next(z for z in range(N) if (F1 >> z) & 1)
            cands = [((t - c2 * f2[z]) / f1[z], c2) for t in (0, 1)]
        for c1, c2 in cands:
            if c1 == 0 or c2 == 0: continue
            vals = [c1 * f1[z] + c2 * f2[z] for z in range(N)]
            if any(v not in (0, 1) for v in vals): continue
            E = sum(1 << z for z in range(N) if vals[z] == 1); I = F1 & F2; total += 1
            if E in flatmasks: t = "E is a flat"
            elif I == 0 and E == F1 | F2: t = "disjoint union"
            elif I == F2 and E == F1 & ~F2: t = "F1 minus F2, nested"
            elif I == F1 and E == F2 & ~F1: t = "F2 minus F1, nested"
            elif E == F1 ^ F2 and (2 * wt(I) == wt(F1) or 2 * wt(I) == wt(F2)): t = "xor, intersection half of one"
            else: t = "OTHER"; bad += 1
            types[t] = types.get(t, 0) + 1
print("combinations of two signed flats with values 0 and 1 only:", total, "; by type:", sorted(types.items()), "; outside the classification:", bad)
