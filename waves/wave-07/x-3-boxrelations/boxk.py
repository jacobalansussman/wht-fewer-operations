# x-3 boxrelations: least number r of calls to a box A that give X -> A X A^T (the matrix A (x) A) for every A in a family.
# Call program: c_j = A (L_j x + sum_{i<j} M_ji c_i), output = Q x + sum_j P_j c_j, with L, M, P, Q fixed and FREE (glue not priced).
# FLOATS: Levenberg-Marquardt (own loop, exact Jacobian) from random starts. A hit is a CANDIDATE (checked on fresh boxes); "none" is not a proof.
# usage: boxk.py K family part r starts seed [seconds]
#   family: generic | inv | sym | refl (1-2P, rank P = K/2) | refl1 (rank P = 1) | orth (det -1, see note) | rot (det +1) | oboth | syminvall (any signature)
#           perm (the address maps: permutation boxes x -> g x, a FINITE family; every member is used, so 'fresh boxes' are the same ones)
#   part: full | sym (X symmetric) | skew | symtl (symmetric, trace 0)
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
K = int(sys.argv[1]); fam = sys.argv[2]; part = sys.argv[3]; r = int(sys.argv[4]); starts = int(sys.argv[5]); seed = int(sys.argv[6])
tmax = float(sys.argv[7]) if len(sys.argv) > 7 else 1e9
rng = np.random.default_rng(seed)
def addressmaps():
    # all permutation matrices x -> g x of the K = 2^k addresses, g an invertible bit matrix (the 'address maps'); K = 4: six of them
    import itertools
    k = K.bit_length() - 1; out = []
    for cols in itertools.product(range(1, K), repeat=k):
        img = [0]*K
        for x in range(K):
            y = 0
            for b in range(k):
                if x >> b & 1: y ^= cols[b]
            img[x] = y
        if len(set(img)) == K:
            Pm = np.zeros((K, K)); Pm[img, range(K)] = 1; out.append(Pm)
    return out
ALLMAPS = addressmaps() if fam == 'perm' else None
def box(kind):
    while True:
        if kind == 'perm': return ALLMAPS[rng.integers(len(ALLMAPS))]
        if kind == 'generic': return rng.normal(size=(K, K))
        if kind == 'sym':
            S = rng.normal(size=(K, K)); return (S + S.T)/2
        if kind == 'inv':
            S = rng.normal(size=(K, K))
            if np.linalg.cond(S) > 30: continue
            return S @ np.diag([1.0]*(K//2) + [-1.0]*(K - K//2)) @ np.linalg.inv(S)
        Qo, _ = np.linalg.qr(rng.normal(size=(K, K)))
        if kind == 'orth': return Qo          # NOTE: numpy's QR gives determinant (-1)^(K-1) here: at K = 2 and K = 4 this family is 'orthogonal with determinant -1'
        if kind in ('rot', 'oboth'):          # rot: determinant +1 (contains the identity); oboth: both components of the orthogonal group
            if (np.linalg.det(Qo) < 0) == (kind == 'rot' or rng.random() < 0.5): Qo[:, 0] *= -1
            return Qo
        if kind == 'refl': return Qo @ np.diag([1.0]*(K - K//2) + [-1.0]*(K//2)) @ Qo.T
        if kind == 'refl1': return Qo @ np.diag([1.0]*(K - 1) + [-1.0]) @ Qo.T
        if kind == 'syminvall':
            m = rng.integers(0, K + 1); return Qo @ np.diag([1.0]*(K - m) + [-1.0]*m) @ Qo.T
        raise SystemExit('family?')
def basis(part):
    cols = []
    for a in range(K):
        for b in range(K):
            E = np.zeros((K, K))
            if part == 'full': E[a, b] = 1
            elif part in ('sym', 'symtl'):
                if a > b: continue
                if a == b:
                    if part == 'symtl':
                        if a == K - 1: continue
                        E[a, a] = 1; E[K-1, K-1] = -1
                    else: E[a, a] = 1
                else: E[a, b] = E[b, a] = 1
            elif part == 'skew':
                if a >= b: continue
                E[a, b] = 1; E[b, a] = -1
            cols.append(E.ravel())
    return np.array(cols).T                      # K^2 x d
B = basis(part); d = B.shape[1]; Bp = np.linalg.pinv(B)   # outputs are read in the same subspace (A X A^T keeps the symmetry type)
if part == 'symtl' and fam not in ('refl', 'refl1', 'orth', 'rot', 'oboth', 'syminvall'): raise SystemExit('trace is kept only by orthogonal boxes')
m = d
nL = r*K*d; nM = (r*(r-1)//2)*K*K; nP = m*K*r; nQ = m*d; nun = nL + nM + nP + nQ
pairs = [(j, i) for j in range(r) for i in range(j)]
def unpack(t):
    L = t[:nL].reshape(r, K, d); Mv = t[nL:nL+nM].reshape(len(pairs), K, K) if pairs else np.zeros((0, K, K))
    P = t[nL+nM:nL+nM+nP].reshape(r, m, K); Q = t[nL+nM+nP:].reshape(m, d)
    return L, Mv, P, Q
def target(As): return np.array([Bp @ np.kron(A, A) @ B for A in As])
def forward(t, As):
    L, Mv, P, Q = unpack(t); c = []
    for j in range(r):
        w = np.broadcast_to(L[j], (len(As), K, d)).copy()
        for i in range(j): w += Mv[pairs.index((j, i))] @ c[i]
        c.append(As @ w)
    F = np.broadcast_to(Q, (len(As), m, d)).copy()
    for j in range(r): F += P[j] @ c[j]
    return F, c
class Late(Exception): pass
def resid(t, As, T):
    if time.time() - t0 > tmax: raise Late()
    return (forward(t, As)[0] - T).ravel()
def jac(t, As, T):
    L, Mv, P, Q = unpack(t); n = len(As); F, c = forward(t, As)
    G = [None]*r
    for j in range(r - 1, -1, -1):
        g = np.broadcast_to(P[j], (n, m, K)).copy()
        for l in range(j + 1, r): g += G[l] @ Mv[pairs.index((l, j))]
        G[j] = g @ As
    J = np.zeros((n, m, d, nun)); eyed = np.eye(d); eyem = np.eye(m)
    for j in range(r):                                   # L_j[a, x']
        J[:, :, :, j*K*d:(j+1)*K*d] = np.einsum('noa,xy->noxay', G[j], eyed).reshape(n, m, d, K*d)
    for q, (j, i) in enumerate(pairs):                   # M_ji[a, b]
        J[:, :, :, nL + q*K*K: nL + (q+1)*K*K] = np.einsum('noa,nbx->noxab', G[j], c[i]).reshape(n, m, d, K*K)
    for j in range(r):                                   # P_j[o', a]
        J[:, :, :, nL + nM + j*m*K: nL + nM + (j+1)*m*K] = np.einsum('op,nax->noxpa', eyem, c[j]).reshape(n, m, d, m*K)
    J[:, :, :, nL + nM + nP:] = np.einsum('op,xy->oxpy', eyem, eyed).reshape(m, d, m*d)[None]
    return J.reshape(n*m*d, nun)
nb = max(12, int(np.ceil(3.0*nun/(m*d))) + 2)
t0 = time.time(); best = 1e9; hits = 0; done = 0; fresh = None
for s in range(starts):
    if time.time() - t0 > tmax: break
    As = np.array(ALLMAPS) if (fam == 'perm' and len(ALLMAPS) <= 200) else np.array([box(fam) for _ in range(nb)]); T = target(As)
    x0 = rng.normal(size=nun)*rng.choice([0.3, 0.6, 1.0])
    xs, v = lm_solve(lambda t: (forward(t, As)[0] - T).ravel(), lambda t: jac(t, As, T), x0, 500, deadline=t0 + tmax)
    best = min(best, v); done += 1
    if v < 1e-9:
        Bs = np.array([box(fam) for _ in range(10)]); tv = float(np.sqrt(((forward(xs, Bs)[0] - target(Bs))**2).mean()))
        if tv < 1e-7:
            hits += 1
            if fresh is None: fresh = tv; np.save('hit_K%d_%s_%s_r%d.npy' % (K, fam, part, r), xs)
print('K=%d %-9s part=%-5s (dim %2d) r=%d: unknowns %d, boxes %d, starts %d, best rms residual %.2e, hits (also right on 10 fresh boxes) %d%s, %.0f s'
      % (K, fam, part, d, r, nun, nb, done, best, hits, '' if fresh is None else ' [fresh rms %.1e]' % fresh, time.time() - t0), flush=True)
