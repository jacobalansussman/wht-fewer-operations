#!/usr/bin/env python3
"""Exact search for the minimum number of gates for the 4-point Walsh-Hadamard transform.

Picture: a gate a*u+b*v is a new POINT on the LINE through two earlier points of projective 3-space.
Start: the 4 coordinate points. Goal: the 4 Hadamard points (rows of H_4), each up to scaling (count G).

mode G : outputs are tested EXACTLY (is the output on a line through two points we hold?), so the only
         enumerated quantity is the coefficient ratio of the gates that are NOT outputs (set T).
mode O : every gate is u+v or u-v with no scaling at all (vectors up to overall sign), outputs must be +-row.
Usage: min4.py G|O <gates> [tset]
"""
import sys
from math import gcd
from itertools import combinations

mode = sys.argv[1]
S = int(sys.argv[2])
tname = sys.argv[3] if len(sys.argv) > 3 else 'small'
TS = {
    'pm1': [(1, 1), (1, -1)],
    'small': [(1, 1), (1, -1), (1, 2), (1, -2), (2, 1), (2, -1)],
    'wide': [(1, 1), (1, -1), (1, 2), (1, -2), (2, 1), (2, -1), (1, 3), (1, -3), (3, 1), (3, -1),
             (2, 3), (2, -3), (3, 2), (3, -2), (1, 4), (1, -4), (4, 1), (4, -1)],
}[tname]


def pnorm(v):
    g = 0
    for x in v:
        g = gcd(g, abs(x))
    if g == 0:
        return None
    v = tuple(x // g for x in v)
    for x in v:
        if x != 0:
            if x < 0:
                v = tuple(-y for y in v)
            break
    return v


def snorm(v):  # up to sign only
    if not any(v):
        return None
    for x in v:
        if x != 0:
            if x < 0:
                v = tuple(-y for y in v)
            break
    return v


E = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
Y = [(1, 1, 1, 1), (1, -1, 1, -1), (1, 1, -1, -1), (1, -1, -1, 1)]


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def on_line(p, u, v):
    # all 3x3 minors of the 3x4 matrix vanish
    for drop in range(4):
        idx = [i for i in range(4) if i != drop]
        if det3([u[i] for i in idx], [v[i] for i in idx], [p[i] for i in idx]) != 0:
            return False
    return True


def reach_output(y, pts):
    if mode == 'G':
        for u, v in combinations(pts, 2):
            if on_line(y, u, v):
                return (u, v)
        return None
    for u, v in combinations(pts, 2):
        for s in (1, -1):
            w = tuple(a + s * b for a, b in zip(u, v))
            if mode == 'P':
                if pnorm(w) == y:
                    return (u, v, snorm(w))
            elif snorm(w) == y:
                return (u, v)
    return None


sols = []
seen = set()
nodes = 0


def dfs(pts, hist, remaining, left):
    global nodes
    nodes += 1
    if not remaining:
        sols.append(list(hist))
        return
    if left < len(remaining):
        return
    key = (frozenset(pts), left)
    if key in seen:
        return
    seen.add(key)
    # option 1: build an output now
    for y in remaining:
        if mode == 'P':
            # every differently SCALED copy of the output that one addition can give is tried
            done = set()
            for u, v in combinations(pts, 2):
                for sg in (1, -1):
                    w = tuple(a + sg * b for a, b in zip(u, v))
                    if pnorm(w) == y and snorm(w) not in done:
                        done.add(snorm(w))
                        dfs(pts + [snorm(w)], hist + [('OUT', snorm(w), (u, v))], [z for z in remaining if z != y], left - 1)
            continue
        pr = reach_output(y, pts)
        if pr is not None:
            newpt = y
            dfs(pts + [newpt], hist + [('OUT', y, pr[:2])], [z for z in remaining if z != y], left - 1)
    # option 2: build a helper (a gate that is not an output)
    if left > len(remaining):
        have = set(pts)
        for u, v in combinations(pts, 2):
            for (a, b) in (TS if mode == 'G' else TS_O):
                w = tuple(a * x + b * y for x, y in zip(u, v))
                w = pnorm(w) if mode == 'G' else snorm(w)
                if w is None or w in have or w in remaining:
                    continue
                if mode == 'P' and pnorm(w) in remaining:
                    continue
                dfs(pts + [w], hist + [('aux', w, (u, v))], remaining, left - 1)


TS_O = [(1, 1), (1, -1)]
start = [pnorm(e) for e in E]
targets = [pnorm(y) for y in Y] if mode in ('G', 'P') else [snorm(y) for y in Y]
dfs(start, [], targets, S)
print(f"mode {mode}  gates {S}  tset {tname}: circuits found {len(sols)}  search nodes {nodes}")
# distinct sets of helper points
helpers = {}
for h in sols:
    key = frozenset(w for (k, w, _) in h if k == 'aux')
    helpers.setdefault(key, h)
print("distinct helper sets:", len(helpers))
for key, h in list(helpers.items())[:40]:
    print("  helpers", sorted(key))
    for (k, w, (u, v)) in h:
        print("      ", k, w, "on line", u, v)

if mode == 'G':
    T3 = {pnorm(t) for t in [(-1, 1, 1, 1), (1, -1, 1, 1), (1, 1, -1, 1), (1, 1, 1, -1)]}
    F4 = set(T3) | set(targets) | set(start)
    for i in range(4):
        for j in range(i + 1, 4):
            for sg in (1, -1):
                v = [0, 0, 0, 0]; v[i] = 1; v[j] = sg
                F4.add(pnorm(tuple(v)))
    with_hub = sum(1 for k in helpers if k & T3)
    inside = sum(1 for k in helpers if k <= F4)
    print("helper sets:", len(helpers), " containing a point of the third tetrahedron:", with_hub,
          " lying entirely in the 24-point configuration:", inside)
    from collections import Counter
    print("helper sets WITHOUT third-tetrahedron point (first 10):")
    n = 0
    for k, h in helpers.items():
        if not (k & T3):
            n += 1
            if n <= 10:
                print("   ", sorted(k))
                for (kk, w, (u, v)) in h:
                    print("        ", kk, w, "on line", u, v)
    print("count without:", n)
