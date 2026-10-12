# x-3 boxrelations: why the hand program "five single calls + one nested pair" for the six address maps at K = 4 does not exist.
# The table splits into 5 numbers that do not move, 5 pairs that move like the 3 addresses (one call each), and ONE number that is
# multiplied by the sign of the permutation. Question: is sign(s) = p^T P M P a (two calls deep) for fixed p, M, a?  And three deep?
# Exact (fractions): for random a, p the 6 linear equations in M are solved or shown inconsistent.
from fractions import Fraction as F
import itertools, random
random.seed(7)
def consistent(rows, rhs):
    M = [r[:] + [b] for r, b in zip(rows, rhs)]; rk = 0
    for c in range(len(rows[0])):
        p = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        for i in range(rk + 1, len(M)):
            if M[i][c] != 0:
                f = M[i][c]/M[rk][c]; M[i] = [a - f*b for a, b in zip(M[i], M[rk])]
        rk += 1
    return not any(all(v == 0 for v in r[:-1]) and r[-1] != 0 for r in M)
maps = [(0,) + s for s in itertools.permutations((1, 2, 3))]
def P(img):
    Pm = [[F(0)]*4 for _ in range(4)]
    for x in range(4): Pm[img[x]][x] = F(1)
    return Pm
def mv(A, v): return [sum(A[i][j]*v[j] for j in range(4)) for i in range(4)]
def vm(v, A): return [sum(v[i]*A[i][j] for i in range(4)) for j in range(4)]
def sign(img): return 1 if sum(img[i] > img[j] for i in range(4) for j in range(i + 1, 4)) % 2 == 0 else -1
rv = lambda: [F(random.randint(-9, 9)) for _ in range(4)]
two = three = 0; T = 200
for trial in range(T):
    a, p = rv(), rv(); M1 = [rv() for _ in range(4)]
    rows2 = []; rows3 = []
    for img in maps:
        Pm = P(img); Pa = mv(Pm, a); pP = vm(p, Pm)
        rows2.append([pP[i]*Pa[j] for i in range(4) for j in range(4)])            # p^T P M P a, linear in M
        mid = mv(Pm, mv(M1, Pa))
        rows3.append([pP[i]*mid[j] for i in range(4) for j in range(4)])           # p^T P M2 P M1 P a, linear in M2
    rhs = [F(sign(img)) for img in maps]
    two += consistent(rows2, rhs); three += consistent(rows3, rhs)
print('sign of the address map as a two-deep word  p^T P M P a      : solvable for %d of %d random (a, p)' % (two, T))
print('sign of the address map as a three-deep word p^T P M2 P M1 P a: solvable for %d of %d random (a, p, M1)' % (three, T))
