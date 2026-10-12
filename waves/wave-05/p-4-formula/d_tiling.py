# p-4-formula (c),(d): the rule nested, k = 2..6. Greedy tilings by tree rectangles (largest first; an UPPER bound, not a minimum):
#   "class"     : rectangles on which m is one non-zero whole number (works for every kernel, constant rho^m - 1);
#   "transform" : rectangles inside the set where m is ODD (rho = -1 sees only the parity of m; +1 and -1 cells may share a rectangle).
# Exact whole-number work. Count (G): gates = N - 2 + tau, tau = 1 + rectangles.
from itertools import product, permutations
import random, sys
def pts(k): return list(product((0,1), repeat=k))
def F(Y, X): k = len(X); return sum(X[i]*Y[k-1-i] for i in range(k))
def q_rule(X):
    k = len(X)
    if k <= 1: return 0
    if k == 3: return (1 - X[0])*X[2] + X[0]*X[1]
    return (1 - X[0])*X[-1] + q_rule(X[1:-1])
def qp_rule(Y):
    k = len(Y)
    if k <= 1: return 0
    return Y[0]*Y[-1] + qp_rule(Y[1:-1])
def nodes(k, order, P):
    out = []
    for d in range(k+1):
        buckets = {}
        for p in P: buckets.setdefault(tuple(p[order[i]] for i in range(d)), []).append(p)
        out.extend(buckets.values())
    return out
def greedy(k, m, ro, co, P, mode):
    R = nodes(k, ro, P); C = nodes(k, co, P)
    cand = sorted(((len(r)*len(c), i, j) for i, r in enumerate(R) for j, c in enumerate(C)), key=lambda t: -t[0])
    covered = set(); n = 0; big = 0
    for area, i, j in cand:
        r, c = R[i], C[j]
        v = m[(r[0], c[0])]
        if mode == 'class':
            if v == 0: continue
            good = all(m[(y, x)] == v and (y, x) not in covered for y in r for x in c)
        else:
            if v % 2 == 0: continue
            good = all(m[(y, x)] % 2 == 1 and (y, x) not in covered for y in r for x in c)
        if good:
            covered.update((y, x) for y in r for x in c); n += 1
    want = sum(1 for z in m if (m[z] != 0 if mode == 'class' else m[z] % 2 == 1))
    assert len(covered) == want
    return n
random.seed(1)
for k in (2, 3, 4, 5, 6):
    P = pts(k); N = 2**k
    m = {(Y, X): F(Y, X) - q_rule(X) - qp_rule(Y) for Y in P for X in P}
    vals = sorted(set(m.values()))
    nat = tuple(range(k))
    if k <= 4: orders = [(a, b) for a in permutations(range(k)) for b in permutations(range(k))]
    elif k == 5:
        pp = list(permutations(range(k))); orders = [(nat, nat)] + [(random.choice(pp), random.choice(pp)) for _ in range(40)]
    else: orders = [(nat, nat)]
    res = {}
    for mode in ('class', 'transform'):
        best = None
        for ro, co in orders:
            n = greedy(k, m, ro, co, P, mode)
            if best is None or n < best[0]: best = (n, ro, co)
        res[mode] = best
    tb = N*k - N + 2
    print("k=%d N=%d | values of m %s | odd cells %d of %d | CLASS: %d rectangles, tau %d, gates %d, per point %.3f (orders %s %s) | TRANSFORM: %d rectangles, tau %d, gates %d, per point %.3f (orders %s %s) | textbook tau %d gates %d | ideal rule tau %s | orders tried %d"
          % (k, N, vals, sum(v % 2 for v in m.values()), N*N, res['class'][0], res['class'][0]+1, N-1+res['class'][0], res['class'][0]/N, res['class'][1], res['class'][2],
             res['transform'][0], res['transform'][0]+1, N-1+res['transform'][0], res['transform'][0]/N, res['transform'][1], res['transform'][2], tb, N*k,
             {2: 5, 3: 13, 4: 37, 5: 101, 6: 293}[k], len(orders)))
    sys.stdout.flush()
