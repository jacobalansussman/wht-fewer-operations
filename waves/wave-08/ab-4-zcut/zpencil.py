# ab-4-zcut/zpencil.py : the PENCIL of cuts on every optimal 12-gate circuit for subset sums Z at 8 points.  Count (G). Exact.
# usage: python3 -B zpencil.py <p> <file> [dp]
# Cut by one address bit: a wire is (a, b), a = entries on L (bit off), b = entries on R (bit on).  Projection at s: a + s*b
# (s = 'inf': b).  x-2's coordinate cut is the pair (0, inf).  Rows of Z are (z, 0) and (z, z): at every s except -1 and inf
# both have class z, so the later one is new at neither projection: E(s, t) >= N/2 whenever s, t are not -1 or inf  [derived].
# A wire is PURE across the cut when a and b are proportional (or one is zero), MIXED otherwise.
# Printed per (circuit, cut): M = mixed gates, P = distinct non-trivial classes z among pure gates, the number n(s) of distinct
# non-trivial classes at several s, and (with 'dp') least E over all valid orders for some pairs (s, t).
import sys, re, itertools
from fractions import Fraction as F
exec(open('zmeter.py').read().split('def projections')[0])
def lift(d, p): return tuple((x if x <= p // 2 else x - p) for x in d)
def proj(s, c):
    L = [x for x in range(N) if not x >> c & 1]; R = [x | 1 << c for x in L]
    if s == 'inf': return lambda w: [w[j] for j in R]
    s = F(s); d = s.denominator; n_ = s.numerator
    return lambda w: [d * w[i] + n_ * w[j] for i, j in zip(L, R)]
def classes(wires, s, c):
    P = proj(s, c); triv = {prim(P(x)) for x in inputs}; triv.add(None)
    return [None if prim(P(w)) in triv else prim(P(w)) for w in wires]
def pure(w, c):
    L = [x for x in range(N) if not x >> c & 1]; R = [x | 1 << c for x in L]
    a = [w[i] for i in L]; b = [w[j] for j in R]
    return all(a[i] * b[j] == a[j] * b[i] for i in range(4) for j in range(4))
def minE(wires, need, ca, cb):
    G = len(wires); lo = {0: 0}; frontier = [0]
    for size in range(G):
        nxt = set()
        for S in frontier:
            for g in range(G):
                if S >> g & 1 or not any(m & S == m for m in need[g]): continue
                na = ca[g] is not None and not any((S >> h & 1) and ca[h] == ca[g] for h in range(G))
                nb = cb[g] is not None and not any((S >> h & 1) and cb[h] == cb[g] for h in range(G))
                d = 0 if (na or nb) else 1; T = S | 1 << g
                if T not in lo or lo[S] + d < lo[T]: lo[T] = lo[S] + d
                nxt.add(T)
        frontier = list(nxt)
    return lo[(1 << G) - 1]
p = int(sys.argv[1]); path = sys.argv[2]; dp = len(sys.argv) > 3
SS = [0, 'inf', -1, 1, 2, -2, F(1, 2), 3, 5, -3, F(2, 3), 7]
PAIRS = [(1, 2), (F(1, 2), -3), (0, 1), (0, 'inf'), (-1, 'inf'), (0, -1)]
tabM = {}; tabn = {s: {} for s in SS}; tabE = {q: {} for q in PAIRS}; allpure = 0; tot = 0; maxM = {}
for line in open(path):
    if 'example' not in line: continue
    hs = [lift([int(ch) for ch in h], p) for h in re.findall(r'\[(\d+)\]', line)]
    wires = list(hs) + list(targets); need = pairs_for(wires)
    made = 0; ch = True
    while ch:
        ch = False
        for g in range(12):
            if not made >> g & 1 and any(m & made == m for m in need[g]): made |= 1 << g; ch = True
    if made != 4095: continue
    tot += 1; Ms = []
    for c in range(3):
        pu = [pure(w, c) for w in wires]; M = pu.count(False)
        # pure classes z: the common direction of a and b
        L = [x for x in range(N) if not x >> c & 1]; R = [x | 1 << c for x in L]
        zs = set()
        for w, f in zip(wires, pu):
            if not f: continue
            a = [w[i] for i in L]; b = [w[j] for j in R]; z = prim(a) or prim(b)
            if sum(1 for t in z if t) > 1: zs.add(z)
        Pn = len(zs); Ms.append(M)
        tabM[(M, Pn)] = tabM.get((M, Pn), 0) + 1
        cls = {s: classes(wires, s, c) for s in SS}
        for s in SS:
            n = len({x for x in cls[s] if x is not None}); tabn[s][n] = tabn[s].get(n, 0) + 1
        if dp:
            for (s, t) in PAIRS:
                e = minE(wires, need, cls[s], cls[t]); tabE[(s, t)][e] = tabE[(s, t)].get(e, 0) + 1
    key = tuple(sorted(Ms)); maxM[key] = maxM.get(key, 0) + 1
print('p=%d: %d circuits replayed over Q; 3 cuts each' % (p, tot))
print('(M mixed gates, P pure classes) : count of (circuit, cut)   [generic n(s) = M + P; gates = M + P + repeated pure gates]')
for k in sorted(tabM): print('   M=%d P=%d  M+P=%d : %d' % (k[0], k[1], k[0] + k[1], tabM[k]))
print('per circuit, sorted M over the three cuts : count'); 
for k in sorted(maxM): print('   %s : %d' % (k, maxM[k]))
print('n(s) = number of distinct non-trivial classes at s : histogram over (circuit, cut)')
for s in SS: print('   s=%-4s %s' % (s, dict(sorted(tabn[s].items()))))
if dp:
    print('least E over all valid orders, for pairs (s, t) : histogram over (circuit, cut)')
    for q in PAIRS: print('   (s, t)=(%s, %s) %s' % (q[0], q[1], dict(sorted(tabE[q].items()))))
