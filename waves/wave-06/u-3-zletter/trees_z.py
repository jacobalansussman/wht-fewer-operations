# u-3-zletter/trees_z.py : all rooted binary merge trees on 2^k labelled leaves, up to PERMUTATIONS OF THE k ADDRESS BITS
# (the symmetries of the subset-sum matrix Z).  Output: orbit size, then the N-1 internal node masks, then N ones (plain centre).
import sys
from itertools import permutations
k = int(sys.argv[1]); N = 1 << k
def trees(leaves):
    if len(leaves) == 1:
        yield frozenset(); return
    first, rest = leaves[0], leaves[1:]
    m = len(rest)
    full = sum(1 << x for x in leaves)
    for sel in range(1 << m):
        A = (first,) + tuple(rest[i] for i in range(m) if sel >> i & 1)
        B = tuple(rest[i] for i in range(m) if not sel >> i & 1)
        if not B: continue
        for ta in trees(A):
            for tb in trees(B):
                yield ta | tb | {full}
allt = list(trees(tuple(range(N))))
print("# labelled trees:", len(allt), file=sys.stderr)
def perm_mask(perm):
    tab = [0] * (1 << N)
    for m in range(1, 1 << N):
        b = m & -m
        tab[m] = tab[m ^ b] | (1 << perm[b.bit_length() - 1])
    return tab
tabs = []
for p in permutations(range(k)):
    perm = [sum(((x >> i) & 1) << p[i] for i in range(k)) for x in range(N)]
    tabs.append(perm_mask(perm))
seen = set(); nor = 0
for t in allt:
    if t in seen: continue
    orb = set(frozenset(tab[m] for m in t) for tab in tabs)
    seen |= orb; nor += 1
    print(len(orb), *sorted(t, key=lambda m: (-bin(m).count('1'), m)), *([1] * N))
print("# orbits under bit permutations:", nor, file=sys.stderr)
