#!/usr/bin/env python3
"""e2-0-pieces: write the mixed-hub program as an explicit count-(O) program: every line is  t = u + v,  t = u - v  or  t = c * u.
Scale rule as in oprice2.py.  usage: oslp.py k  -> oslp_<N>.txt"""
import sys
from fractions import Fraction as F
k = int(sys.argv[1]); N = 1 << k
prog = []
for l in open('slp_%d.txt' % N):
    if l.startswith('#'): continue
    lhs, rhs = l.split('#')[0].split('='); t = rhs.split()
    prog.append((lhs.strip(), F(t[0]), t[2], F(t[4]), t[6]))
true = {'x%d' % i: [F(int(i == j)) for j in range(N)] for i in range(N)}
for nm, a, u, b, v in prog: true[nm] = [a * s + b * t for s, t in zip(true[u], true[v])]
parent = {nm: u for nm, a, u, b, v in prog}
def lam(nm):
    if nm.startswith('hub'): return lam(parent[nm])
    s = sum(1 for t in true[nm] if t); return F(1, 2 ** ((s.bit_length() - 1) // 2))
lines = []; copies = {}
def scaled(u, c):
    if abs(c) == 1: return u
    key = (u, abs(c))
    if key not in copies:
        copies[key] = 'm%d' % (len(copies) + 1); lines.append('%s = %s * %s' % (copies[key], abs(c), u))
    return copies[key]
for nm, a, u, b, v in prog:
    lp = lam(nm); cu = a * lp / lam(u); cv = b * lp / lam(v)
    U = scaled(u, cu); V = scaled(v, cv)
    if cu > 0 and cv > 0: lines.append('%s = %s + %s' % (nm, U, V))
    elif cu > 0: lines.append('%s = %s - %s' % (nm, U, V))
    elif cv > 0: lines.append('%s = %s - %s' % (nm, V, U))
    else: raise SystemExit('a gate -u-v')
with open('oslp_%d.txt' % N, 'w') as f:
    f.write('# count (O) program, %d operations, for (1/%d) * H x on %d points; outputs are the names starting with y\n' % (len(lines), 2 ** (k // 2), N))
    f.write('\n'.join(lines) + '\n')
print('wrote oslp_%d.txt' % N, len(lines), 'operations')
