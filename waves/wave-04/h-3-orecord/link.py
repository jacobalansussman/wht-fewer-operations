#!/usr/bin/env python3
"""h-3-orecord / link.py.  Exact (Fractions).  Is g-1's 20-operation unit e-5's reflection gate R_q seen again?
R_q(v) = I - (2/q) v v^T for a sign vector v on q points (e-5: q-1 additions, 1 multiplication, q subtractions = 2q operations (O)).
(1) For the centre c of g-1's circuit: M = H_8 * R_8(c).  Print the rows of M: which rows of H are untouched, which become short.
(2) The same at 4 points with the brick's hub, and at 16 points with (a) hub x hub (bent) and (b) hub x character x character.
(3) Entropy meter of e-5 (bits = -sum p log2 p over squared entries of the orthonormal matrix), exact rationals inside the log:
    R_q on fresh data for q = 4, 8, 16, and the bits that remain to be made after it."""
from fractions import Fraction as Fr
from math import log2
def H(k):
    N = 1 << k
    return [[(-1) ** bin(j & x).count('1') for x in range(N)] for j in range(N)]
def refl(v):
    q = len(v); return [[Fr(1 if i == j else 0) - Fr(2, q) * v[i] * v[j] for j in range(q)] for i in range(q)]
def mul(A, B):
    n = len(A); m = len(B[0]); return [[sum(A[i][t] * B[t][j] for t in range(len(B))) for j in range(m)] for i in range(n)]
def ent(M, scale2):
    """M real matrix with all rows of squared norm scale2: bits of M/sqrt(scale2)."""
    s = 0.0
    for r in M:
        for z in r:
            p = Fr(z * z) / scale2
            if p: s -= float(p) * log2(float(p))
    return s
def kron(u, v): return [a * b for a in u for b in v]
def report(name, c):
    N = len(c); k = N.bit_length() - 1; Hm = H(k); R = refl(c)
    assert mul(R, R) == [[Fr(1 if i == j else 0) for j in range(N)] for i in range(N)]
    M = mul(Hm, R)
    spec = [sum(Hm[j][x] * c[x] for x in range(N)) for j in range(N)]
    kept = sum(1 for j in range(N) if M[j] == Hm[j]); sup = sorted(sum(1 for z in M[j] if z) for j in range(N))
    print('%s: N=%d centre %s' % (name, N, ''.join('+' if z > 0 else '-' for z in c)))
    print('   Walsh spectrum of the centre (values: how many rows): %s' % {v: spec.count(v) for v in sorted(set(spec))})
    print('   M = H * R_N(centre): rows equal to a row of H: %d; supports of the rows of M: %s' % (kept, sup))
    b = ent(R, 1); print('   bits made by R_N on fresh data: %.4f of %d  (%.4f per operation at 2N = %d operations (O)); bits left: %.4f' % (b, N * k, b / (2 * N), 2 * N, N * k - b))
    return M
hub4 = [1, 1, 1, -1]
report('4 points, brick hub', hub4)
# g-1's centre in ITS input order: g7 = x0 - x1 - x2 - x3 + x4 + x5 - x6 + x7
c8 = [1, -1, -1, -1, 1, 1, -1, 1]
M = report('8 points, g-1 centre', c8)
for j, r in enumerate(M): print('      row %d of M: %s' % (j, ' '.join('%2s' % str(z) for z in r)))
report('16 points, hub x hub (bent)', kron(hub4, hub4))
report('16 points, hub x (+,+) x (+,-)', kron(kron(hub4, [1, 1]), [1, -1]))
report('16 points, g-1 centre x (+,+)', kron(c8, [1, 1]))
print()
print('unit of 20 operations: 24 bits (a flat 8-point transform up to one common scale), 24/20 = %.4f bits per operation' % (24 / 20))
