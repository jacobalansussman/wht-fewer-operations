#!/usr/bin/env python3
"""frames.py [h-7-unitmeter]  Are the frames of the certificate non-degenerate subspaces (ones with an orthonormal basis for
the dot product over two elements)?  For those the address factor of a wire is tight by the argument of h-7.md section 1.
A subspace has an orthonormal basis iff the Gram matrix of a basis is invertible and the subspace has an odd-weight vector.
usage: python3 -I -B frames.py <certificate.json.gz> [more]"""
import sys, json, gzip
from collections import Counter
par = lambda x: bin(x).count("1") & 1
def rank2(rows):
    rows = list(rows); rk = 0
    for bit in range(64):
        p = next((i for i in range(rk, len(rows)) if rows[i] >> bit & 1), None)
        if p is None: continue
        rows[rk], rows[p] = rows[p], rows[rk]
        for i in range(len(rows)):
            if i != rk and rows[i] >> bit & 1: rows[i] ^= rows[rk]
        rk += 1
    return rk
for path in sys.argv[1:]:
    c = json.load(gzip.open(path))
    fr = [tuple(f) for f in c["frames"]]
    used = set(c["start"]) | set(c["final"]) | {g[1] for g in c["A"] + c["B"]}
    res = Counter()
    for i in used:
        b = fr[i]
        if not b:
            res["zero"] += 1; continue
        gram = [sum((par(u & w)) << j for j, w in enumerate(b)) for u in b]
        nd = rank2(gram) == len(b)
        odd = any(par(u) for u in b)
        res["non-degenerate with an odd vector" if nd and odd else "non-degenerate, all even" if nd else "DEGENERATE"] += 1
    print(path.split("/")[-1], "frames used:", len(used), dict(res))
