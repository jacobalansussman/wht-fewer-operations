#!/usr/bin/env python3
"""model.py (g-0-mirror): the mirror at 16 points, exactly.
S = symmetric form of the 16-point transform, kernel (-1)^(p1.y2 + p2.y1).  C0 = the six elliptic sign vectors (rows).
Checks: C0 S = -4 C0, C0 C0^T = 16 I, the 16 columns of C0 (the 'targets', points of the 6-dim mirror) are the 16 even sign
vectors of length 6 up to sign (16 equiangular lines), no three collinear, each pair of targets spans a line holding exactly one
'root' (a vector with two non-zeros), 30 roots, each on 4 such lines.  Writes tables.txt for search.c."""
import itertools, sys
from fractions import Fraction as F
def dot2(a, b): return bin(a & b).count('1') & 1
N = 16
def halves(p): return p >> 2, p & 3
S = [[(-1) ** (dot2(halves(p)[0], halves(y)[1]) ^ dot2(halves(p)[1], halves(y)[0])) for y in range(N)] for p in range(N)]
assert all(S[i][i] == 1 for i in range(N)) and all(S[i][j] == S[j][i] for i in range(N) for j in range(N))
SS = [[sum(S[i][k] * S[k][j] for k in range(N)) for j in range(N)] for i in range(N)]
assert all(SS[i][j] == (16 if i == j else 0) for i in range(N) for j in range(N))
ell, hyp = [], []
for a in range(N):
    v = [(-1) ** (dot2(halves(p)[0], halves(p)[1]) ^ dot2(a, p)) for p in range(N)]
    Sv = [sum(S[i][j] * v[j] for j in range(N)) for i in range(N)]
    if Sv == [-4 * x for x in v]: ell.append(v)
    elif Sv == [4 * x for x in v]: hyp.append(v)
    else: raise SystemExit('not an eigenvector')
print('elliptic', len(ell), 'hyperbolic', len(hyp))
C0 = ell
assert all(sum(C0[i][p] * C0[j][p] for p in range(N)) == (16 if i == j else 0) for i in range(6) for j in range(6))
T = [tuple(C0[i][p] for i in range(6)) for p in range(N)]
def norm(v):
    for x in v:
        if x != 0: return tuple(v) if x > 0 else tuple(-y for y in v)
    return tuple(v)
T = [norm(t) for t in T]
print('targets (columns of C0, sign-normalised):')
for p, t in enumerate(T): print('  p=%2d' % p, t, 'minus signs:', sum(1 for x in t if x < 0))
assert len(set(T)) == 16
gram = sorted(set(abs(sum(a * b for a, b in zip(T[i], T[j]))) for i in range(N) for j in range(i)))
print('absolute inner products between distinct targets:', gram, ' (square length 6): 16 equiangular lines, cosine 1/3')
# P_- = C0^T C0 / 16 = (I - S/4)/2
for i in range(N):
    for j in range(N):
        g = sum(C0[k][i] * C0[k][j] for k in range(6))
        assert F(g, 16) == (F(int(i == j)) - F(S[i][j], 4)) / 2
print('C0^T C0 / 16 = (I - S/4)/2: yes')
def rank(rows):
    A = [[F(x) for x in r] for r in rows]; r = 0
    for c in range(len(A[0])):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        for i in range(r + 1, len(A)):
            if A[i][c] != 0:
                f = A[i][c] / A[r][c]; A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        r += 1
    return r
assert all(rank([T[a], T[b], T[c]]) == 3 for a, b, c in itertools.combinations(range(N), 3))
print('no three targets collinear: yes (560 triples of rank 3)')
dep4 = sum(1 for q in itertools.combinations(range(N), 4) if rank([T[i] for i in q]) == 3)
print('coplanar quadruples of targets (4-term dependencies):', dep4)
roots = {}
for a, b in itertools.combinations(range(N), 2):
    cands = [norm(tuple((x - y) // 2 for x, y in zip(T[a], T[b]))), norm(tuple((x + y) // 2 for x, y in zip(T[a], T[b])))]
    rs = [c for c in cands if sum(1 for x in c if x) == 2]
    assert len(rs) == 1
    roots.setdefault(rs[0], []).append((a, b))
print('roots:', len(roots), ' secants per root:', sorted(set(len(v) for v in roots.values())))
R = sorted(roots)
# root triples (three roots on a line)
rt = [(i, j, k) for i, j, k in itertools.combinations(range(len(R)), 3) if rank([R[i], R[j], R[k]]) == 2]
print('collinear root triples:', len(rt))
with open('tables.txt', 'w') as f:
    f.write('%d %d\n' % (len(R), len(rt)))
    for r in R: f.write(' '.join(map(str, r)) + '   ' + ' '.join('%d %d' % ab for ab in roots[r]) + '\n')
    for t in rt: f.write('%d %d %d\n' % t)
    for t in T: f.write(' '.join(map(str, t)) + '\n')
print('wrote tables.txt')
