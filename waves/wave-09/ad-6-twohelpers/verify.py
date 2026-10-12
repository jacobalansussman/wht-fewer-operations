#!/usr/bin/env python3
"""verify.py [ad-6-twohelpers]  Exact test of pairs of partitions, and the 'selector and atoms' family.

TEST (whole numbers, exact).  Two partitions P1, P2 of the N = 2^k cube points, given as label lists.  Every polynomial
of degree <= d is (a function of the P1 label) + (a function of the P2 label)  if and only if  there are vectors
U[c1], V[c2] with  phi(x) = U[P1(x)] + V[P2(x)]  for every point x, phi(x) = the list of all monomials of degree <= d
at x.  We walk each connected piece of the graph (classes = vertices, points = edges), fix U at one class, propagate,
and check every remaining point.  No rank, no prime: integers only.

FAMILY 'selector and atoms' (degree 2).  Address = (a, y): a = t selector bits, y = the other m = k - t bits.  The m
bits of y are split into 2^t groups ('atoms'), one per value of a.
   P1 forgets a (label: y).            P2 knows a and all of y except the atom whose index is a.
FAMILY 'one more degree'.  P1 forgets one bit a; P2 is R1(y) where a = 0 and R2(y) where a = 1, (R1, R2) a good pair
for degree d - 1 on the other k - 1 bits.
"""
import sys, itertools
from fractions import Fraction

def mons(k, d):
    return [sum(1 << i for i in S) for j in range(d + 1) for S in itertools.combinations(range(k), j)]

def good(k, d, lab1, lab2):
    """exact: returns (True, classes, components) or (False, classes, None)"""
    N = 1 << k; M = mons(k, d); D = len(M)
    c1 = {}; c2 = {}
    for x in range(N):
        c1.setdefault(lab1[x], []).append(x); c2.setdefault(lab2[x], []).append(x)
    U = {}; V = {}; comps = 0
    for root in c1:
        if root in U: continue
        comps += 1; U[root] = [0] * D; stack = [(1, root)]
        while stack:
            side, c = stack.pop()
            if side == 1:
                u = U[c]
                for x in c1[c]:
                    val = [(1 if (x & m) == m else 0) - u[i] for i, m in enumerate(M)]
                    v = lab2[x]
                    if v in V:
                        if V[v] != val: return False, len(c1) + len(c2), None
                    else: V[v] = val; stack.append((2, v))
            else:
                v = V[c]
                for x in c2[c]:
                    val = [(1 if (x & m) == m else 0) - v[i] for i, m in enumerate(M)]
                    u = lab1[x]
                    if u in U:
                        if U[u] != val: return False, len(c1) + len(c2), None
                    else: U[u] = val; stack.append((1, u))
    return True, len(c1) + len(c2), comps

# ---- control: the rank test of aa-cross/h1_graph.py (copied), on small cases
def rank_frac(rows):
    M = [[Fraction(v) for v in r] for r in rows]; rk = 0; nc = len(M[0])
    for c in range(nc):
        piv = None
        for i in range(rk, len(M)):
            if M[i][c] != 0: piv = i; break
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        inv = 1 / M[rk][c]; M[rk] = [v * inv for v in M[rk]]; R = M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], R)]
        rk += 1
        if rk == len(M): break
    return rk
def defect(k, d, a, b):
    N = 1 << k
    I = [[1 if l == c else 0 for l in lab] for lab in (a, b) for c in sorted(set(lab), key=repr)]
    mon = [[1 if (x & m) == m else 0 for x in range(N)] for m in mons(k, d)]
    return rank_frac(I + mon) - rank_frac(I)

def theta(k):
    N = 1 << k
    return [x >> 1 for x in range(N)], [('P', (x >> 1) & 1) if not x & 1 else ('R', x >> 2) for x in range(N)]
def halves(k):
    h = k // 2; N = 1 << k
    return [x >> h for x in range(N)], [x & ((1 << h) - 1) for x in range(N)]

def atoms_even(m, t):
    """split m bit positions into 2^t groups, sizes as equal as possible; returns list of masks"""
    g = 1 << t; masks = [0] * g
    for j in range(m): masks[j % g] |= 1 << j
    return masks
def selector(k, t, atoms=None):
    """the family: returns lab1, lab2"""
    N = 1 << k; m = k - t
    if atoms is None: atoms = atoms_even(m, t)
    full = (1 << m) - 1
    lab1 = [x >> t for x in range(N)]
    lab2 = [(x & ((1 << t) - 1), (x >> t) & (full ^ atoms[x & ((1 << t) - 1)])) for x in range(N)]
    return lab1, lab2
def count_selector(k, t):
    m = k - t; at = atoms_even(m, t)
    return (1 << m) + sum(1 << (m - bin(a).count('1')) for a in at)
def best_t(k):
    return min(range(1, k), key=lambda t: count_selector(k, t))
def onemore(k, pair):
    """P1 forgets bit 0; P2 = R1(y) at a = 0, R2(y) at a = 1"""
    R1, R2 = pair; N = 1 << k
    return [x >> 1 for x in range(N)], [(0, R1[x >> 1]) if not x & 1 else (1, R2[x >> 1]) for x in range(N)]

if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    print("== control of the test itself (rank test of h1_graph.py in fractions against the walk), k = 3..5")
    for k in (3, 4, 5):
        for name, pr in (("theta", theta(k)), ("halves", halves(k))):
            for d in (1, 2, 3):
                g = good(k, d, *pr)[0]; df = defect(k, d, *pr)
                print("  k=%d %-6s degree<=%d : walk says %-5s rank test says missing %d  %s" % (k, name, d, g, df, "agree" if g == (df == 0) else "DISAGREE"))
    print("== selector-and-atoms family, degree 2 (exact walk).  columns: k, N, t, classes, classes/N, good for degree 2, good for degree 3, components")
    for k in range(3, kmax + 1):
        N = 1 << k
        for t in sorted(set([1, 2, 3, best_t(k)])):
            if t >= k: continue
            pr = selector(k, t); g2 = good(k, 2, *pr); g3 = good(k, 3, *pr) if k <= 10 else (None,)
            print("  k=%2d N=%6d t=%d classes %6d = %.4f N   degree 2: %s   degree 3: %s   components %s%s" % (
                k, N, t, g2[1], g2[1] / N, g2[0], g3[0], g2[2], "   <- best t" if t == best_t(k) else ""))
            assert g2[1] == count_selector(k, t)
    print("== small cases against the rank test (fractions): selector family k = 3..6, every t")
    for k in range(3, 7):
        for t in range(1, k):
            pr = selector(k, t); print("  k=%d t=%d classes %d : missing degree<=2: %d ; degree<=3: %d" % (k, t, good(k, 2, *pr)[1], defect(k, 2, *pr), defect(k, 3, *pr)))
    print("== 'one more degree': P1 forgets one bit, P2 = a good pair for degree d-1 on the rest, glued by that bit")
    for k in range(4, min(kmax, 11) + 1):
        N = 1 << k
        pr3 = onemore(k, selector(k - 1, best_t(k - 1))); g3 = good(k, 3, *pr3); g4 = good(k, 4, *pr3)
        line = "  k=%2d degree 3: classes %5d = %.4f N good %s (degree 4: %s)" % (k, g3[1], g3[1] / N, g3[0], g4[0])
        if k >= 5:
            pr4 = onemore(k, onemore(k - 1, selector(k - 2, best_t(k - 2)))); h4 = good(k, 4, *pr4)
            line += " ; degree 4: classes %5d = %.4f N good %s" % (h4[1], h4[1] / N, h4[0])
        print(line)
    print("== the table V2upper(k) = least count in the family over t (formula 2^(k-t) + sum over atoms of 2^(k-t-size))")
    for k in range(3, 41):
        t = best_t(k); c = count_selector(k, t)
        print("  k=%2d t=%d classes/N = %.5f   (theta family 3N/4+2: %.5f)   2 log2(k)/k = %.5f" % (k, t, c / (1 << k), 0.75 + 2 / (1 << k), 2 * __import__('math').log2(k) / k))
