# Border game for fan-in-2 linear gates (w = a*u + b*v, scalings free), exact arithmetic.
# A border program: every node is a vector of polynomials in e over Q, kept primitive (lowest e-coefficient non-zero).
# A gate takes a(e)*u + b(e)*v with a, b in Q[e, 1/e]; its LIMIT is the lowest coefficient vector, as a projective point.
# Question: is the set of limit points of an s-gate border program ever more expensive, exactly, than s gates?
# Exact cost of a point set T: |T| + (fewest helper points); helpers searched exhaustively over GF(p) (all points on all lines).
import sys, random, itertools
from fractions import Fraction as Fr
from math import gcd
n = int(sys.argv[1]); S = int(sys.argv[2]); TRIALS = int(sys.argv[3]); seed = int(sys.argv[4]); P = int(sys.argv[5])
random.seed(seed)
CMAX = int(sys.argv[6]) if len(sys.argv) > 6 else 2
def strip(w):
    k = 0
    while w and all(x == 0 for x in w[0]): w = w[1:]; k += 1
    while w and all(x == 0 for x in w[-1]): w = w[:-1]
    return w, k
def comb(u, a, ma, v, b, mb):
    L = max(len(u)+ma, len(v)+mb)
    w = [[Fr(0)]*n for _ in range(L)]
    for i, c in enumerate(u):
        for j in range(n): w[i+ma][j] += a*c[j]
    for i, c in enumerate(v):
        for j in range(n): w[i+mb][j] += b*c[j]
    return w
def prim(v):
    den = 1
    for x in v: den = den*x.denominator//gcd(den, x.denominator)
    iv = [int(x*den) for x in v]; g = 0
    for x in iv: g = gcd(g, abs(x))
    iv = [x//g for x in iv]
    for x in iv:
        if x:
            if x < 0: iv = [-y for y in iv]
            break
    return tuple(iv)
def ratio(a, b):   # a = k*b ?
    k = None
    for x, y in zip(a, b):
        if y == 0:
            if x != 0: return None
        else:
            r = x/y
            if k is None: k = r
            elif k != r: return None
    return k
def make():
    nodes = [[[Fr(int(i == j)) for i in range(n)]] for j in range(n)]
    log = []
    while len(nodes) < n + S:
        i, j = random.sample(range(len(nodes)), 2)
        if random.random() < 0.6:
            co = [(a, b) for a in range(len(nodes)) for b in range(a+1, len(nodes)) if ratio(nodes[a][0], nodes[b][0]) is not None]
            if co: i, j = random.choice(co)
        u, v = nodes[i], nodes[j]
        k = ratio(u[0], v[0])
        if k is not None:
            d, o = strip(comb(u, Fr(1), 0, v, -k, 0))
            if not d: continue
            lam = random.choice([0, 0, 1, -1, 2])
            w = comb(d, Fr(1), 0, u, Fr(lam), 0) if lam else d
            w, _ = strip(w); log.append(("cancel", i, j, o, lam))
        else:
            c = Fr(random.choice([1, -1, 2, -2, 3]))
            r = random.random()
            if r < 0.45: w = comb(u, Fr(1), 0, v, c, 0); log.append(("gen", i, j, int(c)))
            else:
                m = random.choice([1, 1, 2]); w = comb(u, Fr(1), 0, v, c, m); log.append(("pert", i, j, int(c), m))
            w, _ = strip(w)
            if not w: continue
        nodes.append(w)
    return nodes, log
def modp(t):
    v = [x % P for x in t]
    for x in v:
        if x:
            inv = pow(x, P-2, P); return tuple((y*inv) % P for y in v)
    return None
def line(x, y):
    pts = set()
    for a in range(P):
        pts.add(modp([xi + a*yi for xi, yi in zip(x, y)]))
    pts.add(y); return pts
def exact_helpers(targets, maxh):
    inputs = [tuple(int(i == j) for i in range(n)) for j in range(n)]
    T = set(targets) - set(inputs)
    def close(base, reach, missing):
        base = set(base); reach = set(reach); missing = set(missing)
        ch = True
        while ch:
            ch = False
            for t in list(missing):
                if t in reach:
                    for x in base:
                        reach |= line(x, t)
                    base.add(t); missing.discard(t); ch = True
        return base, reach, missing
    base = set(inputs); reach = set()
    for x, y in itertools.combinations(inputs, 2): reach |= line(x, y)
    base, reach, missing = close(base, reach, T)
    def dfs(base, reach, missing, h):
        if not missing: return True
        if h == 0: return False
        for z in sorted(reach - base):
            r2 = set(reach)
            for x in base: r2 |= line(x, z)
            b2, r3, m2 = close(base | {z}, r2, missing)
            if dfs(b2, r3, m2, h-1): return True
        return False
    for h in range(0, maxh+1):
        if dfs(base, reach, missing, h): return h
    return None
stats = {}; found = 0
inputs = set(tuple(int(i == j) for i in range(n)) for j in range(n))
for trial in range(TRIALS):
    nodes, log = make()
    lim = [prim(w[0]) for w in nodes[n:]]
    T = set(lim) - inputs
    c = S - len(T)
    Tp = set(modp(t) for t in T)
    if len(Tp) != len(T) or None in Tp: continue
    if c == 0 or c > CMAX or len(T) < 2: 
        stats[("skip", c)] = stats.get(("skip", c), 0) + 1; continue
    h = exact_helpers(Tp, c)
    key = (c, h); stats[key] = stats.get(key, 0) + 1
    if h is None:
        found += 1
        print("CANDIDATE border", S, "gates; distinct limits", len(T), "; exact needs more than", c, "helpers mod", P)
        print("  log", log); print("  limits", lim)
        sys.stdout.flush()
        if found >= 6: break
print("n", n, "gates", S, "prime", P, "stats (lost nodes, helpers needed):", sorted(stats.items(), key=str))
