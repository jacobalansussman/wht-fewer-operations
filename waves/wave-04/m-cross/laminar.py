# m-cross: for each circuit that the meter accepted: are the supports modulo 2 of ALL wires one laminar family (any two nested or
# disjoint)?  how many wires per class?  are all wires sign vectors on their support?  exact.
import sys, re, glob, os
src = open(sys.argv[1]).read().split("for N in (4, 8, 16, 32)")[0]
exec(src)
files = [l.split()[0] for l in open(sys.argv[2]) if l.strip() and not l.startswith(('textbook', 'circuits', 'LIGHT', 'k-cross'))]
for rel in files:
    g = parse(rel); N = 1 + max(int(t[1:]) for (_, _, u, _, v) in g for t in (u, v) if re.fullmatch(r'x\d+', t))
    W = {'x%d' % i: [F(int(i == j)) for j in range(N)] for i in range(N)}
    for (name, a, u, b, v) in g: W[name] = [a * p + b * q for p, q in zip(W[u], W[v])]
    cls = {}
    signs = True; odd_ne_supp = 0
    for n, w in W.items():
        p = prim(w); c = canon(p, 1); cls.setdefault(c, []).append(n)
        if len({abs(t) for t in p if t != 0}) > 1: signs = False
        if sum(c) != sum(1 for t in w if t != 0): odd_ne_supp += 1
    sets = [frozenset(i for i in range(N) if c[i]) for c in cls]
    lam = all(a <= b or b <= a or not (a & b) for a in sets for b in sets)
    full = len(cls.get(tuple([1] * N), []))
    multi = sum(1 for c, ns in cls.items() if len(ns) > 1 and sum(c) < N)
    print('%-44s N=%2d classes=%3d (2N-1=%3d) laminar=%s  all wires one magnitude=%s  wires whose odd set is not their support=%d  full-support wires=%3d  smaller classes holding 2+ wires=%d'
          % (rel[-44:], N, len(cls), 2 * N - 1, lam, signs, odd_ne_supp, full, multi))
