#!/usr/bin/env python3
"""replay16.py (g-0-mirror): exact replay.  Count (G): a gate is a*u + b*v, scalings free.
1. Reduced model: from 6 basis points, 14 gates (lines through two present points) reach all 16 targets (4 extra points).
2. Transposed (forward) circuit: 16 inputs x_p -> 6 forms, 24 gates.  Checked: every output form f satisfies f S = -4 f and the
   six are independent, i.e. they are a basis of the mirror (the -4 eigenspace of the symmetric 16-point transform S).
3. For every basis found for the chosen roots: the dual basis B*, and whether B* reaches all 16 targets in 16 gates with no helper
   (then the whole transform costs 24 + 16 + 16 = 56 by this route)."""
import itertools, sys, random
from fractions import Fraction as F
def dot2(a, b): return bin(a & b).count('1') & 1
N = 16
def halves(p): return p >> 2, p & 3
S = [[(-1) ** (dot2(halves(p)[0], halves(y)[1]) ^ dot2(halves(p)[1], halves(y)[0])) for y in range(N)] for p in range(N)]
C0 = []
for a in range(N):
    v = [(-1) ** (dot2(halves(p)[0], halves(p)[1]) ^ dot2(a, p)) for p in range(N)]
    if [sum(S[i][j] * v[j] for j in range(N)) for i in range(N)] == [-4 * x for x in v]: C0.append(v)
def norm(v):
    v = [F(x) for x in v]
    nz = [x for x in v if x != 0]
    if not nz: return tuple(v)
    return tuple(x / nz[0] for x in v)
T = [norm([C0[i][p] for i in range(6)]) for p in range(N)]
def solve(rows, t):          # coefficients x with sum x_j rows[j] = t, or None
    k = len(rows); n = len(t); A = [[F(rows[j][i]) for j in range(k)] + [F(t[i])] for i in range(n)]
    piv = []; r = 0
    for c in range(k):
        p = next((i for i in range(r, n) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]; A[r] = [x / A[r][c] for x in A[r]]
        for i in range(n):
            if i != r and A[i][c] != 0: A[i] = [x - A[i][c] * y for x, y in zip(A[i], A[r])]
        piv.append(c); r += 1
    if any(A[i][k] != 0 for i in range(r, n)): return None
    x = [F(0)] * k
    for i, c in enumerate(piv): x[c] = A[i][k]
    return x
def triples(W):
    out = []
    for i, j, k in itertools.combinations(range(len(W)), 3):
        if solve([W[i], W[j]], W[k]) is not None: out.append((i, j, k))
    return out
def closure_order(B, trip, n):
    have = set(B); order = []; ch = True
    while ch:
        ch = False
        for (i, j, k) in trip:
            s = [x for x in (i, j, k) if x in have]
            if len(s) == 2:
                h = [x for x in (i, j, k) if x not in have][0]; have.add(h); order.append((h, s[0], s[1])); ch = True
    return order if len(have) == n else None
def root(v): return norm(v)
X = [root(r) for r in ([0,0,0,0,1,-1], [0,0,0,0,1,1], [0,0,0,1,-1,0], [0,0,1,-1,0,0])]
if len(sys.argv) > 1:
    X = [root(eval(a)) for a in sys.argv[1:]]
W = T + X; trip = triples(W)
print('extra points (roots):', [tuple(int(x) for x in r) for r in X]); print('collinear triples in W:', len(trip))
sols = [B for B in itertools.combinations(range(len(W)), 6) if closure_order(B, trip, len(W)) is not None]
print('bases of 6 points of W that generate W:', len(sols), ' by number of targets in the basis:',
      {k: sum(1 for B in sols if sum(1 for b in B if b < 16) == k) for k in range(7)})
def transposed(B, order, W):
    """returns list of forms (dict input->coef) for the 6 basis nodes, and the gate count of the forward circuit"""
    cons = {i: [] for i in range(len(W))}        # node -> list of (consumer, weight)
    for (h, u, v) in order:
        a, b = solve([W[u], W[v]], W[h]); cons[u].append((h, a)); cons[v].append((h, b))
    val = {}; gates = 0
    for (h, u, v) in reversed(order):
        pass
    done = set()
    def value(i):
        if i in val: return val[i]
        terms = []
        if i < 16: terms.append({i: F(C0[0][i])})      # T[i] = (sign) * column i of C0; a sign on an input is free
        for (h, a) in cons[i]:
            vh = value(h); terms.append({k: a * c for k, c in vh.items()})
        acc = {}
        for t in terms:
            for k, c in t.items(): acc[k] = acc.get(k, F(0)) + c
        val[i] = acc; return acc
    forms = [value(b) for b in B]
    g = 0
    for i in range(len(W)):
        nterms = (1 if i < 16 else 0) + len(cons[i])
        if nterms >= 2: g += nterms - 1
    return forms, g, cons
def check_mirror(forms):
    rows = [[f.get(p, F(0)) for p in range(N)] for f in forms]
    for r in rows:
        assert [sum(r[i] * S[i][j] for i in range(N)) for j in range(N)] == [-4 * x for x in r], 'not in the mirror'
    A = [r[:] for r in rows]; rk = 0
    for c in range(N):
        p = next((i for i in range(rk, 6) if A[i][c] != 0), None)
        if p is None: continue
        A[rk], A[p] = A[p], A[rk]
        for i in range(rk + 1, 6):
            if A[i][c] != 0:
                f = A[i][c] / A[rk][c]; A[i] = [x - f * y for x, y in zip(A[i], A[rk])]
        rk += 1
    assert rk == 6
    return rows
B = sols[0]; order = closure_order(B, trip, len(W))
print('\nREDUCED CIRCUIT (6 start points, %d gates):' % len(order))
name = lambda i: ('t%d' % i) if i < 16 else ('r%d' % (i - 16))
print('  start:', ' '.join(name(b) for b in B))
for (h, u, v) in order:
    a, b = solve([W[u], W[v]], W[h]); print('  %s = (%s)*%s + (%s)*%s' % (name(h), a, name(u), b, name(v)))
forms, g, cons = transposed(B, order, W)
rows = check_mirror(forms)
print('\nFORWARD CIRCUIT: gates =', g, ' outputs: 6 forms, each checked f S = -4 f, rank 6: a basis of the mirror')
for b, r in zip(B, rows):
    print('  y[%s] =' % name(b), ' '.join('%3s' % x for x in r), '  non-zeros:', sum(1 for x in r if x != 0))
print('  wires of the forward circuit (node: what it adds up):')
for i in range(len(W)):
    nt = (1 if i < 16 else 0) + len(cons[i])
    print('   w[%s] = %s%s' % (name(i), ('x%d ' % i) if i < 16 else '', ' '.join('+ (%s)*w[%s]' % (a, name(h)) for (h, a) in cons[i])), '  gates:', max(0, nt - 1))
# all bases: forward gate count, and the dual basis
cnt = {}
def dual(Bv):
    # rows b*_j with b*_j . b_k = delta_jk
    out = []
    for j in range(6):
        Gm = [[sum(x * y for x, y in zip(Bv[k], e)) for e in [[F(int(i == m)) for i in range(6)] for m in range(6)]] for k in range(6)]
        out.append(solve([[Bv[k][i] for k in range(6)] for i in range(6)], [F(int(k == j)) for k in range(6)]))
    return out
best = {}
random.seed(1)
sample = set(random.sample(range(len(sols)), 120))
for bi, B in enumerate(sols):
    order = closure_order(B, trip, len(W)); forms, g, cons = transposed(B, order, W); check_mirror(forms)
    cnt[g] = cnt.get(g, 0) + 1
    if bi not in sample: continue
    Bv = [W[b] for b in B]
    D = [solve([[Bv[k][i] for k in range(6)] for i in range(6)], [F(int(k == j)) for k in range(6)]) for j in range(6)]
    for j in range(6):
        assert all(sum(x * y for x, y in zip(D[j], Bv[k])) == (1 if j == k else 0) for k in range(6))
    Dn = [norm(d) for d in D]
    W2 = T + [d for d in Dn if d not in T]; nt = 16 - (len(W2) - 16 - 6) - 16 + 16
    trip2 = triples(W2); Bi = [W2.index(d) for d in Dn]
    o2 = closure_order(Bi, trip2, len(W2))
    key = (sum(1 for d in Dn if d in T), o2 is not None)
    best[key] = best.get(key, 0) + 1
    if o2 is not None and 'shown' not in best:
        best['shown'] = 1
        print('\nDUAL BASIS that reaches all 16 targets with no helper: basis', [name(b) for b in B])
        for d in Dn: print('   b* =', ' '.join('%5s' % x for x in d))
print('\nforward gate count over all %d bases:' % len(sols), cnt)
print('dual bases, a random sample of 120: (targets inside B*, B* generates all targets without any helper) -> how many:', {k: v for k, v in best.items() if k != 'shown'})
