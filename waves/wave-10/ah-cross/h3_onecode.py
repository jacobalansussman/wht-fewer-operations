# Hybrid 3: one code for the whole class. Columns of weight below k/2 of the k-th power of the kernel (1,1;1,tau):
# do they span the same space for every tau? Is the set of even-weight points an information set for it?
from fractions import Fraction as F
def rank(M):
    M = [r[:] for r in M]; rk = 0; rows = len(M); cols = len(M[0])
    for c in range(cols):
        p = next((r for r in range(rk, rows) if M[r][c] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]; inv = 1 / M[rk][c]
        for r in range(rows):
            if r != rk and M[r][c] != 0:
                f = M[r][c] * inv; M[r] = [a - f * b for a, b in zip(M[r], M[rk])]
        rk += 1
    return rk
w = lambda x: bin(x).count('1')
for k in (3, 5):
    N = 1 << k; low = [x for x in range(N) if w(x) <= (k - 1) // 2]; n = len(low)
    A = {t: [[F(t) ** w(x & y) for x in low] for y in range(N)] for t in (F(-1), F(3), F(5, 7), F(-2), F(2))}
    for t in A:
        both = [A[F(-1)][y] + A[t][y] for y in range(N)]
        ev = [A[t][y] for y in range(N) if w(y) % 2 == 0]
        print(f"k={k} tau={t}: rank of the low columns {rank(A[t])} of {n}; rank together with the transform's low columns "
              f"{rank(both)} (equal to {n} means the same space); rank on the even-weight points {rank(ev)}")
