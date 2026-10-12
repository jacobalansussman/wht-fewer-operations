#!/usr/bin/env python3
"""Independent checker for an oslp_<N>.txt file (shares no code with the generators).  Reads lines  t = u + v | t = u - v | t = c * u,
counts one operation per line, runs them on the N unit vectors with exact Fractions, and checks that the values of the names
starting with 'y' are, as a set, exactly the N rows of the Walsh-Hadamard matrix divided by the stated power of two, each once."""
import sys, re
from fractions import Fraction
path = sys.argv[1]; N = int(re.search(r'oslp_(\d+)', path).group(1))
val = {}
for i in range(N): val['x%d' % i] = tuple(Fraction(1 if i == j else 0) for j in range(N))
nops = {'+': 0, '-': 0, '*': 0}; outs = []
for line in open(path):
    line = line.strip()
    if not line or line[0] == '#': continue
    m = re.fullmatch(r'(\w+) = (\S+) ([+\-*]) (\S+)', line); assert m, line
    t, a, op, b = m.groups(); assert t not in val, 'name reused'
    if op == '*': val[t] = tuple(Fraction(a) * z for z in val[b])
    elif op == '+': val[t] = tuple(p + q for p, q in zip(val[a], val[b]))
    else: val[t] = tuple(p - q for p, q in zip(val[a], val[b]))
    nops[op] += 1
    if t[0] == 'y': outs.append(val[t])
for d in (1, 2, 4, 8, 16, 32):
    rows = sorted(tuple(Fraction((-1) ** bin(w & x).count('1'), d) for x in range(N)) for w in range(N))
    if sorted(outs) == rows:
        print(path, 'N', N, 'operations', sum(nops.values()), nops, ': outputs are exactly the', N, 'rows of H /', d, '| textbook count for H:', N * (N.bit_length() - 1)); break
else: print(path, 'FAIL')
