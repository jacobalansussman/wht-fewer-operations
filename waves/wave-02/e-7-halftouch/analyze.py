# analyze.py (e-7-halftouch): exact checks on one altmin.c result.
#  1. the lemma: every c with c^T A = 0 has H c = S^T c  (so the transform acts on that space through the sparse S alone)
#  2. the size of that space, the smallest support found among simple combinations, the list of non-zero entries of S
import sys
from fractions import Fraction as Fr
from replay2 import load, child, Hm, mul, rank
def kernel_left(A):           # basis of {c : c^T A = 0}
    N = len(A); m = len(A[0])
    M = [[A[x][i] for x in range(N)] for i in range(m)]      # m x N, kernel of this
    M = [r[:] for r in M]; piv = []; r = 0
    for c in range(N):
        p = next((i for i in range(r, m) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; d = M[r][c]; M[r] = [v / d for v in M[r]]
        for i in range(m):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f*b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
    out = []
    for fc in [c for c in range(N) if c not in piv]:
        v = [Fr(0)] * N; v[fc] = Fr(1)
        for row, pc in zip(M, piv): v[pc] = -row[fc]
        out.append(v)
    return out
hd, N, mode, m, A, B = load(sys.argv[1]); C = child(N, mode); H = Hm(N)
M = mul(mul(A, C), B); S = [[H[x][y] - M[x][y] for y in range(N)] for x in range(N)]
K = kernel_left(A)
ok = all([sum(H[y][x] * c[x] for x in range(N)) for y in range(N)] == [sum(S[x][y] * c[x] for x in range(N)) for y in range(N)] for c in K)
print("file", sys.argv[1], "N", N, "m", m, "| nnz(S)", sum(1 for r in S for v in r if v != 0), "| left kernel of A: dimension", len(K), "| H c = S^T c on all of it:", ok)
print("  supports of the kernel basis vectors:", sorted(sum(1 for v in c if v != 0) for c in K), " (bound from the lemma: at least N / (support of S^T c))")
ent = [(x, y, S[x][y]) for x in range(N) for y in range(N) if S[x][y] != 0]
print("  non-zero entries of S (row, column, value):", " ".join(f"({x},{y},{v})" for x, y, v in ent))
print("  rows of S untouched:", [x for x in range(N) if all(v == 0 for v in S[x])], " columns untouched:", [y for y in range(N) if all(S[x][y] == 0 for x in range(N))])
print("  sum of squares of S:", sum(v*v for r in S for v in r), " lemma's lower bound (N - m) * N =", (N - m) * N)
