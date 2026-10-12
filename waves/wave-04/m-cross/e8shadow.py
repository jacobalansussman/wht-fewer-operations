# m-cross: the published unit's scatter matrix M (h-7: 120 x 120, 1 on the diagonal, +-1/2 on 56 neighbours, rank 8, M M = 15 M),
# rebuilt here as half the Gram matrix of one root per line of E8, and read modulo 2 (after doubling, so that it is primitive).  exact.
from fractions import Fraction as F
from itertools import combinations, product
roots = []
for i, j in combinations(range(8), 2):
    for a, b in product((1, -1), repeat=2):
        v = [F(0)] * 8; v[i] = F(a); v[j] = F(b); roots.append(tuple(v))
for s in product((1, -1), repeat=8):
    if s.count(-1) % 2 == 0: roots.append(tuple(F(t, 2) for t in s))
lines = []
for r in roots:
    if tuple(-t for t in r) not in lines: lines.append(r)
n = len(lines); G = [[sum(a * b for a, b in zip(u, v)) for v in lines] for u in lines]   # G = 2 M
print('lines', n, ' entries of 2M:', sorted({int(t) for row in G for t in row}), ' neighbours per row:', sorted({sum(1 for t in row if abs(t) == 1) for row in G}))
M2 = [[sum(G[i][k] * G[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
print('(2M)(2M) = 30 (2M):', all(M2[i][j] == 30 * G[i][j] for i in range(n) for j in range(n)))
def rank2(rows):
    rows = [sum((int(t) % 2) << j for j, t in enumerate(r)) for r in rows]; rk = 0
    for bit in range(n):
        p = next((i for i in range(rk, len(rows)) if rows[i] >> bit & 1), None)
        if p is None: continue
        rows[rk], rows[p] = rows[p], rows[rk]
        for i in range(len(rows)):
            if i != rk and rows[i] >> bit & 1: rows[i] ^= rows[rk]
        rk += 1
    return rk
print('rank of 2M modulo 2:', rank2(G), '  (rank over the rationals is 8 by h-7)')
S = [frozenset(j for j in range(n) if int(G[i][j]) % 2) for i in range(n)]
print('row classes modulo 2: sizes', sorted({len(s) for s in S}), ' distinct', len(set(S)), ' the diagonal entry survives modulo 2:', any(i in S[i] for i in range(n)))
ov = sorted({len(S[i] & S[j]) for i in range(n) for j in range(i)})
bad = sum(1 for i in range(n) for j in range(i) if S[i] & S[j] and not S[i] <= S[j] and not S[j] <= S[i])
print('pairwise overlaps of the classes:', ov, ' pairs that overlap without nesting:', bad, 'of', n * (n - 1) // 2)
