#!/usr/bin/env python3
"""c-0 big.py: the count-(O) programs at sizes g-1 did not run (1024, 4096 points; 2048 optional), pure Python integers.
Exactness: the program is run on 2^m times the identity (m = number of brick layers); every halving is asserted to divide
exactly; the result is compared with 2^m * H_n.  The program is linear, so this is the statement on the identity itself.
The final multiplications by 2^m are RUN as gates and counted.  Wires are freed after their last use."""
import sys
from fractions import Fraction as F
sys.path.insert(0, "waves/wave-03/c-0")
import verify as V

def check_int(k, plan):
    n, prog, outs, m = V.build(k, plan)
    last = {}
    for t, g in enumerate(prog):
        for i in (g[1:] if g[0] != "scale" else g[2:]): last[i] = t
    for o in outs: last[o] = len(prog)
    s = 1 << m
    v = {i: [s if j == i else 0 for j in range(n)] for i in range(n)}
    nscale = nadd = 0
    for t, g in enumerate(prog):
        if g[0] == "add": r = [p + q for p, q in zip(v[g[1]], v[g[2]])]; nadd += 1
        elif g[0] == "sub": r = [p - q for p, q in zip(v[g[1]], v[g[2]])]; nadd += 1
        else:
            c = g[1]; a = v[g[2]]; nscale += 1
            if isinstance(c, F) and c.denominator != 1:
                assert c == F(1, 2) and not any(p & 1 for p in a); r = [p >> 1 for p in a]
            else: r = [p * int(c) for p in a]
        v[n + 1 + t] = r
        for i in (g[1:] if g[0] != "scale" else g[2:]):
            if last.get(i) == t and i in v: del v[i]
    par = [bin(a).count("1") & 1 for a in range(n)]
    ok = all(v[outs[r]] == [(-s if par[r & x] else s) for x in range(n)] for r in range(n))
    return n, len(prog), nadd, nscale, m, ok

for arg in sys.argv[1:]:
    k = int(arg); mm = k // 3; plan = (3,) * mm + (1,) * (k - 3 * mm)
    n, c, nadd, nscale, m, ok = check_int(k, plan)
    print("[O] %d points, plan %s: %d gates (%d add/sub, %d scale), computes exactly H_%d: %s ; textbook %d ; my formula 20*(n/8)*m + n*(k-3m) + n = %d ; Alman-Rao's published count 23/24 n k + (n/24)(k mod 3) + n - 1 = %s" % (
        n, plan, c, nadd, nscale, n, ok, n * k, 20 * (n // 8) * mm + n * (k - 3 * mm) + n, F(23, 24) * n * k + F(n, 24) * (k % 3) + n - 1), flush=True)
