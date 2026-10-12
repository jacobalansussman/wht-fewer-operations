#!/usr/bin/env python3
# h-5 / tp4.py : 4 points, count (G), over GF(p).  Pool A = product wires (a 2-vector on each bit) + "tight" wires
# (s*s' = 4: inputs, outputs, e_a +- e_b, including the two-bit-entangled ones (1,0,0,+-1), (0,1,+-1,0)).
# Question: is there a 7-gate program (3 helpers) whose wires are all tight OR product?  Control: whole space (answer must be yes: the hub).
import sys, itertools
p = int(sys.argv[1])
def norm(v):
    v = [x % p for x in v]
    for x in v:
        if x:
            inv = pow(x, p - 2, p); return tuple(y * inv % p for y in v)
    return None
E = [norm([int(i == j) for j in range(4)]) for i in range(4)]
Y = [norm([(-1) ** bin(i & j).count('1') for j in range(4)]) for i in range(4)]
P1 = [(1, a) for a in range(p)] + [(0, 1)]
prod = {norm([a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]) for a in P1 for b in P1}
bell = {norm(v) for v in [(1, 0, 0, 1), (1, 0, 0, -1), (0, 1, 1, 0), (0, 1, -1, 0)]}
allpts = {norm(v) for v in itertools.product(range(p), repeat=4) if any(v)}
def third(u, v):
    return {norm([x + a * y for x, y in zip(u, v)]) for a in range(1, p)}
def ok(helpers):
    D = set(E); todo = set(helpers) | set(Y)
    ch = True
    while ch and todo:
        ch = False
        Dl = list(D)
        reach = set()
        for i, u in enumerate(Dl):
            for v in Dl[i + 1:]: reach |= third(u, v)
        for w in list(todo):
            if w in reach: D.add(w); todo.discard(w); ch = True
    return not todo
for name, pool in (('product', prod), ('product+tight', prod | bell), ('everything', allpts)):
    cand = sorted(pool - set(E) - set(Y))
    for h in range(0, 5):
        hit = None; n = 0
        for H in itertools.combinations(cand, h):
            n += 1
            if ok(H): hit = H; break
        print('p=%d pool=%s (%d candidates) gates=%d: %s (%d sets tried)' % (p, name, len(cand), 4 + h, 'REACHED %s' % (hit,) if hit else 'none', n), flush=True)
        if hit: break
