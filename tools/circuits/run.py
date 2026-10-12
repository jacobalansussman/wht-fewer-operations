#!/usr/bin/env python3
"""run.py -- replay every circuit of tools/circuits, print the counts and the tables, rebuild the Lean data file.

usage: python3 -B tools/circuits/run.py [--work DIR] [--kmax K]

Standard library only.  About one minute and 700 MB of memory with the default --kmax 12.

  1. The named circuits (programs/*.txt) and the 20-line program that the Lean file is written from
     (lean/h8_half_o20.txt) are read from their text and replayed exactly against the transform.  Both counts
     are printed: (G), scalings free, and (O), every operation charged.
  2. tables.py regenerates every program from the recursions of gen.py, replays each one, replays the files of
     programs/as_found/, and prints the tables for N = 2 to 16,384: the textbook, Alman and Rao's published
     formulas, and these circuits.  Sizes up to 2^kmax points are replayed; above that the table rows are
     formulas and say so.
  3. Every file of programs/generated/ is compared byte for byte with the file just regenerated, and each named
     circuit is compared, operation by operation, with the regenerated program it is a copy of.
  4. lean/slp2lean.py writes the Lean data file again from lean/h8_half_o20.txt, and the result is compared byte
     for byte with lean/Work/SmallWHT/H8Half.lean at the top of the repository.  (Two folders are called lean:
     tools/circuits/lean/ has the 20-line program and slp2lean.py; lean/ at the top is the Lean project.)

--work DIR   keep the regenerated files in DIR (default: a temporary folder, removed at the end).
--kmax K     replay sizes up to 2^K points, K from 9 to 14 (default 12; 14 needs more memory and took 9
             minutes on the Linux machine used; its output is expected-output-kmax14.txt).

The last line is "OK ..." with exit code 0, or "FAILED: ..." with the first difference and exit code 1.
What is printed (standard output) does not depend on the machine or on the day; times go to standard error.
All of this is a check by Python programs, not a proof.  What Lean checks is said in README.md."""
import sys
sys.dont_write_bytecode = True
import os, re, shutil, subprocess, tempfile, time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
TOP = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import slp

LEAN_FILE = os.path.join(TOP, 'lean', 'Work', 'SmallWHT', 'H8Half.lean')    # the Lean project is the folder lean/ at the top
LEAN_DIR = os.path.join(HERE, 'lean')            # slp2lean.py and h8_half_o20.txt
LEAN_ARGS = ['3', '1/2', 'WHT8Half']             # log2 of the number of points, the factor, the Lean namespace

# file, points, (G), (O), factor on every output, the regenerated program it must equal, what it is
NAMED = [
    ('h4_7gates.txt', 4, 7, 11, Fr(1), 'G_family_4.txt', 'the wiring of gen.py; 7 operations at 4 points are due to Coppersmith, Feig and Linzer 1994'),
    ('h8_19gates.txt', 8, 19, 31, Fr(1), 'G_unit8_19gates.txt', '19 gates'),
    ('h8_half_20ops.txt', 8, 19, 20, Fr(1, 2), 'O_unit8_20ops_factor_half.txt', '19 additions or subtractions, 1 halving'),
    ('h16_52gates.txt', 16, 52, 84, Fr(1), 'G_family_16.txt', 'the family (3/4) N log2 N + N/4 at N = 16'),
]
T0 = time.time()


def say(s=''):
    print(s)
    sys.stdout.flush()


def fail(msg):
    say('FAILED: ' + msg)
    sys.exit(1)


def note(msg):
    sys.stderr.write('[%.0f s] %s\n' % (time.time() - T0, msg))
    sys.stderr.flush()


def body(text):
    """the operations of a program text: comments and blanks removed"""
    out = []
    for raw in text.splitlines():
        s = re.sub(r'\s+', '', raw.split('#', 1)[0])
        if s:
            out.append(s)
    return out


def gates(prog):
    """the program with its names forgotten: every operation as a list of (coefficient, operand), an operand
    being an input number or the number of an earlier operation.  Renamings (name = other name) are followed."""
    ref = {}
    out = []
    for name, terms in prog.lines:
        if len(terms) == 1 and terms[0][0] == 1:
            u = terms[0][1]
            ref[name] = ref.get(u, ('x', int(u[1:])) if re.fullmatch(r'x\d+', u) else None)
            continue
        g = []
        for c, u in terms:
            g.append((c, ('x', int(u[1:])) if re.fullmatch(r'x\d+', u) else ref[u]))
        ref[name] = ('g', len(out))
        out.append(g)
    return out


def first_difference(a, b):
    """a, b: bytes.  One line that says where they first differ."""
    la, lb = a.split(b'\n'), b.split(b'\n')
    for i in range(max(len(la), len(lb))):
        x = la[i] if i < len(la) else None
        y = lb[i] if i < len(lb) else None
        if x != y:
            show = lambda z: '(no such line)' if z is None else repr(z.decode('utf-8', 'replace'))
            return 'line %d: regenerated %s, in the tree %s' % (i + 1, show(x), show(y))
    return 'no difference'


def main():
    a = sys.argv[1:]
    work, kmax, lean_file, lean_dir = None, 12, LEAN_FILE, LEAN_DIR
    i = 0
    while i < len(a):
        if a[i] == '--work' and i + 1 < len(a):
            work = os.path.abspath(a[i + 1]); i += 2
        elif a[i] == '--kmax' and i + 1 < len(a):
            kmax = int(a[i + 1]); i += 2
        elif a[i] == '--lean-file' and i + 1 < len(a):       # for testing outside the repository
            lean_file = os.path.abspath(a[i + 1]); i += 2
        elif a[i] == '--lean-dir' and i + 1 < len(a):        # for testing outside the repository
            lean_dir = os.path.abspath(a[i + 1]); i += 2
        else:
            sys.exit(__doc__)
    if not 9 <= kmax <= 14:
        sys.exit('--kmax must be between 9 and 14 (the files in programs/generated/ go up to 512 = 2^9 points)')
    temp = work is None
    if temp:
        work = tempfile.mkdtemp(prefix='circuits-')
    os.makedirs(work + '/generated', exist_ok=True)
    try:
        run(work, kmax, lean_file, lean_dir)
    finally:
        if temp:
            shutil.rmtree(work, ignore_errors=True)


def run(work, kmax, lean_file, lean_dir):
    say('Small circuits for the Walsh-Hadamard transform H x on N = 2^k points.')
    say('Count (G): a gate is any a*u + b*v; multiplying by a constant is free.')
    say('Count (O): every addition, every subtraction and every multiplication by a constant costs one.')
    say('Everything below is computed in exact integers and fractions by Python.  It is not a proof.')
    say()

    # ------------------------------------------------------------ 1. the named circuits
    say('STEP 1.  The named circuits, read from their text and replayed against the transform.')
    say('  file                        N  textbook   (G)   (O)   add  sub  mul  outputs                 checks')
    named = {}
    for fn, N, G, O, fac, twin, what in NAMED:
        path = os.path.join(HERE, 'programs', fn)
        try:
            p = slp.parse_file(path)
            r = slp.verify(p, labelled=True)
        except (OSError, ValueError, AssertionError) as e:
            fail('programs/%s: %s' % (fn, e))
        got = (r['N'], r['G'], r['O'], r['factors'])
        if got != (N, G, O, [fac]):
            fail('programs/%s: found N, (G), (O), factors = %s, expected %s' % (fn, got, (N, G, O, [fac])))
        named[fn] = p
        say('  %-24s %4d %9d %5d %5d %5d %4d %4d  %-22s  %s' % (
            fn, N, N * r['k'], r['G'], r['O'], r['add'], r['sub'], r['mul'],
            ('H x' if fac == 1 else '(%s) H x' % fac) + ', yJ = row J', '; '.join(r['how'])))
    src = os.path.join(lean_dir, 'h8_half_o20.txt')
    try:
        p20 = slp.parse_file(src)
        p20.outs = [name for name, _ in p20.lines if name.startswith('z')]
        r = slp.verify(p20)
        rows = p20.packed_check()
    except (OSError, ValueError, AssertionError) as e:
        fail('lean/h8_half_o20.txt: %s' % e)
    if (r['N'], r['G'], r['O'], r['strict'], r['factors']) != (8, 19, 20, True, [Fr(1, 2)]):
        fail('lean/h8_half_o20.txt: counts or factor are not 8 points, (G) 19, (O) 20, factor 1/2: %s' % r)
    for o, j, f in rows:
        if o != 'z%d' % j:
            fail('lean/h8_half_o20.txt: the wire %s is row %d' % (o, j))
    say('  %-24s %4d %9d %5d %5d %5d %4d %4d  %-22s  %s' % (
        'lean/h8_half_o20.txt', 8, 24, r['G'], r['O'], r['add'], r['sub'], r['mul'], '(1/2) H x, zJ = row J', '; '.join(r['how'])))
    if gates(p20) != gates(named['h8_half_20ops.txt']):
        fail('lean/h8_half_o20.txt and programs/h8_half_20ops.txt are not the same 20 operations')
    say('  lean/h8_half_o20.txt and programs/h8_half_20ops.txt: the same 20 operations in the same order, under other names.')
    say('  (G) = lines with two terms.  (O) = add + sub + mul.  "packed" is one exact run that is equivalent to all N unit')
    say('  vectors (slp.py says why); "dense" compares every entry with H.')
    say()
    note('step 1 done')

    # ------------------------------------------------------------ 2. regenerate everything, replay, tables
    say('STEP 2.  tables.py: every program regenerated from gen.py and replayed up to %d points; the tables.' % (1 << kmax))
    say()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', CIRCUITS_OUT=work + '/generated', KMAX_RUN=str(kmax))
    p = subprocess.Popen([sys.executable, '-B', os.path.join(HERE, 'tables.py')], cwd=HERE, env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    last = ''
    for line in p.stdout:
        line = line.rstrip('\n')
        if line.strip():
            last = line
        say(re.sub(r'^(ALL CHECKS PASSED\.).*$', r'\1', line))
    p.wait()
    if p.returncode != 0 or not last.startswith('ALL CHECKS PASSED.'):
        fail('tables.py ended with exit code %d; its last line: %s' % (p.returncode, last[:300]))
    say()
    note('step 2 done (%s)' % last)

    # ------------------------------------------------------------ 3. the files in the tree against the regenerated ones
    say('STEP 3.  The program files in this folder against the files just regenerated.')
    shipped = sorted(os.listdir(os.path.join(HERE, 'programs', 'generated')))
    for fn in shipped:
        new = os.path.join(work, 'generated', fn)
        if not os.path.exists(new):
            fail('programs/generated/%s: tables.py did not regenerate a file of this name' % fn)
        x, y = open(new, 'rb').read(), open(os.path.join(HERE, 'programs', 'generated', fn), 'rb').read()
        if x != y:
            fail('programs/generated/%s differs from the regenerated file: %s' % (fn, first_difference(x, y)))
    say('  programs/generated/: %d files, each byte for byte the regenerated file.' % len(shipped))
    for fn, N, G, O, fac, twin, what in NAMED:
        x = body(open(os.path.join(HERE, 'programs', fn)).read())
        y = body(open(os.path.join(work, 'generated', twin)).read())
        if x != y:
            d = next((i for i in range(min(len(x), len(y))) if x[i] != y[i]), min(len(x), len(y)))
            fail('programs/%s is not the regenerated %s: operation %d differs' % (fn, twin, d + 1))
        say('  programs/%-20s the same operations as the regenerated %s  (%s).' % (fn + ':', twin, what))
    say()

    # ------------------------------------------------------------ 4. the Lean data file
    say('STEP 4.  The Lean data file lean/Work/SmallWHT/H8Half.lean (top of the repository), written again from the 20-line program.')
    out = os.path.join(work, 'H8Half.lean')
    q = subprocess.run([sys.executable, '-B', os.path.join(lean_dir, 'slp2lean.py'), 'h8_half_o20.txt'] + LEAN_ARGS + [out],
                       cwd=lean_dir, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in q.stdout.splitlines():
        if line.startswith('CHECK'):
            say('  slp2lean.py: ' + line)
    if q.returncode != 0 or not os.path.exists(out):
        fail('lean/slp2lean.py ended with exit code %d: %s' % (q.returncode, q.stdout.strip()[-300:]))
    x = open(out, 'rb').read()
    if not os.path.exists(lean_file):
        fail('the Lean file %s is not in the tree' % os.path.relpath(lean_file, TOP))
    y = open(lean_file, 'rb').read()
    if x != y:
        fail('the regenerated Lean file differs from lean/Work/SmallWHT/H8Half.lean: ' + first_difference(x, y))
    say('  regenerated file: %d lines, %d bytes; byte for byte the file in the tree.' % (x.count(b'\n'), len(x)))
    say()
    note('done')
    say('OK: %d named circuits and the 20-line program replayed; every size up to %d points regenerated and replayed; '
        '%d program files and the Lean data file reproduced byte for byte.  A Python check, not a proof.'
        % (len(NAMED), 1 << kmax, len(shipped)))


if __name__ == '__main__':
    main()
