#!/usr/bin/env python3
"""summarize.py -- one table from formal/RESULTS.jsonl and formal/RESULTS_SEQ.jsonl
(the last record of every proof is the one that counts).  Writes formal/SUMMARY.md."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        return []
    return [json.loads(l) for l in open(p) if l.strip()]


def main():
    comb = {}
    ctl = []
    for r in load('RESULTS.jsonl'):
        if r['step'].startswith('control'):
            ctl.append(r)
        else:
            comb[(r['size'], r['design'], r['W'], r['step'], r['solver'])] = r
    seq = {}
    sctl = []
    for r in load('RESULTS_SEQ.jsonl'):
        if r['variant'].startswith('control'):
            sctl.append(r)
        else:
            seq[(r['size'], r['design'], r['W'], r['variant'])] = r
    order = {'8': 0, '16': 1, '64': 2, '8x8': 3}
    keys = sorted(set((k[0], k[1], k[2]) for k in comb), key=lambda k: (order[k[0]], k[2], k[1] != 'textbook', k[1]))
    o = []
    o.append('## Combinational variant (c) against the definition')
    o.append('')
    o.append('| size | design | W | step A: design = wide (bitwuzla) | step B: wide = definition (z3) | second opinion on B (yices, 30 s) | result |')
    o.append('|---|---|---|---|---|---|---|')
    for size, design, W in keys:
        def cell(step, solver):
            r = comb.get((size, design, W, step, solver))
            return '-' if r is None else '%s, %.1f s' % (r['verdict'], r['seconds'])
        ra = comb.get((size, design, W, 'A', 'bitwuzla'))
        rb = comb.get((size, design, W, 'B', 'z3'))
        ok = ra and rb and ra['verdict'] == 'PASSED' and rb['verdict'] == 'PASSED'
        y = cell('B', 'yices')
        rp = comb.get((size, design, W, 'B', 'yices-per-output'))
        if rp is not None:
            y += '; one output at a time: %s (%s outputs), %.1f s' % (rp['verdict'], rp['outputs_passed'], rp['seconds'])
        o.append('| %s | %s | %d | %s | %s | %s | %s |' % (size, design, W, cell('A', 'bitwuzla'), cell('B', 'z3'),
                                                       y, '**proved**' if ok else 'not proved (simulated only)'))
    o.append('')
    o.append('Controls (a damaged design; the solver must find an input that shows the damage):')
    o.append('')
    for r in ctl:
        o.append('- %s points, %s, W = %d: %s. Solver %s: %s in %.1f s.'
                 % (r['size'], r['design'], r['W'], r['claim'], r['solver'], r['verdict'], r['seconds']))
    o.append('')
    o.append('## Variants with registers (p, p2, r) against the combinational variant, delayed')
    o.append('')
    o.append('| size | design | W | p | p2 | r |')
    o.append('|---|---|---|---|---|---|')
    keys = sorted(set((k[0], k[1], k[2]) for k in seq), key=lambda k: (order[k[0]], k[2], k[1] != 'textbook', k[1]))
    for size, design, W in keys:
        def cell(v):
            r = seq.get((size, design, W, v))
            return '-' if r is None else '%s, latency %d, %.0f s' % (r['verdict'], r['latency'], r['seconds'])
        o.append('| %s | %s | %d | %s | %s | %s |' % (size, design, W, cell('p'), cell('p2'), cell('r')))
    o.append('')
    if sctl:
        o.append('Controls:')
        o.append('')
        for r in sctl:
            o.append('- %s points, %s, W = %d: %s: %s in %.0f s.' % (r['size'], r['design'], r['W'], r['claim'],
                                                                 r['verdict'], r['seconds']))
        o.append('')
    r3 = {}
    c3 = []
    for r in load('RESULTS3.jsonl'):
        if r['step'].startswith('control'):
            c3.append(r)
        else:
            r3[(r['size'], r['design'], r['W'], r['step'], r['solver'])] = r
    if r3:
        o.append('## Combinational variant (c) against the definition, in three steps (run_formal3.py)')
        o.append('')
        o.append('| size | design | W | A1: every wire of wide fits (z3; yices) | A2: design = wide where every wire fits (bitwuzla) | B: wide = definition (z3; yices) | result |')
        o.append('|---|---|---|---|---|---|---|')
        keys = sorted(set((k[0], k[1], k[2]) for k in r3), key=lambda k: (order[k[0]], k[2], k[1] != 'textbook', k[1]))
        for size, design, W in keys:
            def cell(step, solver):
                r = r3.get((size, design, W, step, solver))
                return '-' if r is None else '%s, %.1f s' % (r['verdict'], r['seconds'])
            yb = cell('B', 'yices')
            rp = r3.get((size, design, W, 'B', 'yices-per-output'))
            if rp is not None:
                yb += '; one output at a time: %s (%s outputs), %.1f s' % (rp['verdict'], rp['outputs_passed'], rp['seconds'])
            ok = all(r3.get((size, design, W, st, sv), {}).get('verdict') == 'PASSED'
                     for st, sv in (('A1', 'z3'), ('A2', 'bitwuzla'), ('B', 'z3')))
            o.append('| %s | %s | %d | %s; %s | %s | %s; %s | %s |'
                     % (size, design, W, cell('A1', 'z3'), cell('A1', 'yices'), cell('A2', 'bitwuzla'),
                        cell('B', 'z3'), yb, '**proved**' if ok else 'not proved (simulated only)'))
        o.append('')
        o.append('Controls:')
        o.append('')
        for r in c3:
            o.append('- %s points, %s, W = %d: %s. Solver %s: %s in %.1f s.'
                     % (r['size'], r['design'], r['W'], r['claim'], r['solver'], r['verdict'], r['seconds']))
        o.append('')
    txt = '\n'.join(o) + '\n'
    with open(os.path.join(HERE, 'SUMMARY.md'), 'w') as f:
        f.write(txt)
    print(txt)


if __name__ == '__main__':
    main()
