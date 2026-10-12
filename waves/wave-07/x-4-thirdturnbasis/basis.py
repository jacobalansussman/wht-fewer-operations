# x-4 thirdturn-basis, experiment 1. Exact (whole numbers and fractions only).
# Addresses x in F_2^(2n); Q(x) = x1x2 + x3x4 + ...; B(x,y) = Q(x+y)+Q(x)+Q(y) (the pairing);
# H(x,y) = (-1)^B(x,y) (the transform with the two bits of each pair exchanged in the output address);
# D = diag (-1)^Q; s = sqrt(N); R = D H / s.
import sys, itertools
from fractions import Fraction as Fr

def pop(v): return bin(v).count('1')

def rank_int(rows):
    """exact rank over the rationals (fraction elimination)"""
    M = [[Fr(v) for v in r] for r in rows]
    rk = 0; ncol = len(M[0]) if M else 0
    for c in range(ncol):
        p = None
        for i in range(rk, len(M)):
            if M[i][c] != 0: p = i; break
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        pv = M[rk][c]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c] / pv
                M[i] = [a - f*b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk

def mul(A, B):
    n = len(A); m = len(B[0]); Bt = list(zip(*B))
    return [[sum(a*b for a, b in zip(row, col)) for col in Bt] for row in A]

def run(n):
    k = 2*n; N = 1 << k; s = 1 << n
    def Q(x): return sum(((x >> (2*i)) & 1) & ((x >> (2*i+1)) & 1) for i in range(n)) & 1
    def Bf(x, y): return (Q(x ^ y) + Q(x) + Q(y)) & 1
    H = [[(-1)**Bf(x, y) for y in range(N)] for x in range(N)]
    d = [(-1)**Q(x) for x in range(N)]
    print('=== N = %d, s = %d ===' % (N, s))
    # --- (0) S3 facts
    DH = [[d[x]*H[x][y] for y in range(N)] for x in range(N)]
    HD = [[H[x][y]*d[y] for y in range(N)] for x in range(N)]
    DH2 = mul(DH, DH)
    DH3 = mul(DH2, DH)
    print('(DH)^3 = s^3 I:', all(DH3[i][j] == (s**3 if i == j else 0) for i in range(N) for j in range(N)))
    # K = off-diagonal part (the part of H that anticommutes with D);  claim  s H = N D + s K - 2 D K^2
    K = [[H[x][y] if d[x] != d[y] else 0 for y in range(N)] for x in range(N)]
    K2 = mul(K, K)
    ok = all(s*H[x][y] == (N*d[x] if x == y else 0) + s*K[x][y] - 2*d[x]*K2[x][y] for x in range(N) for y in range(N))
    print('identity  H = s D + K - (2/s) D K^2  (K = H with the two diagonal blocks set to 0):', ok)
    # Cayley: A = (DH - HD)/s ; (1 - A) R = 1 + A  <=>  (s I - (DH-HD)) DH = s (s I + DH - HD)
    Am = [[DH[x][y] - HD[x][y] for y in range(N)] for x in range(N)]
    L = mul([[(s if x == y else 0) - Am[x][y] for y in range(N)] for x in range(N)], DH)
    ok = all(L[x][y] == s*((s if x == y else 0) + Am[x][y]) for x in range(N) for y in range(N))
    print('Cayley form  R = (1 + A)(1 - A)^-1 with A = R - R^T (entries 0, +-2/s, zero inside each side of the quadric):', ok)
    # chirp: H(x,y) = d(x) chi(x+y) d(y)
    print('Bluestein form  H(x,y) = (-1)^Q(x) (-1)^Q(x+y) (-1)^Q(y):', all(H[x][y] == d[x]*d[x ^ y]*d[y] for x in range(N) for y in range(N)))
    # --- (i) totally singular subspaces of s addresses ("Lagrangian", Q = 0 on all of it)
    sing = [x for x in range(1, N) if Q(x) == 0]
    subs = set()
    def close(gens):
        S = {0}
        for g in gens: S |= {a ^ g for a in S}
        return frozenset(S)
    def grow(gens, S):
        if len(gens) == n: subs.add(S); return
        for v in sing:
            if v in S: continue
            if all(Bf(v, g) == 0 for g in gens):
                S2 = frozenset(S | {a ^ v for a in S})
                if all(Q(a) == 0 for a in S2): grow(gens + [v], S2)
    grow([], frozenset({0}))
    subs = sorted(subs, key=sorted)
    ind = [[1 if x in S else 0 for x in range(N)] for S in subs]
    fixed_ok = all(all(sum(H[x][y]*v[y] for y in range(N)) == s*v[x] for x in range(N)) for v in ind)
    r_ind = rank_int(ind)
    t_dim = (s+1)*(s+2)//6; g_dim = (s-1)*(s-2)//6; m_dim = (N-1)//3
    print('totally singular subspaces of %d addresses: %d ; each indicator fixed by R: %s ; rank of their span: %d ; fixed space on Q=0 has dimension %d'
          % (s, len(subs), fixed_ok, r_ind, t_dim))
    # add delta-free candidates: the other fixed vectors on Q=0, signed indicators (-1)^Q(l) on a coset d0+L of a NON-singular
    # self-orthogonal subspace L (B = 0 on L, Q linear on L, Q(l) = B(l,d0), Q(d0) = 0)
    # enumerate all self-orthogonal subspaces of size s
    allL = set()
    def growL(gens, S):
        if len(gens) == n: allL.add(S); return
        for v in range(1, N):
            if v in S: continue
            if all(Bf(v, g) == 0 for g in gens):
                growL(gens + [v], frozenset(S | {a ^ v for a in S}))
    if n <= 2:
        growL([], frozenset({0}))
    else:
        # N = 64: 135 self-orthogonal planes; enumerate by increasing generators to keep it short
        def growL2(gens, S, lo):
            if len(gens) == n: allL.add(S); return
            for v in range(lo, N):
                if v in S: continue
                if all(Bf(v, g) == 0 for g in gens):
                    growL2(gens + [v], frozenset(S | {a ^ v for a in S}), v + 1)
        growL2([], frozenset({0}), 1)
    extra = []
    for S in allL:
        if all(Q(a) == 0 for a in S): continue
        # find d0 with Q(l) = B(l,d0) for all l in S
        for d0 in range(N):
            if all(Q(l) == Bf(l, d0) for l in S):
                if Q(d0) == 0:
                    v = [0]*N
                    for l in S: v[l ^ d0] = (-1)**Q(l)
                    extra.append(v)
                break
    ok2 = all(all(sum(H[x][y]*v[y] for y in range(N)) == s*v[x] for x in range(N)) and all(v[x] == 0 or d[x] == 1 for x in range(N)) for v in extra)
    print('self-orthogonal subspaces of %d addresses: %d ; signed coset indicators on Q=0 from the non-singular ones: %d, all fixed by R: %s ; rank of singular + signed together: %d'
          % (s, len(allL), len(extra), ok2, rank_int(ind + extra) if (ind + extra) else 0))
    # --- (ii) the fixed vectors on Q = 1 (the "sign" part): pull back the alternating sum over a 6-orbit of (a,b)->(b,a+b), swap
    # exact: the fixed space on Q=1 = kernel of (H + s) on vectors supported on Q=1; find its dimension and the least support
    S1 = [x for x in range(N) if Q(x) == 1]; S0 = [x for x in range(N) if Q(x) == 0]
    M11 = [[H[x][y] + (s if x == y else 0) for y in S1] for x in S1]
    M00 = [[H[x][y] - (s if x == y else 0) for y in S0] for x in S0]
    print('points with Q=0: %d, Q=1: %d ; fixed on Q=0: %d (formula (s+1)(s+2)/6 = %d) ; fixed on Q=1: %d (formula (s-1)(s-2)/6 = %d) ; coupled pairs: (N-1)/3 = %d'
          % (len(S0), len(S1), len(S0) - rank_int(M00), t_dim, len(S1) - rank_int(M11), g_dim, m_dim))
    C = [[H[x][y] for y in S0] for x in S1]
    print('cross block C (Q=1 rows, Q=0 columns): %d x %d, rank %d' % (len(S1), len(S0), rank_int(C)))
    return H, d, subs

for n in (1, 2, 3):
    run(n)
