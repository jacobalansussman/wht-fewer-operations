# ab-4-zcut/zmeter.py : x-2's cut meter on every optimal 12-gate circuit for subset sums Z at 8 points.  Count (G). Exact.
# usage: python3 -B zmeter.py <p> <file of mincirc_all output with every set printed>
# A circuit = the 5 helpers of one line "example ..." plus the 7 non-input rows of Z.  Digits modulo p are lifted to whole
# numbers (p = 2: 0/1; p = 3: 2 read as -1) and the circuit is REPLAYED over the rationals: a wire is made when it lies in
# the span of two wires already made (inputs are made).  Sets that do not replay over Q are counted and skipped.
# Meter [x-2.md section 1], for a pair of projections (P1, P2) of a wire (a, b), a = entries on L, b = entries on R:
#   class of a wire at Pi = Pi(wire) up to a factor; trivial when zero or the image of an input.
#   n(i) = number of distinct non-trivial classes at Pi (does not depend on the order of the gates)
#   E - B = gates - n(1) - n(2) (order-free);  B = gates first in their class at both, E = gates first at neither:
#   B and E depend on the order; least and largest B over ALL valid orders by a walk over subsets of gates.
# Cuts: 'coord' P1 = a, P2 = b (x-2's cut);  'skew' P1 = a, P2 = 2b - a (rows (z,0), (z,z) become (z,-z), (z,z): H's shape).
import sys, itertools, re
from fractions import Fraction as F
from math import gcd
N = 8
Zrows = [tuple(1 if (T & S) == T else 0 for T in range(N)) for S in range(N)]
targets = Zrows[1:]
inputs = [tuple(int(i == j) for j in range(N)) for i in range(N)]
def prim(v):
    g = 0
    for t in v: g = gcd(g, t)
    if g == 0: return None
    s = next(t for t in v if t); s = g if s > 0 else -g
    return tuple(t // s for t in v)
def in_span(w, u, v):
    for i in range(N):
        for j in range(i + 1, N):
            d = u[i] * v[j] - u[j] * v[i]
            if d:
                a = F(w[i] * v[j] - w[j] * v[i], d); b = F(u[i] * w[j] - u[j] * w[i], d)
                return all(a * u[t] + b * v[t] == w[t] for t in range(N))
    return False
def pairs_for(wires):
    """for each gate g: list of (maskneeded) = sets of other gates (0, 1 or 2 of them) that with inputs span it"""
    allp = inputs + wires; out = []
    for g, w in enumerate(wires):
        need = set()
        for i, j in itertools.combinations(range(len(allp)), 2):
            if i - N == g or j - N == g: continue
            if in_span(w, allp[i], allp[j]):
                m = 0
                if i >= N: m |= 1 << (i - N)
                if j >= N: m |= 1 << (j - N)
                need.add(m)
        out.append(sorted(need))
    return out
def projections(kind, c):
    L = [x for x in range(N) if not x >> c & 1]; R = [x | 1 << c for x in L]
    if kind == 'coord': return (lambda w: [w[i] for i in L]), (lambda w: [w[i] for i in R])
    if kind == 'skew': return (lambda w: [w[i] for i in L]), (lambda w: [2 * w[j] - w[i] for i, j in zip(L, R)])
def meter(wires, need, kind, c):
    P1, P2 = projections(kind, c); G = len(wires)
    triv = [set(), set()]
    for x in inputs:
        for s, P in enumerate((P1, P2)): triv[s].add(prim(P(x)))
    cl = []
    for w in wires:
        a, b = prim(P1(w)), prim(P2(w))
        cl.append((None if a in triv[0] else a, None if b in triv[1] else b))
    n1 = len({a for a, b in cl if a is not None}); n2 = len({b for a, b in cl if b is not None})
    full = (1 << G) - 1; INF = 99
    lo = {0: 0}; hi = {0: 0}; frontier = [0]; seen = {0}
    # walk subsets in order of size
    for size in range(G):
        nxt = set()
        for S in frontier:
            for g in range(G):
                if S >> g & 1: continue
                if not any(m & S == m for m in need[g]): continue
                a, b = cl[g]
                na = a is not None and not any((S >> h & 1) and cl[h][0] == a for h in range(G))
                nb = b is not None and not any((S >> h & 1) and cl[h][1] == b for h in range(G))
                d = 1 if (na and nb) else 0; T = S | 1 << g
                if T not in lo or lo[S] + d < lo[T]: lo[T] = lo[S] + d
                if T not in hi or hi[S] + d > hi[T]: hi[T] = hi[S] + d
                nxt.add(T)
        frontier = list(nxt)
    assert full in lo, 'no valid order'
    return n1, n2, G - n1 - n2, lo[full], hi[full]
def lift(d, p): return tuple((x if x <= p // 2 else x - p) for x in d)
def main():
    p = int(sys.argv[1]); path = sys.argv[2]; kinds = sys.argv[3:] or ['coord', 'skew']
    sets = []
    for line in open(path):
        if 'example' not in line: continue
        hs = re.findall(r'\[(\d+)\]', line); sets.append([lift([int(ch) for ch in h], p) for h in hs])
    ok = 0; bad = 0; tab = {k: {} for k in kinds}; perc = {k: {} for k in kinds}; ex = {}
    for hs in sets:
        wires = list(hs) + list(targets)
        need = pairs_for(wires)
        # replayable?
        made = 0; ch = True
        while ch:
            ch = False
            for g in range(len(wires)):
                if not made >> g & 1 and any(m & made == m for m in need[g]): made |= 1 << g; ch = True
        if made != (1 << len(wires)) - 1: bad += 1; continue
        ok += 1
        for k in kinds:
            trip = []
            for c in range(3):
                r = meter(wires, need, k, c); trip.append(r)
                tab[k][r] = tab[k].get(r, 0) + 1
                ex.setdefault((k, r), (hs, c))
            key = tuple(sorted((r[2], r[3]) for r in trip)); perc[k][key] = perc[k].get(key, 0) + 1
    print('p=%d: %d sets read; %d replay over Q with this lift (12 gates), %d do not' % (p, len(sets), ok, bad))
    for k in kinds:
        print('cut kind %s: (n1, n2, E - B, least B over orders, largest B over orders) : number of (circuit, cut) pairs' % k)
        for r in sorted(tab[k]): print('   n1=%d n2=%d E-B=%d Bmin=%d Bmax=%d : %d   e.g. helpers %s cut bit %d' % (*r, tab[k][r], [''.join('%d' % x if x >= 0 else 'm' for x in h) for h in ex[(k, r)][0]], ex[(k, r)][1]))
        print('   per circuit, the three cuts as sorted (E - B, least B): count')
        for key in sorted(perc[k]): print('     %s : %d' % (key, perc[k][key]))
main()
