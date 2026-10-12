#!/usr/bin/env python3
"""c2_e16.py (skeptic c-2): the exception count of g-6 section 4 for blocks of 16 and 32 points.

Rule (g-6 section 4, re-derived by c-2): rows = F_2^m, columns = its dual, a binary tree on the rows with a matching
node R <-> column set R' (|R'| = |R|, nested like the tree), X = exceptional columns, G = the other ("good") columns.
At every node R: the good columns outside R' lie in ONE coset of (R - R)^perp.

Part 1: check an explicit tree + matching + X with |X| = 8 at 16 points (so e(16) <= 8).
Part 2: the lower bound e(w) >= min over 3- and 4-point sets, by brute force over all 3- and 4-subsets R and all R', X is
        replaced by the counting bound  |X| >= w - |R| - w/2^rho(R)  (every tree with >= 3 leaves has a node of 3 or 4
        leaves whose children have at most 2 leaves); prints the minimum over shapes for w = 8, 16, 32, 64.
Part 3: the budget table  c * e(w) <= c + w  and  w * e(c) <= c + w  for every shape w x c with 2 <= w, c, N = 16 .. 4096,
        using the proven lower bounds e(2) = e(4) = 0, e(8) = 3, e(16) = 8, e(w) >= 3w/4 - 4 for w >= 32.
"""
import itertools

def par(v):
    return bin(v).count("1") & 1

def rho(R):
    R = sorted(R)
    span = {0}
    dim = 0
    for p in R[1:]:
        d = p ^ R[0]
        if d not in span:
            span |= {s ^ d for s in span}
            dim += 1
    return dim, span

def rule_ok(R, Rp, G, w):
    good = [e for e in G if e not in Rp]
    if len(good) <= 1:
        return True
    _, span = rho(R)
    perp = {e for e in range(w) if all(par(e & d) == 0 for d in span)}
    return all((e ^ good[0]) in perp for e in good)

def check_tree(tree, w, X):
    """tree: nested tuples; a leaf is (row, column). Returns (ok, list of failing nodes)."""
    G = [e for e in range(w) if e not in X]
    fails = []
    def rec(t):
        if isinstance(t[0], int):
            R, Rp = {t[0]}, {t[1]}
        else:
            R1, R1p = rec(t[0]); R2, R2p = rec(t[1])
            R, Rp = R1 | R2, R1p | R2p
        if not rule_ok(R, Rp, G, w):
            fails.append(sorted(R))
        return R, Rp
    R, Rp = rec(tree)
    assert sorted(R) == list(range(w)) and sorted(Rp) == list(range(w)), "not a matching"
    return (not fails), fails

if __name__ == "__main__":
    # ---- Part 1
    w = 16
    X = {1, 3, 5, 7, 9, 11, 13, 15}                      # good columns = the even ones = a coset of d^perp, d = 1
    plane = (((0, 2), (1, 6)), ((2, 10), (3, 14)))       # rows {0,1},{2,3}: two pairs of direction d = 1; columns 2,6,10,14
    six = (plane, ((4, 4), (5, 12)))                     # third pair of direction 1; columns 4,12
    eight = (six, ((6, 0), (7, 8)))                      # fourth pair; columns 0, 8
    t = eight
    for row, col in zip(range(8, 16), [1, 3, 5, 7, 9, 11, 13, 15]):
        t = (t, (row, col))                              # the other eight rows, split off one at a time
    ok, fails = check_tree(t, w, X)
    print(f"[E16] explicit tree at 16 points with |X| = {len(X)} exceptional columns: rule holds at every node: {ok} {fails}")
    # the same tree with one exceptional column fewer must fail (sanity of the checker)
    worst = 0
    for drop in sorted(X):
        ok2, _ = check_tree(t, w, X - {drop})
        worst += ok2
    print(f"[E16] same tree with any one of the 8 exceptional columns made good: still fine in {worst} of 8 cases")
    # ---- Part 2
    for m in (3, 4, 5, 6):
        w = 1 << m
        best = {}
        for r in (3, 4):
            # up to translation, R contains 0
            for rest in itertools.combinations(range(1, w), r - 1):
                R = (0,) + rest
                dim, _ = rho(R)
                need = w - r - (w >> dim)
                key = (r, dim)
                best[key] = need
        print(f"[E-lb] w={w}: exceptions forced by one node of 3 or 4 rows, by (size, dimension): {sorted(best.items())}; "
              f"minimum {min(best.values())}  (= 3w/4 - 4 = {3*w//4 - 4})")
    # ---- Part 3
    def elow(m):
        return {1: 0, 2: 0, 4: 0, 8: 3, 16: 8}.get(m, 3 * m // 4 - 4)
    for k in range(4, 13):
        N = 1 << k
        rows = []
        for a in range(1, k):
            w, c = 1 << a, 1 << (k - a)
            needA, needB, avail = c * elow(w), w * elow(c), c + w
            verdict = "EXCLUDED" if max(needA, needB) > avail else ("tight" if max(needA, needB) == avail else "open")
            rows.append(f"{w}x{c}: need {max(needA, needB)} have {avail} {verdict}")
        print(f"[budget] N={N}: " + "; ".join(rows))
