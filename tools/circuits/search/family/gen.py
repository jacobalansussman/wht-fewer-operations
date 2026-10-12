#!/usr/bin/env python3
"""e2-0-pieces: the 'mixed hub' family.  count (G): a gate is any a*u + b*v with rational a, b, scalings free.
Builds an explicit straight-line program for the N-point Walsh-Hadamard transform, N = 2^k, with
    T(N) = (3/4) N log2 N + N/4   gates      (4 -> 7, 8 -> 20, 16 -> 52, 32 -> 124, 64 -> 304),
writes it to slp_<N>.txt, and replays it exactly (Fractions) on symbolic inputs: every output must be EXACTLY its row of H.
A character of a cube of size m is indexed by w in [0, m); the top bit of w is the sign on the upper half.
D(cube, e): for every character alpha of the half-size cube, the piece (y_alpha on L, e*y_alpha on R)  [half of the cube's outputs].
A mixed hub is M = (y_a on L) + c*(y_b on R) with a = (gamma,+), b = (gamma,-): two DIFFERENT characters on the two halves.
usage: gen.py k"""
import sys
from fractions import Fraction as F
k = int(sys.argv[1]); N = 1 << k
def par(w, x): return -1 if bin(w & x).count('1') & 1 else 1
def piece(w, idxs, sign=1):
    v = [0] * N
    for pos, i in enumerate(idxs): v[i] = sign * par(w, pos)
    return tuple(v)
vec = {('x', i): tuple(int(i == j) for j in range(N)) for i in range(N)}
prog = []; names = {}
for i in range(N): names[vec[('x', i)]] = ('x', i)
def solve2(u, v, p):
    for i in range(N):
        for j in range(i + 1, N):
            det = u[i] * v[j] - u[j] * v[i]
            if det:
                a = F(p[i] * v[j] - p[j] * v[i], det); b = F(u[i] * p[j] - u[j] * p[i], det)
                return (a, b) if all(a * u[t] + b * v[t] == p[t] for t in range(N)) else None
    return None
cnt = [0]
def gate(target, n1, n2, kind):
    s = solve2(vec[n1], vec[n2], target)
    if s is None or 0 in s: return None
    cnt[0] += 1; nm = (kind, cnt[0]); vec[nm] = target; prog.append((nm, s[0], n1, s[1], n2)); return nm
def cat(*vs): return tuple(sum(c) for c in zip(*vs))
def D(idxs, e):
    m = len(idxs); L, R = idxs[:m // 2], idxs[m // 2:]
    if m == 2:
        return {'P': {0: gate(cat(piece(0, L), piece(0, R, e)), ('x', L[0]), ('x', R[0]), 'p')}, 'W': {}}
    DL = D(L, 1); DR = D(R, -1); P = {}; W = {}
    for g in range(m // 4):
        a, b = g, g + m // 4
        A, B = DL['P'][g], DR['P'][g]
        tau = 1 if (m == 4 or g < m // 8) else -1
        c = -e * tau
        M = gate(cat(vec[A], tuple(c * t for t in vec[B])), A, B, 'hub')
        assert M
        wR = DR['W'][g] if m >= 8 else ('x', R[0])
        wL = DL['W'][g] if m >= 8 else ('x', L[0])
        P[a] = gate(cat(piece(a, L), piece(a, R, e)), M, wR, 'p'); assert P[a], ('Pa', m, g)
        P[b] = gate(cat(piece(b, L), piece(b, R, e)), M, wL, 'p'); assert P[b], ('Pb', m, g)
        W[a] = A; W[b] = B
    return {'P': P, 'W': W}
def top(idxs):
    m = len(idxs); L, R = idxs[:m // 2], idxs[m // 2:]
    DL = D(L, 1); DR = D(R, -1)
    for g in range(m // 4):
        a, b = g, g + m // 4
        A, B = DL['P'][g], DR['P'][g]
        M = gate(cat(vec[A], vec[B]), A, B, 'hub')
        for ch, wit, own in ((a, DR['W'][g] if m >= 8 else None, A), (b, DL['W'][g] if m >= 8 else None, B)):
            first = None
            for s in (1, -1):
                tgt = cat(piece(ch, L), piece(ch, R, s))
                cands = [wit] if wit else [('x', i) for i in idxs]
                for wn in cands:
                    first = gate(tgt, M, wn, 'y')
                    if first: break
                if first: break
            assert first, ('top', g, ch)
            other = cat(piece(ch, L), piece(ch, R, -s))
            assert gate(other, first, own, 'y')
top(list(range(N)))
# exact replay from scratch
val = {('x', i): [F(int(i == j)) for j in range(N)] for i in range(N)}
for nm, a, u, b, v in prog: val[nm] = [a * s + b * t for s, t in zip(val[u], val[v])]
rows = {tuple(par(w, x) for x in range(N)): w for w in range(N)}
got = set()
for nm, a, u, b, v in prog:
    if nm[0] == 'y':
        t = tuple(val[nm]); assert t in rows, 'an output is not exactly a row of H'; got.add(rows[t])
ok = got == set(range(N))
kinds = {}
for nm, *_ in prog: kinds[nm[0]] = kinds.get(nm[0], 0) + 1
coef = sorted({abs(c) for _, a, _, b, _ in prog for c in (a, b)})
supp = {}
for nm, *_ in prog:
    if nm[0] != 'y':
        s = sum(1 for t in vec[nm] if t); supp[s] = supp.get(s, 0) + 1
print('N', N, 'gates', len(prog), 'formula 3/4 N log N + N/4 =', 3 * N * k // 4 + N // 4, 'textbook', N * k, 'ratio %.4f' % (len(prog) / (N * k)),
      'all outputs exact:', ok, 'kinds', kinds, 'coefficients |.|', [str(c) for c in coef], 'helper supports', sorted(supp.items()))
with open('slp_%d.txt' % N, 'w') as f:
    f.write('# count (G) program for the %d-point Walsh-Hadamard transform, %d gates; each line: name = a*u + b*v\n' % (N, len(prog)))
    nmf = lambda n: '%s%d' % n
    for nm, a, u, b, v in prog: f.write('%s = %s * %s + %s * %s    # %s\n' % (nmf(nm), a, nmf(u), b, nmf(v), ' '.join('%d' % t for t in vec[nm]) if N <= 16 else ''))
