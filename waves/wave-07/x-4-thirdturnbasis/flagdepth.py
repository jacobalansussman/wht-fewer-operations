# x-4: "flag depth" of the transform. FLOATS: a hit is a candidate only, no hit is not a proof.
# Model: M = D_0 K_1 D_1 K_2 ... K_r D_r, D_i free diagonals, K_i = sum_j c_j [x+y in M_j] for a flag M_0 < M_1 < ... < M_k
# (running sums up one merge tree and down the same tree with free weights: 3N-3 gates (G) each).
# Flags are coordinate flags in one basis: flag i = span(e_w(1)), span(e_w(1), e_w(2)), ...  (two flags can always be put so).
# Target: ANY Hadamard matrix (entries +-1, M M^T = N I); afterwards test whether it is of Sylvester type (the transform).
import sys, time, itertools
import numpy as np
from scipy.optimize import least_squares

def build(k, perms):
    N = 1 << k
    xs = np.arange(N)
    X = xs[:, None] ^ xs[None, :]
    Ps = []
    for w in perms:
        P = []
        mask = 0
        P.append((X == 0).astype(float))
        for j in range(k):
            mask |= 1 << w[j]
            P.append(((X & ~mask) == 0).astype(float))
        Ps.append(np.array(P))  # (k+1, N, N)
    return N, Ps

def unpack(p, N, k, r):
    ds = [p[i*N:(i+1)*N] for i in range(r+1)]
    off = (r+1)*N
    cs = [p[off + i*(k+1): off + (i+1)*(k+1)] for i in range(r)]
    return ds, cs

def mat(p, N, k, r, Ps):
    ds, cs = unpack(p, N, k, r)
    M = np.diag(ds[r])
    for i in range(r-1, -1, -1):
        K = np.tensordot(cs[i], Ps[i], axes=1)
        M = ds[i][:, None] * (K @ M)
    return M

def resid(p, N, k, r, Ps, iu):
    M = mat(p, N, k, r, Ps)
    G = M @ M.T - N*np.eye(N)
    return np.concatenate([(M*M - 1).ravel(), G[iu] / np.sqrt(N)])

def f2rank(A):
    A = [int(''.join(str(int(v)) for v in row), 2) for row in A]
    rk = 0
    for bit in range(len(bin(max(A + [1]))) , -1, -1):
        piv = None
        for i in range(rk, len(A)):
            if (A[i] >> bit) & 1: piv = i; break
        if piv is None: continue
        A[rk], A[piv] = A[piv], A[rk]
        for i in range(len(A)):
            if i != rk and (A[i] >> bit) & 1: A[i] ^= A[rk]
        rk += 1
    return rk

def trial(k, r, perms, seed, maxnfev=400):
    N, Ps = build(k, perms)
    rng = np.random.default_rng(seed)
    iu = np.triu_indices(N)
    p0 = np.concatenate([rng.choice([-1.0, 1.0], size=(r+1)*N) * (1 + 0.2*rng.standard_normal((r+1)*N)),
                         rng.standard_normal(r*(k+1))])
    # scale so that entries are of size 1
    M0 = mat(p0, N, k, r, Ps); p0[:N] /= np.sqrt(np.mean(M0*M0))
    t = time.time()
    sol = least_squares(resid, p0, args=(N, k, r, Ps, iu), method='trf', max_nfev=maxnfev, xtol=1e-14, ftol=1e-14, gtol=1e-14)
    M = mat(sol.x, N, k, r, Ps)
    err = np.max(np.abs(np.abs(M) - 1)); orth = np.max(np.abs(M @ M.T - N*np.eye(N)))
    out = 'k=%d r=%d flags=%s seed=%d: loss=%.3e max||M|-1|=%.2e max|MM^T-NI|=%.2e nfev=%d %.0fs' % (
        k, r, '/'.join(''.join(str(a+1) for a in w) for w in perms), seed, 2*sol.cost, err, orth, sol.nfev, time.time()-t)
    if err < 1e-6 and orth < 1e-5:
        S = np.sign(M); S = S * S[0][None, :]; S = S * S[:, 0][:, None]
        rk = f2rank((S < 0).astype(int))
        ds, cs = unpack(sol.x, N, k, r)
        out += '  HIT: Hadamard; F2-rank of sign pattern %d (Sylvester type iff %d); coefficient ranges: ' % (rk, k)
        out += ' '.join('[%.2g..%.2g]' % (np.min(np.abs(c[np.abs(c) > 1e-9])) if np.any(np.abs(c) > 1e-9) else 0, np.max(np.abs(c))) for c in cs)
    print(out, flush=True)
    return err < 1e-6 and orth < 1e-5

if __name__ == '__main__':
    mode = sys.argv[1]; budget = float(sys.argv[2]); t0 = time.time()
    rng = np.random.default_rng(12345 if mode == 'A' else 54321)
    if mode == 'A':
        print('--- control: k=4, r=2, flags 1234 / 3412 (the tensor arrangement must be reachable)', flush=True)
        for sd in range(6): trial(4, 2, [(0, 1, 2, 3), (2, 3, 0, 1)], sd)
        print('--- k=4, r=1 (derived: impossible)', flush=True)
        for sd in range(4): trial(4, 1, [(0, 1, 2, 3)], sd)
        print('--- k=4, r=2, opposite flags 1234 / 4321', flush=True)
        for sd in range(4): trial(4, 2, [(0, 1, 2, 3), (3, 2, 1, 0)], sd)
        print('--- THE QUESTION: k=6, r=2, opposite (generic) flags', flush=True)
        sd = 0
        while time.time() - t0 < budget * 0.5:
            trial(6, 2, [(0, 1, 2, 3, 4, 5), (5, 4, 3, 2, 1, 0)], sd); sd += 1
        print('--- k=6, r=2, random relative positions', flush=True)
        while time.time() - t0 < budget:
            w = tuple(int(a) for a in rng.permutation(6)); trial(6, 2, [(0, 1, 2, 3, 4, 5), w], int(rng.integers(1 << 30)))
    else:
        print('--- control: k=6, r=3, flags 123456 / 345612 / 561234 (tensor arrangement must be reachable)', flush=True)
        sd = 0
        while time.time() - t0 < budget * 0.4:
            trial(6, 3, [(0, 1, 2, 3, 4, 5), (2, 3, 4, 5, 0, 1), (4, 5, 0, 1, 2, 3)], sd); sd += 1
        print('--- k=6, r=2, flags 123456 / 345612 and 123456 / 456123', flush=True)
        while time.time() - t0 < budget * 0.7:
            trial(6, 2, [(0, 1, 2, 3, 4, 5), (2, 3, 4, 5, 0, 1)], sd); sd += 1
            trial(6, 2, [(0, 1, 2, 3, 4, 5), (3, 4, 5, 0, 1, 2)], sd); sd += 1
        print('--- k=6, r=2, random relative positions', flush=True)
        while time.time() - t0 < budget:
            w = tuple(int(a) for a in rng.permutation(6)); trial(6, 2, [(0, 1, 2, 3, 4, 5), w], int(rng.integers(1 << 30)))
