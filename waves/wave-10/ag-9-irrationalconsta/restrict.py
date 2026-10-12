#!/usr/bin/env python3
"""ag-9 restrict.py: the lemma "a circuit over a field of degree d gives a rational circuit with at most d*d gates per gate",
run on the specimen of spec4.py (d = 2, numbers x + y*sqrt2).  Count (G).
A wire w over Q(sqrt2) is the pair of rational vectors (w0, w1), w = w0 + sqrt2*w1.  A gate w = u + c*v, c = c0 + c1*sqrt2
(scalings are free, so the coefficient of u is 1) becomes
     w0 = u0 + c0*v0 + 2*c1*v1      (two rational gates)        w1 = u1 + c0*v1 + c1*v0      (two rational gates).
An output is lam * (rational row); one of its two parts is a non-zero multiple of the row, so an output gate needs one part only.
The program builds the rational circuit, replays it with exact fractions, and counts the gates actually needed
(a part that is zero or that repeats a held wire up to scale costs nothing)."""
from fractions import Fraction as F
import sys
def K(a, b=0): return (F(a), F(b))
def mul(x, y): return (x[0]*y[0] + 2*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
def inv(x): n = x[0]*x[0] - 2*x[1]*x[1]; return (x[0]/n, -x[1]/n)
par = [int(x) for x in sys.argv[1:9]] if len(sys.argv) >= 9 else [1, 2, 3, -1, -2, 3, 5, 2]
a, b, c, d = K(par[0], par[1]), K(par[2], par[3]), K(par[4], par[5]), K(par[6], par[7])
n = 4
E = [[K(1) if i == j else K(0) for j in range(n)] for i in range(n)]
def comb(u, cf, v): return [(u[k][0] + mul(cf, v[k])[0], u[k][1] + mul(cf, v[k])[1]) for k in range(n)]
# the circuit over Q(sqrt2): helpers, then each output T_ij = h_i + mu*h_j with mu chosen to make it rational up to a factor
h = {1: comb(E[0], a, E[1]), 2: comb(E[1], b, E[2]), 3: comb(E[2], c, E[0]), 4: comb(E[0], d, E[3])}
gates = [("h1", ("e", 0), a, ("e", 1)), ("h2", ("e", 1), b, ("e", 2)), ("h3", ("e", 2), c, ("e", 0)), ("h4", ("e", 0), d, ("e", 3))]
rows = [[int(x) for x in l.split()] for l in open(sys.argv[9] if len(sys.argv) > 9 else "spec4_b_rows.txt") if l.strip() and l[0] != "#"]
pairs = [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)]
outs = []
for (i, j), row in zip(pairs, rows):
    # solve h_i + mu*h_j = lam*row : two coordinates give mu
    found = None
    for k1 in range(n):
        for k2 in range(k1 + 1, n):
            # (h_i[k1] + mu h_j[k1]) * row[k2] = (h_i[k2] + mu h_j[k2]) * row[k1]
            A = (h[j][k1][0]*row[k2] - h[j][k2][0]*row[k1], h[j][k1][1]*row[k2] - h[j][k2][1]*row[k1])
            B = (h[i][k2][0]*row[k1] - h[i][k1][0]*row[k2], h[i][k2][1]*row[k1] - h[i][k1][1]*row[k2])
            if A != K(0): found = mul(B, inv(A)); break
        if found: break
    w = comb(h[i], found, h[j])
    k0 = next(k for k in range(n) if row[k]); lam = mul(w[k0], inv(K(row[k0])))
    assert all(w[k] == mul(lam, K(row[k])) for k in range(n)), "output is not a multiple of its row"
    outs.append((i, j, found, lam)); gates.append(("T%d%d" % (i, j), ("h", i), found, ("h", j)))
print("circuit over Q(sqrt2): %d gates; every output is an exact multiple of its whole-number row: True" % len(gates))
# restriction of scalars, with exact replay
held = [tuple(F(int(i == j)) for j in range(n)) for i in range(n)]      # rational wires held (the inputs)
def norm(v):
    lead = next((x for x in v if x), None)
    return None if lead is None else tuple(x / lead for x in v)
heldset = {norm(v) for v in held}; count = 0; naive = 0
val = {("e", i): E[i] for i in range(n)}
for name, u, cf, v in gates:
    U, V = val[u], val[v]; Wv = comb(U, cf, V)
    isout = name[0] == "T"
    parts = []
    for part in (0, 1):
        # part 0: u0 + c0*v0 + 2*c1*v1 ; part 1: u1 + c0*v1 + c1*v0   -- built as a chain of gates over held rational wires
        terms = [[x[part] for x in U]] + ([[cf[0]*x[0] for x in V], [2*cf[1]*x[1] for x in V]] if part == 0 else [[cf[0]*x[1] for x in V], [cf[1]*x[0] for x in V]])
        terms = [t for t in terms if any(t)]
        acc = None; g = 0
        for t in terms:
            if acc is None: acc = t; continue
            acc = [p + q for p, q in zip(acc, t)]
            if norm(acc) is not None and norm(acc) not in heldset: heldset.add(norm(acc)); g += 1
        assert acc is None or acc == [x[part] for x in Wv]
        parts.append(g)
    naive += 2 if isout else 4
    count += min(p for p in parts) if isout and all(any(x[q] for x in Wv) for q in (0, 1)) else sum(parts)
    val[("h", int(name[1]))] = Wv
print("rational circuit by restriction of scalars: %d gates (the bound d*d per helper, d per output gives %d); replayed exactly" % (count, naive))
