#!/usr/bin/env python3
"""h-1 checkt.py: exact replay of a helper set for a HALF problem (an arbitrary list of target wires).  Count (G).
Finds an order in which every helper and every target is a*u + b*v (a, b rational, solved exactly) of two wires derived before,
replays from the inputs with Fractions and requires every target to come out exactly (as the listed integer vector).
usage: checkt.py helpers.txt targets.txt K"""
import sys
from fractions import Fraction as F
fn, tn, K = sys.argv[1], sys.argv[2], int(sys.argv[3]); N = 1 << K
rd = lambda f: [tuple(int(t) for t in l.split()) for l in open(f) if l.strip() and l[0] != '#']
H, T = rd(fn), rd(tn)
def solve2(u, v, p):
    for i in range(N):
        for j in range(i + 1, N):
            det = u[i] * v[j] - u[j] * v[i]
            if det:
                a = F(p[i] * v[j] - p[j] * v[i], det); b = F(u[i] * p[j] - u[j] * p[i], det)
                return (a, b) if all(a * u[t] + b * v[t] == p[t] for t in range(N)) else None
    return None
have = [('x%d' % i, tuple(int(i == j) for j in range(N))) for i in range(N)]
todo = [('h%d' % i, w) for i, w in enumerate(dict.fromkeys(H)) if w not in T] + [('t%d' % i, w) for i, w in enumerate(T)]
prog = []; ch = True
while todo and ch:
    ch = False; rest = []
    for nm, w in todo:
        hit = None
        for i in range(len(have)):
            for j in range(i):
                s = solve2(have[i][1], have[j][1], w)
                if s and s[0] != 0 and s[1] != 0: hit = (s[0], have[i][0], s[1], have[j][0]); break
            if hit: break
        if hit: prog.append((nm, hit, w)); have.append((nm, w)); ch = True
        else: rest.append((nm, w))
    todo = rest
if todo: print('%s: NOT derivable (%d wires left)' % (fn, len(todo))); sys.exit(1)
val = {'x%d' % i: [F(int(i == j)) for j in range(N)] for i in range(N)}
for nm, (a, u, b, v), w in prog: val[nm] = [a * s + b * t for s, t in zip(val[u], val[v])]
ok = all(tuple(val['t%d' % i]) == T[i] for i in range(len(T)))
print('%s: N=%d targets=%d gates(G)=%d  every target exact: %s' % (fn, N, len(T), len(prog), ok))
