#!/usr/bin/env python3
"""g-7-thirdturn / inplace4.py -- 4 points, count (G), programs that use NO extra wire:
every gate is  x_i <- a*x_i + b*x_j  on the four wires (scalings and relabellings free).
Question: least number of such gates for the 4-point transform, modulo a small prime p (meet in the middle).
A palindrome  B^-1 (relabel) B  with B in place is such a program; the 7-gate brick is not (it keeps a fifth value).
Modulo p only: 'none modulo p' is not 'none'; a hit modulo p is a candidate.
usage: inplace4.py p maxdepth
"""
import sys, itertools
p = int(sys.argv[1]); D = int(sys.argv[2]); n = 4
inv = {a: pow(a, p - 2, p) for a in range(1, p)}
def canon(rows):
    out = []
    for r in rows:
        f = next(x for x in r if x); iv = inv[f]; out.append(tuple(x * iv % p for x in r))
    return tuple(sorted(out))
def moves(st):
    res = set()
    for i in range(n):
        for k in range(n):
            if i == k: continue
            for c in range(1, p):
                r = tuple((a + c * b) % p for a, b in zip(st[i], st[k]))
                if not any(r): continue
                res.add(canon(st[:i] + (r,) + st[i + 1:]))
    return res
I = canon(tuple(tuple(int(a == b) for b in range(n)) for a in range(n)))
S = [[1, 1, 1, 1], [1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]]
targets = set()
for perm in itertools.permutations(range(n)):
    for d in itertools.product(range(1, p), repeat=n):
        targets.add(canon(tuple(tuple(S[i][perm[k]] * d[k] % p for k in range(n)) for i in range(n))))
fw = [{I}]; seenF = {I}
bw = [set(targets)]; seenB = set(targets)
found = None
for depth in range(1, D + 1):
    # grow the smaller frontier side alternately: forward up to ceil, backward the rest
    if len(fw) - 1 <= len(bw) - 1:
        nx = set()
        for s in fw[-1]: nx |= moves(s)
        nx -= seenF; seenF |= nx; fw.append(nx)
    else:
        nx = set()
        for s in bw[-1]: nx |= moves(s)
        nx -= seenB; seenB |= nx; bw.append(nx)
    hit = seenF & seenB
    print("p=%d total gates %d: forward depth %d (%d states), backward depth %d (%d states), meet: %s" % (
        p, depth, len(fw) - 1, len(seenF), len(bw) - 1, len(seenB), bool(hit)), flush=True)
    if hit:
        found = depth; break
print("RESULT p=%d: least number of in-place gates for the 4-point transform modulo %d = %s" % (p, p, found if found else "more than %d" % D))
