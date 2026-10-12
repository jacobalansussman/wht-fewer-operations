#!/usr/bin/env python3
"""e2-0-pieces: walk through the 8-point programs of a pool, count (G) (gate = any a*u+b*v, scalings free; a program is a
set of points in which every non-input lies on a line through two points derived earlier).
Start from the known 22 (11 + 11).  Moves: drop one helper (if still valid), swap one helper for a pool point (plateau),
drop two helpers and add one (improvement).  Pool: 'stab' (240 real stabiliser states) or 'pm1' (all vectors with entries 0,+-1).
For vectors with entries in {0,+-1} the only third points on a line through u, v are u+-v, u+-2v, 2u+-v (derived in the report).
usage: walk.py pool seconds seed"""
import sys, time, random, itertools, json
from pool import norm, Y, E, N, stab_pool
pool_name, secs, seed = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed)
RAT = [(1, 1), (1, -1), (1, 2), (1, -2), (2, 1), (2, -1)]
STAB = stab_pool() | set(E) | {norm(y) for y in Y}
if pool_name == 'stab':
    inpool = lambda p: p in STAB
else:
    inpool = lambda p: all(-1 <= a <= 1 for a in p)
OUT = [norm(y) for y in Y]; OUTS = set(OUT); INS = set(E)
def third(u, v):
    for a, b in RAT:
        w = norm(tuple(a * x + b * y for x, y in zip(u, v)))
        if w is not None: yield w
def closure(points):
    """derivable subset of points, starting from the inputs"""
    D = set(INS); pend = [p for p in points if p not in D]; ch = True
    while ch and pend:
        ch = False; rest = []
        for p in pend:
            ok = False
            for q in D:
                for r in third(p, q):
                    if r in D and r != q and r != p: ok = True; break
                if ok: break
            if ok: D.add(p); ch = True
            else: rest.append(p)
        pend = rest
    return D, pend
def valid(helpers):
    D, pend = closure(list(helpers) + OUT)
    return all(o in D for o in OUT), D
def extend(D, pend, c):
    """add c (assumed derivable) and continue the closure on pend; return new D, pend"""
    D = set(D); D.add(c); new = [c]; pend = list(pend)
    while new and pend:
        nxt = []; rest = []
        for p in pend:
            ok = False
            for n in new:
                for r in third(p, n):
                    if r in D and r != n and r != p: ok = True; break
                if ok: break
            if ok: nxt.append(p)
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
def start22():
    s = [tuple(int(x in (2 * i, 2 * i + 1)) for x in range(N)) for i in range(4)]
    d = [tuple((x == 2 * i) - (x == 2 * i + 1) for x in range(N)) for i in range(4)]
    def half(p):
        u = tuple(a - b for a, b in zip(p[0], p[1])); v = tuple(a + b for a, b in zip(p[2], p[3]))
        r = tuple(a - b for a, b in zip(u, v))
        return [norm(u), norm(v), norm(r)]
    return set(s + d + half(s) + half(d))
def shape(p):
    supp = [x for x in range(N) if p[x]]
    near = sum(1 for o in OUT if any(True for q in [1] ) and min(sum(1 for x in range(N) if p[x] != s * o[x]) for s in (1, -1)) <= 2)
    return len(supp)
def one_gate_outputs(p, D):
    """how many outputs lie on a line through p and another held point"""
    k = 0
    for o in OUT:
        if o == p: continue
        if any(r in D and r != p and r != o for r in third(o, p)): k += 1
    return k
def describe(H, tag):
    ok, D = valid(H)
    print(tag, 'gates', len(H) + 8, 'valid', ok)
    for h in sorted(H, key=lambda p: (sum(map(abs, p)), p)):
        print('   helper', h, 'support', sum(1 for a in h if a), 'outputs one gate away', one_gate_outputs(h, D))
    sys.stdout.flush()
H = start22() if len(sys.argv) < 5 else set(tuple(p) for p in json.load(open(sys.argv[4])))
ok, D = valid(H); assert ok, 'start invalid'
describe(H, 'START')
t0 = time.time(); seen = {frozenset(H)}; best = len(H); step = 0; sigs = {}
def signature(H):
    return tuple(sorted(sum(1 for a in h if a) for h in H))
while time.time() - t0 < secs:
    step += 1
    Hl = sorted(H)
    # A: redundancy
    for h in Hl:
        ok, _ = valid(H - {h})
        if ok:
            H = H - {h}; print('DROP ->', len(H) + 8, flush=True); break
    else:
        # C: remove two, add one
        improved = False
        for h1, h2 in itertools.combinations(Hl, 2):
            rest = H - {h1, h2}
            D, pend = closure(list(rest) + OUT)
            if all(o in D for o in OUT):
                H = set(p for p in rest if p in D); improved = True; break
            for c in candidates(D):
                D2, pend2 = extend(D, pend, c)
                if all(o in D2 for o in OUT):
                    H = set(p for p in rest if p in D2) | {c}; improved = True; break
            if improved: break
            if time.time() - t0 > secs: break
        if improved:
            print('IMPROVED ->', len(H) + 8, flush=True); describe(H, 'IMPROVED'); seen.add(frozenset(H)); continue
        # B: swap (plateau)
        nbrs = []
        order = Hl[:]; rng.shuffle(order)
        for h in order[:6]:
            rest = H - {h}
            D, pend = closure(list(rest) + OUT)
            for c in candidates(D):
                if c == h: continue
                D2, pend2 = extend(D, pend, c)
                if all(o in D2 for o in OUT) and all(p in D2 for p in rest):
                    nb = frozenset(rest | {c})
                    if nb not in seen: nbrs.append(nb)
        if not nbrs:
            print('no unseen neighbour at step', step, flush=True); break
        H = set(rng.choice(nbrs)); seen.add(frozenset(H))
        sg = signature(H); sigs[sg] = sigs.get(sg, 0) + 1
        print('step', step, 'gates', len(H) + 8, 'neighbours', len(nbrs), 'support multiset', sg, 'time', round(time.time() - t0), flush=True)
    if len(H) < best: best = len(H); describe(H, 'BEST')
describe(H, 'END')
print('visited', len(seen), 'best gates', best + 8, 'support signatures', sigs)
