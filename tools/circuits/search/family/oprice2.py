#!/usr/bin/env python3
"""e2-0-pieces: count (O) price of the mixed-hub programs with an EXPLICIT scale rule, replayed exactly.
Rule: a point whose support has 2^j inputs is held multiplied by 2^(-floor(j/2)); a hub is held at the scale of its two pieces.  Then a gate P = M +- 2w (hub M one level
down, witness w two levels down) needs no multiplication at odd levels and one halving of the hub at even levels.
The program below is rewritten as an (O) program: every line is either  t = u + v, t = u - v  (cost 1)  or  t = c * u  (cost 1),
run on symbolic inputs with Fractions, and every output is compared with  2^(-floor(k/2)) * (row of H)   [mode 'common']
and, after N more multiplications, with the row of H itself [mode 'exact'].   usage: oprice2.py k"""
import sys
from fractions import Fraction as F
k = int(sys.argv[1]); N = 1 << k
prog = []
for l in open('slp_%d.txt' % N):
    if l.startswith('#'): continue
    lhs, rhs = l.split('#')[0].split('='); t = rhs.split()
    prog.append((lhs.strip(), F(t[0]), t[2], F(t[4]), t[6]))
# true vectors, to get supports
true = {'x%d' % i: [F(int(i == j)) for j in range(N)] for i in range(N)}
for nm, a, u, b, v in prog: true[nm] = [a * s + b * t for s, t in zip(true[u], true[v])]
parent = {nm: u for nm, a, u, b, v in prog}
def lam(nm):
    if nm.startswith('hub'): return lam(parent[nm])      # a hub is held at the scale of the two pieces it joins
    s = sum(1 for t in true[nm] if t); j = s.bit_length() - 1
    return F(1, 2 ** (j // 2))
held = {'x%d' % i: [F(int(i == j)) for j in range(N)] for i in range(N)}   # values of the (O) program
copies = {}        # (name, factor) -> value
ops = {'add': 0, 'mul': 0}
def scaled(u, c):
    if c == 1: return held[u]
    if c == -1: return [-t for t in held[u]]           # sign is absorbed in add/subtract
    key = (u, abs(c))
    if key not in copies:
        copies[key] = [abs(c) * t for t in held[u]]; ops['mul'] += 1
    return copies[key] if c > 0 else [-t for t in copies[key]]
for nm, a, u, b, v in prog:
    lp = lam(nm); cu = a * lp / lam(u); cv = b * lp / lam(v)
    U = scaled(u, cu); V = scaled(v, cv)
    if cu < 0 and cv < 0: ops['negneg'] = ops.get('negneg', 0) + 1
    assert abs(cu) in (1, 2, F(1, 2)) and abs(cv) in (1, 2, F(1, 2))
    held[nm] = [s + t for s, t in zip(U, V)]; ops['add'] += 1
    assert held[nm] == [lp * t for t in true[nm]]
lamN = F(1, 2 ** (k // 2))
rows = {tuple(-1 if bin(w & x).count('1') & 1 else 1 for x in range(N)) for w in range(N)}
outs = {tuple(t / lamN for t in held[nm]) for nm, *_ in prog if nm.startswith('y')}
assert outs == rows
tot = ops['add'] + ops['mul']
print('N', N, 'gates of the form -u-v (would need a negation):', ops.get('negneg', 0), 'count (O): additions/subtractions', ops['add'], 'multiplications', ops['mul'], 'total', tot, '(outputs = H x / %d)' % (2 ** (k // 2)),
      '| exact H x: total', tot + N, '| textbook', N * k, '| 7/8 N log N =', 7 * N * k / 8, '| 23/24 N log N + 13/12 N =', round(23 * N * k / 24 + 13 * N / 12, 1))
