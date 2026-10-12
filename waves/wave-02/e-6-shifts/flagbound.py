# e-6-shifts, Law D, the half that can be checked by brute force:
# the largest dimension of an affine subspace a + V of k-bit addresses on which the Hamming weight is constant modulo 4.
# Claim: floor(k/2).  Then "r flags give an affine subspace of dimension >= k - r with all levels constant" [derived]
# forces r >= k - floor(k/2) = ceil(k/2).  Exhaustive over all subspaces (as sorted reduced bases) and all cosets.
import sys, itertools
pc = lambda x: bin(x).count("1")
def subspaces(k, d):
    # all d-dimensional subspaces of Z_2^k, each once, as frozensets (by extension from (d-1)-dimensional ones)
    cur = {frozenset([0])}
    for _ in range(d):
        nxt = set()
        for V in cur:
            for v in range(1, 1 << k):
                if v not in V: nxt.add(frozenset(V | {w ^ v for w in V}))
        cur = nxt
    return cur
for k in range(2, 8):
    best = 0; counts = {}
    for d in range(1, k + 1):
        hit = 0
        for V in subspaces(k, d):
            if any(pc(v) % 2 for v in V): continue          # all weights in V must be even
            reps = set()
            for a in range(1 << k):
                r = min(a ^ v for v in V)
                if r in reps: continue
                reps.add(r)
                if len({pc(a ^ v) % 4 for v in V}) == 1: hit += 1
        counts[d] = hit
        if hit: best = d
        else: break
    print("k=%d  largest affine subspace with weight constant modulo 4: dimension %d (floor(k/2) = %d); cosets found per dimension %s; so flags needed >= %d" % (k, best, k // 2, counts, k - best))
    sys.stdout.flush()
