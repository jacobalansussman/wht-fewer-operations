# s-cross hybrid 1: split the 2^(2n)-point transform by a quadric. Exact: integer matrices, polynomial identities checked in integers.
# H(x,y) = (-1)^(x.y) plain;  Q(x) = x1x2 + x3x4 + ... ; S1 = {Q=1}, S0 = {Q=0}.
import numpy as np, sys
def pop(v): return bin(v).count('1')
def run(n, form):
    k = 2*n; N = 1 << k; r = 1 << n
    def Q(x): return sum(((x >> (2*i)) & 1) * ((x >> (2*i+1)) & 1) for i in range(n)) & 1
    def swap(x):  # exchange the two bits of every pair: x.swap(y) is the polar form of Q
        y = 0
        for i in range(n):
            a = (x >> (2*i)) & 1; b = (x >> (2*i+1)) & 1
            y |= (b << (2*i)) | (a << (2*i+1))
        return y
    if form == 'plain': H = np.array([[(-1)**pop(x & y) for y in range(N)] for x in range(N)], dtype=np.int64)
    else:               H = np.array([[(-1)**pop(x & swap(y)) for y in range(N)] for x in range(N)], dtype=np.int64)
    assert (H @ H == N*np.eye(N, dtype=np.int64)).all() if form == 'plain' else True
    S = [[x for x in range(N) if Q(x) == c] for c in (0, 1)]
    out = []
    for c in (0, 1):
        M = H[np.ix_(S[c], S[c])]; m = len(S[c])
        if not (M == M.T).all(): out.append('block %d%d not symmetric' % (c, c)); continue
        ev = np.linalg.eigvalsh(M.astype(float)); vals = sorted(set(int(round(e)) for e in ev))
        # exact check: product of (M - v I) over the rounded distinct eigenvalues is the zero matrix
        P = np.eye(m, dtype=object)
        Mo = M.astype(object)
        for v in vals: P = P.dot(Mo - v*np.eye(m, dtype=object))
        exact = all(int(t) == 0 for t in P.flatten())
        mult = {v: int(sum(1 for e in ev if abs(e - v) < 1e-6)) for v in vals}
        out.append('block Q=%d: %d points, eigenvalues %s, minimal-polynomial identity exact: %s, trace %d' % (c, m, mult, exact, int(np.trace(M))))
    C = H[np.ix_(S[0], S[1])]
    G = (C.T @ C); ev = np.linalg.eigvalsh(G.astype(float)); vals = sorted(set(int(round(e)) for e in ev))
    out.append('cross block %dx%d: C^T C eigenvalues %s' % (len(S[0]), len(S[1]), {v: int(sum(1 for e in ev if abs(e - v) < 1e-6)) for v in vals}))
    print('n=%d N=%d sqrtN=%d form=%s' % (n, N, r, form)); [print('   ' + o) for o in out]
for n in (1, 2, 3, 4):
    for form in ('plain', 'polar'): run(n, form)
