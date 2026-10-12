import sys, itertools
sys.argv = [sys.argv[0], "19"]
import post, numpy as np
V = post.V
odd = [z for z in V if bin(z).count("1") & 1]
design = [1 if z in odd else 0 for z in V]
cls = {}
for comb in itertools.combinations_with_replacement(range(31), 3):
    n = design[:]
    for i in comb: n[i] += 1
    cls.setdefault(post.canon_fast(n), comb)
for c, comb in sorted(cls.items()):
    nt, best, bs = post.clique_test(c)
    if best <= 8:
        n = np.array(c); cnt = post.A @ n
        tight = np.unique(post.A[cnt == 4] * (n > 0), axis=0)
        print("extras %s -> canonical %s" % ([format(V[i], "05b") for i in comb], post.fmt(c)))
        print("   tight selections %d, largest joined set %d (%s)" % (nt, best, [format(V[i], "05b") for i in range(31) if bs >> i & 1]))
        for row in tight[:12]: print("      tight:", [format(V[i], "05b") + ("x%d" % c[i] if c[i] > 1 else "") for i in range(31) if row[i]])
        hist = {}
        for v in cnt: hist[int(v)] = hist.get(int(v), 0) + 1
        print("   forms by number of moves selected:", sorted(hist.items()))
