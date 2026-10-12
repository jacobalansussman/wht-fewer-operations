#!/usr/bin/env python3
"""ag-9 spec3.py: a matrix where sqrt 2 saves a gate (count (G)).  Three inputs.  Four helpers with entries a + b*sqrt2:
h1 on the line e1 e2, h2 on e2 e3, h3 on e3 e1, h4 on the line h1 e3.  Five outputs T_ij = the point where the line h_i h_j
meets its conjugate line (sqrt2 -> -sqrt2): that point is fixed by the conjugation, so it is rational.  Circuit over
Q(sqrt2): 4 helpers + 5 outputs = 9 gates; each output directly costs 2 gates (support 3), 10 in all.
Exact arithmetic: numbers are pairs of Fractions (a, b) = a + b*sqrt2.  Prints the rows for mincirc and replays the circuit."""
from fractions import Fraction as F
from math import gcd
import sys
def add(x, y): return (x[0] + y[0], x[1] + y[1])
def sub(x, y): return (x[0] - y[0], x[1] - y[1])
def mul(x, y): return (x[0]*y[0] + 2*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
def conj(x): return (x[0], -x[1])
def K(a, b=0): return (F(a), F(b))
def cross(u, v): return tuple(sub(mul(u[(i+1) % 3], v[(i+2) % 3]), mul(u[(i+2) % 3], v[(i+1) % 3])) for i in range(3))
def det(u, v, w):
    c = cross(v, w); s = K(0)
    for i in range(3): s = add(s, mul(u[i], c[i]))
    return s
Z = K(0)
par = [int(x) for x in sys.argv[1:9]] if len(sys.argv) >= 9 else [0, 1, 1, 1, 3, 1, 2, -1]
a, b, c, d = K(par[0], par[1]), K(par[2], par[3]), K(par[4], par[5]), K(par[6], par[7])
h = {1: (K(1), a, Z), 2: (Z, K(1), b), 3: (c, Z, K(1))}
h[4] = (h[1][0], h[1][1], d)                       # h1 + d*e3
cj = lambda v: tuple(conj(x) for x in v)
def rational_point(v):
    # v is fixed by conjugation up to a factor: find a scalar making it rational
    for t in (K(1), K(0, 1)):
        w = tuple(mul(t, x) for x in v)
        if all(x[1] == 0 for x in w):
            r = [x[0] for x in w]; den = 1
            for x in r: den = den * x.denominator // gcd(den, x.denominator)
            r = [int(x * den) for x in r]; g = 0
            for x in r: g = gcd(g, x)
            r = [x // g for x in r]
            if [x for x in r if x][0] < 0: r = [-x for x in r]
            return r
    raise SystemExit("not rational: %r" % (v,))
pairs = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
T = {}
for (i, j) in pairs:
    Lij = cross(h[i], h[j]); T[(i, j)] = rational_point(cross(Lij, cj(Lij)))
print("# helpers (a + b*sqrt2 written a,b):")
for k in sorted(h): print("# h%d =" % k, [("%s,%s" % (x[0], x[1])) for x in h[k]])
print("# replay, exact: each output on the line of its two helpers:", all(det(tuple(K(x) for x in T[p]), h[p[0]], h[p[1]]) == Z for p in pairs),
      "; helpers on their lines:", h[1][2] == Z and h[2][0] == Z and h[3][1] == Z and det(h[4], h[1], (Z, Z, K(1))) == Z)
print("# supports of the outputs:", [sum(1 for x in T[p] if x) for p in pairs])
for p in pairs: print(" ".join(str(x) for x in T[p]), 0)
