#!/usr/bin/env python3
# j-cross / budget.py : test of the guess "gates saved below N log2 N <= (1/2) * sum over wires of log2(s*s'/N)"
# on the two 21-gate 8-point circuits of the second wave (e-2-density, e2-3-drain), and on e2-0's family (from meters.out).
# s = non-zeros of the wire written in the inputs, s' = non-zeros written in the outputs (its Walsh-Hadamard transform).
import re, math
from fractions import Fraction as F
B = 'waves/wave-02/'
def wht(v):
    v = list(v); n = len(v); h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                a, b = v[j], v[j + h]; v[j], v[j + h] = a + b, a - b
        h *= 2
    return v
def ent(v, k):
    n = len(v); out = []
    for b in range(k):
        idx = [i for i in range(n) if not (i >> b) & 1]
        lo = [v[i] for i in idx]; hi = [v[i | (1 << b)] for i in idx]
        piv = next(j for j in range(len(lo)) if lo[j] != 0 or hi[j] != 0)
        if any(lo[piv] * hi[j] - hi[piv] * lo[j] != 0 for j in range(len(lo))): out.append(b)
    return out
def report(name, N, wires):
    k = N.bit_length() - 1
    rows = {tuple(F((-1) ** bin(w & x).count('1')) for x in range(N)) for w in range(N)}
    vals = [v for (_, v) in wires]
    def norm(v):
        p = next(z for z in v if z != 0); return tuple(z / p for z in v)
    assert {norm(r) for r in rows} <= {norm(v) for v in vals}, 'not every row of H is a wire (up to scale)'
    tot = F(0); lines = []
    for (t, v) in wires:
        s = sum(1 for z in v if z != 0); s2 = sum(1 for z in wht(v) if z != 0); P = s * s2
        if P != N:
            lines.append('%s s=%d s\'=%d s*s\'/N=%s entangled bits %s' % (t, s, s2, F(P, N), ent(v, k)))
            tot += F(math.log2(P / N)).limit_denominator(10**6)
    sav = N * k - len(wires)
    print('%s: N=%d gates=%d saving=%d | wires not tight: %d | (1/2)*sum log2(s*s\'/N) = %.3f  -> guess %s'
          % (name, N, len(wires), sav, len(lines), float(tot) / 2, 'HOLDS' if float(tot) / 2 >= sav - 1e-9 else 'BROKEN'))
    for l in lines: print('     ', l)
# e2-3-drain format: n8 = (1)*n0 + (1)*n1   = [..]
N = 8; val = {'n%d' % i: tuple(F(int(i == j)) for j in range(N)) for i in range(N)}; wires = []
for line in open(B + 'e2-3-drain/h8_21gates_drain.txt'):
    m = re.match(r'(n\d+) = \((\S+)\)\*(n\d+) \+ \((\S+)\)\*(n\d+)', line)
    if not m: continue
    t, a, u, b, v = m.groups(); val[t] = tuple(F(a) * p + F(b) * q for p, q in zip(val[u], val[v])); wires.append((t, val[t]))
report('e2-3-drain 21', N, wires)
# e-2-density format: g8  = x3 - x5 ; g15 = g14 + 2*x5 ; g22 = -g16 + 2*g12
val = {'x%d' % i: tuple(F(int(i == j)) for j in range(N)) for i in range(N)}; wires = []
def term(s):
    s = s.strip(); sg = 1
    if s[0] == '-': sg = -1; s = s[1:].strip()
    elif s[0] == '+': s = s[1:].strip()
    if '*' in s: c, n = s.split('*'); return sg * F(c), n.strip()
    return F(sg), s
for line in open(B + 'e-2-density/h8_21gates.txt'):
    line = line.split('#')[0].strip()
    m = re.fullmatch(r'(g\d+)\s*=\s*(-?\s*[\w*]+)\s*([+-])\s*([\w*]+)', line)
    if not m: continue
    t, A, op, Bt = m.groups(); a, u = term(A); b, v = term(op + Bt)
    val[t] = tuple(a * p + b * q for p, q in zip(val[u], val[v])); wires.append((t, val[t]))
report('e-2-density 21', N, wires)
