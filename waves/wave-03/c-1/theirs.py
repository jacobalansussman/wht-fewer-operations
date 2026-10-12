#!/usr/bin/env python3
"""c-1 (critic): replay e2-0's own files with my own parser and exact Fractions.
(G) files slp_<N>.txt: lines  name = a * u + b * v.   (O) files oslp_<N>.txt: lines  t = u + v | t = u - v | t = c * u.
Checks: each line uses only earlier names; the names starting with y are N different rows of H (times one common factor for (O));
also: is the multiset of wires of my own program (mine_<N>.txt) the same as theirs?"""
import sys, re
from fractions import Fraction as F
E = 'waves/wave-02/e2-0-pieces/'
def rowcheck(outs, N, k):
    f = outs[0][0]; seen = set()
    for v in outs:
        assert v[0] == f
        w = sum(1 << i for i in range(k) if v[1 << i] == -f)
        assert v == [f * (1 - 2 * (bin(w & x).count('1') & 1)) for x in range(N)], 'not a row'
        seen.add(w)
    assert len(seen) == N == len(outs)
    return f
for N in (4, 8, 16, 32, 64):
    k = N.bit_length() - 1
    val = {'x%d' % i: [F(int(i == j)) for j in range(N)] for i in range(N)}; n = 0; coefs = set(); outs = []
    for l in open(E + 'slp_%d.txt' % N):
        l = l.split('#')[0].strip()
        if not l: continue
        m = re.fullmatch(r'(\w+) = (\S+) \* (\w+) \+ (\S+) \* (\w+)', l); assert m, l
        t, a, u, b, v = m.groups(); assert t not in val
        a = F(a); b = F(b); assert a != 0 and b != 0
        val[t] = [a * p + b * q for p, q in zip(val[u], val[v])]; n += 1; coefs |= {abs(a), abs(b)}
        if t[0] == 'y': outs.append(val[t])
    f = rowcheck(outs, N, k)
    mine = {'x%d' % i: [int(i == j) for j in range(N)] for i in range(N)}
    for l in open('mine_%d.txt' % N):
        lhs, rhs = l.split('#')[0].split('='); t = rhs.split()
        mine[lhs.strip()] = [int(t[0]) * p + int(t[4]) * q for p, q in zip(mine[t[2]], mine[t[6]])]
    same = sorted(tuple(int(z) for z in v) for v in val.values()) == sorted(tuple(v) for v in mine.values())
    print('(G) their slp_%d.txt: %d gates, coefficients %s, outputs = the %d rows of H times %s, each once: True | same set of wires as my program: %s' % (N, n, sorted(str(c) for c in coefs), N, f, same))
for N in (4, 16, 64):
    k = N.bit_length() - 1
    val = {'x%d' % i: [F(int(i == j)) for j in range(N)] for i in range(N)}; cnt = {'+': 0, '-': 0, '*': 0}; outs = []; consts = set()
    for l in open(E + 'oslp_%d.txt' % N):
        l = l.split('#')[0].strip()
        if not l: continue
        m = re.fullmatch(r'(\w+) = (\S+) ([+\-*]) (\w+)', l); assert m, l
        t, a, op, b = m.groups(); assert t not in val
        if op == '*': val[t] = [F(a) * z for z in val[b]]; consts.add(a)
        elif op == '+': val[t] = [p + q for p, q in zip(val[a], val[b])]
        else: val[t] = [p - q for p, q in zip(val[a], val[b])]
        cnt[op] += 1
        if t[0] == 'y': outs.append(val[t])
    f = rowcheck(outs, N, k)
    print('(O) their oslp_%d.txt: %d operations %s, constants %s, outputs = the %d rows of H times %s, each once: True | H x itself would need %d more multiplications: %d against the textbook %d'
          % (N, sum(cnt.values()), cnt, sorted(consts), N, f, N, sum(cnt.values()) + N, N * k))
