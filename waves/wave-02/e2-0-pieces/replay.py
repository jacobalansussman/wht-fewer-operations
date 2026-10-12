#!/usr/bin/env python3
"""Independent exact replay of a candidate program, count (G): a gate is any a*u + b*v (a, b rational), scalings free.
Input: a list of helper vectors (the outputs are added).  This file shares no code with walk.py.
It (1) finds an order in which every point is a rational combination a*u + b*v of two EARLIER points (solving for a, b
exactly with Fractions), (2) writes the straight-line program, (3) runs it on symbolic inputs (rows of the identity) and on
random integer inputs, and compares every output with the corresponding row of the Walsh-Hadamard matrix times a non-zero scalar."""
import sys, json, random
from fractions import Fraction as F
from itertools import combinations
def solve2(u, v, p):
    """a, b with a*u + b*v == p exactly, or None"""
    n = len(p)
    for i in range(n):
        for j in range(n):
            det = u[i] * v[j] - u[j] * v[i]
            if det:
                a = F(p[i] * v[j] - p[j] * v[i], det); b = F(u[i] * p[j] - u[j] * p[i], det)
                return (a, b) if all(a * u[k] + b * v[k] == p[k] for k in range(n)) else None
    return None
def run(helpers, n=8, label=''):
    H = [[(-1) ** bin(w & x).count('1') for x in range(n)] for w in range(n)]
    targets = [tuple(r) for r in H] + [tuple(h) for h in helpers]
    assert len(set(targets)) == len(targets)
    held = [tuple(int(i == x) for i in range(n)) for x in range(n)]
    names = ['x%d' % i for i in range(n)]; prog = []; todo = list(targets)
    while todo:
        for p in todo:
            hit = None
            for i, j in combinations(range(len(held)), 2):
                s = solve2(held[i], held[j], p)
                if s and s[0] != 0 and s[1] != 0: hit = (i, j, s); break
            if hit:
                i, j, (a, b) = hit
                nm = ('y%d' % targets.index(p)) if targets.index(p) < n else 'h%d' % (len(prog) + 1)
                prog.append((nm, a, names[i], b, names[j])); held.append(p); names.append(nm); todo.remove(p); break
        else:
            print(label, 'STUCK: not derivable:', todo); return None
    # replay from scratch, symbolic
    val = {'x%d' % i: [F(int(i == x)) for x in range(n)] for i in range(n)}
    for nm, a, u, b, v in prog: val[nm] = [a * s + b * t for s, t in zip(val[u], val[v])]
    okS = all(val['y%d' % w] == [F(c) for c in H[w]] for w in range(n))
    rng = random.Random(5); okR = True
    for _ in range(20):
        x = [rng.randrange(-10**6, 10**6) for _ in range(n)]
        v2 = {'x%d' % i: F(x[i]) for i in range(n)}
        for nm, a, u, b, v in prog: v2[nm] = a * v2[u] + b * v2[v]
        okR &= all(v2['y%d' % w] == sum(H[w][i] * x[i] for i in range(n)) for w in range(n))
    print(label, 'gates', len(prog), '(helpers %d + outputs %d)' % (len(prog) - n, n), 'symbolic replay', okS, 'random replay', okR)
    for nm, a, u, b, v in prog: print('   %-4s = %s*%s + %s*%s    %s' % (nm, a, u, b, v, tuple(int(c) for c in val[nm])))
    return prog
if __name__ == '__main__':
    P20 = [(0,0,0,0,0,0,1,1), (0,0,0,0,1,-1,0,0), (0,0,1,1,0,0,0,0), (1,-1,0,0,0,0,0,0),
           (0,0,0,0,1,-1,-1,-1), (0,0,0,0,1,-1,1,-1), (0,0,0,0,1,1,1,1),
           (1,-1,-1,-1,0,0,0,0), (1,-1,-1,1,0,0,0,0), (1,1,-1,-1,0,0,0,0),
           (1,-1,-1,1,-1,1,-1,1), (1,1,-1,-1,-1,-1,-1,-1)]
    run(P20, 8, 'P20')
