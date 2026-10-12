#!/usr/bin/env python3
"""agree.py (p-0-classtest): on how many of the N points do two rows of the kernel power agree up to a factor?
Row w of the k-th power of [[1,1],[1,tau]] is tau^(number of common 1-bits of w and x).  Two rows w, w' have ratio tau^e(x),
e(x) = (ones of x inside w minus w') - (ones of x inside w' minus w), a whole number between -b and a (a, b = sizes of w \\ w', w' \\ w).
Generic tau: they agree up to a factor exactly on a level set of e.  tau a primitive n-th root of unity: on a level set of e modulo n.
The transform is n = 2.  Exact counting, no arithmetic with tau at all.  Prints the largest agreeing fraction for each (a, b)."""
from itertools import product
from fractions import Fraction as F
from math import comb
def best(a, b, n):
    cnt = {}
    for i in range(a + 1):
        for j in range(b + 1):
            e = i - j
            if n: e %= n
            cnt[e] = cnt.get(e, 0) + comb(a, i) * comb(b, j)
    return F(max(cnt.values()), 2 ** (a + b))
print('largest fraction of the points on which two rows agree up to a factor; d = a + b = number of address bits in which the rows differ')
print('%-10s %-10s %-12s %-12s %-12s %-12s' % ('(a,b)', 'generic', 'n=2 (H)', 'n=3', 'n=4 (tau=i)', 'n=6'))
for d in range(1, 9):
    for a in range((d + 1) // 2, d + 1):
        b = d - a
        print('%-10s %-10s %-12s %-12s %-12s %-12s' % ((a, b), best(a, b, 0), best(a, b, 2), best(a, b, 3), best(a, b, 4), best(a, b, 6)))
print()
print('pairs of rows by agreement at N = 8 and 16 (generic tau against the transform):')
for k in (3, 4, 5, 6):
    N = 1 << k; tot = {}; 
    for w in range(N):
        for v in range(w + 1, N):
            a = bin(w & ~v).count('1'); b = bin(v & ~w).count('1'); f = best(max(a, b), min(a, b), 0); tot[f] = tot.get(f, 0) + 1
    npairs = N * (N - 1) // 2
    avg = sum(f * c for f, c in tot.items()) / npairs
    print('  k=%d: %d pairs; generic tau: %s ; mean agreeing fraction %.4f (transform: 1/2 for every pair)' % (k, npairs, sorted((str(f), c) for f, c in tot.items()), float(avg)))
