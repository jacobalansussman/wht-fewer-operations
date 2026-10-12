# z-0/small.py : three small exact checks, pure Python.
#  (1) lemma 2 outside the whole numbers: numbers a + b*sqrt2 (pairs of whole numbers), wires with entries of size <= 1, coefficient unbounded
#  (2) x-8's bridge: whole-number matrix with orthogonal primitive rows: entropy <= 2 log2|det|, equality iff entries 0, +-1
#  (3) what lemma 3 gives as numbers, against the trivial 2N - 2 and against (3/4) N log2 N
import itertools, math, random
from fractions import Fraction as F
from math import gcd, log2

# ---------- (1)
def mul(x, y): return (x[0]*y[0] + 2*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
def val(x): return x[0] + x[1] * math.sqrt(2)
print('(1) numbers a + b*sqrt2.  u = (1, 0), v = (1, e), w = (0, 1), e = (sqrt2 - 1)^k, 1/e = (sqrt2 + 1)^k')
e = (1, 0); inv = (1, 0)
for k in range(1, 9):
    e = mul(e, (-1, 1)); inv = mul(inv, (1, 1))
    assert mul(e, inv) == (1, 0)                      # exact: e * inv = 1, so w = inv*v - inv*u holds exactly, coordinate by coordinate
    # coordinate 1: inv*1 - inv*1 = 0 ; coordinate 2: inv*e - 0 = 1
    print('   k=%d  e = %d + %d*sqrt2 = %.6f  largest entry of u, v, w in size = 1   coefficients +-(%d + %d*sqrt2) = %.1f   budget log2(2*%.1f) = %.2f   (bound for whole numbers of height 1: log2 3 = 1.58)'
          % (k, e[0], e[1], val(e), inv[0], inv[1], val(inv), val(inv), log2(2 * val(inv))))

# ---------- (2)
def det(Mx):
    n = len(Mx); A = [[F(x) for x in r] for r in Mx]; d = F(1)
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c] != 0), None)
        if p is None: return F(0)
        if p != c: A[c], A[p] = A[p], A[c]; d = -d
        d *= A[c][c]
        for r in range(c + 1, n):
            f = A[r][c] / A[c][c]
            if f: A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return d
def kron(A, B): return [[a * b for a in ra for b in rb] for ra in A for rb in B]
def dsum(A, B): return [r + [0] * len(B[0]) for r in A] + [[0] * len(A[0]) + r for r in B]
def check(Mx, name):
    n = len(Mx)
    for i in range(n):
        g = 0
        for x in Mx[i]: g = gcd(g, abs(x))
        assert g == 1, 'row not primitive'
        for j in range(i):
            assert sum(x * y for x, y in zip(Mx[i], Mx[j])) == 0, 'rows not orthogonal'
    d = abs(det(Mx)); phi = 0.0; prodnorm = 1
    for r in Mx:
        s = sum(x * x for x in r); prodnorm *= s
        for x in r:
            if x: p = F(x * x, s); phi -= float(p) * log2(p)
    assert prodnorm == d * d                          # exact: product of squared row lengths = det^2
    small = all(abs(x) <= 1 for r in Mx for x in r); rhs = 2 * log2(d)
    ok = phi <= rhs + 1e-9 and ((abs(phi - rhs) < 1e-9) == small)
    return ok, phi, rhs, small
print('(2) entropy against 2 log2|det| (row lengths and determinant exact; the two logarithms in floating point)')
B = lambda a, b: [[a, b], [b, -a]]
H2 = B(1, 1); tests = []
Hk = [[1]]
for k in range(1, 5):
    Hk = kron(Hk, H2); tests.append(('H at %d points' % 2 ** k, Hk))
tests.append(('brick J - 2I at 4', [[-1, 1, 1, 1], [1, -1, 1, 1], [1, 1, -1, 1], [1, 1, 1, -1]]))
tests.append(('3-4-5 rotation', B(3, 4))); tests.append(('(1,2)', B(1, 2)))
rnd = random.Random(7); blocks = [B(a, b) for a in range(0, 6) for b in range(1, 6) if gcd(a, b) == 1]
for t in range(60):
    Mx = rnd.choice(blocks)
    for _ in range(rnd.randint(0, 2)):
        Mx = kron(Mx, rnd.choice(blocks)) if rnd.random() < 0.6 else dsum(Mx, rnd.choice(blocks))
    tests.append(('random product/sum %d (size %d)' % (t, len(Mx)), Mx))
bad = 0; eq = 0
for name, Mx in tests:
    ok, phi, rhs, small = check(Mx, name); bad += (not ok); eq += (abs(phi - rhs) < 1e-9)
    if not name.startswith('random'): print('   %-22s entropy %.3f   2 log2|det| %.3f   entries all 0,+-1: %s' % (name, phi, rhs, small))
print('   matrices %d ; with equality %d ; violations (entropy above 2 log2|det|, or equality without 0,+-1 entries, or the converse) %d' % (len(tests), eq, bad))
# in place: row_i <- (a row_i + b row_j)/g multiplies the determinant by a/g
viol = 0; moves = 0
for t in range(400):
    n = rnd.randint(2, 5); Mx = [[rnd.randint(-3, 3) for _ in range(n)] for _ in range(n)]
    d0 = det(Mx)
    if d0 == 0: continue
    i, j = rnd.sample(range(n), 2); a = rnd.choice([-5, -3, -2, -1, 1, 2, 3, 4, 5]); b = rnd.randint(-5, 5)
    new = [a * x + b * y for x, y in zip(Mx[i], Mx[j])]; g = 0
    for x in new: g = gcd(g, abs(x))
    M2 = [r[:] for r in Mx]; M2[i] = [x // g for x in new]; moves += 1
    if det(M2) != d0 * F(a, g): viol += 1
print('   in-place moves %d ; determinant not multiplied by exactly a/g: %d' % (moves, viol))

# ---------- (3)
print('(3) lemma 3 as numbers (G): N - 1 + ((N/2) log2 N - (N-1) log2 M) / log2(4 M^2)   [M = 1: divide by log2 3]')
print('      k        N   trivial 2N-2   M=1        M=2        M=4        M=16       M=sqrt(N)   (3/4) N log2 N (best family tonight)')
def lem3(N, M):
    need = (N / 2) * log2(N)
    return N - 1 + (need / log2(3) if M == 1 else (need - (N - 1) * log2(M)) / log2(4 * M * M))
for k in (2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 30, 40, 64, 100):
    N = 2 ** k
    print('   %4d %8.3g %12.4g %10.4g %10.4g %10.4g %10.4g %10.4g %14.4g' % (k, N, 2 * N - 2, lem3(N, 1), lem3(N, 2), lem3(N, 4), lem3(N, 16), lem3(N, 2 ** (k / 2)), 0.75 * N * k))
print('   lemma 3 exceeds the trivial 2N - 2 only when log2 N > 4 + 6 log2 M (M >= 2), or log2 N >= 4 for M = 1:')
for M in (1, 2, 3, 4, 8, 16, 256):
    k = 2
    while lem3(2 ** k, M) <= 2 * 2 ** k - 2: k += 1
    print('      M = %3d : first at N = 2^%d' % (M, k))
