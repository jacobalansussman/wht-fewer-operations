# ab-4-zcut/zcross.py : check of the crossing-wire inequality on every optimal 12-gate circuit for Z at 8 points. Count (G). Exact.
# For a circuit, a cut by one address bit (L = bit off, R = bit on):
#   GL = gates whose wire is non-zero on L, GR = same on R, X = gates non-zero on BOTH (crossing wires), Xh = crossing non-outputs
#   n(L), n(R) = distinct non-trivial classes on L, on R (x-2's counts)
# Claims [derived in ab-4.md section 3]:  GL - n(L) >= N/2 (pairs),  GR - n(R) >= N/2 (deviation lemma),
#   hence gates + X = GL + GR >= n(L) + n(R) + N, i.e.  gates >= n(L) + n(R) + N - X  and  E - B >= N - X.
# Also the rank form of the deviation lemma: the deviations of the R-repeats span the whole L-space (rank N/2), in the order
# in which the circuit is replayed here.
import sys, re
from fractions import Fraction as F
exec(open('zmeter.py').read().split('def projections')[0])
def lift(d, p): return tuple((x if x <= p // 2 else x - p) for x in d)
def rank(rows):
    rows = [[F(x) for x in r] for r in rows]; r = 0
    for c in range(len(rows[0]) if rows else 0):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c] / rows[r][c]; rows[i] = [x - f * y for x, y in zip(rows[i], rows[r])]
        r += 1
    return r
p = int(sys.argv[1]); tab = {}; tot = 0; worst = 99
for line in open(sys.argv[2]):
    if 'example' not in line: continue
    hs = [lift([int(ch) for ch in h], p) for h in re.findall(r'\[(\d+)\]', line)]
    wires = list(hs) + list(targets); need = pairs_for(wires)
    order = []; made = 0; ch = True
    while ch:
        ch = False
        for g in range(12):
            if not made >> g & 1 and any(m & made == m for m in need[g]): made |= 1 << g; order.append(g); ch = True
    if made != 4095: continue
    tot += 1
    for c in range(3):
        L = [x for x in range(N) if not x >> c & 1]; R = [x | 1 << c for x in L]
        a = [[w[i] for i in L] for w in wires]; b = [[w[j] for j in R] for w in wires]
        GL = sum(1 for v in a if any(v)); GR = sum(1 for v in b if any(v)); X = sum(1 for u, v in zip(a, b) if any(u) and any(v))
        Xh = sum(1 for g in range(5) if any(a[g]) and any(b[g]))
        nL = len({prim(v) for v in a if any(v) and sum(1 for t in v if t) > 1}); nR = len({prim(v) for v in b if any(v) and sum(1 for t in v if t) > 1})
        assert GL - nL >= 4 and GR - nR >= 4 and 12 + X >= nL + nR + 8
        # rank form: first wire of each R-class (inputs first), deviations of the repeats
        first = {}
        for j in range(4): first[tuple(int(i == j) for i in range(4))] = ([0] * 4, tuple(int(i == j) for i in range(4)))
        devs = []
        for g in order:
            if not any(b[g]): continue
            cl = prim(b[g])
            if cl not in first: first[cl] = (a[g], b[g]); continue
            fa, fb = first[cl]; i = next(t for t in range(4) if fb[t]); lam = F(b[g][i], fb[i])
            devs.append([F(a[g][t]) - lam * fa[t] for t in range(4)])
        rk = rank(devs) if devs else 0; assert rk == 4, (hs, c, rk)
        key = (nL, nR, 12 - nL - nR, X, Xh, GR - nR, GL - nL); tab[key] = tab.get(key, 0) + 1
        worst = min(worst, 12 + X - nL - nR - 8)
print('p=%d: %d circuits, 3 cuts each; all assertions passed (GL - n(L) >= 4, GR - n(R) >= 4, gates + X >= n(L) + n(R) + N, deviations of rank 4)' % (p, tot))
print('least slack of  gates + X - n(L) - n(R) - N  =', worst)
print('(n(L), n(R), E - B, X crossing gates, Xh crossing helpers, R-repeats, L-repeats) : count')
for k in sorted(tab): print('   n(L)=%d n(R)=%d E-B=%d X=%d Xh=%d Rrep=%d Lrep=%d : %d' % (*k, tab[k]))
