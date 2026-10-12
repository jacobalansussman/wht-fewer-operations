# ai-2: own check of ag-1's whole-number ledger.  Exact whole numbers.  Count (G).
import itertools, math, random, heapq
from math import gcd
from fractions import Fraction
def norm(v):
    g = 0
    for t in v: g = gcd(g, abs(t))
    if g == 0: return None
    v = [t // g for t in v]
    for t in v:
        if t: return tuple(v) if t > 0 else tuple(-q for q in v)
def solve(u, v, w):
    # w primitive on the rational line of u, v (not parallel): return coprime (a, b) and c > 0 with c*w = a*u + b*v, or None
    n = len(u)
    for i in range(n):
        for j in range(i + 1, n):
            d = u[i] * v[j] - u[j] * v[i]
            if d:
                a = Fraction(w[i] * v[j] - w[j] * v[i], d); b = Fraction(u[i] * w[j] - u[j] * w[i], d)
                if any(a * u[t] + b * v[t] != w[t] for t in range(n)): return None
                L = a.denominator * b.denominator // gcd(a.denominator, b.denominator)
                A, B = int(a * L), int(b * L); g = gcd(gcd(abs(A), abs(B)), L)
                return A // g, B // g, L // g
    return None
# 1. every gate between flat wires, NO limit on the coefficients (the coefficients are solved for, not enumerated).
#    The kind of a gate depends only on which column pairs (u_i, v_i) occur, and up to sign there are 4 non-zero pairs,
#    so 4 coordinates (plus a zero column, n = 5) show every case that exists at any n.
for n in (4, 5):
    V = sorted({norm(v) for v in itertools.product((-1, 0, 1), repeat=n)} - {None}); hist = {}
    for i, u in enumerate(V):
        for v in V[:i]:
            for w in V:
                if w == u or w == v: continue
                s = solve(u, v, w)
                if s is None or s[0] == 0 or s[1] == 0: continue
                a, b, c = s; same = all((p - q) % 2 == 0 for p, q in zip(u, v))
                key = (tuple(sorted((abs(a), abs(b)))), c, same); hist[key] = hist.get(key, 0) + 1
    print(f"flat gates, n={n}, {len(V)} wires, coefficients solved exactly: " +
          "; ".join(f"(|a|,|b|)={k[0]} c={k[1]} same residue={k[2]}: {hist[k]}" for k in sorted(hist)))
# 2. the ledger on random circuits, all orders (n = 4) and the top order only (n = 5, 6); coefficients up to 9, any content
def det(M):
    M = [r[:] for r in M]; n = len(M); sign = 1; prev = 1
    for i in range(n):
        p = next((r for r in range(i, n) if M[r][i]), None)
        if p is None: return 0
        if p != i: M[i], M[p] = M[p], M[i]; sign = -sign
        for r in range(i + 1, n):
            for c in range(i + 1, n): M[r][c] = (M[r][c] * M[i][i] - M[r][i] * M[i][c]) // prev
        prev = M[i][i]
    return sign * M[n - 1][n - 1]
def newmax(W, n, orders, old):
    # largest minor by order, only minors through the last row need computing
    new = dict(old); m = len(W) - 1
    for r in orders:
        for rows in itertools.combinations(range(m), r - 1):
            for cols in itertools.combinations(range(n), r):
                d = abs(det([[W[i][j] for j in cols] for i in rows + (m,)]))
                if d > new[r]: new[r] = d
    return new
random.seed(20261011)
for n, orders, trials, glen in ((4, (1, 2, 3, 4), 300, 7), (5, (5,), 200, 7), (6, (6,), 60, 7)):
    viol = gates = neg = halv = grew_on_neg = 0
    for _ in range(trials):
        W = [tuple(1 if i == j else 0 for j in range(n)) for i in range(n)]
        D = {r: (1 if r < n or True else 0) for r in orders}
        for _g in range(glen):
            for _try in range(100):
                u, v = random.sample(W, 2); a = random.randint(1, 9); b = random.choice((-1, 1)) * random.randint(1, 9)
                if gcd(a, b) != 1: continue
                raw = [a * x + b * y for x, y in zip(u, v)]; c = 0
                for t in raw: c = gcd(c, abs(t))
                w = norm(raw)
                if w is None or w in W or tuple(-t for t in w) in W: continue
                if c > 1 or random.random() < 0.25: break
            else: break
            W.append(w); f = Fraction(abs(a) + abs(b), c); Dn = newmax(W, n, orders, D); gates += 1
            neg += f < 1; halv += c % 2 == 0
            for r in orders:
                if Dn[r] > max(Fraction(1), f) * D[r]: viol += 1
                if f < 1 and Dn[r] > D[r]: grew_on_neg += 1
            D = Dn
    print(f"ledger, n={n}, orders {orders}: {gates} gates, {halv} with even content, {neg} of weight below 0; "
          f"violations of 'largest minor of each order grows by at most max(1,(|a|+|b|)/c)': {viol}; minors that grew on a gate of weight below 0: {grew_on_neg}")
# 3. the 19-gate circuit at 8 points (file g-1-tightwires/h8_19gates.txt, retyped here) and the textbook: weights
def replay(prog, n):
    W = {f"x{i}": tuple(1 if j == i else 0 for j in range(n)) for i in range(n)}; tot = 0.0; kinds = {}
    for name, a, u, b, v in prog:
        raw = [a * p + b * q for p, q in zip(W[u], W[v])]; c = 0
        for t in raw: c = gcd(c, abs(t))
        # coefficients relative to the primitive operands: the operands are stored primitive, so (a, b) is already that pair
        g = gcd(abs(a), abs(b)); f = Fraction(abs(a) // g + abs(b) // g, c // g if c % g == 0 else c)
        W[name] = tuple(t // c for t in raw); tot += max(0.0, math.log2(f)); kinds[str(f)] = kinds.get(str(f), 0) + 1
    return W, tot, kinds
P19 = [("g1",1,"x0",1,"x7"),("g2",1,"x1",1,"x6"),("g3",1,"x2",-1,"x5"),("g4",1,"x3",-1,"x4"),("g5",1,"g1",-1,"g2"),("g6",1,"g3",1,"g4"),
       ("g7",1,"g5",-1,"g6"),("g8",1,"g7",-2,"x7"),("g9",1,"g7",-2,"x5"),("g10",1,"g8",2,"x6"),("g11",1,"g9",-2,"x4"),("y7",1,"g10",2,"g4"),
       ("y3",1,"g9",2,"x3"),("y5",-1,"y3",2,"g5"),("y1",1,"g10",2,"g3"),("y6",1,"g11",2,"g2"),("y2",1,"g8",2,"x1"),("y4",1,"y2",2,"g6"),("y0",-1,"g11",2,"g1")]
W, tot, kinds = replay(P19, 8)
ok = all(W[f"y{j}"] == tuple((-1) ** bin(j & x).count("1") for x in range(8)) for j in range(8))
flat = all(all(abs(t) <= 1 for t in w) for w in W.values())
print(f"19 gates at 8 points: computes the transform: {ok}; every wire flat: {flat}; gate factors (|a|+|b|)/c: {kinds}; total weight {tot:.2f}; the determinant asks 12")
# 4. least total weight of a flat circuit for the 4-point transform with halvings free (own search: Dijkstra over wire sets)
n = 4; V = sorted({norm(v) for v in itertools.product((-1, 0, 1), repeat=n)} - {None}); idx = {v: i for i, v in enumerate(V)}
L3 = math.log2(3); der = [[] for _ in V]
for i, u in enumerate(V):
    for j in range(i):
        for w in V:
            if w == u or w == V[j]: continue
            s = solve(u, V[j], w)
            if s is None or s[0] == 0 or s[1] == 0: continue
            f = Fraction(abs(s[0]) + abs(s[1]), s[2]); der[idx[w]].append(((1 << i) | (1 << j), 0.0 if f == 1 else (1.0 if f == 2 else L3)))
def close(S):
    ch = True
    while ch:
        ch = False
        for w in range(len(V)):
            if not S >> w & 1 and any(wt == 0.0 and (S & m) == m for m, wt in der[w]): S |= 1 << w; ch = True
    return S
start = 0
for i in range(n): start |= 1 << idx[norm([1 if k == i else 0 for k in range(n)])]
omask = 0
for j in range(n): omask |= 1 << idx[norm([(-1) ** bin(j & x).count("1") for x in range(n)])]
start = close(start); dist = {start: 0.0}; pq = [(0.0, start)]; found = None; popped = 0
while pq:
    d, S = heapq.heappop(pq)
    if d > dist.get(S, 1e9) + 1e-12: continue
    popped += 1
    if (S & omask) == omask: found = d; break
    missing = bin(omask & ~S).count("1")
    for w in range(len(V)):
        if S >> w & 1: continue
        c = min((x for m, x in der[w] if (S & m) == m), default=None)
        if c is None: continue
        T = close(S | (1 << w)); nd = d + c
        if nd + (bin(omask & ~T).count("1")) > 8.0 + 1e-9: continue      # an output is never a half, so each missing output costs at least 1
        if nd < dist.get(T, 1e9) - 1e-12: dist[T] = nd; heapq.heappush(pq, (nd, T))
print(f"4 points, flat wires, halvings free: least total weight = {found} (states settled {popped}); the determinant asks 4, the textbook spends 8")
