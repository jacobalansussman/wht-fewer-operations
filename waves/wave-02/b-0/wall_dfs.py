#!/usr/bin/env python3
"""b-0: exact search, pure Python, no solver.  Same class as wall_ilp.py (8 points; characters on the aligned blocks of one
chain, and hubs = character on the left half +- a different character on the right half).  Is there a program with at most CAP
gates all of whose points lie in the class?  Backward search: every computed point gets one derivation (u, v); the set of
computed points may not exceed CAP; no point may depend on itself.  Exhaustive, so 'none' is a proof for this class.
usage: wall_dfs.py CAP"""
import sys, itertools, time
from fractions import Fraction as F
CAP = int(sys.argv[1]); N = 8
def canon(v):
    for t in v:
        if t: return tuple(v) if t > 0 else tuple(-s for s in v)
def ch(w, m): return [(-1) ** bin(w & x).count('1') for x in range(m)]
def emb(lo, vals):
    v = [0] * N
    for i, t in enumerate(vals): v[lo + i] = t
    return v
inputs = [canon(emb(i, [1])) for i in range(N)]
pieces = {}; hubs = set()
for m in (2, 4, 8):
    for lo in range(0, N, m):
        for w in range(m): pieces[canon(emb(lo, ch(w, m)))] = m
        h = m // 2
        for a in range(h):
            for b in range(h):
                if a != b:
                    for c in (1, -1): hubs.add(canon(emb(lo, ch(a, h) + [c * t for t in ch(b, h)])))
outputs = [p for p, m in pieces.items() if m == N]
helpers = [p for p, m in pieces.items() if m < N] + sorted(hubs - set(pieces))
pts = inputs + helpers + outputs; idx = {p: i for i, p in enumerate(pts)}; nI = N
def dep(u, v, p):
    for i in range(N):
        for j in range(i + 1, N):
            det = u[i] * v[j] - u[j] * v[i]
            if det:
                a = F(p[i] * v[j] - p[j] * v[i], det); b = F(u[i] * p[j] - u[j] * p[i], det)
                return a != 0 and b != 0 and all(a * u[t] + b * v[t] == p[t] for t in range(N))
    return False
ders = {i: [] for i in range(nI, len(pts))}
for p in helpers + outputs:
    for u, v in itertools.combinations([q for q in pts if q != p], 2):
        if dep(u, v, p): ders[idx[p]].append((idx[u], idx[v]))
nd = sum(len(d) for d in ders.values()); print('points', len(pts), 'derivations', nd, 'cap', CAP, flush=True)
outs = [idx[o] for o in outputs]
choice = {}; nodes = [0]; found = []; t0 = time.time()
def reaches(src, target):         # does src depend on target through the derivations chosen so far?
    stack = [src]; seen = set()
    while stack:
        q = stack.pop()
        if q == target: return True
        if q in seen or q < nI: continue
        seen.add(q)
        if q in choice: stack.extend(choice[q])
    return False
def dfs(C, pending):
    nodes[0] += 1
    if found: return
    if not pending:
        found.append(dict(choice)); return
    # most constrained pending point first
    best = None; bl = None
    for p in pending:
        opts = [(u, v) for (u, v) in ders[p] if len(C | {w for w in (u, v) if w >= nI}) <= CAP and not reaches(u, p) and not reaches(v, p)]
        if best is None or len(opts) < len(bl): best, bl = p, opts
        if not opts: return
    p = best; rest = [q for q in pending if q != p]
    bl.sort(key=lambda d: sum(1 for w in d if w >= nI and w not in C))
    for (u, v) in bl:
        new = [w for w in (u, v) if w >= nI and w not in C]
        choice[p] = (u, v)
        dfs(C | set(new), rest + new)
        del choice[p]
        if found: return
dfs(frozenset(outs), list(outs))
print('search nodes', nodes[0], 'seconds %.1f' % (time.time() - t0))
if found:
    ch_ = found[0]; print('FOUND a program in the class with', len(ch_), 'gates:')
    for p, (u, v) in ch_.items(): print('  ', pts[p], '<-', pts[u], ',', pts[v])
else: print('NONE: no program with at most', CAP, 'gates has all its points in the class (exhaustive)')
