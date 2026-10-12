#!/usr/bin/env python3
"""planes16.py (p-3-hatch32): the bottom of a tree in a block of 16 points, exhaustive.

Every tree has a node with 3 or 4 leaves whose children have at most 2.  A 3-node and a 4-node that is not a plane fail
the count (p-3.md section 4).  Here: the plane P = {0,1,2,3} made of the pairs R1 = {0,1}, R2 = {2,3} (direction d = 1;
all planes with a marked pair of pairs are equivalent under the affine group).  16 cells eta in F_2^4.
  L = the cells perpendicular to P - P = {0,4,8,12};   d-perp = the even cells.
Unknowns: the exceptional set X (f-cells F, plus e in strong mode), and which non-exceptional cells hold a wire of R1'
(the set T1, at most 2 cells) and of R2' (T2, at most 2 cells).  Nothing else about the distribution of wires matters.
Rule (weak / strong):  non-exceptional cells with no wire in R1' lie in one coset of d-perp (strong: the coset of e);
the same for R2'; non-exceptional cells with no wire in P' lie in one coset of L (strong: the coset of e).
Claim to check: with 8 f-cells every solution has T1, T2 disjoint of size 2, T1 + T2 = one coset of L, and the
non-exceptional cells inside one coset of d-perp; with 7 f-cells there is no solution.
"""
import sys, itertools
NC = 16
L = [0, 4, 8, 12]
LCOS = [sum(1 << (a ^ l) for l in L) for a in (0, 1, 2, 3)]
DCOS = [sum(1 << c for c in range(NC) if c % 2 == p) for p in (0, 1)]
def in_one(mask, cosets): return any(mask & ~c == 0 for c in cosets)
def small_subsets(cells):
    out = [0]
    out += [1 << a for a in cells]
    out += [(1 << a) | (1 << b) for a, b in itertools.combinations(cells, 2)]
    return out

def scan(nf, strong):
    sols = 0; ok_struct = True; examples = []
    base = range(1, NC) if strong else range(NC)
    for F in itertools.combinations(base, nf):
        X = sum(1 << c for c in F) | (1 if strong else 0)
        non = [c for c in range(NC) if not (X >> c) & 1]
        nonm = sum(1 << c for c in non)
        dcos = [DCOS[0]] if strong else DCOS          # e = 0 is even and lies in L
        lcos = [LCOS[0]] if strong else LCOS
        subs = small_subsets(non)
        good1 = [T for T in subs if in_one(nonm & ~T, dcos)]
        for T1 in good1:
            for T2 in good1:
                if in_one(nonm & ~(T1 | T2), lcos):
                    sols += 1
                    Y = T1 | T2
                    st = (bin(T1).count("1") == 2 and bin(T2).count("1") == 2 and T1 & T2 == 0
                          and any(Y == c for c in LCOS) and in_one(nonm, DCOS))
                    ok_struct = ok_struct and st
                    if len(examples) < 2:
                        examples.append((F, [c for c in range(NC) if (T1 >> c) & 1], [c for c in range(NC) if (T2 >> c) & 1]))
    mode = "strong (u = chi_0)" if strong else "weak"
    print(f"{nf} f-cells, {mode}: {sols} solutions (F, T1, T2); all have the claimed structure: {ok_struct if sols else 'n/a'}; examples {examples}", flush=True)

if __name__ == "__main__":
    scan(8, False)
    scan(8, True)
    scan(7, False)
    scan(7, True)
