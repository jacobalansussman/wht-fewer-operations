#!/usr/bin/env python3
"""d-4-codes play 2 (exact integers).
The trace-maximal form of the transform is the symplectic Fourier transform S(p,y) = (-1)^{w(p,y)}, w the standard
alternating form on 2j bits. Check at N = 4, 16, 64, 256:
 1. S is symmetric with diagonal +1; for every quadratic form Q with polar form w, (-1)^Q is an eigenvector,
    eigenvalue +sqrt(N) if Q is hyperbolic (Arf 0), -sqrt(N) if elliptic (Arf 1); counts N/2 +- sqrt(N)/2.
 2. S = sqrt(N) * (I - (2/N) * sum over elliptic Q of v_Q v_Q^T)   (exact, integers: N*S = sqrt(N)*(N I - 2 sum)).
 3. With T = diag((-1)^Q0), Q0 hyperbolic: (T S)^3 = N^(3/2) I  (S/sqrt(N) and T generate the symmetric group S_3).
 4. Supports: the smallest support of a vector in the (-sqrt N)-eigenspace found among code atoms.
"""
import sys
pc = lambda x: bin(x).count("1")
def run(j):
    k = 2 * j; N = 1 << k; r = 1 << j
    lo = (1 << j) - 1
    def w(p, y):   # p = (p1,p2), y = (y1,y2): p1.y2 + p2.y1
        return (pc((p >> j) & (y & lo)) + pc((p & lo) & (y >> j))) & 1
    def Q0(x): return pc((x >> j) & (x & lo)) & 1
    S = [[-1 if w(p, y) else 1 for y in range(N)] for p in range(N)]
    assert all(S[p][p] == 1 for p in range(N)) and all(S[p][y] == S[y][p] for p in range(N) for y in range(N))
    ell = []; hyp = []
    for a in range(N):
        v = [-1 if (Q0(x) ^ w(a, x)) else 1 for x in range(N)]
        Sv = [sum(s * t for s, t in zip(S[y], v)) for y in range(N)]
        if Sv == [r * t for t in v]: hyp.append((a, v))
        elif Sv == [-r * t for t in v]: ell.append((a, v))
        else: raise SystemExit("not an eigenvector")
    ok_arf = all(Q0(a) == 1 for a, _ in ell) and all(Q0(a) == 0 for a, _ in hyp)
    print("N=%3d: hyperbolic forms %3d (= N/2+sqrtN/2 = %d), elliptic %3d (= N/2-sqrtN/2 = %d); elliptic <=> Q0(a)=1: %s" % (
        N, len(hyp), N // 2 + r // 2, len(ell), N // 2 - r // 2, ok_arf))
    if N <= 64:
        # reflection identity: N*S == r*(N*I - 2*sum v v^T)
        ok = True
        for p in range(N):
            for y in range(N):
                tot = sum(v[p] * v[y] for _, v in ell)
                if N * S[p][y] != r * ((N if p == y else 0) - 2 * tot): ok = False
        # (T S)^3
        T = [(-1) ** Q0(x) for x in range(N)]
        M = [[T[p] * S[p][y] for y in range(N)] for p in range(N)]
        def mm(A, B): return [[sum(A[i][t] * B[t][q] for t in range(N)) for q in range(N)] for i in range(N)]
        M3 = mm(mm(M, M), M)
        ok3 = all(M3[p][y] == (r ** 3 if p == y else 0) for p in range(N) for y in range(N))
        tr = sum(M[p][p] for p in range(N))
        print("       S = sqrtN (I - (2/N) sum_elliptic v v^T): %s ;  (T S)^3 = N^(3/2) I: %s ; trace(TS)/sqrtN = %s ; standard irreps (N-1)/3 = %d" % (
            ok, ok3, tr / r, (N - 1) // 3))
for j in (1, 2, 3, 4): run(j)
# the 120 labels: even-weight words of length 9 with weight = 2 mod 4, and the 'know' relation
L = [x for x in range(512) if pc(x) % 4 == 2]
print("even-weight words of length 9 with weight 2 mod 4:", len(L), " by weight:", {wt: sum(1 for x in L if pc(x) == wt) for wt in (2, 6)})
deg = sorted(set(sum(1 for y in L if y != x and pc(x & y) % 2 == 0) for x in L))
print("each such word has even overlap with %s others (E8: each root is orthogonal to 126 roots = 63 pairs)" % deg)
