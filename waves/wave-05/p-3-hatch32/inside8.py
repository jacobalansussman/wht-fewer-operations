#!/usr/bin/env python3
"""inside8.py (p-3-hatch32): the 8-point exception count under (G) with the INSIDE rule added (p-3.md section 4).

Grid case: one wire per cell.  Outside rule as in cells8.py.  Inside rule at a node R with wires R':
the rows of the step on R must be independent, and every column outside R' is a multiple of c_R on R, so
    rank( {chi_eta|R : eta a non-exceptional cell of R'}  +  {c_R} )  +  (exceptional cells of R', whose columns are free)  >=  |R|.
c_R is chi_e|R if u = chi_e (strong mode); else chi_g|R for any non-exceptional cell g outside R'; else unknown (counted as 1).
Exceptional columns are all treated as free, which is a relaxation.  Exhaustive over trees and matchings.
Also: the inside rule evaluated on the skeptic's explicit 16-leaf tree (c-2/c2_e16.py), node by node.
"""
import sys, itertools
from fractions import Fraction as Fr
from functools import lru_cache

def dotp(a, b): return bin(a & b).count("1") & 1
def rank(vs):
    M = [[Fr(v) for v in r] for r in vs]; rk = 0
    if not M: return 0
    for c in range(len(M[0])):
        piv = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        for i in range(rk + 1, len(M)):
            if M[i][c] != 0:
                f = M[i][c] / M[rk][c]; M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk

def solve(N, X, e, inside):
    FULL = (1 << N) - 1
    POP = [bin(v).count("1") for v in range(1 << N)]
    def perp(R):
        pts = [x for x in range(N) if (R >> x) & 1]
        return sum(1 << eta for eta in range(N) if all(dotp(eta, p ^ pts[0]) == 0 for p in pts))
    PERP = {}
    nonexc = FULL & ~X
    def rule(R, Rp):
        if POP[R] == 1: return True
        if R not in PERP: PERP[R] = perp(R)
        G = nonexc & ~Rp
        g0 = e if e is not None else ((G & -G).bit_length() - 1 if G else None)
        if G:
            pm = PERP[R]
            for eta in range(N):
                if (G >> eta) & 1 and not (pm >> (eta ^ g0)) & 1: return False
        if inside:
            rows = [x for x in range(N) if (R >> x) & 1]
            vecs = [[-1 if dotp(eta, x) else 1 for x in rows] for eta in range(N) if (Rp >> eta) & 1 and (nonexc >> eta) & 1]
            extra = 0
            if g0 is not None: vecs.append([-1 if dotp(g0, x) else 1 for x in rows])
            else: extra = 1
            if rank(vecs) + extra + POP[Rp & X] < POP[R]: return False
        return True
    @lru_cache(maxsize=None)
    def feas(R, Rp):
        if not rule(R, Rp): return None
        if POP[R] == 1: return (R, Rp)
        low = R & -R; rest = R ^ low; sub = rest
        while True:
            R1 = low | sub
            if R1 != R:
                n1 = POP[R1]; s2 = Rp
                while s2:
                    if POP[s2] == n1:
                        a = feas(R1, s2)
                        if a is not None:
                            b = feas(R ^ R1, Rp ^ s2)
                            if b is not None: return (R, Rp, a, b)
                    s2 = (s2 - 1) & Rp
            if sub == 0: break
            sub = (sub - 1) & rest
        return None
    return feas(FULL, FULL)

def show(t):
    if len(t) == 2: return f"{t[0].bit_length() - 1}>{t[1].bit_length() - 1}"
    return "(" + show(t[2]) + " " + show(t[3]) + ")"

if __name__ == "__main__":
    cases = [("3 kind-q cells {0,1,2}, weak", [0, 1, 2], None),
             ("3 kind-q {1,2,4} + kind u at 0", [0, 1, 2, 4], 0), ("3 kind-q {1,2,3} + kind u at 0", [0, 1, 2, 3], 0),
             ("4 kind-q cells {0,1,2,3} (a plane), weak", [0, 1, 2, 3], None), ("4 kind-q cells {0,1,2,4}, weak", [0, 1, 2, 4], None),
             ("4 kind-q {4,5,6,7} + kind u at 0", [0, 4, 5, 6, 7], 0), ("4 kind-q {1,2,3,4} + kind u at 0", [0, 1, 2, 3, 4], 0),
             ("5 kind-q cells {0,1,2,3,4}, weak", [0, 1, 2, 3, 4], None), ("5 kind-q cells {0,1,2,4,7}, weak", [0, 1, 2, 4, 7], None),
             ("6 kind-q cells {0,1,2,3,4,5}, weak", [0, 1, 2, 3, 4, 5], None), ("6 kind-q cells {0,1,2,4,7,3}, weak", [0, 1, 2, 3, 4, 7], None)]
    print("block of 8 points, grid (one wire per cell), all trees and matchings:", flush=True)
    for name, Xc, e in cases:
        X = sum(1 << c for c in Xc)
        a = solve(8, X, e, False); b = solve(8, X, e, True)
        print(f"  {name}: outside rule only: {'feasible' if a else 'none'};  with the inside rule: {'feasible ' + show(b) if b else 'none'}", flush=True)
    # the skeptic's explicit 16-leaf tree: rows > columns, exceptional columns = the odd ones
    X16 = {1, 3, 5, 7, 9, 11, 13, 15}
    plane = (((0, 2), (1, 6)), ((2, 10), (3, 14))); six = (plane, ((4, 4), (5, 12))); eight = (six, ((6, 0), (7, 8)))
    t = eight
    for row, col in zip(range(8, 16), [1, 3, 5, 7, 9, 11, 13, 15]): t = (t, (row, col))
    print("the explicit 16-leaf tree of c-2 (8 exceptional columns), inside rule node by node:", flush=True)
    def rec(t):
        if isinstance(t[0], int): return [t[0]], [t[1]]
        R1, P1 = rec(t[0]); R2, P2 = rec(t[1]); R, Rp = R1 + R2, P1 + P2
        good_out = [g for g in range(16) if g not in X16 and g not in Rp]
        vecs = [[-1 if dotp(eta, x) else 1 for x in R] for eta in Rp if eta not in X16]
        extra = 0
        if good_out: vecs.append([-1 if dotp(good_out[0], x) else 1 for x in R])
        else: extra = 1
        bound = rank(vecs) + extra + sum(1 for eta in Rp if eta in X16)
        if len(R) <= 8 or bound < len(R):
            print(f"    node of {len(R)} rows {sorted(R)}: rows of the step have rank at most {bound}{'   <-- NOT INVERTIBLE' if bound < len(R) else ''}", flush=True)
        return R, Rp
    rec(t)
