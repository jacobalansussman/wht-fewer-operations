#!/usr/bin/env python3
"""Triangular factorisations of the Walsh-Hadamard matrix under re-orderings of rows and columns.
H[rows][cols] = L * U exactly (Fractions), L unit lower triangular, U upper triangular.
A triangular matrix is invisible to the entropy potential (its leverage matrix M o M^-T is the identity),
so every such factorisation is a program whose first factor carries no potential at all.
Proxy for cost (count G): (nonzeros of L - N) + (nonzeros of U - N).  The textbook is N*log2(N)."""
import sys, random
from fractions import Fraction as F
k = int(sys.argv[1]); trials = int(sys.argv[2]); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
N = 1 << k
H = [[(-1) ** bin(w & x).count('1') for x in range(N)] for w in range(N)]
def lu(rows, cols):
    A = [[F(H[r][c]) for c in cols] for r in rows]
    L = [[F(int(i == j)) for j in range(N)] for i in range(N)]
    for j in range(N):
        if A[j][j] == 0:
            return None
        for i in range(j + 1, N):
            if A[i][j] != 0:
                m = A[i][j] / A[j][j]
                L[i][j] = m
                Ai, Aj = A[i], A[j]
                for c in range(j, N):
                    Ai[c] -= m * Aj[c]
    return L, A
def stats(L, U):
    nl = sum(1 for i in range(N) for j in range(N) if L[i][j] != 0)
    nu = sum(1 for i in range(N) for j in range(N) if U[i][j] != 0)
    vals = sorted({abs(v) for M in (L, U) for row in M for v in row if v != 0})
    return nl, nu, vals
nat = list(range(N))
L, U = lu(nat, nat)
nl, nu, vals = stats(L, U)
print(f"N={N} natural order: nnz L {nl} nnz U {nu} proxy gates {nl+nu-2*N} textbook {N*k} distinct |entries| {[str(v) for v in vals]}")
rng = random.Random(seed)
best = None; hist = {}; fails = 0
for t in range(trials):
    r = nat[:]; c = nat[:]; rng.shuffle(r); rng.shuffle(c)
    res = lu(r, c)
    if res is None:
        fails += 1; continue
    nl, nu, vals = stats(*res)
    g = nl + nu - 2 * N
    hist[g] = hist.get(g, 0) + 1
    if best is None or g < best[0]:
        best = (g, r, c, nl, nu, [str(v) for v in vals])
print("orders tried", trials, "with a vanishing leading minor", fails)
print("histogram of proxy gate count:", sorted(hist.items()))
print("best:", best)
if best:
    L, U = lu(best[1], best[2])
    print("L of best:"); [print("  ", [str(v) for v in row]) for row in L]
    print("U of best:"); [print("  ", [str(v) for v in row]) for row in U]
