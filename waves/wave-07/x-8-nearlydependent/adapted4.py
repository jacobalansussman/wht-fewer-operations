# adapted4.py: mutation 1 at the smallest size. All whole-number A of determinant +-1 with A D A^T = H at 4 points,
# D diagonal with entries +-1, +-2, +-2, +-4 (the Smith form of H), found through the rows of A^-1 with entries in -2..2:
# rows c_0, c_1, c_1', c_2 with c_i H c_j^T = 0 (i != j), c_0 H c_0^T = +-1, c_1 H c_1^T = +-2, c_2 H c_2^T = +-4 (then automatically c_i H = d_i * column i of A).
# For each A: its least number of in-place moves row_i <- row_i +- row_j (wires up to sign and order), by breadth-first search to depth 5.
# Z (subset sums) costs 4.  Everything exact (whole numbers, fractions).
import itertools, sys
from fractions import Fraction as Fr
H = [[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]]
def form(c, d): return sum(c[i]*H[i][j]*d[j] for i in range(4) for j in range(4))
def inv(M):
    n = 4; A = [[Fr(x) for x in r] + [Fr(int(i == j)) for j in range(n)] for i, r in enumerate(M)]
    for c in range(n):
        p = next((i for i in range(c, n) if A[i][c] != 0), None)
        if p is None: return None
        A[c], A[p] = A[p], A[c]; A[c] = [x / A[c][c] for x in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0: f = A[i][c]; A[i] = [x - f*y for x, y in zip(A[i], A[c])]
    return [r[n:] for r in A]
def canon(M):
    rows = []
    for r in M:
        f = next(x for x in r if x); rows.append(tuple(r) if f > 0 else tuple(-x for x in r))
    return tuple(sorted(rows))
vecs = [c for c in itertools.product(range(-2, 3), repeat=4) if any(c) and next(x for x in c if x) > 0]
lev = {1: [], 2: [], 4: []}
for c in vecs:
    q = form(c, c)
    if abs(q) in lev: lev[abs(q)].append(c)
print("vectors with entries in -2..2, up to sign: %d; with c H c^T = +-1: %d, +-2: %d, +-4: %d" % (len(vecs), len(lev[1]), len(lev[2]), len(lev[4])))
sols = set()
for c0 in lev[1]:
    L1 = [c for c in lev[2] if form(c0, c) == 0]; L2 = [c for c in lev[4] if form(c0, c) == 0]
    for a, b in itertools.combinations(L1, 2):
        if form(a, b): continue
        for c2 in L2:
            if form(a, c2) or form(b, c2): continue
            Ainv = [list(c0), list(a), list(b), list(c2)]; A = inv(Ainv)
            if A is None or any(x.denominator != 1 for r in A for x in r): continue
            A = [[int(x) for x in r] for r in A]
            # check A D A^T = H with D read off
            D = [form(c, c) for c in (c0, a, b, c2)]
            ok = all(sum(A[i][s]*D[s]*A[j][s] for s in range(4)) == H[i][j] for i in range(4) for j in range(4))
            if ok: sols.add((canon(A), tuple(sorted(D))))
print("solutions A (wires up to sign and order): %d ; diagonal sign patterns: %s" % (len(sols), sorted(set(d for _, d in sols))))
# in-place cost with moves +-1
I4 = canon([[int(i == j) for j in range(4)] for i in range(4)]); dist = {I4: 0}; level = [I4]
for d in range(1, 6):
    nxt = []
    for M in level:
        for i in range(4):
            for j in range(4):
                if i != j:
                    for s in (1, -1):
                        R = list(M); R[i] = tuple(x + s*y for x, y in zip(M[i], M[j])); c = canon(R)
                        if c not in dist: dist[c] = d; nxt.append(c)
    level = nxt
hist = {}
for A, D in sols: hist[dist.get(A, ">5")] = hist.get(dist.get(A, ">5"), 0) + 1
print("in-place cost (moves +-1) of these A: histogram", sorted(hist.items(), key=lambda t: str(t[0])))
Z0 = [[1,0,0,0],[1,1,0,0],[1,0,1,0],[1,1,1,1]]; Z = canon(Z0)
Zs = {canon([[x*e for x, e in zip(r, sg)] for r in Z0]) for sg in itertools.product((1, -1), repeat=4)}   # Z with the signs of its columns changed (the rows of A^-1 were taken up to sign)
print("subset sums Z: cost", dist.get(Z), "; is a solution up to the signs of its columns:", any(A in Zs for A, _ in sols))
def colclass(A):  # class of A under signs and order of rows AND columns
    return min(canon([[r[p[j]]*sg[j] for j in range(4)] for r in A]) for p in itertools.permutations(range(4)) for sg in itertools.product((1, -1), repeat=4))
cl = {}
for A, D in sols: cl.setdefault(colclass(A), []).append(D)
print("classes of solutions when the inputs may also be relabelled and negated: %d ; the class of Z among them: %s" % (len(cl), colclass(Z0) in cl))
for c, Ds in sorted(cl.items()): print("  class representative", c, " diagonals", sorted(set(Ds)))
best = sorted([(dist.get(A, 99), sum(1 for r in A for x in r if x), A, D) for A, D in sols])[:8]
for c, nz, A, D in best: print("  cost %s, %d non-zero entries, D = %s, A = %s" % (c, nz, D, A))
print("fewest non-zero entries of A^-1 over all solutions:", min(sum(1 for r in inv([list(r) for r in A]) for x in r if x) for A, _ in sols), "(3^k = 9)")
