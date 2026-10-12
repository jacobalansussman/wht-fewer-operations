#!/usr/bin/env python3
"""g-1 sa8.py: search for a circuit below 22 gates at 8 points inside the pool of coset sign vectors (304 wires:
all 240 real stabiliser states = functions of degree <= 2, plus the 64 sign vectors with an odd number of minus signs).
Count (G).  Exact: every wire is an integer vector; a gate is a collinear triple of pool wires (pool.py), so a feasible
state IS a circuit, replayed by construction (the closure only uses exact collinear triples).
State = a set of helper wires.  Energy = (helpers) + 8 + W * (outputs not derivable).  Annealing with add / remove / swap.
usage: sa8.py <seconds> <seed> [start: empty|known] [maxdeg]
Also: exhaustive 'remove 2 helpers, add 1' around the known 22-gate circuits (plans 4+2 and 2+4).
"""
import sys, time, random, math, itertools
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from pool import build_pool, lines
from ref import nz, wht, norm
from ledger import build

def setup(maxdeg):
    pool = build_pool(3, maxdeg); ws, trip = lines(pool)
    n = len(ws); just = [[] for _ in range(n)]
    for (a, b, c) in trip:
        just[a].append((1 << b) | (1 << c)); just[b].append((1 << a) | (1 << c)); just[c].append((1 << a) | (1 << b))
    S = [nz(w) for w in ws]; T = [nz(wht(w)) for w in ws]
    inputs = [i for i in range(n) if S[i] == 1]; outs = [i for i in range(n) if S[i] == 8 and T[i] == 1]
    return ws, just, S, T, inputs, outs

def closure(H, just, inputs, outs):
    """returns (mask of derivable wires among inputs + H + outs, order of derivation)"""
    avail = 0
    for i in inputs: avail |= 1 << i
    todo = [w for w in H] + [o for o in outs if o not in H]; order = []; ch = True
    while ch and todo:
        ch = False; rest = []
        for w in todo:
            if any((avail & m) == m for m in just[w]): avail |= 1 << w; order.append(w); ch = True
            else: rest.append(w)
        todo = rest
    return avail, order

AGREE = {}; LAM = 0.3; TEMP = 0.35
def energy(H, just, inputs, outs, W=0.5):
    """graded: for each output, the largest agreement (positions where a derivable wire equals +-the output) guides the search"""
    avail, order = closure(H, just, inputs, outs)
    missing = sum(1 for o in outs if not avail >> o & 1)
    dead = sum(1 for w in H if not avail >> w & 1)
    live = [w for w in H if avail >> w & 1]
    gap = 0
    for t, o in enumerate(outs):
        if avail >> o & 1: continue
        gap += 8 - max([AGREE[w][t] for w in live] + [1])
    return len(H) + 8 + W * missing + 1.0 * dead + LAM * gap, missing, dead

def known_helpers(ws, plan):
    """the 22-gate circuit written in the frame of the characters, with pair sums inside each brick (so every helper is a pool wire).
    plan (2,1): bricks on the two planes {bit 2 = b}, then butterflies; plan (1,2): the mirror image (butterflies on bit 0 first)."""
    idx = {w: i for i, w in enumerate(ws)}
    def vec(d):
        v = [0] * 8
        for p, c in d.items(): v[p] = c
        return idx[norm(v)]
    H = []
    if plan == (2, 1):
        for b in (0, 4):
            H += [vec({b: 1, b + 1: 1}), vec({b + 2: 1, b + 3: -1}), vec({b: 1, b + 1: 1, b + 2: 1, b + 3: -1})]
            for ch in ((1, 1, 1, 1), (1, -1, 1, -1), (1, 1, -1, -1), (1, -1, -1, 1)): H.append(vec({b + t: ch[t] for t in range(4)}))
    else:
        for q in range(4):                      # butterflies on bit 0: pairs (2q, 2q+1), both characters
            H += [vec({2 * q: 1, 2 * q + 1: 1}), vec({2 * q: 1, 2 * q + 1: -1})]
        for e in (1, -1):                        # bricks over q for each character e of bit 0: pair sums, hub
            f = lambda q: {2 * q: 1, 2 * q + 1: e}
            d1 = dict(f(0)); d1.update(f(1)); d2 = dict(f(2)); d2.update({p: -c for p, c in f(3).items()})
            d3 = dict(d1); d3.update(d2); H += [vec(d1), vec(d2), vec(d3)]
    return H

def main():
    secs, seed = float(sys.argv[1]), int(sys.argv[2]); start = sys.argv[3] if len(sys.argv) > 3 else "empty"
    maxdeg = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    ws, just, S, T, inputs, outs = setup(maxdeg); n = len(ws); rng = random.Random(seed)
    cand = [i for i in range(n) if i not in inputs and i not in outs]
    global LAM
    if len(sys.argv) > 5: LAM = float(sys.argv[5])
    for w in range(n):
        AGREE[w] = [max(sum(1 for x, y in zip(ws[w], ws[o]) if x != 0 and x == y), sum(1 for x, y in zip(ws[w], ws[o]) if x != 0 and x == -y)) for o in outs]
    print("pool: %d wires (degree <= %d), %d candidate helpers, %d outputs" % (n, maxdeg, len(cand), len(outs)), flush=True)
    # 0. the known circuits live in the pool only if their helpers are coset sign vectors: use a balanced sum inside each brick
    kn = []
    for plan in ((2, 1), (1, 2)):
        H = known_helpers(ws, plan); e, miss, dead = energy(H, just, inputs, outs)
        print("known circuit, plan %s: %d helpers, all pool wires; gates = %d, outputs missing %d, helpers not derivable %d" % (plan, len(H), len(H) + 8, miss, dead), flush=True); kn.append(H)
    # balanced versions: found by the search itself from 'empty' (calibration), or by greedy repair here
    def anneal(H0, tmax, temp0=TEMP):
        H = list(H0); E, miss, dead = energy(H, just, inputs, outs); best = (10 ** 9, None); t0 = time.time(); it = 0; hist = {}
        while time.time() - t0 < tmax:
            it += 1; temp = temp0 * (1 - 0.7 * ((time.time() - t0) / tmax))
            H2 = list(H); m = rng.random()
            if m < 0.35 or not H2:
                avail, _ = closure(H2, just, inputs, outs)
                # add a wire that is one gate away from what is held (frontier), else any wire
                w = rng.choice(cand)
                for _ in range(6):
                    if w not in H2 and any((avail & mm) == mm for mm in just[w]): break
                    w = rng.choice(cand)
                if w in H2: continue
                H2.append(w)
            elif m < 0.7:
                H2.pop(rng.randrange(len(H2)))
            else:
                H2.pop(rng.randrange(len(H2))); w = rng.choice(cand)
                if w in H2: continue
                H2.append(w)
            E2, miss2, dead2 = energy(H2, just, inputs, outs)
            if E2 <= E or rng.random() < math.exp(-(E2 - E) / temp):
                H, E, miss, dead = H2, E2, miss2, dead2
                if miss == 0 and dead == 0:
                    g = len(H) + 8; hist[g] = hist.get(g, 0) + 1
                    if g < best[0]: best = (g, list(H)); print("   seed %d t=%.0fs: circuit with %d gates" % (seed, time.time() - t0, g), flush=True)
        return best, it, hist
    if start == "known": H0 = kn[seed % 2]
    else: H0 = []
    best = (10 ** 9, None); it = 0; hist = {}; t00 = time.time(); rounds = 0
    while time.time() - t00 < secs:                      # restarts of 60 s each
        b2, it2, h2 = anneal(H0, min(60.0, secs - (time.time() - t00))); it += it2; rounds += 1
        for g, c in h2.items(): hist[g] = hist.get(g, 0) + c
        if b2[0] < best[0]: best = b2
    print("restarts: %d" % rounds)
    print("seed %d start %s: %d moves; best circuit %s gates; feasible states visited by gate count: %s" % (seed, start, it, best[0], sorted(hist.items())))
    if best[1]:
        H = best[1]; avail, order = closure(H, just, inputs, outs)
        print("   wires of the best circuit in order of derivation (s, s', vector):")
        for w in order: print("      %s (%d,%d) %s" % ("OUT " if w in outs else "help", S[w], T[w], list(ws[w])))
        # exhaustive exchange around it: remove 2 helpers, add 1; remove 1, add 0
        better = 0; tested = 0
        for r in (1, 2):
            for rem in itertools.combinations(range(len(H)), r):
                base = [h for i, h in enumerate(H) if i not in rem]
                for add in ([None] if r == 1 else cand):
                    if add is not None and add in base: continue
                    H2 = base + ([add] if add is not None else []); tested += 1
                    e, miss, dead = energy(H2, just, inputs, outs)
                    if miss == 0 and dead == 0: better += 1
        print("   exhaustive exchange around it (remove 1; remove 2 and add any 1 of %d): %d states tested, %d circuits with %d gates" % (len(cand), tested, better, best[0] - 1))

if __name__ == "__main__":
    main()
