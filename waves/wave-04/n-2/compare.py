#!/usr/bin/env python3
"""compare.py (n-2): the classes from my full searches against the classes from h-2's files, as sets."""
import sys, pickle, itertools
sys.argv = [sys.argv[0], "0"]
import mypost as P
H = "waves/wave-04/h-2-clique17/"
def classes_from(fn, K):
    out = set()
    for line in open(fn):
        p = line.split(); T = int(p[0]); fr = int(p[1]); n0 = list(map(int, p[2:]))
        free = [i for i in range(31) if not fr >> i & 1]
        for e in range(0, K - T + 1):
            for comb in itertools.combinations_with_replacement(free, e):
                n = n0[:]
                for i in comb: n[i] += 1
                out.add(P.canon(n))
    return out
mine = pickle.load(open("classes_W4_K19.pkl", "rb")); mine_all = set().union(*mine.values())
theirs18 = classes_from(H + "leaves18_mac.txt", 18)
print("at most 18 moves: mine %d classes, h-2's leaves18 %d classes, equal sets: %s" % (sum(len(mine[t]) for t in (16, 17, 18)), len(theirs18), theirs18 == set().union(*(mine[t] for t in (16, 17, 18)))))
a = classes_from(H + "leaves19_no00001_mac.txt", 19); b = classes_from(H + "leaves19_no11111_mac.txt", 19)
design = set(); odd = [1 if P.par(z) else 0 for z in P.V]
for comb in itertools.combinations_with_replacement(range(31), 3):
    n = odd[:]
    for i in comb: n[i] += 1
    design.add(P.canon(n))
t19 = a | b | design
print("19 moves: mine %d classes; h-2's: design+3 extras %d, search without 00001 %d, search without 11111 %d, union %d; equal sets: %s"
      % (len(mine[19]), len(design), len(a), len(b), len(t19), t19 == mine[19]))
# which of my 19-move classes miss an odd direction (the part h-2 reached by the symmetry split)
miss = [c for c in mine[19] if any(c[z - 1] == 0 for z in P.V if P.par(z))]
print("my 19-move classes that do not use all 16 odd directions:", len(miss))
for c in miss: print("   ", " ".join("%s:%d" % (format(i + 1, "05b"), c[i]) for i in range(31) if c[i]))
