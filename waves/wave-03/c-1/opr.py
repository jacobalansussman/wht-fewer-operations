#!/usr/bin/env python3
"""c-1 (critic): e2-0's family in count (O): every line is  t = u + v,  t = u - v  or  t = c * u, each charged ONE.
Written from my own derivation, not from e2-0-pieces/oslp.py.  Scale rule: a wire whose support is 2^j is held as 2^(-floor(j/2)) times
its true value; a hub is held at the scale of its two inputs.  Then (my derivation)
   j odd : P = +-M +- W           (no multiplication)
   j even: Mh = (1/2) * M, P = +-Mh +- W     (one halving per hub, shared by the pieces made from that hub)
   top level, k odd: the second output of each kind needs 2*A (one doubling per half piece)
Two targets are priced: (a) H x / 2^floor(k/2)  (b) H x exactly = (a) plus N multiplications by 2^floor(k/2).
Replay is exact: every value is stored times 2^floor(k/2) as an integer; a halving asserts that every entry is even.
usage: opr.py kmin kmax"""
import sys
try:
    import numpy as np
except ImportError:
    np = None

def build(k):
    N = 1 << k
    ops = []           # ('+',u,v) ('-',u,v) ('h',u) halve ('d',u) double ('s',u) multiply by 2^floor(k/2)
    def op(*t): ops.append(t); return N + len(ops) - 1
    def comb(su, u, sv, v):          # su*u + sv*v with signs, never both negative
        if su > 0 and sv > 0: return op('+', u, v)
        if su > 0: return op('-', u, v)
        assert sv > 0, 'a gate -u-v'
        return op('-', v, u)
    def D(lo, m, e, j):
        if m == 2: return [comb(1, lo, e, lo + 1)], [lo]
        h = m // 2; q = m // 4
        PL, WL = D(lo, h, 1, j - 1); PR, WR = D(lo + h, h, -1, j - 1)
        P = [None] * h
        for g in range(q):
            tau = 1 if 8 * g < m else -1
            c = -e * tau
            M = comb(1, PL[g], c, PR[g])
            if j % 2 == 0: M = op('h', M)
            P[g] = comb(1, M, e, WR[g])
            P[g + q] = comb(-tau, M, tau, WL[g])
        return P, PL + PR
    h = N // 2; q = N // 4; outs = []
    PL, WL = D(0, h, 1, k - 1); PR, WR = D(h, h, -1, k - 1)
    dbl = {}
    def two(u):
        if k % 2 == 0: return u
        if u not in dbl: dbl[u] = op('d', u)
        return dbl[u]
    for g in range(q):
        tau = 1 if 8 * g < N else -1
        s = -tau
        M = comb(1, PL[g], 1, PR[g])
        if k % 2 == 0: M = op('h', M)
        fa = comb(1, M, s, WR[g]); oa = comb(-1, fa, 1, two(PL[g]))
        fb = comb(-tau, M, tau, WL[g]); ob = comb(1, fb, -s, two(PR[g]))
        outs += [fa, oa, fb, ob]
    return ops, outs

def check(k, ops, outs, exact):
    """exact integer replay.  values are stored times S = 2^floor(k/2).  returns counts by type."""
    N = 1 << k; S = 1 << (k // 2)
    ops = list(ops); outs = list(outs)
    if exact:
        new = []
        for o in outs: ops.append(('s', o)); new.append(N + len(ops) - 1)
        outs = new
    cnt = {}
    if np is not None:
        V = np.zeros((N + len(ops), N), dtype=np.int64); V[np.arange(N), np.arange(N)] = S
    else:
        V = [[S if i == j else 0 for j in range(N)] for i in range(N)]
    for i, t in enumerate(ops):
        cnt[t[0]] = cnt.get(t[0], 0) + 1
        for u in t[1:]: assert u < N + i
        if np is not None:
            if t[0] == '+': r = V[t[1]] + V[t[2]]
            elif t[0] == '-': r = V[t[1]] - V[t[2]]
            elif t[0] == 'h':
                assert not (V[t[1]] & 1).any(), 'a halving of an odd numerator'; r = V[t[1]] >> 1
            elif t[0] == 'd': r = 2 * V[t[1]]
            else: r = S * V[t[1]]
            V[N + i] = r
        else:
            if t[0] == '+': r = [a + b for a, b in zip(V[t[1]], V[t[2]])]
            elif t[0] == '-': r = [a - b for a, b in zip(V[t[1]], V[t[2]])]
            elif t[0] == 'h':
                assert all(a % 2 == 0 for a in V[t[1]]), 'a halving of an odd numerator'; r = [a // 2 for a in V[t[1]]]
            elif t[0] == 'd': r = [2 * a for a in V[t[1]]]
            else: r = [S * a for a in V[t[1]]]
            V.append(r)
    if np is not None: assert np.abs(V).max() < 2 ** 40
    want = S if exact else 1          # stored value of an entry of the output: (true value) * S
    seen = set()
    for o in outs:
        v = [int(a) for a in V[o]]
        assert v[0] == want
        w = sum(1 << i for i in range(k) if v[1 << i] == -want)
        assert v == [want * (1 - 2 * (bin(w & x).count('1') & 1)) for x in range(N)], 'an output is not a row'
        seen.add(w)
    assert len(seen) == N and len(outs) == N
    return cnt

if __name__ == '__main__':
    for k in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        N = 1 << k
        ops, outs = build(k)
        ca = check(k, ops, outs, False); cb = check(k, ops, outs, True)
        ta = sum(ca.values()); tb = sum(cb.values())
        addsub = ca.get('+', 0) + ca.get('-', 0)
        if k % 2 == 0: fa = 7 * N * k // 8 + N // 4; fb = fa + N
        else: fa = (7 * N * k + 5 * N) // 8; fb = fa + N
        print('k %2d N %5d | (a) H x / %d: %6d operations = %d add/sub + %d halvings + %d doublings; my formula %d %s | (b) H x exactly: %6d (formula %d %s) | textbook for H x: %6d | (b) - textbook = %+d'
              % (k, N, 1 << (k // 2), ta, addsub, ca.get('h', 0), ca.get('d', 0), fa, 'EQUAL' if fa == ta else 'DIFFERENT', tb, fb, 'EQUAL' if fb == tb else 'DIFFERENT', N * k, tb - N * k), flush=True)
