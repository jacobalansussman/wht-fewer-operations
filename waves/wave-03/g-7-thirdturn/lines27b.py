#!/usr/bin/env python3
"""g-7-thirdturn / lines27b.py -- 16 points, exact: the meeting graph of the 27 bases kept by R, in full.
'meet' = a row of one basis spreads over exactly 4 rows of the other; 'skew' = over all 16."""
import itertools
import search16 as s
n = 16
st = s.stabs()
fixed = [v for v in st if s.Rmap(v) == v]
def paulis(v):
    return frozenset(s.prim([v[x ^ t] * (-1 if s.w(c, x) else 1) for x in range(n)]) for t in range(n) for c in range(n))
bl = [paulis(v) for v in fixed]; wt = [sum(1 for x in next(iter(b)) if x) for b in bl]
Smap = lambda f: s.prim([sum(f[x] * s.S[x][y] for x in range(n) if f[x]) for y in range(n)])
bi = {b: i for i, b in enumerate(bl)}
simg = [bi[frozenset(Smap(f) for f in b)] for b in bl]
def spread(b1, b2):
    vals = {sum(1 for g in b2 if sum(a * c for a, c in zip(f, g)) != 0) for f in b1}
    assert len(vals) == 1; return vals.pop()
sp = [[spread(bl[i], bl[k]) if i != k else 0 for k in range(27)] for i in range(27)]
print("spreads that occur between two different bases:", sorted({sp[i][k] for i in range(27) for k in range(27) if i != k}))
print("per basis (meets = spread 4, skew = spread 16):", sorted({(sum(1 for k in range(27) if sp[i][k] == 4), sum(1 for k in range(27) if sp[i][k] == 16)) for i in range(27)}))
flat = [i for i in range(27) if wt[i] == 16]; half = [i for i in range(27) if wt[i] == 4]
print("a half-transform basis meets %s other half-transform bases and %s flat ones" % (sorted({sum(1 for k in half if sp[i][k] == 4) for i in half}), sorted({sum(1 for k in flat if sp[i][k] == 4) for i in half})))
print("a flat basis meets %s flat ones and %s half-transform ones" % (sorted({sum(1 for k in flat if sp[i][k] == 4) for i in flat}), sorted({sum(1 for k in half if sp[i][k] == 4) for i in flat})))
# two sixes: colour the meeting graph on the 12 flat bases
col = {flat[0]: 0}; stack = [flat[0]]; bip = True
while stack:
    i = stack.pop()
    for k in flat:
        if sp[i][k] == 4:
            if k not in col: col[k] = 1 - col[i]; stack.append(k)
            elif col[k] == col[i]: bip = False
print("the 12 flat bases: meeting graph connected: %s, two-colourable: %s, colour classes: %s" % (len(col) == 12, bip, sorted([sum(1 for v in col.values() if v == c) for c in (0, 1)])))
print("S swaps each flat basis with one of the OTHER colour: %s ; and that partner is the one it does not meet in the other six: %s" % (
    all(col[simg[i]] != col[i] for i in flat), all(sp[i][simg[i]] == 16 for i in flat)))
