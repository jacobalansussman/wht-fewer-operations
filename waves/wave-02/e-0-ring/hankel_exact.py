#!/usr/bin/env python3
# e-0-ring / hankel_exact.py : the Hankel ranks at k = 4 and k = 6 redone in exact rational arithmetic, every starting point.
from fractions import Fraction as F
def seq(k, p):
    n = (1 << k) - 1; pw = [1]
    for _ in range(n - 1):
        v = pw[-1] << 1
        if v >> k: v ^= p
        pw.append(v)
    lg = {v: i for i, v in enumerate(pw)}
    def mul(a, b): return 0 if a == 0 or b == 0 else pw[(lg[a] + lg[b]) % n]
    out = []
    for v in pw:
        s = 0; w = v
        for _ in range(k): s ^= w; w = mul(w, w)
        out.append(1 - 2 * s)
    return out
def rank(M):
    M = [[F(x) for x in r] for r in M]; r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(r + 1, len(M)):
            if M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
for k, p in ((3, 0b1011), (4, 0b10011), (5, 0b100101), (6, 0b1000011)):
    c = seq(k, p); n = len(c); h = (n + 1) // 2
    lost = []
    for s in range(n):
        r = rank([[c[(s + i + j) % n] for j in range(h)] for i in range(h)])
        if r < h: lost.append((s, h - r))
    print("k=%d poly %s EXACT: %d of %d starting points singular: %s" % (k, bin(p), len(lost), n, lost), flush=True)
