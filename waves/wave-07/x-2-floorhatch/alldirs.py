# x-2-floorhatch/alldirs.py : the top step of the floor's bookkeeping for EVERY one of the N - 1 ways to cut the addresses in two
# parallel halves (a cut c: L = addresses x with an even number of common ones with c, R = the others).  Count (G).  Exact.
# For every circuit and every cut:  gates = n(L) + n(R) - B + E ;  U = n(L) + n(R) - B = gates new on at least one half.
# Checked here on every cut [x-2.md section 2]:  E >= N/2 + 1  (the pairs of rows, and the first wire that crosses the cut).
# So gates >= U + N/2 + 1 >= (least count at N/2) + N/2 + 1 in EVERY circuit: without "one tree" the recursion keeps its N/2 + 1
# and loses the factor 2.  Printed: for each cut  n(L), n(R), B, E, the share B / min(n(L), n(R)), and the waste
# n(L) + n(R) - 2 f(N/2);  the identity is  e = waste - B + (E - N/2 - 1).
import sys, os
from math import gcd
os.chdir('waves/wave-06/u-8-compose'); exec(open('compose.py').read().split("if __name__ == '__main__':")[0])
def cut(v, X):
    c = [v[i] for i in X]; g = 0
    for t in c: g = gcd(g, t)
    if g == 0: return None
    s = next(t for t in c if t); s = g if s > 0 else -g
    return tuple(t // s for t in c)
def newset(vecs, X):
    seen = set(); nx = set()
    for g, v in enumerate(vecs):
        c = cut(v, X)
        if c is None or sum(1 for t in c if t) < 2 or c in seen: continue
        seen.add(c); nx.add(g)
    return nx
def fl(n): return n - 1 + (n // 2) * (n.bit_length() - 1)
def run(label, vecs, N, detail):
    t = len(vecs); rows = []
    for c in range(1, N):
        L = [x for x in range(N) if bin(x & c).count('1') % 2 == 0]; R = [x for x in range(N) if bin(x & c).count('1') % 2]
        nl, nr = newset(vecs, L), newset(vecs, R); B = len(nl & nr); E = t - len(nl | nr)
        assert E >= N // 2 + 1, (label, c, E)
        waste = len(nl) + len(nr) - 2 * fl(N // 2); assert t - fl(N) == waste - B + (E - N // 2 - 1)
        rows.append((c, len(nl), len(nr), B, E, waste))
    zero = sum(1 for r in rows if r[3] == 0)
    print('%-13s N=%2d gates=%3d e=%2d: cuts %d; cuts with B = 0: %d; B from %d to %d; E from %d to %d (N/2 + 1 = %d); largest share B/min(n) = %.2f; least waste %d, largest %d; least n(L) %d (floor at N/2: %d)'
          % (label, N, t, t - fl(N), N - 1, zero, min(r[3] for r in rows), max(r[3] for r in rows), min(r[4] for r in rows), max(r[4] for r in rows), N // 2 + 1,
             max(r[3] / min(r[1], r[2]) for r in rows), min(r[5] for r in rows), max(r[5] for r in rows), min(min(r[1], r[2]) for r in rows), fl(N // 2)))
    if detail:
        for r in rows: print('      cut %2d: n(L) %2d n(R) %2d B %2d E %2d waste %2d' % r)
def fromgates(path):
    g = parse(path); N = npts(g); W = replay(g, N)
    return [[int(t) for t in W[name]] for (name, *_) in g], N
def fromhatch(path, N):
    out = []
    for line in open(path):
        if line.startswith('w '): out.append([int(t) for t in line[2:].split(':')[1].split()])
    return out, N
t2 = [('s', F(1), 'x0', F(1), 'x1'), ('d', F(1), 'x0', F(-1), 'x1')]; t4 = tensor(t2, t2); t8 = tensor(t4, t2); t16 = tensor(t4, t4)
def fromlist(g):
    N = npts(g); W = replay(g, N); return [[int(t) for t in W[name]] for (name, *_) in g], N
for label, (vecs, N), detail in (('the 19', fromgates(ID + 'g-1-tightwires/h8_19gates.txt'), True), ('textbook 8', fromlist(t8), True), ('staircase 8', fromgates(ID + 'e2-0-pieces/slp_8.txt'), False),
        ('textbook 16', fromlist(t16), False), ('staircase 16', fromgates(ID + 'e2-0-pieces/slp_16.txt'), False), ('second 52', fromgates(ID + 'h-1-staircase3/slp16_52_from54.txt'), False),
        ('staircase 32', fromgates(ID + 'e2-0-pieces/slp_32.txt'), False), ('staircase 64', fromgates(ID + 'e2-0-pieces/slp_64.txt'), False)):
    run(label, vecs, N, detail)
