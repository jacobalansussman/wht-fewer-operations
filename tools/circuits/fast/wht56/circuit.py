"""circuit.py -- read the circuit text files and check them.  Standard library only.

The files in circuits/ are copies, byte for byte, of files in tools/circuits/programs/ of
this repository (circuits/SHA256SUMS lists them).  The format is the one of tools/circuits/slp.py:

    # comment
    name = term                 a renaming (factor 1) or a multiplication by a constant
    name = term + term          one gate
    name = term - term
  with  term = [-] [number *] name  and  number = an integer or p/q.
  The inputs are x0, x1, ...; the output yJ is row J of the transform (times one factor).

THE TRANSFORM.  N = 2^k points.  H[j][i] = +1 when j and i, written in binary, have an even
number of 1-bits in common, and -1 otherwise.  The transform of x is H x.

THE TWO COUNTS (the same rules as slp.py).
  Count (G): one operation is any a*u + b*v.  A multiplication by a constant is free.
  Count (O): every addition, every subtraction and every multiplication by a constant costs one.

Every circuit is checked when it is loaded: it is run on the N unit inputs in exact fractions
and every output yJ is compared with (factor) * row J of H.
"""
import os
import re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
CIRCUIT_DIR = os.path.join(HERE, 'circuits')

_TERM = re.compile(r'([+-]?)(?:(\d+(?:/\d+)?)\*)?([A-Za-z_]\w*)')


def hadamard_entry(j, i):
    """H[j][i]: +1 or -1."""
    return -1 if bin(j & i).count('1') & 1 else 1


def hadamard_matrix(n):
    """The n by n matrix H as a list of rows (n a power of two)."""
    return [[hadamard_entry(j, i) for i in range(n)] for j in range(n)]


def log2_exact(n):
    """k with n = 2^k, or ValueError."""
    if n < 1 or n & (n - 1):
        raise ValueError('the length must be a power of two, got %d' % n)
    return n.bit_length() - 1


class Circuit:
    """One circuit: its gates, its outputs, its factor and its two counts.

    gates   list of (name, [(coefficient, operand name), ...]) with one or two terms;
            renamings are resolved and do not appear.
    outs    outs[J] = the name of the value that is row J (an input name is allowed)
    n, bits the number of points and its logarithm
    factor  every output is factor * (row of H)
    G, O    the two counts
    """

    def __init__(self, text, name=''):
        self.name = name
        alias = {}
        gates = []
        defined = set()
        top = -1
        outputs = {}
        for raw in text.splitlines():
            s = raw.split('#', 1)[0].strip()
            if not s:
                continue
            if '=' not in s:
                raise ValueError('no "=" in line: ' + raw)
            lhs, rhs = s.split('=', 1)
            lhs = lhs.strip()
            rhs = rhs.replace(' ', '').replace('\t', '')
            terms = []
            pos = 0
            while pos < len(rhs):
                m = _TERM.match(rhs, pos)
                if not m or (pos > 0 and not m.group(1)):
                    raise ValueError('cannot read: ' + raw)
                c = Fraction(m.group(2) or 1)
                if m.group(1) == '-':
                    c = -c
                u = m.group(3)
                if re.fullmatch(r'x\d+', u):
                    top = max(top, int(u[1:]))
                elif u not in defined:
                    raise ValueError('%s uses %s before it is defined' % (lhs, u))
                terms.append((c, alias.get(u, u)))
                pos = m.end()
            if lhs in defined or re.fullmatch(r'x\d+', lhs):
                raise ValueError('name defined twice: ' + lhs)
            if not 1 <= len(terms) <= 2 or any(c == 0 for c, _ in terms):
                raise ValueError('a line has one or two terms, none zero: ' + raw)
            defined.add(lhs)
            if len(terms) == 1 and terms[0][0] == 1:
                alias[lhs] = terms[0][1]                  # a renaming: no gate
            else:
                gates.append((lhs, terms))
            if lhs.startswith('y'):
                outputs[lhs] = alias.get(lhs, lhs)
        self.n = top + 1
        self.bits = log2_exact(self.n)
        self.gates = gates
        try:
            self.outs = [outputs['y%d' % j] for j in range(self.n)]
        except KeyError as e:
            raise ValueError('missing output %s' % e)
        # the two counts, by the rules of slp.py
        G = O = 0
        for _, terms in gates:
            if len(terms) == 1:
                O += 1
            else:
                (a, _u), (b, _v) = terms
                G += 1
                O += 1 + (abs(a) != 1) + (abs(b) != 1) + (1 if (a == -1 and b == -1) else 0)
        self.G, self.O = G, O
        self.factor = self._check()

    def _check(self):
        n = self.n
        vec = {}
        for i in range(n):
            e = [Fraction(0)] * n
            e[i] = Fraction(1)
            vec['x%d' % i] = e
        for name, terms in self.gates:
            v = [Fraction(0)] * n
            for c, u in terms:
                v = [p + c * q for p, q in zip(v, vec[u])]
            vec[name] = v
        f = vec[self.outs[0]][0]
        if f == 0:
            raise AssertionError('%s: output 0 is not a multiple of row 0' % self.name)
        for j in range(n):
            if vec[self.outs[j]] != [f * hadamard_entry(j, i) for i in range(n)]:
                raise AssertionError('%s: output y%d is not %s * row %d of H' % (self.name, j, f, j))
        return f


def load(filename):
    with open(os.path.join(CIRCUIT_DIR, filename)) as f:
        return Circuit(f.read(), filename)


# The units.  Each is applied to 1, 2 or 3 address bits at a time.
BUTTERFLY_TEXT = 'y0 = x0 + x1\ny1 = x0 - x1\n'      # the textbook step

_FILES = {
    'B2': None,                         # textbook step, 2 points, 2 operations
    'G4': 'h4_7gates.txt',              # 4 points, 7 gates in count (G); 11 in count (O); integers
    'G8': 'h8_19gates.txt',             # 8 points, 19 gates in count (G); 31 in count (O); integers
    'O4': 'O_family_4_factor.txt',      # 4 points, 8 operations in count (O); output H x / 2
    'O8': 'h8_half_20ops.txt',          # 8 points, 20 operations in count (O); output H x / 2
    'T8': 'O_textbook_8.txt',           # textbook on 8 points, 24 operations (for comparisons)
    'F16': 'h16_52gates.txt',           # 16 points, 52 gates in count (G) (the family at 16 points)
}
_cache = {}


def unit(key):
    """The checked circuit of that name."""
    if key not in _cache:
        if key not in _FILES:
            raise KeyError('no unit called %r' % key)
        fn = _FILES[key]
        _cache[key] = Circuit(BUTTERFLY_TEXT, 'textbook step') if fn is None else load(fn)
    return _cache[key]


def expected_units():
    """(bits, count G, count O, factor) that each unit must have; checked by the tests."""
    h = Fraction(1, 2)
    return {'B2': (1, 2, 2, 1), 'G4': (2, 7, 11, 1), 'G8': (3, 19, 31, 1), 'O4': (2, 7, 8, h),
            'O8': (3, 19, 20, h), 'T8': (3, 24, 24, 1), 'F16': (4, 52, 84, 1)}
