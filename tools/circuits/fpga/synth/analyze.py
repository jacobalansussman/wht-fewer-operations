#!/usr/bin/env python3
"""analyze.py -- read results/*.jsonl (written by batch.py and second.py) and the paper figures of
../rtl/designs.json, and write TABLES.md and summary.json.  Standard library only.

    python3 -B analyze.py

Every frequency is given as  median [lowest - highest] over the seeds  of nextpnr's
"Max frequency" after routing; icetime's figure the same way.  Logic cells are those of the
design alone (harness subtracted, see run.py); they do not depend on the seed, and the script
checks that.
"""
import json
import os
import statistics
import subprocess
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
FPGA = os.path.dirname(HERE)
RES = os.path.join(HERE, 'results')
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))      # the top folder of the repository

NAMES = {'textbook': 'textbook', 'cfl1994': '1994 design', 'cfl1994b': '1994 design, plain layer first',
         'ar2023': 'Alman and Rao step', 'ar2023l': 'Alman and Rao step, sums left to right',
         'ours': 'this work', 'xk265': 'outside core (xk265)', 'xk264': 'outside core (xk264)'}
for _d in ('textbook', 'cfl1994', 'ar2023', 'ours'):
    NAMES[_d + 'S'] = NAMES[_d] + ', other signs'
ORDER = ['textbook', 'textbookS', 'xk265', 'xk264', 'cfl1994', 'cfl1994S', 'cfl1994b', 'ar2023', 'ar2023S', 'ar2023l', 'ours', 'oursS']
PRIMARY = {'8': ['textbook', 'cfl1994', 'ar2023', 'ours'], '16': ['textbook', 'cfl1994', 'ours'],
           '64': ['textbook', 'cfl1994', 'ours'], '8x8': ['textbook', 'ours']}


def load(name):
    p = os.path.join(RES, name)
    L = []
    if os.path.exists(p):
        for line in open(p):
            line = line.strip()
            if line:
                L.append(json.loads(line))
    return L


def med(xs):
    return statistics.median(xs)


def rng(xs, fmt='%.1f'):
    if not xs:
        return '-'
    return (fmt + ' [' + fmt + ' - ' + fmt + ']') % (med(xs), min(xs), max(xs))


def paper_figures():
    d = json.load(open(os.path.join(FPGA, 'rtl', 'designs.json')))
    P = {}
    for x in d['designs']:
        P[(x['size'], x['design'], x['W'])] = dict(adders=x['adders'], depth=x['depth'], adder_bits=x['adder_bits'])
    # 9 bits: ask the generator ../rtl/gen_rtl.py for its figures (it only prints)
    src = {(x['size'], x['design']): x['source'] for x in d['designs']}
    for size in ('8', '16'):
        for dn in ('textbook', 'ours'):
            s = src[(size, dn)]
            path = os.path.join(REPO, s)
            try:
                p = subprocess.run([sys.executable, '-B', os.path.join(FPGA, 'rtl', 'gen_rtl.py'), path, '--variant', 'c',
                                    '--width', '9'], capture_output=True, text=True, timeout=60)
                m = json.loads(p.stderr.strip().splitlines()[-1])
                P[(size, dn, 9)] = dict(adders=m['adders'], depth=m['depth'], adder_bits=m['adder_bits'])
            except Exception:
                pass
    rj = os.path.join(HERE, 'resigned', 'RESIGNED.json')
    if os.path.exists(rj):
        for rec in json.load(open(rj)):
            for key, m in rec['metrics'].items():
                v, w = key.split('_w')
                if v == 'c':
                    P[(rec['size'], rec['design'], int(w))] = dict(adders=m['adders'], depth=m['depth'], adder_bits=m['adder_bits'])
    for W in (8, 9, 12, 16):
        if ('8', 'textbook', W) in P:
            P[('8', 'xk265', W)] = dict(P[('8', 'textbook', W)])
    if ('16', 'textbook', 9) in P:
        P[('16', 'xk264', 9)] = dict(P[('16', 'textbook', 9)])
    return P


def latency(variant, depth):
    if variant == 'c':
        return 1
    if variant == 'r':
        return 2
    K = int(variant[1:]) if len(variant) > 1 else 1
    return -(-depth // K)


def levels(variant, depth):
    """adder levels between two registers"""
    if variant in ('c', 'r'):
        return depth
    return int(variant[1:]) if len(variant) > 1 else 1


def collect(runs):
    """-> {(size, design, variant, W, flow): summary}"""
    G = defaultdict(list)
    for r in runs:
        if r.get('synth_only') or r.get('pack_only'):
            continue
        G[(r['size'], r['design_name'], r['variant'], r['W'], r['flow'])].append(r)
    S = {}
    for k, L in G.items():
        ok = [r for r in L if 'error' not in r]
        s = dict(n=len(ok), errors=[r['error'] for r in L if 'error' in r])
        if ok:
            lcs = sorted(set(r['lc_dut'] for r in ok))
            s['lc'] = ok[0]['lc_dut']
            s['lc_all'] = lcs
            for f in ('dut_carry', 'dut_carry_nolut', 'dut_lut_only', 'dut_lut_ff', 'dut_ff_only', 'dut_ff', 'dut_chain_extra', 'lc_total', 'lc_harness'):
                s[f] = ok[0].get(f)
            s['harness_ok'] = all(r.get('harness_ok') for r in ok)
            s['fmax'] = [r['fmax_nextpnr'] for r in ok if 'fmax_nextpnr' in r]
            s['ice'] = [r['fmax_icetime'] for r in ok if 'fmax_icetime' in r]
            s['crit'] = sorted(set(r.get('crit', '?') for r in ok))
            # a path from the harness to the harness with next to no logic on it is a path of the harness alone;
            # one with many logic cells runs through the design (variant c without output register)
            s['crit_harness_only'] = sum(1 for r in ok if r.get('crit') == 'harness->harness' and r.get('crit_logic_cells', 99) <= 2)
            s['yosys'] = {a: b for a, b in ok[0].get('yosys_dut', {}).items() if a.startswith('SB_')}
        elif L:
            s['lc_total_failed'] = L[0].get('lc_total')
            s['yosys'] = {a: b for a, b in L[0].get('yosys_dut', {}).items() if a.startswith('SB_')}
        S[k] = s
    return S


RUNS = []


def compact(S, P):
    """the short tables for the closing message: (a) and (b) at 8 and 16 points, W = 8 and 12"""
    out = []
    A = out.append
    short = {'textbook': 'textbook', 'cfl1994': '1994 design', 'ar2023': 'Alman and Rao step', 'ours': 'this work', 'oursS': 'this work, other signs'}
    for size in ('8', '16'):
        for W in (8, 12):
            tb = S.get((size, 'textbook', 'c', W, 'default'))
            if not tb or not tb.get('n'):
                continue
            tbn = S.get((size, 'textbook', 'c', W, 'noreg'))
            A('**(a) %s points, W = %d, unpipelined (variant c: input register, all adders, output register), %d seeds**' % (size, W, tb['n']))
            A('')
            A('| design | adders / adder bits / depth | logic cells (same for every seed) | against textbook | adders alone, no output register: cells | against textbook | max MHz, nextpnr: median [lowest - highest] | max MHz, icetime: median |')
            A('|---|---|---|---|---|---|---|---|')
            for dn in ('textbook', 'cfl1994', 'ar2023', 'ours', 'oursS'):
                s = S.get((size, dn, 'c', W, 'default'))
                if not s or not s.get('n'):
                    continue
                pf = P[(size, dn, W)]
                ag = '-' if dn == 'textbook' else '%+d (%+.1f %%)' % (s['lc'] - tb['lc'], 100.0 * (s['lc'] - tb['lc']) / tb['lc'])
                sn = S.get((size, dn, 'c', W, 'noreg'))
                if sn and sn.get('n') and tbn and tbn.get('n'):
                    nr = '%d' % sn['lc']
                    nra = '-' if dn == 'textbook' else '%+d (%+.1f %%)' % (sn['lc'] - tbn['lc'], 100.0 * (sn['lc'] - tbn['lc']) / tbn['lc'])
                else:
                    nr = nra = '-'
                A('| %s | %d / %d / %d | %d | %s | %s | %s | %s | %.1f |' % (short[dn], pf['adders'], pf['adder_bits'], pf['depth'], s['lc'], ag, nr, nra, rng(s['fmax']), med(s['ice'])))
            A('')
            tbp = S.get((size, 'textbook', 'p', W, 'default'))
            if not tbp or not tbp.get('n'):
                continue
            ttop = med(tbp['fmax'])
            A('**(b) %s points, W = %d, fewest logic cells that reach a clock target** (cells include all registers of the design; entry = variant, latency in clocks, cells, median MHz, seeds reaching the target)' % (size, W))
            A('')
            dns = [d for d in ('textbook', 'cfl1994', 'ar2023', 'ours', 'oursS') if (size, d, 'c', W, 'default') in S]
            A('| clock target | ' + ' | '.join(short[d] for d in dns) + ' | this work against textbook |')
            A('|---|' + '---|' * (len(dns) + 1))
            targets = [(12.0, '12 MHz (board oscillator)'), (50.0, '50 MHz'), (75.0, '75 MHz'), (100.0, '100 MHz'), (125.0, '125 MHz'), (150.0, '150 MHz'),
                       (ttop, '%.0f MHz (textbook at one adder per clock)' % ttop)]
            targets.sort(key=lambda t: t[0])
            for T, label in targets:
                line = '| %s |' % label
                best = {}
                for dn in dns:
                    cands = []
                    for k, s in S.items():
                        if k[0] == size and k[1] == dn and k[3] == W and k[4] == 'default' and k[2] != 'r' and s.get('n') and med(s['fmax']) >= T - 1e-9:
                            cands.append((s['lc'], vkey(k[2]), k[2], s))
                    if not cands:
                        line += ' none reaches it |'
                        continue
                    cands.sort(key=lambda c: (c[0], c[1]))
                    lc, _, v, s = cands[0]
                    best[dn] = lc
                    line += ' %s, %d, **%d**, %.0f, %d/%d |' % (v, latency(v, P[(size, dn, W)]['depth']), lc, med(s['fmax']), sum(1 for f in s['fmax'] if f >= T - 1e-9), s['n'])
                if 'ours' in best and 'textbook' in best:
                    line += ' %+d (%+.1f %%) |' % (best['ours'] - best['textbook'], 100.0 * (best['ours'] - best['textbook']) / best['textbook'])
                else:
                    line += ' - |'
                A(line)
            A('')
    # 64 points: cells from packing (they do not depend on placement), speed from the lean-harness runs
    packed = {(r['size'], r['design_name'], r['variant'], r['W']): r for r in RUNS if r.get('pack_only') and r['design_name'] != 'stub' and 'lc_dut' in r and r.get('flow') == 'default'}
    if packed:
        A('**64 points and the 8 x 8 block, W = 8, unpipelined (variant c)**')
        A('')
        A('| design | adders / adder bits / depth | logic cells of the design | against textbook | with the standard harness (1,412 cells): whole image of 7,680 | lean harness: max MHz nextpnr, median [lowest - highest], seeds |')
        A('|---|---|---|---|---|---|')
        tb = packed.get(('64', 'textbook', 'c', 8))
        for size, dn, label in (('64', 'textbook', 'textbook (also the 8 x 8 block)'), ('64', 'cfl1994', '1994 design'), ('64', 'ours', 'this work, family'), ('8x8', 'ours', 'this work, 19-adder circuit in two layers')):
            r = packed.get((size, dn, 'c', 8))
            if not r:
                continue
            pf = P[(size, dn, 8)]
            ag = '-' if dn == 'textbook' else '%+d (%+.1f %%)' % (r['lc_dut'] - tb['lc_dut'], 100.0 * (r['lc_dut'] - tb['lc_dut']) / tb['lc_dut'])
            sl = S.get((size, dn, 'c', 8, 'lean'))
            sp = ('%s, %d' % (rng(sl['fmax']), sl['n'])) if sl and sl.get('n') else ('did not finish' if sl else 'not run')
            A('| %s | %d / %d / %d | %d | %s | %d%s | %s |' % (label, pf['adders'], pf['adder_bits'], pf['depth'], r['lc_dut'], ag, r['lc_total'],
                                                       ' (does not fit)' if r['lc_total'] > 7680 else '', sp))
        A('')
    open(os.path.join(HERE, 'TABLES-SHORT.md'), 'w').write('\n'.join(out) + '\n')


def second_opinion(A, P):
    syn = load('second_synth.jsonl')
    if not syn:
        return
    D = {(r['size'], r['design_name'], r['variant'], r['W'], r['family']): r for r in syn if 'error' not in r}
    A('# Second opinion: other FPGA families')
    A('')
    A('Synthesis only (Yosys 0.69+274), the design module alone, no harness, no place and route, no timing. '
      'Commands: `synth_ice40`, `synth_ecp5`, `synth_xilinx -family xc7 -noclkbuf`, `synth_intel_alm -family cyclonev -noiopad -noclkbuf`. '
      'Counts are the cells yosys prints. ECP5: one CCU2C is two bits of carry chain and takes the place of two LUT4, so '
      '"LUT4 places" = LUT4 + 2 x CCU2C. Xilinx 7-series: one CARRY4 is four bits of carry chain; the LUTs in front of it are counted under LUT. '
      'Cyclone V: one MISTRAL_ALUT_ARITH per adder bit.')
    A('')

    def pct(x, ref):
        return '%d (%+.1f %%)' % (x, 100.0 * (x - ref) / ref) if ref else str(x)

    for size in ('8', '16'):
        for W in (8, 12):
            A('### %s points, W = %d, combinational (variant c, no registers)' % (size, W))
            A('')
            A('| design | adders | adder bits | iCE40: LUT4 (carry cells) | ECP5: LUT4 places (LUT4 + 2 x CCU2C) | Xilinx 7: LUT (CARRY4) | Cyclone V: ALUT (arithmetic + other) |')
            A('|---|---|---|---|---|---|---|')
            ref = {f: D.get((size, 'textbook', 'c', W, f)) for f in ('ice40', 'ecp5', 'xc7', 'cyclonev')}
            for dn in ORDER:
                if not any((size, dn, 'c', W, f) in D for f in ('ice40', 'ecp5', 'xc7', 'cyclonev')):
                    continue
                pf = P.get((size, dn, W), {})
                cells = []
                for f, key, fmt in (('ice40', 'lut', lambda r: '(%d)' % r['carry']),
                                    ('ecp5', 'lut_equiv', lambda r: '(%d + 2 x %d)' % (r['lut'], r['carry'])),
                                    ('xc7', 'lut', lambda r: '(%d)' % r['carry']),
                                    ('cyclonev', 'lut_total', lambda r: '(%d + %d)' % (r['arith'], r['lut']))):
                    r = D.get((size, dn, 'c', W, f))
                    if not r:
                        cells.append('-')
                        continue
                    rr = ref[f][key] if ref[f] else 0
                    cells.append((pct(r[key], rr) if dn != 'textbook' else str(r[key])) + ' ' + fmt(r))
                A('| %s | %s | %s | %s |' % (NAMES[dn], pf.get('adders', '-'), pf.get('adder_bits', '-'), ' | '.join(cells)))
            A('')
            A('### %s points, W = %d, pipelined variants' % (size, W))
            A('')
            A('| design | variant | latency | iCE40: LUT4 / flip-flops | ECP5: LUT4 places / flip-flops | Xilinx 7: LUT / shift-register LUT / flip-flops | Cyclone V: ALUT / flip-flops |')
            A('|---|---|---|---|---|---|---|')
            for dn in ORDER:
                vs = sorted(set(k[2] for k in D if k[0] == size and k[1] == dn and k[3] == W and k[2] != 'c'), key=vkey)
                for v in vs:
                    pf = P.get((size, dn, W), {})
                    cells = []
                    for f, fmt in (('ice40', lambda r: '%d / %d' % (r['lut'], r['ff'])),
                                   ('ecp5', lambda r: '%d / %d' % (r['lut_equiv'], r['ff'])),
                                   ('xc7', lambda r: '%d / %d / %d' % (r['lut'], r['srl'], r['ff'])),
                                   ('cyclonev', lambda r: '%d / %d' % (r['lut_total'], r['ff']))):
                        r = D.get((size, dn, v, W, f))
                        cells.append(fmt(r) if r else '-')
                    A('| %s | %s | %s | %s |' % (NAMES[dn], v, latency(v, pf['depth']) if pf.get('depth') else '-', ' | '.join(cells)))
            A('')
    errs = [r for r in syn if 'error' in r]
    if errs:
        A('Synthesis failed for: ' + ', '.join('%s (%s)' % (r['tag'], r['family']) for r in errs))
        A('')

    ecp = load('second_ecp5_slices.jsonl') or load('second_ecp5.jsonl')
    if ecp:
        A('## ECP5, placed and routed')
        A('')
        A('nextpnr-ecp5 0.11.1-59-g837d0eed, `--25k --package CABGA381 --speed 6 --freq 400`, same harness as on the iCE40 (design kept as its own module). '
          'TRELLIS_COMB is one LUT4 place (a carry cell takes two), TRELLIS_FF one flip-flop; the figures are the whole image less the harness alone.')
        A('')
        stub = {}
        for r in ecp:
            if r['design_name'] == 'stub' and 'util' in r:
                stub[(r['nw'], r['no'])] = r['util']
        G = defaultdict(list)
        for r in ecp:
            if r['design_name'] != 'stub':
                G[(r['size'], r['design_name'], r['variant'], r['W'])].append(r)
        A('The last area column is the larger of the two counts: an ECP5 slice holds two LUT4 places and two flip-flops, and a flip-flop may sit beside a LUT it does not belong to, '
          'so the larger count is a lower bound on the area in half-slices. nextpnr does not print the number of slices touched.')
        A('')
        A('"Slices of the whole image" counts the slices that hold at least one cell after placement, harness included (the harness is the same for every design of a size and width; '
          'alone it occupies the number given below the table); median [lowest - highest] over the seeds.')
        A('')
        A('| points | W | design | variant | latency | TRELLIS_COMB of the design | against textbook, same variant | TRELLIS_FF of the design | larger of the two | slices of the whole image | MHz nextpnr-ecp5 | seeds |')
        A('|---|---|---|---|---|---|---|---|---|---|---|---|')
        for size in ('8', '16'):
            for W in (8, 12):
                for v in ('c', 'p4', 'p3', 'p2', 'p'):
                    refc = None
                    Lr = [r for r in G.get((size, 'textbook', v, W), []) if 'util' in r]
                    if Lr:
                        st = stub.get((Lr[0]['nw'], Lr[0]['no']), {})
                        refc = Lr[0]['util'].get('TRELLIS_COMB', 0) - st.get('TRELLIS_COMB', 0)
                    for dn in ORDER:
                        L = [r for r in G.get((size, dn, v, W), []) if 'util' in r]
                        if not L:
                            continue
                        st = stub.get((L[0]['nw'], L[0]['no']), {})
                        comb = L[0]['util'].get('TRELLIS_COMB', 0) - st.get('TRELLIS_COMB', 0)
                        ff = L[0]['util'].get('TRELLIS_FF', 0) - st.get('TRELLIS_FF', 0)
                        ag = '%+d (%+.1f %%)' % (comb - refc, 100.0 * (comb - refc) / refc) if refc and dn != 'textbook' else '-'
                        pf = P.get((size, dn, W), {})
                        sl = [r['slices'] for r in L if 'slices' in r]
                        A('| %s | %d | %s | %s | %s | %d | %s | %d | %d | %s | %s | %d |' % (size, W, NAMES[dn], v, latency(v, pf['depth']) if pf.get('depth') else '-',
                          comb, ag, ff, max(comb, ff), rng(sl, '%d') if sl else '-', rng([r['fmax_nextpnr'] for r in L if 'fmax_nextpnr' in r]), len(L)))
        A('')
        hs = sorted(set((r['nw'], r['no'], r['util'].get('TRELLIS_COMB', 0), r['util'].get('TRELLIS_FF', 0), r.get('slices', 0)) for r in ecp if r['design_name'] == 'stub' and 'util' in r))
        A('Harness alone on the ECP5 (input bits, output bits, TRELLIS_COMB, TRELLIS_FF, slices): ' + '; '.join('%d, %d, %d, %d, %d' % h for h in hs) + '.')
        A('')


def vkey(v):
    return (0, 0) if v == 'c' else (2, 0) if v == 'r' else (1, -(int(v[1:]) if len(v) > 1 else 1))


def main():
    P = paper_figures()
    runs = (load('g8.jsonl') + load('g16.jsonl') + load('g64.jsonl') + load('gnoreg.jsonl') + load('gS.jsonl')
            + load('g64lean.jsonl') + load('g64wide.jsonl'))
    S = collect(runs)
    RUNS.extend(runs)
    out = []
    A = out.append
    summary = {}

    A('# Tables written by analyze.py')
    A('')
    A('Chip: iCE40HX8K, package ct256 (7,680 logic cells). Tools: oss-cad-suite 2026-10-11: Yosys 0.69+274 '
      '(`synth_ice40 -top top`, defaults, which means abc9), nextpnr-ice40 0.11.1-59-g837d0eed (`--hx8k --package ct256 '
      '--seed S --freq 400`, placer heap, router router1), icetime (`-d hx8k -P ct256 -t -m`).')
    A('')
    A('- **Logic cells** are those of the design alone: cells of the whole image less the harness. '
      'For the combinational variant (c) the design includes one output register; the input register is the harness\'s shift register and is not counted. '
      'For p and pK the design\'s own registers are counted and nothing is added.')
    A('- **MHz** is nextpnr\'s maximum frequency after routing: median [lowest - highest] over the seeds. icetime\'s figure follows in the same form.')
    A('- **Latency** is in clock cycles from the input register to the registered output.')
    A('- **pK** means a register after every K-th adder level; p = p1.')
    A('')

    # ---------------- harness ----------------
    A('## The harness alone')
    A('')
    A('| points | W | input bits | output bits | logic cells of the harness alone | formula NW + NO + 4 | MHz of the harness alone |')
    A('|---|---|---|---|---|---|---|')
    for k in sorted(S, key=lambda k: (int(k[0].split('x')[0]) if k[0] != '8x8' else 64, k[3], k[4])):
        if k[1] != 'stub':
            continue
        rr = [r for r in runs if r['design_name'] == 'stub' and r['size'] == k[0] and r['W'] == k[3] and r['flow'] == k[4] and 'error' not in r and 'fmax_nextpnr' in r]
        if not rr:
            continue
        A('| %s%s | %d | %d | %d | %d | %s | %s |' % (k[0], ' (lean harness)' if k[4] == 'lean' else '', k[3], rr[0]['nw'], rr[0]['no'], rr[0]['lc_total'],
                                                 '-' if k[4] == 'lean' else rr[0]['nw'] + rr[0]['no'] + 4, rng([r['fmax_nextpnr'] for r in rr])))
    lean_stub = [r['lc_total'] for r in runs if r['design_name'] == 'stub' and r.get('flow') == 'lean' and 'lc_total' in r and not r.get('pack_only')]
    for k, s in S.items():
        if k[4] == 'lean' and k[1] != 'stub' and s.get('n') and lean_stub:
            s['harness_ok'] = (s['lc_harness'] == lean_stub[0])
    bad = [k for k, s in S.items() if k[1] != 'stub' and s.get('n') and not s.get('harness_ok')]
    A('')
    A('Harness cells counted by name in every routed image equal NW + NO + 4: %s.' % ('yes, in all %d design/variant/width cases' % sum(1 for k, s in S.items() if k[1] != 'stub' and s.get('n')) if not bad else 'NO for ' + ', '.join(map(str, bad))))
    multi = [k for k, s in S.items() if s.get('n') and len(s.get('lc_all', [])) > 1]
    A('Logic cells the same for every seed: %s.' % ('yes' if not multi else 'NO for ' + ', '.join(map(str, multi))))
    crit_h = [k for k, s in S.items() if k[1] != 'stub' and s.get('n') and s.get('crit_harness_only')]
    A('Critical path inside the harness only (which would hide the design\'s speed): %s.' % ('in no run' if not crit_h else ', '.join('%s_%s_%s_w%d_%s (%d runs)' % (k + (S[k]['crit_harness_only'],)) for k in crit_h)))
    A('')

    def row_all(size, W, flows=('default',)):
        rows = []
        for dn in ORDER:
            vs = sorted(set(k[2] for k in S if k[0] == size and k[1] == dn and k[3] == W), key=vkey)
            for v in vs:
                for fl in flows:
                    s = S.get((size, dn, v, W, fl))
                    if s:
                        rows.append((dn, v, fl, s))
        return rows

    sizes = [s for s in ('8', '16', '64', '8x8') if any(k[0] == s and k[1] != 'stub' for k in S)]
    for size in sizes:
        Ws = sorted(set(k[3] for k in S if k[0] == size and k[1] != 'stub'))
        for W in Ws:
            A('## %s points, W = %d: every variant' % (size, W))
            A('')
            A('| design | variant | adder levels between registers | latency | logic cells | carry cells | LUT only | LUT + flip-flop | flip-flop only | flip-flops | yosys LUT4 / carry / flip-flop | MHz nextpnr | MHz icetime | seeds |')
            A('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
            for dn, v, fl, s in row_all(size, W, ('default', 'noreg', 'retime', 'dff', 'lean')):
                pf = P.get((size, dn, W), {})
                depth = pf.get('depth')
                vn = v + ('' if fl == 'default' else ' (' + {'retime': 'ABC retiming', 'dff': 'abc9 -dff', 'noreg': 'no output register', 'lean': 'lean harness'}[fl] + ')')
                y = s.get('yosys', {})
                ys = '%s / %s / %s' % (y.get('SB_LUT4', '-'), y.get('SB_CARRY', '-'), sum(b for a, b in y.items() if a.startswith('SB_DFF')))
                if not s.get('n'):
                    A('| %s | %s | %s | %s | did not fit or did not finish: %s | | | | | | %s | | | 0 |' % (
                        NAMES[dn], vn, levels(v, depth) if depth else '-', latency(v, depth) if depth else '-',
                        (s['errors'][0][:90] if s['errors'] else ''), ys))
                    continue
                A('| %s | %s | %s | %s | %d | %d | %d | %d | %d | %d | %s | %s | %s | %d |' % (
                    NAMES[dn], vn, levels(v, depth) if depth else '-', latency(v, depth) if depth else '-',
                    s['lc'], s['dut_carry'], s['dut_lut_only'], s['dut_lut_ff'], s['dut_ff_only'], s['dut_ff'], ys,
                    rng(s['fmax']), rng(s['ice']), s['n']))
            A('')

    # ---------------- (a) ----------------
    A('# (a) Area at the same function, no clock constraint')
    A('')
    A('Variant c: all adders between one input register and one output register. Logic cells did not vary with the seed (spread 0), so the spread column shows the same figure three times. '
      '"Without output register" is the same design with no register of its own: the harness\'s signature register takes the outputs directly (one more LUT in the timed path).')
    A('')
    for size in [z for z in sizes if z in ('8', '16')]:
        Ws = sorted(set(k[3] for k in S if k[0] == size and k[1] != 'stub' and k[2] == 'c'))
        for W in Ws:
            tb = S.get((size, 'textbook', 'c', W, 'default'))
            tbn = S.get((size, 'textbook', 'c', W, 'noreg'))
            A('### %s points, W = %d' % (size, W))
            A('')
            A('| design | adders | adder bits | depth | logic cells, median (lowest - highest) | against textbook | of which carry cells / LUT only / flip-flop only | LUT4 beyond the adder bits | MHz nextpnr | MHz icetime | without output register: logic cells | against textbook |')
            A('|---|---|---|---|---|---|---|---|---|---|---|---|')
            for dn in ORDER:
                s = S.get((size, dn, 'c', W, 'default'))
                if not s:
                    continue
                pf = P.get((size, dn, W), {})
                if not s.get('n'):
                    A('| %s | %s | %s | %s | did not fit or finish | | | | | | | |' % (NAMES[dn], pf.get('adders', '-'), pf.get('adder_bits', '-'), pf.get('depth', '-')))
                    continue
                if tb and tb.get('n') and dn != 'textbook':
                    dl = s['lc'] - tb['lc']
                    ag = '%+d cells (%+.1f %%)' % (dl, 100.0 * dl / tb['lc'])
                else:
                    ag = '-'
                y = s.get('yosys', {})
                extra = (y.get('SB_LUT4', 0) - pf['adder_bits']) if pf.get('adder_bits') else '-'
                sn = S.get((size, dn, 'c', W, 'noreg'))
                if sn and sn.get('n'):
                    nr = '%d' % sn['lc']
                    if tbn and tbn.get('n') and dn != 'textbook':
                        dn2 = sn['lc'] - tbn['lc']
                        nra = '%+d cells (%+.1f %%)' % (dn2, 100.0 * dn2 / tbn['lc'])
                    else:
                        nra = '-'
                    summary['a_noreg_%s_%s_w%d' % (size, dn, W)] = dict(lc=sn['lc'], fmax=med(sn['fmax']))
                else:
                    nr, nra = '-', '-'
                A('| %s | %s | %s | %s | %d (%d - %d) | %s | %d / %d / %d | %s | %s | %s | %s | %s |' % (
                    NAMES[dn], pf.get('adders', '-'), pf.get('adder_bits', '-'), pf.get('depth', '-'),
                    s['lc'], min(s['lc_all']), max(s['lc_all']), ag, s['dut_carry'], s['dut_lut_only'], s['dut_ff_only'], extra,
                    rng(s['fmax']), rng(s['ice']), nr, nra))
                summary['a_%s_%s_w%d' % (size, dn, W)] = dict(lc=s['lc'], fmax=med(s['fmax']), fmin=min(s['fmax']), fmax_hi=max(s['fmax']))
            A('')

    # ---------------- 64 points, lean harness ----------------
    lean = [(k, s_) for k, s_ in S.items() if k[4] == 'lean' and k[1] != 'stub']
    if lean:
        A('### 64 points and the 8 x 8 block, W = 8, placed and routed with the lean harness')
        A('')
        A('The standard harness (1,412 cells here) leaves too little room, so these runs use the lean one (894 cells: outputs folded 16 to 1 by XOR before the signature register). '
          'The 8 x 8 block with the textbook network is the same adder network as the 64-point textbook. "Against textbook" compares with the textbook variant of the same latency where one was run.')
        A('')
        A('| design | variant | adder levels between registers | latency | logic cells | against the textbook at the same latency | carry cells / LUT only / flip-flop only | whole image of 7,680 | MHz nextpnr | MHz icetime | seeds |')
        A('|---|---|---|---|---|---|---|---|---|---|---|')
        tbl = {}
        for k, s_ in lean:
            if k[1] == 'textbook' and s_.get('n'):
                tbl[latency(k[2], P[(k[0], k[1], k[3])]['depth'])] = s_
        for (k, s_) in sorted(lean, key=lambda t: (latency(t[0][2], P[(t[0][0], t[0][1], t[0][3])]['depth']) if t[0][2] != 'r' else 99, t[0][0], ORDER.index(t[0][1]))):
            size, dn, v, W, fl = k
            depth = P[(size, dn, W)]['depth']
            nm = NAMES[dn] + (' (the 19-adder circuit in two layers)' if size == '8x8' else (' (family)' if dn == 'ours' else ''))
            if not s_.get('n'):
                A('| %s | %s | %d | %d | did not finish: %s | | | | | | 0 |' % (nm, v, levels(v, depth), latency(v, depth), (s_['errors'][0][:80] if s_['errors'] else '')))
                continue
            t = tbl.get(latency(v, depth)) if v != 'r' else None
            ag = '-' if (dn == 'textbook' or not t) else '%+d (%+.1f %%)' % (s_['lc'] - t['lc'], 100.0 * (s_['lc'] - t['lc']) / t['lc'])
            A('| %s | %s | %d | %d | %d | %s | %d / %d / %d | %d | %s | %s | %d |' % (nm, v, levels(v, depth), latency(v, depth), s_['lc'], ag,
              s_['dut_carry'], s_['dut_lut_only'], s_['dut_ff_only'], s_['lc_total'], rng(s_['fmax']), rng(s_['ice']), s_['n']))
        A('')

    # ---------------- what fits: packing only ----------------
    packed = [r for r in runs if r.get('pack_only')]
    if packed:
        A('# 64 points and the 8 x 8 block: what fits the chip')
        A('')
        A('nextpnr packed every design (no placement) and counted the cells. The chip has 7,680. "Whole image" includes the harness.')
        A('')
        A('| points | W | design | variant | latency | yosys LUT4 / carry / flip-flop | logic cells of the design | harness | whole image | fits 7,680? |')
        A('|---|---|---|---|---|---|---|---|---|---|')
        for r in sorted(packed, key=lambda r: (r['size'], r['W'], ORDER.index(r['design_name']) if r['design_name'] in ORDER else 99, vkey(r['variant']))):
            if r['design_name'] == 'stub' or 'lc_total' not in r:
                continue
            pf = P.get((r['size'], r['design_name'], r['W']), {})
            y = r.get('yosys_dut', {})
            ys = '%s / %s / %s' % (y.get('SB_LUT4', '-'), y.get('SB_CARRY', '-'), sum(b for a, b in y.items() if a.startswith('SB_DFF')))
            A('| %s | %d | %s | %s | %s | %s | %s | %s | %d | %s |' % (r['size'], r['W'], NAMES[r['design_name']], r['variant'],
              latency(r['variant'], pf['depth']) if pf.get('depth') else '-', ys, r.get('lc_dut', '-'), r.get('lc_harness', '-'), r['lc_total'],
              'yes' if r['lc_total'] <= 7680 else 'NO'))
        A('')

    # ---------------- (b) ----------------
    A('# (b) Area at the same clock speed')
    A('')
    A('For each target the table gives, for each design, the variant with the fewest logic cells whose MEDIAN maximum frequency reaches the target '
      '(candidates: c and every pK measured), with the number of seeds that reach it. "none" means no measured variant reaches the target.')
    A('')
    for size in ('8', '16'):
        Ws = sorted(set(k[3] for k in S if k[0] == size and k[1] != 'stub' and k[2] == 'p'))
        for W in Ws:
            tbp = S.get((size, 'textbook', 'p', W, 'default'))
            if not tbp or not tbp.get('n'):
                continue
            ttop = med(tbp['fmax'])
            oursp = S.get((size, 'ours', 'p', W, 'default'))
            otop = med(oursp['fmax']) if oursp and oursp.get('n') else None
            targets = [(12.0, '12 MHz (the board\'s oscillator)'), (50.0, '50 MHz'), (75.0, '75 MHz'), (100.0, '100 MHz'), (125.0, '125 MHz'), (150.0, '150 MHz'), (175.0, '175 MHz'), (200.0, '200 MHz')]
            if otop:
                targets.append((otop, '%.1f MHz (median of this work, one adder per clock)' % otop))
            targets.append((ttop, '%.1f MHz (median of the textbook, one adder per clock: the highest it reaches)' % ttop))
            targets.sort(key=lambda t: t[0])
            A('### %s points, W = %d' % (size, W))
            A('')
            hdr = '| target |'
            for dn in PRIMARY[size]:
                hdr += ' %s: variant, latency, logic cells, MHz, seeds reaching |' % NAMES[dn]
            hdr += ' this work against textbook |'
            A(hdr)
            A('|---|' + '---|' * (len(PRIMARY[size]) + 1))
            for T, label in targets:
                line = '| %s |' % label
                best = {}
                for dn in PRIMARY[size]:
                    cands = []
                    for k, s in S.items():
                        if k[0] == size and k[1] == dn and k[3] == W and k[4] == 'default' and k[2] != 'r' and s.get('n'):
                            if med(s['fmax']) >= T - 1e-9:
                                cands.append((s['lc'], vkey(k[2]), k[2], s))
                    if not cands:
                        line += ' none |'
                        continue
                    cands.sort(key=lambda c: (c[0], c[1]))
                    lc, _, v, s = cands[0]
                    depth = P[(size, dn, W)]['depth']
                    best[dn] = (lc, v, s)
                    line += ' %s, %d, **%d**, %s, %d of %d |' % (v, latency(v, depth), lc, rng(s['fmax']), sum(1 for f in s['fmax'] if f >= T - 1e-9), s['n'])
                if 'ours' in best and 'textbook' in best:
                    dl = best['ours'][0] - best['textbook'][0]
                    line += ' %+d cells (%+.1f %%) |' % (dl, 100.0 * dl / best['textbook'][0])
                    summary['b_%s_w%d_%g' % (size, W, round(T, 1))] = dict(ours=best['ours'][0], ours_v=best['ours'][1], textbook=best['textbook'][0], textbook_v=best['textbook'][1])
                else:
                    line += ' - |'
                A(line)
            A('')

    # ---------------- (c) ----------------
    A('# (c) Speed at the same pipelining')
    A('')
    A('Same number of adder levels between registers (K). MHz nextpnr, median [lowest - highest]; logic cells in brackets.')
    A('')
    for size in ('8', '16'):
        Ws = sorted(set(k[3] for k in S if k[0] == size and k[1] != 'stub' and k[2] == 'p'))
        for W in Ws:
            A('### %s points, W = %d' % (size, W))
            A('')
            A('| adder levels between registers | ' + ' | '.join(NAMES[d] for d in PRIMARY[size]) + ' |')
            A('|---|' + '---|' * len(PRIMARY[size]))
            maxd = max(P[(size, d, W)]['depth'] for d in PRIMARY[size])
            for K in range(1, maxd + 1):
                line = '| %d |' % K
                anyv = False
                for dn in PRIMARY[size]:
                    depth = P[(size, dn, W)]['depth']
                    v = 'p' if K == 1 else ('c' if K == depth else 'p%d' % K)
                    s = S.get((size, dn, v, W, 'default'))
                    if K > depth or not s or not s.get('n'):
                        line += ' - |'
                    else:
                        anyv = True
                        line += ' %s: %s (%d cells, latency %d) |' % (v, rng(s['fmax']), s['lc'], latency(v, depth))
                if anyv:
                    A(line)
            A('')
            A('Same latency (clock cycles):')
            A('')
            A('| latency | ' + ' | '.join(NAMES[d] for d in PRIMARY[size]) + ' |')
            A('|---|' + '---|' * len(PRIMARY[size]))
            for Lt in range(1, maxd + 1):
                line = '| %d |' % Lt
                anyv = False
                for dn in PRIMARY[size]:
                    depth = P[(size, dn, W)]['depth']
                    cands = []
                    for k, s in S.items():
                        if k[0] == size and k[1] == dn and k[3] == W and k[4] == 'default' and k[2] != 'r' and s.get('n') and latency(k[2], depth) == Lt:
                            cands.append((-med(s['fmax']), k[2], s))
                    if not cands:
                        line += ' - |'
                        continue
                    anyv = True
                    cands.sort(key=lambda c: c[0])
                    _, v, s = cands[0]
                    line += ' %s: %s (%d cells) |' % (v, rng(s['fmax']), s['lc'])
                if anyv:
                    A(line)
            A('')
            A('(Where several variants have the same latency, the fastest by median is shown.)')
            A('')

    # ---------------- (d) ----------------
    A('# (d) Latency in clock cycles')
    A('')
    A('| points | design | depth (adder levels) | c | p (one level per clock) | p2 | r |')
    A('|---|---|---|---|---|---|---|')
    for size in ('8', '16', '64', '8x8'):
        for dn in ORDER:
            pf = P.get((size, dn, 8))
            if not pf or dn in ('xk265', 'xk264'):
                continue
            d = pf['depth']
            A('| %s | %s | %d | 1 | %d | %d | 2 |' % (size, NAMES[dn], d, d, -(-d // 2)))
    A('')

    # cross-check: the design inside the harness against the design synthesised alone (second.py, ice40)
    syn = [r for r in load('second_synth.jsonl') if r.get('family') == 'ice40' and 'error' not in r]
    same = diff = 0
    diffs = []
    for r in syn:
        s_ = S.get((r['size'], r['design_name'], r['variant'], r['W'], 'default'))
        if not s_ or not s_.get('yosys'):
            continue
        y = s_['yosys']
        a_ = (y.get('SB_LUT4', 0), y.get('SB_CARRY', 0))
        b_ = (r['lut'], r['carry'])
        if a_ == b_:
            same += 1
        else:
            diff += 1
            diffs.append('%s: in harness %s, alone %s' % (r['tag'], a_, b_))
    if syn:
        A('# Cross-check of the harness')
        A('')
        A('The design kept as its own module inside the harness has the same number of LUT4 and carry cells as the same file synthesised alone and flat (`synth_ice40 -top <design>`): '
          '%d of %d cases equal%s.' % (same, same + diff, '' if not diff else '; different: ' + '; '.join(diffs)))
        A('')
    second_opinion(A, P)
    compact(S, P)

    open(os.path.join(HERE, 'TABLES.md'), 'w').write('\n'.join(out) + '\n')
    json.dump(summary, open(os.path.join(HERE, 'summary.json'), 'w'), indent=1, sort_keys=True)
    print('wrote TABLES.md (%d lines), %d runs read' % (len(out), len(runs)))


if __name__ == '__main__':
    main()
