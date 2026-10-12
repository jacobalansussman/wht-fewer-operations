# d-3-mod4, experiment 4.  Independent count of the identities at 16 and 64 points, and the prediction for 256 points.
# Claim: the two-level flag identities are exactly the splittings of F_2^k into k/2 mutually orthogonal planes (for the dot
# product), none of the "mixed" type (weights 1 and 3 mod 4 on its two odd vectors).  Each plane P gives one flag step with
# values q(projection of y on P), q = weight mod 4.  Invariant of a plane (Brown, mod 8): from its Gauss sum.
# Count the splittings directly and compare with the search (6 at k = 4, 280 at k = 6).  Exact integer arithmetic.
import sys, itertools, time
from collections import Counter
pc = lambda x: bin(x).count("1")
def run(k, full=True):
    n = 1 << k; t0 = time.time()
    planes = set()
    for a in range(1, n):
        for b in range(a + 1, n):
            planes.add(frozenset([a, b, a ^ b]))
    planes = [tuple(sorted(P)) for P in planes]
    def nondeg(P):
        a, b = P[0], P[1]
        return (pc(a) * pc(b) - pc(a & b) ** 2) % 2 == 1
    def typ(P):
        v = tuple(sorted(pc(x) % 4 for x in P))
        return {(1, 1, 2): "pair1", (2, 3, 3): "pair3", (2, 2, 2): "triangle", (0, 0, 2): "hyperbolic", (0, 1, 3): "mixed"}[v]
    inv = {"pair1": 2, "pair3": 6, "triangle": 4, "hyperbolic": 0, "mixed": 0}
    good = [P for P in planes if nondeg(P)]
    tcount = Counter(typ(P) for P in good)
    print("k=%d: planes %d, nondegenerate %d, by type %s" % (k, len(planes), len(good), dict(tcount)))
    perp = lambda P, R: all(pc(x & y) % 2 == 0 for x in P[:2] for y in R[:2])
    ok = [P for P in good if typ(P) != "mixed"]
    idx = {P: i for i, P in enumerate(ok)}
    if k == 4:
        res = Counter()
        for P in ok:
            for R in ok:
                if P < R and perp(P, R): res[tuple(sorted([typ(P), typ(R)]))] += 1
        print("   splittings into 2 planes:", sum(res.values()), dict(res))
    if k == 6:
        res = Counter(); seen = set()
        comp = {}
        for P in ok:
            for R in ok:
                if P < R and perp(P, R):
                    # third plane = vectors orthogonal to both
                    T = [y for y in range(1, n) if all(pc(y & x) % 2 == 0 for x in (P[0], P[1], R[0], R[1]))]
                    T = tuple(sorted(T))
                    if len(T) == 3 and T in idx:
                        key = frozenset([P, R, T])
                        if key not in seen:
                            seen.add(key); res[tuple(sorted([typ(P), typ(R), typ(T)]))] += 1
        print("   splittings into 3 planes:", len(seen))
        for key, c in sorted(res.items()): print("     ", key, c, " invariants sum to", sum(inv[t] for t in key) % 8, "mod 8 (k mod 8 = %d)" % (k % 8))
    print("   (%.0f s)" % (time.time() - t0)); sys.stdout.flush()
run(4); run(6)
