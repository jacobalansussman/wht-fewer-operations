#!/usr/bin/env python3
"""linerel.py [ad-7]  Shortest relations modulo 2 among the 20 line sums of the plane at 16 points, and the relation
'lines through a point = all-ones + q x point' over the whole numbers."""
import itertools, sys
sys.path.insert(0, '.')
from profile import linesums
M = linesums(2); N = 16
masks = [sum(1 << x for x in range(N) if r[x]) for r in M]
for t in range(1, 8):
    c = 0
    for S in itertools.combinations(range(20), t):
        v = 0
        for i in S: v ^= masks[i]
        if v == 0: c += 1
    print("relations modulo 2 with exactly %d lines: %d" % (t, c))
    if c and t >= 4: break
ok = True
for p in range(N):
    s = [sum(M[i][x] for i in range(20) if M[i][p]) for x in range(N)]
    ok &= s == [1 + 4 * (x == p) for x in range(N)]
print("the 5 lines through a point add up to all-ones + 4 x (the point), all 16 points:", ok)
