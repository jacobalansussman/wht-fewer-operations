#!/usr/bin/env python3
"""b-0: replay e2-0's program FILES with my own reader (pure Python, exact Fractions).  slp_<N>.txt: lines 'n = a * u + b * v' (count G,
one gate per line).  oslp_<N>.txt: lines 'n = u + v', 'n = u - v', 'n = c * u' (count O, one operation per line)."""
import sys, re
from fractions import Fraction as Fr
D = 'waves/wave-02/e2-0-pieces/'
def rows(N, d): return sorted(tuple(Fr(-1 if bin(w & x).count('1') & 1 else 1, d) for x in range(N)) for w in range(N))
for N in (4, 8, 16, 32, 64):
    val = {'x%d' % i: [Fr(int(i == j)) for j in range(N)] for i in range(N)}; n = 0; outs = []; cf = set()
    for line in open(D + 'slp_%d.txt' % N):
        line = line.split('#')[0].strip()
        if not line: continue
        m = re.fullmatch(r'(\w+) = (\S+) \* (\w+) \+ (\S+) \* (\w+)', line); assert m, line
        t, a, u, b, v = m.groups(); a = Fr(a); b = Fr(b); assert t not in val and a and b
        val[t] = [a * p + b * q for p, q in zip(val[u], val[v])]; n += 1; cf |= {abs(a), abs(b)}
        if t[0] == 'y': outs.append(tuple(val[t]))
    print('G file slp_%d.txt: %d gates, |coefficients| %s, outputs are exactly the %d rows of H: %s' % (N, n, sorted(map(str, cf)), N, sorted(outs) == rows(N, 1)))
for N in (4, 16, 64):
    val = {'x%d' % i: [Fr(int(i == j)) for j in range(N)] for i in range(N)}; c = {'+': 0, '-': 0, '*': 0}; outs = []; consts = set()
    for line in open(D + 'oslp_%d.txt' % N):
        line = line.split('#')[0].strip()
        if not line: continue
        m = re.fullmatch(r'(\w+) = (\S+) ([-+*]) (\w+)', line); assert m, line
        t, a, op, b = m.groups(); assert t not in val
        if op == '*': val[t] = [Fr(a) * q for q in val[b]]; consts.add(a)
        elif op == '+': val[t] = [p + q for p, q in zip(val[a], val[b])]
        else: val[t] = [p - q for p, q in zip(val[a], val[b])]
        c[op] += 1
        if t[0] == 'y': outs.append(tuple(val[t]))
    d = [d for d in (1, 2, 4, 8, 16) if sorted(outs) == rows(N, d)]
    print('O file oslp_%d.txt: %d operations %s, constants %s, outputs are exactly the rows of H divided by %s' % (N, sum(c.values()), c, sorted(consts), d))
