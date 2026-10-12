#!/usr/bin/env python3
"""e2-0-pieces: is the 20-gate 8-point program locally optimal?  count (G).
Remove every set of 3 helpers from the program, then try to restore all 8 outputs by adding at most 2 pool points
(each new point must lie on a line through two derivable points).  Success = a program with at most 19 gates.
Pool: 'stab' (240 real stabiliser states) or 'pm1' (all 0,+-1 vectors).  usage: deep.py pool program.json nproc"""
import sys, json, itertools, time
from multiprocessing import Pool
from pool import norm, Y, E, N, stab_pool
pool_name = sys.argv[1]; H0 = [tuple(p) for p in json.load(open(sys.argv[2]))]; nproc = int(sys.argv[3])
RAT = [(1, 1), (1, -1), (1, 2), (1, -2), (2, 1), (2, -1)]
STAB = stab_pool() | set(E) | {norm(y) for y in Y}
inpool = (lambda p: p in STAB) if pool_name == 'stab' else (lambda p: all(-1 <= a <= 1 for a in p))
OUT = [norm(y) for y in Y]; INS = set(E)
def third(u, v):
    for a, b in RAT:
        w = norm(tuple(a * x + b * y for x, y in zip(u, v)))
        if w is not None: yield w
def closure(points):
    D = set(INS); pend = [p for p in points if p not in D]; ch = True
    while ch and pend:
        ch = False; rest = []
        for p in pend:
            ok = any(r in D and r != q and r != p for q in D for r in third(p, q))
            if ok: D.add(p); ch = True
            else: rest.append(p)
        pend = rest
    return D, pend
def extend(D, pend, c):
    D = set(D); D.add(c); new = [c]; pend = list(pend)
    while new and pend:
        nxt = []; rest = []
        for p in pend:
            if any(r in D and r != n and r != p for n in new for r in third(p, n)): nxt.append(p)
            else: rest.append(p)
        for p in nxt: D.add(p)
        new = nxt; pend = rest
    return D, pend
def candidates(D, onlywith=None):
    C = set(); Dl = list(D)
    if onlywith is not None:
        for r in Dl:
            if r == onlywith: continue
            for w in third(onlywith, r):
                if w not in D and inpool(w): C.add(w)
        return C
    for i, q in enumerate(Dl):
        for r in Dl[i + 1:]:
            for w in third(q, r):
                if w not in D and inpool(w): C.add(w)
    return C
def work(rem):
    rest = [h for h in H0 if h not in rem]
    D, pend = closure(rest + OUT)
    if all(o in D for o in OUT): return ('drop', rem, [])
    C1 = candidates(D); n = 0
    for c1 in C1:
        D1, p1 = extend(D, pend, c1)
        if all(o in D1 for o in OUT): return ('add1', rem, [c1])
        C2 = (C1 - {c1}) | candidates(D1, c1) | set().union(*[candidates(D1, x) for x in D1 - D - {c1}]) if True else C1
        for c2 in C2:
            if c2 in D1: continue
            n += 1
            D2, p2 = extend(D1, p1, c2)
            if all(o in D2 for o in OUT): return ('add2', rem, [c1, c2])
    return ('none', rem, n)
if __name__ == '__main__':
    t0 = time.time(); k = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    jobs = list(itertools.combinations(H0, k)); found = 0; tried = 0
    with Pool(nproc) as pl:
        for res in pl.imap_unordered(work, jobs):
            if res[0] != 'none':
                found += 1; print('FOUND', res, flush=True)
            else: tried += res[2]
    print('pool', pool_name, 'removed sets of', k, ':', len(jobs), 'pairs of additions tried', tried, 'programs with <= %d gates found:' % (len(H0) + 8 - 1), found, 'time', round(time.time() - t0))
