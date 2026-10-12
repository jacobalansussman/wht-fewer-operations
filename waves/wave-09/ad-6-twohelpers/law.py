#!/usr/bin/env python3
"""law.py [ad-6-twohelpers]  Count-only copy of circuit2.py (same gates, no values), checked against the built circuits
of circuit2.out, then pushed to large k with the number t of selector bits chosen to minimise the gate count.
Also the class counts of the family (formula) and the two lower bounds: girth alone (Moore bound for irregular graphs,
Alon-Hoory-Linial, RECALLED) and the family's own asymptote."""
import sys, math
from functools import lru_cache
def sizes(m, t):
    g = 1 << t; return [len(range(b, m, g)) for b in range(g)]
@lru_cache(None)
def E1(n, const):
    if n == 0: return 0
    if n == 1: return 1 if const else 0
    h = n // 2
    return E1(h, const) + E1(n - h, False) + ((1 << h) - (0 if const else 1)) * ((1 << (n - h)) - 1)
def step(k, t, sub):
    m = k - t; g = 1 << t; sz = sizes(m, t); pc = lambda v: bin(v).count('1')
    tot = sum(pc(b) * sz[b] for b in range(g)) + sub(m)
    for a in range(g):
        w = pc(a); tot += max(0, w + w * (w - 1) // 2 - 1)
        tot += sum((pc(a ^ b) - 1) * sz[b] for b in range(g) if b != a)
        tot += E1(m - sz[a], a != 0)
    return tot + (1 << k) - (1 << sz[0])
def classes(k, t):
    m = k - t; return (1 << m) + sum(1 << (m - s) for s in sizes(m, t))
def best_t_classes(k): return min(range(1, min(k, 8)), key=lambda t: classes(k, t))
@lru_cache(None)
def E2same(k):          # same rule as circuit2.py
    if k <= 2: return (0, 1, 5)[k]
    return step(k, best_t_classes(k), E2same)
@lru_cache(None)
def E2(k):              # t chosen to minimise gates
    if k <= 2: return (0, 1, 5)[k], 0
    return min((step(k, t, lambda m: E2(m)[0]), t) for t in range(1, min(k, 8)))
def ahl(N):             # least n with n >= 2 (1 + (d-1) + (d-1)^2 + (d-1)^3), d = 2N/n  (girth 8, N edges)
    n = 2
    while True:
        d = 2 * N / n
        if d <= 2 or n >= 2 * (1 + (d - 1) + (d - 1) ** 2 + (d - 1) ** 3) - 1e-9: return n
        n += 1
built = {3: 13, 4: 29, 5: 63, 6: 130, 7: 265, 8: 528, 9: 1055, 10: 1827, 11: 3588, 12: 6729, 13: 13114, 14: 25247, 15: 49554, 16: 97078}
print("check of the count-only copy against the built and replayed circuits (circuit2.out):", all(E2same(k) == v for k, v in built.items()))
print("k | classes of the family, best t | classes/N | girth-only lower bound (recalled theorem) | gates (G) for a degree-2 polynomial at all points, best t | gates/N")
for k in list(range(3, 25)) + [28, 32, 40, 48, 56, 64, 80, 96, 128, 160, 200, 256, 400]:
    N = 1 << k; t = best_t_classes(k); c = classes(k, t); g, tg = E2(k)
    lb = ("%d" % ahl(N)) if k <= 20 else "about N^(3/4)"
    print("k=%3d t=%d classes/N=%.5f %s lower %s | gates/N = %.5f (t=%d) ; (log2 k)/k = %.4f" % (k, t, c / N, ("classes=%d" % c) if k <= 12 else "", lb, g / N, tg, math.log2(k) / k))
