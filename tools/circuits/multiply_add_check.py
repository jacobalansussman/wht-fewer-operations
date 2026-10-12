#!/usr/bin/env python3
"""multiply_add_check.py -- is every line of every circuit file one operation of the 1994 paper?

usage: python3 -B tools/circuits/multiply_add_check.py

Standard library only.  It takes a second.

Coppersmith, Feig and Linzer (1994, page 969) charge one for a multiply-add, which computes +-a +- b*c, and
one for a plain addition or a plain multiplication.  Count (G) of this folder is wider: it charges one for
any a*u + b*v, with a constant allowed on both terms.  This program reads every circuit file under
programs/ with the reader of slp.py and looks at the shape of every line:

    one term, no constant        a renaming of an output; no operation
    one term with a constant     one plain multiplication
    two terms, no constant       one plain addition or subtraction
    two terms, one constant      one multiply-add
    two terms, two constants     NOT one operation of the 1994 paper
    more than two terms          NOT one operation of any count here

If no line has one of the last two shapes, every count (G) in this folder is also a count of multiply-adds in
the sense of the 1994 paper, and the comparison with its formulas is like for like.

The last line is "OK ..." with exit code 0, or "FAILED ..." with the first such line and exit code 1.
This is a check by a Python program of the shape of the lines.  That the circuits compute the transform is
checked by run.py."""
import sys
sys.dont_write_bytecode = True
import os
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import slp

SHAPES = ['renaming', 'plain multiplication', 'plain addition or subtraction', 'multiply-add',
          'two constants', 'more than two terms']


def shape(terms):
    consts = [Fr(c) for c, u in terms if abs(Fr(c)) != 1]
    if len(terms) > 2:
        return 5, consts
    if len(terms) == 2:
        return (2 if not consts else 3 if len(consts) == 1 else 4), consts
    if consts:
        return 1, consts
    # one term with coefficient 1 is a renaming; with coefficient -1 it is a change of sign, counted as a multiplication
    return (0 if Fr(terms[0][0]) == 1 else 1), ([Fr(-1)] if Fr(terms[0][0]) != 1 else [])


def main():
    if len(sys.argv) != 1:
        sys.exit(__doc__)
    print('The shape of every line of every circuit file under tools/circuits/programs/.')
    print('  folder               files    lines  renamings  plain mult.  plain add/sub  multiply-adds  two constants  >2 terms   constants in two-term lines')
    total = [0] * 6
    nfiles = 0
    first_bad = None
    for sub in ['', 'generated', 'as_found']:
        d = os.path.join(HERE, 'programs', sub)
        n = [0] * 6
        seen = {}
        files = sorted(f for f in os.listdir(d) if f.endswith('.txt'))
        for f in files:
            prog = slp.parse_file(os.path.join(d, f))
            for name, terms in prog.lines:
                s, consts = shape(terms)
                n[s] += 1
                if len(terms) == 2:
                    for c in consts:
                        seen[c] = seen.get(c, 0) + 1
                if s >= 4 and first_bad is None:
                    first_bad = '%s, line %s: %s' % (os.path.join('programs', sub, f), name, SHAPES[s])
        nfiles += len(files)
        total = [a + b for a, b in zip(total, n)]
        print('  %-19s %6d %8d %10d %12d %14d %14d %14d %9d   %s' % (
            'programs/' + sub if sub else 'programs/', len(files), sum(n), n[0], n[1], n[2], n[3], n[4], n[5],
            ', '.join('%s (%d)' % (c, seen[c]) for c in sorted(seen)) or 'none'))
    print('  %-19s %6d %8d %10d %12d %14d %14d %14d %9d' % (
        'all', nfiles, sum(total), total[0], total[1], total[2], total[3], total[4], total[5]))
    print()
    if first_bad:
        print('FAILED: ' + first_bad)
        sys.exit(1)
    print('OK: %d circuit files, %d lines; no line has a constant on both terms and no line has more than two terms.  '
          'So every line is a renaming, a plain multiplication, a plain addition or subtraction, or one multiply-add.  '
          'A Python check of the shape of the lines, not a proof.' % (nfiles, sum(total)))


if __name__ == '__main__':
    main()
