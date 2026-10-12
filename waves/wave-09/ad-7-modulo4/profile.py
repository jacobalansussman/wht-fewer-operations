#!/usr/bin/env python3
"""profile.py [ad-7]  2-adic profile (Smith normal form over the whole numbers, exact) of the matrices whose modulo-2 rank is
below their rational rank: ab-0's block of neighbour sums (k = 4, 6, 8), the line-sum matrix of the affine plane (16, 64
points), the transform itself (16 points), and subset sums minus... (none: Z is unimodular).
Output for each: the invariant factors (d1 | d2 | ...), written as 2^v with multiplicities, and r_j = number of invariant
factors NOT divisible by 2^j (the number of generators the row module needs modulo 2^j is r_j for the 'unit' part; the rank
over the rationals is the number of non-zero factors)."""
import sys
from collections import Counter
sys.setrecursionlimit(10000)

def smith_diag(M):
    """invariant factors of an integer matrix, exact, by row/column gcd reduction (small matrices)."""
    A = [list(r) for r in M]; m = len(A); n = len(A[0]); out = []
    r0 = 0; c0 = 0
    while r0 < m and c0 < n:
        # find the non-zero entry of least absolute value in the remaining block
        best = None
        for i in range(r0, m):
            for j in range(c0, n):
                if A[i][j] and (best is None or abs(A[i][j]) < abs(A[best[0]][best[1]])): best = (i, j)
        if best is None: break
        while True:
            i, j = best
            A[r0], A[i] = A[i], A[r0]
            for row in A: row[c0], row[j] = row[j], row[c0]
            p = A[r0][c0]; dirty = False
            for i in range(r0 + 1, m):
                if A[i][c0]:
                    f = A[i][c0] // p
                    if f: A[i] = [a - f * b for a, b in zip(A[i], A[r0])]
                    if A[i][c0]: dirty = True
            for j in range(c0 + 1, n):
                if A[r0][j]:
                    f = A[r0][j] // p
                    if f:
                        for row in A: row[j] -= f * row[c0]
                    if A[r0][j]: dirty = True
            if not dirty:
                # make p divide the rest
                bad = None
                for i in range(r0 + 1, m):
                    for j in range(c0 + 1, n):
                        if A[i][j] % p: bad = (i, j); break
                    if bad: break
                if bad is None: break
                A[r0] = [a + b for a, b in zip(A[r0], A[bad[0]])]
            # pick the least non-zero entry in row r0 / column c0 / (after the fix) whole block
            best = None
            for i in range(r0, m):
                for j in range(c0, n):
                    if A[i][j] and (best is None or abs(A[i][j]) < abs(A[best[0]][best[1]])): best = (i, j)
        out.append(abs(A[r0][c0])); r0 += 1; c0 += 1
    return sorted(out)

def show(name, M):
    d = smith_diag(M); c = Counter(d)
    v2 = Counter()
    odd = Counter()
    for x in d:
        v = 0
        while x % 2 == 0: x //= 2; v += 1
        v2[v] += 1; odd[x] += 1
    print("%s : %d x %d, rational rank %d" % (name, len(M), len(M[0]), len(d)))
    print("     invariant factors: " + ", ".join("%d (x%d)" % (x, c[x]) for x in sorted(c)))
    print("     powers of 2: " + ", ".join("2^%d x%d" % (v, v2[v]) for v in sorted(v2)) + "   odd parts: " + ", ".join("%d x%d" % (o, odd[o]) for o in sorted(odd)))
    run = 0; rj = []
    for v in range(0, max(v2) + 1): run += v2[v]; rj.append(run)
    print("     r_j (factors not divisible by 2^j), j = 1.. : " + " ".join(map(str, rj)))
    return d

def block(k):
    N = 1 << k; ev = [x for x in range(N) if bin(x).count('1') % 2 == 0]; od = [x for x in range(N) if bin(x).count('1') % 2 == 1]
    return [[1 if bin(x ^ y).count('1') == 1 else 0 for x in ev] for y in od]

POLY = {2: 0b111, 3: 0b1011, 4: 0b10011}
def gmul(a, b, j):
    r = 0
    for i in range(j):
        if (b >> i) & 1: r ^= a << i
    for i in range(2 * j - 2, j - 1, -1):
        if (r >> i) & 1: r ^= POLY[j] << (i - j)
    return r
def dot(x, y): return bin(x & y).count("1") & 1
def linesums(j):
    q = 1 << j; N = q * q
    spread = [[a | (gmul(m, a, j) << j) for a in range(q)] for m in range(q)] + [[b << j for b in range(q)]]
    lines = []
    for S in spread:
        V = [x for x in range(N) if all(dot(x, s) == 0 for s in S)]
        seen = set()
        for x in range(N):
            if x in seen: continue
            c = sorted(x ^ v for v in V); seen.update(c); lines.append(c)
    return [[1 if x in set(c) else 0 for x in range(N)] for c in lines]

if __name__ == "__main__":
    what = sys.argv[1:] or ["B4", "B6", "L16", "H16", "A4", "L64"]
    for w in what:
        if w[0] == "B": show("block of neighbour sums, k=%s" % w[1:], block(int(w[1:])))
        if w[0] == "A":
            k = int(w[1:]); N = 1 << k
            show("neighbour sums A, k=%d" % k, [[1 if bin(x ^ y).count('1') == 1 else 0 for x in range(N)] for y in range(N)])
        if w[0] == "L":
            N = int(w[1:]); j = {16: 2, 64: 3, 256: 4}[N]
            show("line sums of the affine plane, N=%d" % N, linesums(j))
        if w[0] == "H":
            N = int(w[1:]); show("transform H, N=%d" % N, [[(-1) ** dot(x, y) for x in range(N)] for y in range(N)])
        sys.stdout.flush()
