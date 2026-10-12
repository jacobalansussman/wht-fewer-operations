#!/usr/bin/env python3
"""g-7-thirdturn / basics.py  -- exact (integers and Fractions).  Count (G) wherever a count appears.
Checks, at N = 4, 16, 64:
  1. R = T S / sqrt(N): R^3 = I, trace 1, fixed space of dimension (N+2)/3, R orthogonal, R_N = R_4 tensor ... tensor R_4.
  2. the triple of a coordinate seed: e_x -> (a Walsh row) -> (a quadratic-form sign vector) -> e_x.
  3. for the half-transform basis B_L (L = first half of the address): B_L R B_L^-1 is a signed relabelling made of
     (N-1)/3 three-cycles and one fixed point; in labels (a,b) it is (a,b) -> (a+b+c, a)  [multiplication by a cube root
     of unity in the field with four elements, coordinate by coordinate].
  4. at 4 points: exact least cost(B) + cost(B^-1) over seeds in a box (closure test = exact test for 'no helper needed').
"""
import sys, itertools
from fractions import Fraction as F
pc = lambda x: bin(x).count("1")
def mm(A, B):
    n = len(A); m = len(B[0]); k = len(B)
    return [[sum(A[i][t] * B[t][q] for t in range(k) if A[i][t] != 0) for q in range(m)] for i in range(n)]
def inv(M):
    n = len(M); A = [[F(v) for v in r] + [F(int(i == j)) for j in range(n)] for i, r in enumerate(M)]
    for c in range(n):
        p = next((i for i in range(c, n) if A[i][c] != 0), None)
        if p is None: return None
        A[c], A[p] = A[p], A[c]; pv = A[c][c]; A[c] = [v / pv for v in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c]; A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return [r[n:] for r in A]
def rank(M):
    M = [[F(v) for v in r] for r in M]; r = 0
    if not M: return 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; pv = M[r][c]; M[r] = [v / pv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
        if r == len(M): break
    return r
def setup(j):
    N = 1 << (2 * j); lo = (1 << j) - 1
    w = lambda p, y: (pc((p >> j) & (y & lo)) + pc((p & lo) & (y >> j))) & 1
    Q0 = lambda x: pc((x >> j) & (x & lo)) & 1
    S = [[-1 if w(p, y) else 1 for y in range(N)] for p in range(N)]
    T = [(-1) ** Q0(x) for x in range(N)]
    R = [[F(T[p] * S[p][y], 1 << j) for y in range(N)] for p in range(N)]
    return N, lo, w, Q0, S, T, R
def run(j):
    N, lo, w, Q0, S, T, R = setup(j); I = [[F(int(a == b)) for b in range(N)] for a in range(N)]
    R2 = mm(R, R); R3 = mm(R2, R)
    print("N=%d: R^3 = I: %s; trace R = %s; R R^T = I: %s; dim fixed space = %d (N+2)/3 = %s" % (
        N, R3 == I, sum(R[i][i] for i in range(N)), mm(R, [list(c) for c in zip(*R)]) == I,
        N - rank([[R[a][b] - I[a][b] for b in range(N)] for a in range(N)]), F(N + 2, 3)))
    # tensor structure: address bits (p1 bit i, p2 bit i) form digit i in base 4
    if j >= 2:
        N4, lo4, w4, Q4, S4, T4, R4 = setup(1)
        def dig(x): return [(((x >> (j + i)) & 1) << 1) | ((x >> i) & 1) for i in range(j)]
        ok = True
        for p in range(N):
            for y in range(N):
                v = F(1)
                for a, b in zip(dig(p), dig(y)): v *= R4[a][b]
                if v != R[p][y]: ok = False
        print("      R_N = tensor power of R_4 (digit i = bit i of each half): %s" % ok)
    # coordinate triple
    ok2 = True
    for x in range(N):
        r1 = R[x]; r2 = R2[x]
        if any(r1[y] * (1 << j) != T[x] * S[x][y] for y in range(N)): ok2 = False
        # r2 proportional to (-1)^(Q0(y) + w(x,y)) ?
        if any(r2[y] * (1 << j) != r2[0] * (1 << j) * (-1) ** (Q0(y) ^ w(x, y)) for y in range(N)): ok2 = False
    print("      coordinate seed e_x: e_x R = +-(Walsh row x)/sqrtN, e_x R^2 = +-(-1)^(Q0 + w(x,.))/sqrtN (an eigenvector of S): %s" % ok2)
    # half-transform basis: rows indexed (a,b): sum_{p1} (-1)^(a.p1) e_(p1,b)
    r = 1 << j
    BL = [[((-1) ** pc(a & (y >> j))) if (y & lo) == b else 0 for y in range(N)] for a in range(r) for b in range(r)]
    BLi = inv(BL); M = mm(mm(BL, R), BLi)
    mono = all(sum(1 for v in row if v != 0) == 1 for row in M) and all(sum(1 for row in M if row[c] != 0) == 1 for c in range(N))
    perm = {}; signs = set()
    for i in range(N):
        c = next(q for q in range(N) if M[i][q] != 0); perm[i] = c; signs.add(M[i][c])
    # row i of (B R) = sign * row perm[i] of B : so the form with label i is sent to the form with label perm[i]
    cyc = {}; seen = set()
    for i in range(N):
        if i in seen: continue
        L = 0; t = i
        while t not in seen: seen.add(t); t = perm[t]; L += 1
        cyc[L] = cyc.get(L, 0) + 1
    lab = lambda i: (i // r, i % r)
    # look for c with (a,b) -> (a+b+c, a) or one of its relatives
    forms = {"(a+b+c, a)": lambda a, b, c: (a ^ b ^ c, a), "(b, a+b+c)": lambda a, b, c: (b, a ^ b ^ c)}
    found = []
    for nm, fn in forms.items():
        for c in range(r):
            if all(lab(perm[i]) == fn(lab(i)[0], lab(i)[1], c) for i in range(N)): found.append((nm, c))
    print("      half-transform basis: B R B^-1 is a signed relabelling: %s; entries %s; cycles {length: count} = %s; rule on labels (a,b): %s" % (
        mono, sorted(signs), cyc, found))
    return N, R, R2
for j in (1, 2, 3):
    run(j)

# ---- 4 points: exact least cost(B) + cost(B^-1), count (G)
N, lo, w, Q0, S, T, R = setup(1); R2 = mm(R, R)
def prim(v):
    v = [F(x) for x in v]; nz = [x for x in v if x != 0]
    if not nz: return None
    return tuple(x / nz[0] for x in v)
def closure_cost(rows):
    """exact: (number of distinct non-coordinate rows) if they can all be made with no helper, else that number + 1 as a LOWER bound flag."""
    n = len(rows[0]); avail = {tuple(F(int(i == k)) for k in range(n)) for i in range(n)}
    tg = {prim(r) for r in rows} - avail; need = len(tg); todo = set(tg); ch = True
    while ch and todo:
        ch = False
        for t in list(todo):
            av = list(avail)
            if any(rank([list(u), list(v), list(t)]) == 2 for u, v in itertools.combinations(av, 2)):
                avail.add(t); todo.discard(t); ch = True
    return need, (len(todo) == 0)
U = [[1, 1, 0, 0], [1, 0, 1, 0]]
print("\n4 points. fixed forms (left): x0+x1 and x0+x2 fixed by R:", [mm([u], R)[0] == [F(x) for x in u] for u in U])
print("seed e_0 gives", [prim(v) for v in ([1, 0, 0, 0], R[0], R2[0])])
best = {}; nB = 0
box = [-2, -1, 0, 1, 2]
for f in itertools.product(box, repeat=4):
    if not any(f): continue
    if prim(f) != tuple(F(x) for x in f) and prim(f) != tuple(F(x, abs(next(y for y in f if y))) for x in f): pass
    fr = mm([list(f)], R)[0]; fr2 = mm([fr], R)[0]
    for al, be in [(1, 0), (0, 1), (1, 1), (1, -1), (1, 2), (2, 1), (1, -2), (2, -1), (1, 3), (3, 1)]:
        f0 = [al * U[0][k] + be * U[1][k] for k in range(4)]
        B = [list(map(F, f)), fr, fr2, list(map(F, f0))]; Bi = inv(B)
        if Bi is None: continue
        nB += 1
        c1, ok1 = closure_cost(B); c2, ok2 = closure_cost(Bi)
        lb = (c1 if ok1 else c1 + 1) + (c2 if ok2 else c2 + 1)
        key = (lb, ok1 and ok2)
        if key not in best: best[key] = (f, f0, c1, ok1, c2, ok2)
print("4 points: %d invertible B in the box.  (lower bound on cost(B)+cost(B^-1), exact?) -> example" % nB)
for key in sorted(best): print("   ", key, best[key])
