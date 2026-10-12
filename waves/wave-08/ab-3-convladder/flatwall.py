#!/usr/bin/env python3
"""flatwall.py -- ab-3.  Exhaustive check at k = 4 (16 points) of the two facts the 'flat calculus' lemma uses:
(a) the largest flat (coset of a subspace of the address space) on which the weight is constant has dimension k/2;
(b) the largest flat on which the quadric sign (-1)^(choose(weight,2)) -- H's own q, and its spectrum up to sign -- is
    constant has dimension k/2.   Also k = 6 for both (all subspaces by their reduced bases)."""
import sys, itertools
def pop(x): return bin(x).count("1")
def subspaces(k):
    """all subspaces of F_2^k as frozensets of vectors, by closure search"""
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
for k in (2, 3, 4, 5):
    subs = subspaces(k); best_w = 0; best_q = 0; cnt = {}
    for S in subs:
        d = len(S).bit_length() - 1; cnt[d] = cnt.get(d, 0) + 1
        reps = set()
        for c in range(1 << k):
            m = min(c ^ s for s in S)
            if m in reps: continue
            reps.add(m)
            if d > best_w and len({pop(c ^ s) for s in S}) == 1: best_w = d
            if d > best_q and len({(pop(c ^ s) * (pop(c ^ s) - 1) // 2) & 1 for s in S}) == 1: best_q = d
    print(f"k={k}: subspaces by dimension {dict(sorted(cnt.items()))}; largest flat with constant weight: dimension {best_w};"
          f" largest flat with constant quadric sign (weight mod 4 in {{0,1}} or in {{2,3}}): dimension {best_q}; k/2 = {k/2}")
