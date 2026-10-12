#!/usr/bin/env python3
"""h-0 onepergate / census_out.py : which wires are one gate from SEVERAL OUTPUTS with tight partners?  ANY coefficients.  Exact.
A wire w is 'one gate from output y with a tight partner p' exactly when w lies on the line through y and p.
Here: every non-tight point w that lies on a line (output, tight wire) and on at least one other line through two tight wires.
For each such w: the outputs it is one gate from, with the level of each partner (level d = a character on a coset of size 2^d,
so level 0 = an input, free; level k-1 = half of an output, as dear as the textbook's last step).
usage: census_out.py k
"""
import sys, itertools, pickle, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/g1')
from ref import tight_wires, wht, nz, norm
k = int(sys.argv[1]); N = 1 << k
tw = tight_wires(k); ws = sorted(tw); n = len(ws); lev = [tw[w] for w in ws]
U = np.array(ws, dtype=np.int64); Gm = U @ U.T
outs = [i for i in range(n) if lev[i] == k]
def normrows(P):
    g = np.gcd.reduce(np.abs(P), axis=1); g[g == 0] = 1; P = P // g[:, None]
    first = np.argmax(P != 0, axis=1); sgn = np.sign(P[np.arange(len(P)), first]); sgn[sgn == 0] = 1
    return P * sgn[:, None]
pts = {}    # point -> set of (output index, partner members tuple)
nbase = 0
for i in outs:
    done = set()
    for j in range(n):
        if j == i or j in done: continue
        a, b, c = int(Gm[i, i]), int(Gm[i, j]), int(Gm[j, j]); det = a * c - b * b
        xi = U @ U[i]; xj = U @ U[j]
        P = det * U - np.outer(c * xi - b * xj, U[i]) - np.outer(a * xj - b * xi, U[j])
        Pn = normrows(P); zero = ~np.any(Pn != 0, axis=1)
        members = tuple(np.nonzero(zero)[0].tolist())
        for m in members: done.add(m)
        nbase += 1
        order = np.lexsort(Pn.T[::-1]); srt = Pn[order]; same = np.all(srt[1:] == srt[:-1], axis=1); start = 0
        for t in range(1, n + 1):
            if t == n or not same[t - 1]:
                if t - start >= 2 and not zero[order[start]]:
                    grp = order[start:t].tolist()
                    for p, q in itertools.combinations(grp, 2):
                        cidx = int(np.nonzero(P[q])[0][0]); num = int(P[p][cidx]); den = int(P[q][cidx])
                        w = norm([den * x - num * y for x, y in zip(ws[p], ws[q])])
                        if w is None or w in tw: continue
                        pts.setdefault(w, set()).add((i, members))
                start = t
print('N = %d: %d tight wires, %d outputs, %d lines through an output and another tight wire' % (N, n, len(outs), nbase), flush=True)
print('non-tight points on such a line and on a second tight line: %d' % len(pts))
hist = {}; ex = {}
for w, L in pts.items():
    s = nz(w); s2 = nz(wht(w)); mags = tuple(sorted({abs(x) for x in w if x}))
    # per output: the cheapest partner level on the line (the line holds the output and tight wires of lower level)
    per = {}
    for (i, members) in L:
        pl = min(lev[t] for t in members if t != i); per[i] = min(per.get(i, 99), pl)
    prof = tuple(sorted(per.values()))
    key = (len(per), prof, s, s2, mags)
    hist[key] = hist.get(key, 0) + 1; ex.setdefault(key, w)
print('classes (outputs one gate away, levels of their partners, s, s\', |entries|): count, example')
for key in sorted(hist, key=lambda z: (-z[0], z)): print('  ', key, ':', hist[key], list(ex[key]))
best = max(hist, key=lambda z: z[0])
print('most outputs served by one non-tight wire with tight partners: %d' % best[0])
# the cheapest way to serve m outputs: total partner support
print('least total partner support by number of outputs served:')
bym = {}
for key in hist:
    m = key[0]; tot = sum(2 ** d for d in key[1]); bym[m] = min(bym.get(m, 10 ** 9), tot)
for m in sorted(bym): print('   %d outputs: partners of total support %d  (N/4 per pair of outputs would be %d)' % (m, bym[m], N // 4 * m // 2))
