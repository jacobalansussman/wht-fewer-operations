#!/usr/bin/env python3
"""pairs.py -- can the covering bound (2^m - 1)/2^(m-2) moves per array be met with equality?  [e2-2-ladder]  Exact, tiny.
Old letters only.  At equality every direction z is used W/2^(m-2) times and every form q = (a.z)(b.z) with a.b = 1
(the forms with q(I) = 1 that are 1 on the fewest directions, 2^(m-2) of them) selects exactly W reflections whose
product is -1 on W arrays: such W reflections commute and are independent (a frame).
If every two directions z != z' lie together in the 1-set of one such form, then ALL reflections of the unit commute,
and a commuting family in dimension W has at most W different reflections of a frame, against (2^m - 1) W / 2^(m-2) needed.
This program checks the 'every two directions' statement, and counts the forms.
"""
import itertools
def dot(a, b): return bin(a & b).count("1") & 1
for m in (3, 4, 5, 6, 7):
    V = range(1, 1 << m)
    forms = [(a, b) for a in V for b in V if a < b and dot(a, b) == 1]
    cover = {}
    for a, b in forms:
        ones = [z for z in V if dot(a, z) and dot(b, z)]
        assert len(ones) == 1 << (m - 2)
        for z, zz in itertools.combinations(ones, 2):
            cover[(z, zz)] = cover.get((z, zz), 0) + 1
    npairs = (len(V) * (len(V) - 1)) // 2
    missing = [p for p in itertools.combinations(V, 2) if p not in cover]
    print("m = %d: %d product forms with a.b = 1, each 1 on %d directions; pairs of directions %d, covered %d, not covered %d %s"
          % (m, len(forms), 1 << (m - 2), npairs, len(cover), len(missing), [(bin(x)[2:], bin(y)[2:]) for x, y in missing[:6]]))
