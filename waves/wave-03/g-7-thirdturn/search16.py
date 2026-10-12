#!/usr/bin/env python3
"""g-7-thirdturn / search16.py -- 16 points, exact integers.  Count (G), measured by a fixed, simple yardstick:
'pair sharing' = greedy common-pair extraction (a new node u + c*v whenever the same pair with the same ratio occurs in two
or more targets), then every target is finished alone.  It is an UPPER bound on the count (G) and it does not know the
7-gate brick (it gives 8 for the 4-point transform, 64 for the 16-point one, 32 for the half transform).
Search: B = [f, fR, fR^2 for 5 seeds f; one fixed form f0], seeds from the 4320 real 'stabilizer' vectors
(orbit of a coordinate under butterflies, sign changes (-1)^(x_i x_j), (-1)^(x_i), address additions).
usage: search16.py <mode: B | both> <seconds> <rng seed> [start: L | rand]
"""
import sys, time, random, json
from math import gcd
from fractions import Fraction as F
pc = lambda x: bin(x).count("1")
n = 16; j = 2; lo = 3
w = lambda p, y: (pc((p >> j) & (y & lo)) + pc((p & lo) & (y >> j))) & 1
Q0 = lambda x: pc((x >> j) & (x & lo)) & 1
S = [[-1 if w(p, y) else 1 for y in range(n)] for p in range(n)]
T = [(-1) ** Q0(x) for x in range(n)]
def prim(v):
    g = 0
    for x in v: g = gcd(g, abs(x))
    if g == 0: return None
    s = 1
    for x in v:
        if x != 0: s = 1 if x > 0 else -1; break
    return tuple(s * x // g for x in v)
def Rmap(f):      # f -> f T S, primitive
    ft = [f[x] * T[x] for x in range(n)]
    return prim([sum(ft[x] * S[x][y] for x in range(n) if ft[x]) for y in range(n)])
# --- stabilizer vectors
def gens(f):
    out = []
    for i in range(4):
        b = 1 << i
        out.append(prim([f[x & ~b] + (-1 if x & b else 1) * f[x | b] for x in range(n)]))          # butterfly on bit i
        out.append(prim([f[x] * (-1 if x & b else 1) for x in range(n)]))                           # sign (-1)^(x_i)
        out.append(prim([f[x ^ b] for x in range(n)]))                                              # address shift
        for k in range(i + 1, 4):
            c = 1 << k
            out.append(prim([f[x] * (-1 if (x & b) and (x & c) else 1) for x in range(n)]))         # sign (-1)^(x_i x_k)
            out.append(prim([f[x ^ (c if x & b else 0)] for x in range(n)]))                        # address addition
            out.append(prim([f[x ^ (b if x & c else 0)] for x in range(n)]))
    return out
def stabs():
    e0 = tuple([1] + [0] * 15); seen = {e0}; fr = [e0]
    while fr:
        nx = []
        for f in fr:
            for g in gens(f):
                if g not in seen: seen.add(g); nx.append(g)
        fr = nx
    return sorted(seen)
# --- yardstick
def cse(rows, rng=None):
    tg = [{i: c for i, c in enumerate(r) if c} for r in rows]; nodes = len(rows[0]); ng = 0; prog = []
    while True:
        cnt = {}
        for d in tg:
            if len(d) < 2: continue
            it = sorted(d.items()); L = len(it)
            for i in range(L):
                a, ca = it[i]
                for k in range(i + 1, L):
                    b, cb = it[k]; g = gcd(ca, cb); p, q = ca // g, cb // g
                    if p < 0: p, q = -p, -q
                    key = (a, b, p, q); cnt[key] = cnt.get(key, 0) + 1
        if not cnt: break
        mx = max(cnt.values())
        if mx < 2: break
        cands = [k for k, v in cnt.items() if v == mx]
        key = rng.choice(cands) if rng else min(cands)
        a, b, p, q = key; new = nodes; nodes += 1; ng += 1; prog.append((new, a, b, p, q))
        for d in tg:
            if a in d and b in d and d[a] * q == d[b] * p:
                lam = d[a] // p; del d[a]; del d[b]; d[new] = lam
    cost = ng; done = set()
    for d in tg:
        it = sorted(d.items()); g = 0
        for _, c in it: g = gcd(g, abs(c))
        s = 1 if it[0][1] > 0 else -1; key = tuple((v, s * c // g) for v, c in it)
        if key in done: continue
        done.add(key); cost += len(d) - 1
    return cost, prog, tg
def inv_int(M):
    A = [[F(v) for v in r] + [F(int(i == k)) for k in range(n)] for i, r in enumerate(M)]
    for c in range(n):
        p = next((i for i in range(c, n) if A[i][c] != 0), None)
        if p is None: return None
        A[c], A[p] = A[p], A[c]; pv = A[c][c]; A[c] = [v / pv for v in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c]; A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    out = []
    for r in A:
        r = r[n:]; den = 1
        for v in r: den = den * v.denominator // gcd(den, v.denominator)
        out.append(prim([int(v * den) for v in r]))
    return out
PR = 1000003
def full_rank(M):
    A = [[v % PR for v in r] for r in M]; r = 0
    for c in range(n):
        p = next((i for i in range(r, n) if A[i][c]), None)
        if p is None: return False
        A[r], A[p] = A[p], A[r]; iv = pow(A[r][c], PR - 2, PR)
        for i in range(r + 1, n):
            if A[i][c]:
                f = A[i][c] * iv % PR; A[i] = [(x - f * y) % PR for x, y in zip(A[i], A[r])]
        r += 1
    return True
if __name__ == "__main__":
    mode, secs, seed = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]); start = sys.argv[4] if len(sys.argv) > 4 else "L"
    rng = random.Random(seed); t0 = time.time()
    st = stabs(); idx = {v: i for i, v in enumerate(st)}
    nxt = [idx[Rmap(v)] for v in st]
    assert all(nxt[nxt[nxt[i]]] == i for i in range(len(st)))
    fixed = [i for i in range(len(st)) if nxt[i] == i]
    trip = sorted({tuple(sorted((i, nxt[i], nxt[nxt[i]]))) for i in range(len(st)) if nxt[i] != i})
    wt = lambda i: sum(1 for x in st[i] if x)
    types = {}
    for t in trip:
        k = tuple(sorted(wt(i) for i in t)); types[k] = types.get(k, 0) + 1
    print("stabilizer vectors: %d; fixed by R: %d (weights %s); three-cycles: %d; weight types of the cycles: %s" % (
        len(st), len(fixed), sorted({wt(i) for i in fixed}), len(trip), dict(sorted(types.items()))), flush=True)
    # calibration of the yardstick
    H2 = [[1, 1], [1, -1]]
    kron = lambda A, B: [[a * b for a in ra for b in rb] for ra in A for rb in B]
    H4 = kron(H2, H2); I4 = [[int(a == b) for b in range(4)] for a in range(4)]
    print("yardstick: 4-point transform %d (textbook 8, best 7); half transform at 16 points %d (textbook 32, with bricks 28); 16-point transform %d (textbook 64, best 56)" % (
        cse(H4)[0], cse(kron(H4, I4))[0], cse(kron(H4, H4))[0]), flush=True)
    light = [t for t in trip if sum(wt(i) for i in t) <= 12]
    mid = [t for t in trip if sum(wt(i) for i in t) <= 18]
    def rows_of(state):
        tr, f0 = state; rows = []
        for t in tr: rows += [st[i] for i in t]
        rows.append(st[f0]); return rows
    def energy(state):
        rows = rows_of(state)
        if len(set(rows)) < 16 or not full_rank(rows): return None
        cB = cse(rows)[0]
        if mode == "B": return (cB, cB, None)
        Bi = inv_int(rows); cI = cse(Bi)[0]
        return (cB + cI, cB, cI)
    def start_state():
        if start == "L":
            # half-transform basis: rows sum_{p1} (-1)^(a.p1) e_(p1,b)
            rows = [prim([((-1) ** pc(a & (y >> j))) if (y & lo) == b else 0 for y in range(n)]) for a in range(4) for b in range(4)]
            ids = [idx[r] for r in rows]; f0 = next(i for i in ids if nxt[i] == i)
            tr = sorted({tuple(sorted((i, nxt[i], nxt[nxt[i]]))) for i in ids if nxt[i] != i})
            assert len(tr) == 5
            return (list(tr), f0)
        while True:
            s = ([rng.choice(light) for _ in range(5)], rng.choice(fixed))
            if energy(s) is not None: return s
    s = start_state(); E = energy(s); best = E; bests = [(E, s)]; hist = {}; nev = 0; temp = 0.7
    print("start (%s): total %s  cost(B) %s  cost(B^-1) %s" % (start, E[0], E[1], E[2]), flush=True)
    while time.time() - t0 < secs:
        tr, f0 = list(s[0]), s[1]; m = rng.random()
        if m < 0.15: f0 = rng.choice(fixed)
        else:
            pool = light if m < 0.6 else (mid if m < 0.9 else trip)
            tr[rng.randrange(5)] = rng.choice(pool)
        s2 = (tr, f0); E2 = energy(s2)
        if E2 is None: continue
        nev += 1; hist[E2[0]] = hist.get(E2[0], 0) + 1
        if E2[0] <= E[0] or rng.random() < pow(2.718281828, -(E2[0] - E[0]) / temp):
            s, E = s2, E2
            if E[0] < best[0]:
                best = E; bests.append((E, s)); print("  t=%.0f best total %s  cost(B) %s  cost(B^-1) %s  after %d states" % (time.time() - t0, E[0], E[1], E[2], nev), flush=True)
    print("DONE mode=%s seed=%d states=%d best=%s histogram(lowest)=%s" % (mode, seed, nev, best, {k: hist[k] for k in sorted(hist)[:8]}))
    E, s = bests[-1]; rows = rows_of(s)
    print("best B (rows in threes f, fR, fR^2; last row fixed), weights of rows:", [sum(1 for x in r if x) for r in rows])
    for r in rows: print("   ", " ".join("%2d" % x for x in r))
    c, prog, tg = cse(rows); print("pair-sharing program for B: %d gates; nodes:" % c, prog)
    if mode != "B":
        Bi = inv_int(rows); c2, prog2, tg2 = cse(Bi)
        print("B^-1 rows (scaled to integers):")
        for r in Bi: print("   ", " ".join("%2d" % x for x in r))
        print("pair-sharing program for B^-1: %d gates" % c2)
    json.dump({"E": E, "triples": [list(t) for t in s[0]], "f0": s[1], "rows": [list(r) for r in rows]}, open("best_%s_%d_%s.json" % (mode, seed, start), "w"))
