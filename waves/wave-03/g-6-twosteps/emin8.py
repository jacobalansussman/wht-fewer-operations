#!/usr/bin/env python3
"""emin8.py: machine check of the counting step of g-6.md section 4 for blocks of 8 points.

Setting (after the block law): rows omega in W = F_2^3, columns eta in the dual, a binary tree on the rows, a matching m of
rows to columns (node R of rows <-> set R' = m(R) of columns), and a set X of "exceptional" columns.
Rule for every node R:  the columns outside R' and outside X ("good columns") must have characters that are pairwise
proportional on R, i.e. they lie in ONE coset of the subgroup perpendicular to R - R.
Question: the least |X| for which some tree and some matching satisfy the rule at every node.
Method: feasible(R, R') = rule(R, R') and (R is a leaf, or some split R = R1 + R2, R' = R1' + R2' with |R1| = |R1'| has both
halves feasible).  Exact, exhaustive over all trees and matchings (memoised over the 12,870 pairs of equal-size subsets).
"""
import sys, itertools
from functools import lru_cache

K = 3
N = 1 << K
FULL = (1 << N) - 1
POP = [bin(v).count("1") for v in range(1 << N)]
DOT = [[bin(a & b).count("1") & 1 for b in range(N)] for a in range(N)]

def perp_mask(R):
    pts = [x for x in range(N) if (R >> x) & 1]
    diffs = [p ^ pts[0] for p in pts]
    m = 0
    for eta in range(N):
        if all(DOT[eta][d] == 0 for d in diffs):
            m |= 1 << eta
    return m

PERP = [perp_mask(R) if R else FULL for R in range(1 << N)]

def run(X):
    def rule(R, Rp):
        G = FULL & ~Rp & ~X
        if G == 0:
            return True
        g0 = (G & -G).bit_length() - 1
        pm = PERP[R]
        for eta in range(N):
            if (G >> eta) & 1 and not (pm >> (eta ^ g0)) & 1:
                return False
        return True

    @lru_cache(maxsize=None)
    def feasible(R, Rp):
        if not rule(R, Rp):
            return None
        if POP[R] == 1:
            return (R, Rp)
        low = R & -R
        rest = R ^ low
        sub = rest
        while True:                                   # R1 = low + sub, sub runs over submasks of rest, R1 != R
            R1 = low | sub
            if R1 != R:
                n1 = POP[R1]
                s2 = Rp
                while s2:                             # R1' over submasks of R' with the same size
                    if POP[s2] == n1:
                        a = feasible(R1, s2)
                        if a is not None:
                            b = feasible(R ^ R1, Rp ^ s2)
                            if b is not None:
                                return (R, Rp, a, b)
                    s2 = (s2 - 1) & Rp
            if sub == 0:
                break
            sub = (sub - 1) & rest
        return None

    return feasible(FULL, FULL)

def show(t):
    if len(t) == 2:
        r = t[0].bit_length() - 1
        c = t[1].bit_length() - 1
        return f"{r}>{c}"
    return "(" + show(t[2]) + " " + show(t[3]) + ")"

if __name__ == "__main__":
    for e in range(0, 4):
        sets = list(itertools.combinations(range(N), e))
        found = None
        tried = 0
        for Xs in sets:
            X = sum(1 << v for v in Xs)
            tried += 1
            t = run(X)
            if t is not None:
                found = (Xs, t)
                break
        if found:
            print(f"|X| = {e}: FEASIBLE, e.g. exceptional columns {found[0]}, tree with matching row>column: {show(found[1])}", flush=True)
        else:
            print(f"|X| = {e}: no tree and no matching, all {tried} exceptional sets tried", flush=True)
