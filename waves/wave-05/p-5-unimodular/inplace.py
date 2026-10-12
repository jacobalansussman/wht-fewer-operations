# inplace.py: two plays with IN-PLACE circuits of bounded coefficients (a move: row_i <- row_i + s*row_j, s = +1 or -1; no extra value).
# The state is an integer matrix of determinant +-1. Meter: Phi(M) = - sum_il p_il log2|p_il|, p_il = M_il * (M^-1)_li
# (each row of p sums to 1; Phi is additive under Kronecker products; for a unitary M it is Ailon's entropy).
import sys, itertools, time
from fractions import Fraction as Fr
from math import log2
def inv(M):
    n = len(M); A = [[Fr(x) for x in r] + [Fr(int(i == j)) for j in range(n)] for i, r in enumerate(M)]
    for c in range(n):
        p = next(i for i in range(c, n) if A[i][c] != 0); A[c], A[p] = A[p], A[c]
        A[c] = [x / A[c][c] for x in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0: f = A[i][c]; A[i] = [x - f*y for x, y in zip(A[i], A[c])]
    return [r[n:] for r in A]
def phi(M):
    I = inv(M); n = len(M); s = 0.0; l1 = 0
    for i in range(n):
        for l in range(n):
            p = M[i][l] * I[l][i]
            if p != 0: s -= float(p) * log2(abs(p)); l1 += abs(p)
    return s, l1
def canon(M):  # rows up to sign and order
    rows = []
    for r in M:
        f = next(x for x in r if x); rows.append(r if f > 0 else tuple(-x for x in r))
    return tuple(sorted(rows))
def moves(M):
    n = len(M)
    for i in range(n):
        for j in range(n):
            if i != j:
                for s in (1, -1):
                    R = list(M); R[i] = tuple(a + s*b for a, b in zip(M[i], M[j])); yield tuple(R)
# play 1: the largest |Phi| reachable with m moves on 3 wires
n = 3; I3 = tuple(tuple(int(i == j) for j in range(n)) for i in range(n))
seen = {canon(I3)}; level = [I3]; t0 = time.time()
print("3 wires, moves +-1: m, states new at depth m, max |Phi|, max |Phi|/m, max sum|p|, an extremal matrix")
for m in range(1, int(sys.argv[1]) + 1):
    nxt = []
    for M in level:
        for R in moves(M):
            c = canon(R)
            if c not in seen: seen.add(c); nxt.append(c)
    level = nxt; best = (0, None); bl = 0
    for M in level:
        f, l1 = phi(M)
        if abs(f) > abs(best[0]): best = (f, M)
        bl = max(bl, l1)
    print("  m=%d new=%d max|Phi|=%.3f per move %.3f  max sum|p|=%s  %s  (%.0fs)" % (m, len(level), abs(best[0]), abs(best[0]) / m, bl, best[1], time.time() - t0), flush=True)
# play 2: K(x)K in place on 4 wires, meet in the middle. textbook: 8 moves.
def kron(A, B): return tuple(tuple(x*y for x in ra for y in rb) for ra in A for rb in B)
for nm, K in [("K=[[1,1],[1,2]]", ((1,1),(1,2)))]:
    T = canon(kron(K, K)); I4 = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))
    print(nm, "second power: Phi = %.1f, sum|p| = %s" % phi(kron(K, K)))
    F = {canon(I4): 0}; lev = [canon(I4)]
    for d in range(1, 5):
        nx = []
        for M in lev:
            for R in moves(M):
                c = canon(R)
                if c not in F: F[c] = d; nx.append(c)
        lev = nx
    B = {T: 0}; lev = [T]
    for d in range(1, 4):
        nx = []
        for M in lev:
            for R in moves(M):
                c = canon(R)
                if c not in B: B[c] = d; nx.append(c)
        lev = nx
    meet = [F[c] + B[c] for c in B if c in F]
    print("  forward states (<=4 moves): %d, backward (<=3): %d; least moves found: %s  (no meeting means at least 8 moves in place with +-1)" % (len(F), len(B), min(meet) if meet else "none <= 7"))
    # the meter along the textbook in-place program
    M = [list(r) for r in I4]; seq = [(1,0),(0,1)] ; prog = []
    # block on bit 0: pairs (0,1),(2,3); bit 1: pairs (0,2),(1,3).  K block in place: a <- a + b ; b <- b + a  gives (a+b, a+2b): rows of K up to order
    for (a, b) in [(0,1),(2,3),(0,2),(1,3)]: prog += [(a, b), (b, a)]
    out = []
    for (i, j) in prog:
        M[i] = [x + y for x, y in zip(M[i], M[j])]; out.append("%.2f" % phi(tuple(map(tuple, M)))[0])
    print("  textbook in place, Phi after each of the 8 moves:", " ".join(out), "; ends at K(x)K up to row order:", canon(tuple(map(tuple, M))) == T)
