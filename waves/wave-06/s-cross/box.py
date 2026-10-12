# s-cross hybrid 2: how many calls to a box A does X -> (A (x) A) X need, when the algorithm is linear and the same for every box?
# calls c_j = A (L_j x + sum_{i<j} M_ji c_i), outputs Q x + sum_j P_j c_j, identity wanted for every A in a family. K = 2.
# FLOATS: this is a search (least squares from random starts). A small residual is a CANDIDATE only; "none found" is not "none".
import numpy as np, sys
from scipy.optimize import least_squares
K = 2
def boxes(kind, rng, n):
    out = []
    while len(out) < n:
        if kind == 'generic': A = rng.normal(size=(K, K))
        elif kind == 'involution':
            S = rng.normal(size=(K, K))
            if abs(np.linalg.det(S)) < 0.3: continue
            A = S @ np.diag([1.0, -1.0]) @ np.linalg.inv(S)
        elif kind == 'reflection':
            u = rng.normal(size=K); u /= np.linalg.norm(u); A = np.eye(K) - 2*np.outer(u, u)
        out.append(A)
    return out
def unpack(t, r):
    i = 0
    L = t[i:i + r*K*K*K].reshape(r, K, K*K); i += r*K*K*K
    M = np.zeros((r, r, K, K))
    for j in range(r):
        for h in range(j): M[j, h] = t[i:i + K*K].reshape(K, K); i += K*K
    P = t[i:i + K*K*r*K].reshape(K*K, r*K); i += K*K*r*K
    Qm = t[i:i + K**4].reshape(K*K, K*K)
    return L, M, P, Qm
def nun(r): return r*K**3 + (r*(r-1)//2)*K*K + K*K*r*K + K**4
def resid(t, r, As):
    L, M, P, Qm = unpack(t, r); res = []
    for A in As:
        c = []
        for j in range(r):
            w = L[j].copy()
            for h in range(j): w = w + M[j, h] @ c[h]
            c.append(A @ w)
        F = Qm + P @ np.vstack(c)
        res.append((F - np.kron(A, A)).ravel())
    return np.concatenate(res)
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
for kind, r, starts in (('generic', 4, 6), ('generic', 3, 60), ('involution', 3, 60), ('reflection', 3, 60), ('involution', 2, 40), ('reflection', 2, 40)):
    As = boxes(kind, rng, 14); best = 1e9; hits = 0
    for s in range(starts):
        t0 = rng.normal(size=nun(r))
        sol = least_squares(resid, t0, args=(r, As), method='lm', max_nfev=4000)
        v = float(np.sqrt((sol.fun**2).mean())); best = min(best, v); hits += v < 1e-9
        if v < 1e-9 and hits == 1:
            test = boxes(kind, rng, 6); tv = float(np.sqrt((resid(sol.x, r, test)**2).mean()))
            print('   first hit %s r=%d: residual %.2e, on 6 fresh boxes %.2e' % (kind, r, v, tv)); np.save('box_%s_r%d.npy' % (kind, r), sol.x)
    print('%-11s calls r=%d: %d starts, best rms residual %.3e, starts below 1e-9: %d' % (kind, r, starts, best, hits), flush=True)
