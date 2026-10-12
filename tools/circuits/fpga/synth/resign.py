#!/usr/bin/env python3
"""resign.py -- the same circuit with other signs: fewer subtractions for the iCE40.

WHY.  On the iCE40 the carry chain of a logic cell reads the cell's own LUT inputs.  yosys builds
a - b as a + (NOT b) + 1, and NOT b has to be a real signal: one extra LUT per bit of every
operand that is subtracted somewhere.  An addition needs no such LUT.  So on this chip the cost
of a circuit is about  (adder bits) + (bits of the distinct operands that are subtracted).

WHAT.  Every intermediate line g of a circuit may be kept as g or as -g: the adder count, the
depth and the wiring stay the same, only some "+" become "-" and some "-" become "+".
A line  n = c1*u + c2*v  becomes  s_n*n = (s_n*c1*s_u)*(s_u*u) + (s_n*c2*s_v)*(s_v*v);
it stays one adder unless both signs come out negative, which is not allowed.  Outputs keep
their sign.  This program looks for the choice of signs with the smallest
    adder bits + bits of the distinct subtracted operands        (at input width 8),
by trying every choice when there are at most 16 free lines, and by a random local search
otherwise (then the result is "best found", not "best").

It writes resigned/<size>_<design>S.txt (the circuit file, same text format), lets the UNCHANGED
generator ../rtl/gen_rtl.py check it (it refuses a file whose outputs are not the rows of H)
and write the Verilog into v_resigned/, and simulates each file against the checked
combinational file of ../rtl/v (4,000 random vectors and corner vectors).

    python3 -B resign.py
Standard library only; uses iverilog/vvp.  One process.
"""
import itertools
import json
import os
import random
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
RTL = os.path.join(os.path.dirname(HERE), 'rtl')
sys.path.insert(0, RTL)
sys.path.insert(0, HERE)
import gen_rtl as G          # read only: parse_text, to_text, Circuit
import gen_extra as E        # the test bench

REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))      # the top folder of the repository
OUTC = os.path.join(HERE, 'resigned')
OUTV = os.path.join(HERE, 'v_resigned')
TMP = os.path.join(HERE, 'work', 'sim_resigned')
BIN = os.path.join(os.environ.get('OSS_CAD_SUITE', '/opt/oss-cad-suite'), 'bin')      # the unpacked oss-cad-suite

WANT = [('8', 'textbook'), ('8', 'cfl1994'), ('8', 'ar2023'), ('8', 'ours'),
        ('16', 'textbook'), ('16', 'cfl1994'), ('16', 'ours')]
VARIANTS = {'8': ['c', 'p', 'p2', 'p3'], '16': ['c', 'p', 'p2', 'p4']}
WIDTHS = (8, 12, 16)


def src_path(s):
    return os.path.join(REPO, s)


def cost_of(circ, Wd=8):
    """(adder bits, bits of distinct subtracted operands, number of subtractions)"""
    wd = circ.widths(Wd)
    ab = sum(wd[a[0]] for a in circ.adders)
    subs = set()
    nsub = 0
    for node, (sa, A, ka), (sb, B, kb) in circ.adders:
        if sa < 0:
            subs.add(A)
            nsub += 1
        if sb < 0:
            subs.add(B)
            nsub += 1
    return ab, sum(wd[u] for u in subs), nsub


def resign_lines(lines, base, sign):
    """lines with the signs applied; None if some line would have two negative terms.
    base[name] = the adder line (or input) a name stands for; sign[adder line] = +1 or -1."""
    out = []
    for name, terms in lines:
        if len(terms) == 1:
            out.append((name, terms))
            continue
        sn = sign.get(name, 1)
        new = [(sn * c * sign.get(base.get(u, u), 1), u) for c, u in terms]
        if new[0][0] < 0 and new[1][0] < 0:
            return None
        if new[0][0] < 0:                 # write the positive term first
            new = [new[1], new[0]]
        out.append((name, new))
    return out


def best_signs(lines, outs, Wd=8, seed=1):
    base = {}
    adders = []
    for name, terms in lines:
        if len(terms) == 1:
            base[name] = base.get(terms[0][1], terms[0][1])
        else:
            base[name] = name
            adders.append(name)
    c0 = G.Circuit(lines, outs, 'original')
    fixed = set(h for h, _ in c0.outs)
    free = [n for n in adders if n not in fixed]

    def evaluate(sign):
        L = resign_lines(lines, base, sign)
        if L is None:
            return None, None
        try:
            c = G.Circuit(L, outs, 'resigned')
        except ValueError:
            return None, None
        ab, ib, ns = cost_of(c, Wd)
        return (ab + ib, ns), L

    best = (evaluate({})[0], {})
    exact = len(free) <= 16
    tried = 0
    if exact:
        for bits in itertools.product((1, -1), repeat=len(free)):
            sign = {n: b for n, b in zip(free, bits) if b < 0}
            cst, _ = evaluate(sign)
            tried += 1
            if cst is not None and cst < best[0]:
                best = (cst, sign)
    else:
        rnd = random.Random(seed)
        for restart in range(6):
            cur = {}
            ccost = evaluate(cur)[0]
            T = 6.0
            for it in range(4000):
                n = rnd.choice(free)
                nxt = dict(cur)
                if n in nxt:
                    del nxt[n]
                else:
                    nxt[n] = -1
                if rnd.random() < 0.3:          # flip a second line too: many moves need two
                    m = rnd.choice(free)
                    if m in nxt:
                        del nxt[m]
                    else:
                        nxt[m] = -1
                cst, _ = evaluate(nxt)
                tried += 1
                if cst is None:
                    continue
                d = cst[0] - ccost[0]
                if d <= 0 or rnd.random() < pow(2.718281828, -d / T):
                    cur, ccost = nxt, cst
                    if ccost < best[0]:
                        best = (ccost, dict(cur))
                T = max(0.3, T * 0.999)
    cst, L = evaluate(best[1])
    return L, best[1], exact, tried, len(free)


def main():
    for d in (OUTC, OUTV, TMP):
        os.makedirs(d, exist_ok=True)
    env = dict(os.environ, PATH=BIN + ':' + os.environ['PATH'])
    dj = json.load(open(os.path.join(RTL, 'designs.json')))
    rows = {(x['size'], x['design'], x['W']): x for x in dj['designs']}
    report = []
    bad = 0
    for size, design in WANT:
        row = rows[(size, design, 8)]
        text = open(src_path(row['source'])).read()
        lines, outs = G.parse_text(text)
        c0 = G.Circuit(lines, outs, row['source'])
        a0 = cost_of(c0, 8)
        L, sign, exact, tried, nfree = best_signs(lines, outs, 8)
        c1 = G.Circuit(L, outs, 'resigned')
        a1 = cost_of(c1, 8)
        name = '%s_%sS' % (size, design)
        hdr = ('%s points: the circuit of %s with other signs (written by resign.py).\n'
               'Same adders, same wiring, same depth; the lines kept with the opposite sign: %s.\n'
               'At input width 8: adder bits %d -> %d, bits of distinct subtracted operands %d -> %d, subtractions %d -> %d.\n'
               '%s' % (size, row['source'], ' '.join(sorted(sign)) or '(none)', a0[0], a1[0], a0[1], a1[1], a0[2], a1[2],
                       'Every choice of signs was tried (%d).' % tried if exact else
                       'Random local search over %d free lines, %d choices tried: best found, not proved best.' % (nfree, tried)))
        txt = G.to_text(L, hdr)
        if outs:
            txt += '# OUT ' + ' '.join(outs) + '\n'
        cf = os.path.join(OUTC, name + '.txt')
        open(cf, 'w').write(txt)
        rec = dict(size=size, design=design + 'S', of=design, adders=len(c1.adders), depth=c1.depth, exact=exact, tried=tried,
                   negated=sorted(sign), before=dict(adder_bits=a0[0], sub_bits=a0[1], subs=a0[2]),
                   after=dict(adder_bits=a1[0], sub_bits=a1[1], subs=a1[2]), files={}, metrics={})
        print('%-14s adders %d depth %d   adder bits %d -> %d   subtracted-operand bits %d -> %d   subtractions %d -> %d   %s' % (
            name, len(c1.adders), c1.depth, a0[0], a1[0], a0[1], a1[1], a0[2], a1[2], 'exact' if exact else 'best found'), flush=True)
        assert c1.depth == c0.depth and len(c1.adders) == len(c0.adders)
        for W in WIDTHS:
            rw = rows[(size, design, W)]
            for v in VARIANTS[size]:
                K = int(v[1:]) if len(v) > 1 and v[0] == 'p' else 1
                if v != 'c' and K >= c1.depth:
                    continue
                bn = '%s_%s_w%d' % (name, v, W)
                out = os.path.join(OUTV, bn + '.v')
                p = subprocess.run([sys.executable, '-B', os.path.join(RTL, 'gen_rtl.py'), cf, '--variant', v, '--width', str(W),
                                    '--name', 'wht_' + bn, '-o', out], capture_output=True, text=True, cwd=TMP)
                if p.returncode != 0:
                    print(bn, 'GENERATOR FAILED', p.stderr[-300:])
                    bad += 1
                    continue
                met = json.loads(p.stderr.strip().splitlines()[-1])
                lat = 0 if v == 'c' else -(-c1.depth // K)
                nw, no = rw['N'] * W, rw['N'] * rw['OW']
                cfile = os.path.join(RTL, rw['files']['c']['file'])
                tbt = E.tb('wht_' + bn, rw['files']['c']['module'], nw, no, max(lat, 1))
                if lat == 0:      # both combinational: compare in the same cycle
                    tbt = tbt.replace('if (yp !== dl[0] || vp !== dv[0])', 'if (yp !== yc || vp !== vc)')
                    assert 'yp !== yc' in tbt
                tbf = os.path.join(TMP, bn + '_tb.v')
                open(tbf, 'w').write(tbt)
                vvp = os.path.join(TMP, bn + '.vvp')
                c1r = subprocess.run(['iverilog', '-g2005', '-o', vvp, tbf, out, cfile], capture_output=True, text=True, env=env)
                ok = False
                res = ''
                if c1r.returncode == 0:
                    c2r = subprocess.run(['vvp', '-n', vvp], capture_output=True, text=True, env=env)
                    rl = [l for l in c2r.stdout.splitlines() if l.startswith('RESULT')]
                    res = rl[0] if rl else 'NO RESULT'
                    ok = res.endswith('errors=0')
                    os.remove(vvp)
                else:
                    res = 'IVERILOG FAILED ' + (c1r.stderr + c1r.stdout)[-200:]
                if not ok:
                    bad += 1
                rec['files']['%s_w%d' % (v, W)] = dict(file=out, sim=res, ok=ok)
                if v in ('c', 'p'):
                    rec['metrics']['%s_w%d' % (v, W)] = {k: met.get(k) for k in ('adders', 'depth', 'adder_bits', 'reg_data', 'reg_delay', 'reg_after_adders')}
        report.append(rec)
    json.dump(report, open(os.path.join(OUTC, 'RESIGNED.json'), 'w'), indent=1)
    nfiles = sum(len(r['files']) for r in report)
    print('files written and simulated: %d, failures: %d' % (nfiles, bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
