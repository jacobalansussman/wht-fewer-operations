#!/usr/bin/env python3
"""h-6-classhub / gen_mixed.py : the staircase for a tensor product of k DIFFERENT kernels, [[1,1],[1,tau_j]] on address bit j.  Count (G).
usage: gen_mixed.py tau_0 tau_1 ... tau_(k-1)   (rationals; bit 0 is the lowest address bit).  Hub rule: c = tau_top^e * tau_next^(top - 1).
(derived from gen_tau.py; the text below is gen_tau.py's)
Target: the N = 2^k rows of K^(tensor k), row w has entry tau^(number of common 1-bits of w and x) at input x.
Rule found by hand (h-6.md section 1): hub M = A + c*B with c = tau^(e - 1 + top), e = the extension asked of this node (0 or 1),
top = top bit of the quarter character gamma; at tau = -1 this is gen.py's sign rule.
usage: gen_tau.py k tauspec [print]     tauspec: sym | p/q | i | w3 | w6 | s7
Replays from scratch in the same exact arithmetic: every output must EQUAL its row (factor 1)."""
import sys
from field import parse_tau
def build(k, taus, verbose=False):
    import math
    N = 1 << k; tau = taus[0]; one = tau ** 0; zero = one - one
    def tpow(w, x):
        r = one
        for j in range(k):
            if (w >> j) & (x >> j) & 1: r = r * taus[j]
        return r
    lg = lambda m: m.bit_length() - 1
    def bits(w): return bin(w).count('1')
    def piece(w, idxs, scal=None):
        v = [zero] * N
        for pos, i in enumerate(idxs): v[i] = tpow(w, pos) * (one if scal is None else scal)
        return tuple(v)
    vec = {('x', i): tuple(one if i == j else zero for j in range(N)) for i in range(N)}
    prog = []
    def solve2(u, v, p):
        for i in range(N):
            for j in range(i + 1, N):
                det = u[i] * v[j] - u[j] * v[i]
                if det:
                    a = (p[i] * v[j] - p[j] * v[i]) / det; b = (u[i] * p[j] - u[j] * p[i]) / det
                    return (a, b) if all(a * u[t] + b * v[t] == p[t] for t in range(N)) else None
        return None
    cnt = [0]
    def gate(target, n1, n2, kind):
        s = solve2(vec[n1], vec[n2], target)
        if s is None or not s[0] or not s[1]: return None
        cnt[0] += 1; nm = (kind, cnt[0]); vec[nm] = target; prog.append((nm, s[0], n1, s[1], n2)); return nm
    def cat(*vs): return tuple(sum(c[1:], c[0]) for c in zip(*vs))
    def D(idxs, e):
        m = len(idxs); L, R = idxs[:m // 2], idxs[m // 2:]
        if m == 2:
            return {'P': {0: gate(cat(piece(0, L), piece(0, R, taus[0] ** e)), ('x', L[0]), ('x', R[0]), 'p')}, 'W': {}}
        DL = D(L, 0); DR = D(R, 1); P = {}; W = {}
        for g in range(m // 4):
            a, b = g, g + m // 4
            A, B = DL['P'][g], DR['P'][g]
            top = 0 if (m == 4 or g < m // 8) else 1
            c = (taus[lg(m) - 1] ** e) * (taus[lg(m) - 2] ** (top - 1))
            M = gate(cat(vec[A], tuple(c * t for t in vec[B])), A, B, 'hub'); assert M
            wR = DR['W'][g] if m >= 8 else ('x', R[0]); wL = DL['W'][g] if m >= 8 else ('x', L[0])
            P[a] = gate(cat(piece(a, L), piece(a, R, taus[lg(m) - 1] ** e)), M, wR, 'p'); assert P[a], ('Pa', m, g)
            P[b] = gate(cat(piece(b, L), piece(b, R, taus[lg(m) - 1] ** e)), M, wL, 'p'); assert P[b], ('Pb', m, g)
            W[a] = A; W[b] = B
        return {'P': P, 'W': W}
    def top_(idxs):
        m = len(idxs); L, R = idxs[:m // 2], idxs[m // 2:]
        DL = D(L, 0); DR = D(R, 1)
        for g in range(m // 4):
            a, b = g, g + m // 4
            A, B = DL['P'][g], DR['P'][g]
            top = 0 if (m == 4 or g < m // 8) else 1; c = taus[lg(m) - 2] ** (top - 1)     # e = 0 at the top level
            M = gate(cat(vec[A], tuple(c * t for t in vec[B])), A, B, 'hub')
            for ch, wit, own in ((a, DR['W'][g] if m >= 8 else None, A), (b, DL['W'][g] if m >= 8 else None, B)):
                first = None
                for e in (0, 1):
                    tgt = cat(piece(ch, L), piece(ch, R, taus[lg(m) - 1] ** e))
                    for wn in ([wit] if wit else [('x', i) for i in idxs]):
                        first = gate(tgt, M, wn, 'y')
                        if first: break
                    if first: break
                assert first, ('top', g, ch)
                other = cat(piece(ch, L), piece(ch, R, taus[lg(m) - 1] ** (1 - e)))
                assert gate(other, first, own, 'y')
    top_(list(range(N)))
    # exact replay from scratch
    val = {('x', i): [one if i == j else zero for j in range(N)] for i in range(N)}
    for nm, a, u, b, v in prog: val[nm] = [a * s + b * t for s, t in zip(val[u], val[v])]
    rows = {tuple(tpow(w, x) for x in range(N)): w for w in range(N)}
    got = set()
    for nm, a, u, b, v in prog:
        assert tuple(val[nm]) == vec[nm]
        if nm[0] == 'y':
            t = tuple(val[nm]); assert t in rows, 'an output is not exactly a row'; got.add(rows[t])
    ok = got == set(range(N)) and len(rows) == N
    return prog, vec, ok
if __name__ == '__main__':
    from fractions import Fraction as F
    taus = [F(t) for t in sys.argv[1:]]; k = len(taus); N = 1 << k
    prog, vec, ok = build(k, taus)
    print('N', N, 'taus (bit 0 first)', [str(t) for t in taus], 'gates', len(prog), 'formula (3/4) N log2 N + N/4 =', 3 * N * k // 4 + N // 4, 'textbook', N * k, 'all outputs exact:', ok)
