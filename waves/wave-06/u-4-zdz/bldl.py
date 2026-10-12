# u-4-zdz / bldl.py : "yes, and" number 2.  Most orders of the addresses have a zero pivot.  Allow pivots of size 2 as well:
#     (H in the order p) = L B L^T,  L lower triangular with ones on the diagonal and zeros inside the blocks,
#     B block diagonal with blocks of size 1 and 2 (each 2 x 2 block costs at most 2 gates (G)).
# For every order (first address fixed to 0: moving it is a sign scaling) and every way of cutting 0..N-1 into blocks of size
# 1 and 2: the number of non-zeros of L below the blocks.  cost(H) <= 2 * (that number) + 2 * (number of 2 x 2 blocks).
# Is anything sparser than subset sums (19 at 8 points; 5 at 4 points)?  Exact fractions.   usage: bldl.py K
import sys, itertools
from fractions import Fraction as F
def pop(x): return bin(x).count('1')
K = int(sys.argv[1]); N = 1 << K
def cuts(n):
    if n == 0: yield (); return
    for c in cuts(n - 1): yield (1,) + c
    if n >= 2:
        for c in cuts(n - 2): yield (2,) + c
CUTS = list(cuts(N))
def fact(p, cut):
    A = [[F((-1) ** pop(p[i] & p[j])) for j in range(N)] for i in range(N)]
    Lnz = 0; c = 0; rows = []
    for s in cut:
        if s == 1:
            d = A[c][c]
            if d == 0: return None
            for i in range(c + 1, N):
                if A[i][c] != 0:
                    f = A[i][c] / d; Lnz += 1; rows.append((i, c, f))
                    for j in range(c + 1, N): A[i][j] -= f * A[c][j]
        else:
            a, b, d2 = A[c][c], A[c][c + 1], A[c + 1][c + 1]; det = a * d2 - b * b
            if det == 0: return None
            for i in range(c + 2, N):
                u, v = A[i][c], A[i][c + 1]
                if u == 0 and v == 0: continue
                l1 = (u * d2 - v * b) / det; l2 = (v * a - u * b) / det
                if l1 != 0: Lnz += 1; rows.append((i, c, l1))
                if l2 != 0: Lnz += 1; rows.append((i, c + 1, l2))
                for j in range(c + 2, N): A[i][j] -= l1 * A[c][j] + l2 * A[c + 1][j]
        c += s
    return Lnz, rows
hist = {}; best = None; tried = 0; failed = 0
for rest in itertools.permutations(range(1, N)):
    p = (0,) + rest
    for cut in CUTS:
        tried += 1; r = fact(p, cut)
        if r is None: failed += 1; continue
        nb = sum(1 for s in cut if s == 2); bound = 2 * r[0] + 2 * nb
        key = (r[0], nb); hist[key] = hist.get(key, 0) + 1
        if best is None or bound < best[0]: best = (bound, r[0], nb, p, cut, r[1])
print('N=%d: factorisations tried %d, impossible (singular pivot) %d' % (N, tried, failed))
print('histogram {(non-zeros of L below the blocks, number of 2x2 blocks): how many}:')
for k2 in sorted(hist): print('   ', k2, hist[k2], '  bound on the transform: %d gates' % (2 * k2[0] + 2 * k2[1]))
print('least bound 2*nonzeros + 2*blocks = %d  (subset sums: %d by non-zeros, %d by Yates; textbook %d)' % (best[0], 2 * (3 ** K - 2 ** K), N * K, N * K))
print('   order', best[3], 'cut', best[4], 'L entries (row, column, value):', [(i, j, str(f)) for i, j, f in best[5]])
