#!/usr/bin/env python3
"""thmcheck.py -- ab-3.  Machine check of the level-set-flats theorem in its first non-trivial instances.
k = 5: the weight is constant on no flat of dimension above 2, so the theorem says: the weight is not a function of
fewer than 3 flat indicators.  Exhaustive over ALL pairs of flats (any dimensions, covering or not): is the weight
constant on each of the four cells (in both, first only, second only, neither)?  Expect: no pair.
Also k = 4: quadric sign (weight mod 4 in {0,1}) and weight, all single flats (expect none), and all pairs for the
quadric sign at k = 4 (theorem: at least 2; pairs may exist -- count them)."""
import sys
def pop(x): return bin(x).count("1")
def subspaces(k):
    seen = {frozenset([0])}; frontier = [frozenset([0])]
    while frontier:
        nxt = []
        for S in frontier:
            for v in range(1, 1 << k):
                if v in S: continue
                T = frozenset(S | {s ^ v for s in S})
                if T not in seen: seen.add(T); nxt.append(T)
        frontier = nxt
    return seen
def flats(k):
    out = set()
    for S in subspaces(k):
        if len(S) == 1 << k: continue          # the whole space: a constant, not an atom
        for c in range(1 << k):
            out.add(sum(1 << (c ^ s) for s in S))
    return sorted(out)
def run(k, name, classes):
    N = 1 << k; full = (1 << N) - 1; F = flats(k)
    def const(cell): return cell == 0 or any(cell & ~c == 0 for c in classes)
    singles = sum(1 for a in F if const(a) and const(full & ~a))
    pairs = 0
    for i, a in enumerate(F):
        na = full & ~a
        for b in F[i + 1:]:
            nb = full & ~b
            if const(a & b) and const(a & nb) and const(na & b) and const(na & nb): pairs += 1
    print(f"k={k} {name}: {len(F)} flats; single flats that determine it: {singles}; pairs of flats that determine it: {pairs}", flush=True)
for k in (4, 5):
    N = 1 << k
    wclasses = [sum(1 << y for y in range(N) if pop(y) == w) for w in range(k + 1)]
    qclasses = [sum(1 << y for y in range(N) if (pop(y) % 4 in (0, 1)) == t) for t in (True, False)]
    run(k, "weight (neighbour sums' spectrum)", wclasses)
    run(k, "quadric sign, weight mod 4 in {0,1} (the transform's spectrum)", qclasses)
