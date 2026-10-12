#!/usr/bin/env python3
"""collapse.py (ag-8): the class shapes with 8 gates at 4 points that have NO irredundant circuit at the transform: what happens to
them at tau = -1?  For each such shape take its labelled specimen (found at tau = 11 modulo 13), and solve the same wiring with the
same names EXACTLY (fractions) at tau = -1 and, as a control, at tau = 3.
  YES            : all 12 points exist and every gate is a true gate (then the circuit is redundant at the transform, or has twins)
  YES-DEGENERATE : coefficients exist but some gate has become a copy of one of its operands, or reads the same wire twice:
                   a gate has DIED (its coefficient is a multiple of 1 + tau)
  NO             : no coefficients at tau = -1 in this labelling (the circuit exists only as a limit: a coefficient has a pole)
  UNDECIDED      : the linear propagation stalls
Also, for the shapes that DO occur at the transform, the same tally (control: expect YES)."""
import pickle, sys
from fractions import Fraction as F
import wsolve
from wsolve import solve, MODE
r = pickle.load(open('cen2_13_4_11.pkl', 'rb')); m = r['m']; T0 = 4 + m
Hshapes = set(r['HS'])
def run(pts, w, tau):
    done = set(range(4)); order = []; rest = sorted(w)
    while rest:
        for c in rest:
            if w[c][0] in done and w[c][1] in done: order.append(c); done.add(c); rest.remove(c); break
    nm = lambda n: 'x%d' % n if n < 4 else ('T%d' % n if n >= T0 else 'h%d' % n)
    gates = [(nm(c), nm(w[c][0]), nm(w[c][1])) for c in order]; out = {nm(T0 + i): i for i in range(4)}
    MODE['q'] = True
    try: q = solve(4, gates, out, F(tau))
    finally: MODE['q'] = False
    return q, gates
tal = {}; ex = {}
for c, (pts, w) in r['G'].items():
    kind = 'occurs at the transform' if c in Hshapes else 'absent at the transform'
    q3, gates = run(pts, w, 3); q1, _ = run(pts, w, -1)
    key = (kind, 'tau=3: ' + q3[0], 'tau=-1: ' + q1[0]); tal[key] = tal.get(key, 0) + 1
    if key not in ex: ex[key] = (gates, q1[1].get('deg') if q1[0] == 'YES-DEGENERATE' else None, q1[1].get('pts') if q1[0].startswith('YES') else None)
for k, v in sorted(tal.items()): print(v, k)
print()
for k, (gates, deg, pts) in sorted(ex.items()):
    print(k); print('   wiring:', ' '.join('%s<-(%s,%s)' % g for g in gates))
    if deg: print('   dead gates at tau=-1:', deg)
    if pts: print('   points at tau=-1:', {n: tuple(str(x) for x in p) for n, p in pts.items() if not n.startswith('x')})
