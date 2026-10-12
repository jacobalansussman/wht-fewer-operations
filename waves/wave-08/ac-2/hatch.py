#!/usr/bin/env python3
"""ac-2/hatch.py  (a) hatch H1 by fraction: a total is one block of rank f*h or of rank r; number of totals at the order bound.
(b) pair rule: tight characters of 'every direction once' at m = 4, 5 counted exactly over ALL quadratic forms."""
import itertools, sys
sys.argv = sys.argv[:1]
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import price2
from price2 import shape, K, Kf
print('== (a) best what-if saving over ALL classes with h <= 9 (every r from 1 to h-1), totals 1/K per pair per stage, each ONE block of rank f*h')
for s, idle in ((3, 'B1'), (3, 'C0'), (5, 'B1'), (5, 'A5')):
    row = []
    for f in (1.0, 0.9, 0.76, 0.6, 0.51, 0.45, 0.4, 0.35, 0.3):
        b = max((shape(h, r, s, idle, 1 / float(K(h, r)), f * h), h, r) for h in range(2, 10) for r in range(1, h))
        row.append('f=%.2f: %.4f (%d,%d)' % ((f,) + b))
    print('   %d-stage %s : ' % (s, idle) + ' ; '.join(row))
print('   the same restricted to r <= h/2:')
for s, idle in ((3, 'B1'), (3, 'C0'), (5, 'B1'), (5, 'A5')):
    row = []
    for f in (1.0, 0.76, 0.51, 0.4, 0.3, 0.2, 0.1):
        b = max((shape(h, r, s, idle, 1 / float(K(h, r)), max(1, f * h)), h, r) for h in range(2, 10) for r in range(1, h // 2 + 1))
        row.append('f=%.2f: %.4f (%d,%d)' % ((f,) + b))
    print('   %d-stage %s : ' % (s, idle) + ' ; '.join(row))
print('== (a2) a total is one block of rank r (it does only the moves the source skipped): best over h <= 9, and first width reaching 1e-1')
for s, idle in ((3, 'B1'), (3, 'C0'), (5, 'B1'), (5, 'A5')):
    b = max((shape(h, r, s, idle, 1 / float(K(h, r)), r), h, r) for h in range(2, 10) for r in range(1, h))
    hit = None
    for h in range(2, 400):
        bb = max((shape(h, r, s, idle, 1 / Kf(h, r), r), r) for r in range(1, h))
        if bb[0] >= 0.1: hit = (h, bb[1], bb[0]); break
    print('   %d-stage %s : best for h <= 9: %.4f at (%d,%d) ; first width with 1e-1: %s' % ((s, idle) + b + (('h = %d, r = %d (%.4f)' % hit) if hit else 'none below 400',)))
print('== (b) pair rule: quadratic forms Q on m bits (Q(0) = 0); active directions = non-zero z with Q(z) = 1; <Q,I> = Q(e_1)+...+Q(e_m) mod 2')
for m in (3, 4, 5):
    N = 1 << m; W = 1 << (m - 2); lin = list(range(m)); quad = list(itertools.combinations(range(m), 2))
    tight = []; minact = None; hist = {}
    for a in range(1 << m):
        for b in range(1 << len(quad)):
            def Q(z):
                v = bin(a & z).count('1')
                for k, (i, j) in enumerate(quad):
                    if (b >> k) & 1 and (z >> i) & 1 and (z >> j) & 1: v += 1
                return v & 1
            act = [z for z in range(1, N) if Q(z)]
            odd = sum(Q(1 << i) for i in range(m)) & 1
            if odd:
                hist[len(act)] = hist.get(len(act), 0) + 1
                if len(act) == W: tight.append(frozenset(act))
    pairs = set()
    for A in tight:
        for p in itertools.combinations(sorted(A), 2): pairs.add(p)
    print('   m = %d: forms with <Q,I> = 1 by number of active directions: %s ; W = 2^(m-2) = %d ; tight characters: %d ; pairs of directions lying together in a tight character: %d of %d' % (m, sorted(hist.items()), W, len(tight), len(pairs), (N - 1) * (N - 2) // 2))
