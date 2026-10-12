#!/usr/bin/env python3
"""m2_16.py [ad-1-linesums]  16 points, the 20 line sums of the plane over the field with 4 elements.
(1) A circuit over the TWO-ELEMENT FIELD (every gate is an exclusive or) with 57 gates; adding-only needs 60.
(2) The same wiring over the whole numbers: what it computes instead, i.e. the carry that stops the lift.
(3) Relations among the 20 line sums over the rationals (rank) and modulo 2.
Exact: bit masks modulo 2, whole numbers otherwise."""
from fractions import Fraction
import itertools
def gmul(a, b):
    r = 0
    for i in range(2):
        if (b >> i) & 1: r ^= a << i
    if r & 4: r ^= 0b111
    return r
F = range(4); NZ = (1, 2, 3)
inv = {a: next(b for b in NZ if gmul(a, b) == 1) for a in NZ}
def pt(x, y): return x | (y << 2)
def vec(points):
    v = [0] * 16
    for p in points: v[p] += 1
    return tuple(v)
V = {x: vec(pt(x, y) for y in F) for x in F}                       # vertical lines (columns)
L = {(m, c): vec(pt(x, gmul(m, x) ^ c) for x in F) for m in F for c in F}   # y = m x + c ; m = 0: rows
targets = list(V.values()) + list(L.values())
assert len(set(targets)) == 20
# ---------- (1) the circuit modulo 2 ----------
def run(mod):
    """returns (gate count, dict of computed vectors) ; arithmetic modulo `mod` (None = whole numbers)"""
    g = [0]
    def add(u, v, a=1, b=1):
        g[0] += 1
        w = tuple(a * s + b * t for s, t in zip(u, v))
        return tuple(s % mod for s in w) if mod else w
    e = [tuple(1 if i == p else 0 for i in range(16)) for p in range(16)]
    def linesum(points):
        p = list(points); return add(add(e[p[0]], e[p[1]]), add(e[p[2]], e[p[3]]))
    out = {}
    H = {c: linesum(pt(x, c) for x in F) for c in F}                # 12 gates
    Vv = {x: linesum(pt(x, y) for y in F) for x in F}               # 12 gates
    for c in F: out[('L', 0, c)] = H[c]
    for x in F: out[('V', x)] = Vv[x]
    h = {c: add(*[H[d] for d in NZ if d != c]) for c in NZ}         # 3 gates : the two other non-zero rows
    v = {x: add(Vv[x], Vv[0]) for x in NZ}                          # 3 gates
    Z = {m: linesum(pt(x, gmul(m, x)) for x in F) for m in NZ}      # 9 gates : the three slanted lines through 0
    for m in NZ: out[('L', m, 0)] = Z[m]
    w = {(c, x): add(h[c], v[x]) for c in NZ for x in NZ}           # 9 gates
    for m in NZ:
        for c in NZ:
            out[('L', m, c)] = add(Z[m], w[(c, gmul(c, inv[m]))])   # 9 gates
    return g[0], out
gates, out = run(2)
ok = all(out[('V', x)] == tuple(t % 2 for t in V[x]) for x in F) and \
     all(out[('L', m, c)] == tuple(t % 2 for t in L[(m, c)]) for m in F for c in F)
print("(1) circuit over the two-element field: gates =", gates, " all 20 line sums correct modulo 2:", ok)
print("    adding-only count (exact, no two lines share two points): 60")
# ---------- (2) the same wiring over the whole numbers ----------
gates, outZ = run(None)
print("(2) same wiring, whole numbers, every gate u + v:")
bad = 0
for m in NZ:
    for c in NZ:
        d = tuple(a - b for a, b in zip(outZ[('L', m, c)], L[(m, c)]))
        if any(d): bad += 1
        if (m, c) in ((1, 1), (2, 3)):
            print("    line y = %d x + %d : computed - wanted =" % (m, c), d)
print("    lines wrong over the whole numbers:", bad, "of 9")
# exact identity over the whole numbers:  L_m(c) = h_c - L_m(0) - (V_{c/m} + V_0) + 2 * (sum over the rectangle {0, c/m} x {0, c})
idok = True
for m in NZ:
    for c in NZ:
        x = gmul(c, inv[m])
        hc = tuple(sum(L[(0, d)][i] for d in NZ if d != c) for i in range(16))
        rect = vec([pt(0, 0), pt(x, 0), pt(0, c), pt(x, c)])
        rhs = tuple(hc[i] - L[(m, 0)][i] - V[x][i] - V[0][i] + 2 * rect[i] for i in range(16))
        idok &= (rhs == L[(m, c)])
print("    identity L_m(c) = h_c - L_m(0) - V_(c/m) - V_0 + 2 * (rectangle {0, c/m} x {0, c}) over the whole numbers:", idok)
print("    the nine rectangles cost 21 gates more (3 + 9 + 9), and each line needs one more gate: 57 + 21 + 9 = 87 > 60")
# ---------- (3) relations ----------
def rank(rows, p=None):
    M = [[(Fraction(v) if p is None else v % p) for v in r] for r in rows]; rk = 0
    for c in range(len(M[0])):
        piv = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        iv = (1 / M[rk][c]) if p is None else pow(M[rk][c], p - 2, p)
        M[rk] = [(v * iv) if p is None else (v * iv) % p for v in M[rk]]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c]; M[i] = [(a - f * b) if p is None else (a - f * b) % p for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
print("(3) rank of the 20 x 16 matrix: rationals", rank(targets), " modulo 2:", rank(targets, 2), " modulo 3:", rank(targets, 3))
print("    over the rationals: 20 - 16 = 4 relations = 'the five parallel classes have the same total' and nothing else")
dirs = [[V[x] for x in F]] + [[L[(m, c)] for c in F] for m in F]
for t in range(1, 6):
    print("    modulo 2, rank of the lines of the first %d directions: %d" % (t, rank([r for d in dirs[:t] for r in d], 2)))
