# x-4, exact checks for the "flag depth" reading of the third turn. Whole numbers and fractions only.
# H(x,y) = (-1)^B(x,y) = d(x) chi(x+y) d(y), chi = (-1)^Q: the transform is an XOR-convolution with a chirp between two free sign changes.
# A "flag kernel" is K(x,y) = f(x+y) with f = sum_j c_j [u in M_j] for a chain M_0 = {0} < M_1 < ... (running sums up a merge tree,
# weights, and down the same tree).
import sys, itertools
from fractions import Fraction as Fr

def pop(v): return bin(v).count('1')

def rank_fr(rows):
    M = [[Fr(v) for v in r] for r in rows]; rk = 0
    for c in range(len(M[0])):
        p = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c] / M[rk][c]; M[i] = [a - f*b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk

def part1(n):
    k = 2*n; N = 1 << k; s = 1 << n
    def Q(x): return sum(((x >> (2*i)) & 1) & ((x >> (2*i+1)) & 1) for i in range(n)) & 1
    H = [[(-1)**((Q(x ^ y) + Q(x) + Q(y)) & 1) for y in range(N)] for x in range(N)]
    # circuit: wires are rows over the N inputs; count gates (G): one gate = a*u + b*v
    W = [[(-1)**Q(x) if y == x else 0 for y in range(N)] for x in range(N)]   # after the free sign change D
    gates = 0
    def lin(a, u, b, v): return [a*p + b*q for p, q in zip(u, v)]
    for i in range(n):
        m = (1 << (2*i)) | (1 << (2*i+1))          # M_1 = {0, m}
        e = 1 << (2*i)                              # M_2 = M_1 + {0, e}
        S1 = {}; S2 = {}
        for x in range(N):
            c1 = min(x, x ^ m)
            if c1 not in S1: S1[c1] = lin(1, W[c1], 1, W[c1 ^ m]); gates += 1
        for c1 in list(S1):
            c2 = min(c1, min(c1 ^ e, c1 ^ e ^ m))
            if c2 not in S2:
                other = min(c2 ^ e, c2 ^ e ^ m)
                S2[c2] = lin(1, S1[c2], 1, S1[other]); gates += 1
        Y1 = {}
        for c1 in S1:
            c2 = min(c1, min(c1 ^ e, c1 ^ e ^ m))
            Y1[c1] = lin(-2, S1[c1], 1, S2[c2]); gates += 1          # c_1 = -2, c_2 = 1
        Wn = []
        for x in range(N):
            Wn.append(lin(2, W[x], 1, Y1[min(x, x ^ m)])); gates += 1  # c_0 = 2
        W = Wn
    out = [[(-1)**Q(x) * v for v in W[x]] for x in range(N)]
    print('N=%d: H = D K_1 ... K_%d D with %d flag kernels (each f = 2[0] - 2[M_1] + [M_2] on one pair of bits): %s ; gates (G) of this plain program: %d = (9/4) N x %d ; textbook %d'
          % (N, n, n, out == H, gates, n, N*k))
    return H

def mech():
    # the mechanism of the depth-2 lemma on the 16-point solution: (1 - tau_1) E0 T E2 (1 - tau_2) = a b (1 - tau_1) D1 (1 - tau_2)
    n = 2; k = 4; N = 16
    def Q(x): return sum(((x >> (2*i)) & 1) & ((x >> (2*i+1)) & 1) for i in range(n)) & 1
    T = [[(-1)**((Q(x ^ y) + Q(x) + Q(y)) & 1) for y in range(N)] for x in range(N)]
    e0 = [(-1)**Q(x) for x in range(N)]; e2 = e0; m1 = 0b0011; m2 = 0b1100; a = b = 2
    A = [[e0[x]*T[x][y]*e2[y] for y in range(N)] for x in range(N)]
    L = [[A[x][y] - A[x ^ m1][y] - A[x][y ^ m2] + A[x ^ m1][y ^ m2] for y in range(N)] for x in range(N)]
    def dl(u, v): return 1 if u == v else 0
    Rr = [[a*b*(dl(x, y) - dl(x, y ^ m2) - dl(x ^ m1, y) + dl(x ^ m1, y ^ m2)) for y in range(N)] for x in range(N)]
    print('16 points, the known depth-2 solution: (1-tau1) E0 T E2 (1-tau2) = a b (1-tau1)(1-tau2):', L == Rr)

def csp(k, beta, m1, m2):
    """case beta(m1,m2) = 0: count the solutions of  [p(x) = chi(y)] or [q(y) = psi(x)]  for all y not in x + span(m1,m2),
    p, q with values +1, -1 or 'other' (2 = any real number that is not +-1); p(x+m1) = 1/p(x), q(y+m2) = 1/q(y)."""
    N = 1 << k
    chi = [(-1)**beta(m1, y) for y in range(N)]; psi = [(-1)**beta(x, m2) for x in range(N)]
    S = {0, m1, m2, m1 ^ m2}
    sols = []
    p = [None]*N
    dom = [set((1, -1, 2)) for _ in range(N)]
    def rec(x, dom):
        if x == N:
            cnt = 1
            for y in range(N): cnt *= len(dom[y])
            sols.append((tuple(p), cnt, tuple(tuple(sorted(dq)) for dq in dom))); return
        if p[x] is not None: return rec(x + 1, dom)
        for v in (1, -1, 2):
            p[x] = v; p[x ^ m1] = v     # +-1 are their own inverses; 'other' stays 'other'
            nd = [set(dq) for dq in dom]; ok = True
            for xx in (x, x ^ m1):
                for y in range(N):
                    if (xx ^ y) in S: continue
                    if v != chi[y]:
                        nd[y] &= {psi[xx]}
                        if not nd[y]: ok = False; break
                if not ok: break
            if ok: rec(x + 1, nd)
            p[x] = None; p[x ^ m1] = None
    rec(0, dom)
    tot = sum(c for _, c, _ in sols)
    char = 0
    for pp, c, dq in sols:
        for eta in (1, -1):
            if all(pp[x] == eta*psi[x] for x in range(N)) and all(dq[y] == (-eta*chi[y],) for y in range(N)): char += 1
    return tot, char

def rank_block(k):
    N = 1 << k
    T = [[(-1)**pop(x & y) for y in range(N)] for x in range(N)]
    res = set()
    for lam in range(1, N):
        X = [x for x in range(N) if pop(x & lam) % 2 == 0]; Y = [y for y in range(N) if pop(y & lam) % 2 == 1]
        res.add(rank_fr([[T[x][y] for y in Y] for x in X]))
    return sorted(res)

if __name__ == '__main__':
    for n in (1, 2, 3): part1(n)
    mech()
    dot = lambda x, y: pop(x & y) & 1
    def symp(n):
        def Q(x): return sum(((x >> (2*i)) & 1) & ((x >> (2*i+1)) & 1) for i in range(n)) & 1
        return lambda x, y: (Q(x ^ y) + Q(x) + Q(y)) & 1
    print('depth-2 lemma, the forced step (case beta(m1,m2) = 0), by exhaustive search with pruning:')
    for (k, name, beta, pairs) in ((4, 'pairing of Q', symp(2), ((0b0011, 0b1100), (0b0001, 0b0100), (0b0001, 0b0011))),
                                   (5, 'dot product', dot, ((0b00001, 0b00010), (0b00011, 0b01100), (0b00011, 0b00101), (0b00111, 0b11001))),
                                   (6, 'pairing of Q', symp(3), ((0b000011, 0b001100), (0b000001, 0b000100), (0b000001, 0b000011), (0b000111, 0b111000)))):
        for (m1, m2) in pairs:
            if beta(m1, m2) != 0: print('  k=%d %s m1=%s m2=%s: beta(m1,m2)=1, other case (by hand)' % (k, name, bin(m1), bin(m2))); continue
            tot, char = csp(k, beta, m1, m2)
            print('  k=%d (%d points) %s m1=%s m2=%s: solutions %d, of which the two character solutions p = eta psi, q = -eta chi: %d' % (k, 1 << k, name, bin(m1), bin(m2), tot, char))
    for k in (3, 4, 5):
        print('rank of the block (rows in a hyperplane, columns in its complement) of the %d-point transform, over all hyperplanes: %s ; N/4 = %d' % (1 << k, rank_block(k), (1 << k)//4))
    print('least r allowed by  r >= 2^(ceil(k/r) - 2)  (and r >= 3 from 32 points on), against the tensor arrangement k/2:')
    for k in (4, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64, 128, 256, 1024):
        r = 1
        while True:
            t = -(-k // r) - 1          # largest t with r t < k
            if 2*r >= 2**t and (k < 5 or r >= 3) and (k < 3 or r >= 2): break
            r += 1
        print('  k=%d: r >= %d ; k/2 = %d ; k/log2(k) = %.1f' % (k, r, k//2, k / (len(bin(k)) - 3 + 1e-9) if k > 1 else 0))
