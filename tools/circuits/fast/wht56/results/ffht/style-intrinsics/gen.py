#!/usr/bin/env python3
"""gen.py -- write plans.inc from plans.json.

    python3 gen.py              (reads plans.json, writes plans.inc, prints a summary)
    python3 gen.py --from-baseline ../baseline/ffht_structure.json     (rewrites plans.json first)

plans.json is the pass plan of every size, 2^3 .. 2^30, floats and doubles: for each size the
passes in the order they run, each as [depth, levels, registers, distance].  It is FFHT's own
plan (the one its generator kept for each size, file hall_of_fame_avx.txt of FFHT; here taken
from the baseline's reading of FFHT's generated code, baseline/ffht_structure.json).  Only the
plan is taken: which levels go into which pass, and which block is finished before the next.

plans.inc is C text for impl.inc: for every size one function per recursion depth,

    depth = the base block:   the passes of the base block, one after the other;
    a larger depth d:         the function of the depth below on each part, then one pass.

P = the number of passes that take 8 registers through 3 levels (the passes that use the 8-point
step); every number goes through each of them once.  The one at the highest levels is written
PASS3L / FIRST8L and gets P; the others are PASS3 / FIRST8.
"""
import json
import sys

W = {'float': 8, 'double': 4}
LW = {'float': 3, 'double': 2}


def from_baseline(path):
    src = json.load(open(path))
    out = {'float': {}, 'double': {}}
    for e in src:
        k = e['log_n']
        if k < 3 or e['kind'] == 'plain C':
            continue
        passes = []
        for p in e['passes']:
            depth = p['depth'] if p['depth'] is not None else k
            passes.append([depth, len(p['levels']), p['registers'], p['stride'] if p['stride'] else W[e['type']]])
        out[e['type']][str(k)] = passes
    json.dump(out, open('plans.json', 'w'), indent=None, separators=(',', ':'))
    open('plans.json', 'a').write('\n')


def check(typ, k, passes):
    """the passes must do every level 0..k-1 exactly once, in rising order"""
    lw, w = LW[typ], W[typ]
    level = 0
    for n, (depth, nlev, reg, dist) in enumerate(passes):
        if n == 0:
            assert dist == w and nlev == lw + {1: 0, 2: 1, 4: 2, 8: 3}[reg], (typ, k, passes)
        else:
            assert dist == 1 << level and nlev == {2: 1, 4: 2, 8: 3}[reg], (typ, k, passes)
        level += nlev
        assert level <= depth, (typ, k, passes)
    assert level == k, (typ, k, passes)
    depths = sorted(set(p[0] for p in passes))
    assert depths[-1] == k
    for d in depths[1:]:
        assert len([p for p in passes if p[0] == d]) == 1       # one pass per recursion depth
    return depths


def emit(typ, k, passes, out, summary):
    depths = check(typ, k, passes)
    kern = [i for i, p in enumerate(passes) if p[2] == 8]
    P = len(kern)
    last = kern[-1] if kern else None
    text = []
    for di, d in enumerate(depths):
        body = []
        if di > 0:
            sub = depths[di - 1]
            parts = 1 << (d - sub)
            body.append('for (int i = 0; i < %d; i++) FN(k%d_d%d)(buf + (size_t)i * %d);' % (parts, k, sub, 1 << sub))
        for i, (depth, nlev, reg, dist) in enumerate(passes):
            if depth != d:
                continue
            n = 1 << d
            if i == 0:
                if reg == 8:
                    body.append('FIRST8L(buf, %d, %d);' % (n, P) if i == last else 'FIRST8(buf, %d);' % n)
                else:
                    body.append('FIRST%d(buf, %d);' % (reg, n))
            elif reg == 8:
                body.append('PASS3L(buf, %d, %d, %d);' % (n, dist, P) if i == last else 'PASS3(buf, %d, %d);' % (n, dist))
            else:
                body.append('PASS%d(buf, %d, %d);' % ({2: 1, 4: 2}[reg], n, dist))
        if d == k and P > 0:
            body.append('SWEEP(buf, %d, %d);' % (1 << k, P))
        text.append('%s FN(k%d_d%d)(ELT *buf) { %s }' % ('TOP' if d == k else 'BLOCK', k, d, ' '.join(body)))
    out.append('/* %s 2^%d: P = %d; base block 2^%d */' % (typ, k, P, depths[0]))
    out.extend(text)
    summary.append((typ, k, P, depths[0], sum(1 for p in passes), [p[1] for p in passes]))
    return P


def main():
    if len(sys.argv) == 3 and sys.argv[1] == '--from-baseline':
        from_baseline(sys.argv[2])
    plans = json.load(open('plans.json'))
    out = ['/* plans.inc -- written by gen.py from plans.json.  Do not edit.  See gen.py. */']
    summary = []
    for typ, guard in (('float', 'PLAN_FLOAT'), ('double', 'PLAN_DOUBLE')):
        out.append('#ifdef %s' % guard)
        Ps = {}
        for k in range(3, 31):
            Ps[k] = emit(typ, k, plans[typ][str(k)], out, summary)
        out.append('void NAME(ELT *buf, int k)')
        out.append('{')
        out.append('    switch (k) {')
        for k in range(3, 31):
            out.append('    case %d: FN(k%d_d%d)(buf); break;' % (k, k, k))
        out.append('    default: break;')
        out.append('    }')
        out.append('}')
        out.append('#endif')
        out.append('#ifdef PLAN_P_%s' % typ.upper())
        out.append('/* P for 2^0 .. 2^30 %ss: the number of 8-register passes */' % typ)
        out.append('static const signed char plan_P_%s[31] = {%s};' % (typ, ', '.join(str(Ps.get(k, -1)) for k in range(31))))
        out.append('#endif')
    open('plans.inc', 'w').write('\n'.join(out) + '\n')
    for typ, k, P, base, np, levs in summary:
        print('%-6s 2^%-2d P=%d base=2^%-2d passes=%d levels per pass=%s' % (typ, k, P, base, np, levs))


main()
