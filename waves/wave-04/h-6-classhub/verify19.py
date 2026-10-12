#!/usr/bin/env python3
"""h-6-classhub / verify19.py : the 19-gate program for EVERY tau, exact.  Count (G).
Wiring = g-1's h8_19gates.txt with its inputs renamed by the address map A with columns (1, 2, 7) (file input x_j -> x_{A j});
gate ratios as functions of tau read off the exact solutions of solve19.py:
  theta = 1, 1, t, t, t, 1, t, (t-1), -t(t-1), t(t-1), -t(t-1), t(t-1), t(t-1), (t-1), -(t-1), -(t-1), -(t-1), -(t-1), (t-1).
Replays with tau a SYMBOL (rational functions, exact) or a number; every output must be proportional to its row of K x K x K.
usage: verify19.py tauspec [print]"""
import sys
from field import parse_tau
tau = parse_tau(sys.argv[1]); one = tau ** 0; zero = one - one; N = 8
A = [1, 2, 7]
img = [(A[0] if x & 1 else 0) ^ (A[1] if x & 2 else 0) ^ (A[2] if x & 4 else 0) for x in range(N)]
wiring = [('g1', 'x0', 'x7'), ('g2', 'x1', 'x6'), ('g3', 'x2', 'x5'), ('g4', 'x3', 'x4'), ('g5', 'g1', 'g2'), ('g6', 'g3', 'g4'), ('g7', 'g5', 'g6'),
          ('g8', 'g7', 'x7'), ('g9', 'g7', 'x5'), ('g10', 'g8', 'x6'), ('g11', 'g9', 'x4'), ('y7', 'g10', 'g4'), ('y3', 'g9', 'x3'), ('y5', 'y3', 'g5'),
          ('y1', 'g10', 'g3'), ('y6', 'g11', 'g2'), ('y2', 'g8', 'x1'), ('y4', 'y2', 'g6'), ('y0', 'g11', 'g1')]
t = tau; d = tau - one
theta = [one, one, t, t, t, one, t, d, zero - t * d, t * d, zero - t * d, t * d, t * d, d, zero - d, zero - d, zero - d, zero - d, d]
ren = lambda n: ('x%d' % img[int(n[1:])]) if n[0] == 'x' else n
val = {'x%d' % i: [one if i == j else zero for j in range(N)] for i in range(N)}
lines = []
for (nm, u, v), th in zip(wiring, theta):
    val[nm] = [a + th * b for a, b in zip(val[ren(u)], val[ren(v)])]
    lines.append('%-4s = %s + [%s] * %s    # %s' % (nm, ren(u), th, ren(v), '  '.join(str(z) for z in val[nm])))
bits = lambda w: bin(w).count('1')
found = {}
for nm, *_ in wiring:
    y = val[nm]
    for w in range(N):
        r = [tau ** bits(w & x) for x in range(N)]
        if y[0] and all(y[x] * r[0] == y[0] * r[x] for x in range(N)): found[w] = (nm, y[0])
print('tau =', sys.argv[1], '| gates', len(wiring), '| rows of K x K x K reached (row: wire, factor):', {w: (found[w][0], str(found[w][1])) for w in sorted(found)}, '| ALL 8 EXACT:', len(found) == N)
if len(sys.argv) > 2: print('\n'.join(lines))
