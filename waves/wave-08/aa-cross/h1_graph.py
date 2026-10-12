#!/usr/bin/env python3
"""h1_graph.py [aa-cross]  ab-3's two-subspace question as a graph.  Two partitions P1, P2 of the cube's N points.
F(P) = functions constant on the classes of P.  Question: do F(P1) + F(P2) contain every real polynomial of degree <= d,
with few classes in all?  Exact rational rank (Fractions) for the constructions; the k = 4 search uses rank modulo 1000003
as a filter and every hit is re-checked in Fractions."""
import sys, random, time, itertools
from fractions import Fraction
P = 1000003
def rank_mod(rows, p=P):
    M = [list(r) for r in rows]; rk = 0; nc = len(M[0])
    for c in range(nc):
        piv = None
        for i in range(rk, len(M)):
            if M[i][c] % p: piv = i; break
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        inv = pow(M[rk][c], p - 2, p); M[rk] = [v * inv % p for v in M[rk]]
        R = M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] % p:
                f = M[i][c]; M[i] = [(a - f * b) % p for a, b in zip(M[i], R)]
        rk += 1
        if rk == len(M): break
    return rk
def rank_frac(rows):
    M = [[Fraction(v) for v in r] for r in rows]; rk = 0; nc = len(M[0])
    for c in range(nc):
        piv = None
        for i in range(rk, len(M)):
            if M[i][c] != 0: piv = i; break
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        inv = 1 / M[rk][c]; M[rk] = [v * inv for v in M[rk]]; R = M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], R)]
        rk += 1
        if rk == len(M): break
    return rk
def monos(k, d):
    N = 1 << k; out = []
    for j in range(d + 1):
        for S in itertools.combinations(range(k), j):
            m = sum(1 << i for i in S); out.append([1 if (x & m) == m else 0 for x in range(N)])
    return out
def indic(lab):
    cl = sorted(set(lab)); return [[1 if l == c else 0 for l in lab] for c in cl]
def defect(a, b, mon, rk=rank_mod):
    I = indic(a) + indic(b); r0 = rk(I); return rk(I + mon) - r0, len(I), r0
def theta(k):
    N = 1 << k
    a = [x >> 1 for x in range(N)]                       # forget bit 0
    b = [('P', (x >> 1) & 1) if not x & 1 else ('R', x >> 2) for x in range(N)]   # bit0=0: keep bit 1 only; bit0=1: forget bit 1
    return a, b
print("== theta family: P1 forgets bit 0; P2 keeps only bit 1 where bit 0 = 0, and forgets bit 1 where bit 0 = 1")
for k in range(3, 8):
    a, b = theta(k); N = 1 << k
    rk = rank_frac if k <= 6 else rank_mod
    d1 = defect(a, b, monos(k, 1), rk); d2 = defect(a, b, monos(k, 2), rk); d3 = defect(a, b, monos(k, 3), rk)
    print("k=%d N=%3d classes %3d + %3d = %3d (N = %d, 3N/4 + 2 = %d) rank %3d ; missing degree<=1: %d, degree<=2: %d, degree<=3: %d  [%s]" % (
        k, N, len(set(a)), len(set(b)), d2[1], N, 3 * N // 4 + 2, d2[2], d1[0], d2[0], d3[0], "Fractions" if k <= 6 else "mod p"))
print("== control, degree 1: halves of the bits")
for k in (4, 6):
    h = k // 2; N = 1 << k; a = [x >> h for x in range(N)]; b = [x & ((1 << h) - 1) for x in range(N)]
    print("k=%d classes %d: missing degree<=1 %d, degree<=2 %d" % (k, defect(a, b, monos(k, 1), rank_frac)[1], defect(a, b, monos(k, 1), rank_frac)[0], defect(a, b, monos(k, 2), rank_frac)[0]))
def search(k, d, p1, p2, secs, seed):
    rnd = random.Random(seed); N = 1 << k; mon = monos(k, d); t0 = time.time(); best = None; tries = 0; hits = []
    while time.time() - t0 < secs:
        a = [rnd.randrange(p1) for _ in range(N)]; b = [rnd.randrange(p2) for _ in range(N)]
        cur = defect(a, b, mon)[0]; stall = 0
        while cur and stall < 400 and time.time() - t0 < secs:
            which = rnd.random() < 0.5; lab = a if which else b; x = rnd.randrange(N); old = lab[x]
            lab[x] = rnd.randrange(p1 if which else p2)
            if lab[x] == old: continue
            new = defect(a, b, mon)[0]; tries += 1
            if new <= cur:
                stall = 0 if new < cur else stall + 1; cur = new
            else: lab[x] = old; stall += 1
        if best is None or cur < best: best = cur
        if cur == 0:
            ex = defect(a, b, mon, rank_frac)
            if ex[0] == 0: hits.append((ex[1], ex[2], list(a), list(b)))
            if len(hits) >= 3: break
    return best, tries, hits
if len(sys.argv) > 1:
    k = int(sys.argv[1]); d = int(sys.argv[2]); secs = float(sys.argv[3])
    for tot in [int(v) for v in sys.argv[4:]]:
        res = []
        for p1 in range(max(2, tot // 2 - 2), tot // 2 + 1):
            p2 = tot - p1; best, tries, hits = search(k, d, p1, p2, secs / 3, 7 * tot + p1)
            res.append((p1, p2, best, tries, len(hits)))
            for h in hits[:1]: print("   HIT k=%d degree<=%d classes used %d rank %d  P1=%s P2=%s" % (k, d, h[0], h[1], h[2], h[3]))
        print("k=%d degree<=%d total classes <= %d : (p1, p2, least defect reached, evaluations, exact hits) %s" % (k, d, tot, res))
