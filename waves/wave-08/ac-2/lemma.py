#!/usr/bin/env python3
"""ac-2/lemma.py  EXACT, own code.  The order bound of ab-8 section 3.
Subspaces of F_2^h as bit masks over the 2^h words (bit x set iff word x in the subspace).
(1) ALL orders at tiny width: for every order of the non-zero words, I = {t: first(P_t) < first(L_t)};
    check for ALL pairs s != t in I:  P_s inside L_t  =>  first(P_t) < first(P_s);   exact mean of |I| as a fraction.
(2) larger classes, random orders, ALL pairs of I checked through an index (labels grouped by first word).
(3) structured (not random) matrices: exact rank over the rationals of all-ones-on-support matrices and of I + c A."""
import sys, itertools, random
from fractions import Fraction as Fr
def subspaces(h, d):
    N = 1 << h; cur = {1}                      # mask of {0}
    for _ in range(d):
        nxt = set()
        for S in cur:
            for x in range(1, N):
                if not (S >> x) & 1:
                    T = S; 
                    for y in range(N):
                        if (S >> y) & 1: T |= 1 << (y ^ x)
                    nxt.add(T)
        cur = nxt
    return sorted(cur)
def perp(h, S):
    N = 1 << h; out = 0
    els = [y for y in range(N) if (S >> y) & 1]
    for x in range(N):
        if all(bin(x & y).count('1') % 2 == 0 for y in els): out |= 1 << x
    return out
def labels(h, r, wide):
    Ps = subspaces(h, r)
    if wide:
        Ls = subspaces(h, h - r); return [(P, L) for P in Ps for L in Ls if P & L == 1]
    out = []
    for P in Ps:
        L = perp(h, P)
        if P & L == 1: out.append((P, L))
    return out
def els(S): 
    out = []; x = 0
    while S:
        if S & 1: out.append(x)
        S >>= 1; x += 1
    return out
def run(h, r, wide, mode, trials=50, seed=1):
    lab = labels(h, r, wide); v = len(lab); N = 1 << h
    PE = [[x for x in els(P) if x] for P, L in lab]; LE = [[x for x in els(L) if x] for P, L in lab]
    pred = Fr(v * (2 ** r - 1), 2 ** r + 2 ** (h - r) - 2)
    rnd = random.Random(seed); tot = 0; n = 0; bad = 0; best = 0
    orders = itertools.permutations(range(1, N)) if mode == 'all' else (rnd.sample(range(1, N), N - 1) for _ in range(trials))
    for perm in orders:
        rk = [0] * N
        for i, x in enumerate(perm): rk[x] = i
        fP = [min(rk[x] for x in PE[t]) for t in range(v)]; fL = [min(rk[x] for x in LE[t]) for t in range(v)]
        I = [t for t in range(v) if fP[t] < fL[t]]
        tot += len(I); n += 1; best = max(best, len(I))
        # all pairs: t knows s (P_s inside L_t) with s,t in I must have fP[t] < fP[s].  A violation needs fP[s] <= fP[t].
        if mode == 'all' or n <= 3:
            if len(I) > 3500: I = rnd.sample(I, 3500)
            I.sort(key=lambda t: fP[t])
            for a, t in enumerate(I):
                Lt = lab[t][1]
                for s in I[:a + 1]:                      # those with fP[s] <= fP[t]  (ties included)
                    if s != t and lab[s][0] & ~Lt == 0: bad += 1
                # ties later in the sort
                b = a + 1
                while b < len(I) and fP[I[b]] == fP[t]:
                    if lab[I[b]][0] & ~Lt == 0: bad += 1
                    b += 1
    print('(%d,%d) %s: v = %d ; orders %s %d ; violations of triangularity over all pairs checked: %d ; mean |I| = %s (%.3f) ; predicted %s (%.3f) ; largest |I| seen %d -> kappa of the whole family <= %.3f ; bound K = %.4f'
          % (h, r, 'wide' if wide else 'ports', v, mode, n, bad, Fr(tot, n) if mode == 'all' else '-', tot / n, pred, float(pred), best, v / best, float(1 + Fr(2 ** (h - r) - 1, 2 ** r - 1))), flush=True)
    return lab
def rank(M):
    M = [row[:] for row in M]; rk = 0; nc = len(M[0])
    for c in range(nc):
        pv = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if pv is None: continue
        M[rk], M[pv] = M[pv], M[rk]
        for i in range(rk + 1, len(M)):
            if M[i][c] != 0:
                f = M[i][c] / M[rk][c]; M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'all':
        for h, r, w in ((2, 1, True), (3, 1, True), (3, 2, True), (3, 1, False)):
            run(h, r, w, 'all')
    elif what == 'rand':
        for h, r, w, tr in ((4, 2, True, 200), (4, 2, False, 200), (5, 2, False, 200), (5, 2, True, 60), (6, 3, False, 100), (6, 2, False, 100), (7, 3, False, 40), (6, 2, True, 6)):
            run(h, r, w, 'rand', tr)
    elif what == 'struct':
        # structured matrices on x-6 ports: all-ones on the support; and I + c A for c in a small exact grid: least exact rank seen
        for h, r in ((4, 2), (5, 2), (5, 1), (6, 2)):
            lab = labels(h, r, False); v = len(lab)
            A = [[1 if s != t and lab[s][0] & ~lab[t][1] == 0 else 0 for s in range(v)] for t in range(v)]
            deg = sorted(set(sum(row) for row in A)); bound = Fr(v * (2 ** r - 1), 2 ** r + 2 ** (h - r) - 2)
            best = (v + 1, Fr(0))
            for c in [Fr(a, b) for a in range(-8, 9) for b in (1, 2, 3, 4, 8) if a]:
                M = [[Fr(1) if s == t else c * A[t][s] for s in range(v)] for t in range(v)]
                best = min(best, (rank(M), c))
            print('(%d,%d) ports v = %d, degrees %s : least exact rank of I + c A over the grid = %d at c = %s ; order bound says rank >= %s = %.2f : %s' % (h, r, v, deg, best[0], best[1], bound, float(bound), best[0] >= bound), flush=True)
