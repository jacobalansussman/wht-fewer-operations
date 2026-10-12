#!/usr/bin/env python3
# h-5 / bentdist.py : the sign vector w(x) = Re((1-i) i^(weight of x)) at 2^k points, and its distance (number of entries that differ,
# after the better of the two overall signs) to each of the 2^k outputs.  Exact integers.
for k in range(2, 9):
    N = 1 << k
    w = [(1, 1, -1, -1)[bin(x).count('1') % 4] for x in range(N)]
    d = {}
    for c in range(N):
        diff = sum(1 for x in range(N) if w[x] != (-1) ** bin(c & x).count('1'))
        diff = min(diff, N - diff); d[diff] = d.get(diff, 0) + 1
    print('k=%d N=%d: distance to the outputs -> how many outputs: %s' % (k, N, sorted(d.items())))
