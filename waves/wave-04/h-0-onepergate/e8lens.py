#!/usr/bin/env python3
"""h-0 onepergate / e8lens.py : the 240 stabiliser wires at 8 points as two copies of the E8 root system, and the angle of every gate.
Exact: inner products and squared lengths are integers; cos^2 of the angle between u and v is <u,v>^2 / (<u,u><v,v>) as a Fraction.
copy A = pair wires and full sign vectors with a quadratic sign rule;  copy B = single inputs and all sign patterns on half-cubes.
"""
import sys, itertools
from fractions import Fraction as F
sys.path.insert(0, 'waves/wave-03/g-1-tightwires')
from pool import build_pool
from ref import nz, wht, norm
sys.path.insert(0, 'waves/wave-04/h-0-onepergate')
import opg
pool = build_pool(3, 2); ws = sorted(pool)
A = [w for w in ws if nz(w) in (2, 8)]; B = [w for w in ws if nz(w) in (1, 4)]
def dot(u, v): return sum(a * b for a, b in zip(u, v))
def cos2(u, v): return F(dot(u, v) ** 2, dot(u, u) * dot(v, v))
print('stabiliser wires (up to sign): %d = copy A %d + copy B %d' % (len(ws), len(A), len(B)))
for nm, S in (('A', A), ('B', B)):
    vals = {}
    for u, v in itertools.combinations(S, 2): c = cos2(u, v); vals[c] = vals.get(c, 0) + 1
    deg = sorted({sum(1 for v in S if v != u and cos2(u, v) == F(1, 4)) for u in S})
    print('  copy %s: cos^2 between different wires: %s ; each wire is at 60 degrees to %s others (E8: 120 lines, cos^2 in {0, 1/4}, 56 neighbours)' % (nm, {str(k): v for k, v in sorted(vals.items())}, deg))
vals = {}
for u in A:
    for v in B: c = cos2(u, v); vals[c] = vals.get(c, 0) + 1
print('  between the copies: cos^2 values', {str(k): v for k, v in sorted(vals.items())})
SA = set(A); SB = set(B)
swap = all(norm(wht(w)) in SB for w in A) and all(norm(wht(w)) in SA for w in B)
print('  the transform swaps the two copies:', swap)
tight = lambda w: nz(w) * nz(wht(w)) == 8
print('  tight wires: copy A %d, copy B %d ; over-limit: copy A %d, copy B %d' % (sum(map(tight, A)), sum(map(tight, B)), sum(1 for w in A if not tight(w)), sum(1 for w in B if not tight(w))))
def kind(v):
    w = norm([int(z) for z in v])
    return 'A' if w in SA else ('B' if w in SB else '-')
I = 'waves/wave-04/'
for path in (I + 'g-1-tightwires/h8_19gates.txt', I + 'e2-0-pieces/slp_8.txt', I + 'e-2-density/h8_21gates.txt', I + 'e2-3-drain/h8_21gates_drain.txt'):
    gates, alias = opg.parse(path); val = opg.evaluate(gates, alias, 8); hist = {}; outside = 0
    for name, tt in gates:
        u = alias.get(tt[0][1], (1, tt[0][1]))[1]; v = alias.get(tt[1][1], (1, tt[1][1]))[1]
        iu = [int(z) for z in val[u]]; iv = [int(z) for z in val[v]]
        c = cos2(iu, iv); key = (kind(val[u]) + kind(val[v]) + '>' + kind(val[name]), str(c)); hist[key] = hist.get(key, 0) + 1
        if kind(val[name]) == '-': outside += 1
    print('%s: %d gates, %d gate wires outside both copies' % (path.split('/')[-1], len(gates), outside))
    for key in sorted(hist): print('      inputs in copies %s, cos^2 of the angle between the two inputs = %s : %d gates' % (key[0], key[1], hist[key]))
