import sys
args = sys.argv[:]; sys.argv = [args[0], "19"]
import post, post2, numpy as np, itertools
V = post.V; dot = post.dot
odd = [z for z in V if bin(z).count("1") & 1]
frames = [F for F in itertools.combinations(odd, 5) if all(dot(a, b) == 0 for a, b in itertools.combinations(F, 2))]
def name(z):
    if z == 31: return "centre"
    if bin(z).count("1") & 1:
        fs = [i for i, F in enumerate(frames) if z in F]; return "o%d%d" % tuple(fs)
    fs = [i for i, F in enumerate(frames) if (z ^ 31) in F]; return "e%d%d" % tuple(fs)
seen = set()
for line in open(args[1]):
    p = line.split(); n = list(map(int, p[2:])); c = post.canon_fast(n)
    if c in seen: continue
    seen.add(c)
    kind, nt, cl, s, info = post2.both(c)
    print(kind, "tight", nt, "largest joined", cl, ":", post.fmt(c))
    print("    as pairs of frames (o = odd direction, e = its even partner 11111 + o):", " ".join("%s%s" % (name(V[i]), "x%d" % c[i] if c[i] > 1 else "") for i in range(31) if c[i]))
