"""Tests of wht56.  Plain unittest.  One command, from the folder that contains wht56:

    python3 -B -m wht56 --selftest          (or: python3 -B -m unittest wht56.tests.test_wht56 -v)

The numpy tests are skipped when numpy is not installed, the C tests when there is no C
compiler called cc (or $CC).  The numbers typed into TestCounts are the published ones: they
are copied from the tables of notes/explicit-circuits.md and from
tools/circuits/expected-output.txt, except the 64 for H x / sqrt(N) at 16 points, which is in
the text of the note and not in its tables.
"""
import hashlib
import os
import random
import shutil
import subprocess
import tempfile
import unittest
from fractions import Fraction

from wht56 import circuit, plans, codegen, reference as R

try:
    import numpy as np
except ImportError:                                   # pragma: no cover
    np = None

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
CC = os.environ.get('CC', 'cc')


def close(a, b, scale):
    return all(abs(p - q) <= 1e-9 * scale for p, q in zip(a, b)) and len(a) == len(b)


class TestCircuitFiles(unittest.TestCase):
    def test_files_are_the_copies(self):
        with open(os.path.join(circuit.CIRCUIT_DIR, 'SHA256SUMS')) as f:
            for line in f:
                digest, name = line.split()
                with open(os.path.join(circuit.CIRCUIT_DIR, name), 'rb') as g:
                    self.assertEqual(hashlib.sha256(g.read()).hexdigest(), digest, name)

    def test_units(self):
        # loading a unit already checks it on every unit input, exactly
        for key, want in circuit.expected_units().items():
            c = circuit.unit(key)
            self.assertEqual((c.bits, c.G, c.O, c.factor), want, key)

    def test_a_spoiled_circuit_is_refused(self):
        with open(os.path.join(circuit.CIRCUIT_DIR, 'h8_half_20ops.txt')) as f:
            text = f.read()
        bad = text.replace('g20 = g1 - g12', 'g20 = g1 + g12')
        self.assertNotEqual(bad, text)
        with self.assertRaises(AssertionError):
            circuit.Circuit(bad, 'spoiled')


class TestAgainstTheMatrix(unittest.TestCase):
    """Every program against the definition: the explicit matrix, up to 2^10 points."""

    def programs(self, k):
        yield 'textbook', R.textbook
        yield 'wht O exact', lambda x: R.wht(x)
        yield 'wht O layers', lambda x: R.wht(x, plan=plans.layers_plan(k))
        yield 'wht G', lambda x: R.wht(x, count='G')
        yield 'family', R.family

    def test_every_unit_vector_up_to_64(self):
        for k in range(0, 7):
            n = 1 << k
            H = circuit.hadamard_matrix(n)
            for name, f in self.programs(k):
                for i in range(n):
                    e = [0] * n
                    e[i] = 1
                    self.assertEqual(f(e), [H[j][i] for j in range(n)], (name, n, i))

    def test_random_integers_up_to_1024(self):
        rnd = random.Random(2026)
        for k in range(0, 11):
            n = 1 << k
            x = [rnd.randint(-10 ** 9, 10 ** 9) for _ in range(n)]
            want = R.matrix_times(x)
            for name, f in self.programs(k):
                self.assertEqual(f(x), want, (name, n))

    def test_length_1_and_2(self):
        for name, f in self.programs(0):
            self.assertEqual(f([7]), [7], name)
        for name, f in self.programs(1):
            self.assertEqual(f([7, 3]), [10, 4], name)
        self.assertEqual(R.wht([7, 3], norm='raw'), [10, 4])
        self.assertEqual(R.wht([Fraction(1, 3)], norm='ortho'), [Fraction(1, 3)])

    def test_bad_lengths(self):
        for f in (R.textbook, R.wht, R.family):
            for n in (0, 3, 6, 12, 1000):
                with self.assertRaises(ValueError):
                    f([1] * n)
        with self.assertRaises(ValueError):
            R.layers8([1] * 16)                       # a power of two, not a power of 8


class TestRandomInputs(unittest.TestCase):
    """Random integer, fraction, float and complex inputs up to 2^15 against the textbook."""

    def test_integers_every_size_to_2_15(self):
        rnd = random.Random(1)
        for k in range(0, 16):
            n = 1 << k
            x = [rnd.randint(-10 ** 6, 10 ** 6) for _ in range(n)]
            want = R.textbook(x)
            for got in (R.wht(x), R.wht(x, count='G'), R.family(x),
                        R.wht(x, plan=plans.layers_plan(k))):
                self.assertEqual(got, want, n)
                self.assertTrue(all(type(v) is int for v in got), n)

    def test_fractions(self):
        rnd = random.Random(2)
        for k in (3, 4, 5, 6, 9):
            n = 1 << k
            x = [Fraction(rnd.randint(-99, 99), rnd.randint(1, 9)) for _ in range(n)]
            want = R.textbook(x)
            self.assertEqual(R.wht(x), want)
            self.assertEqual(R.wht(x, plan=plans.layers_plan(k)), want)
            self.assertEqual(R.family(x), want)
            m = k // 3
            self.assertEqual(R.wht(x, norm='raw', plan=plans.layers_plan(k)), [v / 2 ** m for v in want])

    def test_floats_and_complex(self):
        rnd = random.Random(3)
        for k in (1, 2, 5, 9, 12, 15):
            n = 1 << k
            xf = [rnd.uniform(-1, 1) for _ in range(n)]
            xc = [complex(rnd.uniform(-1, 1), rnd.uniform(-1, 1)) for _ in range(n)]
            for x in (xf, xc):
                want = R.textbook(x)
                self.assertTrue(close(R.wht(x, plan=plans.layers_plan(k)), want, n), n)
                self.assertTrue(close(R.wht(x, count='G'), want, n), n)
                self.assertTrue(close(R.family(x), want, n), n)
                s = n ** 0.5
                self.assertTrue(close(R.wht(x, norm='ortho'), [v / s for v in want], n), n)

    def test_halved_form_on_integers_is_exact(self):
        x = list(range(-256, 256))
        half = R.layers8_half(x)
        self.assertEqual([8 * v for v in half], R.textbook(x))
        self.assertEqual(R.layers8(x), R.textbook(x))
        self.assertEqual(R.layers8_int(x), R.textbook(x))
        self.assertTrue(all(type(v) is int for v in R.layers8(x)))


class TestInverse(unittest.TestCase):
    def test_H_H_is_N(self):
        rnd = random.Random(4)
        for k in range(0, 13):
            n = 1 << k
            x = [rnd.randint(-999, 999) for _ in range(n)]
            nx = [n * v for v in x]
            self.assertEqual(R.wht(R.wht(x)), nx)
            self.assertEqual(R.family(R.family(x)), nx)
            self.assertEqual(R.wht(R.wht(x, count='G'), plan=plans.layers_plan(k)), nx)

    def test_ortho_twice_is_identity(self):
        x = [Fraction(i * i - 7, 3) for i in range(64)]
        self.assertEqual(R.wht(R.wht(x, norm='ortho'), norm='ortho'), x)


class TestCounts(unittest.TestCase):
    """The counter is on: these are the operations really performed."""

    def test_powers_of_8_count_O(self):
        # 20 j 8^(j-1) + 8^j: the count of the Lean theorem hadamard_pow8_circuit
        for j, want in ((1, 28), (2, 384), (3, 4352), (4, 45056), (5, 442368)):
            n = 8 ** j
            self.assertEqual(20 * j * 8 ** (j - 1) + 8 ** j, want)
            t = R.count(R.layers8, n)
            self.assertEqual(t.O, want)
            self.assertEqual((t.add + t.sub, t.mul, t.neg), (19 * j * n // 8, j * n // 8 + n, 0))
            self.assertEqual(R.count(R.layers8_half, n).O, want - n)
            self.assertEqual(plans.formula_pow8(j), want)
        self.assertLess(4352, 9 * 512)                # below the textbook at 512 points
        t = R.count(R.layers8_int, 512)
        self.assertEqual((t.G, t.O), (3648, 5952))    # the integer form: 19 and 31 per 8 points

    def test_published_table_count_O(self):
        layers = {3: 28, 4: 72, 5: 176, 6: 384, 7: 896, 8: 2048, 9: 4352, 10: 9728, 11: 21504,
                  12: 45056, 13: 98304, 14: 212992}
        for k, want in layers.items():
            n = 1 << k
            self.assertEqual(R.count(R.wht, n, plan=plans.layers_plan(k)).O, want, k)
            self.assertEqual(plans.formula_layers_O(k), want, k)
            self.assertEqual(R.count(R.wht, n).O, min(want, k * n), k)       # cheapest mix
            self.assertLess(want, plans.alman_rao_exact(k), k)
        for k in range(1, 9):
            self.assertEqual(R.count(R.wht, 1 << k).O, k << k)               # the textbook, to 256
        raw = {2: 8, 3: 20, 4: 56, 5: 144, 6: 320, 7: 768, 8: 1792, 9: 3840, 10: 8704,
               11: 19456, 12: 40960}
        for k, want in raw.items():
            self.assertEqual(R.count(R.wht, 1 << k, norm='raw').O, want, k)
        ortho = {2: 8, 3: 28, 4: 64, 6: 384, 8: 2048, 9: 4352, 10: 9728, 12: 45056, 15: 442368}
        for k, want in ortho.items():
            self.assertEqual(R.count(R.wht, 1 << k, norm='ortho').O, want, k)
            self.assertLess(want, (k << k) + (1 << k))                       # textbook and N more

    def test_textbook(self):
        for k in list(range(0, 13)) + [15]:
            t = R.count(R.textbook, 1 << k)
            self.assertEqual((t.O, t.G, t.mul), (k << k, k << k, 0))

    def test_published_table_count_G(self):
        family = {2: 7, 3: 20, 4: 52, 5: 128, 6: 304, 7: 704, 8: 1600, 9: 3584, 10: 7936,
                  11: 17408, 12: 37888}
        for k in range(2, 16):
            n = 1 << k
            want = 3 * n * k // 4 + n // 4
            if k in family:
                self.assertEqual(want, family[k])
            self.assertEqual(R.count(R.family, n).G, want, k)
            self.assertLess(want, plans.published_G(k) + (k == 2), k)        # equal at 4 points
        layers = {1: 2, 2: 7, 3: 19, 4: 54, 5: 132, 6: 304, 7: 736, 8: 1664, 9: 3648, 10: 8320,
                  11: 18176, 12: 38912, 15: 389120}
        self.assertEqual(3 * 32768 * 15 // 4 + 32768 // 4, 376832)
        for k, want in layers.items():
            self.assertEqual(R.count(R.wht, 1 << k, count='G').G, want, k)
        # the family in count (O), as these integer programs run it (tools/circuits: slp_N.txt)
        for k, want in ((2, 11), (3, 32), (4, 84), (5, 208), (6, 496)):
            self.assertEqual(R.count(R.family, 1 << k).O, want, k)

    def test_formulas_agree_with_plans(self):
        for r in plans.table(16):
            k = r['k']
            self.assertEqual(r['O_best'], min(r['O_layers'], r['textbook']), k)
            self.assertEqual(r['G_layers'], plans.plan_cost(plans.best_plan(k, 'G'), 'G'), k)


class TestGenerator(unittest.TestCase):
    def run_python(self, k, count, norm):
        src = codegen.python_source(k, count, norm)
        ns = {}
        exec(compile(src, '<generated>', 'exec'), ns)
        f = ns['wht%d' % (1 << k)]
        gates, _outs, fac = codegen.straight_line(k, count, norm)
        return src, f, gates, fac

    def test_python_straight_line(self):
        rnd = random.Random(6)
        for k, count, norm, lines in ((3, 'O', 'raw', 20), (3, 'O', 'exact', 24), (6, 'O', 'raw', 320),
                                      (9, 'O', 'exact', 4352), (9, 'O', 'raw', 3840),
                                      (10, 'O', 'exact', 9728), (3, 'G', 'exact', 19), (5, 'G', 'exact', 132)):
            n = 1 << k
            src, f, gates, fac = self.run_python(k, count, norm)
            self.assertEqual(len(gates), lines, (k, count, norm))
            self.assertEqual(sum(1 for s in src.splitlines() if s.startswith('    t')), lines)
            x = [rnd.randint(-999, 999) for _ in range(n)]
            want = [fac * v for v in R.textbook(x)]
            got = f(x, c1_2=Fraction(1, 2)) if 'c1_2' in src else f(x)
            self.assertEqual(got, want, (k, count, norm))
            t = R.Tally()
            xs = [R.Counted(v, t) for v in x]
            f(xs, c1_2=Fraction(1, 2)) if 'c1_2' in src else f(xs)
            self.assertEqual(t.O if count == 'O' else t.G, lines)            # one line, one operation

    def test_kernels_header_is_current(self):
        with open(os.path.join(PKG, 'c', 'kernels.h')) as f:
            self.assertEqual(f.read(), codegen.c_kernels_header())

    @unittest.skipUnless(shutil.which(CC), 'no C compiler')
    def test_c_straight_line(self):
        k = 6
        n = 1 << k
        x = [(i * 37) % 101 - 50 for i in range(n)]
        main = ('#include <stdio.h>\n' + codegen.c_source(k, 'O', 'exact', plans.layers_plan(k)) +
                'int main(void){double x[%d],y[%d];for(int i=0;i<%d;i++)x[i]=(double)((i*37)%%101-50);'
                'wht%d(x,y);for(int i=0;i<%d;i++)printf("%%.0f\\n",y[i]);return 0;}\n' % (n, n, n, n, n))
        d = tempfile.mkdtemp()
        try:
            with open(os.path.join(d, 'g.c'), 'w') as f:
                f.write(main)
            subprocess.check_call([CC, '-O1', '-o', os.path.join(d, 'g'), os.path.join(d, 'g.c')])
            out = subprocess.check_output([os.path.join(d, 'g')]).decode().split()
            self.assertEqual([int(v) for v in out], R.textbook(x))
        finally:
            shutil.rmtree(d)


class TestBadArguments(unittest.TestCase):
    def test_count_must_be_O_or_G(self):
        with self.assertRaises(ValueError):
            R.wht([1, 2, 3, 4], count='X')

    @unittest.skipUnless(np is not None, 'numpy is not installed')
    def test_method_is_checked_at_every_length(self):
        from wht56 import fast
        for n in (1, 2, 8):
            with self.assertRaises(ValueError):
                fast.fwht(np.ones(n), method='bad')

    def test_double_negative_gate_is_refused_by_the_generator(self):
        self.assertEqual(codegen._expr([(-1, 'u'), (-1, 'v')], str, str), '-(u + v)')
        with self.assertRaises(ValueError):
            codegen._expr([(-2, 'u'), (-1, 'v')], str, str)


C_BAD_LENGTH_DRIVER = r'''
#include <stdio.h>
#include "wht56.h"
int main(void)
{
    static const size_t bad[] = {0, 3, 5, 6, 7, 12, 24, 100};
    void (*f[4])(double *, size_t) = {wht56_textbook_r2, wht56_textbook_r8, wht56_k8_raw, wht56_k8};
    for (int v = 0; v < 4; v++)
        for (int q = 0; q < 8; q++) {
            double x[128];
            for (int i = 0; i < 128; i++) x[i] = i + 1;
            f[v](x, bad[q]);
            for (int i = 0; i < 128; i++)
                if (x[i] != i + 1) { printf("TOUCHED %d %d\n", v, (int)bad[q]); return 1; }
            if (wht56_valid_length(bad[q]) || wht56_k8_raw_factor(bad[q]) != 0.0) { printf("WRONG\n"); return 1; }
        }
    if (!wht56_valid_length(1) || !wht56_valid_length(64) || wht56_k8_raw_factor(64) != 0.25) { printf("WRONG\n"); return 1; }
    printf("UNTOUCHED OK\n");
    return 0;
}
'''


@unittest.skipUnless(shutil.which(CC), 'no C compiler')
class TestC(unittest.TestCase):
    def test_a_length_that_is_not_a_power_of_two_is_left_alone(self):
        d = tempfile.mkdtemp()
        try:
            with open(os.path.join(d, 'bad.c'), 'w') as f:
                f.write(C_BAD_LENGTH_DRIVER)
            exe = os.path.join(d, 'bad')
            subprocess.check_call([CC, '-std=c11', '-O2', '-I', os.path.join(PKG, 'c'), '-o', exe,
                                   os.path.join(d, 'bad.c'), os.path.join(PKG, 'c', 'wht56.c'), '-lm'])
            self.assertIn('UNTOUCHED OK', subprocess.check_output([exe]).decode())
        finally:
            shutil.rmtree(d)

    def test_the_four_c_transforms_agree(self):
        d = tempfile.mkdtemp()
        try:
            exe = os.path.join(d, 'bench')
            subprocess.check_call([CC, '-std=c11', '-O2', '-o', exe, os.path.join(PKG, 'c', 'bench.c'),
                                   os.path.join(PKG, 'c', 'wht56.c'), '-lm'])
            # one run; every size from 2 points to 2^13 and 2^16 (blocked passes), checked inside
            out = subprocess.check_output([exe, '1'] + [str(k) for k in list(range(1, 14)) + [16]]).decode()
            self.assertIn('CHECK OK', out)
            self.assertNotIn('FAILED', out)
        finally:
            shutil.rmtree(d)


@unittest.skipUnless(np is not None, 'numpy is not installed')
class TestNumpy(unittest.TestCase):
    METHODS = ('k8', 'textbook8', 'textbook2')

    def test_against_the_matrix_up_to_1024(self):
        from wht56 import fast
        g = np.random.default_rng(7)
        for k in range(0, 11):
            n = 1 << k
            H = np.array(circuit.hadamard_matrix(n), dtype=np.int64)
            xi = g.integers(-10 ** 6, 10 ** 6, n)
            xf = g.standard_normal(n)
            xc = g.standard_normal(n) + 1j * g.standard_normal(n)
            for m in self.METHODS:
                got = fast.fwht(xi, method=m)
                self.assertEqual(got.dtype, np.int64)
                self.assertTrue(np.array_equal(got, (H * xi).sum(axis=1)), (m, n))
                self.assertTrue(np.allclose(fast.fwht(xf, method=m), (H * xf).sum(axis=1), rtol=0, atol=1e-9 * n), (m, n))
                self.assertTrue(np.allclose(fast.fwht(xc, method=m), (H * xc).sum(axis=1), rtol=0, atol=1e-9 * n), (m, n))

    def test_random_to_2_15_against_the_textbook(self):
        from wht56 import fast
        g = np.random.default_rng(8)
        for k in (11, 12, 13, 14, 15):
            n = 1 << k
            xi = g.integers(-10 ** 6, 10 ** 6, n)
            self.assertEqual(fast.fwht(xi).tolist(), R.textbook(xi.tolist()), n)
            xf = g.standard_normal(n)
            xc = g.standard_normal(n) + 1j * g.standard_normal(n)
            for x in (xf, xc):
                want = np.array(R.textbook(x.tolist()))
                for m in self.METHODS:
                    self.assertTrue(np.allclose(fast.fwht(x, method=m), want, rtol=0, atol=1e-9 * n), (m, n))

    def test_norms_inverse_inplace_batch(self):
        from wht56 import fast
        g = np.random.default_rng(9)
        for k in (0, 1, 2, 3, 4, 7, 9, 10):
            n = 1 << k
            x = g.standard_normal(n) + 1j * g.standard_normal(n)
            exact = fast.fwht(x, method='textbook2')
            for m in self.METHODS:
                self.assertTrue(np.allclose(fast.fwht(x, 'ortho', m), exact / np.sqrt(n), atol=1e-9 * n))
                raw = fast.fwht(x, 'raw', m)
                self.assertTrue(np.allclose(raw, exact * fast.raw_factor(n, x.dtype, m), atol=1e-9 * n))
                self.assertTrue(np.allclose(fast.ifwht(fast.fwht(x, method=m), m), x, atol=1e-9))
                self.assertTrue(np.allclose(fast.fwht(fast.fwht(x, method=m), method=m), n * x, atol=1e-9 * n))
                y = x.copy()
                self.assertIs(fast.fwht(y, 'exact', m, inplace=True), y)
                self.assertTrue(np.allclose(y, exact, atol=1e-9 * n))
            b = g.standard_normal((3, 5, n))
            got = fast.fwht(b)
            for i in range(3):
                for j in range(5):
                    self.assertTrue(np.allclose(got[i, j], fast.fwht(b[i, j], method='textbook2'), atol=1e-9 * n))
        self.assertEqual(fast.raw_factor(512), 1 / 8)
        self.assertEqual(fast.fwht([1, 2, 3, 4]).tolist(), [10, -2, -4, 0])
        self.assertTrue(np.allclose(fast.ifwht([10, -2, -4, 0]), [1, 2, 3, 4]))
        with self.assertRaises(ValueError):
            fast.fwht(np.zeros(12))
        with self.assertRaises(ValueError):
            fast.fwht(np.zeros(8, dtype=np.int64), norm='ortho', inplace=True)

    def test_the_numpy_kernels_do_the_counted_operations(self):
        from wht56 import fast
        for key, integer, want in (('O8', False, 20), ('G8', True, 31), ('T8', False, 24), ('B2', False, 2)):
            kern, nt, nscr, bits = codegen.numpy_kernel(key, integer)
            calls = [0]

            def counted(f):
                def g(*a, **kw):
                    calls[0] += 1
                    return f(*a, **kw)
                return g
            dt = np.int64 if integer else np.float64
            rows = [np.arange(5, dtype=dt) * (i + 1) for i in range(1 << bits)]
            want_rows = np.einsum('ji,ic->jc', np.array(circuit.hadamard_matrix(1 << bits)), np.array(rows))
            f = circuit.unit(key).factor
            kern(rows, [np.empty(5, dt) for _ in range(nt)], [np.empty(5, dt) for _ in range(nscr)],
                 counted(np.add), counted(np.subtract), counted(np.multiply), counted(np.negative))
            self.assertEqual(calls[0], want, key)
            self.assertTrue(np.allclose(np.array(rows), float(f) * want_rows), key)
        self.assertEqual(fast.operations(512), 4352)
        self.assertEqual(fast.operations(512, method='textbook8'), 4608)
        self.assertEqual(fast.operations(512, norm='ortho'), 4352)
        self.assertEqual(fast.operations(512, method='textbook8', norm='ortho'), 4608 + 512)
        self.assertEqual(fast.operations(512, np.int64), 5952)


if __name__ == '__main__':
    unittest.main()
