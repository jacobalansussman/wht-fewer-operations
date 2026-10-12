# u-9: the repair experiment for subset sums.  Take a best modulo-2 picture, delete the +-2 cells of M, look at the remainder.
import sys, re
from fractions import Fraction
def rank(Mx):
    M = [[Fraction(v) for v in r] for r in Mx]; r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c]), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
def load(fn):
    best = None; L = open(fn).read().split("\n")
    out = []
    for i, l in enumerate(L):
        if l.startswith("BEST"): out.append((int(l.split()[1]), [int(v) for v in L[i + 1].split()[1:]], [int(v) for v in L[i + 2].split()[1:]]))
    return out
def study(rows, cols):
    N = len(rows)
    P = [[1 if (r & c) == c else 0 for c in cols] + [0] for r in rows] + [[0] * (N + 1)]
    M = [[P[a][b] - P[a + 1][b] - P[a][b + 1] + P[a + 1][b + 1] for b in range(N)] for a in range(N)]
    odd = [(a, b) for a in range(N) for b in range(N) if M[a][b] & 1]; two = [(a, b, M[a][b]) for a in range(N) for b in range(N) if abs(M[a][b]) == 2]
    # replay modulo 2 on all basis vectors: F_b = xor of the first b+1 inputs; y_a = y_(a+1) xor (xor of F_b over odd cells of row a)
    ok2 = True; okZ = True
    for t in range(N):
        x = [1 if cols[b] == t else 0 for b in range(N)]
        F = []; s = 0
        for b in range(N): s += x[b]; F.append(s)
        y2 = [0] * (N + 1); yz = [0] * (N + 1); y1 = [0] * (N + 1)
        for a in range(N - 1, -1, -1):
            y2[a] = (y2[a + 1] + sum(F[b] for b in range(N) if M[a][b] & 1)) % 2
            yz[a] = yz[a + 1] + sum(M[a][b] * F[b] for b in range(N))
            y1[a] = y1[a + 1] + sum(M[a][b] * F[b] for b in range(N) if M[a][b] & 1)
        for a in range(N):
            z = 1 if (rows[a] & t) == t else 0
            ok2 &= (y2[a] == z); okZ &= (yz[a] == z)
    # remainder R = (Z - Z')/2 in address coordinates, Z' = rebuild of the odd part of M
    Zp = [[0] * (N + 1) for _ in range(N + 1)]
    for a in range(N - 1, -1, -1):
        for b in range(N - 1, -1, -1): Zp[a][b] = (M[a][b] if M[a][b] & 1 else 0) + Zp[a + 1][b] + Zp[a][b + 1] - Zp[a + 1][b + 1]
    R = [[(P[a][b] - Zp[a][b]) // 2 for b in range(N)] for a in range(N)]
    assert all((P[a][b] - Zp[a][b]) % 2 == 0 for a in range(N) for b in range(N))
    nzr = sum(1 for r in R if any(r)); nzc = sum(1 for b in range(N) if any(R[a][b] for a in range(N)))
    print(f"N={N}: odd cells {len(odd)}, checkerboards {len(two)}; exclusive-or replay on all {N} basis vectors: {ok2}; whole-number replay: {okZ}")
    print(f"   exclusive-or circuit: {N - 2 + len(odd)} gates (Yates {N // 2 * (N.bit_length() - 1)}); whole-number two-chain circuit in these orders: {N - 2 + len(odd) + len(two)} gates")
    print(f"   remainder (Z - Z')/2: rank {rank(R) if any(any(r) for r in R) else 0}, non-zero rows {nzr}, non-zero columns {nzc}, entries {sorted(set(v for r in R for v in r))}")
    print("   rows", rows); print("   cols", cols)
    for a, b, v in two: print(f"   checkerboard at outputs {rows[a]:0{N.bit_length()-1}b},{rows[a+1] if a+1<N else -1:0{N.bit_length()-1}b} inputs {cols[b]:0{N.bit_length()-1}b},{cols[b+1] if b+1<N else -1:0{N.bit_length()-1}b} value {v}")
for fn in sys.argv[1:]:
    for best, rows, cols in load(fn)[-1:]: study(rows, cols)
