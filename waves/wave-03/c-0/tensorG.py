#!/usr/bin/env python3
"""c-0 tensorG.py: count (G) tensor products of the 19-gate circuit, my own code, exact integers, all unit vectors.
16 points = one layer of 8-point circuits (2 of them) + one layer of butterflies (8, two gates each): 54.
64 points = two layers of 8-point circuits: 304.  512 points = three layers: 3648 (one size beyond g-1)."""
import sys
sys.path.insert(0, "waves/wave-03/c-0")
import verify as V

def run(k, plan):
    n = 1 << k; cur = [[int(i == j) for j in range(n)] for i in range(n)]; gates = 0; pos = 0
    for part in plan:
        blk = list(range(pos, pos + part)); pos += part; rest = [d for d in range(k) if d not in blk]
        for base in range(1 << len(rest)):
            a0 = sum(((base >> q) & 1) << d for q, d in enumerate(rest))
            idx = [a0 + sum(((t >> q) & 1) << d for q, d in enumerate(blk)) for t in range(1 << part)]
            if part == 3:
                w = {"x%d" % t: cur[i] for t, i in enumerate(idx)}
                for (name, a, u, b, v) in V.G:
                    w[name] = [a * p + b * q for p, q in zip(w[u], w[v])]; gates += 1
                for t, i in enumerate(idx): cur[i] = w["y%d" % t]
            else:
                p, q = cur[idx[0]], cur[idx[1]]
                cur[idx[0]] = [x + y for x, y in zip(p, q)]; cur[idx[1]] = [x - y for x, y in zip(p, q)]; gates += 2
    ok = all(cur[r] == [V.chi(r, x) for x in range(n)] for r in range(n))
    return n, gates, ok

for k, plan in ((4, (3, 1)), (6, (3, 3)), (9, (3, 3, 3))):
    n, g, ok = run(k, plan)
    print("[G] %d points, plan %s: %d gates, computes exactly H_%d (every output factor 1): %s ; textbook %d ; ratio %.4f" % (n, plan, g, n, ok, n * k, g / (n * k)))
