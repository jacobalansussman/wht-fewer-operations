#!/usr/bin/env python3
"""e2-0-pieces: price of a count-(G) program in count (O) (every addition/subtraction 1, every multiplication by a constant 1).
Every point may be held at any power-of-two scale; a gate P = a*U + b*V computed at scale s_P needs a copy of U at scale
s_P + log2|a| and of V at s_P + log2|b|; the first copy of a point is free (it is where its gate lands; scale 0 for inputs), each
further copy costs one multiplication.  Outputs: 'exact' = every output also at scale 0; 'common' = any single common scale.
Minimised by simulated annealing over the gate scales (an UPPER bound on the (O) price of this program, not a proof of minimum).
usage: oprice.py slp_N.txt seconds"""
import sys, random, math, time
prog = []
for l in open(sys.argv[1]):
    if l.startswith('#'): continue
    lhs, rhs = l.split('#')[0].split('=')
    t = rhs.split()
    from fractions import Fraction as F
    a, u, b, v = F(t[0]), t[2], F(t[4]), t[6]
    lg = lambda c: {1: 0, 2: 1, F(1, 2): -1}[abs(c)]
    prog.append((lhs.strip(), lg(a), u, lg(b), v))
names = [p[0] for p in prog]; outs = [n for n in names if n.startswith('y')]
def cost(s, mode, shift=0):
    need = {}
    for nm, la, u, lb, v in prog:
        need.setdefault(u, set()).add(s[nm] + la); need.setdefault(v, set()).add(s[nm] + lb)
    for o in outs: need.setdefault(o, set()).add(shift if mode == 'common' else 0)
    c = 0
    for n, S in need.items():
        base = s.get(n, 0)          # inputs sit at scale 0
        c += len(S - {base})
    return c
rng = random.Random(1); secs = float(sys.argv[2])
for mode in ('exact', 'common'):
    best = None; t0 = time.time()
    while time.time() - t0 < secs / 2:
        s = {n: rng.randint(-2, 2) for n in names}; shift = rng.randint(-3, 3); c = cost(s, mode, shift); T = 1.0
        for it in range(6000):
            n = rng.choice(names); old = s[n]; s[n] = old + rng.choice((-1, 1)); c2 = cost(s, mode, shift)
            if c2 <= c or rng.random() < math.exp((c - c2) / T): c = c2
            else: s[n] = old
            T = max(0.02, T * 0.999)
            if best is None or c < best[0]: best = (c, dict(s), shift)
    print(sys.argv[1], 'gates (G)', len(prog), 'outputs', mode, ': multiplications', best[0], '-> count (O) at most', len(prog) + best[0], flush=True)
