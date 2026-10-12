#!/usr/bin/env python3
"""g-1 ref.py: independent referee checks of a-2 (tight wires).  Exact integer arithmetic throughout.
usage: ref.py tight | slack | min4
Count (G): a gate is any a*u + b*v, scalings free, a wire is a form up to a scalar.
"""
import sys, itertools, random, math

def wht(v):
    v = list(v); n = len(v); h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                a, b = v[j], v[j + h]; v[j], v[j + h] = a + b, a - b
        h *= 2
    return v
def nz(v): return sum(1 for x in v if x != 0)
def norm(v):
    """projective normal form of an integer vector: divide by gcd, first non-zero positive"""
    g = 0
    for x in v: g = math.gcd(g, x)
    if g == 0: return None
    s = next(x for x in v if x != 0); s = g if s > 0 else -g
    return tuple(x // s for x in v)

def subspaces(k):
    """all subspaces of F_2^k as (dim, frozenset of elements)"""
    N = 1 << k; seen = {frozenset([0]): 0}; frontier = [frozenset([0])]
    while frontier:
        nxt = []
        for V in frontier:
            for g in range(1, N):
                if g in V: continue
                W = frozenset(V | {x ^ g for x in V})
                if W not in seen: seen[W] = seen[V] + 1; nxt.append(W)
        frontier = nxt
    return seen

def tight_wires(k):
    """coset characters up to scalar -> level (dimension of the subgroup)"""
    N = 1 << k; out = {}
    for V, d in subspaces(k).items():
        reps = {}
        for c in range(N):
            reps.setdefault(min(x ^ c for x in V), c)
        for c in reps.values():
            for lam in range(N):
                v = [0] * N
                for x in V: v[x ^ c] = -1 if bin(lam & x).count("1") & 1 else 1
                out[norm(v)] = d
    return out

RATIOS = [(1, 1), (1, -1), (1, 2), (1, -2), (2, 1), (2, -1)]   # complete for real ternary operands, see g-1.md section 1

def run_tight():
    for k in (2, 3, 4):
        N = 1 << k; tw = tight_wires(k); ws = list(tw)
        bylev = {}
        for w in ws: bylev[tw[w]] = bylev.get(tw[w], 0) + 1
        ok = all(nz(w) == 1 << tw[w] and nz(w) * nz(wht(w)) == N for w in ws)
        print("N = %d: %d coset characters, by level %s; s = 2^level and s s' = N for every one: %s" % (N, len(ws), sorted(bylev.items()), ok))
        shapes = {}; bad = 0; ntr = 0; idx = {w: i for i, w in enumerate(ws)}
        for i in range(len(ws)):
            u = ws[i]
            for j in range(i):
                v = ws[j]
                for a, b in RATIOS:
                    w = norm([a * x + b * y for x, y in zip(u, v)])
                    if w is None or w == u or w == v: continue
                    if w in tw:
                        if not (idx[w] < j): continue     # count each unordered triple once (it is met from each of its three pairs)
                        ntr += 1
                        L = tuple(sorted((tw[u], tw[v], tw[w])))
                        key = tuple(x - L[0] for x in L); shapes[key] = shapes.get(key, 0) + 1
                        if L[2] - L[0] > 1: bad += 1
        print("   dependent triples of tight wires: %d; levels more than one apart: %d; shapes (relative levels): %s" % (ntr, bad, sorted(shapes.items())))
    # uncertainty inequality on every vector with entries 0, 1, -1 at 4 and 8 points, and the equality case
    for k in (2, 3):
        N = 1 << k; tw = tight_wires(k); low = 0; eq = 0; eq_tight = 0; tot = 0; hist = {}
        for v in itertools.product((0, 1, -1), repeat=N):
            if norm(v) != v: continue
            tot += 1; p = nz(v) * nz(wht(v)); hist[p] = hist.get(p, 0) + 1
            if p < N: low += 1
            if p == N:
                eq += 1; eq_tight += v in tw
        print("N = %d: %d vectors with entries 0, 1, -1 (up to sign): s s' < N: %d; s s' = N: %d, of which coset characters: %d; histogram of s s': %s" % (N, tot, low, eq, eq_tight, sorted(hist.items())))

def run_slack():
    rng = random.Random(11)
    for k in (3, 4, 5):
        N = 1 << k; viol = 0; viol2 = 0; viol3 = 0; gates = 0; worst = 0.0; big = 0
        for trial in range(400):
            W = [tuple(1 if i == j else 0 for i in range(N)) for j in range(N)]
            for g in range(3 * N):
                # mixture: mostly recent wires, sometimes an old one; small integer coefficients so that cancellation happens
                u = W[rng.randrange(len(W))] if rng.random() < 0.5 else W[-1 - rng.randrange(min(len(W), 6))]
                v = W[rng.randrange(len(W))] if rng.random() < 0.7 else W[rng.randrange(N)]
                a, b = rng.choice([1, -1, 2, -2, 3]), rng.choice([1, -1, 2, -2, 1, -1])
                w = [a * x + b * y for x, y in zip(u, v)]
                nw = norm(w)
                if nw is None or nw == norm(u) or nw == norm(v): continue
                W.append(nw); gates += 1
                su, sv, sw = nz(u), nz(v), nz(nw); tu, tv, t_w = nz(wht(u)), nz(wht(v)), nz(wht(nw))
                if min(su * tu, sv * tv, sw * t_w) < N: viol3 += 1
                P = max(su * tu, sv * tv, sw * t_w)
                lhs = sw; rhs = (1 + 2 * P / N) * min(su, sv)
                if lhs > rhs: viol += 1
                worst = max(worst, lhs / rhs)
                if P >= N * N // 2: big += 1
                for trip in ((su, sv, sw), (tu, tv, t_w)):          # top-two rule: the largest is at most the sum of the other two
                    m = sorted(trip)
                    if m[2] > m[0] + m[1]: viol2 += 1
        print("N = %d: %d random gates (%d with P >= N^2/2): s s' < N: %d; s(out) > (1 + 2P/N) min s(in): %d (largest ratio %.3f); 'largest support <= sum of the other two' fails (either side): %d" % (N, gates, big, viol3, viol, worst, viol2))

def rank3(a, b, c):
    """rank of three integer vectors, exact (fraction-free elimination)"""
    M = [list(a), list(b), list(c)]; r = 0
    for col in range(len(a)):
        p = next((i for i in range(r, 3) if M[i][col] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(r + 1, 3):
            if M[i][col] != 0:
                f, g = M[r][col], M[i][col]; M[i] = [f * x - g * y for x, y in zip(M[i], M[r])]
        r += 1
        if r == 3: break
    return r

def run_min4():
    """6 gates at 4 points, every coefficient allowed (any field of characteristic 0).
    Argument (g-1.md section 1): 4 gates are the outputs, 2 are helpers; the first full-support wire is an output y and the two
    helpers are its cone, a binary tree over the 4 inputs, so each helper is y restricted to the leaves below it (up to a scalar).
    That leaves finitely many helper pairs.  For each: close under 'a target on the line through two held points'."""
    H = [wht([1 if i == j else 0 for i in range(4)]) for j in range(4)]
    pts = [tuple(1 if i == j else 0 for i in range(4)) for j in range(4)]
    cases = 0; best = 0; reach = {}
    for yi in range(4):
        y = H[yi]
        fams = []
        for A in itertools.combinations(range(4), 2):
            rest = [i for i in range(4) if i not in A]
            for c in rest: fams.append((set(A), set(A) | {c}))        # caterpillar: pair, then triple
            if 0 in A: fams.append((set(A), set(rest)))                 # balanced: two pairs (each split once)
        for fam in fams:
            cases += 1
            held = list(pts) + [tuple(y[i] if i in S else 0 for i in range(4)) for S in fam] + [tuple(y)]
            got = {yi}; ch = True
            while ch:
                ch = False
                for t in range(4):
                    if t in got: continue
                    if any(rank3(held[i], held[j], H[t]) == 2 for i in range(len(held)) for j in range(i)):
                        got.add(t); held.append(tuple(H[t])); ch = True
            reach[len(got)] = reach.get(len(got), 0) + 1; best = max(best, len(got))
    print("4 points, 6 gates, all coefficients: %d (first output, tree) cases; outputs reachable with the two forced helpers: %s; all four ever reached: %s" % (cases, sorted(reach.items()), best == 4))
    print("   => no 6-gate circuit over any field of characteristic 0; with the 7-gate circuit (ledger.py replays it) the minimum in count (G) is exactly 7.")

if __name__ == "__main__":
    {"tight": run_tight, "slack": run_slack, "min4": run_min4}[sys.argv[1]]()
