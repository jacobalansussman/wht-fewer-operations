#!/usr/bin/env python3
"""look.py <dir> [nshow] -- summarise steiner_*.jsonl: best size, number of distinct shapes, the best programs."""
import json, sys, glob, os
d = sys.argv[1]; nshow = int(sys.argv[2]) if len(sys.argv) > 2 else 1
for f in sorted(glob.glob(os.path.join(d, 'steiner_*.jsonl'))):
    recs = [json.loads(l) for l in open(f) if l.strip()]
    b = [r for r in recs if 'U' in r and r.get('exact_total') is not None]; s = [r for r in recs if 'summary' in r]
    if not b: print(os.path.basename(f), 'no records'); continue
    m = min(r['exact_total'] for r in b); best = [r for r in b if r['exact_total'] == m]
    cs = sorted(set(abs(g[2]) for r in best for g in r['gates']))
    print('==', os.path.basename(f), 'best exact size', m, '| distinct shapes at best', len(best), '| next', len([r for r in b if r['exact_total'] == m + 1]),
          '| aux counts', sorted(set(r['aux_gates'] for r in best)), '| |coef| used', cs, '| evaluated', s[0]['evaluated'] if s else '?')
    if s: print('   hist U:', dict(list(s[0]['hist_U'].items())[:6]))
    for r in best[:nshow]:
        print('   dists', r['dists'], 't', r['t']); print('     ' + '\n     '.join(r['prog']))
