#!/usr/bin/env python3
"""replay21.py (h-8): exact integer replay of a count-(G) program file (name = a * u + b * v), check that the 8 rows of the
Walsh-Hadamard matrix all appear (up to sign), and print s, s' of every wire."""
import sys
N = 8; pc = lambda x: bin(x).count("1")
w = {"x%d" % i: [1 if j == i else 0 for j in range(N)] for i in range(N)}
gates = 0; over = []; rows = []
for line in open(sys.argv[1]):
    line = line.split("#")[0].strip()
    if not line: continue
    name, rhs = [t.strip() for t in line.split("=")]
    a, u, b, v = rhs.replace("*", " ").replace("+", " ").split()
    w[name] = [int(a) * p + int(b) * q for p, q in zip(w[u], w[v])]
    gates += 1
    vec = w[name]; s = sum(1 for z in vec if z)
    sp = sum(1 for y in range(N) if sum(vec[x] * (-1) ** pc(x & y) for x in range(N)))
    if s * sp > N: over.append((name, s, sp))
    rows.append((name, s, sp, vec))
H = [[(-1) ** pc(x & y) for x in range(N)] for y in range(N)]
got = [any(v == r or v == [-z for z in r] for v in w.values()) for r in H]
for name, s, sp, vec in rows: print("  %-6s s=%d s'=%d %s %s" % (name, s, sp, "OVER " if s * sp > N else "tight", vec))
print("gates:", gates, " over-limit wires:", len(over), over, " all 8 outputs present:", all(got), " gates + over-limit =", gates + len(over))
