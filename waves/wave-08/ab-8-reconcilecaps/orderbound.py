#!/usr/bin/env python3
"""orderbound.py [ab-8-reconcilecaps]  EXACT check of the order bound on the WIDE class of labels (P, L), any complement L,
and on x-6's ports (L = P-perp).  For a random order of the non-zero words, I = {labels whose smallest word of P u L lies in P}.
Checked: (1) inside I, 't knows s' (P_s inside L_t) implies first(P_t) < first(P_s) strictly, so any matrix with unit diagonal
that vanishes off the knows relation is triangular on I;  (2) the mean of |I| is  v (2^r - 1) / (2^r + 2^(h-r) - 2);
(3) for a random rational matrix M with that support, rank(M) >= |I| (exact fractions, small families)."""
import sys, itertools, random
from fractions import Fraction as Fr
h, r, wide = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3] == 'wide'
N = 1 << h; PC = [bin(x).count('1') & 1 for x in range(N)]
def span(B):
    S = [0]
    for b in B: S += [s ^ b for s in S]
    return frozenset(S)
def subs(d):
    out = set()
    for B in itertools.combinations(range(1, N), d):
        S = span(B)
        if len(S) == 1 << d: out.add(S)
    return sorted(out, key=sorted)
Ps = subs(r); Ls = subs(h - r)
perp = lambda P: frozenset(a for a in range(N) if all(PC[a & p] == 0 for p in P))
labels = [(P, L) for P in Ps for L in Ls if len(P & L) == 1 and (wide or L == perp(P))]
v = len(labels); print('class (%d,%d) %s: %d labels' % (h, r, 'WIDE (any complement)' if wide else "x-6 ports (L = P-perp)", v))
knows = lambda t, s: labels[s][0] <= labels[t][1]            # t knows s
rnd = random.Random(7); tot = 0; trials = 200; ok = True
for _ in range(trials):
    perm = list(range(1, N)); rnd.shuffle(perm); rk = {x: i for i, x in enumerate(perm)}
    first = lambda U: min(rk[x] for x in U if x)
    I = [t for t in range(v) if first(labels[t][0]) < first(labels[t][1])]
    tot += len(I)
    if _ < 5:
        fp = {t: first(labels[t][0]) for t in I}
        samp = I if len(I) <= 300 else rnd.sample(I, 300)
        for t in samp:
            for s in samp:
                if s != t and knows(t, s) and not fp[t] < fp[s]: ok = False
print('   triangular on I in 5 random orders: %s ; mean |I| over %d orders = %.2f ; predicted v (2^r-1)/(2^r+2^(h-r)-2) = %.2f ; kappa <= %.4f'
      % (ok, trials, tot / trials, v * (2 ** r - 1) / (2 ** r + 2 ** (h - r) - 2), (2 ** r + 2 ** (h - r) - 2) / (2 ** r - 1)))
# (3) exact rank of a random matrix with the allowed support on a random sub-family of 40 labels
def rank(M):
    M = [row[:] for row in M]; rk = 0
    for c in range(len(M[0])):
        pv = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if pv is None: continue
        M[rk], M[pv] = M[pv], M[rk]
        for i in range(rk + 1, len(M)):
            if M[i][c] != 0:
                f = M[i][c] / M[rk][c]; M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
for trial in range(3):
    fam = rnd.sample(range(v), min(v, 40))
    M = [[Fr(1) if t == s else (Fr(rnd.randint(-3, 3)) if knows(t, s) else Fr(0)) for s in fam] for t in fam]
    perm = list(range(1, N)); rnd.shuffle(perm); rk = {x: i for i, x in enumerate(perm)}
    first = lambda U: min(rk[x] for x in U if x)
    I = [t for t in fam if first(labels[t][0]) < first(labels[t][1])]
    print('   random sub-family of %d, random rational matrix with the allowed support: rank %d >= |I| = %d : %s' % (len(fam), rank(M), len(I), rank(M) >= len(I)))
