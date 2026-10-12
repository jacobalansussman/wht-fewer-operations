# x-4: flag depth at 8 points. FLOATS (a hit is a candidate only; no hit is not a proof).
# Is the 8-point transform, in any labelling T(x,y) = (-1)^(x . g y), equal to D_0 K_1 D_1 K_2 D_2 with K_i flag kernels on any two flags?
# Fixed target, least squares on M - T from random starts (the problem is linear in each factor). Controls first.
import sys, time, itertools
import numpy as np
from scipy.optimize import least_squares

def pop(v): return bin(v).count('1')

def flagP(k, basis):
    N = 1 << k; xs = np.arange(N); X = xs[:, None] ^ xs[None, :]
    P = [(X == 0).astype(float)]; span = {0}
    for v in basis:
        span |= {a ^ v for a in span}
        P.append(np.isin(X, list(span)).astype(float))
    return np.array(P)

def all_flags(k):
    N = 1 << k; seen = {}
    def rec(basis, span):
        if len(basis) == k:
            key = tuple(sorted(tuple(sorted(s)) for s in spans(basis)))
            seen.setdefault(key, tuple(basis)); return
        for v in range(1, N):
            if v not in span: rec(basis + [v], span | {a ^ v for a in span})
    def spans(basis):
        out = []; span = {0}
        for v in basis:
            span = span | {a ^ v for a in span}; out.append(frozenset(span))
        return out
    rec([], {0})
    return list(seen.values())

def all_gl(k):
    N = 1 << k; out = []
    def rec(cols, span):
        if len(cols) == k: out.append(tuple(cols)); return
        for v in range(1, N):
            if v not in span: rec(cols + [v], span | {a ^ v for a in span})
    rec([], {0})
    return out

def target(k, g):
    N = 1 << k
    def gy(y):
        r = 0
        for i in range(k):
            if (y >> i) & 1: r ^= g[i]
        return r
    return np.array([[(-1.0)**pop(x & gy(y)) for y in range(N)] for x in range(N)])

def mat(p, N, k, r, Ps):
    ds = [p[i*N:(i+1)*N] for i in range(r+1)]; off = (r+1)*N
    M = np.diag(ds[r])
    for i in range(r-1, -1, -1):
        K = np.tensordot(p[off + i*(k+1): off + (i+1)*(k+1)], Ps[i], axes=1)
        M = ds[i][:, None] * (K @ M)
    return M

def solve(k, r, Ps, T, rng, tries):
    N = 1 << k; best = 1e9; bestp = None
    for _ in range(tries):
        p0 = np.concatenate([rng.choice([-1.0, 1.0], size=(r+1)*N) * np.exp(0.5*rng.standard_normal((r+1)*N)), rng.standard_normal(r*(k+1))])
        try:
            sol = least_squares(lambda p: (mat(p, N, k, r, Ps) - T).ravel(), p0, method='lm', max_nfev=3000, xtol=1e-15, ftol=1e-15, gtol=1e-15)
        except Exception as e:
            continue
        err = np.max(np.abs(mat(sol.x, N, k, r, Ps) - T))
        if err < best: best = err; bestp = sol.x
        if best < 1e-9: break
    return best, bestp

if __name__ == '__main__':
    part = int(sys.argv[1]); budget = float(sys.argv[2]); t0 = time.time(); rng = np.random.default_rng(1000 + part)
    np.set_printoptions(precision=5, suppress=True, linewidth=200)
    if part == 0:
        # controls
        T = target(1, (1,)); hits = sum(solve(1, 2, [flagP(1, [1])]*2, T, rng, 1)[0] < 1e-9 for _ in range(20))
        print('control: one bit (2 points), r=2 (derived: possible): hits %d of 20 single starts' % hits, flush=True)
        hits = sum(solve(1, 1, [flagP(1, [1])], T, rng, 1)[0] < 1e-9 for _ in range(20))
        print('control: one bit (2 points), r=1 (derived: impossible over the reals): hits %d of 20 single starts' % hits, flush=True)
        # 16 points, tensor arrangement; target in symplectic labelling: B(x,y) = x1y2+x2y1+x3y4+x4y3  => g swaps bits in pairs
        T = target(4, (2, 1, 8, 4)); Ps = [flagP(4, [3, 1, 12, 4]), flagP(4, [12, 4, 3, 1])]
        hits = sum(solve(4, 2, Ps, T, rng, 1)[0] < 1e-9 for _ in range(40))
        print('control: 16 points, r=2, the tensor arrangement (exists, exact): hits %d of 40 single starts' % hits, flush=True)
        Ps = [flagP(4, [1, 2, 4, 8])]
        hits = sum(solve(4, 1, Ps, T, rng, 1)[0] < 1e-9 for _ in range(20))
        print('control: 16 points, r=1 (derived: impossible): hits %d of 20' % hits, flush=True)
        # 8 points r=3: pair (1 kernel) and a single bit (2 kernels)
        T = target(3, (2, 1, 4)); Ps = [flagP(3, [3, 1, 4]), flagP(3, [4, 1, 2]), flagP(3, [4, 1, 2])]
        hits = sum(solve(3, 3, Ps, T, rng, 1)[0] < 1e-9 for _ in range(40))
        print('control: 8 points, r=3, pair then single bit twice (exists by derivation): hits %d of 40 single starts' % hits, flush=True)
    k = 3; flags = all_flags(k); gls = all_gl(k)
    print('8 points: %d flags, %d labellings' % (len(flags), len(gls)), flush=True)
    f1 = (1, 2, 4)   # first flag fixed (free by a change of coordinates)
    configs = [(f2, g) for f2 in flags for g in gls]
    order = np.random.default_rng(7).permutation(len(configs))
    mine = [configs[i] for i in order[part::2]]
    P1 = flagP(k, list(f1)); done = 0; nh = 0; worst_best = []
    rnd = 0
    while time.time() - t0 < budget:
        rnd += 1
        for (f2, g) in mine:
            if time.time() - t0 > budget: break
            T = target(k, g)
            best, p = solve(k, 2, [P1, flagP(k, list(f2))], T, rng, 2)
            done += 1
            if best < 1e-9:
                nh += 1
                if nh <= 6:
                    print('HIT (candidate): flag2=%s g=%s err=%.1e params=%s' % (f2, g, best, np.array2string(p)), flush=True)
            else:
                worst_best.append(best)
    wb = np.array(worst_best) if worst_best else np.array([0.0])
    print('8 points, r=2: %d configurations visited (rounds %d, 2 starts each), hits %d ; smallest miss %.3e, median miss %.3e' % (done, rnd, nh, wb.min(), np.median(wb)), flush=True)
