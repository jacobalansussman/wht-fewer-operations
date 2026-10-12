#!/usr/bin/env python3
# e-0-ring / verify16.py : exact check, integers only, of the 16-point identity
#     (trace-one mask) = -(1 + t + t^4)(1 + t^2 + t^8) + J - C3 + C5      in Z[t]/(t^15 - 1)
# J = all fifteen powers, C3 = 1 + t^5 + t^10 (the subgroup of order 3), C5 = 1 + t^3 + t^6 + t^9 + t^12 (order 5),
# and of the statement that the 16 x 16 matrix it describes IS the Walsh-Hadamard matrix up to relabelling rows and columns.
# Then the same question at 64 points: which products of Frobenius twists f(t^(2^b)) of the defining trinomial divide the mask?
n = 15
pw = [1]
for _ in range(14):
    v = pw[-1] << 1
    if v >> 4: v ^= 0b10011
    pw.append(v)
lg = {v: i for i, v in enumerate(pw)}
def mul(a, b): return 0 if a == 0 or b == 0 else pw[(lg[a] + lg[b]) % 15]
def tr(v):
    s = 0; w = v
    for _ in range(4): s ^= w; w = mul(w, w)
    return s
def pm(a, b):
    out = [0] * n
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): out[(i + j) % n] += x * y
    return out
def P(*exps):
    v = [0] * n
    for e in exps: v[e % n] += 1
    return v
mask = [tr(pw[m]) for m in range(n)]
f1 = P(0, 1, 4); f2 = P(0, 2, 8)
J = [1] * n; C3 = P(0, 5, 10); C5 = P(0, 3, 6, 9, 12)
rhs = [-a + j - c3 + c5 for a, j, c3, c5 in zip(pm(f1, f2), J, C3, C5)]
print("mask                         :", mask)
print("-(1+t+t^4)(1+t^2+t^8)+J-C3+C5:", rhs)
assert mask == rhs
print("IDENTITY HOLDS exactly in Z[t]/(t^15 - 1).")
# the transform's own element M = J - 2 mask = 2 f1 f2 - J + 2 C3 - 2 C5
M = [1 - 2 * m for m in mask]
assert M == [2 * a - 1 + 2 * c3 - 2 * c5 for a, c3, c5 in zip(pm(f1, f2), C3, C5)]
# the 16 x 16 matrix: rows and columns indexed by field elements, entry (-1)^Trace(x y)
els = [0] + pw
Hm = [[(-1) ** tr(mul(x, y)) for y in els] for x in els]
# on the non-zero addresses the entry at (theta^i, theta^j) is M[(i + j) mod 15]
assert all(Hm[1 + i][1 + j] == M[(i + j) % n] for i in range(n) for j in range(n))
# it is the Walsh-Hadamard matrix up to relabelling: every row is a character of the additive group (Z/2)^4, all 16 distinct
for r in Hm:
    assert all(r[els.index(x ^ y)] == r[els.index(x)] * r[els.index(y)] for x in els for y in els)
assert len(set(map(tuple, Hm))) == 16
print("The matrix (-1)^Trace(xy) is the 16-point Walsh-Hadamard matrix up to relabelling; its non-zero block is the circulant of")
print("   M = 2 (1+t+t^4)(1+t^2+t^8) - J + 2 C3 - 2 C5   (read along i + j).")
# other exact forms of the same thing on the mixed piece: squares
sq = pm(P(0), P(0))
g = [0] * n; g[0] = 1; g[1] = -1; g[4] = -1
gg = pm(g, g); sh = [0] * n; sh[10] = 1
cand = [-x for x in pm(sh, gg)]
diff = [a - b for a, b in zip(mask, cand)]
print("mask + t^10 (1 - t - t^4)^2 =", diff, " (must vanish on the mixed piece only: checked in unit16.py)")
# gate counts (G: any a*u + b*v is one gate) of the circuit this identity gives, against the textbook 64 and the best known 56
two_trinomials = 2 * 2 * n
print("gates (G) for the two trinomial passes alone: %d  (textbook 64, best known 56): the identity is NOT a cheaper circuit at 16 points." % two_trinomials)
