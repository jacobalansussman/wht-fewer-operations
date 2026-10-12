#!/usr/bin/env python3
"""g-7-thirdturn / lines27.py -- 16 points, exact.  The stabilizer bases kept by R (and by every twist T_a S).
Each vector of the pool fixed by R generates one basis (its images under address shifts and characters).  Count them,
check each is closed under R, give row weights, see what S and T do to the set of bases, and how two bases meet."""
import itertools
import search16 as s
n = 16
st = s.stabs(); idx = {v: i for i, v in enumerate(st)}
fixed = [v for v in st if s.Rmap(v) == v]
def paulis(v):
    out = set()
    for t in range(n):
        for c in range(n):
            out.add(s.prim([v[x ^ t] * (-1 if s.w(c, x) else 1) for x in range(n)]))
    return frozenset(out)
Smap = lambda f: s.prim([sum(f[x] * s.S[x][y] for x in range(n) if f[x]) for y in range(n)])
Tmap = lambda f: s.prim([f[x] * s.T[x] for x in range(n)])
bases = {}
for v in fixed:
    b = paulis(v); bases[b] = v
print("vectors fixed by R: %d ; distinct bases they generate: %d ; sizes: %s" % (len(fixed), len(bases), sorted({len(b) for b in bases})))
ok = all(frozenset(s.Rmap(f) for f in b) == b for b in bases)
print("each basis closed under R:", ok, "; orthogonal:", all(all(sum(a * c for a, c in zip(f, g)) == 0 for f, g in itertools.combinations(sorted(b), 2)) for b in bases))
wts = {}
for b in bases:
    k = tuple(sorted({sum(1 for x in f if x) for f in b})); wts[k] = wts.get(k, 0) + 1
print("non-zeros per row -> number of bases:", wts)
bl = list(bases); bi = {b: i for i, b in enumerate(bl)}
for name, M in (("S", Smap), ("T", Tmap)):
    img = [bi.get(frozenset(M(f) for f in b)) for b in bl]
    fixedb = sum(1 for i, t in enumerate(img) if t == i); moved = sum(1 for i, t in enumerate(img) if t is not None and t != i); out = sum(1 for t in img if t is None)
    print("%s maps the set of bases to itself: %s ; bases kept: %d ; swapped in pairs: %d ; sent outside: %d" % (name, out == 0, fixedb, moved, out))
# incidence: two bases 'meet' if some row of one has exactly 4*... use the common-stabilizer size: count rows of b2 with few non-zeros in basis b1 is costly; use inner products
def overlap(b1, b2):
    f = next(iter(b1)); return sorted({sum(1 for g in b2 if sum(a * c for a, c in zip(f, g)) != 0)})
deg = {}
for b1 in bl:
    row = tuple(sorted(sum(1 for b2 in bl if b2 != b1 and overlap(b1, b2) == [k]) for k in (4, 16)))
    deg[row] = deg.get(row, 0) + 1
print("for each basis: (number of other bases in which each of its rows spreads over 4 rows, over 16 rows), sorted -> count:", deg)
