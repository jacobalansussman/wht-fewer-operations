#!/usr/bin/env python3
"""steiner.py -- search over AUXILIARY forms only; the outputs complete themselves.  Count (G).
State: a list of gates  node = u + c*v  (c from a small pool of rationals, large and small on purpose).
Energy U = (gates built) + sum over targets t of d(t),  d(t) = (fewest current nodes whose span contains t) - 1,
exact for spans of up to 4 nodes.  U is the size of an honest circuit: build the nodes, then finish each target alone.
Annealing on U (add / delete / change a gate).  Every new best is replayed exactly in Fractions.
usage: steiner.py <task> <seconds> <seed> <outdir> [mode: empty|seed] [temp] [goal]
"""
import numpy as np, sys, json, time, os, math, itertools
from fractions import Fraction as F
import slp

COEFS = [1, -1, 1, -1, 2, -2, 0.5, -0.5, 3, -3, 1 / 3, -1 / 3, 4, -4, 0.25, -0.25, 1.5, -1.5, 8, -8, 0.125, -0.125]
_subs = {}

def subsets(m, k):
    if (m, k) not in _subs: _subs[(m, k)] = np.array(list(itertools.combinations(range(m), k)), dtype=np.int64)
    return _subs[(m, k)]

def build(n, gates):
    M = [np.eye(n)[i] for i in range(n)]
    for (u, v, c) in gates: M.append(M[u] + c * M[v])
    return np.array(M)

def dists(M, T, maxk=4):
    nt = T.shape[0]; m = M.shape[0]
    nr = np.linalg.norm(M, axis=1); nr = np.where(nr > 1e-12, nr, 1.0); A = M / nr[:, None]
    Tn = T / np.linalg.norm(T, axis=1)[:, None]
    d = np.full(nt, -1); comp = [None] * nt
    C = np.abs(A @ Tn.T)                                     # m x nt
    for t in range(nt):
        i = int(np.argmax(C[:, t]))
        if C[i, t] > 1 - 1e-9: d[t] = 0; comp[t] = [i]
    for k in range(2, maxk + 1):
        if (d >= 0).all(): break
        I = subsets(m, k); S = A[I]                           # S: (#,k,n)
        G = S @ S.transpose(0, 2, 1); B = S @ Tn.T            # (#,k,k), (#,k,nt)
        X = np.linalg.pinv(G, rcond=1e-9, hermitian=True) @ B
        res = 1.0 - (B * X).sum(1)                            # (#,nt)
        for t in range(nt):
            if d[t] < 0:
                j = int(np.argmin(res[:, t]))
                if res[j, t] < 1e-9: d[t] = k - 1; comp[t] = [int(x) for x in I[j]]
    for t in range(nt):
        if d[t] < 0:                                          # greedy fallback (an upper bound)
            r = Tn[t].copy(); sel = []
            while np.linalg.norm(r) > 1e-7 and len(sel) < M.shape[1] + 2:
                c = np.abs(A @ r); c[sel] = -1; sel.append(int(np.argmax(c)))
                Q = A[sel]; x = np.linalg.lstsq(Q.T, Tn[t], rcond=None)[0]; r = Tn[t] - Q.T @ x
            d[t] = max(maxk, len(sel) - 1); comp[t] = sel
    return d, comp

def solve_exact(rows, t):
    k = len(rows); n = len(t); A = [[rows[j][i] for j in range(k)] + [t[i]] for i in range(n)]
    piv = []; r = 0
    for c in range(k):
        p = next((i for i in range(r, n) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]; A[r] = [x / A[r][c] for x in A[r]]
        for i in range(n):
            if i != r and A[i][c] != 0: A[i] = [x - A[i][c] * y for x, y in zip(A[i], A[r])]
        piv.append(c); r += 1
    if any(A[i][k] != 0 for i in range(r, n)): return None
    x = [F(0)] * k
    for i, c in enumerate(piv): x[c] = A[i][k]
    return x

def exact_replay(n, gates, T, comp):
    rows = [[F(int(i == j)) for j in range(n)] for i in range(n)]; prog = []
    for (u, v, c) in gates:
        cf = F(c).limit_denominator(1000); rows.append([rows[u][j] + cf * rows[v][j] for j in range(n)])
        prog.append('n%d = n%d + (%s)*n%d' % (len(rows) - 1, u, cf, v))
    total = len(gates)
    for t in range(T.shape[0]):
        tt = [F(int(x)) for x in T[t]]; sub = comp[t]
        x = solve_exact([rows[s] for s in sub], tt)
        if x is None: return None, None
        used = [(s, c) for s, c in zip(sub, x) if c != 0]
        total += max(0, len(used) - 1)
        prog.append('out%d = ' % t + ' + '.join('(%s)*n%d' % (c, s) for s, c in used))
    return total, prog

def main():
    name, secs, seed, outdir = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    mode = sys.argv[5] if len(sys.argv) > 5 else 'empty'
    temp = float(sys.argv[6]) if len(sys.argv) > 6 else 0.45
    rng = np.random.default_rng(seed); T, known, outs0 = slp.task(name); n = T.shape[1]
    os.makedirs(outdir, exist_ok=True); tag = 'steiner_%s_s%d_%s' % (name, seed, mode)
    fo = open(os.path.join(outdir, tag + '.jsonl'), 'w'); t0 = time.time()
    def start():
        if mode == 'seed':
            return [(u, v, b / a) for (u, v, a, b) in known]
        return []
    def U(g):
        M = build(n, g); d, comp = dists(M, T, 4 if n <= 8 else 3); return len(g) + int(d.sum()), d, comp
    g = start(); E, d, comp = U(g); best = 10 ** 9; nev = 0; hist = {}; shapes = {}
    cap = int(sys.argv[7]) if len(sys.argv) > 7 else 10 ** 9
    last_improve = time.time()
    while time.time() - t0 < secs:
        g2 = list(g); m = rng.random(); K = len(g2)
        if m < 0.4 or K == 0:
            u, v = rng.choice(n + K, size=2, replace=False)
            if rng.random() < 0.5 and K > 0: u = n + K - 1 - int(rng.integers(min(K, 3)))
            if u == v: continue
            g2.append((int(u), int(v), float(rng.choice(COEFS))))
        elif m < 0.65:
            k = int(rng.integers(K)); u0, v0, _ = g2[k]; dead = n + k
            def fx(x):
                if x == dead: x = int(rng.choice([u0, v0]))
                return x - 1 if x > dead else x
            g2 = [(fx(u), fx(v), c) for i, (u, v, c) in enumerate(g2) if i != k]
            if any(u == v for (u, v, c) in g2): continue
        else:
            k = int(rng.integers(K)); u, v, c = g2[k]; s = rng.random()
            if s < 0.4: c = float(rng.choice(COEFS))
            elif s < 0.7: u = int(rng.integers(n + k))
            else: v = int(rng.integers(n + k))
            if u == v: continue
            g2[k] = (u, v, c)
        if len(g2) > 40: continue
        E2, d2, comp2 = U(g2); nev += 1; hist[E2] = hist.get(E2, 0) + 1
        if E2 <= E or rng.random() < math.exp(-(E2 - E) / temp):
            g, E, d, comp = g2, E2, d2, comp2
            if E <= best + 1:
                key = tuple(sorted(tuple(np.round(r / r[np.argmax(np.abs(r))], 6)) for r in build(n, g)[n:]))
                if key not in shapes and len(shapes) < 4000:
                    total, prog = exact_replay(n, g, T, comp)
                    shapes[key] = E
                    rec = {'task': name, 'U': E, 'exact_total': total, 'aux_gates': len(g), 'dists': [int(x) for x in d],
                           'gates': g, 'comp': comp, 'prog': prog, 't': round(time.time() - t0, 1)}
                    fo.write(json.dumps(rec) + '\n'); fo.flush()
                    if E < best: best = E; last_improve = time.time(); print(tag, 'best', best, 'exact', total, 't', round(time.time() - t0, 1), flush=True)
        if time.time() - last_improve > 90 and mode != 'seed':
            g = start(); E, d, comp = U(g); last_improve = time.time()
    fo.write(json.dumps({'summary': tag, 'evaluated': nev, 'best': best, 'hist_U': {str(k): hist[k] for k in sorted(hist)}}) + '\n')
    fo.close(); print(tag, 'DONE evaluated', nev, 'best', best, 'hist', {k: hist[k] for k in sorted(hist)[:8]}, flush=True)

if __name__ == '__main__':
    main()
