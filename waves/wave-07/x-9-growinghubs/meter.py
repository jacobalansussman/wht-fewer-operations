#!/usr/bin/env python3
"""x-9-growinghubs/meter.py: lemma P as a meter on circuits that exist.  Exact fractions.
For every wire M of a circuit (inputs excluded) and every row O of H: the least support of a witness O - a*M over all a != 0.
Per circuit: for s = 1, 2, 4, ... the largest number of rows any ONE wire reaches with witnesses of at most s points,
against the cap 1/(1 - 2s/N)^2 of x-9.md (valid for s < N/2).  usage: meter.py file ..."""
import sys, re
from fractions import Fraction as F
term = re.compile(r'([+-])?\s*(-?\d+(?:/\d+)?)?\s*\*?\s*([A-Za-z]+\d+)')
for fn in sys.argv[1:]:
    val = {}; order = []
    lines = [l.split('#')[0].strip() for l in open(fn)]
    lines = [l for l in lines if '=' in l]
    names = set()
    for l in lines:
        for m in term.finditer(l.split('=', 1)[1]): names.add(m.group(3))
    N = 1 + max(int(n[1:]) for n in names if n[0] == 'x' and n[1:].isdigit())
    for i in range(N): val['x%d' % i] = [F(int(i == j)) for j in range(N)]
    for l in lines:
        nm, rhs = [t.strip() for t in l.split('=', 1)]
        v = [F(0)] * N
        for m in term.finditer(rhs):
            c = F(m.group(2)) if m.group(2) else F(1)
            if m.group(1) == '-': c = -c
            v = [a + c * b for a, b in zip(v, val[m.group(3)])]
        val[nm] = v; order.append(nm)
    rows = [tuple(-1 if bin(w & x).count('1') & 1 else 1 for x in range(N)) for w in range(N)]
    held = {tuple(val[n]) for n in order}
    assert all(tuple(F(t) for t in r) in held for r in rows), 'not all rows of H are held'
    ss = [s for s in (1, 2, 4, 8, 16, 32) if s < N // 2] + [N // 2 - 1] if N > 4 else [1]
    ss = sorted(set(ss))
    best = {s: (0, None) for s in ss}; nsign = 0; nweighted = 0
    for n in order:
        M = val[n]
        if tuple(M) in {tuple(F(t) for t in r) for r in rows}: continue      # outputs themselves are not counted as hubs
        mags = {abs(x) for x in M if x}
        if len(mags) == 1: nsign += 1
        else: nweighted += 1
        mins = []
        for O in rows:
            cand = {F(O[x]) / M[x] for x in range(N) if M[x]}
            mins.append(min(sum(1 for x in range(N) if a * M[x] != O[x]) for a in cand))
        for s in ss:
            c = sum(1 for m in mins if m <= s)
            if c > best[s][0]: best[s] = (c, n)
    print('%s: %d points, %d gates, helpers: %d sign vectors, %d with several magnitudes' % (fn.split('/')[-1], N, len(order), nsign, nweighted))
    for s in ss:
        cap = 1 / (1 - 2 * s / N) ** 2
        print('   witnesses of at most %2d points: one wire reaches at most %2d rows (wire %s); cap %.2f' % (s, best[s][0], best[s][1], min(cap, N)))
