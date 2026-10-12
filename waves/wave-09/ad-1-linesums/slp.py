#!/usr/bin/env python3
"""slp.py -- let the machine propose straight-line programs.  Count (G): a gate is any a*u + b*v.
Wiring is searched by annealing; for a fixed wiring the coefficients are solved by batched Levenberg-Marquardt
(floating point).  Anything that reaches zero is normalised, rationalised and replayed exactly in Fractions.
usage: slp.py <task> <K gates> <seconds> <seed> <outdir> [mode]
tasks: H4 H8 H16 H4x2 H8x2? Z4 Z8 Z16 ; mode: seed (known circuit minus gates) | rand
"""
import numpy as np, sys, json, time, os, math
from fractions import Fraction

H2 = np.array([[1, 1], [1, -1.]]); Z2 = np.array([[1, 0], [1, 1.]])
J4 = np.ones((4, 4)) - 2 * np.eye(4)

def kp(A, k):
    M = np.array([[1.]])
    for _ in range(k): M = np.kron(M, A)
    return M

def circ_J4(nodes, base):
    i0, i1, i2, i3 = nodes
    g = [(i0, i1, 1., 1.), (i2, i3, 1., 1.), (base, base + 1, 1., 1.)]
    s = base + 2; outs = []
    for j, i in enumerate(nodes):
        g.append((s, i, 1., -2.)); outs.append(base + 3 + j)
    return g, outs

def task(name):
    """returns T (rows = targets), known gates [(u,v,a,b)], outs"""
    if name == 'H4':
        g, o = circ_J4([0, 1, 2, 3], 4); return J4.copy(), g, o
    if name == 'H4x2':
        T = np.zeros((8, 8)); T[:4, :4] = J4; T[4:, 4:] = J4
        g1, o1 = circ_J4([0, 1, 2, 3], 8); g2, o2 = circ_J4([4, 5, 6, 7], 15)
        return T, g1 + g2, o1 + o2
    if name == 'H8':
        T = np.kron(J4, H2); g = []; base = 8; y = {}
        for b in range(2):
            gg, oo = circ_J4([2 * j + b for j in range(4)], base); g += gg; base += 7
            for i in range(4): y[(i, b)] = oo[i]
        outs = []
        for i in range(4):
            g.append((y[(i, 0)], y[(i, 1)], 1., 1.)); outs.append(base); base += 1
            g.append((y[(i, 0)], y[(i, 1)], 1., -1.)); outs.append(base); base += 1
        return T, g, outs
    if name == 'H16':
        T = np.kron(J4, J4); g = []; base = 16; y = {}
        for b in range(4):
            gg, oo = circ_J4([4 * j + b for j in range(4)], base); g += gg; base += 7
            for i in range(4): y[(i, b)] = oo[i]
        outs = [None] * 16
        for i in range(4):
            gg, oo = circ_J4([y[(i, b)] for b in range(4)], base); g += gg; base += 7
            for a in range(4): outs[4 * i + a] = oo[a]
        return T, g, outs
    if name in ('Z4', 'Z8', 'Z16'):
        k = {'Z4': 2, 'Z8': 3, 'Z16': 4}[name]; n = 1 << k
        T = kp(Z2, k); cur = list(range(n)); g = []; base = n
        for bit in range(k):
            for i in range(n):
                if i >> bit & 1:
                    g.append((cur[i], cur[i ^ (1 << bit)], 1., 1.)); cur[i] = base; base += 1
        return T, g, cur
    if name == 'K8':      # generic cousin: entries 2^(Hamming distance); no known circuit supplied
        return kp(np.array([[1, 2], [2, 1.]]), 3), [], []
    if name == 'K4':
        return kp(np.array([[1, 2], [2, 1.]]), 2), [], []
    if name.startswith('H8r'):   # a subset of the rows of the 8-point transform, e.g. H8r0246
        T = np.kron(J4, H2); return T[[int(ch) for ch in name[3:]]], [], []
    if name == 'H8c4':    # 8-point transform when only inputs 0..3 can be non-zero is trivial; instead: outputs 0..3 of H8 on all inputs
        T = kp(H2, 3); return T[:4], [], []
    if name == 'Z8H':   # subset-sum matrix times its transpose pattern is not needed; placeholder
        raise SystemExit('no')
    raise SystemExit('unknown task')

def feval(wiring, outs, T, p):
    R, P = p.shape; n = T.shape[1]; K = len(wiring)
    M = np.zeros((R, n + K, n)); M[:, :n, :] = np.eye(n)
    J = np.zeros((R, n + K, n, P))
    for k, (u, v) in enumerate(wiring):
        a = p[:, 2 * k][:, None]; b = p[:, 2 * k + 1][:, None]
        M[:, n + k] = a * M[:, u] + b * M[:, v]
        J[:, n + k] = a[:, :, None] * J[:, u] + b[:, :, None] * J[:, v]
        J[:, n + k, :, 2 * k] += M[:, u]; J[:, n + k, :, 2 * k + 1] += M[:, v]
    r = (M[:, outs, :] - T).reshape(R, -1)
    Jr = J[:, outs].reshape(R, -1, P)
    return r, Jr, M

def lm(wiring, outs, T, p, iters, giveup=None):
    R, P = p.shape
    r, J, M = feval(wiring, outs, T, p); c = (r * r).sum(1); lam = np.full(R, 1e-2)
    idx = np.arange(P)
    for it in range(iters):
        A = np.einsum('rij,rik->rjk', J, J); g = np.einsum('rij,ri->rj', J, r)
        d = A[:, idx, idx]
        A[:, idx, idx] = d + lam[:, None] * (d + 1e-9)
        try:
            step = np.linalg.solve(A, -g[:, :, None])[:, :, 0]
        except np.linalg.LinAlgError:
            lam *= 10; continue
        p2 = p + step
        r2, J2, M2 = feval(wiring, outs, T, p2); c2 = (r2 * r2).sum(1)
        ok = np.isfinite(c2) & (c2 < c)
        p[ok] = p2[ok]; r[ok] = r2[ok]; J[ok] = J2[ok]; M[ok] = M2[ok]; c[ok] = c2[ok]
        lam = np.where(ok, lam * 0.3, lam * 6); lam = np.clip(lam, 1e-14, 1e8)
        if c.min() < 1e-26: break
        if giveup is not None and it == giveup[0] and c.min() > giveup[1]: break
    return p, c, M

def supports_ok(wiring, outs, T):
    n = T.shape[1]; s = [1 << i for i in range(n)]
    for (u, v) in wiring: s.append(s[u] | s[v])
    used = set(outs)
    for (u, v) in wiring: used.add(u); used.add(v)
    for k in range(len(wiring)):
        if n + k not in used: return False
        if wiring[k][0] == wiring[k][1]: return False
    for j, o in enumerate(outs):
        t = sum(1 << i for i in range(n) if T[j, i] != 0)
        if t & ~s[o]: return False
    return len(set(outs)) == len(outs)

def energy(wiring, outs, T, warm, rng, R=6, iters=18):
    P = 2 * len(wiring); p = np.empty((R, P))
    h = R // 2
    if warm is not None and warm.shape[0] == P:
        for i in range(h): p[i] = warm + rng.normal(size=P) * [0.0, 0.05, 0.5, 1.0][i % 4]
    else:
        h = 0
    for i in range(h, R):
        p[i] = rng.normal(size=P) * np.exp(rng.normal(size=P) * rng.choice([0.3, 1.0, 2.5]))
    p, c, M = lm(wiring, outs, T, p, iters, giveup=(7, 0.5))
    i = int(np.argmin(c))
    if 1e-26 < c[i] < 1e-3:
        pp, cc, MM = lm(wiring, outs, T, p[i:i + 1].copy(), 300)
        return float(cc[0]), pp[0], MM[0]
    return float(c[i]), p[i].copy(), M[i].copy()

def mutate(wiring, outs, n, rng, T):
    w = [list(x) for x in wiring]; o = list(outs); K = len(w)
    m = rng.random()
    if m < 0.65:
        k = rng.integers(K); s = rng.integers(2)
        w[k][s] = int(rng.integers(n + k))
    elif m < 0.8:
        j = rng.integers(len(o)); lo = 0 if (T[j] != 0).sum() == 1 else n
        o[j] = int(rng.integers(lo, n + K))
    elif m < 0.9:
        i, j = rng.integers(len(o), size=2); o[i], o[j] = o[j], o[i]
    else:
        for _ in range(2):
            k = rng.integers(K); s = rng.integers(2); w[k][s] = int(rng.integers(n + k))
    return [tuple(x) for x in w], o

def delete_gate(gates, outs, n, d, rng):
    """remove gate d; users are rewired to one of its inputs; an output that pointed at it goes to a random gate"""
    u0, v0 = gates[d][0], gates[d][1]; dead = n + d
    def fix(x):
        if x == dead: x = int(rng.choice([u0, v0]))
        return x - 1 if x > dead else x
    g2 = [(fix(u), fix(v), a, b) for i, (u, v, a, b) in enumerate(gates) if i != d]
    K2 = len(g2)
    o2 = [(int(rng.integers(n, n + K2)) if x == dead else (x - 1 if x > dead else x)) for x in outs]
    return g2, o2

def frac_replay(wiring, outs, T, M):
    """normalise each node row (largest entry = 1), rationalise, solve each gate exactly, check outputs."""
    n = T.shape[1]; rows = []
    for k in range(M.shape[0]):
        r = M[k]; m = r[np.argmax(np.abs(r))]
        if abs(m) < 1e-12: return None, 'zero row'
        rows.append([Fraction(float(x / m)).limit_denominator(96) for x in r])
        if max(abs(float(rows[-1][i]) - r[i] / m) for i in range(n)) > 1e-7: return None, 'not small rationals'
    coef = []
    for k, (u, v) in enumerate(wiring):
        ru, rv, rk = rows[u], rows[v], rows[n + k]; sol = None
        for i in range(n):
            for j in range(i + 1, n):
                det = ru[i] * rv[j] - ru[j] * rv[i]
                if det != 0:
                    a = (rk[i] * rv[j] - rk[j] * rv[i]) / det; b = (ru[i] * rk[j] - ru[j] * rk[i]) / det
                    sol = (a, b); break
            if sol: break
        if sol is None: return None, 'parallel operands'
        a, b = sol
        if any(a * ru[i] + b * rv[i] != rk[i] for i in range(n)): return None, 'gate %d inconsistent' % k
        coef.append((str(a), str(b)))
    for j, o in enumerate(outs):
        t = [Fraction(int(x)) for x in T[j]]; r = rows[o]
        piv = next(i for i in range(n) if t[i] != 0); s = r[piv] / t[piv]
        if s == 0 or any(r[i] != s * t[i] for i in range(n)): return None, 'output %d not proportional' % j
    return {'rows': [[str(x) for x in r] for r in rows], 'coef': coef}, 'exact'

def family_dim(wiring, outs, T, p):
    r, J, M = feval(wiring, outs, T, p[None, :].copy())
    sv = np.linalg.svd(J[0], compute_uv=False)
    rank = int((sv > 1e-7 * sv[0]).sum())
    aux = len(wiring) - len([o for o in set(outs) if o >= T.shape[1]])
    return 2 * len(wiring) - rank - aux, rank

def main():
    name, K, secs, seed, outdir = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    mode = sys.argv[6] if len(sys.argv) > 6 else 'seed'
    temp = float(sys.argv[7]) if len(sys.argv) > 7 else 0.6
    rng = np.random.default_rng(seed); T, gates, outs0 = task(name); n = T.shape[1]
    os.makedirs(outdir, exist_ok=True)
    tag = '%s_K%d_s%d_%s' % (name, K, seed, mode); fo = open(os.path.join(outdir, tag + '.jsonl'), 'w')
    t0 = time.time(); seen = set(); nsol = 0; nnear = 0; nev = 0; hist = {}
    def fresh():
        if mode == 'seed':
            g, o = list(gates), list(outs0)
            while len(g) > K:
                g, o = delete_gate(g, o, n, int(rng.integers(len(g))), rng)
            while len(g) < K:   # pad with a random extra gate at the end
                g.append((int(rng.integers(n + len(g))), int(rng.integers(n + len(g))), 1., 1.))
            w = [(u, v) for (u, v, a, b) in g]; warm = np.array([x for (u, v, a, b) in g for x in (a, b)])
            return w, o, warm
        w = [(int(rng.integers(n + k)), int(rng.integers(n + k))) for k in range(K)]
        o = [int(x) for x in rng.choice(np.arange(n, n + K), size=T.shape[0], replace=False)] if K >= T.shape[0] else \
            [int(x) for x in rng.choice(np.arange(0, n + K), size=T.shape[0], replace=False)]
        return w, o, None
    w, o, warm = fresh(); tries = 0
    while not supports_ok(w, o, T) and tries < 20000: w, o, warm = fresh(); tries += 1
    E, p, M = energy(w, o, T, warm, rng); E = math.log10(E + 1e-30); since = 0
    while time.time() - t0 < secs:
        w2, o2 = mutate(w, o, n, rng, T)
        if (w2 == w and o2 == o) or not supports_ok(w2, o2, T): continue
        c2, p2, M2 = energy(w2, o2, T, p, rng); E2 = math.log10(c2 + 1e-30); nev += 1
        b = int(max(-30, min(2, math.floor(E2)))); hist[b] = hist.get(b, 0) + 1
        if E2 < -6:
            key = (tuple(w2), tuple(o2))
            if key not in seen:
                seen.add(key)
                rec = {'task': name, 'K': K, 'wiring': w2, 'outs': o2, 'log10res2': E2, 'params': [float(x) for x in p2],
                       'maxabs': float(np.abs(p2).max()), 'minabs': float(np.abs(p2).min()), 't': time.time() - t0}
                if E2 < -20:
                    ex, why = frac_replay(w2, o2, T, M2); rec['kind'] = 'zero'; rec['replay'] = why; rec['exact'] = ex
                    rec['family_dim'], rec['jac_rank'] = family_dim(w2, o2, T, p2); nsol += 1
                else:
                    rec['kind'] = 'near'; nnear += 1
                    Mn = M2 / np.abs(M2).max(axis=1, keepdims=True); rec['rows'] = [[round(float(x), 6) for x in r] for r in Mn]
                fo.write(json.dumps(rec) + '\n'); fo.flush()
        if E2 <= E or rng.random() < math.exp(-(max(E2, -4) - max(E, -4)) / temp):
            since = 0 if E2 < E - 1e-9 else since + 1
            w, o, p, E = w2, o2, p2, E2
        else:
            since += 1
        if since > 400 or (E < -20 and since > 40):
            w, o, warm = fresh(); tries = 0
            while not supports_ok(w, o, T) and tries < 20000: w, o, warm = fresh(); tries += 1
            E, p, M = energy(w, o, T, warm, rng); E = math.log10(E + 1e-30); since = 0
    fo.write(json.dumps({'summary': tag, 'evaluated': nev, 'zeros': nsol, 'near': nnear,
                         'hist_log10res2': {str(k): hist[k] for k in sorted(hist)}}) + '\n'); fo.close()
    print(tag, 'evaluated', nev, 'zeros', nsol, 'near', nnear, 'hist', {k: hist[k] for k in sorted(hist)}, flush=True)

if __name__ == '__main__':
    main()
