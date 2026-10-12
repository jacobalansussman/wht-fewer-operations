#!/usr/bin/env python3
"""nb.py -- neighbour sums for the annealer slp.py (count (G): a gate is any a*u + b*v, scalings free).
Targets:  B<k>      one block of the neighbour-sum matrix A at 2^k points: outputs = odd addresses, inputs = even addresses
          A<k>c<c>  the whole matrix A + c*identity at 2^k points
Seed circuit: the pairing circuit (adding only), which section 1 of ab-0.md shows is the least adding-only circuit.
usage: nb.py <target> <K gates> <seconds> <seed> <outdir> [mode] [temp]     (same as slp.py)
       nb.py check <target>       exact replay of the seed circuit, prints its gate count
"""
import sys, numpy as np
sys.path.insert(0, sys.path[0] + '/../j-machine')
sys.path.insert(0, '.')
import slp
from fractions import Fraction

def wt(x): return bin(x).count('1')

def build(name):
    if name[0] == 'B':
        k = int(name[1:]); N = 1 << k
        ins = [x for x in range(N) if wt(x) % 2 == 0]; outs_addr = [y for y in range(N) if wt(y) % 2 == 1]; c = 0
    else:
        k, c = name[1:].split('c'); k = int(k); c = int(c); N = 1 << k
        ins = list(range(N)); outs_addr = list(range(N))
    idx = {x: i for i, x in enumerate(ins)}; n = len(ins)
    T = np.zeros((len(outs_addr), n))
    for r, y in enumerate(outs_addr):
        for j in range(k): T[r, idx[y ^ (1 << j)]] = 1
        if c: T[r, idx[y]] = c
    # pairing circuit: directions (0,1),(2,3),...; pair gate x(y+e_a)+x(y+e_b) serves y and y+e_a+e_b
    gates = []; base = n; pair = {}
    for a in range(0, k - 1, 2):
        ea, eb = 1 << a, 1 << (a + 1)
        for y in outs_addr:
            key = (a, min(y, y ^ ea ^ eb))
            if key not in pair:
                gates.append((idx[y ^ ea], idx[y ^ eb], 1., 1.)); pair[key] = base; base += 1
    outs = []
    for y in outs_addr:
        terms = [pair[(a, min(y, y ^ (1 << a) ^ (1 << (a + 1))))] for a in range(0, k - 1, 2)]
        if k % 2: terms.append(idx[y ^ (1 << (k - 1))])
        cur = terms[0]
        for t in terms[1:]:
            gates.append((cur, t, 1., 1.)); cur = base; base += 1
        if c:
            gates.append((cur, idx[y], 1., float(c))); cur = base; base += 1
        outs.append(cur)
    import os
    K = int(os.environ.get('NB_CHAIN', '0'))
    if K:      # a start that passes the annealer's support test: one wire holding every input, then one gate per output
        R = T.shape[0]; extra = K - (n - 1) - R; assert extra in (0, 1)
        gates = [(0, 1, 1., 1.)] + [(n + i, i + 2, 1., 1.) for i in range(n - 2)]; full = [n + n - 2]; base = n + n - 1
        if extra: gates.append((full[0], 0, 1., 1.)); full.append(base); base += 1
        outs = []
        for r in range(R):
            gates.append((full[r % len(full)], r % n, 1., -1.)); outs.append(base); base += 1
    return T, gates, outs

def check(name):
    T, gates, outs = build(name); n = T.shape[1]
    rows = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for (u, v, a, b) in gates:
        rows.append([Fraction(a) * rows[u][j] + Fraction(b) * rows[v][j] for j in range(n)])
    ok = all([rows[o][j] for j in range(n)] == [Fraction(int(x)) for x in T[r]] for r, o in enumerate(outs))
    print(name, 'inputs', n, 'outputs', T.shape[0], 'seed gates', len(gates), 'exact replay', ok,
          'rank', np.linalg.matrix_rank(T))

if __name__ == '__main__':
    if sys.argv[1] == 'check':
        for nm in sys.argv[2:]: check(nm)
    else:
        slp.task = build
        slp.main()
