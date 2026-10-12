# ag-4: check H_N = diag(1, M) (H_2 x H') entry by entry, and (change of basis of a random generator) = 2 H' U. Exact fractions.
from fractions import Fraction as Fr
import random
def pc(x): return bin(x).count("1")
def mm(A, B):
    Bt = list(zip(*B)); return [[sum(a * b for a, b in zip(r, c)) for c in Bt] for r in A]
for k in (3, 5, 7):
    N = 1 << k; r = (k - 1) // 2; full = N - 1; h = N // 2
    X = [x for x in range(N) if pc(x) <= r]; Xc = [full ^ x for x in X]
    E = [y for y in range(N) if pc(y) % 2 == 0]; O = [y for y in range(N) if pc(y) % 2 == 1]
    ch = lambda y, x: (-1) ** pc(x & y)
    HE = [[ch(y, x) for x in X] for y in E]; HO = [[ch(y, x) for x in X] for y in O]
    M = [[Fr(2 * v, N) for v in row] for row in mm(HO, [list(c) for c in zip(*HE)])]
    MH = mm(M, HE)
    ok = all(ch(E[i], Xc[j]) == HE[i][j] for i in range(h) for j in range(h)) \
        and all(ch(O[i], X[j]) == MH[i][j] for i in range(h) for j in range(h)) \
        and all(ch(O[i], Xc[j]) == -MH[i][j] for i in range(h) for j in range(h))
    msg = f"k {k} N {N}: H_N = diag(1, M) (H_2 x H') on every entry: {ok}"
    if k <= 5:
        random.seed(k)
        while True:
            U = [[Fr(random.randint(-3, 3)) for _ in range(h)] for _ in range(h)]
            A_E = U; A_O = mm(M, U)                      # a generator with an arbitrary basis: (U ; M U)
            B = [[sum(ch(E[i], x) * A_E[i][j] + ch(O[i], x) * A_O[i][j] for i in range(h)) for j in range(h)] for x in X]
            Z = [[sum(ch(E[i], x) * A_E[i][j] + ch(O[i], x) * A_O[i][j] for i in range(h)) for j in range(h)] for x in Xc]
            HEt = [list(c) for c in zip(*HE)]             # rows x in X, columns e in E
            two = [[2 * v for v in row] for row in mm(HEt, U)]
            msg += f" | random basis U: change of basis = 2 H' U: {B == two}; high characters all zero: {all(v == 0 for row in Z for v in row)}"
            break
    print(msg)
