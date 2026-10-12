# x-4: flag depth at 8 points, second version: analytic Jacobian, enough iterations, controls that have more equations than unknowns.
# FLOATS: a hit is a candidate only; no hit is not a proof.
import sys, time
import numpy as np
from scipy.optimize import least_squares
from depth3 import flagP, all_flags, all_gl, target

def make(N, k, r, Ps, T):
    def parts(p):
        ds = [p[i*N:(i+1)*N] for i in range(r+1)]; off = (r+1)*N
        Ks = [np.tensordot(p[off + i*(k+1): off + (i+1)*(k+1)], Ps[i], axes=1) for i in range(r)]
        return ds, Ks
    def prefsuf(ds, Ks):
        Pre = [np.eye(N)]                      # Pre[i] = D0 K1 D1 ... K_i   (no D_i)
        for i in range(1, r+1): Pre.append((Pre[i-1] * ds[i-1][None, :]) @ Ks[i-1])
        Suf = [None]*(r+1); Suf[r] = np.eye(N)  # Suf[i] = K_{i+1} D_{i+1} ... K_r D_r
        for i in range(r-1, -1, -1): Suf[i] = Ks[i] @ (ds[i+1][:, None] * Suf[i+1])
        return Pre, Suf
    def res(p):
        ds, Ks = parts(p); Pre, Suf = prefsuf(ds, Ks)
        return ((Pre[r] * ds[r][None, :]) - T).ravel()
    def jac(p):
        ds, Ks = parts(p); Pre, Suf = prefsuf(ds, Ks)
        J = np.zeros((N*N, (r+1)*N + r*(k+1)))
        for i in range(r+1):
            # dM/d d_i[z] = Pre[i][:, z] outer Suf[i][z, :]
            J[:, i*N:(i+1)*N] = np.einsum('xz,zy->xyz', Pre[i], Suf[i]).reshape(N*N, N)
        off = (r+1)*N
        for i in range(r):
            Lm = Pre[i] * ds[i][None, :]; Rm = ds[i+1][:, None] * Suf[i+1]
            J[:, off + i*(k+1): off + (i+1)*(k+1)] = np.einsum('xu,juv,vy->xyj', Lm, Ps[i], Rm).reshape(N*N, k+1)
        return J
    return res, jac

def solve(N, k, r, Ps, T, rng, tries=1):
    res, jac = make(N, k, r, Ps, T); best = 1e9; bp = None
    for _ in range(tries):
        p0 = np.concatenate([rng.choice([-1.0, 1.0], size=(r+1)*N) * np.exp(0.5*rng.standard_normal((r+1)*N)), rng.standard_normal(r*(k+1))])
        try: sol = least_squares(res, p0, jac=jac, method='lm', max_nfev=4000, xtol=1e-15, ftol=1e-15, gtol=1e-15)
        except Exception as e: continue
        err = np.max(np.abs(res(sol.x)))
        if err < best: best = err; bp = sol.x
        if best < 1e-9: break
    return best, bp

if __name__ == '__main__':
    budget = float(sys.argv[1]); t0 = time.time(); rng = np.random.default_rng(2026)
    np.set_printoptions(precision=6, suppress=True, linewidth=250)
    T = target(4, (2, 1, 8, 4)); Ps = [flagP(4, [3, 1, 12, 4]), flagP(4, [12, 4, 3, 1])]
    errs = [solve(16, 4, 2, Ps, T, rng)[0] for _ in range(12)]
    print('control: 16 points, r=2, tensor arrangement (exists, exact): hits %d of 12 single starts ; errors %s' % (sum(e < 1e-9 for e in errs), ' '.join('%.0e' % e for e in errs)), flush=True)
    errs = [solve(16, 4, 1, [flagP(4, [1, 2, 4, 8])], T, rng)[0] for _ in range(6)]
    print('control: 16 points, r=1 (derived: impossible): hits %d of 6 ; errors %s' % (sum(e < 1e-9 for e in errs), ' '.join('%.0e' % e for e in errs)), flush=True)
    T = target(3, (2, 1, 4)); Ps = [flagP(3, [3, 1, 4]), flagP(3, [4, 1, 2]), flagP(3, [4, 1, 2])]
    errs = [solve(8, 3, 3, Ps, T, rng)[0] for _ in range(12)]
    print('control: 8 points, r=3, one pair then one bit twice (exists by derivation): hits %d of 12 single starts ; errors %s' % (sum(e < 1e-9 for e in errs), ' '.join('%.0e' % e for e in errs)), flush=True)
    k = 3; flags = all_flags(k); gls = all_gl(k); P1 = flagP(k, [1, 2, 4])
    configs = [(f2, g) for f2 in flags for g in gls]
    order = np.random.default_rng(7).permutation(len(configs)); done = 0; nh = 0; miss = []; hitcfg = []
    rnd = 0
    while time.time() - t0 < budget:
        rnd += 1
        for idx in order:
            if time.time() - t0 > budget: break
            f2, g = configs[idx]; T = target(k, g)
            best, p = solve(8, k, 2, [P1, flagP(k, list(f2))], T, rng)
            done += 1
            if best < 1e-9:
                nh += 1; hitcfg.append((f2, g))
                if nh <= 4: print('HIT (candidate): flag1=(1,2,4) flag2=%s labelling g=%s err=%.1e\n   params=%s' % (f2, g, best, np.array2string(p)), flush=True)
            else: miss.append(best)
    ms = np.array(miss) if miss else np.array([0.0])
    print('8 points, r=2: %d solves over %d configurations (round %d), hits %d in %d distinct configurations ; smallest miss %.3e, median miss %.3e'
          % (done, len(configs), rnd, nh, len(set(hitcfg)), ms.min(), np.median(ms)), flush=True)
