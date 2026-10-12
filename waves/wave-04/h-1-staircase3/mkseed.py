#!/usr/bin/env python3
"""h-1 mkseed.py: turn a straight-line program file (lines 'name = a * u + b * v' or g-1's 'g1 = x0 + x7' style) into helper vectors.
usage: mkseed.py slpfile N > seedfile     (replays with fractions; prints every non-output wire as a 0/+-1 vector, scaled)"""
import sys, re
from fractions import Fraction as F
from math import gcd
fn, N = sys.argv[1], int(sys.argv[2])
val = {'x%d' % i: [F(int(i == j)) for j in range(N)] for i in range(N)}
def term(t):
    t = t.strip().replace(' ', '')
    m = re.fullmatch(r'([+-]?[\d/]*)\*?([A-Za-z]\w*)', t)
    c = m.group(1)
    c = F(1) if c in ('', '+') else F(-1) if c == '-' else F(c)
    return c, m.group(2)
rows = set()
for a in range(N): rows.add(tuple(-1 if bin(a & x).count('1') & 1 else 1 for x in range(N)))
out = []
for line in open(fn):
    line = line.split('#')[0].strip()
    if '=' not in line: continue
    nm, rhs = line.split('=')
    rhs = rhs.replace('+ -', '- ').replace('- -', '+ ')
    parts = re.findall(r'[+-]?[^+-]+', rhs.replace(' ', ''))
    assert len(parts) == 2, line
    (a, u), (b, v) = term(parts[0]), term(parts[1])
    w = [a * s + b * t for s, t in zip(val[u], val[v])]; val[nm.strip()] = w
    den = 1
    for t in w: den = den * t.denominator // gcd(den, t.denominator)
    iw = [int(t * den) for t in w]; g = 0
    for t in iw: g = gcd(g, abs(t))
    iw = tuple(t // g for t in iw)
    neg = tuple(-t for t in iw)
    if iw in rows or neg in rows: continue
    assert all(abs(t) <= 1 for t in iw), ('not a 0/+-1 wire', nm, iw)
    out.append(iw)
print('# helpers of %s' % fn)
for w in out: print(' '.join(map(str, w)))
