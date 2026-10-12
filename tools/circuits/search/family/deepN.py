#!/usr/bin/env python3
"""e2-0-pieces: local optimality of a program at N points, count (G).  Remove every set of k helpers, try to restore all
outputs by adding at most k-1 points with entries in {0,+-1} (each on a line through two derivable points; for such vectors the
third points of a line through u, v are u+-v, u+-2v, 2u+-v).  usage: deepN.py N slp_N.txt nproc k"""
import sys, itertools, time
from math import gcd
from multiprocessing import Pool
N = int(sys.argv[1]); nproc = int(sys.argv[3]); k = int(sys.argv[4])
def norm(v):
    g = 0
    for a in v: g = gcd(g, abs(a))
    if g == 0: return None
    v = tuple(a // g for a in v)
    for a in v:
        if a: return v if a > 0 else tuple(-b for b in v)
H0 = []
for l in open(sys.argv[2]):
    if l.startswith('#'): continue
    nm = l.split('=')[0].strip()
    if not nm.startswith('y'): H0.append(norm(tuple(int(t) for t in l.split('#')[1].split())))
OUT = [norm(tuple(-1 if bin(w & x).count('1') & 1 else 1 for x in range(N))) for w in range(N)]
INS = set(tuple(int(i == x) for i in range(N)) for x in range(N))
RAT = [(1, 1), (1, -1), (1, 2), (1, -2), (2, 1), (2, -1)]
inpool = lambda p: all(-1 <= a <= 1 for a in p)
def third(u, v):
    for a, b in RAT:
        w = norm(tuple(a * x + b * y for x, y in zip(u, v)))
        if w is not None: yield w
def closure(points):
    D = set(INS); pend = [p for p in points if p not in D]; ch = True
    while ch and pend:
        ch = False; rest = []
        for p in pend:
            if any(r in D and r != q and r != p for q in D for r in third(p, q)): D.add(p); ch = True
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
def candidates(D):
    C = set(); Dl = list(D)
    for i, q in enumerate(Dl):
        for r in Dl[i + 1:]:
            for w in third(q, r):
                if w not in D and inpool(w): C.add(w)
    return C
def work(rem):
    rest = [h for h in H0 if h not in rem]
    D, pend = closure(rest + OUT)
    if all(o in D for o in OUT): return ('drop', rem, 0)
    C1 = candidates(D)
    for c1 in C1:
        D1, p1 = extend(D, pend, c1)
        if all(o in D1 for o in OUT): return ('add1', rem, c1)
    return ('none', rem, len(C1))
if __name__ == '__main__':
    t0 = time.time(); ok, _ = closure(H0 + OUT); assert all(o in ok for o in OUT)
    jobs = list(itertools.combinations(H0, k)); found = 0; tried = 0
    with Pool(nproc) as pl:
        for res in pl.imap_unordered(work, jobs, chunksize=4):
            if res[0] != 'none': found += 1; print('FOUND', res, flush=True)
            else: tried += res[2]
            if time.time() - t0 > 520: print('TIME LIMIT, partial'); break
    print('N', N, 'helpers', len(H0), 'removed sets of', k, ':', len(jobs), 'single additions tried', tried, 'shorter programs found:', found, 'time', round(time.time() - t0))
