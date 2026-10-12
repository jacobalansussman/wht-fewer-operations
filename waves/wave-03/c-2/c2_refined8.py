#!/usr/bin/env python3
"""c2_refined8.py (skeptic c-2): the REFINED exception count for a block of 8 points.

g-6's rule: at every node R of the tree inside a block, the good columns outside R' lie in one coset of (R - R)^perp.
Refinement [derived, c-2]: if the block has an exception of the first kind, i.e. its outgoing direction u is proportional
to a character chi_eta1, then that coset is the one THROUGH eta1 (because the common direction is u restricted to R), and
eta1 itself is not good.  So: good columns outside R' lie in (eta1 + (R - R)^perp) minus {eta1}.
Question: the least number of exceptional columns (eta1 included) for which some tree and matching satisfy the refined rule.
By translation of the columns eta1 = 0 without loss of generality.  Exhaustive over trees, matchings and exceptional sets.
"""
import itertools

w = 8
FULL = (1 << w) - 1

def par(v):
    return bin(v).count("1") & 1

def pts(m):
    return [x for x in range(w) if (m >> x) & 1]

PERP = {}
def perp(R):
    if R not in PERP:
        p = pts(R)
        PERP[R] = {e for e in range(w) if all(par(e & (q ^ p[0])) == 0 for q in p)}
    return PERP[R]

def search(X, eta1):
    memo = {}
    def rule(R, Rp):
        if R == FULL:
            return True
        allowed = {eta1 ^ e for e in perp(R)} - {eta1}
        return all(e in allowed for e in range(w) if not ((Rp | X) >> e) & 1)
    def feas(R, Rp):
        key = (R, Rp)
        if key in memo:
            return memo[key]
        res = None
        if rule(R, Rp):
            p = pts(R)
            if len(p) == 1:
                res = f"{p[0]}>{pts(Rp)[0]}"
            else:
                first, rest = p[0], p[1:]
                cols = pts(Rp)
                for n1 in range(0, len(rest)):
                    for extra in itertools.combinations(rest, n1):
                        R1 = (1 << first) | sum(1 << v for v in extra)
                        for cc in itertools.combinations(cols, n1 + 1):
                            R1p = sum(1 << v for v in cc)
                            x = feas(R1, R1p)
                            if x is None:
                                continue
                            y = feas(R ^ R1, Rp ^ R1p)
                            if y is not None:
                                res = f"({x} {y})"
                                break
                        if res: break
                    if res: break
        memo[key] = res
        return res
    return feas(FULL, FULL)

if __name__ == "__main__":
    eta1 = 0
    for e in range(1, 6):
        found = None
        n = 0
        for others in itertools.combinations(range(1, w), e - 1):
            X = (1 << eta1) | sum(1 << v for v in others)
            n += 1
            r = search(X, eta1)
            if r is not None:
                found = (others, r)
                break
        if found:
            print(f"[R8] block of 8 with a first-kind exception: {e} exceptional columns in all SUFFICE "
                  f"(eta1 = 0, others {found[0]}), tree {found[1]}", flush=True)
            break
        print(f"[R8] block of 8 with a first-kind exception: {e} exceptional columns in all are NOT enough ({n} sets tried)", flush=True)
