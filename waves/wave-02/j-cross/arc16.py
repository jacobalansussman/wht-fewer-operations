#!/usr/bin/env python3
# j-cross / arc16.py : e-0's half-arc null spaces at 16 points, exactly, and a test of the subfield explanation.
# c[m] = (-1)^Trace(theta^m), m mod 15.  Hankel block: rows i = 0..7, columns j = 0..7, entry c[start + i + j].
# A null vector v is an input on the arc {theta^(start+j)} whose transform vanishes at theta^0..theta^7.
from fractions import Fraction as F
import sys
def field(k, p):
    n = (1 << k) - 1; pw = [1]
    for _ in range(n - 1):
        v = pw[-1] << 1
        if v >> k: v ^= p
        pw.append(v)
    lg = {v: i for i, v in enumerate(pw)}
    def mul(a, b): return 0 if a == 0 or b == 0 else pw[(lg[a] + lg[b]) % n]
    def tr(v):
        s = 0; w = v
        for _ in range(k): s ^= w; w = mul(w, w)
        return s
    return n, pw, lg, mul, tr
def nullspace(M):
    M = [[F(x) for x in r] for r in M]; rows = len(M); cols = len(M[0]); piv = []; r = 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; M[r] = [a / M[r][c] for a in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
    free = [c for c in range(cols) if c not in piv]; out = []
    for fc in free:
        v = [F(0)] * cols; v[fc] = F(1)
        for i, pc in enumerate(piv): v[pc] = -M[i][fc]
        out.append(v)
    return out
for k, p in ((4, 0b10011), (6, 0b1000011)):
    n, pw, lg, mul, tr = field(k, p); c = [1 - 2 * tr(v) for v in pw]; h = (n + 1) // 2; q = 1 << (k // 2)
    print('k=%d  c =' % k, ''.join('+' if x == 1 else '-' for x in c), ' subfield exponents: multiples of', q + 1)
    # T(m) = trace down to the subfield of theta^m, as a subfield element (0 or an exponent multiple of q+1)
    def trq(v):
        w = v; s = v
        for _ in range(k // 2): w = mul(w, w)      # w = v^q
        return v ^ w
    nsing = 0
    for st in range(n):
        M = [[c[(st + i + j) % n] for j in range(h)] for i in range(h)]
        ns = nullspace(M)
        if not ns: continue
        nsing += 1
        if k == 4 or nsing <= 3:
            for v in ns:
                den = 1
                supp = [(st + j) % n for j in range(h) if v[j] != 0]
                # sums of v over the classes of exponents modulo q+1 (cosets of the subfield's units = rays) and modulo q-1 (circles)
                ray = {}; cir = {}
                for j in range(h):
                    m = (st + j) % n
                    ray[m % (q + 1)] = ray.get(m % (q + 1), 0) + v[j]; cir[m % (q - 1)] = cir.get(m % (q - 1), 0) + v[j]
                # the full transform of the input on all n+1 points
                x = [F(0)] * (n + 1)
                for j in range(h): x[pw[(st + j) % n]] = v[j]
                y = [sum(x[a] * (-1) ** bin(a & b).count('1') for a in range(n + 1)) for b in range(n + 1)]
                # with the trace form: y at theta^i = sum_m v_m c[i+m]; print where it vanishes in exponent order
                yt = [sum(v[j] * c[(st + j + i) % n] for j in range(h)) for i in range(n)]
                y0 = sum(v)
                print('  start %2d lost %d | v = %s' % (st, len(ns), ' '.join(str(z) for z in v)))
                print('      support exponents %s | sums over rays (mod %d): %s | over circles (mod %d): %s'
                      % (supp, q + 1, [str(ray.get(r, 0)) for r in range(q + 1)], q - 1, [str(cir.get(r, 0)) for r in range(q - 1)]))
                print('      transform at exponents 0..%d: %s | at the origin: %s | zeros: %d of %d'
                      % (n - 1, ' '.join(str(z) for z in yt), y0, sum(1 for z in yt if z == 0) + (y0 == 0), n + 1))
    print('  singular starting points: %d of %d' % (nsing, n))
