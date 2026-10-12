#!/usr/bin/env python3
"""kloop_gen.py -- one pass of 8 registers and 3 levels, alone, for every kernel: C on stdout.

  python3 -B kloop_gen.py > kloop/kloop_passes.c         (run in the style-generator folder)

Each function  void kloop_T_K_L(T *buf)  is exactly what the patched gen.py writes for the pass
that does the three highest levels of an array of 2^L numbers (composite_step: its loops, its
assembly block), with kernel K:
    T    FFHT's textbook block          (24 additions and subtractions)
    H20  the 20-operation block         (19 additions and subtractions, 1 multiplication by 1/2)
    F19m the 19-gate block with FMA, the constant 2 as a memory operand
    F19r the same, the constant 2 loaded once per block into a register
    H20x the 20-operation block as the pass that repairs the scale: 8 more multiplications,
         their constant as a memory operand of each
    H20xr the same with that constant loaded once into a free register (1 instruction more)
and two kernels that do NOT compute the transform and exist only to be timed.  They separate
the number of operations from the length of the longest chain of operations:
    S20  20 additions and subtractions, longest chain 3: the textbook block without 4 of its
         last 8 operations (4 results are stored one level early)
    D24  24 additions and subtractions, longest chain 7: the 20-operation block with an addition
         in place of its halving, and 4 more additions whose results nobody uses
So T and D24 have the same instructions and differ in the chain; H20 and S20 have the same
number of operations and differ in the chain.
The sizes: L = 9 and 12 for floats, 8 and 11 for doubles (2 KiB and 16 KiB of data: both inside
the first-level cache of 32 KiB), so that the time is the time of the instructions and not of
the memory.  kloop_main.c times them.
"""
import sys

import k8kernel
import gen

SHALLOW20_TEXT = """
t1 = x0 + x1
t2 = x0 - x1
t3 = x2 + x3
t4 = x2 - x3
t5 = x4 + x5
t6 = x4 - x5
t7 = x6 + x7
t8 = x6 - x7
t9 = t1 + t3
t10 = t1 - t3
t11 = t2 + t4
t12 = t2 - t4
t13 = t5 + t7
t14 = t5 - t7
t15 = t6 + t8
t16 = t6 - t8
t17 = t9 + t13
t18 = t9 - t13
t19 = t11 + t15
t20 = t11 - t15
y0 = t17
y1 = t19
y2 = t10
y3 = t12
y4 = t18
y5 = t20
y6 = t14
y7 = t16
"""
DEEP24_TEXT = """
g1 = x0 + x7
g2 = x1 + x6
g3 = x2 - x5
g4 = x3 - x4
e1 = x1 + x3
e2 = x4 + x5
e3 = x6 + x7
e4 = x1 - x6
g5 = g1 - g2
g6 = g3 + g4
g7 = g5 - g6
m8 = g7 + g1
g9 = m8 - x7
g10 = m8 - x5
g11 = g9 + x6
g12 = g10 - x4
g13 = g11 + g4
g14 = g10 + x3
g15 = g5 - g14
g16 = g11 + g3
g17 = g12 + g2
g18 = g9 + x1
g19 = g18 + g6
g20 = g1 - g12
y0 = g20
y1 = g16
y2 = g18
y3 = g14
y4 = g19
y5 = g15
y6 = g17
y7 = g13
"""
k8kernel.CIRCUITS['shallow20'] = k8kernel.parse(SHALLOW20_TEXT)     # timing only: not the transform
k8kernel.CIRCUITS['deep24'] = k8kernel.parse(DEEP24_TEXT)           # timing only: not the transform

# (name, kernel, constant 2 of fma19, scale, constant 2^P of the repairing pass)
KERNELS = [('T', 'textbook', 'mem', 'raw', 'mem'), ('H20', 'half20', 'mem', 'raw', 'mem'),
           ('H20x', 'half20', 'mem', 'exact', 'mem'), ('H20xr', 'half20', 'mem', 'exact', 'reg'),
           ('F19m', 'fma19', 'mem', 'raw', 'mem'), ('F19r', 'fma19', 'reg', 'raw', 'mem'),
           ('S20', 'shallow20', 'mem', 'raw', 'mem'), ('D24', 'deep24', 'mem', 'raw', 'mem')]
SIZES = {'float': (9, 12), 'double': (8, 11)}
STEP = {'float': gen.float_avx_composite_step, 'double': gen.double_avx_composite_step}

out = ['/* written by kloop_gen.py with the patched gen.py: do not edit */\n']
k8kernel.SCALE = 'exact'
for kernel in ('half20', 'fma19'):
    k8kernel.KERNEL = kernel
    out.append(k8kernel.preamble())
names = []
for tag, kernel, fmac, scale, scalec in KERNELS:
    k8kernel.KERNEL = kernel
    k8kernel.FMA_CONST = fmac
    k8kernel.SCALE = scale
    k8kernel.SCALE_CONST = scalec
    for type_name in ('float', 'double'):
        for log_n in SIZES[type_name]:
            body = STEP[type_name]('buf', log_n, log_n - 3, log_n, '  ')
            body = k8kernel.finish(body, type_name, 0)
            name = 'kloop_%s_%s_%d' % (type_name, tag, log_n)
            out.append('void %s(%s *buf);\nvoid %s(%s *buf) {\n%s}\n' % (name, type_name, name, type_name, body))
            names.append((type_name, tag, log_n, name))
sys.stdout.write(''.join(out))
with open('kloop/kloop_list.inc', 'w') as f:
    for type_name, tag, log_n, name in names:
        f.write('void %s(%s *buf);\n' % (name, type_name))
    for type_name in ('float', 'double'):
        f.write('static const struct { const char *kernel; int log_n; void (*f)(%s *); } list_%s[] = {\n' % (type_name, type_name))
        for tn, tag, log_n, name in names:
            if tn == type_name:
                f.write('    {"%s", %d, %s},\n' % (tag, log_n, name))
        f.write('};\n')
