#!/usr/bin/env python3
"""mca.py -- what a model of the processor says about the loops of the steps (llvm-mca).

    python3 mca.py build2/whti.dis [llvm-mca program]

For the base block of 2^14 numbers of some variants (whti_<variant>_<f|d>_k14_d12) every
innermost loop is cut out of the listing, written as assembly text, and given to llvm-mca for
two processor models: broadwell (one unit for vector additions, as the published tables say for
the processor this machine reports) and skylake (two units).  Printed per loop: the instructions,
the micro-operations, and the cycles per turn the model predicts when the loop runs many times
(its "Total Cycles" for 1000 turns / 1000), and the model's lower bound from the units alone
("Block RThroughput").  A model is not a measurement; it is here to say which unit is the limit.
"""
import re
import subprocess
import sys

sys.path.insert(0, '.')
from asmcount import read, loops, count      # noqa: E402

MCA = sys.argv[2] if len(sys.argv) > 2 else 'llvm-mca-18'
funcs = read(sys.argv[1])
WHICH = ['T', 'N', 'NF', 'Nm', 'Nc', 'G', 'Tp', 'Nmp', 'Tq']
print('%-22s %4s %5s %5s | %-28s | %-28s' % ('function', 'loop', 'instr', 'uops', 'broadwell: cycles/turn (bound)', 'skylake: cycles/turn (bound)'))
for t in 'fd':
    for v in WHICH:
        nm = 'whti_%s_%s_k14_d12' % (v, t)
        if nm not in funcs:
            print('%s: not in the listing (merged with an identical function)' % nm)
            continue
        ins = funcs[nm]
        for n, (s, e) in enumerate(loops(ins)):
            lines = ['.L0:']
            for a, mn, ops in ins[s:e + 1]:
                if mn.startswith('j'):
                    ops = '.L0'
                lines.append('\t%s\t%s' % (mn, ops))
            text = '\n'.join(lines) + '\n'
            cells = []
            uops = '?'
            for cpu in ('broadwell', 'skylake'):
                r = subprocess.run([MCA, '-mcpu=' + cpu, '-iterations=1000'], input=text, capture_output=True, text=True)
                m1 = re.search(r'Total Cycles:\s+(\d+)', r.stdout)
                m2 = re.search(r'Block RThroughput:\s+([\d.]+)', r.stdout)
                m3 = re.search(r'Total uOps:\s+(\d+)', r.stdout)
                if not m1:
                    cells.append('failed: ' + r.stderr.strip().split('\n')[0][:60])
                    continue
                uops = '%d' % (int(m3.group(1)) / 1000)
                cells.append('%.2f (%.2f)' % (int(m1.group(1)) / 1000.0, float(m2.group(1))))
            c = count(ins, s, e)
            print('%-22s %4d %5d %5s | %-28s | %-28s' % (nm, n + 1, c['total'], uops, cells[0], cells[1]))
