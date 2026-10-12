"""reference.py -- the transform in pure Python, exact on integers and fractions.
Standard library only.

    textbook(x)        the usual program: N log2 N additions and subtractions
    layers8_half(x)    N = 8^j: j layers of the 20-operation circuit; returns H x / 2^j
    layers8(x)         N = 8^j: the same and N multiplications; returns H x exactly;
                       20 j 8^(j-1) + 8^j operations in count (O)
    layers8_int(x)     N = 8^j: j layers of the 19-gate circuit, no halving, integers stay
                       integers; 19 gates per 8 points in count (G), 31 operations in count (O)
    wht(x, ...)        any N = 2^k: the cheapest mix of 8-point, 4-point and 2-point units
    family(x)          any N = 2^k: the family with (3/4) N log2 N + N/4 gates in count (G)

All take a list of N numbers (int, Fraction, float or complex) and return a new list.
Order: output J is the sum over i of (-1)^(number of 1-bits common to J and i) * x[i].

THE OPERATION COUNTER.  Pass tally=Tally() to any of them.  The inputs are then wrapped in
objects that add one to the tally at every addition, subtraction, negation and
multiplication by a constant that the program really performs.  tally.O is count (O): all
of them.  tally.G is count (G): the additions and subtractions only, because every one of
them is one gate a*u + b*v and the multiplications by constants are free there.
"""
import math
from fractions import Fraction
from .circuit import unit, log2_exact
from . import plans, codegen


class Tally:
    """Counts of the operations performed."""
    __slots__ = ('add', 'sub', 'mul', 'neg')

    def __init__(self):
        self.add = self.sub = self.mul = self.neg = 0

    @property
    def O(self):
        return self.add + self.sub + self.mul + self.neg

    @property
    def G(self):
        return self.add + self.sub

    def __repr__(self):
        return 'Tally(add=%d, sub=%d, mul=%d, neg=%d; O=%d, G=%d)' % (
            self.add, self.sub, self.mul, self.neg, self.O, self.G)


class Counted:
    """A number that reports every operation done on it to a Tally."""
    __slots__ = ('v', 't')

    def __init__(self, v, t):
        self.v = v
        self.t = t

    def __add__(self, o):
        self.t.add += 1
        return Counted(self.v + o.v, self.t)

    def __sub__(self, o):
        self.t.sub += 1
        return Counted(self.v - o.v, self.t)

    def __neg__(self):
        self.t.neg += 1
        return Counted(-self.v, self.t)

    def __mul__(self, c):
        if isinstance(c, Counted):
            raise TypeError('the transform is linear: two values are never multiplied')
        self.t.mul += 1
        return Counted(c * self.v, self.t)

    __rmul__ = __mul__


def _enter(x, tally):
    a = list(x)
    log2_exact(len(a))
    exact = all(isinstance(v, (int, Fraction)) for v in a)
    ints = all(isinstance(v, int) for v in a)
    if tally is not None:
        a = [Counted(v, tally) for v in a]
    return a, exact, ints


def _leave(a, tally, ints):
    if tally is not None:
        a = [v.v for v in a]
    if ints:            # a conversion of type, not an operation
        a = [int(v) if isinstance(v, Fraction) and v.denominator == 1 else v for v in a]
    return a


_kernels = {}


def _apply_unit(a, key, pos, exact):
    """One unit along the address bits pos, pos+1, ..: in place on the list a."""
    if key not in _kernels:
        _kernels[key] = codegen.python_kernel(key)
    kern, fr = _kernels[key]
    extra = tuple(f if exact else float(f) for f in fr)
    m = unit(key).n
    s = 1 << pos
    offs = [u * s for u in range(m)]
    for base in range(0, len(a), m * s):
        for i in range(base, base + s):
            res = kern(*([a[i + o] for o in offs]), *extra)
            for o, v in zip(offs, res):
                a[i + o] = v


def _run_plan(a, plan, exact):
    pos = 0
    for key in plan:
        _apply_unit(a, key, pos, exact)
        pos += unit(key).bits


def textbook(x, tally=None):
    """H x by the textbook program: k layers of N additions and subtractions."""
    a, _exact, ints = _enter(x, tally)
    n = len(a)
    h = 1
    while h < n:
        for base in range(0, n, 2 * h):
            for i in range(base, base + h):
                u, v = a[i], a[i + h]
                a[i] = u + v
                a[i + h] = u - v
        h *= 2
    return _leave(a, tally, ints)


def wht(x, norm='exact', count='O', tally=None, plan=None):
    """The transform of any length N = 2^k by the cheapest mix of the small circuits.

    count='O': units that are cheap when every operation is charged (the 20-operation 8-point
               circuit, the 8-operation 4-point circuit, the textbook step).
    count='G': units that are cheap when a*u + b*v is one operation (19 gates on 8 points,
               7 on 4 points); these never divide, so integers stay integers.
    norm='exact': H x.   norm='raw': H x times the factor the units leave (a power of 1/2).
    norm='ortho': H x / sqrt(N) (a float when k is odd).
    plan: a list of unit names to use instead of the cheapest plan.

    Exact for Python int and Fraction.  With count='O' on integers the 20-operation circuit
    halves in exact fractions and the result is multiplied back: exact, of type int, and slow;
    count='G' never leaves the integers.  numpy scalars (numpy.int64 ...) are not recognised
    as integers here: convert them with int() first, or use fast.fwht."""
    if norm not in ('exact', 'raw', 'ortho'):
        raise ValueError("norm must be 'exact', 'raw' or 'ortho'")
    if count not in ('O', 'G'):
        raise ValueError("count must be 'O' or 'G'")
    a, exact, ints = _enter(x, tally)
    n = len(a)
    k = log2_exact(n)
    if plan is None:
        plan = plans.best_plan(k, count, norm)
    elif sum(unit(u).bits for u in plan) != k:
        raise ValueError('the plan does not cover %d address bits' % k)
    _run_plan(a, plan, exact)
    f = plans.plan_factor(plan)
    if norm == 'exact' and f != 1:
        c = 1 / f
        c = int(c) if c.denominator == 1 else (c if exact else float(c))
        a = [c * v for v in a]                       # N multiplications
    elif norm == 'ortho' and f * f * n != 1:
        if k % 2 == 0:
            c = 1 / (f * (1 << (k // 2)))
            c = int(c) if c.denominator == 1 else (c if exact else float(c))
        else:
            c = float(1 / f) / math.sqrt(n)
        a = [c * v for v in a]                       # N multiplications
    return _leave(a, tally, ints and norm != 'raw' and not (norm == 'ortho' and k % 2))


def _pow8(n):
    k = log2_exact(n)
    if k % 3:
        raise ValueError('the length must be a power of 8, got %d' % n)
    return k // 3


def layers8_half(x, tally=None):
    """N = 8^j.  j layers of the 20-operation circuit.  Returns H x / 2^j (fractions, if the
    inputs are integers).  20 j 8^(j-1) operations in count (O)."""
    j = _pow8(len(x))
    return wht(x, norm='raw', tally=tally, plan=['O8'] * j)


def layers8(x, tally=None):
    """N = 8^j.  H x exactly: j layers of the 20-operation circuit, then one multiplication
    by 2^j for each output.  20 j 8^(j-1) + 8^j operations in count (O)."""
    j = _pow8(len(x))
    return wht(x, norm='exact', tally=tally, plan=['O8'] * j)


def layers8_int(x, tally=None):
    """N = 8^j.  H x exactly by j layers of the 19-gate circuit: no division, integers stay
    integers.  19 j 8^(j-1) gates in count (G); 31 j 8^(j-1) operations in count (O)."""
    j = _pow8(len(x))
    return wht(x, norm='exact', tally=tally, plan=['G8'] * j)


def family(x, tally=None):
    """H x by the family with (3/4) N log2 N + N/4 gates in count (G), for every N = 2^k
    with k >= 2 (2 gates at k = 1).  No division: integers stay integers.

    The recursion is the one stated in the first lines of tools/circuits/gen.py
    (construction 1); this function follows it on numbers, where gen.py writes text.
    A "piece" (lo, m, a) is row a of the m-point transform on the inputs lo .. lo+m-1."""
    a, _exact, ints = _enter(x, tally)
    n = len(a)
    k = log2_exact(n)
    if k == 0:
        return _leave(a, tally, ints)
    if k == 1:
        return _leave([a[0] + a[1], a[0] - a[1]], tally, ints)
    P = {}
    for i in range(n):
        P[(i, 1, 0)] = a[i]

    def E(lo, m, s):
        # make the pieces (lo, m, a) with a < m/2 if s = +1, with a >= m/2 if s = -1
        if m == 2:
            P[(lo, 2, 0 if s > 0 else 1)] = (a[lo] + a[lo + 1]) if s > 0 else (a[lo] - a[lo + 1])
            return
        h, q = m // 2, m // 4
        E(lo, h, 1)
        E(lo + h, h, -1)
        off = 0 if s > 0 else h
        for d in range(q):
            A = P[(lo, h, d)]
            B = P[(lo + h, h, d + q)]
            if q >= 2 and d >= q // 2:                 # hub = A + s B
                M = (A + B) if s > 0 else (A - B)
                t = 2 * P[(lo + h + q, q, d)]
                P1 = (M + t) if s > 0 else (M - t)
                P2 = M - 2 * P[(lo + q, q, d)]
            else:                                      # hub = A - s B
                M = (A - B) if s > 0 else (A + B)
                t = 2 * P[(lo + h, q, d)]
                P1 = (M + t) if s > 0 else (M - t)
                P2 = 2 * P[(lo, q, d)] - M
            P[(lo, m, d + off)] = P1
            P[(lo, m, d + q + off)] = P2

    h, q = n // 2, n // 4
    E(0, h, 1)
    E(h, h, -1)
    out = [None] * n
    for d in range(q):
        A = P[(0, h, d)]
        B = P[(h, h, d + q)]
        M = A + B
        if q >= 2 and d >= q // 2:
            P1 = M + 2 * P[(h + q, q, d)]
            P2 = M - 2 * P[(q, q, d)]
            P1o = 2 * A - P1
            P2o = P2 - 2 * B
            out[d], out[d + q], out[d + h], out[d + q + h] = P1, P2, P1o, P2o
        else:
            P1 = M - 2 * P[(h, q, d)]
            P2 = 2 * P[(0, q, d)] - M
            P1o = 2 * A - P1
            P2o = P2 + 2 * B
            out[d + h], out[d + q + h], out[d], out[d + q] = P1, P2, P1o, P2o
    return _leave(out, tally, ints)


def count(fn, n, **kw):
    """Run fn on n inputs with the counter on; return the Tally."""
    t = Tally()
    fn(list(range(1, n + 1)), tally=t, **kw)
    return t


def matrix_times(x):
    """H x from the definition: N^2 operations.  For tests."""
    n = len(x)
    log2_exact(n)
    out = []
    for j in range(n):
        s = 0
        for i in range(n):
            s = s - x[i] if bin(j & i).count('1') & 1 else s + x[i]
        out.append(s)
    return out
