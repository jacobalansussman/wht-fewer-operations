# 16 points, exact.  Class: a symmetric form M of the transform (M = signed relabelling of H16/4, M^2 = I) written as a product of
# COMMUTING reflections along mutually orthogonal vectors with entries 0, +1, -1.  A reflection along such a vector of support q costs
# (q-1) additions + 1 scaling + q subtractions = 2q in count (O), 2q-1 in count (G) (support 2 = signed swap = free).
# For each form: list every 0/+-1 vector of the (-1)-eigenspace U, then the orthogonal bases of U of least total support.
import sys, itertools
from fractions import Fraction as Fr
N = 16
H = [[(-1) ** bin(a & b).count("1") for b in range(N)] for a in range(N)]
def bit(v, k): return (v >> k) & 1
def bent():
    f = lambda v: (bit(v, 0) & bit(v, 1)) ^ (bit(v, 2) & bit(v, 3))
    sw = lambda v: (bit(v, 1)) | (bit(v, 0) << 1) | (bit(v, 3) << 2) | (bit(v, 2) << 3)
    return [[(-1) ** f(a) * H[a][sw(b)] * (-1) ** f(b) for b in range(N)] for a in range(N)]
def grover():
    r = [[(1 if i != j else -1) for j in range(4)] for i in range(4)]   # J - 2I
    return [[r[a // 4][b // 4] * r[a % 4][b % 4] for b in range(N)] for a in range(N)]
def eigspace(M, lam):
    A = [[Fr(M[i][j] - (lam if i == j else 0)) for j in range(N)] for i in range(N)]
    piv = []; r = 0
    for c in range(N):
        p = next((i for i in range(r, N) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]; x = A[r][c]; A[r] = [a / x for a in A[r]]
        for i in range(N):
            if i != r and A[i][c] != 0:
                y = A[i][c]; A[i] = [a - y * b for a, b in zip(A[i], A[r])]
        piv.append(c); r += 1
    free = [c for c in range(N) if c not in piv]
    basis = []
    for fcol in free:
        v = [Fr(0)] * N; v[fcol] = Fr(1)
        for i, c in enumerate(piv): v[c] = -A[i][fcol]
        basis.append(v)
    return basis, free
def study(name, M, lam):
    sym = all(M[i][j] == M[j][i] for i in range(N) for j in range(N))
    sq = all(sum(M[i][k] * M[k][j] for k in range(N)) == (16 if i == j else 0) for i in range(N) for j in range(N))
    basis, free = eigspace(M, lam); d = len(basis)
    vecs = set()
    for co in itertools.product((0, 1, -1), repeat=d):
        if not any(co): continue
        v = [sum(c * b[j] for c, b in zip(co, basis)) for j in range(N)]
        if all(x in (0, 1, -1) for x in v):
            v = tuple(int(x) for x in v)
            if next(x for x in v if x) < 0: v = tuple(-x for x in v)
            vecs.add(v)
    vecs = sorted(vecs, key=lambda v: (sum(map(abs, v)), v))
    hist = {}
    for v in vecs: hist[sum(map(abs, v))] = hist.get(sum(map(abs, v)), 0) + 1
    print("%s: symmetric=%s square=16I=%s diag=%s ; eigenvalue %d space has dimension %d ; 0/+-1 vectors in it by support: %s"
          % (name, sym, sq, sorted(set(M[i][i] for i in range(N))), lam, d, sorted(hist.items())))
    orth = lambda u, v: sum(a * b for a, b in zip(u, v)) == 0
    best = [10 ** 9, None]; cnt = [0]
    sup = [sum(map(abs, v)) for v in vecs]
    def dfs(start, chosen, tot):
        cnt[0] += 1
        if len(chosen) == d:
            if tot < best[0]: best[0] = tot; best[1] = list(chosen)
            return
        need = d - len(chosen)
        for i in range(start, len(vecs)):
            if tot + need * sup[i] >= best[0]: break
            if all(orth(vecs[i], c) for c in chosen):
                chosen.append(vecs[i]); dfs(i + 1, chosen, tot + sup[i]); chosen.pop()
    dfs(0, [], 0)
    if best[1] is None: print("   no orthogonal basis of 0/+-1 vectors"); return
    paid = sum(s for s in map(lambda v: sum(map(abs, v)), best[1]) if s > 2)
    print("   least total support of an orthogonal 0/+-1 basis: %d (supports %s) -> count (O) = %d, count (G) = %d ; nodes %d"
          % (best[0], [sum(map(abs, v)) for v in best[1]], 2 * paid, sum(2 * sum(map(abs, v)) - 1 for v in best[1] if sum(map(abs, v)) > 2), cnt[0]))
    for v in best[1]: print("     ", v)
    sys.stdout.flush()
B = bent(); G = grover()
study("bent form, (-4)-eigenspace", B, -4)
study("Grover form (J-2I)x(J-2I), (-4)-eigenspace", G, -4)
study("Sylvester form H16, (-4)-eigenspace", H, -4)
study("Sylvester form H16, (+4)-eigenspace", H, 4)
