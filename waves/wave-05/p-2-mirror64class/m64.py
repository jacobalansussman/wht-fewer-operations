#!/usr/bin/env python3
"""m64.py (p-2-mirror64class): g-0's reduced model for the mirror of the subset-sum power, m base-4 digits (N = 4^m; m = 3: 64).
Targets = distinct non-zero columns of I - R^(x)m (read side) or rows (write side), up to scale.
Pool = points lying on at least two secants (lines through two targets).  A gate = a new point on a line through two present
points.  Search: start set of r independent points of targets + pool, helpers as few as possible.  Heuristic (upper bound on x).
Every reported solution is replayed exactly (integer rank tests) before it is printed.
usage: m64.py <m> <side: read|write> <seconds> <seed> [a b c d]
"""
import sys, time, random, itertools
from fractions import Fraction as Fr
from math import gcd
import numpy as np

m = int(sys.argv[1]); side = sys.argv[2]; budget = float(sys.argv[3]); seed = int(sys.argv[4])
ker = [[1, 1], [1, 0]] if len(sys.argv) < 9 else [[int(sys.argv[5]), int(sys.argv[6])], [int(sys.argv[7]), int(sys.argv[8])]]
random.seed(seed); t0 = time.time()

def kron(A, B): return [[a*b for a in ra for b in rb] for ra in A for rb in B]
def matmul(A, B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
a, b, c, d = [Fr(x) for x in (ker[0][0], ker[0][1], ker[1][0], ker[1][1])]; det = a*d - b*c
P = [[Fr(0)]*4 for _ in range(4)]; P[1][1] = Fr(1); P[2][2] = Fr(1); P[0][3] = -b/c; P[3][0] = -c/b
R = [[x/det for x in r] for r in matmul(kron([[a, b], [c, d]], [[a, b], [c, d]]), P)]
M = R
for _ in range(m-1): M = kron(M, R)
n = len(M)
M = [[(1 if i == j else 0) - M[i][j] for j in range(n)] for i in range(n)]
vecs = [[M[i][j] for i in range(n)] for j in range(n)] if side == "read" else M
def prim(v):
    den = 1
    for x in v:
        x = Fr(x); den = den*x.denominator//gcd(den, x.denominator)
    w = [int(Fr(x)*den) for x in v]; g = 0
    for x in w: g = gcd(g, abs(x))
    if g == 0: return None
    s = next(x for x in w if x != 0); s = 1 if s > 0 else -1
    return tuple(s*x//g for x in w)
T = []; seen = set(); nonzero = 0
for v in vecs:
    p = prim(v)
    if p is None: continue
    nonzero += 1
    if p not in seen: seen.add(p); T.append(p)
nT = len(T)
def irank(rows):
    A = [[Fr(x) for x in r] for r in rows]; r = 0
    for cc in range(len(A[0])):
        p = next((i for i in range(r, len(A)) if A[i][cc] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        for i in range(r+1, len(A)):
            if A[i][cc] != 0:
                f = A[i][cc]/A[r][cc]; A[i] = [x - f*y for x, y in zip(A[i], A[r])]
        r += 1
    return r
r = irank(T)
print("m=%d N=%d side=%s kernel=%s: non-zero %d, distinct targets D=%d, dimension r=%d ; gates needed D - r + x = %d + x" % (m, n, side, ker, nonzero, nT, r, nT - r))
TA = np.array(T, dtype=np.int64); G = TA @ TA.T
# collinear triples and coplanar quadruples of targets, by Gram determinants (float filter, exact confirmation)
tri = np.array(list(itertools.combinations(range(nT), 3)))
d3 = np.linalg.det(G[tri[:, :, None], tri[:, None, :]].astype(float))
ct = [tuple(t) for t in tri[np.abs(d3) < 0.5] if irank([T[i] for i in t]) == 2]
print("collinear triples of targets:", len(ct))
quad = np.array(list(itertools.combinations(range(nT), 4)))
cq = []
for s in range(0, len(quad), 200000):
    q = quad[s:s+200000]
    d4 = np.linalg.det(G[q[:, :, None], q[:, None, :]].astype(float))
    for t in q[np.abs(d4) < 0.5]:
        if irank([T[i] for i in t]) == 3: cq.append(tuple(int(x) for x in t))
print("coplanar quadruples of targets (4-term relations):", len(cq), " (%.0f s)" % (time.time() - t0)); sys.stdout.flush()
def nullvec(vs):
    k = len(vs); L = len(vs[0]); A = [[Fr(vs[j][i]) for j in range(k)] for i in range(L)]
    piv = []; rr = 0
    for cc in range(k):
        p = next((i for i in range(rr, L) if A[i][cc] != 0), None)
        if p is None: continue
        A[rr], A[p] = A[p], A[rr]; f = A[rr][cc]; A[rr] = [x/f for x in A[rr]]
        for i in range(L):
            if i != rr and A[i][cc] != 0:
                f = A[i][cc]; A[i] = [x - f*y for x, y in zip(A[i], A[rr])]
        piv.append(cc); rr += 1
    free = [cc for cc in range(k) if cc not in piv]
    if len(free) != 1: return None
    z = [Fr(0)]*k; z[free[0]] = Fr(1)
    for i, cc in enumerate(piv): z[cc] = -A[i][free[0]]
    return z
pool = {}
Tset = {p: i for i, p in enumerate(T)}
for q in cq:
    z = nullvec([T[i] for i in q])
    if z is None or any(x == 0 for x in z): continue
    for (i1, i2) in ((0, 1), (0, 2), (0, 3)):
        v = prim([z[i1]*x + z[i2]*y for x, y in zip(T[q[i1]], T[q[i2]])])
        if v is None or v in Tset: continue
        rest = tuple(q[j] for j in range(4) if j not in (i1, i2))
        pool.setdefault(v, set()).update([tuple(sorted((q[i1], q[i2]))), tuple(sorted(rest))])
Pl = sorted(pool)
hist = {}
for v in Pl: hist[len(pool[v])] = hist.get(len(pool[v]), 0) + 1
print("pool (points on at least two secants): %d ; by number of secants through them: %s" % (len(Pl), sorted(hist.items())))
W = list(T) + Pl; nW = len(W)
# lines with at least three points of W, by two random projections to 3 dimensions modulo a prime (filter), then exact check
pr = 1000003
WA = np.array(W, dtype=np.int64)
def keys(sd):
    rng = np.random.default_rng(sd); Pm = rng.integers(1, pr, size=(n, 3)); Q = (WA % pr) @ Pm % pr
    ii, jj = np.triu_indices(nW, 1)
    A, B = Q[ii], Q[jj]
    cx = (A[:, 1]*B[:, 2] - A[:, 2]*B[:, 1]) % pr; cy = (A[:, 2]*B[:, 0] - A[:, 0]*B[:, 2]) % pr; cz = (A[:, 0]*B[:, 1] - A[:, 1]*B[:, 0]) % pr
    lead = np.where(cx != 0, cx, np.where(cy != 0, cy, cz))
    inv = np.ones_like(lead); base = lead.copy(); e = pr - 2
    while e:
        if e & 1: inv = inv*base % pr
        base = base*base % pr; e >>= 1
    return ii, jj, (cx*inv % pr)*pr*pr + (cy*inv % pr)*pr + (cz*inv % pr)
ii, jj, k1 = keys(seed + 1); _, _, k2 = keys(seed + 2)
order = np.lexsort((k2, k1)); k1s, k2s = k1[order], k2[order]
same = (k1s[1:] == k1s[:-1]) & (k2s[1:] == k2s[:-1])
lines = []; s = 0; L = len(order)
bounds = np.flatnonzero(~same) + 1; starts = np.concatenate(([0], bounds)); ends = np.concatenate((bounds, [L]))
for s, e in zip(starts, ends):
    if e - s < 3: continue          # a line with 3 points gives 3 pairs
    pts = sorted(set(int(x) for x in ii[order[s:e]]) | set(int(x) for x in jj[order[s:e]]))
    if irank([W[i] for i in pts]) == 2: lines.append(pts)
    else: print("  (projection collision discarded, %d points)" % len(pts))
lh = {}
for l in lines: lh[len(l)] = lh.get(len(l), 0) + 1
print("lines with at least 3 points of targets + pool: %d ; by size %s  (%.0f s)" % (len(lines), sorted(lh.items()), time.time() - t0)); sys.stdout.flush()
inc = [[] for _ in range(nW)]
for li, l in enumerate(lines):
    for p in l: inc[p].append(li)
# independence modulo a large prime (filter), exact check at the end
BP = 2147483629
class Span:
    def __init__(s): s.rows = []; s.piv = []
    def reduce(s, v):
        v = [x % BP for x in v]
        for row, pc in zip(s.rows, s.piv):
            if v[pc]:
                f = v[pc]; v = [(x - f*y) % BP for x, y in zip(v, row)]
        return v
    def add(s, v):
        v = s.reduce(v)
        pc = next((i for i, x in enumerate(v) if x), None)
        if pc is None: return False
        iv = pow(v[pc], BP - 2, BP); v = [x*iv % BP for x in v]
        s.rows.append(v); s.piv.append(pc); return True
    def contains(s, v): return not any(s.reduce(v))
def closure_from(B, allowed=None):
    """incremental line closure. returns (present set, parent dict point -> (line, p1, p2))"""
    present = set(); cnt = {}; par = {}; stack = list(B)
    for p in B: par[p] = None
    while stack:
        p = stack.pop()
        if p in present: continue
        present.add(p)
        for li in inc[p]:
            l = lines[li]
            if allowed is not None:
                have = [q for q in l if q in present]
            else:
                have = None
            cnt[li] = cnt.get(li, 0) + 1
            if cnt[li] == 2:
                two = [q for q in l if q in present][:2]
                for q in l:
                    if q not in present and q not in par and (allowed is None or q in allowed):
                        par[q] = (li, two[0], two[1]); stack.append(q)
            elif cnt[li] > 2:
                pass
    return present, par
def closure_size_targets(B, allowed=None):
    pres, _ = closure_from(B, allowed); return pres
best = None
def attempt():
    """randomised greedy choice of r independent start points; then prune helpers"""
    sp = Span(); B = []; pres = set()
    cand_all = list(range(nW))
    while len(B) < r:
        cands = [p for p in random.sample(cand_all, min(nW, 60)) if p not in pres]
        # prefer targets as candidates half of the time
        cands += [p for p in random.sample(range(nT), min(nT, 30)) if p not in pres]
        scored = []
        for p in cands:
            if sp.contains(W[p]): continue
            pr2 = closure_size_targets(B + [p])
            scored.append((sum(1 for q in pr2 if q < nT) + 0.01*len(pr2) + random.random()*0.5, p))
            if len(scored) >= 25: break
        if not scored:
            # fall back: any independent point
            rest = [p for p in range(nW) if p not in pres and not sp.contains(W[p])]
            if not rest: return None
            p = random.choice(rest)
        else: p = max(scored)[1]
        sp.add(W[p]); B.append(p); pres = closure_size_targets(B)
    if any(t not in pres for t in range(nT)): return ("miss", sum(1 for t in range(nT) if t not in pres))
    # helpers reached; prune: keep only those on the derivation of some target, then try removals
    pres, par = closure_from(B)
    need = set(B); stack = [t for t in range(nT)]
    while stack:
        p = stack.pop()
        if p in need and par.get(p) is None and p in B: continue
        if p in need and p >= nT: continue
        need.add(p)
        if par[p] is not None:
            for q in par[p][1:]:
                if q not in need or q < nT:
                    if q not in need: stack.append(q)
                    need.add(q)
    allowed = set(range(nT)) | need
    helpers = [p for p in allowed if p >= nT]
    random.shuffle(helpers)
    for h in helpers:
        if h in B: continue
        trial = allowed - {h}
        pres2, _ = closure_from(B, trial)
        if all(t in pres2 for t in range(nT)): allowed = trial
    pres2, par2 = closure_from(B, allowed)
    used = set(p for p in pres2 if p >= nT) | set(p for p in B if p >= nT)
    # helpers present but never used as a parent and not targets can be dropped unless they are start points
    return ("ok", len(used), B, allowed, par2, pres2)
tries = 0; misses = 0
while time.time() - t0 < budget:
    res = attempt(); tries += 1
    if res is None or res[0] == "miss": misses += 1; continue
    if best is None or res[1] < best[1]:
        best = res
        print("  try %d: x = %d helpers (%.0f s)" % (tries, res[1], time.time() - t0)); sys.stdout.flush()
print("tries %d, of which %d did not reach all targets" % (tries, misses))
if best:
    _, x, B, allowed, par, pres = best
    # exact replay: B independent of rank r; every derived point lies on the line through its two parents
    assert irank([W[p] for p in B]) == r, "start set not independent"
    order = []; done = set(B); pend = [p for p in pres if p not in done]
    while pend:
        prog = False
        for p in list(pend):
            li, q1, q2 = par[p]
            if q1 in done and q2 in done:
                assert irank([W[p], W[q1], W[q2]]) == 2 and irank([W[q1], W[q2]]) == 2
                order.append((p, q1, q2)); done.add(p); pend.remove(p); prog = True
        assert prog, "cyclic derivation"
    assert all(t in done for t in range(nT))
    helpers = [p for p in done if p >= nT]
    gates = len(order)
    print("REPLAYED EXACTLY: start points %d (targets among them %d), gates %d = D - r + x with x = %d helpers" % (len(B), sum(1 for p in B if p < nT), gates, len(helpers)))
    print("  reduced-circuit gates %d ; forward %s cost = %s" % (gates, side, ("N' + D - 2r + x = %d" % (nonzero + nT - 2*r + len(helpers))) if side == "read" else ("D' - r + x' = %d" % gates)))
    print("  start:", [("t%d" % p if p < nT else "h%d" % p) for p in B])
    for (p, q1, q2) in order: print("   %s on line(%s, %s)" % (*[("t%d" % z if z < nT else "h%d" % z) for z in (p, q1, q2)],))
    for p in helpers: print("  h%d =" % p, W[p])
