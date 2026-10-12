#!/usr/bin/env python3
"""tables.py -- regenerate every program, check every one exactly, print the tables.
    python3 -B tables.py            (standard library only)
run.py calls this program; run it alone only if you want its files in programs/generated/.
Programs up to 512 points are written to the folder named by the environment
variable CIRCUITS_OUT (default programs/generated/); larger ones (to 4,096
points) are generated, checked from their text, and not kept.  Add the word
"keep" to write those too.  KMAX_RUN=14 replays up to 16,384 points (several
GB of memory).  Counts and format: see slp.py.  Constructions: see gen.py."""
import os, sys, time
from fractions import Fraction as Fr
import slp, gen

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('CIRCUITS_OUT') or os.path.join(HERE, 'programs', 'generated')   # run.py sets CIRCUITS_OUT to its working folder
KEEP = 'keep' in sys.argv
KMAX_RUN = int(os.environ.get('KMAX_RUN', '12'))   # largest size generated and replayed: default 2^12 = 4,096 points
KMAX_TAB = 14
T0 = time.time()
os.makedirs(OUT, exist_ok=True)


def say(s=''):
    print(s); sys.stdout.flush()


def check(lines, fname, header, want_factor, want=None, labelled=True):
    """Write the text, read it back with the reader of slp.py, check, compare the count."""
    txt = gen.text(lines, header)
    prog = slp.parse_text(txt)
    r = slp.verify(prog, labelled=labelled)
    assert r['factors'] == [want_factor], (fname, r['factors'])
    if want:
        for key, v in want.items():
            assert r[key] == v, (fname, key, r[key], v)
    if prog.N <= 512 or KEEP:
        with open(os.path.join(OUT, fname), 'w') as f:
            f.write(txt)
    return r



# ---------------------------------------------------------------- 0. the checker tested on wrong programs
def verdict(prog, packed):
    try:
        return tuple(prog.packed_check() if packed else prog.dense_check())
    except AssertionError:
        return None


def mutants(prog):
    names = ['x0']
    for li, (name, terms) in enumerate(prog.lines):
        for ti, (c, u) in enumerate(terms):
            for new in ((-c, u), (2 * c, u), (c / 2, u), (c, names[-1]), (c, 'x0')):
                if new != (c, u):
                    lines = [(n, list(t)) for n, t in prog.lines]
                    lines[li][1][ti] = new
                    yield lines
        names.append(name)


say('PART 0.  The checker tried on wrong programs.  Every line of five small programs is spoiled in up to ten ways')
say('(a sign, a factor 2 or 1/2, a wrong operand); the packed check must give the same verdict as the dense check.')
AF = os.path.join(HERE, 'programs', 'as_found')
tot = bad = same = 0
for fn in ('h8_19gates.txt', 'h8_21gates.txt', 'slp_8.txt', 'oslp_16.txt', 'slp_16.txt'):
    base = slp.parse_file(os.path.join(AF, fn))
    good = verdict(base, True)
    assert good is not None and good == verdict(base, False)
    for lines in mutants(base):
        try:
            p = slp.Program(lines, base.outs)
        except ValueError:
            continue
        a, b = verdict(p, True), verdict(p, False)
        assert a == b, (fn, 'the two checks disagree on a spoiled program')
        tot += 1
        full = a is not None and sorted(j for _, j, _ in a) == list(range(p.N)) and len(set(f for _, _, f in a)) == 1
        if full:
            same += 1
        else:
            bad += 1
say('  %d spoiled programs: the two checks agree on all; %d rejected, %d still compute a multiple of H (a change that cancels).' % (tot, bad, same))
say()

# ---------------------------------------------------------------- 1. files as found
say('PART 1.  The programs as the searches left them (programs/as_found/, copied unchanged).')
say('  file                N    (G)  (O)  (O\')  add  sub  mul  neg  strict  outputs               checks')
NEG = 0
for fn in sorted(os.listdir(AF)):
    p = slp.parse_file(os.path.join(AF, fn))
    r = slp.verify(p)
    NEG += r['neg']
    say('  %-18s %4d %5d %4d %4d %4d %4d %4d %4d  %-6s  %-20s  %s' % (
        fn, r['N'], r['G'], r['O'], r['OAR'], r['add'], r['sub'], r['mul'], r['neg'], r['strict'],
        '(%s) * rows of H' % slp.fmt_fac(r['factors']), '; '.join(r['how'])))
say('  Every file: each of the N rows of H appears exactly once among the outputs, all with the one factor shown.')
say('  (G) = lines with two terms.  (O) = additions + subtractions + multiplications + negations, line by line.')
say('  (O\') = the same with a multiplication by -1 free (Alman and Rao).  Negations in these files: %d%s' % (NEG, ', so (O) = (O\') throughout.' if NEG == 0 else '.'))
say()

# ---------------------------------------------------------------- 2. units and families
U = gen.units()
say('PART 2.  The units (each checked on all unit vectors when built).')
for key in ('B2', 'G4', 'G8', 'O4', 'O8'):
    t = U[key]
    say('  %-3s %-55s (G)=%2d (O)=%2d strict=%s factor %s' % (key, t.name, t.counts['G'], t.counts['O'], t.counts['strict'], t.factor))
check(U['O8'].lines, 'O_unit8_20ops_factor_half.txt', 'count (O), 8 points, 20 operations, output yJ = (1/2) * row J of H', Fr(1, 2), dict(O=20, OAR=20, strict=True))
check(U['G8'].lines, 'G_unit8_19gates.txt', 'count (G), 8 points, 19 gates, output yJ = row J of H', Fr(1), dict(G=19))
say()


def famG(k):
    return (3 * k + 1) * (1 << k) // 4


def famO(k):       # outputs H x / 2^floor(k/2)
    N = 1 << k
    return (7 * k * N + 2 * N) // 8 if k % 2 == 0 else (7 * k * N + 5 * N) // 8


say('PART 3.  The family (gen.py, construction 1), generated and replayed for k = 2 .. %d.' % KMAX_RUN)
say('  k      N   (G) gates  formula (3/4)Nk+N/4 |  (O) ops  formula   factor of outputs | (O) exact H x = previous + N')
FAMT = {}
for k in range(2, KMAX_RUN + 1):
    N = 1 << k
    lg, _ = gen.family(k, 'G')
    rg = check(lg, 'G_family_%d.txt' % N, 'count (G), %d points, %d gates, construction 1 of gen.py; output yJ = row J of H' % (N, famG(k)), Fr(1), dict(G=famG(k)))
    lo, fac = gen.family(k, 'O')
    assert fac == Fr(1, 1 << (k // 2))
    ro = check(lo, 'O_family_%d_factor.txt' % N, 'count (O), %d points, %d operations, construction 1 of gen.py; output yJ = (%s) * row J of H' % (N, famO(k), fac), fac, dict(O=famO(k), OAR=famO(k), G=famG(k), strict=True))
    lx, _ = gen.family(k, 'O', exact=True)
    rx = check(lx, 'O_family_%d_exact.txt' % N, 'count (O), %d points, %d operations, construction 1 of gen.py with a final scaling; output yJ = row J of H' % (N, famO(k) + N), Fr(1), dict(O=famO(k) + N, OAR=famO(k) + N, strict=True))
    say('  %2d %6d %10d %10d            | %8d %8d   %-17s | %8d' % (k, N, rg['G'], famG(k), ro['O'], famO(k), fac, rx['O']))
    if k <= 6:
        FAMT[k] = (lg, lo)
say('  All replayed: packed check (equivalent to all N unit vectors), dense check for N <= 64, 4 random vectors each.')
say('  (O) formula: (7/8)Nk + N/4 for even k, (7/8)Nk + (5/8)N for odd k.')
say()

# ---------------------------------------------------------------- 3. dynamic programme over layer plans
# cost per point of a unit = operations / points; the cost per point of a layered program is the sum.
unitsG = [('B2', 1, Fr(2, 2)), ('G4', 2, Fr(7, 4)), ('G8', 3, Fr(19, 8))] + \
         [('F%d' % j, j, Fr(famG(j), 1 << j)) for j in range(3, KMAX_TAB + 1)]
unitsO = [('B2', 1, Fr(2, 2), 0), ('O4', 2, Fr(8, 4), 1), ('O8', 3, Fr(20, 8), 1)] + \
         [('FO%d' % j, j, Fr(famO(j), 1 << j), 1) for j in range(2, KMAX_TAB + 1)]


def dpG(units):
    best = {0: (Fr(0), [])}
    for k in range(1, KMAX_TAB + 1):
        c = None
        for name, bits, r in units:
            if bits <= k:
                v = best[k - bits][0] + r
                if c is None or v < c[0]:
                    c = (v, best[k - bits][1] + [name])
        best[k] = c
    return best


def dpO(units):
    """state (k, z): z = 1 when the outputs carry a factor other than 1."""
    best = {(0, 0): (Fr(0), [])}
    for k in range(1, KMAX_TAB + 1):
        for z in (0, 1):
            c = None
            for name, bits, r, e in units:
                if bits > k:
                    continue
                for z0 in (0, 1):
                    if (k - bits, z0) in best and (z0 | e) == z:
                        v = best[(k - bits, z0)][0] + r
                        if c is None or v < c[0]:
                            c = (v, best[(k - bits, z0)][1] + [name])
            if c:
                best[(k, z)] = c
    return best


def describe(plan):
    out = []
    for name in sorted(set(plan), key=plan.index):
        n = plan.count(name)
        d = {'B2': 'textbook step', 'G4': '7-gate 4-point unit', 'G8': '19-gate 8-point unit',
             'O4': '8-operation 4-point unit', 'O8': '20-operation 8-point unit'}.get(name)
        if d is None:
            d = 'family on %d points' % (1 << int(name.lstrip('FO')))
        out.append(('%d x ' % n if n > 1 else '') + d)
    return ' + '.join(out)


def template(name):
    if name in U:
        return U[name]
    if name not in TCACHE:
        j = int(name.lstrip('FO'))
        TCACHE[name] = gen.Template(gen.family(j, 'O' if name.startswith('FO') else 'G')[0], name)
    return TCACHE[name]


TCACHE = {}
bG = dpG(unitsG)
bG19 = dpG(unitsG[:3])                       # layers of the small units only (no family)
bO = dpO(unitsO)

# ---------------------------------------------------------------- 4. layered programs replayed
say('PART 4.  Layered programs, generated and replayed (k <= %d).' % KMAX_RUN)
say('  (G), best layering of the 2-, 4- and 8-point units alone (no family):')
RUN_G19 = {}
for k in range(1, KMAX_RUN + 1):
    N = 1 << k
    v, plan = bG19[k]
    lines, _ = gen.layered(k, [template(n) for n in plan], False)
    r = check(lines, 'G_layers_%d.txt' % N, 'count (G), %d points, %d gates: %s; output yJ = row J of H' % (N, v * N, describe(plan)), Fr(1), dict(G=int(v * N)))
    RUN_G19[k] = r['G']
    say('    k=%2d N=%5d gates %6d   %s' % (k, N, r['G'], describe(plan)))
say('  (O), layers of the 20-operation 8-point unit, textbook steps for the bits left over:')
say('     k      N   common factor   operations   then exact H x (N more)   textbook')
RUN_O8 = {}
for k in range(3, KMAX_RUN + 1):
    N = 1 << k
    m, j = divmod(k, 3)
    plan = ['O8'] * m + ['B2'] * j
    cost = 20 * (N // 8) * m + N * j
    lf, fac = gen.layered(k, [template(n) for n in plan], False)
    assert fac == Fr(1, 1 << m)
    rf = check(lf, 'O_layers8_%d_factor.txt' % N, 'count (O), %d points, %d operations: %s; output yJ = (%s) * row J of H' % (N, cost, describe(plan), fac), fac, dict(O=cost, OAR=cost, strict=True))
    lx, _ = gen.layered(k, [template(n) for n in plan], True)
    rx = check(lx, 'O_layers8_%d_exact.txt' % N, 'count (O), %d points, %d operations: %s, then every output times %d; output yJ = row J of H' % (N, cost + N, describe(plan), 1 << m), Fr(1), dict(O=cost + N, OAR=cost + N, strict=True))
    RUN_O8[k] = (rf['O'], rx['O'])
    say('    %2d %6d   %-13s %10d   %10d                %8d' % (k, N, fac, rf['O'], rx['O'], k * N))
say('  (O), textbook, k = 1 .. %d:' % KMAX_RUN)
for k in range(1, KMAX_RUN + 1):
    N = 1 << k
    lines, _ = gen.layered(k, [U['B2']] * k, True)
    r = check(lines, 'O_textbook_%d.txt' % N, 'textbook, %d points, %d operations in either count; output yJ = row J of H' % (N, k * N), Fr(1), dict(O=k * N, G=k * N, strict=True))
say('    all replayed, k*N operations each, outputs exactly the rows of H.')
say('  (O), the family on 2^(k-1) points and one textbook layer, odd k (cheaper than the family itself at odd k):')
for k in range(3, KMAX_RUN + 1, 2):
    N = 1 << k
    lines, fac = gen.layered(k, [template('FO%d' % (k - 1)), U['B2']], False)
    want = 2 * famO(k - 1) + N
    r = check(lines, 'O_family_plus_step_%d_factor.txt' % N, 'count (O), %d points, %d operations; output yJ = (%s) * row J of H' % (N, want, fac), fac, dict(O=want, strict=True))
    say('    k=%2d N=%5d operations %6d = (7/8)Nk + (3/8)N   (the family itself: %d)   factor %s' % (k, N, r['O'], famO(k), fac))
say()

# ---------------------------------------------------------------- 5. the tables
def AR_stated(k):          # Theorem 1.1 as published: (23/24) N log2 N + (13/12) N, an upper bound
    N = 1 << k
    return Fr(23, 24) * N * k + Fr(13, 12) * N


def AR_fine(k):            # the exact count in the proof of their Theorem 6.2: (23/24)Nk + (N/24)(k mod 3) + N - 1
    N = 1 << k
    return Fr(23, 24) * N * k + Fr(N, 24) * (k % 3) + N - 1


say('TABLE (O).  Exact transform H x (every output with factor 1), count (O): additions, subtractions and')
say('multiplications by constants all charged.  "here" = the cheaper of the textbook and the best layered program')
say('found by the dynamic programme over all layerings of: textbook step, 4-point unit, 8-point unit, family on')
say('2^j points (any j), with N final multiplications when the factor is not 1.')
say('Alman and Rao (2023): "Thm 1.1" is the bound they state, (23/24) N k + (13/12) N; "Thm 6.2" is the exact count')
say('in the proof of their Theorem 6.2, (23/24) N k + (N/24)(k mod 3) + N - 1.')
say('   k       N  textbook  Alman-Rao  Alman-Rao     here  here/    replayed     how (here)')
say('                 N*k    Thm 1.1    Thm 6.2    exact  textbook')
OURS_O = {}
ROWS_O = []
for k in range(1, KMAX_TAB + 1):
    N = 1 << k
    tb = k * N
    vz, pz = bO[(k, 1)] if (k, 1) in bO else (None, None)
    v0, p0 = bO[(k, 0)]
    ex_layer = vz * N + N if vz is not None else None
    if ex_layer is not None and ex_layer < v0 * N:
        ours, how = int(ex_layer), describe(pz) + ', then N multiplications'
    elif ex_layer is not None and ex_layer == v0 * N:
        ours, how = int(v0 * N), 'textbook (tie with: ' + describe(pz) + ', then N multiplications)'
    else:
        ours, how = int(v0 * N), 'textbook'
    OURS_O[k] = ours
    rep = 'no (formula)'
    if k <= KMAX_RUN:
        if ours == tb:
            rep = 'yes'
        if k >= 3 and RUN_O8[k][1] == ours:
            rep = 'yes'
    cf = ''
    if vz is not None:
        ex = sum(0 if n == 'B2' else 1 if n in ('O4', 'O8') else int(n[2:]) // 2 for n in pz)
        cf = '%7d  %-7s %s' % (int(vz * N), '1/%d' % (1 << ex), describe(pz))
        if k >= 3:                       # the dynamic programme must agree with the closed form
            assert int(vz * N) == 20 * (N // 8) * (k // 3) + N * (k % 3), (k, pz)
            if k <= KMAX_RUN:
                assert RUN_O8[k][0] == int(vz * N)
    ROWS_O.append((k, how, cf))
    say('  %2d %7d %8d %10.1f %10.1f %8d  %6.4f  %-12s %s' % (
        k, N, tb, float(AR_stated(k)), float(AR_fine(k)), ours, ours / tb, rep, how))
firstO = min(k for k in OURS_O if OURS_O[k] < k * (1 << k))
say('  Below the textbook: from k = %d (%d points) on, at every k up to %d; equal to it below that.' % (firstO, 1 << firstO, KMAX_TAB))
assert all(OURS_O[k] < k * (1 << k) for k in range(firstO, KMAX_TAB + 1))
say('  Below Alman and Rao (both columns): at every k in the table: %s.' % all(OURS_O[k] < AR_fine(k) and OURS_O[k] < AR_stated(k) for k in OURS_O))
kk = 1
while AR_fine(kk) >= kk * (1 << kk):
    kk += 1
say('  Alman and Rao\'s exact count (proof of their Theorem 6.2) is first below the textbook at k = %d; the bound of their Theorem 1.1 at k = %d.' % (
    kk, min(k for k in range(1, 60) if AR_stated(k) < k * (1 << k))))
say('  The same sizes when one common factor on all outputs is allowed (count (O); cheapest layering):')
say('   k       N  textbook  operations  factor  how')
for k, how, cf in ROWS_O:
    if cf:
        say('  %2d %7d %8d    %s' % (k, 1 << k, k << k, cf))
say('  General k = 3m + j (j = 0, 1, 2), m >= 1: layers cost N*(k - m/2) with factor 2^-m, exact H x costs N*(k - m/2 + 1).')
say('  That is (5/6) N k + N when 3 divides k, (5/6) N k + (7/6) N when j = 1, (5/6) N k + (4/3) N when j = 2.')
say()

say('TABLE (G).  Exact transform H x, count (G): a gate is any a*u + b*v, scalings free.')
say('"7/8 published" = (7/8) N k for even k and (7/8) N k + N/8 for odd k: the two formulas of Coppersmith, Feig and Linzer 1994')
say('(page 969), who charge one for a multiply-add, +-a +- b*c (narrower than count (G)); a 4-point step with 7 additions is also')
say('in Reshef and Alrod 2002 and in Alman and Rao 2023.  The column is computed from the two formulas.')
say('   k       N  textbook  7/8 published  small units only  family (3/4)Nk+N/4         here  here/textbook  replayed      how (here)')
OURS_G = {}
for k in range(1, KMAX_TAB + 1):
    N = 1 << k
    tb = k * N
    pub = 7 * N * k // 8 if k % 2 == 0 else 7 * N * (k - 1) // 8 + N
    v, plan = bG[k]
    v19, p19 = bG19[k]
    fam = famG(k) if k >= 2 else 2
    ours = int(v * N)
    assert ours == min(fam, int(v19 * N))
    OURS_G[k] = ours
    how = describe(plan)
    if fam == int(v19 * N) and k > 2:
        how = 'family; tie with ' + describe(p19)
    elif fam == ours and k >= 2:
        how = 'family' if k > 2 else '7-gate 4-point unit (= family)'
    rep = 'yes' if k <= KMAX_RUN else 'no (formula)'
    say('  %2d %7d %8d %10d %14d %18d %16d   %6.4f       %-12s  %s' % (k, N, tb, pub, int(v19 * N), fam, ours, ours / tb, rep, how))
say('  The family is below the textbook at every k >= 2 and below the published 7/8 count at every k >= 3 (equal at k = 2).')
say('  Layers of the 19-gate unit alone: (19/24) N k when 3 divides k; below the family only at k = 3 (19 against 20), equal at k = 6.')
say()
say('TABLE (O), orthonormal.  H x / sqrt(N) for even k (for odd k, 1/sqrt(N) is not rational), count (O).')
say('"layers" = the cheapest layering with any common factor, then N multiplications to reach 1/sqrt(N).')
say('The textbook gives H x in N*k and needs N more multiplications for H x / sqrt(N).')
say('   k       N  textbook+N  family (7/8)Nk+N/4  layers+N     best  which')
for k in range(2, KMAX_TAB + 1, 2):
    N = 1 << k
    vz, pz = bO[(k, 1)]
    ex = sum(0 if n == 'B2' else 1 if n in ('O4', 'O8') else int(n[2:]) // 2 for n in pz)
    lay = int(vz * N) + (0 if 2 * ex == k else N)
    fam = famO(k)
    say('  %2d %7d %10d %14d %13d %8d  %s' % (k, N, k * N + N, fam, lay, min(fam, lay),
        'family' if fam < lay else 'tie' if fam == lay else 'layers of the 8-point unit, then N multiplications'))
say('  Beyond the table (formulas): the family stays cheaper up to k = 16 and at k = 20, ties at k = 18, 22, 26,')
say('  and layers of the 8-point unit are cheaper at k = 24 and from k = 28 on:')
for k in range(16, 34, 2):
    lay = Fr(k) - Fr(k // 3, 2) + 1
    fam = Fr(7 * k, 8) + Fr(1, 4)
    say('    k=%2d  family %s N   layers %s N' % (k, float(fam), float(lay)))
say()
say('ALL CHECKS PASSED.  %.0f seconds.' % (time.time() - T0))
