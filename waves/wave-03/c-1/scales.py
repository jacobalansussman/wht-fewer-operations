#!/usr/bin/env python3
"""c-1 (critic): is e2-0's scale rule the cheapest way to price ITS OWN gate list in count (O)?
Keep the wiring of my count-(G) program (mine_<N>.txt, same gates as e2-0's slp_<N>.txt).  Every wire X may be held as 2^t(X) * X
with any integer t(X) (inputs: t = 0).  A gate P = a*U + b*V then reads  held(P) = a*2^(tP-tU) * held(U) + b*2^(tP-tV) * held(V).
Price: 1 per gate, plus 1 for every different pair (wire, |factor|) with |factor| != 1 (one multiplication makes that copy; shared).
No gate of the list has two negative coefficients, so signs never cost.
Target 'exact': every output has t = 0 (H x itself).  Target 'common': all outputs share one free t.
Search: simulated annealing with restarts over t in [-R, R].  A LOCAL search: the minimum found is an upper bound, not a proof.
usage: scales.py N restarts seed"""
import sys, random, math
N = int(sys.argv[1]); restarts = int(sys.argv[2]); random.seed(int(sys.argv[3]))
gates = []; kind = {}
for l in open('waves/wave-03/c-1/mine_%d.txt' % N):
    lhs, rhs = l.split('#')[0].split('='); t = rhs.split(); kd = l.split('#')[1].strip()
    gates.append((lhs.strip(), int(t[0]), t[2], int(t[4]), t[6])); kind[lhs.strip()] = kd
names = [g[0] for g in gates]
val = {'x%d' % i: [int(i == j) for j in range(N)] for i in range(N)}
for nm, a, u, b, v in gates: val[nm] = [a * p + b * q for p, q in zip(val[u], val[v])]
parent = {nm: u for nm, a, u, b, v in gates}
def rule(nm):          # e2-0's rule: support 2^j held at 2^(-floor(j/2)); a hub at the scale of its first input
    if kind[nm] == 'hub': return rule(parent[nm]) if parent[nm] in kind else 0
    return -((sum(1 for t in val[nm] if t).bit_length() - 1) // 2)
START = sys.argv[4] if len(sys.argv) > 4 else 'random'
helpers = [n for n in names if kind[n] != 'y']; outs = [n for n in names if kind[n] == 'y']
k = N.bit_length() - 1; R = k
def cost(t):
    copies = set()
    for nm, a, u, b, v in gates:
        for c, w in ((a, u), (b, v)):
            e = t[nm] - t.get(w, 0) + (1 if abs(c) == 2 else 0)
            if e: copies.add((w, e))
    return len(gates) + len(copies)
def anneal(target):
    best = None
    for r in range(restarts):
        t = {n: (rule(n) if START == 'rule' else random.randint(-R, 0)) for n in helpers}
        t0 = (-(k // 2) if (START == 'rule' and target == 'common') else 0)
        for n in outs: t[n] = t0
        free = list(helpers) + (['*out*'] if target == 'common' else [])
        c = cost(t); T = 2.0
        TOP = 0.6 if START == 'rule' else 2.0
        if best is None or c < best[0]: best = (c, dict(t))
        if r == 0: print('  start', START, 'target', target, 'cost at the start', c, flush=True)
        steps = 4000 * len(free) // 10
        for s in range(steps):
            T = TOP * (1 - s / steps) + 0.05
            n = random.choice(free); d = random.choice((-1, 1))
            if n == '*out*':
                for o in outs: t[o] += d
            else: t[n] += d
            c2 = cost(t)
            if c2 <= c or random.random() < math.exp((c - c2) / T): c = c2
            else:
                if n == '*out*':
                    for o in outs: t[o] -= d
                else: t[n] -= d
            if best is None or c < best[0]: best = (c, dict(t))
    return best
for target in ('common', 'exact'):
    c, t = anneal(target)
    lv = sorted({t[o] for o in outs})
    print('N', N, 'target', target, ': cheapest pricing found', c, 'operations (gates %d + scaled copies %d); output exponents' % (len(gates), c - len(gates)), lv,
          '| e2-0 rule:', {'common': {4: 8, 8: 26, 16: 60, 32: 160, 64: 352}, 'exact': {4: 12, 8: 34, 16: 76, 32: 192, 64: 416}}[target].get(N), '| textbook for H x:', N * k, flush=True)
