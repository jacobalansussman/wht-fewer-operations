# x-0-twojobs: turn a gate file (one gate a*u + b*v per line) into the list of its helper wires (primitive whole-number vectors,
# one per line), for tj.c.  Parser copied from s-cross/pmeter.py.   usage: prep.py gatefile > helpers.txt
import sys, re
from fractions import Fraction as Fr
from math import gcd
from functools import reduce
def prim(w):
    den = reduce(lambda a, b: a*b//gcd(a, b), [t.denominator for t in w], 1)
    iv = [int(t*den) for t in w]; g = reduce(gcd, [abs(t) for t in iv], 0)
    iv = [t//g for t in iv] if g else iv
    l = next((t for t in iv if t), 0)
    return tuple(iv) if l >= 0 else tuple(-t for t in iv)
def term(s):
    m = re.fullmatch(r'([+-]?)(?:([\d/]+)\*)?([A-Za-z_]\w*)', s)
    c = Fr(m.group(2)) if m.group(2) else Fr(1)
    return (-c if m.group(1) == '-' else c), m.group(3)
def load(path):
    gates = []
    for line in open(path):
        line = line.split('#')[0].strip()
        if '=' not in line: continue
        nm, rhs = line.split('=', 1); rhs = rhs.replace(' ', '')
        m = re.fullmatch(r'([+-]?(?:[\d/]+\*)?[A-Za-z_]\w*)([+-])(-?(?:[\d/]+\*)?[A-Za-z_]\w*)', rhs)
        a, u = term(m.group(1)); b, v = term(m.group(3))
        if m.group(2) == '-': b = -b
        gates.append((nm.strip(), a, u, b, v))
    return gates
gates = load(sys.argv[1])
N = 1 + max(int(t[1:]) for g in gates for t in (g[2], g[4]) if re.fullmatch(r'x\d+', t))
W = {'x%d' % i: [Fr(int(i == j)) for j in range(N)] for i in range(N)}
for (nm, a, u, b, v) in gates: W[nm] = [a*p + b*r for p, r in zip(W[u], W[v])]
H = {prim([Fr((-1)**bin(s & x).count('1')) for x in range(N)]) for s in range(N)}
I = {prim(W['x%d' % i]) for i in range(N)}
seen = set()
for nm, w in W.items():
    p = prim(w)
    if p in H or p in I or p in seen: continue
    seen.add(p); print(' '.join(map(str, p)))
sys.stderr.write('%s: N=%d gates=%d helpers=%d outputs present=%d\n' % (sys.argv[1].split('/')[-1], N, len(gates), len(seen), sum(1 for h in H if any(prim(w) == h for w in W.values()))))
