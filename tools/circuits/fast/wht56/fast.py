"""fast.py -- the transform on numpy arrays.  Needs numpy; the rest of the package does not.

    fwht(a, norm='exact', method='k8', inplace=False)

a       an array whose last axis has length N = 2^k.  float64, complex128 and int64 are the
        types this was written and tested for (float32 and complex64 run the same code; other
        integer types are converted to int64).
method  'k8'         the 8-point circuits of this folder on three address bits at a time, and
                     a textbook step for each bit left over.  Floats and complex numbers use
                     the 20-operation circuit (19 additions and subtractions, one halving).
                     Integers cannot be halved, so they use the 19-gate circuit, which doubles
                     instead: 31 operations for 8 points when every operation is charged,
                     MORE than the textbook's 24.
        'textbook8'  the textbook, three layers at a time: 24 operations for 8 points.  It
                     moves memory exactly as 'k8' does, so it is the fair comparison.
        'textbook2'  the textbook, one layer at a time.
norm    'exact'  H x.  With 'k8' on floats this is one more pass: N multiplications by 2^m,
                 m = floor(k/3).  Integers and the textbook need no such pass.
        'ortho'  H x / sqrt(N).  One pass of N multiplications in every method, the textbook
                 included.  An integer array is converted to float64 first, which cannot
                 be done in place.
        'raw'    whatever comes out, no last pass: H x / 2^m with 'k8' on floats, H x otherwise.
                 raw_factor(N, dtype, method) gives the factor.
Integer arrays of every type are converted to int64 and computed in int64: sums that do not
fit wrap around without a message, and uint64 values of 2^63 or more come out wrong.  That is
numpy's arithmetic; use the pure-Python reference for large integers.
inplace True: a must be a C-contiguous writeable array of a supported type; it is overwritten
        and returned.  False (default): a is not touched.

What each costs for N = 2^k = 8^m points, every operation charged (one numpy call on a slice
of n numbers is n operations):
                      'raw'             'exact'              'ortho'
    textbook          N k               N k                  N k + N
    'k8', floats      (5/6) N k         (5/6) N k + N        (5/6) N k + N
    'k8', integers    (31/24) N k       (31/24) N k          not available
So when the orthonormal transform is wanted, both pay the last N and the saving is a sixth
of the additions and subtractions.  The kernels are written by codegen.py from the circuit
files.  Each also makes one or two copies of a row (see codegen.numpy_kernel_source), which
are not arithmetic and are not counted.
"""
import math
import numpy as np
from .circuit import log2_exact
from . import codegen

_kern = {}


def _kernel(key, integer):
    if (key, integer) not in _kern:
        _kern[(key, integer)] = codegen.numpy_kernel(key, integer)
    return _kern[(key, integer)]


def _units(k, method, integer):
    if method == 'k8':
        return [('G8' if integer else 'O8')] * (k // 3) + ['B2'] * (k % 3)
    if method == 'textbook8':
        return ['T8'] * (k // 3) + ['B2'] * (k % 3)
    if method == 'textbook2':
        return ['B2'] * k
    raise ValueError("method must be 'k8', 'textbook8' or 'textbook2'")


def raw_factor(n, dtype=np.float64, method='k8'):
    """The f with fwht(a, norm='raw') == f * H a."""
    k = log2_exact(n)
    if method != 'k8' or np.issubdtype(np.dtype(dtype), np.integer):
        return 1.0
    return 0.5 ** (k // 3)


def operations(n, dtype=np.float64, method='k8', norm='exact'):
    """The number of arithmetic operations fwht performs on one vector of length n,
    every operation charged (count (O))."""
    k = log2_exact(n)
    integer = np.issubdtype(np.dtype(dtype), np.integer)
    per8 = {'k8': 31 if integer else 20, 'textbook8': 24, 'textbook2': 24}[method]
    ops = (k // 3) * per8 * n // 8 + (k % 3) * n
    f = raw_factor(n, dtype, method)
    if (norm == 'exact' and f != 1.0) or (norm == 'ortho' and k > 0):
        ops += n
    return ops


def fwht(a, norm='exact', method='k8', inplace=False):
    if norm not in ('exact', 'ortho', 'raw'):
        raise ValueError("norm must be 'exact', 'ortho' or 'raw'")
    if method not in ('k8', 'textbook8', 'textbook2'):
        raise ValueError("method must be 'k8', 'textbook8' or 'textbook2'")
    if inplace:
        if not (isinstance(a, np.ndarray) and a.flags.c_contiguous and a.flags.writeable):
            raise ValueError('inplace=True needs a C-contiguous writeable numpy array')
        if a.dtype.kind not in 'fc' and a.dtype != np.int64:
            raise ValueError('inplace=True needs a float, complex or int64 array')
    else:
        a = np.array(a, order='C', copy=True)
        if a.dtype.kind in 'biu':
            a = a.astype(np.float64 if norm == 'ortho' else np.int64)
        elif a.dtype.kind not in 'fc':
            raise TypeError('cannot transform an array of type %s' % a.dtype)
    integer = a.dtype.kind == 'i'
    if integer and norm == 'ortho':
        raise ValueError("norm='ortho' is not available for an integer array in place")
    if a.ndim == 0:
        raise ValueError('the array has no axis')
    n = a.shape[-1]
    k = log2_exact(n)
    if k == 0 or a.size == 0:
        return a
    batch = a.size // n
    bufs = {}
    pos = 0
    for key in _units(k, method, integer):
        kern, nt, nscr, bits = _kernel(key, integer)
        m = 1 << bits
        s = 1 << pos
        blocks = n // (m * s)
        v = a.reshape(batch, blocks, m, s)
        rows = [v[:, :, u, :] for u in range(m)]
        if bits not in bufs:                   # buffers of batch * N / 2^bits numbers, reused
            bufs[bits] = [np.empty(batch * (n >> bits), a.dtype) for _ in range(nt + nscr)]
        shaped = [b.reshape(batch, blocks, s) for b in bufs[bits]]
        kern(rows, shaped[:nt], shaped[nt:], np.add, np.subtract, np.multiply, np.negative)
        pos += bits
    f = raw_factor(n, a.dtype, method)
    if norm == 'exact' and f != 1.0:
        a *= 1.0 / f                           # N multiplications
    elif norm == 'ortho':
        a *= 1.0 / (f * math.sqrt(n))          # N multiplications
    return a


def ifwht(a, method='k8', inplace=False):
    """The inverse of fwht(norm='exact'): H x / N, because H H = N.  The result is a float or
    complex array (an integer array is converted first, so it cannot be done in place)."""
    if not inplace:
        a = np.array(a, order='C', copy=True)
        if a.dtype.kind in 'biu':
            a = a.astype(np.float64)
    elif not isinstance(a, np.ndarray) or a.dtype.kind not in 'fc':
        raise ValueError('inplace=True needs a float or complex array')
    a = fwht(a, norm='raw', method=method, inplace=True)
    n = a.shape[-1]
    a *= 1.0 / (raw_factor(n, a.dtype, method) * n)
    return a
