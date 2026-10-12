#!/usr/bin/env python3
"""w5_look.py (n-2): the one 21-move count vector for 5 arrays, read in the frame picture."""
import sys, pickle
sys.argv = [sys.argv[0], "0"]
import mypost as P
cl = pickle.load(open("classes_W5_K21.pkl", "rb"))
(c,) = cl[21]
frames = sorted({tuple(sorted(b)) for b in P.bases})
odd = [1 if P.par(z) else 0 for z in P.V]
hits = []
for f in frames:
    n = odd[:]
    for z in f: n[z - 1] += 1
    hits.append(P.canon(n) == c)
print("the 21-move vector:", " ".join("%s:%d" % (format(i + 1, "05b"), c[i]) for i in range(31) if c[i]))
print("equals 'every odd-weight direction once, plus one frame' for each of the 6 frames:", hits)
kind, nt, clq, info = P.judge(list(c))
print("verdict with W =", P.W, ":", kind, "; tight selections", nt, "; largest joined set", clq)
