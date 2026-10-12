# v-2: my own search for "calls to a box". FLOATS: a hit is a CANDIDATE, "none" is not a proof.
# Program: c_j = A (L_j x + sum_{i<j} M_ji c_i), out = Q x + sum_j P_j c_j, wanted (A kron A) x for every A of a family.
# usage: calls.py K seconds_per_case seed case1 case2 ...   with case = family:r
import numpy as np, sys, time
from scipy.optimize import least_squares
K = int(sys.argv[1]); CAP = float(sys.argv[2]); rng = np.random.default_rng(int(sys.argv[3])); K2 = K*K
def box(kind):
    while True:
        if kind == 'generic': return rng.normal(size=(K, K))
        if kind == 'symmetric':
            B = rng.normal(size=(K, K)); return (B + B.T)/2
        if kind == 'orthogonal':
            q, r = np.linalg.qr(rng.normal(size=(K, K))); return q*np.sign(np.diag(r))*rng.choice([-1.0, 1.0])
        if kind == 'rotation':
            q, r = np.linalg.qr(rng.normal(size=(K, K))); q = q*np.sign(np.diag(r))
            if np.linalg.det(q) < 0: q[:, 0] = -q[:, 0]
            return q
        if kind == 'involution':
            S = rng.normal(size=(K, K))
            if abs(np.linalg.det(S)) < 0.3: continue
            d = np.ones(K); d[:max(1, K//2)] = -1
            return S @ np.diag(d) @ np.linalg.inv(S)
        if kind == 'reflection':          # 1 - 2 u u^T, one mirror direction
            u = rng.normal(size=K); u /= np.linalg.norm(u); return np.eye(K) - 2*np.outer(u, u)
        if kind == 'halfreflection':      # 1 - 2 P, P an orthogonal projection of rank K/2
            q, r = np.linalg.qr(rng.normal(size=(K, K))); d = np.ones(K); d[:K//2] = -1
            return q @ np.diag(d) @ q.T
        if kind == 'scaledreflection':    # t (1 - 2 u u^T): the family closed under scaling
            u = rng.normal(size=K); u /= np.linalg.norm(u); return rng.normal()*(np.eye(K) - 2*np.outer(u, u))
        raise SystemExit('family?')
def nun(r): return r*K*K2 + (r*(r-1)//2)*K2 + K2*r*K + K2*K2
def run(t, r, As, want):
    i = 0; L = t[i:i + r*K*K2].reshape(r, K, K2); i += r*K*K2
    C = []
    for j in range(r):
        W = np.broadcast_to(L[j], (len(As), K, K2)).copy()
        for h in range(j):
            W += t[i:i + K2].reshape(K, K) @ C[h]; i += K2
        C.append(As @ W)
    P = t[i:i + K2*r*K].reshape(K2, r*K); i += K2*r*K
    Q = t[i:i + K2*K2].reshape(K2, K2)
    F = Q + P @ np.concatenate(C, axis=1)
    return (F - want).ravel()
def kr(As): return np.stack([np.kron(A, A) for A in As])
for case in sys.argv[4:]:
    kind, r = case.split(':'); r = int(r); nb = 14 if K == 2 else 24
    As = np.stack([box(kind) for _ in range(nb)]); want = kr(As); t0 = time.time(); best = 9e9; hits = 0; starts = 0; fresh = None
    while time.time() - t0 < CAP and hits < 3:
        starts += 1
        sol = least_squares(run, rng.normal(size=nun(r))*0.7, args=(r, As, want), method='lm', max_nfev=60*nun(r) if K == 2 else 6*nun(r))
        v = float(np.sqrt((sol.fun**2).mean())); best = min(best, v)
        if v < 1e-9:
            hits += 1; T = np.stack([box(kind) for _ in range(8)]); fresh = float(np.sqrt((run(sol.x, r, T, kr(T))**2).mean()))
            np.save('hit_K%d_%s_r%d.npy' % (K, kind, r), sol.x)
    print('K=%d %-16s calls r=%d: starts %d, hits %d, best rms residual %.2e, last hit on 8 fresh boxes %s, %.0f s'
          % (K, kind, r, starts, hits, best, 'n/a' if fresh is None else '%.1e' % fresh, time.time() - t0), flush=True)
