#!/usr/bin/env python3
"""tower.py [ag-0-ladderdegree3]   Pairs of partitions for degree 3 in which P1 forgets a selector with several
values ("colours") and P2 at colour c is a partition R_c of the y cube.  Exact test: verify.good of ad-6.

FAMILY W ("tower of lamps", iterated regular wreath product).  L colours, each atom s bits.
  level 1: one atom U1 (s bits).
  level j+1: one atom of s bits for EVERY value of all the bits of levels 1..j  (2^(m_j) atoms), m_1 = s,
             m_(j+1) = m_j + s * 2^(m_j).
  R_j forgets the level-j atom whose index is the present value of ALL bits of levels below j.
  (R_1 forgets U1.)  Selector a in {0..2^t-1}; colour a < L uses R_(a+1); colours >= L use the discrete partition.
  P1 = forget a.   P2 = (a, R_a(y)).

usage: tower.py W L s [d]     -> builds, tests degree d (default 3) and also d-1, d+1
"""
import sys, os, itertools, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ad-6-twohelpers"))
from verify import good

def tower_levels(L, s):
    """returns list of (offset, width) per level and total m; level j has 2^(m_(j-1)) atoms of s bits"""
    offs = []; m = 0
    for j in range(L):
        natoms = 1 if j == 0 else (1 << m)
        offs.append((m, natoms)); m += s * natoms
    return offs, m

def build_W(L, s, t=None, drop=()):
    offs, m = tower_levels(L, s)
    if t is None:
        t = max(1, (L - 1).bit_length())
    k = t + m; N = 1 << k
    amask = (1 << t) - 1; smask = (1 << s) - 1
    lab1 = [0] * N; lab2 = [0] * N
    for x in range(N):
        a = x & amask; y = x >> t
        lab1[x] = y
        if a < L and a not in drop:
            off, natoms = offs[a]
            idx = y & ((1 << off) - 1) if a > 0 else 0     # value of all lower bits
            pos = off + s * idx
            lab2[x] = (a, y & ~(smask << pos))
        else:
            lab2[x] = (a, y)
    return k, lab1, lab2

if __name__ == "__main__":
    fam = sys.argv[1]; L = int(sys.argv[2]); s = int(sys.argv[3]); d = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    t0 = time.time()
    k, l1, l2 = build_W(L, s)
    N = 1 << k
    print("family W: L=%d colours, atoms of s=%d bits: k=%d N=%d" % (L, s, k, N), flush=True)
    for dd in (d - 1, d, d + 1):
        g = good(k, dd, l1, l2)
        print("  degree <= %d : good %s   classes %d = %.4f N   components %s   (%.1f s)" % (dd, g[0], g[1], g[1] / N, g[2], time.time() - t0), flush=True)
