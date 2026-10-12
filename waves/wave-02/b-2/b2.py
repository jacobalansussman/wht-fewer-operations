# b2.py (critic b-2): exact checks of e-7's "slack law" (Lemma 4) with my own code.  Integer / rational arithmetic only,
# except the two rank lower bounds marked "mod p" (a rank modulo a prime never exceeds the true rank, so it is a valid LOWER bound).
import sys, math
from fractions import Fraction as Fr
def par(x): return bin(x).count("1") & 1
def Hm(n): return [[-1 if par(i & j) else 1 for j in range(n)] for i in range(n)]
def reduce(v, basis):
    v = v[:]
    for p, b in basis:
        if v[p]:
            f, g = v[p], b[p]
            v = [g * vi - f * bi for vi, bi in zip(v, b)]
    g = 0
    for x in v: g = math.gcd(g, x)
    if g == 0: return None
    return [x // g for x in v]
def piv(v): return next(i for i, x in enumerate(v) if x)
def rank_int(rows):
    basis = []
    for r in rows:
        v = reduce(list(r), basis)
        if v is not None: basis.append((piv(v), v))
    return len(basis)
def kdim_table(C, N):
    """for every subset T of the N columns of the integer matrix C: dim{w supported on T : C w = 0} = |T| - rank(C[:,T])"""
    cols = [[C[i][y] for i in range(len(C))] for y in range(N)]
    tab = [0] * (1 << N); basis = []
    def go(i, mask, cnt):
        if i == N: tab[mask] = cnt - len(basis); return
        go(i + 1, mask, cnt)
        v = reduce(cols[i], basis)
        if v is None: go(i + 1, mask | (1 << i), cnt + 1)
        else:
            basis.append((piv(v), v)); go(i + 1, mask | (1 << i), cnt + 1); basis.pop()
    go(0, 0, 0); return tab
def null_vec(C, T):
    """the (unique up to scale) integer w supported on T with C w = 0, when that space has dimension 1"""
    rows = [[Fr(C[i][y]) for y in T] for i in range(len(C))]; t = len(T); pv = []; r = 0
    for c in range(t):
        p = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]; d = rows[r][c]; rows[r] = [x / d for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]; rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        pv.append(c); r += 1
    free = [c for c in range(t) if c not in pv]; assert len(free) == 1
    w = [Fr(0)] * t; w[free[0]] = Fr(1)
    for row, pc in zip(rows[:r], pv): w[pc] = -row[free[0]]
    L = 1
    for x in w: L = L * x.denominator // math.gcd(L, x.denominator)
    return [int(x * L) for x in w]
def sparsest_basis(C, N, tab=None):
    """exact sparsest basis of {w : C w = 0} in R^N: greedy over ALL vectors of minimal support (Coleman-Pothen: greedy is optimal)"""
    if tab is None: tab = kdim_table(C, N)
    dim = tab[(1 << N) - 1]
    el = [m for m in range(1, 1 << N) if tab[m] == 1 and all(tab[m & ~(1 << i)] == 0 for i in range(N) if m >> i & 1)]
    el.sort(key=lambda m: (bin(m).count("1"), m)); basis = []; out = []
    for m in el:
        T = [i for i in range(N) if m >> i & 1]; w = null_vec(C, T); v = [0] * N
        for i, x in zip(T, w): v[i] = x
        red = reduce(v, basis)
        if red is not None:
            basis.append((piv(red), red)); out.append(v)
            if len(out) == dim: break
    return out, tab, len(el)
def stats(vecs, N):
    rw = [sum(1 for v in vecs if v[x]) for x in range(N)]; cw = sorted(sum(1 for x in v if x) for v in vecs)
    return sum(cw), max(rw), cw
def matI(n, s): return [[(s if i == j else 0) for j in range(n)] for i in range(n)]
def add(X, Y): return [[a + b for a, b in zip(r, q)] for r, q in zip(X, Y)]
def relabelled(N):
    j = (N.bit_length() - 1) // 2; sw = [0, 2, 1, 3]; H = Hm(N)
    def f(y):
        o = 0
        for d in range(j): o |= sw[(y >> (2 * d)) & 3] << (2 * d)
        return o
    return [[H[x][f(y)] for y in range(N)] for x in range(N)]
def chain_bound(N, m, dminus, improved):
    """lower bound on nnz(A) from the chain: the t lightest columns touch a set T with  t - r <= cap(|T|)"""
    r = m - dminus; best = (0, 0)
    def cap(T):
        c = Fr(T * T, N)
        if improved: c = min(c, dminus - (N - T) + Fr((N - T) ** 2, N))
        return c
    for t in range(max(r, 0) + 1, m + 1):
        T = next(T for T in range(0, N + 1) if cap(T) >= t - r)
        b = -(-m * T // t)
        if b > best[0]: best = (b, t)
    return best
print("=== 1. the two ingredients, exhaustively over all subsets T, N = 4 and 16 ===")
keep = {}
for N in (4, 16):
    s = math.isqrt(N)
    for name, M in (("identity remainder (M = H)", Hm(N)), ("best relabelling (M = H Q^T)", relabelled(N))):
        sym = all(M[x][y] == M[y][x] for x in range(N) for y in range(N))
        sq = all(sum(M[x][z] * M[z][y] for z in range(N)) == (N if x == y else 0) for x in range(N) for y in range(N))
        dminus = rank_int(add(M, matI(N, -s)))      # rank(M - sI) = dimension of the -s eigenspace = rank(H - S)
        Cm = add(M, matI(N, s))                     # (M + sI) w = 0  <=>  w in E_minus
        tab = kdim_table(Cm, N); viol1 = viol2 = 0; mx = [0] * (N + 1)
        for mask in range(1 << N):
            t = bin(mask).count("1"); j = tab[mask]; mx[t] = max(mx[t], j)
            if j * N > t * t: viol1 += 1
            if (j - dminus + (N - t)) * N > (N - t) ** 2: viol2 += 1
        print(f"N={N} {name}: symmetric {sym}, M^2 = N*I {sq}, rank(H-S) = dim E_minus = {dminus}")
        print(f"   subsets violating  dim <= |T|^2/N : {viol1} of {1<<N};  violating my sharper  dim <= dimE - s + s^2/N (s = N-|T|): {viol2}")
        print("   |T| : largest dim found / floor(|T|^2/N) / floor(sharper) :", " ".join(f"{t}:{mx[t]}/{t*t//N}/{min(t*t//N, (dminus*N - (N-t)*N + (N-t)**2)//N)}" for t in range(N + 1)))
        bas, _, nel = sparsest_basis(Cm, N, tab); nz, rwmax, cw = stats(bas, N)
        keep[(N, name[:3])] = bas
        for rho_m in ((N // 2),):
            if dminus <= rho_m:
                lb = chain_bound(N, rho_m, dminus, False); lb2 = chain_bound(N, rho_m, dminus, True)
                print(f"   middle of {rho_m} numbers: slack r = {rho_m - dminus}; e-7's chain forces nnz(A) >= {lb[0]} (at t = {lb[1]} columns), sharper chain >= {lb2[0]}")
        print(f"   EXACT sparsest basis of E_minus itself ({nel} minimal-support vectors examined): column weights {cw}, total {nz} = {Fr(nz, N)} per row on average, max per row {rwmax}")
print()
print("=== 2. the door, A-side only: a 3N/4-dimensional space V containing E_minus(H_N), spanned by sparse vectors ===")
def eig_bases(n):
    s = math.isqrt(n); H = Hm(n)
    bm, _, _ = sparsest_basis(add(H, matI(n, s)), n); bp, _, _ = sparsest_basis(add(H, matI(n, -s)), n)
    return bm, bp
EB = {4: eig_bases(4), 16: eig_bases(16)}
print("sparsest bases: E_minus(4)", EB[4][0], " E_plus(4)", EB[4][1], "; E_minus(16) column weights", stats(EB[16][0], 16)[2], " E_plus(16)", stats(EB[16][1], 16)[2])
def rank_mod(rows, p=(1 << 61) - 1):
    rows = [[x % p for x in r] for r in rows]; r = 0; nc = len(rows[0])
    for c in range(nc):
        q = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if q is None: continue
        rows[r], rows[q] = rows[q], rows[r]; inv = pow(rows[r][c], p - 2, p); pr = rows[r]
        for i in range(r + 1, len(rows)):
            if rows[i][c]:
                f = rows[i][c] * inv % p; ri = rows[i]
                for k in range(c, nc):
                    if pr[k]: ri[k] = (ri[k] - f * pr[k]) % p
        r += 1
    return r
def door(n1, n2):
    N = n1 * n2; s = math.isqrt(N); bm1, bp1 = EB[n1]; bm2, bp2 = EB[n2]
    # complement of E_minus(n1) by unit vectors
    basis = []
    for b in bm1:
        v = reduce(b, basis); basis.append((piv(v), v))
    X = []
    for x in range(n1):
        e = [0] * n1; e[x] = 1; v = reduce(e, basis)
        if v is not None: basis.append((piv(v), v)); X.append(x)
    assert len(X) == n1 // 2
    cols = []
    for b in bm1:
        for y in range(n2):
            v = [0] * N
            for x in range(n1):
                if b[x]: v[x * n2 + y] = b[x]
            cols.append(v)
    for x in X:
        for b in bm2:
            v = [0] * N
            for y in range(n2):
                if b[y]: v[x * n2 + y] = b[y]
            cols.append(v)
    K = [[a * b for a in k1 for b in k2] for k1 in bp1 for k2 in bp2]
    H = Hm(N)
    okK = all([sum(H[x][y] * k[y] for y in range(N)) for x in range(N)] == [s * a for a in k] for k in K)   # K inside E_plus, exactly
    okA = all(sum(a * b for a, b in zip(c, k)) == 0 for c in cols for k in K)                                 # every column of A orthogonal to K, exactly
    rk = rank_mod(cols); rkK = rank_mod(K)
    nz, rwmax, cw = stats(cols, N)
    print(f"N={N} = {n1} x {n2}: A has {len(cols)} columns (3N/4 = {3*N//4}); K = E_plus({n1}) (x) E_plus({n2}) has {len(K)} vectors, rank mod p >= {rkK}; H k = sqrt(N) k exactly: {okK}; A^T k = 0 exactly: {okA}; rank(A) mod p >= {rk}")
    print(f"   => col(A) = orthogonal complement of K, which contains E_minus(H_{N}).  nnz(A) = {nz} = {nz/N:.3f} per row on average, max per row {rwmax}, column weights from {cw[0]} to {cw[-1]};  Lemma 4 allows 0.75 per row")
    return nz
door(4, 4)
if len(sys.argv) > 1:
    door(4, 16); door(16, 4); door(16, 16)
