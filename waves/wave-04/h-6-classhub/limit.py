#!/usr/bin/env python3
"""h-6-classhub / limit.py : what the staircase program for K = [[1,1],[1,tau]] turns into at the three degenerate kernels.
Every wire of the staircase has entries tau^(a_x) with coefficient 1 (checked here: the exponent vectors read at tau = 2 and at
tau = 3 agree; the symbolic run gen_tau.py k sym confirms it for k <= 4).  A wire is a projective point, so its limit is its
leading part.  Five limits:
  inf-up   tau -> infinity, inputs unscaled        : limit of a wire = positions where a_x is largest ; targets -> [x contains w]
  inf-down tau -> infinity, input x scaled tau^-|x| : positions where a_x - |x| is largest             ; targets -> [x inside w]  (subset sums)
  zero-a   tau -> 0, inputs unscaled               : positions where a_x is smallest                  ; targets -> [x disjoint from w]
  zero-b   tau -> 0, input x scaled tau^-|x|        : positions where a_x - |x| is smallest            ; targets -> [x contains complement of w]
  one      tau -> 1                                 : the support                                       ; all targets -> the all-ones row
For each gate w = a*u + b*v:  'alive' = limit(w) is a new point on the line through limit(u) != limit(v);
'free' = limit(w) is a point already held (the gate is not needed);  'dead' = neither: limit(w) is NOT on the line through the
limits of its two inputs (when limit(u) = limit(v) it is the derivative along the degeneration).  A dead gate is repaired with
1 gate if two held points span it, else with 2 gates if one extra helper does, else flagged.
Limit points are 0/1 vectors (sets); for sets T, P, Q: T is on the line through P and Q iff T = P + Q (disjoint) or T = P - Q or Q - P.
usage: limit.py k"""
import sys, math
from fractions import Fraction as F
from gen_tau import build
k = int(sys.argv[1]); N = 1 << k
def expo(prog, vec, base):
    out = {}
    for nm in vec:
        e = []
        for t in vec[nm]:
            if t == 0: e.append(None)
            else:
                t = F(t); a = 0
                while t > 1: t /= base; a += 1
                while t < 1: t *= base; a -= 1
                assert t == 1, 'entry is not a pure power of tau'
                e.append(a)
        out[nm] = tuple(e)
    return out
p2, v2, ok2 = build(k, F(2)); p3, v3, ok3 = build(k, F(3)); assert ok2 and ok3
E2 = expo(p2, v2, 2); E3 = expo(p3, v3, 3); assert E2 == E3 and [g[0] for g in p2] == [g[0] for g in p3]
wt = [bin(x).count('1') for x in range(N)]
def lim(e, mode):
    if mode == 'one': return sum(1 << x for x in range(N) if e[x] is not None)
    s = [(e[x] - (wt[x] if mode in ('inf-down', 'zero-b') else 0)) for x in range(N) if e[x] is not None]
    best = max(s) if mode.startswith('inf') else min(s)
    return sum(1 << x for x in range(N) if e[x] is not None and e[x] - (wt[x] if mode in ('inf-down', 'zero-b') else 0) == best)
def online(T, P, Q): return P != Q and ((P & Q) == 0 and (P | Q) == T or (Q & ~P) == 0 and (P & ~Q) == T or (P & ~Q) == 0 and (Q & ~P) == T)
print('N', N, 'staircase gates', len(p2), '| textbook for the generic kernel', N * k, '| textbook for a kernel with a zero', N * k // 2)
for mode in ('inf-up', 'inf-down', 'zero-a', 'zero-b', 'one'):
    held = set(1 << x for x in range(N)); L = {('x', x): 1 << x for x in range(N)}
    alive = free = dead = rep1 = rep2 = bad = badcost = coin = 0; badlist = []; deadkinds = {}; freekinds = {}; alivekinds = {}; sample = []
    for nm, a, u, b, v in p2:
        T = lim(E2[nm], mode); L[nm] = T; P, Q = L[u], L[v]
        if T in held: free += 1; freekinds[nm[0]] = freekinds.get(nm[0], 0) + 1; continue
        if online(T, P, Q): alive += 1; alivekinds[nm[0]] = alivekinds.get(nm[0], 0) + 1; held.add(T); continue
        dead += 1; deadkinds[nm[0]] = deadkinds.get(nm[0], 0) + 1; coin += (P == Q)
        if len(sample) < 3: sample.append((nm, 'inputs coincide' if P == Q else 'off the line', bin(T).count('1'), bin(P).count('1'), bin(Q).count('1')))
        hl = list(held); fixed = False
        for X in hl:
            if (X & ~T) == 0 and (T & ~X) in held and (T & ~X) != X: fixed = True; break     # T = X + Y
            if (T & ~X) == 0 and (X & ~T) in held: fixed = True; break                       # T = X - Y
        if fixed: rep1 += 1; held.add(T); continue
        for X in hl:                                   # one extra helper Hh = X +- Y, then T = Hh +- Z
            if fixed: break
            for Y in hl:
                if X >= Y: continue
                cands = []
                if X & Y == 0: cands.append(X | Y)
                if (Y & ~X) == 0: cands.append(X & ~Y)
                if (X & ~Y) == 0: cands.append(Y & ~X)
                for Hh in cands:
                    if (Hh & ~T) == 0 and (T & ~Hh) in held: fixed = True; break
                    if (T & ~Hh) == 0 and (Hh & ~T) in held: fixed = True; break
                if fixed: held.add(Hh); break
        if fixed: rep2 += 1; held.add(T)
        else:
            # fewest held sets that partition T (disjoint union); repair cost = pieces - 1 gates.  An upper bound on the repair.
            subs = [h for h in held if (h & ~T) == 0]; memo = {}
            def part(rem):
                if rem == 0: return 0
                if rem in memo: return memo[rem]
                low = rem & -rem; best = 10 ** 9
                for h in subs:
                    if (h & low) and (h & ~rem) == 0: best = min(best, 1 + part(rem & ~h))
                memo[rem] = best; return best
            np_ = part(T); bad += 1; badcost += np_ - 1; badlist.append(np_ - 1); held.add(T)
    total = alive + rep1 + 2 * rep2 + badcost
    print('%-8s alive %4d %s | free %4d %s | dead %4d %s (repaired with 1 gate: %d, with 2 gates: %d, by a partition into held sets: %d costing %s) | LIMIT PROGRAM: %d gates (textbook for this limit: %d) | dead gates whose two inputs have the SAME limit: %d of %d | first dead: %s'
          % (mode, alive, alivekinds, free, freekinds, dead, deadkinds, rep1, rep2, bad, sorted(badlist), total, N - 1 if mode == 'one' else N * k // 2, coin, dead, sample))
