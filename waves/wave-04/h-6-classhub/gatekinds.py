#!/usr/bin/env python3
"""h-6-classhub / gatekinds.py : read the tau-programs as moves on EXPONENT TABLES.  Every wire is tau^(e(x)) on its support
(coefficient 1; checked: exponents read at tau = 2 and tau = 3 agree).  A wire is then a partial integer table e, up to adding a constant.
For each gate w from u, v:  'join' = supports disjoint;  'shift +1' / 'shift -1' = one input's support lies inside the other's and
w equals the bigger wire with its exponents raised / lowered by one exactly on the smaller support;  'other' = anything else.
usage: gatekinds.py k | gatekinds.py 19"""
import sys
from fractions import Fraction as F
arg = sys.argv[1]
if arg == '19':
    src = open('limit19.py').read(); src = src[src.index('def build19'):src.index('p2, v2, ok2')]; ns = {'F': F}; exec(src, ns); b = ns['build19']; N = 8
else:
    from gen_tau import build
    k = int(arg); N = 1 << k; b = lambda t: build(k, t)
def expo(vec, base):
    out = {}
    for nm in vec:
        e = []
        for t in vec[nm]:
            if t == 0: e.append(None); continue
            t = F(t); a = 0
            while t > 1: t /= base; a += 1
            while t < 1: t *= base; a -= 1
            assert t == 1; e.append(a)
        out[nm] = e
    return out
p2, v2, _ = b(F(2)); p3, v3, _ = b(F(3)); E = expo(v2, 2); assert E == expo(v3, 3)
kinds = {}; nonlin = 0
for nm, a, u, v_, in [(g[0], g[1], g[2], g[4]) for g in p2]:
    eu, ev, ew = E[u], E[v_], E[nm]
    su = {x for x in range(N) if eu[x] is not None}; sv = {x for x in range(N) if ev[x] is not None}
    if not su & sv: kind = 'join'
    else:
        big, small, eb = (su, sv, eu) if sv <= su else (sv, su, ev)
        if not small <= big: kind = 'other'
        else:
            off = {ew[x] - eb[x] for x in big - small}; on = {ew[x] - eb[x] for x in small}
            kind = 'shift %+d' % (on.pop() - off.pop()) if len(off) == 1 and len(on) == 1 else 'other'
    kinds[kind] = kinds.get(kind, 0) + 1
print('program', arg, '| N', N, '| gates', len(p2), '| kinds of gate:', dict(sorted(kinds.items())))
