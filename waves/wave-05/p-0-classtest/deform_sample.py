#!/usr/bin/env python3
"""p-0-classtest / deform_sample.py = h-6-classhub / deform.py with one added mode: sample S seed (random frames).\nh-6-classhub / deform.py : does a given circuit for the Walsh-Hadamard transform (tau = -1) move with tau?  EXACT, first order.
Keep the circuit's wiring (which gate reads which two wires), let every gate be w = u + theta*v with its own free theta, and ask
for the outputs to stay proportional to the rows of K^(tensor k), K = [[1,1],[1,tau]], as tau leaves -1.
Equations F(theta, tau) = 0: for each output y and its row r, y[x]*r[x0] - y[x0]*r[x] = 0 for all x.
First-order test (implicit function theorem, necessary condition): dF/dtau must lie in the column space of dF/dtheta at tau = -1.
If it does not, NO family of programs with this wiring through this program exists for tau near -1: the circuit is rigid at tau = -1.
At tau = -1 every invertible bit matrix A (an 'address map') and every shift t turns a correct program into a correct program
(inputs renamed x -> A x + t); for other tau these are different problems, so all 168 * 8 frames are tested.
usage: deform.py programfile k [frames: all|id]"""
import sys, re, itertools
from fractions import Fraction as F
path = sys.argv[1]; k = int(sys.argv[2]); N = 1 << k; which = sys.argv[3] if len(sys.argv) > 3 else 'all'
gates = []
for line in open(path):
    line = line.split('#')[0].strip()
    if not line or '=' not in line: continue
    nm, rhs = [s.strip() for s in line.split('=')]
    m = re.match(r'^(-?[\d/]*)\s*\*?\s*([a-z]+\d+)\s*([+-])\s*(-?[\d/]*)\s*\*?\s*([a-z]+\d+)$', rhs)
    assert m, rhs
    def num(s): return F(1) if s == '' else F(-1) if s == '-' else F(s)
    a = num(m.group(1)); b = num(m.group(4)) * (1 if m.group(3) == '+' else -1)
    gates.append((nm, a, m.group(2), b, m.group(5)))
def rank(M):
    M = [list(r) for r in M]; r = 0
    for c in range(len(M[0]) if M else 0):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; pv = M[r][c]
        for i in range(r + 1, len(M)):
            if M[i][c] != 0:
                f = M[i][c] / pv
                for j in range(c, len(M[0])): M[i][j] -= f * M[r][j]
        r += 1
        if r == len(M): break
    return r
def bits(w): return bin(w).count('1')
def test(perm):
    """perm: input x_j of the file becomes input x_perm[j].  returns (ok at tau=-1, rank J, rank [J|Ftau], #equations)"""
    G = len(gates); val = {'x%d' % j: [F(int(perm[j] == i)) for i in range(N)] for j in range(N)}
    tan = {nm: [[F(0)] * N for _ in range(G)] for nm in val}          # tangent of each wire in each theta direction
    for gi, (nm, a, u, b, v) in enumerate(gates):
        th = b / a
        val[nm] = [a * (s + th * t) for s, t in zip(val[u], val[v])]            # the file's own scaling of the wire: a*(u + theta*v)
        T = [[a * (s + th * t) for s, t in zip(tan[u][d], tan[v][d])] for d in range(G)]
        T[gi] = [s + a * t for s, t in zip(T[gi], val[v])]
        tan[nm] = T
    rows = {}
    for w in range(N):
        r = tuple((-1) ** bits(w & x) for x in range(N)); rows[r] = w; rows[tuple(-t for t in r)] = w
    outs = {}
    for nm, *_ in gates:
        y = val[nm]; lead = next((t for t in y if t), None)
        if lead is None: continue
        key = tuple(t / abs(lead) for t in y)
        if all(abs(t) == 1 for t in key) and key in rows: outs.setdefault(rows[key], nm)
    if len(outs) != N: return (False, 0, 0, 0)
    J = []; Ft = []
    for w, nm in outs.items():
        y = val[nm]; r = [F((-1) ** bits(w & x)) for x in range(N)]
        dr = [F(bits(w & x) * (-1) ** (bits(w & x) - 1)) if bits(w & x) else F(0) for x in range(N)]     # d/dtau tau^m at tau = -1
        for x in range(1, N):
            J.append([tan[nm][d][x] * r[0] - tan[nm][d][0] * r[x] for d in range(G)])
            Ft.append(y[x] * dr[0] - y[0] * dr[x])
    rJ = rank(J); rA = rank([row + [f] for row, f in zip(J, Ft)])
    return (True, rJ, rA, len(J))
def gl(k):
    out = []
    for cols in itertools.product(range(1, N), repeat=k):
        img = [0] * N
        for x in range(N):
            y = 0
            for j in range(k):
                if x >> j & 1: y ^= cols[j]
            img[x] = y
        if len(set(img)) == N: out.append((cols, img))
    return out
# p-0-classtest: third mode "sample S seed": S random frames (random invertible bit matrix A, random shift t), the identity frame first
if which == 'sample':
    import random
    S = int(sys.argv[4]); rnd = random.Random(int(sys.argv[5])); pairs = [(tuple(1 << j for j in range(k)), list(range(N)), 0)]
    while len(pairs) < S:
        cols = tuple(rnd.randrange(1, N) for _ in range(k)); img = [0] * N
        for x in range(N):
            y = 0
            for j in range(k):
                if x >> j & 1: y ^= cols[j]
            img[x] = y
        if len(set(img)) == N: pairs.append((cols, img, rnd.randrange(N)))
else:
    frames = gl(k) if which == 'all' else [(tuple(1 << j for j in range(k)), list(range(N)))]
    shifts = range(N) if which == 'all' else [0]
    pairs = [(cols, img, t) for cols, img in frames for t in shifts]
tally = {}; movers = []
for cols, img, t in pairs:
    if True:
        perm = [img[x] ^ t for x in range(N)]
        ok, rJ, rA, ne = test(perm)
        key = ('correct at tau=-1' if ok else 'NOT correct', 'rank dF/dtheta = %d of %d unknowns' % (rJ, len(gates)), 'MOVES to first order' if rA == rJ else 'rigid (first-order obstruction)')
        tally[key] = tally.get(key, 0) + 1
        if ok and rA == rJ: movers.append((cols, t))
print(path.split('/')[-1], '| gates', len(gates), '| frames tested', len(pairs))
for key, n in sorted(tally.items()): print('  %5d frames: %s' % (n, ' | '.join(key)))
print('  frames that move (columns of A, shift):', movers[:12], '...' if len(movers) > 12 else '')
