#!/usr/bin/env python3
"""gen2.py  (h-8-provethewrongthi, 2026-10-11)   exact integers only.

mode "wide k":  check of the lemma "no lone wide wire" at N = 2^k.  For every tight line whose two tight wires differ by
                3 or more levels: is any non-tight point of that line on a second tight line?  (derived: never)
mode "chain k": the smallest configuration the level count cannot charge.  h1 = a full hub (s*s' = 4N, seven tight lines
                through it).  h2 = a*h1 + b*t with t tight (so h1 and h2 meet in a gate), and h2 lands on a tight wire w
                with a tight partner p (h2 on the tight line through p and w).  Lists such h2 by (s, s'), the level of t,
                and the levels of p and w.  A landing with level difference 3 is a gate that crosses three levels.
"""
import sys, itertools
from math import gcd
from collections import defaultdict
mode = sys.argv[1]; k = int(sys.argv[2]); N = 1 << k
pc = lambda x: bin(x).count("1")
def norm(v):
    g = 0
    for a in v: g = gcd(g, abs(a))
    if g == 0: return None
    v = [a // g for a in v]
    for a in v:
        if a != 0:
            if a < 0: v = [-b for b in v]
            break
    return tuple(v)
def subspaces():
    subs = set()
    for r in range(k + 1):
        for gens in itertools.combinations(range(1, N), r):
            S = {0}
            for g in gens: S |= {s ^ g for s in S}
            if len(S) == 1 << r: subs.add(frozenset(S))
    return subs
tight = {}
for V in subspaces():
    chars = set()
    for a in range(N): chars.add(tuple((x, (-1) ** pc(a & x)) for x in sorted(V)))
    reps = sorted({min(c ^ v for v in V) for c in range(N)})
    for c in reps:
        for ch in chars:
            vec = [0] * N
            for x, sg in ch: vec[x ^ c] = sg
            tight[norm(vec)] = len(V).bit_length() - 1
T = sorted(tight); lev = [tight[t] for t in T]; nT = len(T)
print("N =", N, "tight wires:", nT, "per level:", [lev.count(d) for d in range(k + 1)], flush=True)
def had(v): return [sum(v[x] * (-1) ** pc(x & y) for x in range(N)) for y in range(N)]
def ss(v): return sum(1 for a in v if a), sum(1 for a in had(v) if a)
dot = lambda a, b: sum(x * y for x, y in zip(a, b))

def meet(u, v, skip=()):
    """all (p, w, h): tight p, w (indices) and h = a non-zero vector in span(u,v) and in span(T[p],T[w])"""
    uu, vv, uv = dot(u, u), dot(v, v), dot(u, v)
    D = uu * vv - uv * uv
    groups = defaultdict(list)
    for p in range(nT):
        if p in skip: continue
        P = T[p]; up, vp = dot(u, P), dot(v, P)
        c1 = vv * up - uv * vp; c2 = uu * vp - uv * up
        r = [D * P[x] - c1 * u[x] - c2 * v[x] for x in range(N)]
        g = 0
        for a in r: g = gcd(g, abs(a))
        if g == 0: continue
        sgn = 1
        for a in r:
            if a != 0:
                if a < 0: sgn = -1
                break
        groups[tuple(sgn * a // g for a in r)].append((p, sgn * g))
    for key, mem in groups.items():
        if len(mem) < 2: continue
        for (p, lp), (w, lw) in itertools.combinations(mem, 2):
            h = norm([lw * T[p][x] - lp * T[w][x] for x in range(N)])
            if h is not None: yield p, w, h

if mode == "wide":
    wide = 0; bad = 0; pts = 0
    for i in range(nT):
        for j in range(i + 1, nT):
            if abs(lev[i] - lev[j]) < 3: continue
            wide += 1
            for p, w, h in meet(T[i], T[j], skip=(i, j)):
                if h in tight: continue
                pts += 1; bad += 1
                if bad <= 5: print("  EXCEPTION", T[i], T[j], T[p], T[w], h)
    print("tight pairs with level difference >= 3:", wide, "; non-tight points of such a line that lie on a second tight line:", bad, " (derived: 0)")
else:
    hubs = {3: [(1, 1, 1, -1, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, -1, -1)], 2: [(1, 1, 1, -1)],
            4: [(1, 1, 1, -1) + (0,) * 12, (1, 1, 1, 1, 1, 1, -1, -1) + (0,) * 8, (1,) * 12 + (-1,) * 4]}[k]
    for h1 in hubs:
        s1, sp1 = ss(h1)
        stat = defaultdict(int); ex = {}
        seen = set()
        for ti in range(nT):
            t = T[ti]
            for p, w, h2 in meet(h1, t, skip=(ti,)):
                if h2 in tight or h2 == norm(h1): continue
                key0 = (h2, ti, frozenset((p, w)))
                if key0 in seen: continue
                seen.add(key0)
                s, sp = ss(h2)
                lv = tuple(sorted((lev[p], lev[w])))
                key = (s, sp, "t level %d" % lev[ti], "landing line levels %s" % (lv,))
                stat[key] += 1; ex.setdefault(key, (h2, t, T[p], T[w]))
        print("hub h1 =", list(h1), "(s,s') =", (s1, sp1))
        print("  second wires h2 = a*h1 + b*t that lie on a tight line (p, w):  (s, s', level of t, levels on the landing line) : count, example h2 | t | p | w")
        for key in sorted(stat):
            e = ex[key]
            print("   ", key, ":", stat[key], " e.g.", list(e[0]), "|", list(e[1]), "|", list(e[2]), "|", list(e[3]))
        byd = defaultdict(int)
        for key, c in stat.items():
            lo, hi = [int(z) for z in key[3].split("(")[1].rstrip(")").split(",")]
            byd[hi - lo] += c
        print("  landings by level difference of the landing line:", dict(sorted(byd.items())), flush=True)
