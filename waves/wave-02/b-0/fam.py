#!/usr/bin/env python3
"""b-0: my own generator and exact checker for the mixed-hub family (shares no code with e2-0's gen.py / oslp.py / ocheck.py).
Coefficients are written down from my own derivation (no linear solving).  Exact integer arithmetic throughout (numpy int64,
values of count-(G) nodes are checked to lie in {-1,0,1}; count-(O) values are carried multiplied by 2^K and every halving is
checked to divide exactly).
usage: fam.py kmin kmax [dump]"""
import sys, numpy as np
def build(k):
    N = 1 << k
    gates = []          # (a, u, b, v): node = a*u + b*v ; node ids: 0..N-1 inputs, then N + index
    kind = []           # 'p' piece / 'h' hub / 'y' output ; level j (support 2^j)
    def g(a, u, b, v, kd, lev):
        gates.append((a, u, b, v)); kind.append((kd, lev)); return N + len(gates) - 1
    def D(lo, m, e, lev):
        # returns P[alpha], W[alpha], alpha in [0, m/2)
        if m == 2:
            return [g(1, lo, e, lo + 1, 'p', 1)], [lo]
        h = m // 2
        PL, WL = D(lo, h, +1, lev - 1); PR, WR = D(lo + h, h, -1, lev - 1)
        P = [None] * h; W = [None] * h
        for gam in range(m // 4):
            tau = 1 if 8 * gam < m else -1
            c = -e * tau
            A, B = PL[gam], PR[gam]
            M = g(1, A, c, B, 'h', lev)
            P[gam] = g(1, M, 2 * e, WR[gam], 'p', lev)
            P[gam + m // 4] = g(-tau, M, 2 * tau, WL[gam], 'p', lev)
            W[gam] = A; W[gam + m // 4] = B
        return P, W
    h = N // 2
    PL, WL = D(0, h, +1, k - 1); PR, WR = D(h, h, -1, k - 1)
    outs = []
    for gam in range(N // 4):
        tau = 1 if 8 * gam < N else -1
        A, B = PL[gam], PR[gam]
        M = g(1, A, 1, B, 'h', k)
        if tau == 1:
            am = g(1, M, -2, WR[gam], 'y', k); ap = g(2, A, -1, am, 'y', k)
            bm = g(2, WL[gam], -1, M, 'y', k); bp = g(1, bm, 2, B, 'y', k)
        else:
            ap = g(1, M, 2, WR[gam], 'y', k); am = g(2, A, -1, ap, 'y', k)
            bp = g(1, M, -2, WL[gam], 'y', k); bm = g(1, bp, -2, B, 'y', k)
        outs += [ap, am, bp, bm]
    return N, gates, kind, outs
def checkG(N, gates, outs):
    val = np.zeros((N + len(gates), N), dtype=np.int8)
    val[np.arange(N), np.arange(N)] = 1
    for i, (a, u, b, v) in enumerate(gates):
        t = a * val[u].astype(np.int64) + b * val[v].astype(np.int64)
        assert np.abs(t).max() <= 1, 'value outside {-1,0,1}'
        val[N + i] = t
    seen = set(); x = np.arange(N)
    for o in outs:
        r = val[o].astype(np.int64); assert r[0] == 1
        w = sum((1 << i) for i in range(N.bit_length() - 1) if r[1 << i] == -1)
        par = np.zeros(N, dtype=np.int64); y = w & x
        while y.any(): par ^= (y & 1); y >>= 1
        assert (r == 1 - 2 * par).all(), 'output is not a row of H'; seen.add(w)
    assert seen == set(range(N)) and len(outs) == N
    return val
def toO(N, k, gates, kind, outs, target):
    """count (O): every line is add, sub or scale-by-constant, each charged 1.  Node of support 2^j stored times 2^-floor(j/2);
    a hub stored at the scale of its two pieces.  target: exponent t so that outputs are H / 2^t (extra multiplications at the end if needed)."""
    s = [0] * N
    for (kd, lev) in kind: s.append((lev - 1) // 2 if kd == 'h' else lev // 2)
    ops = []; cache = {}
    def scaled(u, d):            # node holding 2^d * stored(u)
        if d == 0: return ('n', u)
        if (u, d) not in cache: ops.append(('scale', d, ('n', u))); cache[(u, d)] = ('m', len(ops) - 1)
        return cache[(u, d)]
    ref = {}
    for i, (a, u, b, v) in enumerate(gates):
        t = N + i
        du = (abs(a).bit_length() - 1) + s[u] - s[t]; dv = (abs(b).bit_length() - 1) + s[v] - s[t]
        U = scaled(u, du); V = scaled(v, dv)
        if a > 0 and b > 0: ops.append(('add', U, V))
        elif a > 0: ops.append(('sub', U, V))
        elif b > 0: ops.append(('sub', V, U))
        else: raise SystemExit('gate -u-v')
        ref[t] = len(ops) - 1
    fin = []
    for o in outs:
        d = s[o] - target
        if d == 0: fin.append(('g', ref[o]))
        else: ops.append(('scale', d, ('g', ref[o]))); fin.append(('g', len(ops) - 1))
    return ops, fin, ref
def checkO(N, k, ops, fin, ref, target):
    K = k + 2
    val = {}
    def get(r):
        if r[0] == 'n': return (np.int64(1) << K) * (np.arange(N) == r[1]).astype(np.int64) if r[1] < N else store[ref[r[1]]]
        return store[r[1]]
    store = [None] * len(ops)
    for i, op in enumerate(ops):
        if op[0] == 'scale':
            x = get(op[2]); d = op[1]
            if d > 0: store[i] = x << d
            else:
                assert (x % (1 << -d) == 0).all(), 'halving not exact'; store[i] = x >> (-d)
        elif op[0] == 'add': store[i] = get(op[1]) + get(op[2])
        else: store[i] = get(op[1]) - get(op[2])
    x = np.arange(N); seen = set()
    for f in fin:
        r = store[f[1]]; unit = np.int64(1) << (K - target) if K >= target else None
        assert (r % unit == 0).all(); r = r // unit
        w = sum((1 << i) for i in range(k) if r[1 << i] == -1)
        par = np.zeros(N, dtype=np.int64); y = w & x
        while y.any(): par ^= (y & 1); y >>= 1
        assert (r == 1 - 2 * par).all(); seen.add(w)
    assert seen == set(range(N))
    c = {'add': 0, 'sub': 0, 'scale': 0}
    for op in ops: c[op[0]] += 1
    consts = sorted({op[1] for op in ops if op[0] == 'scale'})
    return c, consts
if __name__ == '__main__':
    kmin, kmax = int(sys.argv[1]), int(sys.argv[2])
    for k in range(kmin, kmax + 1):
        N, gates, kind, outs = build(k)
        checkG(N, gates, outs)
        coefs = sorted({abs(c) for (a, u, b, v) in gates for c in (a, b)})
        nh = sum(1 for kd, _ in kind if kd == 'h')
        print('G  N=%d k=%d gates=%d formula(3/4 N k + N/4)=%s textbook=%d ratio=%.4f |coef|=%s hubs=%d  all %d outputs exact rows of H: True'
              % (N, k, len(gates), 3 * N * k / 4 + N / 4, N * k, len(gates) / (N * k), coefs, nh, N), flush=True)
        for target, nm in ((k // 2, 'H/2^%d' % (k // 2)), (0, 'H itself')):
            ops, fin, ref = toO(N, k, gates, kind, outs, target)
            if N <= 4096:
                c, consts = checkO(N, k, ops, fin, ref, target); ok = 'exact check passed'
            else:
                c = {'add': 0, 'sub': 0, 'scale': 0}
                for op in ops: c[op[0]] += 1
                consts = sorted({op[1] for op in ops if op[0] == 'scale'}); ok = 'counted only'
            print('   O  %-9s ops=%d (add %d sub %d scale %d, scale exponents %s) 7/8 N k + N/4 = %s  textbook N k = %d  [%s]'
                  % (nm, len(ops), c['add'], c['sub'], c['scale'], consts, 7 * N * k / 8 + N / 4, N * k, ok), flush=True)
