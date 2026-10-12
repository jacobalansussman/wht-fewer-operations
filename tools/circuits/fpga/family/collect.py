#!/usr/bin/env python3
"""collect.py -- read paper.json, synth_out/*.json, pnr/*.log and print the tables (Markdown).
Also writes results.json.  Standard library only.  Use: python3 -B collect.py > tables.md
"""
import glob
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIZES = [16, 32, 64, 128, 256]
DES = ['textbook', 'cfl1994', 'family']
LAB = {'textbook': 'textbook', 'cfl1994': '1994', 'family': 'family'}
WIDTHS = [9, 12]


def cells(path):
    if not os.path.exists(path):
        return None
    try:
        d = json.load(open(path))
    except Exception:
        return None
    m = list(d['modules'].values())[0]
    return m.get('num_cells_by_type', {})


def syn(N, d, v, W, fam):
    c = cells(os.path.join(HERE, 'synth_out', '%d_%s_%s_w%d.%s.json' % (N, d, v, W, fam)))
    if c is None:
        return None
    if fam == 'ice40':
        return dict(lut=c.get('SB_LUT4', 0), carry=c.get('SB_CARRY', 0),
                    ff=sum(n for k, n in c.items() if k.startswith('SB_DFF')), raw=c)
    if fam == 'ecp5':
        return dict(lut4=c.get('LUT4', 0), ccu=c.get('CCU2C', 0), lut=c.get('LUT4', 0) + 2 * c.get('CCU2C', 0),
                    ff=c.get('TRELLIS_FF', 0), mux=c.get('PFUMX', 0) + c.get('L6MUX21', 0), raw=c)
    lut = sum(n for k, n in c.items() if re.fullmatch(r'LUT[1-6]', k))
    return dict(lut=lut, carry4=c.get('CARRY4', 0), ff=sum(n for k, n in c.items() if k.startswith('FD')),
                srl=c.get('SRL16E', 0) + c.get('SRLC32E', 0), muxf=c.get('MUXF7', 0) + c.get('MUXF8', 0), raw=c)


def nplog(path):
    """Utilisation and maximum frequency from a nextpnr log."""
    if not os.path.exists(path):
        return None
    t = open(path, errors='replace').read()
    r = dict(util={}, fmax=None, error=None)
    for m in re.finditer(r'Info:\s+(\w+):\s*(\d+)/\s*(\d+)', t):
        r['util'][m.group(1)] = int(m.group(2))
    f = re.findall(r"Max frequency for clock\s+'[^']*':\s*([\d.]+) MHz", t)
    if f:
        r['fmax'] = float(f[-1])
    e = re.findall(r'ERROR: (.*)', t)
    if e:
        r['error'] = e[0][:160]
    r['routed'] = bool(re.search(r'Program finished normally|Routing complete', t)) and not e
    return r


def unit(fam, u):
    if fam == 'ice40':
        return dict(cells=u.get('ICESTORM_LC', 0))
    return dict(comb=u.get('TRELLIS_COMB', 0), ff=u.get('TRELLIS_FF', 0))


def packed(N, d, v, W, fam):
    a = nplog(os.path.join(HERE, 'pnr', '%d_%s_%s_w%d.%s.pack.log' % (N, d, v, W, fam)))
    b = nplog(os.path.join(HERE, 'pnr', '%d_null_c_w%d.%s.pack.log' % (N, W, fam)))
    if not a or not b or not a['util'] or not b['util']:
        return None
    ua, ub = unit(fam, a['util']), unit(fam, b['util'])
    return dict((k, ua[k] - ub[k]) for k in ua), ua, ub


def placed(N, d, v, W, fam):
    """Per seed: cells with the wrapper subtracted (same seed's null where it exists, else seed 1), fmax."""
    out = []
    for s in (1, 2, 3):
        a = nplog(os.path.join(HERE, 'pnr', '%d_%s_%s_w%d.%s.s%d.log' % (N, d, v, W, fam, s)))
        if a is None:
            continue
        b = nplog(os.path.join(HERE, 'pnr', '%d_null_c_w%d.%s.s%d.log' % (N, W, fam, s))) or \
            nplog(os.path.join(HERE, 'pnr', '%d_null_c_w%d.%s.s1.log' % (N, W, fam)))
        err = a['error']
        bn = '%d_%s_%s_w%d' % (N, d, v, W)
        byhand = os.path.join(HERE, 'jobs', 'STOPPED_BY_HAND.txt')
        if err and 'ICESTORM_LC' in err and a['util']:
            err = 'does not fit: %d logic cells with the wrapper, 7,680 on the chip' % a['util'].get('ICESTORM_LC', 0)
        elif not a['routed'] and not err:
            if os.path.exists(byhand) and (bn + ' ' + fam) in open(byhand).read():
                err = 'not routed: stopped by hand after 6 of its 10 minutes, with 92,550 connections still to route (111,173 at the start of routing); after placement the tool estimated %s MHz' % a['fmax']
            else:
                err = 'not routed within the 10-minute limit; after placement the tool estimated %s MHz' % a['fmax']
        rec = dict(seed=s, fmax=a['fmax'] if a['routed'] else None, error=err, routed=a['routed'],
                   total=unit(fam, a['util']) if a['util'] else None)
        if a['util'] and b and b['util']:
            ua, ub = unit(fam, a['util']), unit(fam, b['util'])
            rec['net'] = dict((k, ua[k] - ub[k]) for k in ua)
        out.append(rec)
    return out


def ratio(a, b):
    return '%.3f' % (a / b) if a and b else '-'


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def fm(x, f='%d'):
    return '-' if x is None else f % x


def main():
    paper = json.load(open(os.path.join(HERE, 'paper.json')))
    P = dict(((r['N'], r['design'], r['W']), r) for r in paper)
    R = {}
    o = []
    w = o.append

    # ---- table 1: on paper
    w('### Table 1. On paper (from the circuit text; widths exact, counted by gen_rtl.py)\n')
    w('| N | design | adders | of them subtractions | depth (adder levels) | adder bits W=9 | adder bits W=12 | '
      'pipelined register bits W=9: after adders + delay = total | the same, W=12 |')
    w('|---|---|---|---|---|---|---|---|---|')
    for N in SIZES:
        for d in DES:
            a, b = P[(N, d, 9)], P[(N, d, 12)]
            w('| %d | %s | %d | %d | %d | %d | %d | %d + %d = %d | %d + %d = %d |'
              % (N, LAB[d], a['adders'], a['subtractors'], a['depth'], a['adder_bits'], b['adder_bits'],
                 a['reg_after_adders'], a['reg_delay'], a['reg_data'],
                 b['reg_after_adders'], b['reg_delay'], b['reg_data']))
    w('')

    for W in WIDTHS:
        # ---- table 2: synthesis, combinational
        w('### Table 2 (W = %d). Synthesis, combinational variant, bare core (no wrapper, no placement)\n' % W)
        w('| N | design | iCE40: SB_LUT4 | iCE40: SB_CARRY | ECP5: LUT4 | ECP5: CCU2C | ECP5: LUT4 + 2 x CCU2C | '
          'Xilinx 7: LUTs | Xilinx 7: CARRY4 |')
        w('|---|---|---|---|---|---|---|---|---|')
        for N in SIZES:
            for d in DES:
                i, e, x = syn(N, d, 'c', W, 'ice40'), syn(N, d, 'c', W, 'ecp5'), syn(N, d, 'c', W, 'xilinx')
                R[(N, d, 'c', W)] = dict(ice40=i, ecp5=e, xilinx=x)
                w('| %d | %s | %s | %s | %s | %s | %s | %s | %s |'
                  % (N, LAB[d], fm(i and i['lut']), fm(i and i['carry']), fm(e and e['lut4']), fm(e and e['ccu']),
                     fm(e and e['lut']), fm(x and x['lut']), fm(x and x['carry4'])))
        w('')
        # ---- table 3: synthesis, pipelined
        w('### Table 3 (W = %d). Synthesis, pipelined variant (a register after every adder level), bare core\n' % W)
        w('| N | design | iCE40: SB_LUT4 | iCE40: flip-flops | ECP5: LUT4 + 2 x CCU2C | ECP5: flip-flops | '
          'Xilinx 7: LUTs | Xilinx 7: shift-register LUTs (SRL16E + SRLC32E) | Xilinx 7: flip-flops | Xilinx 7: CARRY4 |')
        w('|---|---|---|---|---|---|---|---|---|---|')
        for N in SIZES:
            for d in DES:
                i, e, x = syn(N, d, 'p', W, 'ice40'), syn(N, d, 'p', W, 'ecp5'), syn(N, d, 'p', W, 'xilinx')
                R[(N, d, 'p', W)] = dict(ice40=i, ecp5=e, xilinx=x)
                w('| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s |'
                  % (N, LAB[d], fm(i and i['lut']), fm(i and i['ff']), fm(e and e['lut']), fm(e and e['ff']),
                     fm(x and x['lut']), fm(x and x['srl']), fm(x and x['ff']), fm(x and x['carry4'])))
        w('')
        # ---- table 4: packing
        w('### Table 4 (W = %d). After packing by nextpnr (--pack-only), wrapper subtracted\n' % W)
        w('iCE40: logic cells (ICESTORM_LC; one cell = one LUT4 + carry + one flip-flop).  '
          'ECP5: TRELLIS_COMB (LUT4 places; a CCU2C takes two) and TRELLIS_FF.  '
          'In brackets: the wrapper alone (null core), which was subtracted.\n')
        w('| N | design | iCE40 cells, combinational | iCE40 cells, pipelined | ECP5 COMB, combinational | '
          'ECP5 COMB + FF, pipelined |')
        w('|---|---|---|---|---|---|')
        for N in SIZES:
            for d in DES:
                row = '| %d | %s |' % (N, LAB[d])
                for fam in ('ice40', 'ecp5'):
                    for v in ('c', 'p'):
                        pk = packed(N, d, v, W, fam)
                        R[(N, d, v, W)]['pack_' + fam] = pk and pk[0]
                        if not pk:
                            row += ' - |'
                        elif fam == 'ice40':
                            row += ' %d (wrapper %d) |' % (pk[0]['cells'], pk[2]['cells'])
                        elif v == 'c':
                            row += ' %d (wrapper %d; FF %d) |' % (pk[0]['comb'], pk[2]['comb'], pk[0]['ff'])
                        else:
                            row += ' %d + %d = %d |' % (pk[0]['comb'], pk[0]['ff'], pk[0]['comb'] + pk[0]['ff'])
                w(row)
        w('')
        # ---- table 5: place and route
        w('### Table 5 (W = %d). Place and route (nextpnr 0.11.1-59, --freq 200, seeds 1, 2, 3), wrapper subtracted\n' % W)
        w('| N | design | variant | chip | cells per seed (wrapper subtracted) | maximum frequency per seed, MHz | median MHz | note |')
        w('|---|---|---|---|---|---|---|---|')
        for N in SIZES:
            for fam, chip in (('ice40', 'iCE40-HX8K ct256'), ('ecp5', 'ECP5 LFE5U-85F CABGA381')):
                for v in ('c', 'p'):
                    for d in DES:
                        pl = placed(N, d, v, W, fam)
                        R[(N, d, v, W)]['pnr_' + fam] = pl
                        if not pl:
                            continue
                        cs = []
                        for r in pl:
                            n = r.get('net')
                            if not n:
                                cs.append('-')
                            elif fam == 'ice40':
                                cs.append('%d' % n['cells'])
                            else:
                                cs.append('%d COMB + %d FF' % (n['comb'], n['ff']))
                        fs = [r['fmax'] for r in pl]
                        es = sorted(set(r['error'] for r in pl if r['error']))
                        note = '; '.join(es) if len(es) == 1 and all(r['error'] for r in pl) else \
                            '; '.join('seed %d: %s' % (r['seed'], r['error']) for r in pl if r['error'])
                        w('| %d | %s | %s | %s | %s | %s | %s | %s |'
                          % (N, LAB[d], {'c': 'combinational', 'p': 'pipelined'}[v], chip, ' / '.join(cs),
                             ' / '.join(fm(f, '%.2f') for f in fs), fm(med(fs), '%.2f'), note))
        w('')

    # ---- the table that answers the question, W = 9 and W = 12
    for W in WIDTHS:
        w('### Table 6 (W = %d). The answer: one block per size\n' % W)
        w('Columns: adders and adder bits are on paper.  LUTs are after synthesis of the combinational variant '
          '(iCE40: SB_LUT4; ECP5: LUT4 + 2 x CCU2C; Xilinx 7-series: LUTs, and CARRY4 cells).  "Placed" is after '
          'place and route with the wrapper subtracted (median of the seeds that ran; iCE40-HX8K logic cells, '
          'ECP5-85F TRELLIS_COMB); where a design was only packed, the packed figure is given with "(packed)".  '
          'MHz is the median maximum frequency of the combinational variant between the wrapper\'s registers.  '
          'The last three columns are the pipelined variant, registers included: iCE40 logic cells after packing; '
          'ECP5 COMB + FF after packing; Xilinx LUTs + shift-register LUTs + flip-flops after synthesis.\n')
        w('| N | design | adders | adder bits | iCE40 LUT4 | ECP5 LUT | Xilinx LUT | Xilinx CARRY4 | iCE40 placed cells | '
          'ECP5 placed COMB | depth | iCE40 MHz | ECP5 MHz | pipelined: iCE40 cells | pipelined: ECP5 COMB+FF | '
          'pipelined: Xilinx LUT+SRL+FF |')
        w('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        for N in SIZES:
            vals = {}
            for d in DES:
                p = P[(N, d, W)]
                rc, rp = R[(N, d, 'c', W)], R[(N, d, 'p', W)]
                v = {}
                v['adders'] = p['adders']
                v['bits'] = p['adder_bits']
                v['ice'] = rc['ice40'] and rc['ice40']['lut']
                v['ecp'] = rc['ecp5'] and rc['ecp5']['lut']
                v['xil'] = rc['xilinx'] and rc['xilinx']['lut']
                v['xc4'] = rc['xilinx'] and rc['xilinx']['carry4']
                pi = [r for r in (rc.get('pnr_ice40') or []) if r['routed'] and r.get('net')]
                pe = [r for r in (rc.get('pnr_ecp5') or []) if r['routed'] and r.get('net')]
                v['ice_pl'] = med([r['net']['cells'] for r in pi])
                v['ice_pl_tag'] = ''
                if v['ice_pl'] is None and rc.get('pack_ice40'):
                    v['ice_pl'] = rc['pack_ice40']['cells']
                    v['ice_pl_tag'] = ' (packed)'
                v['ecp_pl'] = med([r['net']['comb'] for r in pe])
                v['ecp_pl_tag'] = ''
                if v['ecp_pl'] is None and rc.get('pack_ecp5'):
                    v['ecp_pl'] = rc['pack_ecp5']['comb']
                    v['ecp_pl_tag'] = ' (packed)'
                v['depth'] = p['depth']
                v['ice_f'] = med([r['fmax'] for r in pi])
                v['ecp_f'] = med([r['fmax'] for r in pe])
                v['p_ice'] = rp.get('pack_ice40') and rp['pack_ice40']['cells']
                v['p_ecp'] = rp.get('pack_ecp5') and (rp['pack_ecp5']['comb'] + rp['pack_ecp5']['ff'])
                x = rp['xilinx']
                v['p_xil'] = x and (x['lut'] + x['srl'] + x['ff'])
                vals[d] = v
                w('| %d | %s | %d | %d | %s | %s | %s | %s | %s%s | %s%s | %d | %s | %s | %s | %s | %s |'
                  % (N, LAB[d], v['adders'], v['bits'], fm(v['ice']), fm(v['ecp']), fm(v['xil']), fm(v['xc4']),
                     fm(v['ice_pl']), v['ice_pl_tag'], fm(v['ecp_pl']), v['ecp_pl_tag'], v['depth'],
                     fm(v['ice_f'], '%.2f'), fm(v['ecp_f'], '%.2f'), fm(v['p_ice']), fm(v['p_ecp']), fm(v['p_xil'])))
            keys = ['adders', 'bits', 'ice', 'ecp', 'xil', 'xc4', 'ice_pl', 'ecp_pl', 'depth', 'ice_f', 'ecp_f',
                    'p_ice', 'p_ecp', 'p_xil']
            for lab, a, b in (('family / textbook', 'family', 'textbook'), ('family / 1994', 'family', 'cfl1994')):
                w('| %d | **%s** | %s |' % (N, lab, ' | '.join(ratio(vals[a][k], vals[b][k]) for k in keys)))
            R[('answer', N, W)] = vals
        w('')
    # ---- table 7: the 1994 design with every line kept as one adder
    w('### Table 7 (W = 9). Sensitivity: every adder line kept as written ("(* keep *)" on every adder wire), combinational\n')
    w('By default yosys merges the two additions z0 = x1 + x2, z1 = z0 + x3 of the 1994 circuit into one sum of three '
      '(a row of full adders in LUTs and one carry chain).  With the attribute it cannot.  '
      'Textbook and family were run this way at 16 and 32 points only, as a control.\n')
    w('| N | design | iCE40 SB_LUT4: default -> kept | ECP5 LUT4 + 2 x CCU2C: default -> kept | '
      'Xilinx LUTs: default -> kept | Xilinx CARRY4: default -> kept |')
    w('|---|---|---|---|---|---|')
    K = {}
    for N in SIZES:
        for d in DES:
            row, any_ = '| %d | %s |' % (N, LAB[d]), False
            for fam, key in (('ice40', 'lut'), ('ecp5', 'lut'), ('xilinx', 'lut'), ('xilinx', 'carry4')):
                c = cells(os.path.join(HERE, 'synth_keep', '%d_%s_c_w9.%s.json' % (N, d, fam)))
                dflt = R[(N, d, 'c', 9)][fam]
                if c is None:
                    row += ' - |'
                    continue
                any_ = True
                if fam == 'ice40':
                    kv = c.get('SB_LUT4', 0)
                elif fam == 'ecp5':
                    kv = c.get('LUT4', 0) + 2 * c.get('CCU2C', 0)
                elif key == 'lut':
                    kv = sum(n for k, n in c.items() if re.fullmatch(r'LUT[1-6]', k))
                else:
                    kv = c.get('CARRY4', 0)
                K[(N, d, fam, key)] = kv
                row += ' %s -> %d |' % (fm(dflt and dflt[key]), kv)
            if any_:
                w(row)
    w('')
    w('Family (default) divided by 1994 (kept), W = 9, combinational:\n')
    w('| N | adders | adder bits | iCE40 SB_LUT4 | ECP5 LUT4 + 2 x CCU2C | Xilinx LUTs | Xilinx CARRY4 |')
    w('|---|---|---|---|---|---|---|')
    for N in SIZES:
        f = R[(N, 'family', 'c', 9)]
        row = '| %d | %s | %s |' % (N, ratio(P[(N, 'family', 9)]['adders'], P[(N, 'cfl1994', 9)]['adders']),
                                    ratio(P[(N, 'family', 9)]['adder_bits'], P[(N, 'cfl1994', 9)]['adder_bits']))
        for fam, key in (('ice40', 'lut'), ('ecp5', 'lut'), ('xilinx', 'lut'), ('xilinx', 'carry4')):
            row += ' %s |' % ratio(f[fam] and f[fam][key], K.get((N, 'cfl1994', fam, key)))
        w(row)
    w('')
    sys.stdout.write('\n'.join(o) + '\n')
    with open(os.path.join(HERE, 'results.json'), 'w') as f:
        json.dump(dict((' '.join(str(x) for x in k), v) for k, v in R.items()), f, indent=1, default=str)


if __name__ == '__main__':
    main()
