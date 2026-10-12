#!/usr/bin/env python3
"""cells8.py (p-3-hatch32): the exception count for a block of 8 points, WITHOUT hypothesis (G), and with the pinned coset.

Setting (p-3.md section 2).  One block of the first step: 8 rows omega in F_2^3, 8 "cells" eta in the dual F_2^3
(cell eta = the meeting of this block with block eta of the second step), 8 middle wires, each lying in one cell
(hypothesis (G) = every cell holds exactly one wire; here any distribution is allowed).
A cell is EXCEPTIONAL if u ~ chi_eta (at most one such cell, called e; then u is that character) or q_eta ~ chi_xi
("f-cell"; over the whole word there is at most one f-cell per eta, so at most w = 8 in all).
A non-exceptional cell holds at least one wire, and chi_eta lies in the span of its wires' columns modulo u.
Rule at a node R (rows) with wire set R': every non-exceptional cell with NO wire in R' has chi_eta|R proportional to
one common vector; in mode "strong" (u = chi_e, which never vanishes) that vector is chi_e|R, so those cells lie in the
coset e + (R-R)^perp; in mode "weak" (u not a character, or the block does not talk to the outside) they lie in one
coset, any coset.  Weak is a relaxation of the truth, strong is exact for u = chi_e.
Question: for which exceptional sets is there a distribution of wires, a tree and a matching obeying the rule at every node?
Exhaustive over distributions (multisets), trees and matchings (memoised over pairs of equal-size subsets).
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

def run(cell_of, X, e):
    """cell_of[wire] = cell; X = bitmask of exceptional cells; e = the cell with u ~ chi_e, or None (weak mode)."""
    touched = [0] * (1 << N)
    for m in range(1, 1 << N):
        low = (m & -m).bit_length() - 1
        touched[m] = touched[m & (m - 1)] | (1 << cell_of[low])
    nonexc = FULL & ~X
    assert nonexc & ~touched[FULL] == 0, "a non-exceptional cell is empty"

    def rule(R, Rp):
        if POP[R] == 1:
            return True
        G = nonexc & ~touched[Rp]
        if G == 0:
            return True
        pm = PERP[R]
        g0 = e if e is not None else (G & -G).bit_length() - 1
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
        while True:
            R1 = low | sub
            if R1 != R:
                n1 = POP[R1]
                s2 = Rp
                while s2:
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

def show(t, cell_of):
    if len(t) == 2:
        r = t[0].bit_length() - 1
        c = t[1].bit_length() - 1
        return f"{r}>w{c}(cell {cell_of[c]})"
    return "(" + show(t[2], cell_of) + " " + show(t[3], cell_of) + ")"

def distributions(X, grid_only):
    """all multisets of 8 wires over 8 cells in which every non-exceptional cell is non-empty"""
    if grid_only:
        yield list(range(N))
        return
    need = [c for c in range(N) if not (X >> c) & 1]
    extra = N - len(need)
    for add in itertools.combinations_with_replacement(range(N), extra):
        yield sorted(need + list(add))

def case(name, Xcells, e, grid_only=False):
    X = sum(1 << c for c in Xcells)
    tried = 0
    for cell_of in distributions(X, grid_only):
        tried += 1
        t = run(cell_of, X, e)
        if t is not None:
            occ = [cell_of.count(c) for c in range(N)]
            print(f"{name}: FEASIBLE after {tried} distributions; wires per cell {occ}; tree {show(t, cell_of)}", flush=True)
            return True
    print(f"{name}: NO distribution, tree and matching ({tried} distributions, all trees, all matchings)", flush=True)
    return False

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    # symmetry: GL(3,2) on the rows acts on the cells; translations of the cells are multiplications by a character.
    # strong mode: e = 0 without loss; the f-cells are a set of non-zero cells (an f-cell equal to e is a smaller X).
    # weak mode: the affine group is 3-transitive on cells.
    if which in ("all", "calib"):
        print("calibration against emin8.py (grid, any 3 exceptional columns, weak rule): expect FEASIBLE; with 2: expect NO", flush=True)
        case("  grid, weak, X = {0,1,2}", [0, 1, 2], None, grid_only=True)
        case("  grid, weak, X = {0,1}", [0, 1], None, grid_only=True)
    if which in ("all", "two"):
        print("two f-cells (what 8 x 4 at 32 points can afford per block):", flush=True)
        case("  any distribution, weak (u not a character), f-cells {0,1}", [0, 1], None)
        case("  any distribution, strong (u = chi_0), f-cells {1,2}", [0, 1, 2], 0)
        case("  grid, strong (u = chi_0), f-cells {1,2}", [0, 1, 2], 0, grid_only=True)
    if which in ("all", "three"):
        print("three f-cells:", flush=True)
        case("  grid, weak, f-cells {0,1,2}", [0, 1, 2], None, grid_only=True)
        case("  any distribution, weak, f-cells {0,1,2}", [0, 1, 2], None)
        case("  any distribution, strong, f-cells {1,2,4}", [0, 1, 2, 4], 0)
        case("  any distribution, strong, f-cells {1,2,3}", [0, 1, 2, 3], 0)
    if which in ("all", "four"):
        print("four f-cells (what 8 x 2 at 16 points can afford per block):", flush=True)
        case("  any distribution, weak, f-cells {0,1,2,3}", [0, 1, 2, 3], None)
        case("  any distribution, weak, f-cells {0,1,2,4}", [0, 1, 2, 4], None)
        case("  grid, weak, f-cells {0,1,2,3}", [0, 1, 2, 3], None, grid_only=True)
