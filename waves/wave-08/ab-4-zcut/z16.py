# ab-4-zcut/z16.py : the cut meter and the crossing-helper inequality on stored circuits for Z at 16 and 32 points
# (files of u-3-zletter, lines "name = c * a + c * b").  Count (G). Exact (whole numbers).   usage: python3 -B z16.py file ...
import sys, re, itertools
from math import gcd
def prim(v):
    g = 0
    for t in v: g = gcd(g, t)
    if g == 0: return None
    s = next(t for t in v if t); s = g if s > 0 else -g
    return tuple(t // s for t in v)
def load(path):
    W = {}; gates = []; N = 0; lines = [l.split('#')[0].strip() for l in open(path)]
    for l in lines:
        for m in re.findall(r'x(\d+)', l): N = max(N, int(m) + 1)
    for i in range(N): W['x%d' % i] = tuple(int(i == j) for j in range(N))
    for l in lines:
        if '=' not in l: continue
        name, rhs = l.split('='); name = name.strip(); terms = [t.strip().split('*') for t in rhs.split('+')]
        v = [0] * N
        for c, a in terms:
            u = W[a.strip()]; c = int(c); v = [x + c * y for x, y in zip(v, u)]
        W[name] = tuple(v)
        if len(terms) == 2: gates.append(tuple(v))
    return N, gates
def classes(wires, X):
    out = set()
    for w in wires:
        c = prim([w[i] for i in X])
        if c is not None and sum(1 for t in c if t) > 1: out.add(c)
    return out
for path in sys.argv[1:]:
    N, gates = load(path); k = N.bit_length() - 1
    Z = [tuple(1 if (T & S) == T else 0 for T in range(N)) for S in range(N)]
    assert all(r in set(gates) or sum(r) == 1 for r in Z), 'not all rows held'
    T = len(gates); yates = (N // 2) * k
    print('%s: N=%d gates=%d (all %d rows held exactly); Yates %d' % (path.split('/')[-1], N, T, N, yates))
    for c in range(k):
        L = [x for x in range(N) if not x >> c & 1]; R = [x | 1 << c for x in L]
        nL, nR = len(classes(gates, L)), len(classes(gates, R))
        X = sum(1 for w in gates if any(w[i] for i in L) and any(w[i] for i in R)); Xh = X - N // 2
        GL = sum(1 for w in gates if any(w[i] for i in L)); GR = sum(1 for w in gates if any(w[i] for i in R))
        assert GL - nL >= N // 2 and GR - nR >= N // 2 and T >= nL + nR + N - X
        print('   plain cut bit %d: n(L)=%d n(R)=%d (Yates half %d)  E-B=%d (N/2=%d)  crossing gates X=%d, crossing helpers %d  R-repeats %d L-repeats %d  gates on L alone %d'
              % (c, nL, nR, (N // 4) * (k - 1), T - nL - nR, N // 2, X, Xh, GR - nR, GL - nL, T - GR))
    best = None
    for order in itertools.permutations(range(k)):
        tot = 0; bylev = {}
        def rec(X, d):
            global tot
            if len(X) == 1: return
            b = order[d]; X0 = [x for x in X if not x >> b & 1]; X1 = [x for x in X if x >> b & 1]
            cl = classes(gates, X0 + X1); h = len(X0); zr = {prim([r[i] for i in X0 + X1]) for r in Z} - {None}
            xh = sum(1 for c in cl if any(c[:h]) and any(c[h:]) and c not in zr)
            n, n0, n1 = len(cl), len(classes(gates, X0)), len(classes(gates, X1))
            assert n >= n0 + n1 + h - xh
            tot += xh; t = bylev.setdefault(len(X), [0, 0]); t[0] += xh; t[1] += n - n0 - n1 - h
            rec(X0, d + 1); rec(X1, d + 1)
        rec(list(range(N)), 0)
        assert T >= yates - tot
        if best is None or tot < best[0]: best = (tot, order, dict(bylev))
        if k > 4 and order != tuple(range(k)) and order != tuple(reversed(range(k))): 
            if sum(1 for _ in [0]) and order[0] > 1: break
    print('   least total of Xh over the trees tried: %d at bit order %s; per node size [Xh in all, sum of (n(X) - n(X0) - n(X1) - |X|/2)]: %s' % (best[0], best[1], best[2]))
