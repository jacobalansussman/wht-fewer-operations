# check.py: exact checks of the three hand statements of x-8 (fractions; logarithms are floats and only used in inequalities with slack).
#  A. PAIR LAW: under any in-place move row_i <- a*row_i + b*row_j, the vector s(l) = p_il + p_jl is unchanged, coordinate by coordinate,
#     and no other row of p changes.   (p_il = M_il (M^-1)_li)
#  B. TWO CURRENCIES: entropy of the pair = - sum_l s(l) log2 max(|p_il|,|p_jl|) + err, |err| <= 1.4427 * sum_l |s(l)|.
#  C. DENOMINATOR LEMMA: whole-number M, every p in [0,1]  =>  row entropy_i <= log2 D_i, D_i = least whole number with D_i * (column i of M^-1) whole.
#     ORTHOGONAL ROWS, primitive: D_i = |row_i|^2 and Phi <= 2 log2 |det M|, with equality exactly when every entry is 0, +1 or -1.
#  D. in place, the determinant of the primitive state is multiplied by a/g only (b does not count): |det| after the move = |a| |det| / g.
import random, sys
from fractions import Fraction as Fr
from math import log2, gcd
from functools import reduce
def inv(M):
    n = len(M); A = [[Fr(x) for x in r] + [Fr(int(i == j)) for j in range(n)] for i, r in enumerate(M)]
    for c in range(n):
        p = next((i for i in range(c, n) if A[i][c] != 0), None)
        if p is None: return None
        A[c], A[p] = A[p], A[c]; A[c] = [x / A[c][c] for x in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0: f = A[i][c]; A[i] = [x - f*y for x, y in zip(A[i], A[c])]
    return [r[n:] for r in A]
def det(M):
    n = len(M); A = [[Fr(x) for x in r] for r in M]; d = Fr(1)
    for c in range(n):
        p = next((i for i in range(c, n) if A[i][c] != 0), None)
        if p is None: return Fr(0)
        if p != c: A[c], A[p] = A[p], A[c]; d = -d
        d *= A[c][c]
        for i in range(c+1, n):
            f = A[i][c] / A[c][c]
            if f: A[i] = [x - f*y for x, y in zip(A[i], A[c])]
    return d
def P(M):
    I = inv(M); n = len(M); return [[M[i][l] * I[l][i] for l in range(n)] for i in range(n)]
def eta(p): return 0.0 if p == 0 else -float(p) * log2(abs(float(p)))
def ent(row): return sum(eta(p) for p in row)
def prim(r):
    g = reduce(gcd, [abs(int(x)) for x in r]); return [int(x) // g for x in r], g
def kron(A, B): return [[x*y for x in ra for y in rb] for ra in A for rb in B]
random.seed(8)
# A, B, D on random states reached by random moves (ill conditioned ones included)
nA = 0; worst = 0.0; nD = 0
for trial in range(400):
    n = random.choice([3, 4, 5, 6]); M = [[int(i == j) for j in range(n)] for i in range(n)]
    for step in range(random.randint(2, 14)):
        i, j = random.sample(range(n), 2); a = random.choice([1, 1, 2, 3, -1]); b = random.choice([1, -1, 2, -2, 3, 5])
        p0 = P(M); d0 = det(M)
        new = [a*x + b*y for x, y in zip(M[i], M[j])]; M2 = [r[:] for r in M]; M2[i] = new
        if inv(M2) is None: continue
        p1 = P(M2)
        assert all(p0[i][l] + p0[j][l] == p1[i][l] + p1[j][l] for l in range(n)), "pair law fails"
        assert all(p0[r] == p1[r] for r in range(n) if r not in (i, j)), "another row moved"
        nA += 1
        for pp in (p0, p1):
            s = [pp[i][l] + pp[j][l] for l in range(n)]
            main = sum(-float(s[l]) * log2(max(abs(float(pp[i][l])), abs(float(pp[j][l])))) for l in range(n) if s[l] != 0)
            err = ent(pp[i]) + ent(pp[j]) - main; mass = sum(abs(float(x)) for x in s)
            assert abs(err) <= 1.4427 * mass + 1e-9, ("two currencies fails", err, mass)
            if mass > 0: worst = max(worst, abs(err) / mass)
        newp, g = prim(new); M3 = [r[:] for r in M]; M3[i] = newp
        assert abs(det(M3)) == abs(d0) * abs(a) / g, "determinant law fails"; nD += 1
        M = M3
print("A pair law: exact on %d random moves (sizes 3..6, coefficients up to 5).  D determinant law |det| -> |a| |det| / g: exact on %d moves." % (nA, nD))
print("B two currencies: |err| / sum|s| at most %.4f over those states (claimed bound 1.4427)" % worst)
# C on landed states: Kronecker powers, the witnesses printed by rt, and orthogonal whole-number matrices built from 2 x 2 blocks
H = [[1, 1], [1, -1]]; R345 = [[3, 4], [-4, 3]]; R512 = [[5, 12], [-12, 5]]; I2 = [[1, 0], [0, 1]]
def test(name, M, orth):
    p = P(M); assert all(0 <= x <= 1 for r in p for x in r), name + ": not landed"
    I = inv(M); n = len(M); tot = 0.0; bound = 0.0
    for i in range(n):
        D = reduce(lambda u, v: u * v // gcd(u, v), [I[l][i].denominator for l in range(n)], 1)
        e = ent(p[i]); assert e <= log2(D) + 1e-9, (name, "row", i, e, D); tot += e; bound += log2(D)
    line = "  %-34s Phi = %7.3f <= sum log2 D_i = %7.3f" % (name, tot, bound)
    if orth:
        assert all(sum(x*y for x, y in zip(M[i], M[j])) == 0 for i in range(n) for j in range(i)), name + ": rows not orthogonal"
        d = abs(det(M)); v = 2 * log2(float(d)); assert tot <= v + 1e-9
        unit = all(x in (0, 1, -1) for r in M for x in r); assert (abs(tot - v) < 1e-9) == unit, (name, "equality case")
        line += " ; 2 log2|det| = %7.3f ; entries all 0,+-1: %s ; equality: %s" % (v, unit, abs(tot - v) < 1e-9)
    print(line)
print("C denominator lemma on landed states:")
test("H (2 points)", H, True); test("H (4 points)", kron(H, H), True); test("H (8 points)", kron(H, kron(H, H)), True); test("H (16 points)", kron(kron(H, H), kron(H, H)), True)
test("rotation 3-4-5", R345, True); test("H x rotation 3-4-5", kron(H, R345), True); test("3-4-5 x 5-12-13", kron(R345, R512), True)
test("(1,1,1),(1,-1,0),(1,1,-2)", [[1,1,1],[1,-1,0],[1,1,-2]], True)
test("rt witness (0,1,1)(1,-1,1)(1,1,-1)", [[0,1,1],[1,-1,1],[1,1,-1]], False)
test("rt witness (1,-2,1)(1,1,-1)(1,3,3)", [[1,-2,1],[1,1,-1],[1,3,3]], False)
test("rt witness (1,-3,-5)(1,1,-1)(2,-1,3)", [[1,-3,-5],[1,1,-1],[2,-1,3]], False)
test("J - 2I (4 points, the brick)", [[1 - 2*int(i == j) for j in range(4)] for i in range(4)], True)
# unimodular states: landed => Phi = 0.  random +-1 walks, keep the landed ones
cnt = 0
for trial in range(4000):
    n = 4; M = [[int(i == j) for j in range(n)] for i in range(n)]
    for step in range(random.randint(1, 7)):
        i, j = random.sample(range(n), 2); s = random.choice([1, -1]); M[i] = [x + s*y for x, y in zip(M[i], M[j])]
    p = P(M)
    if all(0 <= x <= 1 for r in p for x in r): cnt += 1; assert all(x in (0, 1) for r in p for x in r)
print("unimodular walks (+-1 moves, 4 wires): %d of 4000 end states are landed, and every one has all p in {0,1}: entropy exactly 0" % cnt)
print("ALL CHECKS PASSED")
