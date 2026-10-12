#!/usr/bin/env python3
"""paul.py -- Paul's batch discount made explicit, count (G).  [e2-2-ladder, 2026-10-10]   Exact integers.

Task: n copies of a typical n x n matrix A = the product A X for an n x n array X, A known in advance.
Count (G): a gate is any a*u + b*v; multiplying by a known number is free.  So only additions cost:
  the sums of blocks of A are free (A is known), a 1 x 1 product is free.
Separate copies.  One copy of a typical A: at most n(n-1) gates (each output is a chain of n-1 gates);
  at least (n-1)^2 [derived: a gate has one free ratio after scaling, outputs and inputs can be rescaled for free
  (2n-1 parameters), and a typical A has n^2 independent entries; a count of parameters, not a proof read by anyone].
Strassen with A fixed, one level: 7 products of half size; additions on the X side and after the products only.
  Strassen 1969: 5 sums of blocks of X (B11+B22, B12-B22, B21-B11, B11+B12, B21+B22) and 8 additions afterwards
  = 13 (n/2)^2 gates.  Winograd's variant: 4 + 7 = 11 (n/2)^2 gates.
T(n) = min( n * n(n-1),  7 T(n/2) + g (n/2)^2 ).
"""
def table(g):
    T = {1: 0}
    pure = {1: 0}
    rows = []
    n = 1
    while n < 4096:
        n *= 2
        naive_hi = n * n * (n - 1)
        naive_lo = n * (n - 1) ** 2
        rec = 7 * T[n // 2] + g * (n // 2) ** 2
        pure[n] = 7 * pure[n // 2] + g * (n // 2) ** 2
        T[n] = min(naive_hi, rec)
        rows.append((n, naive_lo, naive_hi, pure[n], rec, T[n]))
    return rows

for g, name in ((13, "Strassen 1969"), (11, "Winograd's variant")):
    print("== %s: %d additions of half-size blocks per level" % (name, g))
    print("%6s %16s %16s %18s %18s %10s %10s" % ("n", "separate, lower", "separate, upper", "recipe down to 1x1", "recipe, best cut", "theta_lo", "theta_hi"))
    first = None
    for n, lo, hi, pure, rec, best in table(g):
        tl, th = best / hi, best / lo
        print("%6d %16d %16d %18d %18d %10.4f %10.4f" % (n, lo, hi, pure, best, tl, th))
        if first is None and best < lo:
            first = n
    print("first n at which the batch is below the LOWER count of n separate copies: %s" % first)
    print()

print("== the transform in the same recipe (derived by hand, see e2-2.md section 4)")
print("left factors of Strassen's seven products on [[H,H],[H,-H]]: 2H? no: H+(-H)=0 ... three vanish, four are multiples of H  [j-manyatonce]")
print("left factors on the 4-point brick 2I - J split into 2 x 2 blocks A11 = A22 = [[1,-1],[-1,1]], A12 = A21 = -J:")
import itertools
from fractions import Fraction as Fr
A11 = [[1, -1], [-1, 1]]; A22 = A11; A12 = [[-1, -1], [-1, -1]]; A21 = A12
def add(P, Q, s=1): return [[P[i][j] + s * Q[i][j] for j in range(2)] for i in range(2)]
def kind(Mx):
    det = Mx[0][0] * Mx[1][1] - Mx[0][1] * Mx[1][0]
    nz = sum(1 for r in Mx for x in r if x)
    if nz == 0: return "zero (free)"
    if det == 0: return "rank one: 1 gate per column"
    if nz == 2: return "a signed permutation with scaling (free)"
    if nz == 3: return "triangular: 1 gate per column"
    return "full: 2 gates per column"
fac = [("A11+A22", add(A11, A22)), ("A21+A22", add(A21, A22)), ("A11", A11), ("A22", A22),
       ("A11+A12", add(A11, A12)), ("A21-A11", add(A21, A11, -1)), ("A12-A22", add(A12, A22, -1))]
tot = 0
for nm, Mx in fac:
    k = kind(Mx)
    c = 0 if "free" in k else (1 if "1 gate" in k else 2)
    tot += 2 * c            # a 2 x 2 block of X holds 2 columns
    print("   %-8s = %-22s %s" % (nm, Mx, k))
print("   products: %d gates for four 4-point arrays; additions of the recipe: 13 * 4 = 52 (Strassen) or 44 (Winograd); four bricks separately: 28" % tot)
