#!/usr/bin/env python3
"""greedy.py -- 'steepest drain'.  Count (G).  Potential P = sum over targets of d(t) (see steiner.py); it starts at N(N-1)
for the transform and a gate can lower it by at most N.  At each step try every pair of nodes with coefficients +-1, +-2, +-1/2
and add the node that lowers P most (random among ties).  Prints the drain of every gate: the 'drain profile'.
usage: greedy.py <task> <seed> <outdir> <max seconds>"""
import numpy as np, sys, json, time, os
import slp, steiner
name, seed, outdir, secs = sys.argv[1], int(sys.argv[2]), sys.argv[3], float(sys.argv[4])
rng = np.random.default_rng(seed); T, known, outs0 = slp.task(name); n = T.shape[1]
CO = [1., -1., 2., -2., .5, -.5]
os.makedirs(outdir, exist_ok=True); fo = open(os.path.join(outdir, 'greedy_%s_s%d.jsonl' % (name, seed)), 'w')
g = []; M = steiner.build(n, g); d, comp = steiner.dists(M, T); P = int(d.sum()); t0 = time.time(); prof = []; bestU = P; bestrec = None
while P > 0 and time.time() - t0 < secs and len(g) < 3 * n:
    m = n + len(g); cands = []
    keys = set(tuple(np.round(r / r[np.argmax(np.abs(r))], 6)) for r in M)
    for u in range(m):
        for v in range(u + 1, m):
            for c in CO:
                r = M[u] + c * M[v]
                if np.abs(r).max() < 1e-9: continue
                k = tuple(np.round(r / r[np.argmax(np.abs(r))], 6))
                if k in keys: continue
                keys.add(k); cands.append((u, v, c))
    best = -1; pool = []; drains = {}
    for (u, v, c) in cands:
        if time.time() - t0 > secs: break
        d2, _ = steiner.dists(steiner.build(n, g + [(u, v, c)]), T); dr = P - int(d2.sum()); drains[dr] = drains.get(dr, 0) + 1
        if dr > best: best = dr; pool = [(u, v, c)]
        elif dr == best: pool.append((u, v, c))
    if not pool: break
    u, v, c = pool[int(rng.integers(len(pool)))]; g.append((u, v, c)); M = steiner.build(n, g); d, comp = steiner.dists(M, T); P = int(d.sum())
    step = {'gate': len(g), 'node': [float(x) for x in M[-1]], 'from': [u, v, c], 'drain': best, 'ties': len(pool), 'candidates': len(cands),
            'drain_counts': {str(k): drains[k] for k in sorted(drains, reverse=True)[:4]}, 'P': P, 'U': len(g) + P, 't': round(time.time() - t0, 1)}
    prof.append(best); fo.write(json.dumps(step) + '\n'); fo.flush()
    if len(g) + P <= bestU:
        bestU = len(g) + P; total, prog = steiner.exact_replay(n, g, T, comp); bestrec = {'U': bestU, 'exact_total': total, 'prog': prog, 'profile': list(prof)}
fo.write(json.dumps({'summary': name, 'seed': seed, 'profile': prof, 'bestU': bestU, 'best': bestrec}) + '\n'); fo.close()
print('greedy', name, 'seed', seed, 'bestU', bestU, 'exact', bestrec and bestrec['exact_total'], 'profile', prof, flush=True)
