#!/usr/bin/env python3
# j-cross / prod4.py : programs whose every value is a product vector (a 2-vector on each address bit, any entries).
# A value is a point of (projective line)^k; a gate joins two points that differ in ONE coordinate and gives any third point
# on that axis-parallel line.  Inputs: {0, inf}^k.  Outputs: {1, -1}^k.  Least number of added points?
# Coordinates are only labels (equal / unequal), so with enough labels the answer is the answer over the rationals:
# a solution with g added points uses at most g - N helper points, so 4 + (g - N) labels per axis suffice.
import itertools, sys
def run(k, L, budget):
    labs = list(range(L))            # 0 = '0', 1 = 'inf', 2 = '+1', 3 = '-1', others free
    pts = list(itertools.product(labs, repeat=k))
    inputs = set(itertools.product((0, 1), repeat=k)); outs = set(itertools.product((2, 3), repeat=k))
    cand = [p for p in pts if p not in inputs and p not in outs]
    def buildable(T):
        have = set(inputs); todo = set(T)
        while todo:
            for p in list(todo):
                ok = False
                for i in range(k):
                    c = sum(1 for q in have if q != p and all(q[j] == p[j] for j in range(k) if j != i))
                    if c >= 2: ok = True; break
                if ok: have.add(p); todo.discard(p); break
            else: return False
        return True
    for g in range(len(outs), budget + 1):
        h = g - len(outs); n = 0; hit = None
        for H in itertools.combinations(cand, h):
            n += 1
            if buildable(outs | set(H)): hit = H; break
        print('k=%d labels=%d gates=%d: %s (%d helper sets tried)' % (k, L, g, 'REACHED with helpers %s' % (hit,) if hit else 'impossible', n), flush=True)
        if hit: return g
    return None
run(2, 8, 8)      # 4 points: 8 labels are enough for every program with at most 8 gates
run(3, 4, 15)     # 8 points, labels 0, inf, +1, -1 only (coset-character-like), small budgets only: a sanity run, not the bound
