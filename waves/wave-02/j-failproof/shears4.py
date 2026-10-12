#!/usr/bin/env python3
"""Volume-free question at 4 points.  U = H_4/2 is orthogonal with determinant 1.
In-place program = sequence of shears  row_i <- row_i + c*row_j  (determinant 1 each, no scaling, no copy).
(1) replay a 9-shear program exactly;  (2) meet-in-the-middle: is there one with <= 5 shears, c in {+-1,+-2,+-1/2},
target = U up to permuting rows and flipping signs of rows (384 targets)?  Entries are kept as integers times 1/64."""
from itertools import permutations, product
S = 64
H = [[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]]
U = tuple(tuple(S * v // 2 for v in row) for row in H)
I = tuple(tuple(S * int(i == j) for j in range(4)) for i in range(4))
def shear(M, i, j, num, den):  # row_i += (num/den) row_j
    r = tuple(a + (num * b) // den for a, b in zip(M[i], M[j]))
    assert all((num * b) % den == 0 for b in M[j])
    return M[:i] + (r,) + M[i + 1:]
# (1) nine shears: w0 = r = x0-x1-x2-x3 ; w_i += r/2 ; w0 = w1+w2+w3-w0 needs a sign flip, so do it as shears on -r:
M = I
for j in (1, 2, 3):
    M = shear(M, 0, j, -1, 1)          # w0 = x0-x1-x2-x3 = r
for i in (1, 2, 3):
    M = shear(M, i, 0, 1, 2)           # w_i = x_i + r/2
for j in (1, 2, 3):
    M = shear(M, 0, j, -1, 1)          # w0 = r - (w1+w2+w3)
print("nine-shear program gives (times 1/64):")
for row in M: print("   ", row)
tg = set()
for p in permutations(range(4)):
    for sg in product((1, -1), repeat=4):
        tg.add(tuple(tuple(sg[i] * v for v in U[p[i]]) for i in range(4)))
print("is it U up to row order and row signs:", M in tg, " targets:", len(tg))
moves = [(i, j, n, d) for i in range(4) for j in range(4) if i != j for (n, d) in ((1, 1), (-1, 1), (2, 1), (-2, 1), (1, 2), (-1, 2))]
def step(layer, inverse=False):
    out = set()
    for M in layer:
        for (i, j, n, d) in moves:
            try:
                out.add(shear(M, i, j, n, d))
            except AssertionError:
                pass
    return out
F = [{I}]
for d in range(3):
    F.append(step(F[-1]))
    print("forward depth", d + 1, "states", len(F[-1]))
B = [tg]
for d in range(2):
    B.append(step(B[-1]))       # the inverse of a shear is a shear, so the same move set serves backwards
    print("backward depth", d + 1, "states", len(B[-1]))
best = None
for a in range(4):
    for b in range(3):
        if F[a] & B[b]:
            if best is None or a + b < best: best = a + b
print("shortest program found with <= 5 shears from this coefficient set:", best)
# streaming extension: forward depth 4 against backward depth 2  (programs with exactly 6 shears)
hit = None
B2 = B[2]
for M in F[3]:
    for (i, j, n, d) in moves:
        try:
            X = shear(M, i, j, n, d)
        except AssertionError:
            continue
        if X in B2:
            hit = X
            break
    if hit: break
print("a 6-shear program from this coefficient set exists:", hit is not None, hit)
