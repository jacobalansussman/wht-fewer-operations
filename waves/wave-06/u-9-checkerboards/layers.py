# u-9: exact small checks of the digit picture.  Whole numbers only.
from fractions import Fraction
def pc(v): return bin(v).count("1")
def gray(k): return [i ^ (i >> 1) for i in range(1 << k)]
def brev(v, k): return int(format(v, f"0{k}b")[::-1], 2)
def second(A, rows, cols):
    N = len(rows); P = [[A[r][c] for c in cols] + [0] for r in rows] + [[0] * (N + 1)]
    return [[P[a][b] - P[a + 1][b] - P[a][b + 1] + P[a + 1][b + 1] for b in range(N)] for a in range(N)]
def rebuild(M):
    N = len(M); A = [[0] * (N + 1) for _ in range(N + 1)]
    for a in range(N - 1, -1, -1):
        for b in range(N - 1, -1, -1): A[a][b] = M[a][b] + A[a + 1][b] + A[a][b + 1] - A[a + 1][b + 1]
    return [r[:N] for r in A[:N]]
def rank(Mx):
    M = [[Fraction(v) for v in r] for r in Mx]; r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c]), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
for k in range(2, 7):
    N = 1 << k
    H = [[(-1) ** pc(y & x) for x in range(N)] for y in range(N)]
    m = [[pc(y & x) for x in range(N)] for y in range(N)]
    B = [[pc(y & x) & 1 for x in range(N)] for y in range(N)]
    F = [[pc(y & x) // 2 for x in range(N)] for y in range(N)]
    assert all(H[y][x] == 1 - 2 * m[y][x] + 4 * F[y][x] for y in range(N) for x in range(N))   # H = J - 2 m + 4 floor(m/2)
    # Gray order on the outputs ending at 0, the bit-reversed Gray order on the inputs ending at 0
    rows = gray(k)[::-1]; cols = [brev(g, k) for g in gray(k)][::-1]
    MB = second(B, rows, cols); Mm = second(m, rows, cols); MF = second(F, rows, cols)
    odd = sum(1 for r in MB for v in r if v & 1); chk = sum(1 for r in MB for v in r if abs(v) == 2)
    oth = sum(1 for r in MB for v in r if abs(v) > 2)
    nm = sum(1 for r in Mm for v in r if v); same_support = all((MB[a][b] & 1) == (1 if Mm[a][b] else 0) for a in range(N) for b in range(N))
    same_sign = all(MB[a][b] == Mm[a][b] for a in range(N) for b in range(N) if MB[a][b] & 1)
    # delete the +-2 cells: B' = rebuild(odd part); remainder (B - B')/2
    M1 = [[v if v & 1 else 0 for v in r] for r in MB]; Bp = rebuild(M1)
    R = [[(B[rows[a]][cols[b]] - Bp[a][b]) for b in range(N)] for a in range(N)]
    assert all(v % 2 == 0 for r in R for v in r); R = [[v // 2 for v in r] for r in R]
    isF = all(R[a][b] == -F[rows[a]][cols[b]] for a in range(N) for b in range(N))
    lay = sum(sum(1 for x in range(N) if pc(x) >= j) for j in range(1, k + 1))
    print(f"N={N}: Gray x reversed Gray: odd cells of the parity matrix {odd} [(N/2)log2N = {k*N//2}], checkerboards {chk} [(N/2)(N/2-1) = {N//2*(N//2-1)}], other {oth}; "
          f"corners of the whole-number matrix m {nm}, same cells as the odd cells: {same_support}, same signs: {same_sign}; "
          f"remainder after deleting the checkerboards equals -floor(m/2): {isF}; rank of floor(m/2) = {rank(F) if N <= 32 else '-'}; corners of floor(m/2) in the same orders {sum(1 for r in MF for v in r if v)}; "
          f"sum over digits j of the inputs of weight >= j = {lay}", flush=True)
