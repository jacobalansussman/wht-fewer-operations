# ag-4: the half-rate space S_k (k odd) is { (u on the even-weight points, M u on the odd-weight points) } with M an orthogonal
# matrix that is the half-size transform conjugating the sign of the majority function. Exact fractions.
from fractions import Fraction as Fr
from math import comb
import sys
def pc(x): return bin(x).count("1")
def matmul(A, B):
    Bt = list(zip(*B)); return [[sum(a * b for a, b in zip(r, c)) for c in Bt] for r in A]
for k in (3, 5, 7):
    N = 1 << k; r = (k - 1) // 2
    X = [x for x in range(N) if pc(x) <= r]             # low frequencies
    E = [y for y in range(N) if pc(y) % 2 == 0]; O = [y for y in range(N) if pc(y) % 2 == 1]
    HE = [[(-1) ** pc(x & y) for x in X] for y in E]    # characters of weight <= r at the even points
    HO = [[(-1) ** pc(x & y) for x in X] for y in O]
    # (1) HE is a Hadamard matrix of order N/2 (it is the transform of the group of even points)
    P = matmul(HE, [list(c) for c in zip(*HE)])
    had = all(P[i][j] == (N // 2 if i == j else 0) for i in range(N // 2) for j in range(N // 2))
    # (2) M = HO * HE^-1 = (2/N) HO HE^T : the systematic generator on the even points
    HEt = [list(c) for c in zip(*HE)]
    M = [[Fr(2 * v, N) for v in row] for row in matmul(HO, HEt)]
    MMt = matmul(M, [list(c) for c in zip(*M)])
    orth = all(MMt[i][j] == (1 if i == j else 0) for i in range(N // 2) for j in range(N // 2))
    # (3) entries depend only on the distance between the odd point and the even point
    ker = {}
    radial = True
    for i, y in enumerate(O):
        for j, e in enumerate(E):
            w = pc(y ^ e)
            if w in ker and ker[w] != M[i][j]: radial = False
            ker[w] = M[i][j]
    # (4) relabel the odd point y as the even point y ^ 1: M' is symmetric, M'^2 = 1, trace = N/2 - 2 * (#high characters of the (k-1)-cube)
    idx = {e: j for j, e in enumerate(E)}
    Mp = [[None] * (N // 2) for _ in range(N // 2)]
    for i, y in enumerate(O):
        for j in range(N // 2): Mp[idx[y ^ 1]][j] = M[i][j]
    sym = all(Mp[i][j] == Mp[j][i] for i in range(N // 2) for j in range(N // 2))
    sq = matmul(Mp, Mp); inv = all(sq[i][j] == (1 if i == j else 0) for i in range(N // 2) for j in range(N // 2))
    tr = sum(Mp[i][i] for i in range(N // 2))
    high = sum(comb(k - 1, j) for j in range((k + 1) // 2, k))
    # (5) M' = Hh * diag(sign) * Hh^-1 with Hh the transform of the (k-1)-cube and sign = -1 on weights >= (k+1)/2 (majority, ties to +)
    #     coordinates of an even point e: its bits 1..k-1 (bit 0 is then the parity); frequency x' in k-1 bits
    n1 = k - 1; Nh = 1 << n1
    def proj(e): return e >> 1
    Epos = {proj(e): j for j, e in enumerate(E)}
    D = [(-1 if pc(x) >= (k + 1) // 2 else 1) for x in range(Nh)]
    conj = [[Fr(sum((-1) ** pc(x & a) * D[x] * (-1) ** pc(x & b) for x in range(Nh)), Nh) for b in range(Nh)] for a in range(Nh)]
    same = all(conj[a][b] == Mp[Epos[a]][Epos[b]] for a in range(Nh) for b in range(Nh))
    neg = all(conj[a][b] == -Mp[Epos[a]][Epos[b]] for a in range(Nh) for b in range(Nh))
    # (6) every vector of S_k has the same energy on the even and on the odd points; and the outputs really lie in S_k
    import random; random.seed(k)
    u = [Fr(random.randint(-9, 9)) for _ in range(N // 2)]
    v = [sum(M[i][j] * u[j] for j in range(N // 2)) for i in range(N // 2)]
    f = [0] * N
    for j, e in enumerate(E): f[e] = u[j]
    for i, y in enumerate(O): f[y] = v[i]
    inS = all(sum(f[y] * (-1) ** pc(x & y) for y in range(N)) == 0 for x in range(N) if pc(x) > r)
    energy = sum(a * a for a in u) == sum(a * a for a in v)
    print("k", k, "N", N, "| characters of weight <= k/2 on the even points form a Hadamard matrix of order N/2:", had,
          "| M orthogonal:", orth, "| M depends on distance only:", radial)
    print("   kernel by distance:", {w: str(ker[w]) for w in sorted(ker)})
    print("   relabelled M symmetric:", sym, "| M^2 = 1:", inv, "| trace", tr, "= N/2 - 2*(high characters of the (k-1)-cube) =", N // 2 - 2 * high,
          "| M = transform * majority sign * inverse transform:", same, "(or its negative:", neg, ")")
    print("   random even-point data extended by M lies in S_k:", inS, "| energy on even points = energy on odd points:", energy)
    print("   nonzero entries of M:", sum(1 for row in M for v_ in row if v_ != 0), "of", (N // 2) ** 2)
