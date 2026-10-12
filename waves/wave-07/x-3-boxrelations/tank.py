# x-3 boxrelations, the FIRST-ORDER (tangent) problem. If a call program with r calls gives A (x) A for every A in a smooth
# family through A0, then differentiating at A0 gives r terms with  sum_j P_j E L_j = E (x) A0 + A0 (x) E  for every E in the
# tangent space T of the family at A0 (P_j: K -> K^2, L_j: K^2 -> K fixed).  So  r(family) >= rho(T) = least such r.
# This is a tensor-rank problem; FLOATS (Levenberg-Marquardt, own loop, exact Jacobian). A hit is a candidate, "none" is not a proof.
# usage: tank.py K family r starts seed seconds     family: gl | so | sym | refl | inv
import numpy as np, sys, time
def lm_solve(fun, jacf, x, maxit, tol=1e-13, deadline=None):
    # plain Levenberg-Marquardt on the normal equations (numpy / LAPACK); returns x and the rms residual
    lam = 1e-2; f = fun(x); c = float(f @ f)
    for it in range(maxit):
        if deadline is not None and time.time() > deadline: break
        if c/len(f) < tol*tol: break
        J = jacf(x); g = J.T @ f; H = J.T @ J; dg = np.diag(H).copy() + 1e-12; ok = False
        for tries in range(12):
            try: step = np.linalg.solve(H + lam*np.diag(dg), -g)
            except np.linalg.LinAlgError: lam *= 10; continue
            f2 = fun(x + step); c2 = float(f2 @ f2)
            if c2 < c: x = x + step; f = f2; c = c2; lam = max(lam/5, 1e-15); ok = True; break
            lam *= 6
        if not ok: break
    return x, float(np.sqrt(c/len(f)))
K = int(sys.argv[1]); fam = sys.argv[2]; r = int(sys.argv[3]); starts = int(sys.argv[4]); seed = int(sys.argv[5]); tmax = float(sys.argv[6])
rng = np.random.default_rng(seed); h = K//2
A0 = np.eye(K) if fam in ('gl', 'so', 'sym') else np.diag([1.0]*(K - h) + [-1.0]*h)
Es = []
for a in range(K):
    for b in range(K):
        E = np.zeros((K, K))
        if fam == 'gl': E[a, b] = 1
        elif fam == 'so':
            if a >= b: continue
            E[a, b] = 1; E[b, a] = -1
        elif fam == 'sym':
            if a > b: continue
            E[a, b] = E[b, a] = 1
        elif fam == 'refl':                       # symmetric and anticommuting with A0
            if not (a < K - h <= b): continue
            E[a, b] = E[b, a] = 1
        elif fam == 'inv':                        # anticommuting with A0
            if (a < K - h) == (b < K - h): continue
            E[a, b] = 1
        Es.append(E)
Es = np.array(Es); n = len(Es); N = K*K
T = np.array([np.kron(E, A0) + np.kron(A0, E) for E in Es])        # n x N x N
def unpack(t): return t[:r*N*K].reshape(r, N, K), t[r*N*K:].reshape(r, K, N)
def resid(t):
    P, L = unpack(t); return (np.einsum('joa,nab,jbx->nox', P, Es, L) - T).ravel()
def jac(t):
    P, L = unpack(t); J = np.zeros((n, N, N, 2*r*N*K))
    EL = np.einsum('nab,jbx->njax', Es, L); PE = np.einsum('joa,nab->njob', P, Es); I = np.eye(N)
    for j in range(r):
        J[:, :, :, j*N*K:(j+1)*N*K] = np.einsum('op,nax->noxpa', I, EL[:, j]).reshape(n, N, N, N*K)
        J[:, :, :, r*N*K + j*K*N: r*N*K + (j+1)*K*N] = np.einsum('nob,xy->noxby', PE[:, j], I).reshape(n, N, N, K*N)
    return J.reshape(n*N*N, -1)
t0 = time.time(); best = 1e9; hits = 0; done = 0
for s in range(starts):
    if time.time() - t0 > tmax: break
    xs, v = lm_solve(resid, jac, rng.normal(size=2*r*N*K)*rng.choice([0.3, 0.6, 1.0]), 500, deadline=t0 + tmax)
    best = min(best, v); hits += v < 1e-10; done += 1
    if v < 1e-10 and hits == 1: np.save('tan_K%d_%s_r%d.npy' % (K, fam, r), xs)
# two cheap exact-in-principle lower bounds (ranks in floats): what the inputs must keep, what the outputs must span
Bm = T.reshape(n*N, N); rin = np.linalg.matrix_rank(Bm); rout = np.linalg.matrix_rank(T.transpose(1, 0, 2).reshape(N, n*N))
print('K=%d tangent %-4s (dim %2d) r=%d: starts %d, best rms %.2e, hits %d | rank bounds: inputs kept %d, outputs spanned %d, so r >= %d | %.0f s'
      % (K, fam, n, r, done, best, hits, rin, rout, -(-max(rin, rout)//K), time.time() - t0), flush=True)
