#!/usr/bin/env python3
"""count_tables.py -- exact operation counts of five constructions of the Walsh-Hadamard transform, in the two
counts of this repository, at N = 8, 16, 32, 64, 128, 256, 512, 4,096 and 32,768 points.

    python3 -B tools/circuits/count_tables.py [--kmax-gen K] [--json PATH] [--repo PATH]

Standard library only.  It uses this folder's reader and counter (slp.py) and generator (gen.py).  For every size
up to 2^K (default K = 12, that is 4,096 points) it builds each circuit, counts it with slp.py's own counter,
checks it on two random integer vectors against the definition of the transform, and checks that the count equals
a closed formula.  Larger sizes are given by the formula alone, unless --kmax-gen is raised: K = 15 builds the
32,768-point circuits too (about 50 s and 1.5 GB of memory on an Apple M4; the default run takes about 5 s and
160 MB).  It writes nothing unless --json PATH is given (then the table, as JSON, to PATH).
The tables it prints are the "exact counts" tables of the top README.md.

THE TWO COUNTS (slp.py's header):
  doublings free     = count (G): a line a*u + b*v is one operation; a line with one term (a scaling) costs
                       nothing.  Every constant in these circuits is +-2^e, so this is the count with doublings
                       and halvings free: the number of adders in hardware.
  doublings charged  = count (O): every addition, subtraction and multiplication by a constant is one operation
                       (OpenAI's circuit model, the model of the Lean theorem).  Doublings, halvings and the final
                       multiplications by 2^j are each charged.

THE FIVE CONSTRUCTIONS (k = log2 N; the output is H x exactly in every case):
  textbook : k layers of N/2 butterflies.
  CFL 1994 : the 4-point circuit printed by Coppersmith, Feig and Linzer (1994, page 969), as this repository writes
             it (CFL4 in fpga/family/fam.py, read as text), along each pair of address bits, then one textbook
             layer when k is odd.  Their own figure is the doublings-free count.  The doublings-charged column
             counts each doubling of that same circuit as one operation: it is my reading of their circuit, a
             figure they did not give.
  AR 2023  : the 8-point step of Alman and Rao (arXiv:2211.06459v2, Algorithm 5, as fpga/rtl/circuits/8_ar2023.txt
             writes it) along each group of three address bits, then textbook layers for the k mod 3 bits left over,
             as their proof of Theorem 6.2 does.  The doublings-free column is counted on the built circuit (my
             count of their construction).  The doublings-charged column is their own total from the proof of
             their Theorem 6.2, (23/24) N k + (N/24)(k mod 3) + N - 1, which applies the input doublings once for the
             whole transform; the program checks that it equals the doublings-free count + (N/8)(k div 3) halvings
             + (N - 1) multiplications by powers of 2.
  5/6      : the construction of the Lean theorem: the 20-operation 8-point step (19 additions and subtractions and
             one halving) along each group of three bits, textbook layers for leftover bits, and N final
             multiplications by 2^(k div 3).  The Lean theorem covers N = 8^j only; "(Lean)" marks those sizes.
  3/4      : the family of gen.py, construction 1: (3/4) N k + N/4 doublings free.  Doublings charged:
             "rescaled" is gen.family(k, 'O', exact=True), halvings in place of doublings and then N final
             multiplications; "literal" is the doublings-free circuit itself with each doubling charged.
"""
import argparse
import json
import os
import random
import re
import sys
from fractions import Fraction as Fr

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REPO = os.path.normpath(os.path.join(HERE, '..', '..'))
SIZES_K = [3, 4, 5, 6, 7, 8, 9, 12, 15]


def load(repo):
    tc = os.path.join(repo, 'tools', 'circuits')
    sys.path.insert(0, tc)
    import slp
    import gen
    with open(os.path.join(tc, 'fpga', 'family', 'fam.py')) as f:
        cfl4 = re.search(r'CFL4 = """(.*?)"""', f.read(), re.S).group(1)
    with open(os.path.join(tc, 'fpga', 'rtl', 'circuits', '8_ar2023.txt')) as f:
        ar8 = f.read()
    return slp, gen, cfl4, ar8


# ---------------------------------------------------------------- closed formulas
def f_textbook(k):
    return k << k


def f_cfl_free(k):            # their two formulas, page 969
    N = 1 << k
    return 7 * N * k // 8 if k % 2 == 0 else 7 * N * k // 8 + N // 8


def f_cfl_charged(k):         # 10 per 4-point block per layer (4 additions/subtractions + 3 doublings + 3 additions)
    N = 1 << k
    return 10 * (N // 4) * (k // 2) + N * (k % 2)


def f_ar_free(k):             # 22 additions/subtractions per 8-point block per layer; textbook for k mod 3 bits
    N = 1 << k
    return 22 * (N // 8) * (k // 3) + N * (k % 3)


def f_ar_charged(k):          # their total, proof of Theorem 6.2
    N = 1 << k
    v = Fr(23, 24) * N * k + Fr(N, 24) * (k % 3) + N - 1
    assert v.denominator == 1
    return int(v)


def f_56_free(k):
    N = 1 << k
    return 19 * (N // 8) * (k // 3) + N * (k % 3)


def f_56_charged(k):          # N (k - m/2 + 1), m = k div 3
    N = 1 << k
    return 20 * (N // 8) * (k // 3) + N * (k % 3) + N


def f_34_free(k):
    return (3 * k + 1) * (1 << k) // 4


def f_34_charged(k):          # gen.py's header: (7/8)Nk + N/4 (k even), (7/8)Nk + 5N/8 (k odd), + N
    N = 1 << k
    return (7 * k * N + (2 * N if k % 2 == 0 else 5 * N)) // 8 + N


# ---------------------------------------------------------------- checks
def random_check(slp, lines, N, trials=2, seed=7):
    """Run the program on random integer vectors; compare with H x computed by butterflies."""
    prog = slp.Program(lines)
    assert prog.N == N
    rnd = random.Random(seed + N)
    for _ in range(trials):
        x = [rnd.randint(-10**9, 10**9) for _ in range(N)]
        val = {'x%d' % i: Fr(x[i]) for i in range(N)}
        for name, terms in lines:
            v = Fr(0)
            for c, u in terms:
                v += c * val[u]
            val[name] = v
        y = x[:]
        h = 1
        while h < N:
            for i in range(0, N, 2 * h):
                for j in range(i, i + h):
                    a, b = y[j], y[j + h]
                    y[j], y[j + h] = a + b, a - b
            h *= 2
        for j in range(N):
            if val['y%d' % j] != y[j]:
                raise AssertionError('output y%d differs from row %d of H x' % (j, j))
    return prog.counts()


def powers_of_two_only(lines):
    for _, terms in lines:
        for c, _u in terms:
            a = abs(c)
            if a.numerator & (a.numerator - 1) or a.denominator & (a.denominator - 1):
                return False
    return True


# ---------------------------------------------------------------- build
def build_all(slp, gen, cfl4, ar8, k):
    N = 1 << k
    U = gen.units()
    B2 = U['B2']
    C4 = gen.Template(slp.parse_text(cfl4).lines, 'CFL 1994, 4 points')
    A8 = gen.Template(slp.parse_text(ar8).lines, 'Alman-Rao 2023, 8 points')
    assert C4.factor == 1 and A8.factor == 1
    out = {}

    lines, _ = gen.layered(k, [B2] * k, True)
    out['textbook'] = (lines, random_check(slp, lines, N))

    lines, fac = gen.layered(k, [C4] * (k // 2) + ([B2] if k % 2 else []), True)
    out['cfl'] = (lines, random_check(slp, lines, N))

    lines, fac = gen.layered(k, [A8] * (k // 3) + [B2] * (k % 3), True)
    out['ar'] = (lines, random_check(slp, lines, N))

    lines, fac = gen.layered(k, [U['O8']] * (k // 3) + [B2] * (k % 3), True)
    out['56'] = (lines, random_check(slp, lines, N))

    lines, fac = gen.family(k, 'G')
    assert fac == 1
    out['34G'] = (lines, random_check(slp, lines, N))

    lines, fac = gen.family(k, 'O', exact=True)
    assert fac == 1
    out['34O'] = (lines, random_check(slp, lines, N))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=DEFAULT_REPO, help='the top folder of the repository (default: found from '
                    'this file)')
    ap.add_argument('--kmax-gen', type=int, default=12, help='build and check the circuits up to 2^K points '
                    '(default 12)')
    ap.add_argument('--json', default=None, help='also write the table as JSON to this path (default: nothing '
                    'is written)')
    args = ap.parse_args()
    slp, gen, cfl4, ar8 = load(args.repo)

    rows = []
    for k in SIZES_K:
        N = 1 << k
        r = dict(N=N, k=k,
                 textbook=f_textbook(k),
                 cfl_free=f_cfl_free(k), cfl_charged=f_cfl_charged(k),
                 ar_free=f_ar_free(k), ar_charged=f_ar_charged(k),
                 s56_free=f_56_free(k), s56_charged=f_56_charged(k),
                 s34_free=f_34_free(k), s34_charged=f_34_charged(k), s34_literal=None,
                 source='formula', lean_56=(k % 3 == 0))
        # the totals of Alman and Rao: doublings free + halvings + (N - 1)
        assert r['ar_charged'] == r['ar_free'] + (N // 8) * (k // 3) + N - 1
        if k <= args.kmax_gen:
            b = build_all(slp, gen, cfl4, ar8, k)
            got = dict(
                textbook=(b['textbook'][1]['G'], b['textbook'][1]['O']),
                cfl=(b['cfl'][1]['G'], b['cfl'][1]['O']),
                ar=(b['ar'][1]['G'], None),
                s56=(b['56'][1]['G'], b['56'][1]['O']),
                s34=(b['34G'][1]['G'], b['34O'][1]['O']),
            )
            assert got['textbook'] == (r['textbook'], r['textbook']), (k, got['textbook'])
            assert got['cfl'] == (r['cfl_free'], r['cfl_charged']), (k, got['cfl'])
            assert got['ar'][0] == r['ar_free'], (k, got['ar'])
            assert got['s56'] == (r['s56_free'], r['s56_charged']), (k, got['s56'])
            assert got['s34'] == (r['s34_free'], r['s34_charged']), (k, got['s34'])
            r['s34_literal'] = b['34G'][1]['O']
            # every constant is +-2^e, so (G) = "doublings free"
            for key in b:
                assert powers_of_two_only(b[key][0]), key
            # the (O) circuits of 5/6 and of the rescaled family are strict (u+v, u-v, c*u only)
            assert b['56'][1]['strict'] and b['34O'][1]['strict']
            r['source'] = 'built, counted by slp.py, checked on 2 random integer vectors; equals the formula'
        rows.append(r)

    def n(v):
        return '' if v is None else '{:,}'.format(v)

    print('DOUBLINGS FREE (count (G); adders in hardware)')
    print('| N | textbook | CFL 1994 | Alman-Rao 2023 | 5/6 circuit | 3/4 family |')
    print('|---:|---:|---:|---:|---:|---:|')
    for r in rows:
        print('| %s | %s | %s | %s | %s | %s |' % (n(r['N']), n(r['textbook']), n(r['cfl_free']),
              n(r['ar_free']), n(r['s56_free']), n(r['s34_free'])))
    print()
    print('DOUBLINGS CHARGED (count (O); OpenAI circuit model)')
    print('| N | textbook | CFL 1994 | Alman-Rao 2023 | 5/6 circuit | 3/4 family, rescaled | 3/4 family, literal |')
    print('|---:|---:|---:|---:|---:|---:|---:|')
    for r in rows:
        print('| %s | %s | %s | %s | %s | %s | %s |' % (n(r['N']), n(r['textbook']), n(r['cfl_charged']),
              n(r['ar_charged']), n(r['s56_charged']) + (' (Lean)' if r['lean_56'] else ''),
              n(r['s34_charged']), n(r['s34_literal'])))
    print()
    for r in rows:
        print('N = %6d: %s' % (r['N'], r['source']))
    if args.json:
        with open(args.json, 'w') as f:
            json.dump(rows, f, indent=1)
        print('written: %s' % args.json)
    print('OK: every built circuit equals its formula.  A Python check, not a proof.')


if __name__ == '__main__':
    main()
