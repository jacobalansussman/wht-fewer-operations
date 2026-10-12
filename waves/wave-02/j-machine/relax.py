#!/usr/bin/env python3
"""relax.py -- the wiring itself made continuous.  Count (G).
Every gate starts as a dense combination of ALL earlier nodes; a 'trimmed' L1 pressure (free on a gate's two largest
weights, soft-threshold on the rest, ramped up) squeezes each gate down to two operands; then the hard circuit is polished
by Levenberg-Marquardt (slp.lm) and anything that reaches zero is replayed exactly in Fractions (slp.frac_replay).
usage: relax.py <task> <K> <seconds> <seed> <outdir> [batch] [steps]
"""
import numpy as np, sys, json, time, os, math
import slp

def one_round(T, K, B, steps, rng, lr=0.02, lam_max=0.05):
    n = T.shape[1]
    free = [j for j in range(T.shape[0]) if (T[j] != 0).sum() == 1]       # targets that are inputs: free
    tj = [j for j in range(T.shape[0]) if j not in free]
    pos = np.sort(rng.choice(K, size=len(tj), replace=False)) if rng.random() < 0.5 else np.arange(K - len(tj), K)
    perm = rng.permutation(len(tj)); out_nodes = [0] * T.shape[0]
    for i, j in enumerate(perm): out_nodes[tj[j]] = int(n + pos[i])
    for j in free: out_nodes[j] = int(np.argmax(np.abs(T[j])))
    on = np.array([out_nodes[j] for j in tj]); Tt = T[tj]
    isout = np.zeros(n + K, bool); isout[on] = True
    nodes = n + K
    mask = np.zeros((K, nodes));
    for k in range(K): mask[k, :n + k] = 1
    W = rng.normal(size=(B, K, nodes)) * rng.choice([0.2, 0.5]) * mask
    m = np.zeros_like(W); v = np.zeros_like(W)
    for t in range(1, steps + 1):
        M = np.zeros((B, nodes, n)); M[:, :n] = np.eye(n)
        for k in range(K):
            M[:, n + k] = np.einsum('bj,bjn->bn', W[:, k, :n + k], M[:, :n + k])
        G = np.zeros((B, nodes, n)); G[:, on] = 2 * (M[:, on] - Tt)
        gW = np.zeros_like(W)
        for k in range(K - 1, -1, -1):
            g = G[:, n + k]
            gW[:, k, :n + k] = np.einsum('bjn,bn->bj', M[:, :n + k], g)
            G[:, :n + k] += W[:, k, :n + k, None] * g[:, None, :]
        m = 0.9 * m + 0.1 * gW; v = 0.999 * v + 0.001 * gW * gW
        W -= lr * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-8) * mask
        frac = t / steps
        lam = lam_max * max(0.0, (frac - 0.15) / 0.7) if frac < 0.85 else lam_max * 4
        if lam > 0:
            a = np.abs(W); kth = np.partition(a, -2, axis=-1)[..., -2:-1]
            keep = a >= kth
            W = np.where(keep, W, np.sign(W) * np.maximum(a - lr * lam * 20, 0))
        if t % 50 == 0:      # gauge: give auxiliary rows norm 1 (exact, loss unchanged)
            M = np.zeros((B, nodes, n)); M[:, :n] = np.eye(n)
            for k in range(K):
                M[:, n + k] = np.einsum('bj,bjn->bn', W[:, k, :n + k], M[:, :n + k])
                if not isout[n + k]:
                    s = np.linalg.norm(M[:, n + k], axis=1); s = np.where(s > 1e-9, s, 1.0)
                    W[:, k, :] /= s[:, None]; M[:, n + k] /= s[:, None]; W[:, k + 1:, n + k] *= s[:, None]
    # harden
    res = []
    a = np.abs(W); idx = np.argsort(a, axis=-1)[..., -2:]
    for b in range(B):
        wiring = []; pl = []
        for k in range(K):
            u, v = int(idx[b, k, 1]), int(idx[b, k, 0]); a_, b_ = float(W[b, k, u]), float(W[b, k, v])
            if u >= n + k: u, a_ = 0, 0.0
            if v >= n + k: v, b_ = (1 if u == 0 else 0), 0.0
            wiring.append((u, v)); pl += [a_, b_]
        p = np.array(pl)[None, :]
        r, J, Mh = slp.feval(wiring, out_nodes, T, p.copy())
        res.append((float((r * r).sum()), b, wiring, p[0]))
    res.sort(key=lambda x: x[0])
    return res, out_nodes

def main():
    name, K, secs, seed, outdir = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    B = int(sys.argv[6]) if len(sys.argv) > 6 else 64
    steps = int(sys.argv[7]) if len(sys.argv) > 7 else 3000
    rng = np.random.default_rng(seed); T, gates, outs0 = slp.task(name); n = T.shape[1]
    os.makedirs(outdir, exist_ok=True); tag = 'relax_%s_K%d_s%d' % (name, K, seed)
    fo = open(os.path.join(outdir, tag + '.jsonl'), 'w'); t0 = time.time()
    hist = {}; hard = {}; rounds = 0; zeros = 0; near = 0; seen = set()
    while time.time() - t0 < secs:
        res, outs = one_round(T, K, B, steps, rng); rounds += 1
        for (c, b, wiring, p) in res:
            hb = int(max(-30, min(3, math.floor(math.log10(c + 1e-30))))); hard[hb] = hard.get(hb, 0) + 1
        for (c, b, wiring, p) in res[:12]:
            if not np.isfinite(c): continue
            pp, cc, MM = slp.lm(wiring, outs, T, p[None, :].copy(), 250)
            E = math.log10(float(cc[0]) + 1e-30); hb = int(max(-30, min(3, math.floor(E)))); hist[hb] = hist.get(hb, 0) + 1
            if E < -5:
                key = (tuple(wiring), tuple(outs))
                if key in seen: continue
                seen.add(key)
                rec = {'task': name, 'K': K, 'wiring': wiring, 'outs': outs, 'log10res2': E, 'params': [float(x) for x in pp[0]],
                       'maxabs': float(np.abs(pp[0]).max()), 'minabs': float(np.abs(pp[0]).min()), 't': time.time() - t0}
                Mn = MM[0] / (np.abs(MM[0]).max(axis=1, keepdims=True) + 1e-300)
                rec['rows'] = [[round(float(x), 6) for x in r] for r in Mn]
                if E < -20:
                    ex, why = slp.frac_replay(wiring, outs, T, MM[0]); rec['kind'] = 'zero'; rec['replay'] = why; rec['exact'] = ex
                    rec['family_dim'], rec['jac_rank'] = slp.family_dim(wiring, outs, T, pp[0]); zeros += 1
                    used = set(outs)
                    for (u, v) in wiring: used.add(u); used.add(v)
                    rec['gates_used'] = sum(1 for k in range(K) if n + k in used)
                else:
                    rec['kind'] = 'near'; near += 1
                fo.write(json.dumps(rec) + '\n'); fo.flush()
    fo.write(json.dumps({'summary': tag, 'rounds': rounds, 'batch': B, 'steps': steps, 'zeros': zeros, 'near': near,
                         'hist_polished_best12': {str(k): hist[k] for k in sorted(hist)},
                         'hist_hardened_all': {str(k): hard[k] for k in sorted(hard)}}) + '\n'); fo.close()
    print(tag, 'rounds', rounds, 'zeros', zeros, 'near', near, 'polished', {k: hist[k] for k in sorted(hist)},
          'hard', {k: hard[k] for k in sorted(hard)}, flush=True)

if __name__ == '__main__':
    main()
