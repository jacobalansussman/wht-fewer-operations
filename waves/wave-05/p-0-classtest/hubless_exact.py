#!/usr/bin/env python3
"""hubless_exact.py (p-0-classtest): exact replay of the 7-gate circuits WITHOUT a full-support helper (count G).
(1) K = [[1,1],[1,2]] (tau = 2), over the rationals.  (2) K = [[1,1],[1,t]] with t^2 - t + 1 = 0 (a primitive sixth root of unity),
in Z[t]/(t^2 - t + 1), elements written (a, b) = a + b t.  Each output must EQUAL its row of K (x) K.
Also checks, with t a free rational, that circuit (2) fails for t not a root of t^2 - t + 1 (the one entry that goes wrong is printed)."""
from fractions import Fraction as F
def replay(prog, add, mul, basis):
    val = dict(basis)
    for nm, a, u, b, v in prog: val[nm] = [add(mul(a, s), mul(b, t)) for s, t in zip(val[u], val[v])]
    return val
# (1) tau = 2, rationals
e = {('x%d' % i): [F(int(i == j)) for j in range(4)] for i in range(4)}
prog1 = [('h0', 1, 'x2', 1, 'x3'), ('h1', 1, 'x1', 1, 'x3'), ('h2', 1, 'x0', 2, 'h0'), ('r10', 1, 'x1', 1, 'h2'),
         ('r00', 1, 'r10', -1, 'h0'), ('r01', 1, 'h1', 1, 'r00'), ('r11', 2, 'h1', 1, 'h2')]
v = replay(prog1, lambda a, b: a + b, lambda a, b: a * b, e)
rows = {'r%d%d' % (w >> 1, w & 1): [F(2) ** bin(w & x).count('1') for x in range(4)] for w in range(4)}
print('(1) tau = 2: 7 gates;', {k: [str(z) for z in v[k]] for k in ('h0', 'h1', 'h2')}, '| outputs equal their rows:', all(v[k] == rows[k] for k in rows),
      '| helper supports', [sum(1 for z in v[k] if z) for k in ('h0', 'h1', 'h2')], '| coefficients used: 1, -1, 2')
# (2) t^2 = t - 1
def add(a, b): return (a[0] + b[0], a[1] + b[1])
def mul(a, b): return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0] + a[1] * b[1])      # t^2 = t - 1
one, zero, t = (1, 0), (0, 0), (0, 1); omt = (1, -1)
e2 = {('x%d' % i): [one if i == j else zero for j in range(4)] for i in range(4)}
prog2 = [('h4', one, 'x0', one, 'x2'), ('h6', one, 'h4', one, 'x3'), ('r00', one, 'h6', one, 'x1'), ('r01', t, 'r00', omt, 'h4'),
         ('h5', one, 'x0', t, 'x1'), ('r10', omt, 'h5', t, 'h6'), ('r11', omt, 'h5', t, 'r01')]
v2 = replay(prog2, add, mul, e2)
def tp(n):
    r = one
    for _ in range(n): r = mul(r, t)
    return r
rows2 = {'r%d%d' % (w >> 1, w & 1): [tp(bin(w & x).count('1')) for x in range(4)] for w in range(4)}
print('(2) t^2 - t + 1 = 0: 7 gates; outputs equal their rows:', all(v2[k] == rows2[k] for k in rows2),
      '| helper supports', [sum(1 for z in v2[k] if z != zero) for k in ('h4', 'h5', 'h6')])
for tt in (F(3), F(-1), F(2), F(1, 2)):
    prog3 = [('h4', 1, 'x0', 1, 'x2'), ('h6', 1, 'h4', 1, 'x3'), ('r00', 1, 'h6', 1, 'x1'), ('r01', tt, 'r00', 1 - tt, 'h4'),
             ('h5', 1, 'x0', tt, 'x1'), ('r10', 1 - tt, 'h5', tt, 'h6'), ('r11', 1 - tt, 'h5', tt, 'r01')]
    v3 = replay(prog3, lambda a, b: a + b, lambda a, b: a * b, e)
    rows3 = {'r%d%d' % (w >> 1, w & 1): [tt ** bin(w & x).count('1') for x in range(4)] for w in range(4)}
    bad = [(k, x, str(v3[k][x]), str(rows3[k][x])) for k in rows3 for x in range(4) if v3[k][x] != rows3[k][x]]
    print('    same wiring and placement at t = %s: wrong entries (output, column, got, wanted): %s' % (tt, bad))
