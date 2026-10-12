#!/usr/bin/env python3
"""centres4.py (p-0-classtest): what the 7-gate circuits at 4 points are made of, for every tau over GF(p).
(1) PERSPECTIVE CENTRES: points h with all four coordinates non-zero such that EVERY row of K (x) K agrees with h, up to a factor,
    on three of the four coordinates (so row = factor * h + one input: one gate each).  The brick is 3 gates for h + 4 gates.
(2) the helper sets found by the exhaustive search (mincirc_sets), sorted by the sizes of the supports of the three helpers, and how
    many of them contain a perspective centre.
usage: centres4.py p"""
import sys, subprocess, os, itertools
here = os.path.dirname(os.path.abspath(__file__)); p = int(sys.argv[1])
def canon(v):
    f = next(x for x in v if x); iv = pow(f, -1, p); return tuple(x * iv % p for x in v)
pts = [(1, a, b, c) for a in range(1, p) for b in range(1, p) for c in range(1, p)]
for tau in range(2, p):
    rows = [tuple(pow(tau, bin(w & x).count('1'), p) for x in range(4)) for w in range(4)]
    centres = []
    for h in pts:
        sees = []
        for r in rows:
            best = None
            for drop in range(4):
                idx = [i for i in range(4) if i != drop]
                lam = r[idx[0]] * pow(h[idx[0]], -1, p) % p
                if all((r[i] - lam * h[i]) % p == 0 for i in idx): best = drop; break
            sees.append(best)
        if all(s is not None for s in sees): centres.append((h, tuple(sees)))
    inp = '\n'.join(' '.join(map(str, r)) for r in rows) + '\n'
    res = subprocess.run([os.path.join(here, 'mincirc_sets'), str(p), '4', '3', '100000000'], input=inp, capture_output=True, text=True).stdout
    sets = [[tuple(int(x) for x in s.split(',')) for s in line.split()[1:]] for line in res.splitlines() if line.startswith('SET')]
    cset = {h for h, _ in centres}
    hist = {}; withc = 0; nofull = 0
    for S in sets:
        key = tuple(sorted(sum(1 for x in h if x) for h in S)); hist[key] = hist.get(key, 0) + 1
        if any(canon(h) in cset for h in S): withc += 1
        if all(sum(1 for x in h if x) < 4 for h in S): nofull += 1
    print('p=%d tau=%d: perspective centres %d %s | helper sets %d, by support sizes %s | sets containing a centre %d | sets with NO full-support helper %d'
          % (p, tau, len(centres), [(''.join('%X' % x for x in h), ''.join(map(str, s))) for h, s in centres], len(sets), sorted(hist.items()), withc, nofull))
