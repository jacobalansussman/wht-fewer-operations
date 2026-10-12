#!/usr/bin/env python3
"""check_counts.py -- count adders and register bits in the Verilog files with yosys,
and compare with the numbers gen_rtl.py reports (designs.json).

For every file: yosys reads it, runs "proc" and "opt_clean" only (nothing is
optimised away), and writes the netlist as JSON.  Counted from that netlist:
  adders        cells of type $add or $sub
  adder bits    the sum of their output widths
  register bits the sum of the widths of the $dff cells
The script fails if any number differs from designs.json.

USE (from fpga/rtl):  python3 -B check_counts.py      ->  COUNTS.txt
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(os.environ.get('OSS_CAD_SUITE', '/opt/oss-cad-suite'), 'bin')      # the unpacked oss-cad-suite
ENV = dict(os.environ, PATH=BIN + ':' + os.environ.get('PATH', ''))
TMP = os.path.join(HERE, 'work', 'counts')


def count(vfile, module):
    js = os.path.join(TMP, module + '.json')
    subprocess.check_call([BIN + '/yosys', '-q', '-p',
                           'read_verilog %s; hierarchy -top %s; proc; opt_clean; write_json %s' % (vfile, module, js)],
                          env=ENV, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(js) as f:
        cells = json.load(f)['modules'][module]['cells']
    os.remove(js)
    add = bits = ff = other = 0
    for c in cells.values():
        t = c['type']
        if t in ('$add', '$sub'):
            add += 1
            bits += int(c['parameters']['Y_WIDTH'], 2)
        elif t == '$dff':
            ff += int(c['parameters']['WIDTH'], 2)
        elif t in ('$shl', '$sshl'):
            pass
        else:
            other += 1
    return add, bits, ff, other


def main():
    os.makedirs(TMP, exist_ok=True)
    with open(os.path.join(HERE, 'designs.json')) as f:
        dj = json.load(f)
    out, bad = [], 0
    for r in dj['designs']:
        for vn, e in r['files'].items():
            add, bits, ff, other = count(os.path.join(HERE, e['file']), e['module'])
            if vn == 'c':
                want_ff = 0
            elif vn == 'p':
                want_ff = r['reg_data'] + r['reg_valid']
            elif vn == 'p2':
                want_ff = r['p2_reg_data'] + r['p2_latency']
            else:
                want_ff = r['r_reg_data'] + r['r_reg_valid']
            ok = (add == r['adders'] and bits == r['adder_bits'] and ff == want_ff and other == 0)
            bad += not ok
            out.append('%-22s adders %4d (gen_rtl %4d)  adder bits %5d (%5d)  register bits %6d (%6d)  %s'
                       % (os.path.basename(e['file']), add, r['adders'], bits, r['adder_bits'], ff, want_ff,
                          'same' if ok else 'DIFFERENT'))
    out.append('%d files, %d with a difference' % (len(out), bad))
    with open(os.path.join(HERE, 'COUNTS.txt'), 'w') as f:
        f.write('\n'.join(out) + '\n')
    print('\n'.join(out[-3:]))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
