#!/usr/bin/env python3
"""gen1.py  (h-8-provethewrongthi, 2026-10-11)   exact integers only.

Question: which over-limit wires can live with tight neighbours only?
A wire = a linear form on N = 2^k inputs up to a scalar.  Tight = a character on a coset (s*s' = N), level d = log2 s.
A "tight line" = the 2-dimensional span of two non-parallel tight wires.  A gate a*u + b*v = w is three wires on one line.
An over-limit wire that is MADE from two tight wires and READ into a tight wire with a tight partner lies on two
different tight lines.  This program lists every non-tight wire that lies on at least two tight lines (any rational
coefficients: the wire is the intersection of the two lines, so nothing is assumed about its entries), and for each:
s, s', and for every tight line through it the levels of the tight wires on that line.

usage: gen1.py k [out.json]
"""
import sys, json, itertools
from math import gcd
from collections import defaultdict

k = int(sys.argv[1]); N = 1 << k
out = sys.argv[2] if len(sys.argv) > 2 else None
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
    for a in range(N):
        chars.add(tuple((x, (-1) ** pc(a & x)) for x in sorted(V)))
    reps = sorted({min(c ^ v for v in V) for c in range(N)})
    for c in reps:
        for ch in chars:
            vec = [0] * N
            for x, sg in ch: vec[x ^ c] = sg
            tight[norm(vec)] = len(V).bit_length() - 1
T = sorted(tight)
lev = [tight[t] for t in T]
nT = len(T)
print("N =", N, "tight wires:", nT, "per level:", [lev.count(d) for d in range(k + 1)])

def had(v):
    return [sum(v[x] * (-1) ** pc(x & y) for x in range(N)) for y in range(N)]
def ss(v):
    return sum(1 for a in v if a), sum(1 for a in had(v) if a)

dot = lambda a, b: sum(x * y for x, y in zip(a, b))
G = [[dot(T[i], T[j]) for j in range(nT)] for i in range(nT)]

found = defaultdict(set)      # non-tight wire -> set of tight lines (as frozenset of the tight wires on that line)
lines = {}                    # (i,j) -> frozenset of all tight wires on the line through i,j
for i in range(nT):
    u = T[i]
    for j in range(i + 1, nT):
        v = T[j]
        uu, vv, uv = G[i][i], G[j][j], G[i][j]
        D = uu * vv - uv * uv
        groups = defaultdict(list); online = [i, j]
        for p in range(nT):
            if p == i or p == j: continue
            up, vp = G[i][p], G[j][p]
            c1 = vv * up - uv * vp; c2 = uu * vp - uv * up
            P = T[p]
            r = [D * P[x] - c1 * u[x] - c2 * v[x] for x in range(N)]
            g = 0
            for a in r: g = gcd(g, abs(a))
            if g == 0: online.append(p); continue
            sgn = 1
            for a in r:
                if a != 0:
                    if a < 0: sgn = -1
                    break
            key = tuple(sgn * a // g for a in r)
            groups[key].append((p, sgn * g))
        L = frozenset(online); lines[(i, j)] = L
        for key, mem in groups.items():
            if len(mem) < 2: continue
            for (p, lp), (w, lw) in itertools.combinations(mem, 2):
                # residual(p) = lp*key, residual(w) = lw*key  =>  lw*p - lp*w lies in span(u,v)
                h = norm([lw * T[p][x] - lp * T[w][x] for x in range(N)])
                if h is None or h in tight: continue
                found[h].add(L)
                # the other line is recorded when (p,w) is the outer pair

# statistics
print("non-tight wires on at least two tight lines:", sum(1 for h in found if len(found[h]) >= 2),
      " (on exactly one, seen as an intersection: %d)" % sum(1 for h in found if len(found[h]) < 2))
stat = defaultdict(int); worst = 0; examples = {}
maxdiff_two = 0
rows = []
for h, Ls in found.items():
    if len(Ls) < 2: continue
    s, sp = ss(h)
    diffs = []
    for L in Ls:
        ls = sorted(lev[t] for t in L)
        diffs.append((ls[0], ls[-1], len(L)))
    diffs.sort()
    md = max(b - a for a, b, _ in diffs)
    maxdiff_two = max(maxdiff_two, md)
    worst = max(worst, s * sp / N)
    # landings: tight wires one gate from h, per level
    land = defaultdict(set)
    for L in Ls:
        for t in L: land[lev[t]].add(t)
    landc = tuple(sorted((d, len(ts)) for d, ts in land.items()))
    key = (s, sp, len(Ls), md, landc)
    stat[key] += 1
    examples.setdefault(key, h)
    rows.append((h, s, sp, [sorted(L) for L in Ls]))
print("largest s*s'/N among them: %.4f   (derived bound: 6.25)" % worst)
print("largest level difference on a tight line through such a wire:", maxdiff_two, "  (derived: at most 2)")
print("classes  (s, s', tight lines through it, largest level difference, [(level, tight wires one gate away)]) : count, example")
for key in sorted(stat):
    print("  ", key, ":", stat[key], " e.g.", list(examples[key]))

# the converse check: a tight line whose two wires differ by 3 or more levels: does any non-tight point on it lie on another tight line?
bad = 0; wide = 0
for (i, j), L in lines.items():
    ls = [lev[t] for t in L]
    if max(ls) - min(ls) >= 3:
        wide += 1
        for h, Ls in found.items():
            if L in Ls and len(Ls) >= 2: bad += 1
print("tight lines with level difference >= 3:", wide, "; non-tight wires on such a line AND on a second tight line:", bad, " (derived: 0)")

if out:
    json.dump({"N": N, "tight": [list(t) for t in T], "level": lev,
               "gen1": [{"h": list(h), "s": s, "sp": sp, "lines": Ls} for h, s, sp, Ls in rows]}, open(out, "w"))
    print("wrote", out)
