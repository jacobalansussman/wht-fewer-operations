#!/usr/bin/env python3
"""mutation_test.py -- does the simulation bench notice a wrong design?

Takes correct files from v/, damages each in one place, and runs the same bench
and the same vectors on the damaged copies (Icarus Verilog).  Every damaged
copy must show mismatches; the undamaged file run beside them must show none.
The damaged copies are written to work/mut/ and are never used for anything else.

USE (from fpga/rtl, after gen_rtl.py --all and sim/golden.py):
    python3 -B sim/mutation_test.py
Result: sim/MUTATION.txt
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)
import golden  # noqa: E402

BIN = os.path.join(os.environ.get('OSS_CAD_SUITE', '/opt/oss-cad-suite'), 'bin')      # the unpacked oss-cad-suite
MUT = os.path.join(ROOT, 'work', 'mut')

# (label, source file, module, latency, what is damaged, pattern, replacement)
CASES = [
    ('8_ours_c_w8: wire n_g7 one bit too narrow', '8_ours_c_w8', 0,
     'wire signed [10:0] n_g7 =', 'wire signed [9:0] n_g7 ='),
    ('8_ours_c_w8: wire n_g5 one bit too narrow', '8_ours_c_w8', 0,
     'wire signed [9:0] n_g5 =', 'wire signed [8:0] n_g5 ='),
    ('8_ours_c_w8: one sign changed in n_g10', '8_ours_c_w8', 0,
     'n_g10 = n_g8 + (x6 <<< 1)', 'n_g10 = n_g8 - (x6 <<< 1)'),
    ('8_ours_c_w8: a doubling dropped in n_y3', '8_ours_c_w8', 0,
     'n_y3 = n_g9 + (x3 <<< 1)', 'n_y3 = n_g9 + x3'),
    ('8_ours_p_w8: one delay register skipped (x6 taken one stage early)', '8_ours_p_w8', 6,
     'n_g10 = n_g8_r4 + (x6_r4 <<< 1)', 'n_g10 = n_g8_r4 + (x6_r3 <<< 1)'),
    ('8_ours_p_w8: valid one stage short', '8_ours_p_w8', 6,
     'assign out_valid = vld[5];', 'assign out_valid = vld[4];'),
    ('8_cfl1994_c_w8: wire n_t3 one bit too narrow', '8_cfl1994_c_w8', 0, None, None),
    ('16_ours_c_w8: wire n_p12 one bit too narrow', '16_ours_c_w8', 0, None, None),
]


def main():
    os.makedirs(MUT, exist_ok=True)
    out = []
    for N, tag in ((8, '8'), (16, '16')):
        Wd = 8
        with open(os.path.join(ROOT, 'work', 'vec', '%d_w%d.json' % (N, Wd))) as f:
            info = json.load(f)
        duts, files, labels = [], [], []
        n = 0
        for label, base, lat, pat, rep in CASES:
            if not base.startswith(tag + '_'):
                continue
            txt = open(os.path.join(ROOT, 'v', base + '.v')).read()
            if pat is None:
                node = re.search(r'wire n_(\w+) one bit', label).group(1)
                m = re.search(r'wire signed \[(\d+):0\] n_%s =' % node, txt)
                pat = m.group(0)
                rep = 'wire signed [%d:0] n_%s =' % (int(m.group(1)) - 1, node)
            assert txt.count(pat) == 1, (label, pat)
            mod = 'mut%d_%s' % (n, base)
            p = os.path.join(MUT, mod + '.v')
            with open(p, 'w') as f:
                f.write(txt.replace(pat, rep).replace('module wht_' + base, 'module ' + mod))
            duts.append(('MUTANT%d' % n, mod, lat))
            files.append(p)
            labels.append(label)
            n += 1
        # undamaged files beside them
        for base, lat in sorted(set((b, l) for _, b, l, _, _ in CASES if b.startswith(tag + '_'))):
            duts.append(('GOOD_' + base, 'wht_' + base, lat))
            files.append(os.path.join(ROOT, 'v', base + '.v'))
        save_tb = golden.TB
        golden.TB = MUT
        tb = golden.write_tb('mut' + tag, N, Wd, duts, info)
        golden.TB = save_tb
        vvp = os.path.join(MUT, 'mut%s.vvp' % tag)
        subprocess.check_call([BIN + '/iverilog', '-g2005', '-o', vvp, '-s', 'tb', tb] + files)
        log = subprocess.run([BIN + '/vvp', '-n', vvp], cwd=os.path.join(ROOT, 'work', 'vec'),
                             stdout=subprocess.PIPE, universal_newlines=True).stdout
        first = {}
        for m in re.finditer(r'MISMATCH (\w+) vector (\d+)', log):
            first.setdefault(m.group(1), int(m.group(2)))
        for m in re.finditer(r'RESULT (\w+) latency \d+ checked (\d+) errors (\d+)', log):
            name, chk, err = m.group(1), int(m.group(2)), int(m.group(3))
            if name.startswith('MUTANT'):
                i = int(name[6:])
                ok = err > 0
                out.append('%-70s %6d of %d vectors differ; first at vector %s (corner cases are vectors 0 to %d)   %s'
                           % (labels[i], err, chk, first.get(name, '-'), info['corner'] - 1,
                              'CAUGHT' if ok else 'NOT CAUGHT'))
            else:
                out.append('%-70s %6d of %d vectors differ   %s'
                           % (name[5:] + ' (undamaged)', err, chk, 'OK' if err == 0 else 'WRONG'))
    txt = '\n'.join(out) + '\n'
    with open(os.path.join(HERE, 'MUTATION.txt'), 'w') as f:
        f.write(txt)
    sys.stdout.write(txt)
    if 'NOT CAUGHT' in txt or 'WRONG' in txt:
        sys.exit(1)


if __name__ == '__main__':
    main()
