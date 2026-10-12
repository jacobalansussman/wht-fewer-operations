#!/usr/bin/env python3
"""mkvariants.py -- write whti.h and variants.c from the list of steps and styles.

    python3 mkvariants.py

The steps are the blocks of kernels.inc, the styles the three of whti.c.  variants.c is the list
the harness reads (name, function, scale, sizes, one line of description); the first of each list
is FFHT.
"""
KERNS = ['T', 'N', 'NF', 'Nm', 'Nc', 'NFc', 'Ns', 'G', 'N2', 'N3']
DESC = {
    'T':   ('exact', 'textbook step, 24 add/sub'),
    'N':   ('scale', 'new step, 19 add/sub + 1 mul by 0.5; H x / 2^P'),
    'NF':  ('scale', 'new step, halving fused: 17 add/sub + 2 fmsub; H x / 2^P'),
    'Nm':  ('exact', 'new step; one pass with 8 more mul by 2^P'),
    'Nc':  ('exact', 'new step; one pass as 7 add/sub + 1 mul + 12 fma with 2^P'),
    'NFc': ('exact', 'new step with fused halving; one pass as 7 add/sub + 1 mul + 12 fma with 2^P'),
    'Ns':  ('exact', 'new step; then a loop that multiplies every number by 2^P'),
    'G':   ('exact', '19-gate form: 7 add/sub + 12 fma in every 8-register pass'),
    'N2':  ('scale', 'new step, lines in the order outputs-first; H x / 2^P'),
    'N3':  ('scale', 'new step, lines in the order g9-side-first; H x / 2^P'),
}
STYLE = {'': 'mask levels in a register, loads as gcc likes',
         'p': 'mask levels in a register, 8 loads first',
         'q': "FFHT's levels in a register, 8 loads first",
         'w': 'staggered passes, mask levels level by level, loads as gcc likes',
         'wp': 'staggered passes, mask levels level by level, 8 loads first'}


# the variants that are also taken from the second copy of whti.c (jumps inside 32-byte blocks)
J32 = [('T', ''), ('N', ''), ('NF', ''), ('Nc', ''), ('NFc', ''), ('Nm', ''), ('G', ''), ('T', 'p'), ('N', 'p'), ('NF', 'p'), ('NFc', 'p'), ('T', 'q'), ('N', 'q'),
       ('T', 'w'), ('N', 'w'), ('NF', 'w'), ('T', 'wp'), ('N', 'wp'), ('NF', 'wp')]


KERNS_W = ['T', 'N', 'NF', 'Nc', 'NFc', 'G']         # the steps of kernels_w.inc (styles w, wp)


def names():
    for s in ('', 'p', 'q'):
        for k in KERNS:
            if s == 'q' and k in ('N2', 'N3'):
                continue
            yield k, s
    for s in ('w', 'wp'):
        for k in KERNS_W:
            yield k, s


h = ['/* whti.h -- written by mkvariants.py; see whti.c */', '#ifndef WHTI_H', '#define WHTI_H']
c = ['/* variants.c -- the list of transforms for the harness (../harness/harness.c, unchanged).',
     ' * Written by mkvariants.py; the first of each list is FFHT. */',
     '#include <stddef.h>', '#include "variants.h"', '#include "fht.h"', '#include "whti.h"', '',
     'static void ffht_f(float *b, int k) { (void)fht_float(b, k); }',
     'static void ffht_d(double *b, int k) { (void)fht_double(b, k); }', '']
for t, T in (('f', 'float'), ('d', 'double')):
    c.append('const variant_%s variants_%s[] = {' % (t, t))
    c.append('    {"ffht", ffht_%s, NULL, 1, 30, "FFHT fht_%s: its own fht.o, built by its own Makefile"},' % (t, T))
    for k, s in names():
        h.append('void whti_%s%s_%s(%s *buf, int k);' % (k, s, t, T))
        sc = 'whti_P_%s' % t if DESC[k][0] == 'scale' else 'NULL'
        c.append('    {"%s%s", whti_%s%s_%s, %s, 3, 30, "%s [%s]"},' % (k, s, k, s, t, sc, DESC[k][1], STYLE[s]))
    for k, s in J32:
        sc = 'whti_P_%s' % t if DESC[k][0] == 'scale' else 'NULL'
        c.append('    {"%s%sj", j32_whti_%s%s_%s, %s, 3, 30, "%s [%s; jumps kept inside 32-byte blocks]"},' % (k, s, k, s, t, sc, DESC[k][1], STYLE[s]))
    c.append('};')
    c.append('const int n_variants_%s = (int)(sizeof variants_%s / sizeof variants_%s[0]);' % (t, t, t))
    c.append('')
h += ['int whti_P_f(int k);', 'int whti_P_d(int k);']
h += ['/* the same file compiled with -Wa,-mbranches-within-32B-boundaries (Makefile, J32) */']
for t, T in (('f', 'float'), ('d', 'double')):
    for k, s in J32:
        h.append('void j32_whti_%s%s_%s(%s *buf, int k);' % (k, s, t, T))
h += ['#endif']
open('whti.h', 'w').write('\n'.join(h) + '\n')
open('variants.c', 'w').write('\n'.join(c))
