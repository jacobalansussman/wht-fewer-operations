#!/usr/bin/env python3
# h-5 / gatetypes.py : check two hand statements on EVERY gate of the pool (pool_q.txt: pair class, entries 0,+-1; pool_gf3.txt read as integer vectors is skipped).
#  (1) every gate is of type I (along one bit), II (along one pair, common factor on the third bit) or III (triangle: the three wires are entangled on the three different pairs);
#  (2) births(result; parents) <= max(1, number of entangled bits of the wider parent), for each of the three roles of each collinear triple.
import sys
N = 8
L = open(sys.argv[1]).read().split('\n'); n, ntr = map(int, L[0].split())
ws = [tuple(map(int, L[1 + i].split())) for i in range(n)]
tr = [tuple(map(int, l.split())) for l in L[3 + n:] if l.strip()]
def halves(w, i): return [w[x] for x in range(N) if not (x >> i) & 1], [w[x] for x in range(N) if (x >> i) & 1]
def prop(a, b): return all(a[i] * b[j] == a[j] * b[i] for i in range(len(a)) for j in range(i + 1, len(a)))
def B(w): return tuple(i for i in range(3) if not prop(*halves(w, i)))
def factor(w, i):
    lo, hi = halves(w, i); k = next(j for j in range(4) if lo[j] or hi[j]); return (lo[k], hi[k])
def restv(w, i):
    lo, hi = halves(w, i); return lo if any(lo) else hi
def inK(w, i, t): return all(w[x | (1 << i)] == t * w[x] for x in range(N) if not (x >> i) & 1)
cnt = {'I': 0, 'II': 0, 'III': 0, 'none': 0}; viol = 0; hist = {}
for a, b, c in tr:
    T = [ws[a], ws[b], ws[c]]; Bs = [B(w) for w in T]; ty = None
    for l in range(3):
        if all(l not in bb for bb in Bs) and prop(restv(T[0], l), restv(T[1], l)) and prop(restv(T[0], l), restv(T[2], l)): ty = 'I'
    if ty is None:
        for m in range(3):
            if all(m not in bb for bb in Bs) and prop(factor(T[0], m), factor(T[1], m)) and prop(factor(T[0], m), factor(T[2], m)): ty = 'II'
    if ty is None and sorted(Bs) == [(0, 1), (0, 2), (1, 2)]: ty = 'III'
    cnt[ty or 'none'] += 1
    for r in range(3):
        w, u, v = T[r], T[(r + 1) % 3], T[(r + 2) % 3]
        births = sum(1 for i in range(3) for t in (1, -1) if inK(w, i, t) and not inK(u, i, t) and not inK(v, i, t))
        wid = max(1, len(B(u)), len(B(v))); hist[(births, wid)] = hist.get((births, wid), 0) + 1
        if births > wid: viol += 1
print(sys.argv[1], 'gates (collinear triples):', len(tr), 'by type:', cnt)
print('births against width of the wider parent, (births, width): count ->', sorted(hist.items()), '; violations of births <= width:', viol)
