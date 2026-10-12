#!/usr/bin/env python3
"""designs.py [ag-0-ladderdegree3]   "Coloured atoms" designs, tested exactly with ad-6's verify.good.

A design: m state bits y; L colours; for each colour c a function act_c(y) -> mask of the bits that colour c
forgets at y (its ACTIVE ATOM).  act_c must not depend on the bits it returns.  R_c = "forget the active atom".
Pair on k = t + m bits (t selector bits, colour = selector value; selector values >= L get the discrete partition):
   P1 forgets the selector;   P2 = (colour, R_colour(y)).
RULE D (sufficient, derived in ag-0.md): for any two bits p, q in atoms of different colours, either q has one fixed
value whenever p's atom is active, or p has one fixed value whenever q's atom is active.
Also: check that the P1 helper A(y) is a polynomial of degree <= 3 in y (Moebius transform of the solved U).
"""
import sys, os, itertools, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ad-6-twohelpers"))
from verify import good, mons

def pair_from_design(m, acts, t=None):
    L = len(acts)
    if t is None: t = max(1, (L - 1).bit_length())
    k = t + m; N = 1 << k; am = (1 << t) - 1
    lab1 = [0] * N; lab2 = [0] * N
    for x in range(N):
        a = x & am; y = x >> t
        lab1[x] = y
        if a < L:
            mask = acts[a](y)
            assert acts[a](y ^ mask) == mask or True
            lab2[x] = (a, y & ~mask)
        else:
            lab2[x] = (a, y)
    return k, t, lab1, lab2

def rule_D(m, acts):
    """exact check of rule D by enumeration of all states.  returns number of violating bit pairs"""
    L = len(acts); seen = {}            # (colour, mask) -> [and of states, or of states]
    for y in range(1 << m):
        for c in range(L):
            mk = acts[c](y); key = (c, mk)
            if key not in seen: seen[key] = [y, y]
            else: seen[key][0] &= y; seen[key][1] |= y
    atoms = list(seen)
    fixed = {a: ~(seen[a][0] ^ seen[a][1]) & ((1 << m) - 1) for a in atoms}   # bits constant on act(a)
    bad = 0
    for a in atoms:
        for b in atoms:
            if a[0] >= b[0]: continue
            for p in range(m):
                if not a[1] >> p & 1: continue
                for q in range(m):
                    if not b[1] >> q & 1: continue
                    if not (fixed[a] >> q & 1) and not (fixed[b] >> p & 1): bad += 1
    return bad, len(atoms)

def solve_U(k, d, lab1, lab2):
    """the walk of verify.good, returning U (vectors on P1 classes) if good, else None"""
    N = 1 << k; M = mons(k, d); D = len(M)
    c1 = {}; c2 = {}
    for x in range(N):
        c1.setdefault(lab1[x], []).append(x); c2.setdefault(lab2[x], []).append(x)
    U = {}; V = {}
    for root in c1:
        if root in U: continue
        U[root] = [0] * D; stack = [(1, root)]
        while stack:
            side, c = stack.pop()
            if side == 1:
                u = U[c]
                for x in c1[c]:
                    val = [(1 if (x & mm) == mm else 0) - u[i] for i, mm in enumerate(M)]
                    v = lab2[x]
                    if v in V:
                        if V[v] != val: return None
                    else: V[v] = val; stack.append((2, v))
            else:
                v = V[c]
                for x in c2[c]:
                    val = [(1 if (x & mm) == mm else 0) - v[i] for i, mm in enumerate(M)]
                    u = lab1[x]
                    if u in U:
                        if U[u] != val: return None
                    else: U[u] = val; stack.append((1, u))
    return U, V, M

def degree_of_U(m, U, D):
    """U: dict y -> vector of length D.  Moebius transform in y of each coordinate; returns the largest size of a set
    with a nonzero coefficient, over all coordinates."""
    worst = 0
    for i in range(D):
        f = [U[y][i] for y in range(1 << m)]
        for b in range(m):
            bit = 1 << b
            for y in range(1 << m):
                if y & bit: f[y] -= f[y ^ bit]
        for y in range(1 << m):
            if f[y] != 0:
                w = bin(y).count("1")
                if w > worst: worst = w
    return worst

# ---------------- designs
def tower(L, s):
    offs = []; m = 0
    for j in range(L):
        n = 1 if j == 0 else (1 << m)
        offs.append(m); m += s * n
    sm = (1 << s) - 1
    def mk(j):
        off = offs[j]
        if j == 0: return lambda y: sm
        return lambda y: sm << (off + s * (y & ((1 << off) - 1)))
    return m, [mk(j) for j in range(L)]

def tree(L):
    """permutational tree, s = 1: level j has 2^(j-1) one-bit atoms indexed by the values of the ACTIVE atoms above"""
    offs = [(1 << j) - 1 for j in range(L)]; m = (1 << L) - 1
    def path(y, j):                 # index of the active atom at level j
        idx = 0
        for l in range(j):
            b = (y >> (offs[l] + idx)) & 1
            idx = idx * 2 + b
        return idx
    def mk(j): return lambda y: 1 << (offs[j] + path(y, j))
    return m, [mk(j) for j in range(L)]

def caterpillar2(r):
    """two colours, s = 1, NEITHER forgets a fixed set.  bits: beta_1..beta_r (bits 0..r-1), alpha_1..alpha_r (bits r..2r-1),
       alpha_end (bit 2r).  colour 0 forgets alpha_i, i = first index with beta_i = 1 (alpha_end if none);
       colour 1 forgets beta_i, i = first index < r with alpha_i = 1 (beta_r if none)."""
    m = 2 * r + 1
    def a0(y):
        for i in range(r):
            if (y >> i) & 1: return 1 << (r + i)
        return 1 << (2 * r)
    def a1(y):
        for i in range(r - 1):
            if (y >> (r + i)) & 1: return 1 << i
        return 1 << (r - 1)
    return m, [a0, a1]

def parity_lamps(L):
    """edge lamps of the cube Q_L (s = 1): colour i forgets the lamp on the direction-i edge at the vertex v, v_j = parity
       of all lamps of colour j.  bits: colour i, position u in {0,1}^(L-1) -> i * 2^(L-1) + u"""
    h = 1 << (L - 1); m = L * h
    def mk(i):
        def f(y):
            u = 0; pos = 0
            for j in range(L):
                if j == i: continue
                par = bin((y >> (j * h)) & (h - 1)).count("1") & 1
                u |= par << pos; pos += 1
            return 1 << (i * h + u)
        return f
    return m, [mk(i) for i in range(L)]

if __name__ == "__main__":
    which = sys.argv[1:] or ["all"]
    tests = [("tower L=2 s=1", tower(2, 1)), ("tower L=2 s=2", tower(2, 2)), ("tower L=3 s=1", tower(3, 1)),
             ("tree L=3 (permutational, 7 bits)", tree(3)), ("tree L=2", tree(2)),
             ("caterpillar r=2", caterpillar2(2)), ("caterpillar r=3", caterpillar2(3)), ("caterpillar r=4", caterpillar2(4)), ("caterpillar r=5", caterpillar2(5)),
             ("parity lamps L=2", parity_lamps(2)), ("parity lamps L=3", parity_lamps(3))]
    for name, (m, acts) in tests:
        t0 = time.time()
        bad, natoms = rule_D(m, acts)
        k, t, l1, l2 = pair_from_design(m, acts)
        N = 1 << k
        g2 = good(k, 2, l1, l2); g3 = good(k, 3, l1, l2); g4 = good(k, 4, l1, l2) if k <= 13 else (None,)
        line = "%-34s m=%2d atoms=%4d k=%2d  rule D violations %5d | good deg2 %s deg3 %s deg4 %s | classes %d = %.4f N" % (
            name, m, natoms, k, bad, g2[0], g3[0], g4[0], g3[1], g3[1] / N)
        if g3[0]:
            U, V, M = solve_U(k, 3, l1, l2)
            # coordinates of U are indexed by monomials of (selector, y); U is a function of y
            dg = degree_of_U(m, U, len(M))
            line += " | degree of helper A in y: %d" % dg
        print(line + "  (%.1f s)" % (time.time() - t0), flush=True)
