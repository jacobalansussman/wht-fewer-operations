#!/usr/bin/env python3
"""flatbasis.py [ad-1-linesums]  One formula, two known programs.  For ANY N flats whose indicators form an invertible matrix B:
   H = P * (diagonal of the flats' sizes) * B^-1 ,  P = the columns H b / |flat|, each a +-1 pattern on the dual subspace.
(a) flats = coordinate subcubes {x contains S}: this is H = Z D Z^T (Yates on both sides).
(b) flats = 16 of the 20 lines of the plane: P is five 4-point transforms on the five slices: the slice theorem.
Checks at 16 points, whole numbers / fractions: P has entries 0, +-1 only, its columns are supported on the dual subspace, and
the count of non-zeros of P and of B^-1 (a crude size, not a gate count)."""
from fractions import Fraction as F
N = 16; K = 4
def dot(x, y): return bin(x & y).count("1") & 1
H = [[(-1) ** dot(x, y) for x in range(N)] for y in range(N)]
def gmul(a, b):
    r = 0
    for i in range(2):
        if (b >> i) & 1: r ^= a << i
    if r & 4: r ^= 0b111
    return r
def inverse(M):
    n = len(M); A = [[F(v) for v in r] + [F(int(i == c)) for c in range(n)] for i, r in enumerate(M)]
    for c in range(n):
        p = next((i for i in range(c, n) if A[i][c] != 0), None)
        if p is None: return None
        A[c], A[p] = A[p], A[c]; A[c] = [v / A[c][c] for v in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0: A[i] = [u - A[i][c] * v for u, v in zip(A[i], A[c])]
    return [r[n:] for r in A]
def study(name, flats):
    B = [[1 if x in fl else 0 for fl in flats] for x in range(N)]            # columns = indicators
    Bi = inverse(B)
    if Bi is None: print(name, ": indicators dependent"); return
    P = [[F(sum(H[y][x] for x in fl), len(fl)) for fl in flats] for y in range(N)]
    ok_entries = all(v in (0, 1, -1) for r in P for v in r)
    # check H = P diag(|flat|) B^-1
    ok = all(sum(P[y][c] * len(flats[c]) * Bi[c][x] for c in range(N)) == H[y][x] for y in range(N) for x in range(N))
    supp = [sum(1 for y in range(N) if P[y][c] != 0) for c in range(N)]
    print("%-28s H = P * sizes * B^-1 exactly: %s ; P has entries 0, +-1 only: %s ; non-zeros per column of P x flat size: %s ; non-zeros of P: %d, of B^-1: %d, largest |entry| of B^-1: %s"
          % (name, ok, ok_entries, sorted(set(s * len(fl) for s, fl in zip(supp, flats))), sum(supp), sum(1 for r in Bi for v in r if v != 0), max(abs(v) for r in Bi for v in r)))
study("coordinate subcubes (Yates)", [frozenset(x for x in range(N) if x & S == S) for S in range(N)])
lines = [frozenset(x | (y << 2) for y in range(4)) for x in range(4)] + [frozenset(x | ((gmul(m, x) ^ c) << 2) for x in range(4)) for m in range(4) for c in range(4)]
# drop one line from each of four parallel classes (the four relations): keep all 4 columns, 3 of each other class
keep = lines[:4] + [l for i, l in enumerate(lines[4:]) if i % 4 != 3]
study("16 lines of the plane", keep)
# a mixed basis: the whole space, 3 lines of each of the 5 classes
mixed = [frozenset(range(N))] + [l for i, l in enumerate(lines) if i % 4 != 3]
study("whole space + 15 lines", mixed)
