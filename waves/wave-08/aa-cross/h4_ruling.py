#!/usr/bin/env python3
"""h4_ruling.py [aa-cross]  Fact D, second half, at 16 points, whole numbers.  The zeros of y1 y2 + y3 y4 are the union of
three planes that meet pairwise in 0 (a partial spread), so the quadric-sign convolution is built from the coset sums of
those three planes: C = J - 2 * (sum over the three planes of 'sum over the plane') + 4 * identity, entry by entry."""
import itertools
N = 16
q = lambda y: ((y & 1) * ((y >> 1) & 1) + ((y >> 2) & 1) * ((y >> 3) & 1)) & 1
zero = [y for y in range(N) if q(y) == 0]
planes = list({frozenset({0, a, b, a ^ b}) for a, b in itertools.combinations(range(1, N), 2) if all(q(y) == 0 for y in (a, b, a ^ b))})
tri = [t for t in itertools.combinations(planes, 3) if all(len(x & y) == 1 for x, y in itertools.combinations(t, 2)) and set().union(*t) == set(zero)]
print("zeros of the form: %d ; planes inside the zero set: %d ; triples of planes meeting pairwise in 0 that cover it: %d" % (len(zero), len(planes), len(tri)))
t = tri[0]
ok = all((1 - 2 * q(x ^ y)) == -1 + 2 * sum(1 for P in t if (x ^ y) in P) - 4 * (1 if x == y else 0) for x in range(N) for y in range(N))
print("quadric signs(x + y) = -1 + 2 * (number of the three planes containing x + y) - 4 * [x = y] on all 256 entries:", ok)
print("so the 16-point convolution with quadric signs = -J + 2 * (three families of plane sums, spread back) - 4 * identity")
