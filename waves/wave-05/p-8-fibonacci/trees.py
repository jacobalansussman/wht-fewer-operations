# p-8-fibonacci/trees.py : all rooted binary merge trees on 2^k labelled leaves, up to the affine group AGL(k,2)
# acting on the labels.  A tree = frozenset of its internal node masks (leaf sets of size >= 2).
# Output: one line per orbit: orbit size, then the internal node masks.   Exact, combinatorial.
import sys
k = int(sys.argv[1]); N = 1 << k
def trees(leaves):
    # all rooted binary trees on the tuple of leaves (unordered children): yields frozenset of internal masks
    if len(leaves) == 1:
        yield frozenset(); return
    first, rest = leaves[0], leaves[1:]
    m = len(rest)
    full = sum(1 << x for x in leaves)
    for sel in range(1 << m):          # subset of rest that goes with 'first'
        A = (first,) + tuple(rest[i] for i in range(m) if sel >> i & 1)
        B = tuple(rest[i] for i in range(m) if not sel >> i & 1)
        if not B: continue
        for ta in trees(A):
            for tb in trees(B):
                yield ta | tb | {full}
allt = list(trees(tuple(range(N))))
idx = {t: i for i, t in enumerate(allt)}
print("# labelled trees:", len(allt), file=sys.stderr)
# generators of AGL(k,2): translation by 1, and the linear maps  x1 += x2 (transvection), cyclic shift of the bits
def perm_mask(perm):
    tab = [0] * (1 << N)
    for m in range(1 << N):
        r = 0; mm = m
        while mm:
            b = mm & -mm; r |= 1 << perm[b.bit_length() - 1]; mm ^= b
        tab[m] = r
    return tab
gens = []
gens.append([x ^ 1 for x in range(N)])
gens.append([x ^ ((x >> 1 & 1)) for x in range(N)])                      # bit0 += bit1
gens.append([((x << 1) | (x >> (k - 1))) & (N - 1) for x in range(N)])   # rotate bits
tabs = [perm_mask(g) for g in gens]
par = list(range(len(allt)))
def find(a):
    while par[a] != a:
        par[a] = par[par[a]]; a = par[a]
    return a
for i, t in enumerate(allt):
    for tab in tabs:
        j = idx[frozenset(tab[m] for m in t)]
        a, b = find(i), find(j)
        if a != b: par[a] = b
orb = {}
for i in range(len(allt)): orb.setdefault(find(i), []).append(i)
print("# orbits under AGL:", len(orb), file=sys.stderr)
for r, mem in sorted(orb.items(), key=lambda kv: -len(kv[1])):
    t = allt[mem[0]]
    print(len(mem), *sorted(t, key=lambda m: (-bin(m).count('1'), m)))
