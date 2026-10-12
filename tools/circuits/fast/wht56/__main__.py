"""python3 -m wht56 ...   (run from the folder that contains the folder wht56)

  --selftest              run the tests (tests/test_wht56.py); under a minute
  --count K               the operation counts at 2^K points: formulas, and the operations
                          really performed by the pure-Python programs with the counter on
  --table [KMAX]          the counts table for 2 .. 2^KMAX points (default 12), by formula
  --bench [K ...]         time the pure-Python and the numpy versions (and say how to time C)
  --gen python|c|kernels  write straight-line code to standard output
        --size N              the number of points (python, c); default 8
        --count-model O|G     which units to use (default O)
        --norm exact|raw      default exact
"""
import argparse
import os
import sys
import time

from . import plans, codegen, reference


def cmd_count(k):
    n = 1 << k
    print('N = 2^%d = %d point%s.  Textbook: %d operations in either count.' % (k, n, '' if n == 1 else 's', k * n))
    print('Count (O): every addition, subtraction and multiplication by a constant costs one.')
    print('Count (G): one operation is any a*u + b*v; multiplying by a constant is free.')
    print()
    rows = [
        ('textbook', reference.textbook, {}),
        ("count (O), exact H x, cheapest mix of units", reference.wht, dict(norm='exact')),
        ("count (O), 8-point circuit in layers, exact H x", reference.wht,
         dict(norm='exact', plan=plans.layers_plan(k))),
        ("count (O), raw (H x times a power of 1/2)", reference.wht, dict(norm='raw')),
        ("count (O), H x / sqrt(N)", reference.wht, dict(norm='ortho')),
        ("count (G), cheapest mix of the 19-, 7- and 2-gate units", reference.wht, dict(count='G')),
        ("count (G), the family (3/4) N log2 N + N/4", reference.family, {}),
    ]
    print('%-56s %10s %10s   %s' % ('program', '(O) done', '(G) done', 'units'))
    for name, fn, kw in rows:
        if k > 16:
            print('%-56s %10s' % (name, '(too large to run here; see --table)'))
            continue
        t = reference.count(fn, n, **kw)
        if fn is reference.wht:
            p = kw.get('plan') or plans.best_plan(k, kw.get('count', 'O'), kw.get('norm', 'exact'))
            how = ' '.join(p)
        else:
            how = ''
        print('%-56s %10d %10d   %s' % (name, t.O, t.G, how))
    print()
    print('By formula at this size:')
    print('  textbook N log2 N                                   %d' % (k * n))
    print('  textbook and N multiplications (for H x / sqrt N)   %d' % (k * n + n))
    print('  count (O), layers of the 20-operation circuit       %d' % plans.formula_layers_O(k))
    if k % 3 == 0 and k:
        print('  count (O), 20 j 8^(j-1) + 8^j with j = %-2d            %d' % (k // 3, plans.formula_pow8(k // 3)))
    print('  count (O), Alman and Rao (2023), exact count         %s' % plans.alman_rao_exact(k))
    print('  count (G), family (3/4) N log2 N + N/4               %d' % plans.formula_family_G(k))
    print('  count (G), rate 7/8 of 1994 on pairs of bits         %d%s' % (
        plans.published_G(k), '   (their formula for an odd power of two: (7/8) N log2 N + N/8)' if k % 2 else ''))


def cmd_table(kmax):
    print('Operations for exact H x.  (G): a*u + b*v is one operation.  (O): everything is charged.')
    print('%8s %9s | %9s %9s %9s | %11s %9s %9s' % (
        'points', 'textbook', '(G) 1994', '(G)family', '(G)layers', '(O)AlmanRao', '(O)layers', '(O) best'))
    for r in plans.table(kmax):
        if r['k'] < 2:
            continue
        print('%8d %9d | %9d %9d %9d | %11s %9d %9d' % (
            r['N'], r['textbook'], r['G_published'], r['G_family'], r['G_layers'],
            r['O_alman_rao'], r['O_layers'], r['O_best']))
    print('(G) 1994: the formulas of Coppersmith, Feig and Linzer (page 969): (7/8) N log2 N when N is a power of four,')
    print('          and (7/8) N log2 N + N/8 at the other sizes, which is one textbook layer more.')


def _best(fn, make, runs):
    best = None
    for _ in range(runs):
        x = make()
        t0 = time.perf_counter()
        fn(x)
        t = time.perf_counter() - t0
        best = t if best is None or t < best else best
    return best


def cmd_bench(ks):
    import platform
    print('machine: %s %s; Python %s' % (platform.system(), platform.machine(), platform.python_version()))
    print('nanoseconds per point for one transform; best of several runs')
    print()
    print('PURE PYTHON (lists of floats; this is a reference, not a fast program)')
    import random
    rnd = random.Random(5)
    print('%-8s %14s %14s %14s' % ('points', 'textbook', 'wht (exact)', 'family'))
    for k in [k for k in ks if k <= 12] or [9]:
        n = 1 << k
        x = [rnd.uniform(-1, 1) for _ in range(n)]
        row = [_best(f, lambda: x, 5) * 1e9 / n
               for f in (reference.textbook, reference.wht, reference.family)]
        print('2^%-6d %14.1f %14.1f %14.1f' % (k, row[0], row[1], row[2]))
    print()
    try:
        import numpy as np
    except ImportError:
        print('NUMPY: not installed for this python; skipped')
    else:
        from . import fast
        print('NUMPY %s (float64, in place, the copy of the input not timed)' % np.__version__)
        cols = [('textbook2', 'exact'), ('textbook8', 'exact'), ('k8', 'raw'), ('k8', 'exact'),
                ('textbook8', 'ortho'), ('k8', 'ortho')]
        print('%-8s' % 'points' + ''.join(' %16s' % ('%s/%s' % c) for c in cols))
        g = np.random.default_rng(5)
        for k in ks:
            n = 1 << k
            src = g.standard_normal(n)
            runs = 30 if k <= 15 else (9 if k <= 18 else 5)
            best = [None] * len(cols)
            for _ in range(runs):                  # the variants take turns
                for ci, (m, nm) in enumerate(cols):
                    x = src.copy()
                    t0 = time.perf_counter()
                    fast.fwht(x, norm=nm, method=m, inplace=True)
                    t = time.perf_counter() - t0
                    if best[ci] is None or t < best[ci]:
                        best[ci] = t
            print('2^%-6d' % k + ''.join(' %16.2f' % (b * 1e9 / n) for b in best))
    print()
    print('C: sh %s [output directory [runs [k ...]]]' % os.path.join(os.path.dirname(__file__), 'c', 'build_and_bench.sh'))


def main(argv=None):
    ap = argparse.ArgumentParser(prog='python3 -m wht56', description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--count', type=int, metavar='K')
    ap.add_argument('--table', type=int, nargs='?', const=12, metavar='KMAX')
    ap.add_argument('--bench', type=int, nargs='*', metavar='K')
    ap.add_argument('--gen', choices=('python', 'c', 'kernels'))
    ap.add_argument('--size', type=int, default=8)
    ap.add_argument('--count-model', choices=('O', 'G'), default='O')
    ap.add_argument('--norm', choices=('exact', 'raw'), default='exact')
    a = ap.parse_args(argv)
    did = False
    if a.selftest:
        import unittest
        from .tests import test_wht56
        suite = unittest.defaultTestLoader.loadTestsFromModule(test_wht56)
        res = unittest.TextTestRunner(verbosity=2).run(suite)
        if not res.wasSuccessful():
            return 1
        did = True
    if a.count is not None:
        if a.count < 0:
            ap.error('K must be 0 or more')
        cmd_count(a.count)
        did = True
    if a.table is not None:
        cmd_table(a.table)
        did = True
    if a.bench is not None:
        cmd_bench(a.bench or [9, 12, 15, 18, 21])
        did = True
    if a.gen:
        if a.gen == 'kernels':
            sys.stdout.write(codegen.c_kernels_header())
        else:
            if a.size < 1 or a.size & (a.size - 1):
                ap.error('--size must be a power of two')
            k = a.size.bit_length() - 1
            f = codegen.python_source if a.gen == 'python' else codegen.c_source
            sys.stdout.write(f(k, a.count_model, a.norm))
        did = True
    if not did:
        ap.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
