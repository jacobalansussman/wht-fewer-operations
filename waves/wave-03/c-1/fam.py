#!/usr/bin/env python3
"""c-1 (critic): my own generator and my own replay of e2-0's 'mixed hub' family.  Shares no code with e2-0-pieces/gen.py.
Coefficients are written from my own hand derivation (closed form, no 2x2 solving):
  cube of size m, halves L, R, quarter character g, tau = +1 if g < m/8 else -1, e = sign asked, c = -e*tau
    M        = A + c*B                       A = (y_g on L), B = (y_g on RL, -y_g on RR)
    P[g]     = M + 2e*WR[g]                  WR[g] = y_g on RL (tau=+1) or on RR (tau=-1): a piece made two levels down
    P[g+m/4] = -tau*M + 2*tau*WL[g]          WL[g] = y_g on LL (tau=+1) or on LR (tau=-1)
  top: M = A + B, s = -tau:  first_a = M + 2s*WR, other_a = -first_a + 2A ; first_b = -tau*M + 2tau*WL, other_b = first_b - 2s*B
Count (G): one gate per line a*u + b*v.
Replay: exact integer arithmetic (all coefficients are integers) on the N unit vectors, numpy int32, with an overflow guard;
every output must equal a row of the Sylvester matrix H, and the N outputs must be N different rows.
usage: fam.py kmin kmax [write]"""
import sys
try:
    import numpy as np
except ImportError:
    np = None

def build(k):
    N = 1 << k
    prog = []                      # (a, u, b, v): node index = N + position; inputs are 0..N-1
    kind = []
    def gate(a, u, b, v, kd):
        prog.append((a, u, b, v)); kind.append(kd); return N + len(prog) - 1
    def D(lo, m, e):
        """returns (P, W): P[g] for g < m/2 = the piece (y_g on L, e*y_g on R) of the cube [lo, lo+m); W[g] = y_g on a half."""
        if m == 2:
            return [gate(1, lo, e, lo + 1, 'p')], [lo]
        h = m // 2; q = m // 4
        PL, WL = D(lo, h, 1); PR, WR = D(lo + h, h, -1)
        P = [None] * h
        for g in range(q):
            tau = 1 if 8 * g < m else -1
            c = -e * tau
            M = gate(1, PL[g], c, PR[g], 'hub')
            P[g] = gate(1, M, 2 * e, WR[g], 'p')
            P[g + q] = gate(-tau, M, 2 * tau, WL[g], 'p')
        return P, PL + PR
    h = N // 2; q = N // 4
    PL, WL = D(0, h, 1); PR, WR = D(h, h, -1)
    for g in range(q):
        tau = 1 if 8 * g < N else -1
        s = -tau
        M = gate(1, PL[g], 1, PR[g], 'hub')
        fa = gate(1, M, 2 * s, WR[g], 'y'); gate(-1, fa, 2, PL[g], 'y')
        fb = gate(-tau, M, 2 * tau, WL[g], 'y'); gate(1, fb, -2 * s, PR[g], 'y')
    return prog, kind

def replay(k, prog, kind):
    if np is None: return replay_pure(k, prog, kind)
    N = 1 << k
    V = np.zeros((N + len(prog), N), dtype=np.int32)
    V[np.arange(N), np.arange(N)] = 1
    for i, (a, u, b, v) in enumerate(prog):
        assert u < N + i and v < N + i and a != 0 and b != 0
        V[N + i] = a * V[u] + b * V[v]
    assert np.abs(V).max() < 2 ** 20          # no overflow anywhere: int32 arithmetic was exact
    outs = [N + i for i, kd in enumerate(kind) if kd == 'y']
    assert len(outs) == N
    x = np.arange(N)
    seen = set()
    for o in outs:
        v = V[o]
        assert v[0] == 1, 'an output does not start with +1'
        w = 0
        for i in range(k):
            if v[1 << i] == -1: w |= 1 << i
        par = x & w
        for sh in (16, 8, 4, 2, 1): par = par ^ (par >> sh)
        row = 1 - 2 * (par & 1)
        assert (v == row).all(), 'an output is not a row of H'
        seen.add(w)
    assert len(seen) == N, 'rows repeated'
    supp = {}
    for i, kd in enumerate(kind):
        if kd != 'y':
            s = int((V[N + i] != 0).sum()); supp[s] = supp.get(s, 0) + 1
    return int(np.abs(V).max()), sorted(supp.items())

def replay_pure(k, prog, kind):
    """the same with Python integers only (unbounded, so exact with no guard needed)"""
    N = 1 << k
    V = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
    for i, (a, u, b, v) in enumerate(prog):
        assert u < N + i and v < N + i and a != 0 and b != 0
        U = V[u]; W = V[v]
        V.append([a * s + b * t for s, t in zip(U, W)])
    outs = [N + i for i, kd in enumerate(kind) if kd == 'y']
    assert len(outs) == N
    seen = set()
    for o in outs:
        v = V[o]
        assert v[0] == 1, 'an output does not start with +1'
        w = 0
        for i in range(k):
            if v[1 << i] == -1: w |= 1 << i
        assert v == [1 - 2 * (bin(w & x).count('1') & 1) for x in range(N)], 'an output is not a row of H'
        seen.add(w)
    assert len(seen) == N, 'rows repeated'
    supp = {}; mx = 0
    for i, kd in enumerate(kind):
        r = V[N + i]; mx = max(mx, max(abs(t) for t in r))
        if kd != 'y':
            s = sum(1 for t in r if t); supp[s] = supp.get(s, 0) + 1
    return mx, sorted(supp.items())

if __name__ == '__main__':
    kmin, kmax = int(sys.argv[1]), int(sys.argv[2])
    for k in range(kmin, kmax + 1):
        N = 1 << k
        prog, kind = build(k)
        G = len(prog); form = 3 * N * k // 4 + N // 4
        coefs = sorted({abs(c) for a, u, b, v in prog for c in (a, b)})
        if k <= 13:
            mx, supp = replay(k, prog, kind)
            chk = 'all %d outputs are exactly the %d rows of H (each once); largest |entry| on any wire %d' % (N, N, mx)
        else:
            chk = 'not replayed'; supp = []
        print('k %2d N %5d gates(G) %6d  formula 3/4 N k + N/4 = %6d  %s  textbook %6d ratio %.4f | |coef| %s | %s | helpers by support %s'
              % (k, N, G, form, 'EQUAL' if G == form else 'DIFFERENT', N * k, G / (N * k), coefs, chk, supp if k <= 7 else '(omitted)'), flush=True)
        if len(sys.argv) > 3 and k <= 6:
            with open('waves/wave-03/c-1/mine_%d.txt' % N, 'w') as f:
                nm = lambda t: 'x%d' % t if t < N else 'n%d' % (t - N + 1)
                for i, (a, u, b, v) in enumerate(prog): f.write('%s = %d * %s + %d * %s   # %s\n' % (nm(N + i), a, nm(u), b, nm(v), kind[i]))
