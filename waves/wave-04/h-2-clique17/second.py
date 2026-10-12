#!/usr/bin/env python3
"""second.py m W z:n z:n ...  -- a second-order test for a count vector that survived counting, the clique lemma and the
zero-form lemma.   [h-2-clique17]   Exact integers.
If a form q0 with q0(I) = 0 selects the set A0 and A0 contains a pairwise joined set T with |A0| = 2 |T| (equality in the
zero-form lemma), then rank U_A0 = rank W_A0 = |T|: all the vectors u_i, i in A0, lie in the span of those of T.
Two such forms with the same |T| whose common part contains a joined set of that size have the SAME span, so their union is
a set of moves of rank |T|; and so on.  A joined set larger than |T| inside such a union is a contradiction.
Prints what it finds; 'no contradiction' proves nothing."""
import sys, itertools
import numpy as np
m, W = int(sys.argv[1]), int(sys.argv[2]); NP = (1 << m) - 1
V = list(range(1, NP + 1))
n = np.zeros(NP, dtype=np.int64)
for tok in sys.argv[3:]:
    z, c = tok.split(":"); n[int(z, 2) - 1] = int(c)
pairs = [(i, j) for i in range(m) for j in range(i, m)]; npr = len(pairs)
mon = np.array([[(z >> i & 1) & (z >> j & 1) for z in V] for (i, j) in pairs], dtype=np.int64)
diag = [t for t, (i, j) in enumerate(pairs) if i == j]
Qs = np.arange(1, 1 << npr); bits = (Qs[:, None] >> np.arange(npr)[None, :]) & 1
lam = bits[:, diag].sum(axis=1) % 2
A1 = np.unique((bits[lam == 1] @ mon) % 2, axis=0); A0 = np.unique((bits[lam == 0] @ mon) % 2, axis=0)
def wclique(adj, cand):
    best = 0
    def bk(wR, Pm):
        nonlocal best
        if wR > best: best = wR
        if wR + sum(int(n[j]) for j in range(NP) if Pm >> j & 1) <= best: return
        while Pm:
            v = Pm & -Pm; i = v.bit_length() - 1
            bk(wR + int(n[i]), Pm & adj[i]); Pm &= ~v
    bk(0, cand); return best
cnt = A1 @ n; assert cnt.min() >= W
tight = np.unique(A1[cnt == W] * (n > 0), axis=0)
adj = [0] * NP; intight = 0
for row in tight:
    msk = sum(1 << i for i in range(NP) if row[i]); intight |= msk
    for i in range(NP):
        if row[i]: adj[i] |= msk & ~(1 << i)
name = lambda msk: [format(V[i], "0%db" % m) for i in range(NP) if msk >> i & 1]
print("m = %d, W = %d, %d moves; tight selections %d; largest joined set %d" % (m, W, int(n.sum()), len(tight), wclique(adj, intight)))
c0 = A0 @ n; flats = {}
for r in range(len(A0)):
    if c0[r] == 0: continue
    sel = sum(1 << i for i in range(NP) if A0[r][i] and n[i] > 0)
    t = wclique(adj, sel & intight)
    if 2 * t > c0[r]: print("  zero-form lemma violated:", name(sel), int(c0[r]), t); sys.exit()
    if 2 * t == c0[r]: flats[sel] = t
print("  forms with q(I) = 0 at equality in the zero-form lemma: %d" % len(flats))
fl = [[msk, t] for msk, t in flats.items()]
changed = True; merges = 0
while changed:
    changed = False
    for i in range(len(fl)):
        for j in range(i + 1, len(fl)):
            if fl[i] is None or fl[j] is None or fl[i][1] != fl[j][1]: continue
            if fl[i][0] | fl[j][0] == fl[i][0]: fl[j] = None; continue
            if wclique(adj, fl[i][0] & fl[j][0] & intight) == fl[i][1]:
                fl[i][0] |= fl[j][0]; fl[j] = None; changed = True; merges += 1
    fl = [f for f in fl if f is not None]
print("  after merging sets with the same span: %d sets (%d merges)" % (len(fl), merges))
bad = 0
for msk, t in fl:
    c = wclique(adj, msk & intight)
    if c > t:
        bad += 1
        if bad <= 3: print("  CONTRADICTION: the moves along %s span only %d dimensions but contain a pairwise joined set of %d" % (name(msk), t, c))
print("  -> %s" % ("EXCLUDED at second order (%d contradictions)" % bad if bad else "no contradiction found at second order (proves nothing)"))
