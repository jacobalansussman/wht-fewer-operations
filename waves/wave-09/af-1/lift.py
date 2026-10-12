#!/usr/bin/env python3
"""af-1/lift.py  Skeptic's replay of ad-1's companion claim: 57 exclusive-or gates for the 20 line sums at 16 points,
and "it does not lift". Own code. Exact: bit masks modulo 2, Fractions over the rationals, residues modulo small primes.
(1) the 57-gate program written as an explicit list of gates and replayed modulo 2;
(2) lift test with ARBITRARY coefficients on the same wiring (ad-1 tested only the coefficients +1);
(3) the whole-number identity with the rectangle, and the paid-for program replayed exactly, gates counted;
(4) one size further, 64 points: ranks, and the shortest relation among lines modulo 2."""
from fractions import Fraction
from itertools import combinations
import sys
def field(j, poly):
    q = 1 << j
    def mul(a, b):
        r = 0
        while b:
            if b & 1: r ^= a
            a <<= 1
            if a >> j: a ^= poly
            b >>= 1
        return r
    return q, mul
def rank(rows, p=None):
    M = [[(Fraction(v) if p is None else v % p) for v in r] for r in rows]; rk = 0
    ncol = len(M[0])
    for c in range(ncol):
        piv = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        iv = (1 / M[rk][c]) if p is None else pow(M[rk][c], p - 2, p)
        M[rk] = [v * iv if p is None else v * iv % p for v in M[rk]]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c]; M[i] = [(a - f * b) if p is None else (a - f * b) % p for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
def rank2(masks):
    basis = {}; rk = 0
    for m in masks:
        while m:
            h = m.bit_length() - 1
            if h in basis: m ^= basis[h]
            else: basis[h] = m; rk += 1; break
    return rk
# ------------------------------------------------------------------ 16 points
q, mul = field(2, 0b111); N = 16; NZ = [1, 2, 3]
inv = {a: next(b for b in NZ if mul(a, b) == 1) for a in NZ}
P = lambda x, y: 4 * y + x
def ind(pts):
    v = [0] * N
    for p in pts: v[p] += 1
    return v
row = {c: ind(P(x, c) for x in range(4)) for c in range(4)}
col = {x: ind(P(x, y) for y in range(4)) for x in range(4)}
lin = {(m, c): ind(P(x, mul(m, x) ^ c) for x in range(4)) for m in NZ for c in range(4)}
target = {('row', c): row[c] for c in range(4)}; target.update({('col', x): col[x] for x in range(4)})
target.update({('lin', m, c): lin[(m, c)] for m in NZ for c in range(4)})
assert len({tuple(v) for v in target.values()}) == 20
# (1) explicit program: wires 0..15 inputs; gate = (u, v, a, b) meaning a*wire u + b*wire v
def build(paid):
    G = []; name = {}
    def g(u, v, a=1, b=1): G.append((u, v, a, b)); return 15 + len(G)
    def four(pts): p = list(pts); return g(g(p[0], p[1]), g(p[2], p[3]))
    for c in range(4): name[('row', c)] = four(P(x, c) for x in range(4))
    for x in range(4): name[('col', x)] = four(P(x, y) for y in range(4))
    for m in NZ: name[('lin', m, 0)] = four(P(x, mul(m, x)) for x in range(4))
    h = {c: g(*[name[('row', d)] for d in NZ if d != c]) for c in NZ}
    v = {x: g(name[('col', x)], name[('col', 0)]) for x in NZ}
    if not paid:
        w = {(c, x): g(h[c], v[x]) for c in NZ for x in NZ}
        for m in NZ:
            for c in NZ: name[('lin', m, c)] = g(name[('lin', m, 0)], w[(c, mul(c, inv[m]))])
    else:   # L_m(c) = h_c - L_m(0) - (V_x + V_0) + 2 * rectangle{0,x} x {0,c},  x = c/m
        w = {(c, x): g(h[c], v[x], 1, -1) for c in NZ for x in NZ}
        b0 = {x: g(P(0, 0), P(x, 0)) for x in NZ}
        bc = {(c, x): g(P(0, c), P(x, c)) for c in NZ for x in NZ}
        rect = {(c, x): g(b0[x], bc[(c, x)]) for c in NZ for x in NZ}
        for m in NZ:
            for c in NZ:
                x = mul(c, inv[m])
                name[('lin', m, c)] = g(g(w[(c, x)], name[('lin', m, 0)], 1, -1), rect[(c, x)], 1, 2)
    return G, name
def replay(G, name, mod):
    W = [[1 if i == p else 0 for i in range(N)] for p in range(N)]
    for (u, v, a, b) in G:
        r = [a * s + b * t for s, t in zip(W[u], W[v])]
        W.append([t % mod for t in r] if mod else r)
    return {k: W[i] for k, i in name.items()}
G, name = build(False); out = replay(G, name, 2)
print("(1) 16 points, exclusive-or program: gates = %d ; all 20 line sums right modulo 2: %s"
      % (len(G), all(out[k] == [t % 2 for t in target[k]] for k in target)))
outZ = replay(G, name, None)
print("    same wiring, whole numbers, every coefficient +1: lines right = %d of 20" % sum(outZ[k] == target[k] for k in target))
# (2) arbitrary coefficients: the wires row, col, lin(m,0) are OUTPUTS, so in any lift they are fixed up to a scale;
#     lin(m,c) = a*lin(m,0) + b*w, w = a'*h_c + b'*v_x, h_c in span(row d, row e), v_x in span(col x, col 0).
#     So a lift exists only if lin(m,c) lies in the span of those five line sums.
for p in (None, 3, 5, 7, 2):
    n_in = 0
    for m in NZ:
        for c in NZ:
            x = mul(c, inv[m]); d, e = [t for t in NZ if t != c]
            five = [lin[(m, 0)], row[d], row[e], col[x], col[0]]
            n_in += (rank(five + [lin[(m, c)]], p) == rank(five, p))
    print("(2) %-16s: lines lin(m,c) inside the span of their five feeding line sums: %d of 9"
          % ("rationals" if p is None else "modulo %d" % p, n_in))
allv = list(target.values())
print("    rank of the 20 x 16 matrix: rationals %d, modulo 2: %d, modulo 3: %d" % (rank(allv), rank(allv, 2), rank(allv, 3)))
# (3) the identity and the paid program
G2, name2 = build(True); out2 = replay(G2, name2, None)
print("(3) paid-for program over the whole numbers (coefficients 1, -1, 2): gates = %d ; all 20 line sums right exactly: %s"
      % (len(G2), all(out2[k] == target[k] for k in target)))
# shortest relation modulo 2 at 16 points, exhaustive over all 2^20 subsets of lines is cheap via the null space
masks = [sum(1 << i for i in range(N) if v[i] & 1) for v in allv]
best = None
for r in range(1, 8):
    for S in combinations(range(20), r):
        t = 0
        for i in S: t ^= masks[i]
        if t == 0: best = (r, S); break
    if best: break
print("    shortest relation among lines modulo 2 at 16 points: %d lines" % best[0])
# ------------------------------------------------------------------ 64 points
q, mul = field(3, 0b1011); N = 64
L = []; cls = []
for m in range(q):
    for c in range(q): L.append(sum(1 << (8 * (mul(m, x) ^ c) + x) for x in range(q))); cls.append(m)
for x in range(q): L.append(sum(1 << (8 * y + x) for y in range(q))); cls.append(q)
assert len(set(L)) == 72
rows64 = [[(m >> i) & 1 for i in range(N)] for m in L]
print("(4) 64 points: rank modulo 2 = %d ; modulo 3 = %d ; modulo 2147483647 = %d (so the rank over the rationals is 64: "
      "a rank modulo a prime never exceeds the rational rank, and 64 is the number of columns)"
      % (rank2(L), rank(rows64, 3), rank(rows64, 2147483647)))
seen = {0: ()}; clash = None
for r in range(1, 5):
    for S in combinations(range(72), r):
        t = 0
        for i in S: t ^= L[i]
        if t in seen: clash = (seen[t], S); break
        seen[t] = S
    if clash: break
print("    all sums of at most 4 lines modulo 2 are distinct: %s  (so every relation modulo 2 has at least 9 lines)" % (clash is None))
t = sum(1 << (8 * y) for y in range(q))            # the column x = 0
rel = L[8 * q]
for m in range(q): rel ^= L[8 * m + mul(m, m)]
print("    the nine lines  y = m x + m^2 (all m)  and  x = 0  add to zero modulo 2: %s ; a line of 8 points from the other 8 costs 7 gates, the same as adding its points" % (rel == 0))
