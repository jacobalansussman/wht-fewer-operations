#!/usr/bin/env python3
"""walkthrough.py -- the numbers and the check for each of the ten steps of UNDERSTAND.md.

    python3 walkthrough.py 5                      the numbers and the check of step 5
    python3 walkthrough.py all                    all ten steps
    python3 walkthrough.py 9 path/to/H8Half.lean  step 9, reading the 20 gates from that Lean file

Standard library only (Python 3.9 or later).  Everything printed is computed here, in exact whole
numbers and fractions, from the definition of the transform and from the three circuit listings
below.  Where a line says "expected", the program compares a number it computed with the number
written in the page.  This is a check by a Python program.  It is not a proof, and it does not run
Lean.
"""
import os
import random
import re
import sys
from fractions import Fraction as Fr

# ----------------------------------------------------------------------------------------------
# The transform, from its definition.
# ----------------------------------------------------------------------------------------------

def sign(j, c):
    """Entry of H in row j, column c: +1 if j and c have an even number of 1-bits in common."""
    return -1 if bin(j & c).count('1') % 2 else 1


def transform(x):
    """H x by the definition: N*N multiplications by +1 or -1.  Slow and obviously right."""
    n = len(x)
    return [sum(sign(j, c) * x[c] for c in range(n)) for j in range(n)]


# ----------------------------------------------------------------------------------------------
# The three circuits of the page.  One line is one value.
# ----------------------------------------------------------------------------------------------

C4 = """
p  = x0 + x1
q  = x2 - x3
h  = p + q
y0 = h + 2*x3
y1 = h - 2*x1
y2 = h - 2*x2
y3 = -h + 2*x0
"""

C8_19 = """
g1  = x0 + x7
g2  = x1 + x6
g3  = x2 - x5
g4  = x3 - x4
g5  = g1 - g2
g6  = g3 + g4
g7  = g5 - g6
g8  = g7 - 2*x7
g9  = g7 - 2*x5
g10 = g8 + 2*x6
g11 = g9 - 2*x4
y7  = g10 + 2*g4
y3  = g9 + 2*x3
y5  = -y3 + 2*g5
y1  = g10 + 2*g3
y6  = g11 + 2*g2
y2  = g8 + 2*x1
y4  = y2 + 2*g6
y0  = -g11 + 2*g1
"""

C8_20 = """
g1 = x0 + x7
g2 = x1 + x6
g3 = x2 - x5
g4 = x3 - x4
g5 = g1 - g2
g6 = g3 + g4
g7 = g5 - g6
m8 = 1/2*g7
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

TERM = re.compile(r'^(-)?\s*(?:(\d+(?:/\d+)?)\s*\*\s*)?([A-Za-z]\w*)$')
TWO = re.compile(r'^(.*?\S)\s+([+-])\s+(.*)$')


def parse(text):
    """A listing -> [(name, [(constant, name), ...])], one or two terms per line."""
    prog = []
    for raw in text.splitlines():
        line = raw.split('#')[0].strip()
        if not line:
            continue
        name, rhs = [s.strip() for s in line.split('=', 1)]
        m = TWO.match(rhs)
        parts = [(m.group(1), '+'), (m.group(3), m.group(2))] if m else [(rhs, '+')]
        terms = []
        for txt, op in parts:
            t = TERM.match(txt.strip())
            if not t:
                raise ValueError('cannot read: ' + raw)
            c = Fr(t.group(2)) if t.group(2) else Fr(1)
            if t.group(1):
                c = -c
            if op == '-':
                c = -c
            terms.append((c, t.group(3)))
        prog.append((name, terms))
    return prog


def run(prog, x):
    """Run a listing on the numbers x0, x1, ... ; returns every named value."""
    v = {'x%d' % i: xi for i, xi in enumerate(x)}
    for name, terms in prog:
        v[name] = sum(c * v[u] for c, u in terms)
    return v


def as_rows(prog, n):
    """Every value of a listing written in x0..x(n-1): run it on all n unit inputs at once."""
    units = [[Fr(1) if i == c else Fr(0) for c in range(n)] for i in range(n)]
    v = {'x%d' % i: units[i] for i in range(n)}
    for name, terms in prog:
        v[name] = [sum(c * v[u][i] for c, u in terms) for i in range(n)]
    return v


def cost_g(terms):
    """Count (G): one a*u + b*v is one operation; a line with one term is free."""
    return 1 if len(terms) == 2 else 0


def cost_o(terms):
    """Count (O): every addition, subtraction and multiplication by a constant costs one."""
    if len(terms) == 1:
        return 0 if terms[0][0] == 1 else 1          # a renaming is free, c*u costs one
    a, b = terms[0][0], terms[1][0]
    return 1 + (abs(a) != 1) + (abs(b) != 1) + (1 if a == -1 and b == -1 else 0)


def counts(prog):
    return sum(cost_g(t) for _, t in prog), sum(cost_o(t) for _, t in prog)


def pattern(vec):
    """+ for +1, - for -1, a dot for 0; a factor in front when the entries are halves."""
    f = Fr(1)
    for cand in (Fr(1), Fr(1, 2)):
        if all(e in (0, cand, -cand) for e in vec):
            f = cand
            break
    else:
        return ' '.join(str(e) for e in vec)
    s = ' '.join('+' if e > 0 else '-' if e < 0 else '.' for e in vec)
    return s if f == 1 else s + '   times 1/2'


def show(terms):
    out = []
    for k, (c, u) in enumerate(terms):
        mag = abs(c)
        body = u if mag == 1 else '%s*%s' % (mag, u)
        if k == 0:
            out.append(('-' if c < 0 else '') + body)
        else:
            out.append(('- ' if c < 0 else '+ ') + body)
    return ' '.join(out)


# ----------------------------------------------------------------------------------------------
# Bookkeeping for the checks.
# ----------------------------------------------------------------------------------------------

FAILS = []


def check(label, ok):
    print(('  ok    ' if ok else '  FAIL  ') + label)
    if not ok:
        FAILS.append(label)
    return ok


def head(n, title):
    print('=' * 78)
    print('STEP %d.  %s' % (n, title))
    print('=' * 78)


def commas(n):
    return '{:,}'.format(n)


# ----------------------------------------------------------------------------------------------
# The textbook program and the layers of the 20-operation circuit.
# ----------------------------------------------------------------------------------------------

def textbook(x):
    """The butterfly.  Returns (H x, number of additions and subtractions made)."""
    x = list(x)
    n = len(x)
    ops = 0
    step = 1
    while step < n:
        for i in range(n):
            if not i & step:
                a, b = x[i], x[i + step]
                x[i], x[i + step] = a + b, a - b
                ops += 2
        step *= 2
    return x, ops


def compile8(prog):
    """The 20-line listing as a short list of (kind, wire, wire); wires 0..7 are the inputs."""
    wire = {'x%d' % i: i for i in range(8)}
    ops, outs = [], [None] * 8
    for name, terms in prog:
        if len(terms) == 1 and terms[0][0] == 1:                 # a renaming, free
            wire[name] = wire[terms[0][1]]
        elif len(terms) == 1 and terms[0][0] == Fr(1, 2):
            ops.append(('half', wire[terms[0][1]], 0))
            wire[name] = 7 + len(ops)
        else:
            (a, u), (b, w) = terms
            assert a == 1 and abs(b) == 1, 'not a plain addition or subtraction'
            ops.append(('add' if b == 1 else 'sub', wire[u], wire[w]))
            wire[name] = 7 + len(ops)
        if name[0] == 'y':
            outs[int(name[1:])] = wire[name]
    return ops, outs


def layers(x, j, ops8, outs8):
    """Exact H x on 8^j whole numbers: j layers of the 20-operation circuit, then one multiplication
    per output.  Returns (result, operations in the layers, multiplications at the end); every
    operation is counted when it is made.  Whole numbers only: the caller gives inputs that are
    multiples of 2^j, and the program stops if a halving is ever not exact."""
    x = list(x)
    n = len(x)
    made = 0
    for d in range(j):
        shift = 3 * d
        for base in range(n):
            if (base >> shift) & 7:
                continue
            idx = [base + (t << shift) for t in range(8)]
            w = [x[i] for i in idx]
            for kind, a, b in ops8:
                if kind == 'add':
                    w.append(w[a] + w[b])
                elif kind == 'sub':
                    w.append(w[a] - w[b])
                else:
                    if w[a] % 2:
                        raise ArithmeticError('a halving is not exact')
                    w.append(w[a] // 2)
                made += 1
            for t in range(8):
                x[idx[t]] = w[outs8[t]]
    scale = 2 ** j
    return [scale * v for v in x], made, n


def mine(j):
    """The bound of the Lean statement, with Lean's subtraction on whole numbers (0 - 1 = 0)."""
    return 20 * (j * 8 ** max(j - 1, 0)) + 8 ** j


def alman_rao(k):
    """The exact count in the proof of Theorem 6.2 of Alman and Rao, arXiv:2211.06459:
    additions, halvings, multiplications by a power of two."""
    n = 2 ** k
    add = Fr(22, 24) * n * k + Fr(n, 24) * (k % 3)
    half = Fr(1, 24) * n * k
    mul = n - 1
    return add, half, mul


def mine_any(k):
    """Layers on three address bits at a time, a textbook layer for each bit left over, and N
    multiplications at the end.  For k = 3m + r with m at least 1 this is N (k - m/2 + 1)."""
    n, m = 2 ** k, k // 3
    return n * k if m == 0 else 20 * m * n // 8 + (k % 3) * n + n


# ----------------------------------------------------------------------------------------------
# The ten steps.
# ----------------------------------------------------------------------------------------------

def step1():
    head(1, 'What the transform is, at 2 and 4 points')
    for n in (2, 4):
        print('H at %d points (row j, column c; + is +1, - is -1):' % n)
        for j in range(n):
            print('   row %d   %s' % (j, ' '.join('+' if sign(j, c) > 0 else '-' for c in range(n))))
    print('2 points: (5, 3)        ->', transform([5, 3]))
    print('4 points: (1, 2, 3, 4)  ->', transform([1, 2, 3, 4]))
    print('THE CHECK: the transform of (3, 1, 4, 1).')
    y = transform([3, 1, 4, 1])
    print('   computed:', y)
    check('expected (9, 5, -1, -1)', y == [9, 5, -1, -1])


def step2():
    head(2, 'The textbook program and why it costs N log2 N')
    y, ops = textbook([3, 1, 4, 1])
    print('The butterfly on (3, 1, 4, 1): after layer 1 (4, 2, 5, 3), after layer 2', y, '; operations:', ops)
    check('the butterfly gives the transform of step 1', y == transform([3, 1, 4, 1]))
    rng = random.Random(2)
    print('   points  layers  operations made   N log2 N')
    good = True
    for k in (1, 2, 3, 6, 9, 12):
        n = 2 ** k
        x = [rng.randint(-9, 9) for _ in range(n)]
        y, ops = textbook(x)
        if n <= 512:
            good = good and y == transform(x)
        good = good and ops == n * k
        print('   %6s  %6d  %15s  %9s' % (commas(n), k, commas(ops), commas(n * k)))
    check('operations made = N log2 N at each size; result equal to the definition up to 512 points', good)
    print('THE CHECK: the textbook count at 512 points.')
    check('expected 512 * 9 = 4,608', textbook([0] * 512)[1] == 4608)


def step3():
    head(3, 'The two ways of counting')
    print('   line                    count (G)   count (O)')
    lines = ['a = u + v', 'b = u - v', 'c = u + 2*v', 'd = -u + 2*v', 'e = 1/2*u', 'f = 3*u - 5*v']
    got = {}
    for ln in lines:
        (name, terms), = parse(ln)
        got[name] = (cost_g(terms), cost_o(terms))
        print('   %-22s  %9d   %9d' % (ln, cost_g(terms), cost_o(terms)))
    y, ops = textbook([1, 2, 3, 4, 5, 6, 7, 8])
    print('The textbook program has only plain additions and subtractions, so it costs the same in both: %d at 8 points.' % ops)
    print('THE CHECK: the line  y3 = -h + 2*x0  of step 4.')
    (name, terms), = parse('y3 = -h + 2*x0')
    print('   computed: count (G)', cost_g(terms), ', count (O)', cost_o(terms))
    check('expected 1 in count (G) and 2 in count (O) (one doubling, one subtraction)',
          (cost_g(terms), cost_o(terms)) == (1, 2))


def step4():
    head(4, 'The known 4-point circuit with 7 operations')
    prog = parse(C4)
    rows = as_rows(prog, 4)
    for name, terms in prog:
        print('   %-3s = %-12s   %s' % (name, show(terms), pattern(rows[name])))
    ok = all(rows['y%d' % j] == [sign(j, c) for c in range(4)] for j in range(4))
    check('y0..y3 are rows 0..3 of H (all four inputs, exactly)', ok)
    g, o = counts(prog)
    print('   count (G): %d    count (O): %d    textbook: 8' % (g, o))
    check('expected 7 in count (G), and 11 in count (O) (7 additions or subtractions and 4 doublings)',
          (g, o) == (7, 11))
    print('THE CHECK: run it on (3, 1, 4, 1).')
    v = run(prog, [3, 1, 4, 1])
    print('   p = %s, q = %s, h = %s, outputs (%s, %s, %s, %s)' % (v['p'], v['q'], v['h'], v['y0'], v['y1'], v['y2'], v['y3']))
    check('expected p = 4, q = 3, h = 7 and the outputs (9, 5, -1, -1) of step 1',
          [v['p'], v['q'], v['h'], v['y0'], v['y1'], v['y2'], v['y3']] == [4, 3, 7, 9, 5, -1, -1])


def step5():
    head(5, 'The 8-point circuit with 19 operations: the centre')
    prog = parse(C8_19)
    rows = as_rows(prog, 8)
    for name, terms in prog:
        note = '    <- the centre' if name == 'g7' else ''
        print('   %-3s = %-14s  %s%s' % (name, show(terms), pattern(rows[name]), note))
    ok = all(rows['y%d' % j] == [sign(j, c) for c in range(8)] for j in range(8))
    check('y0..y7 are rows 0..7 of H (all eight inputs, exactly)', ok)
    g, o = counts(prog)
    check('expected 19 lines, each one operation of count (G); the textbook has 24', (g, len(prog)) == (19, 19))
    centre = rows['g7']
    print('Each row of H against the centre:')
    print('   row   differs from the centre at   so the row is')
    fine = True
    for j in range(8):
        row = [sign(j, c) for c in range(8)]
        diff = [c for c in range(8) if row[c] != centre[c]]
        same = [c for c in range(8) if row[c] == centre[c]]
        if len(diff) <= 4:
            rebuilt = [centre[c] - 2 * centre[c] * (c in diff) for c in range(8)]
            how = 'centre - 2*(the centre at ' + ', '.join('x%d' % c for c in diff) + ')'
        else:
            rebuilt = [-centre[c] + 2 * centre[c] * (c in same) for c in range(8)]
            how = '-centre + 2*(the centre at ' + ', '.join('x%d' % c for c in same) + ')'
        fine = fine and rebuilt == row
        print('   %d     %-27s  %s' % (j, ', '.join('x%d' % c for c in diff), how))
    check('each row rebuilt from the centre in that way equals the row', fine)
    print('THE CHECK: y2 = g8 + 2*x1 and y3 = g9 + 2*x3, by hand from the centre.')
    c = centre
    y2 = [c[i] - 2 * (i == 7) + 2 * (i == 1) for i in range(8)]
    y3 = [c[i] - 2 * (i == 5) + 2 * (i == 3) for i in range(8)]
    print('   centre - 2*x7 + 2*x1 :', pattern(y2), '   row 2 of H:', pattern([sign(2, i) for i in range(8)]))
    print('   centre - 2*x5 + 2*x3 :', pattern(y3), '   row 3 of H:', pattern([sign(3, i) for i in range(8)]))
    check('expected + + - - + + - - and + - - + + - - +',
          pattern(y2) == '+ + - - + + - -' and pattern(y3) == '+ - - + + - - +'
          and y2 == [sign(2, i) for i in range(8)] and y3 == [sign(3, i) for i in range(8)])


def step6():
    head(6, 'From 19 to 20: one halving in place of twelve doublings')
    p19, p20 = parse(C8_19), parse(C8_20)
    g19, o19 = counts(p19)
    doubles = sum(1 for _, t in p19 for c, _ in t if abs(c) == 2)
    print('The 19 lines in count (O): %d additions or subtractions + %d doublings = %d.' % (g19, doubles, o19))
    check('expected 19 + 12 = 31', (g19, doubles, o19) == (19, 12, 31))
    rows = as_rows(p20, 8)
    for name, terms in p20:
        if name[0] == 'y':
            continue
        outs = [n2 for n2, t in p20 if n2[0] == 'y' and t[0][1] == name]
        note = '    <- the one halving' if name == 'm8' else ('    = ' + outs[0] if outs else '')
        print('   %-3s = %-10s  %s%s' % (name, show(terms), pattern(rows[name]), note))
    ok = all(rows['y%d' % j] == [Fr(sign(j, c), 2) for c in range(8)] for j in range(8))
    check('y0..y7 are rows 0..7 of H divided by 2 (all eight inputs, exactly)', ok)
    g, o = counts(p20)
    adds = sum(1 for _, t in p20 if len(t) == 2)
    muls = sum(1 for _, t in p20 if len(t) == 1 and t[0][0] != 1)
    plain = all(cost_o(t) <= 1 for _, t in p20)
    check('expected 19 additions or subtractions + 1 halving = 20 in count (O); no line needs more than one operation',
          (adds, muls, o) == (19, 1, 20) and plain)
    r19 = as_rows(p19, 8)
    pairs = [('g8', 'g9'), ('g9', 'g10'), ('g10', 'g11'), ('g11', 'g12'), ('y7', 'g13'), ('y3', 'g14'),
             ('y5', 'g15'), ('y1', 'g16'), ('y6', 'g17'), ('y2', 'g18'), ('y4', 'g19'), ('y0', 'g20')]
    check('each of the 12 lines after the halving holds exactly half of the matching line of the 19',
          all([e / 2 for e in r19[a]] == rows[b] for a, b in pairs))
    print('THE CHECK: run the 20 lines on x0 = 1, all other inputs 0.')
    v = run(p20, [Fr(1)] + [Fr(0)] * 7)
    print('   g7 =', v['g7'], ', m8 =', v['m8'], ', outputs:', ', '.join(str(v['y%d' % j]) for j in range(8)))
    check('expected every output 1/2', all(v['y%d' % j] == Fr(1, 2) for j in range(8)))


def step7():
    head(7, 'From 8 points to 8^j points: layers, then one multiplication per output')
    ops8, outs8 = compile8(parse(C8_20))
    check('the 20-line listing has 20 operations', len(ops8) == 20)
    rng = random.Random(7)
    print('    points   j   in the layers   at the end      total   20 j 8^(j-1) + 8^j   textbook   checked on')
    table = {}
    for j in (1, 2, 3, 4):
        n = 8 ** j
        one = 2 ** j                      # inputs are multiples of 2^j, so every halving stays whole
        if j <= 3:
            inputs = [{c: one} for c in range(n)]
            what = 'all %d unit inputs' % n
        else:
            inputs = [{c: one} for c in rng.sample(range(n), 24)]
            inputs += [{c: one * rng.randint(-99, 99) for c in rng.sample(range(n), 40)} for _ in range(4)]
            what = '24 unit inputs and 4 random inputs (a sample)'
        good, lay, end = True, None, None
        for sparse in inputs:
            x = [sparse.get(c, 0) for c in range(n)]
            y, lay, end = layers(x, j, ops8, outs8)
            want = [sum(sign(r, c) * v for c, v in sparse.items()) for r in range(n)]
            good = good and y == want
        table[n] = lay + end
        print('   %7s   %d   %13s   %10s   %8s   %18s   %8s   %s' % (
            commas(n), j, commas(lay), commas(end), commas(lay + end), commas(mine(j)), commas(n * 3 * j), what))
        check('%s points: the result is exactly H x, and the operations made equal the formula' % commas(n),
              good and lay + end == mine(j) and lay == 20 * j * 8 ** (j - 1))
    check('expected 28, 384, 4,352, 45,056 against the textbook 24, 384, 4,608, 49,152',
          [table[8], table[64], table[512], table[4096]] == [28, 384, 4352, 45056])
    print('   (5/6) N log2 N + N at the same sizes:', ', '.join(commas(int(Fr(5, 6) * 8 ** j * 3 * j + 8 ** j)) for j in (1, 2, 3, 4)))
    check('20 j 8^(j-1) + 8^j = (5/6) N log2 N + N for j = 1..12',
          all(mine(j) == Fr(5, 6) * 8 ** j * 3 * j + 8 ** j for j in range(1, 13)))
    print('THE CHECK: 512 points by hand: 20 * 3 * 64 + 512.')
    print('   computed: %d + %d = %d' % (20 * 3 * 64, 512, 20 * 3 * 64 + 512))
    check('expected 3,840 + 512 = 4,352, which is 256 below 4,608', 20 * 3 * 64 + 512 == 4352 and 4608 - 4352 == 256)


def step8():
    head(8, 'The best explicit count in print, like for like')
    print('Alman and Rao (arXiv:2211.06459), exact count in the proof of their Theorem 6.2, against mine;')
    print('both charge every addition, subtraction, halving and final multiplication.')
    print('    points  textbook | Alman and Rao: add/sub  halvings  mult.   total | mine: add/sub  halvings  mult.   total')
    tot = {}
    for j in (1, 2, 3, 4):
        k, n = 3 * j, 8 ** j
        a, h, m = alman_rao(k)
        ma, mh, mm = 19 * j * n // 8, j * n // 8, n
        tot[n] = (int(a + h + m), ma + mh + mm)
        print('   %7s  %8s | %21s  %8s  %6s  %6s | %12s  %8s  %6s  %6s' % (
            commas(n), commas(n * k), commas(int(a)), commas(int(h)), commas(m), commas(int(a + h + m)),
            commas(ma), commas(mh), commas(mm), commas(ma + mh + mm)))
        check('%s points: mine equals 20 j 8^(j-1) + 8^j, and the difference is (3/8) j N - 1 = %s' % (
            commas(n), commas(3 * j * n // 8 - 1)),
            ma + mh + mm == mine(j) and int(a + h + m) - mine(j) == 3 * j * n // 8 - 1)
    check('expected Alman and Rao 30, 431, 4,927, 51,199 and mine 28, 384, 4,352, 45,056',
          [tot[n] for n in (8, 64, 512, 4096)] == [(30, 28), (431, 384), (4927, 4352), (51199, 45056)])
    first_ar = next(k for k in range(1, 99) if sum(alman_rao(k)) < 2 ** k * k)
    first_bound = next(k for k in range(1, 99) if Fr(23, 24) * 2 ** k * k + Fr(13, 12) * 2 ** k < 2 ** k * k)
    first_mine = next(k for k in range(1, 99) if mine_any(k) < 2 ** k * k)
    print('First size below the textbook: their exact count at 2^%d = %s points; the bound of their Theorem 1.1,' % (first_ar, commas(2 ** first_ar)))
    print('(23/24) N log2 N + (13/12) N, at 2^%d; mine at 2^%d = %d points.' % (first_bound, first_mine, 2 ** first_mine))
    check('expected 2^24, 2^27 and 2^9', (first_ar, first_bound, first_mine) == (24, 27, 9))
    check('mine is below their exact count at every power of two from 8 points to 2^60',
          all(mine_any(k) < sum(alman_rao(k)) for k in range(3, 61)))
    print('THE CHECK: their formula at 512 points: (23/24) * 512 * 9 + 512 - 1.')
    val = Fr(23, 24) * 512 * 9 + 512 - 1
    print('   computed: 4,608 * 23/24 = %s, plus 511 = %s' % (commas(int(Fr(23, 24) * 4608)), commas(int(val))))
    check('expected 4,416 + 511 = 4,927', val == 4927)


LEAN_STATEMENT = """theorem OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit (j : N) :
    exists C : Circuit (2 ^ (3 * j)),
      C.Computes (hadamard (3 * j))
      and
      C.size <= 20 * (j * 8 ^ (j - 1)) + 8 ^ j"""


def find_lean(arg):
    if arg:
        return arg if os.path.isfile(arg) else None
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for d, subdirs, files in os.walk(root):
        subdirs[:] = [s for s in subdirs if s not in ('.git', '.lake', 'node_modules')]
        if 'H8Half.lean' in files:
            return os.path.join(d, 'H8Half.lean')
    return None


def read_lean_gates(path):
    """The 20 gates and the 8 outputs as data in H8Half.lean.  Wires 0..7 are the inputs, wire 8 is
    the constant 0 of the model, and gate t is wire 8 + t."""
    with open(path, encoding='utf-8') as f:
        text = f.read()
    gates = []
    for m in re.finditer(r'def p(\d+) : Program 8 \d+ := \.step p\d+ \(\.(add|sub|scale)(.*)\)\s*$', text, re.M):
        nums = [int(s) for s in re.findall(r'⟨(\d+), by decide⟩', m.group(3))]
        const = re.search(r'\(([^()]*?) : ℂ\)', m.group(3))
        gates.append((int(m.group(1)), m.group(2), nums, const.group(1).strip() if const else None))
    m = re.search(r'outputs := !\[(.*?)\]', text, re.S)
    outs = [int(s) for s in re.findall(r'⟨(\d+), by decide⟩', m.group(1))] if m else []
    return gates, outs


def step9(lean_path=None):
    head(9, 'What Lean checked')
    print('The statement (written here with "exists", "and", "<=" for the symbols of the Lean file):')
    for i, ln in enumerate(LEAN_STATEMENT.splitlines(), 1):
        print('   line %d   %s' % (i, ln.strip()))
    print('The bound of line 5, with Lean\'s subtraction on whole numbers (0 - 1 is 0):')
    print('   j   points   20 * (j * 8^(j-1)) + 8^j   (5/6) N log2 N + N   textbook')
    for j in range(5):
        n = 8 ** j
        print('   %d   %6s   %24s   %19s   %8s' % (j, commas(n), commas(mine(j)),
              commas(int(Fr(5, 6) * n * 3 * j + n)), commas(n * 3 * j)))
    check('the bound is 1, 28, 384, 4,352, 45,056 for j = 0..4', [mine(j) for j in range(5)] == [1, 28, 384, 4352, 45056])
    path = find_lean(lean_path)
    if path is None:
        print('H8Half.lean was not found' + (' at ' + lean_path if lean_path else ' under the folder above docs/') +
              '; give its path as a second argument to read the 20 gates from it.')
        if lean_path:
            check('the file given on the command line exists', False)
    else:
        print('The 20 gates as data in', path)
        gates, outs = read_lean_gates(path)
        ops8, outs8 = compile8(parse(C8_20))
        same = len(gates) == 20 and len(outs) == 8
        w = [[Fr(1) if i == c else Fr(0) for c in range(8)] for i in range(8)] + [[Fr(0)] * 8]
        for t, (num, kind, nums, const) in enumerate(gates):
            if kind == 'scale':
                same = same and const.replace(' ', '') == '1/2' and t < 20 and ops8[t] == ('half', nums[0] - (nums[0] > 8), 0)
                w.append([e / 2 for e in w[nums[0]]])
            else:
                a, b = nums
                same = same and t < 20 and ops8[t] == (kind, a - (a > 8), b - (b > 8))
                w.append([p + q if kind == 'add' else p - q for p, q in zip(w[a], w[b])])
        kinds = [g[1] for g in gates]
        print('   gates read: %d (%d add, %d sub, %d scale); outputs: wires %s' % (
            len(gates), kinds.count('add'), kinds.count('sub'), kinds.count('scale'), outs))
        check('the Lean file holds 20 gates, the same operations in the same order as the 20 lines of step 6', same)
        ok = len(outs) == 8 and all(w[outs[j]] == [Fr(sign(j, c), 2) for c in range(8)] for j in range(8))
        check('run here in Python, output j of those gates is row j of H divided by 2', ok)
        with open(path, encoding='utf-8') as f:
            body = f.read()
        check('the file has no "sorry" (the word Lean uses for a missing proof) and no "axiom"',
              not re.search(r'\bsorry\b', body) and not re.search(r'^\s*axiom\b', body, re.M))
    print('This program does not run Lean.  That Lean accepted the proof is a fact about a build, not about this page.')
    print('THE CHECK: line 5 at j = 3.')
    print('   computed: 20 * (3 * 8^2) + 8^3 =', commas(mine(3)))
    check('expected 20 * 192 + 512 = 4,352, the number in the Lean theorem hadamard_512_circuit', mine(3) == 4352)


def step10():
    head(10, 'What this is not')
    print('My count divided by the textbook count, N = 8^j.  It is 5/6 + 1/log2 N: it falls towards 5/6 and stops there.')
    print('        j   log2 N   mine / textbook')
    vals = {}
    for j in (1, 2, 3, 4, 10, 100, 1000):
        r = Fr(mine(j), 8 ** j * 3 * j)
        vals[j] = r
        print('   %6d   %6d   %.4f' % (j, 3 * j, float(r)))
    check('the ratio equals 5/6 + 1/(3j) at each of these sizes and is above 5/6',
          all(r == Fr(5, 6) + Fr(1, 3 * j) and r > Fr(5, 6) for j, r in vals.items()))
    print('A better exponent would make this ratio fall to 0.  Here it cannot go below 5/6 = %.4f.' % (5 / 6))
    print('The same for the published count (23/24) N log2 N + N - 1: it stops at 23/24 = %.4f.' % (23 / 24))
    print('THE CHECK: the ratio at 8^10 points (log2 N = 30).')
    print('   computed: 5/6 + 1/30 = %s = %.4f' % (Fr(5, 6) + Fr(1, 30), float(Fr(5, 6) + Fr(1, 30))))
    check('expected 13/15 = 0.8667', vals[10] == Fr(13, 15))


STEPS = {1: step1, 2: step2, 3: step3, 4: step4, 5: step5, 6: step6, 7: step7, 8: step8, 9: step9, 10: step10}


def main(argv):
    if len(argv) < 2 or argv[1] not in ['all'] + [str(n) for n in STEPS]:
        print(__doc__)
        return 2
    todo = list(STEPS) if argv[1] == 'all' else [int(argv[1])]
    extra = argv[2] if len(argv) > 2 else None
    for n in todo:
        before = len(FAILS)
        if n == 9:
            step9(extra)
        else:
            STEPS[n]()
        print('STEP %d: %s' % (n, 'every check passed.' if len(FAILS) == before else 'A CHECK FAILED.'))
        print()
    if FAILS:
        print('FAILED: %d check(s): %s' % (len(FAILS), '; '.join(FAILS)))
        return 1
    if argv[1] == 'all':
        print('OK: all ten steps, every check passed.  A Python check, not a proof.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
