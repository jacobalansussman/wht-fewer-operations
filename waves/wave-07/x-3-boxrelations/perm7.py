# x-3 boxrelations: an EXACT 7-call program for the family of the six address maps at K = 4 (textbook 8, telescoping bound 6).
# Box: P = permutation matrix of an invertible bit matrix g on the addresses 0..3 (address 0 is fixed, 1, 2, 3 are permuted by any s in S3).
# Target: Y = P X P^T, that is Y[g x, g y] = X[x, y]. Glue is free and fixed (the same for all six boxes). Fractions throughout.
# Calls 1 to 5 are single calls; calls 6 and 7 are nested and give sign(s) times one number (the sign is not a linear function of P).
from fractions import Fraction as F
import itertools, random
random.seed(3)
def solve(rows, rhs):                       # exact Gaussian elimination, returns one solution or None
    n = len(rows[0]); M = [r[:] + [b] for r, b in zip(rows, rhs)]; piv = []; rk = 0
    for c in range(n):
        p = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]; M[rk] = [v/M[rk][c] for v in M[rk]]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0: M[i] = [a - M[i][c]*b for a, b in zip(M[i], M[rk])]
        piv.append(c); rk += 1
    if any(all(v == 0 for v in r[:-1]) and r[-1] != 0 for r in M): return None
    x = [F(0)]*n
    for i, c in enumerate(piv): x[c] = M[i][-1]
    return x
maps = [(0,) + s for s in itertools.permutations((1, 2, 3))]           # img[x] = g x
def call(img, w):                                                      # the box: (P w)[g x] = w[x]
    out = [F(0)]*4
    for x in range(4): out[img[x]] = w[x]
    return out
def sign(img): return 1 if sum(img[i] > img[j] for i in range(4) for j in range(i + 1, 4)) % 2 == 0 else -1
cyc = {1: (2, 3), 2: (3, 1), 3: (1, 2)}                                # for z, the other two addresses in cyclic order
def cross111(t): return [F(0), t[2] - t[3], t[3] - t[1], t[1] - t[2]]  # t x (1,1,1) on the slots 1..3
# glue of the nested pair: a 4 x 4 matrix M with p^T P M P a = sign for all six maps (6 linear equations in M)
a = [F(1), F(2), F(-1), F(0)]; p = [F(1), F(1), F(2), F(-3)]
rows = []
for img in maps:
    Pa = call(img, a); pP = [p[img[x]] for x in range(4)]              # (p^T P)[x] = p[g x]
    rows.append([pP[i]*Pa[j] for i in range(4) for j in range(4)])
m = solve(rows, [F(sign(img)) for img in maps]); assert m is not None, 'no glue for this a, p'
M = [m[4*i:4*i + 4] for i in range(4)]
def program(img, X):
    ncalls = 0
    def box(w):
        nonlocal ncalls; ncalls += 1; return call(img, w)
    Y = [[None]*4 for _ in range(4)]
    c1 = box([X[0][y] for y in range(4)])                               # call 1: row 0
    c2 = box([X[x][0] for x in range(4)])                               # call 2: column 0
    c3 = box([X[x][x] for x in range(4)])                               # call 3: the diagonal
    u = [F(0)] + [X[cyc[z][0]][cyc[z][1]] for z in (1, 2, 3)]; v = [F(0)] + [X[cyc[z][1]][cyc[z][0]] for z in (1, 2, 3)]
    c4 = box([u[z] + v[z] for z in range(4)])                           # call 4: sums over the two orders of each pair
    t = [u[z] - v[z] for z in range(4)]; mean = (t[1] + t[2] + t[3])/3; t0 = [F(0)] + [t[z] - mean for z in (1, 2, 3)]
    c5 = box(cross111(t0)); d0 = [-w/3 for w in cross111(c5)]           # call 5: the sum-zero part of the differences, turned a quarter
    c6 = box([mean*w for w in a])                                       # call 6
    c7 = box([sum(M[i][j]*c6[j] for j in range(4)) for i in range(4)])  # call 7, nested in call 6
    sm = sum(p[i]*c7[i] for i in range(4))                              # = sign * mean
    for y in range(4): Y[0][y] = c1[y]
    for x in range(4): Y[x][0] = c2[x]
    for x in range(4): Y[x][x] = c3[x]
    for z in (1, 2, 3):
        x, y = cyc[z]; dz = d0[z] + sm; Y[x][y] = (c4[z] + dz)/2; Y[y][x] = (c4[z] - dz)/2
    return Y, ncalls
ok = 0
for img in maps:
    for trial in range(50):
        X = [[F(random.randint(-99, 99), random.randint(1, 9)) for _ in range(4)] for _ in range(4)]
        Y, n = program(img, X); assert n == 7
        want = [[None]*4 for _ in range(4)]
        for x in range(4):
            for y in range(4): want[img[x]][img[y]] = X[x][y]
        assert Y == want, (img, trial); ok += 1
print('7 calls give P X P^T exactly for all 6 address maps at K = 4: %d cases right (textbook 8 calls; telescoping bound 6)' % ok)
print('glue of the nested pair, M =', [[str(v) for v in r] for r in M], ' a =', [str(v) for v in a], ' p =', [str(v) for v in p])
