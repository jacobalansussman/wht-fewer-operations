"""codegen.py -- write straight-line code from the circuit files.  Standard library only.

Three things are written here, all from the text files in circuits/ and never by hand:

  1. Straight-line programs for a whole size N = 2^k, as Python or as C:
         python_source(k)   c_source(k)
     One line is one operation of count (O) (an addition, a subtraction, or a multiplication
     by a constant), or one gate of count (G) when the units of count (G) are used.
  2. The small kernels that the pure-Python reference (reference.py) and the numpy version
     (fast.py) call in a loop:   python_kernel(unit)   numpy_kernel(unit)
  3. The header c/kernels.h of the C version:   c_kernels_header()

A gate a*u + b*v is always written so that the operations performed are the ones that
count (O) charges: "2*v - u" and not "-u + 2*v"; "-(u + v)" when both signs are minus.
"""
from fractions import Fraction
from .circuit import unit
from . import plans


# ---------------------------------------------------------------- expressions

def _expr(terms, nm, const):
    """One gate as an expression.  nm(name) and const(positive Fraction) give the texts."""
    def t(c, u):
        a = abs(c)
        return nm(u) if a == 1 else '%s*%s' % (const(a), nm(u))
    if len(terms) == 1:
        c, u = terms[0]
        if c == -1:
            return '-' + nm(u)
        return ('-' if c < 0 else '') + t(c, u)
    (a, u), (b, v) = terms
    if a < 0 and b > 0:
        (a, u), (b, v) = (b, v), (a, u)
    if a > 0:
        return '%s %s %s' % (t(a, u), '+' if b > 0 else '-', t(b, v))
    _only_minus_one_twice(a, b)
    return '-(%s + %s)' % (t(a, u), t(b, v))


def _only_minus_one_twice(a, b):
    """Two negative constants: only -u - v is written, as -(u + v), which is what count (O)
    charges (an addition and a change of sign).  Any other such gate, say -2u - v, would be
    written with one operation more than the count charges, so it is refused.  No circuit of
    this folder has one."""
    if (a, b) != (-1, -1):
        raise ValueError('a gate %s*u + %s*v with two negative constants that are not both -1 is not '
                         'supported by the code generator' % (a, b))


def _const_py(c):
    """Integers as literals; p/q as the name c<p>_<q>, a keyword argument of the function."""
    return str(c.numerator) if c.denominator == 1 else 'c%d_%d' % (c.numerator, c.denominator)


def _const_c(c):
    return repr(float(c))


def _fraction_names(gates):
    s = set()
    for _, terms in gates:
        for c, _u in terms:
            if abs(c).denominator != 1:
                s.add(abs(c))
    return sorted(s)


# ---------------------------------------------------------------- whole sizes

def straight_line(k, count='O', norm='exact', plan=None):
    """The gates for 2^k points: (gates, outs, factor).  gates as in circuit.Circuit.gates,
    with inputs x0.., and values t1, t2, ...; outs[J] is the name of row J; every output is
    factor * (row of H).  norm is 'exact' or 'raw' (see plans.py)."""
    if norm not in ('exact', 'raw'):
        raise ValueError("norm must be 'exact' or 'raw' here")
    if plan is None:
        plan = plans.best_plan(k, count, norm)
    n = 1 << k
    if sum(unit(u).bits for u in plan) != k:
        raise ValueError('the plan does not cover %d bits' % k)
    wires = ['x%d' % i for i in range(n)]
    gates = []
    pos = 0
    fac = Fraction(1)
    for uname in plan:
        c = unit(uname)
        m = c.n
        new = wires[:]
        for base in range(n):
            if (base >> pos) & (m - 1):
                continue
            mp = {'x%d' % u: wires[base + (u << pos)] for u in range(m)}
            for name, terms in c.gates:
                w = 't%d' % (len(gates) + 1)
                gates.append((w, [(cf, mp[u]) for cf, u in terms]))
                mp[name] = w
            for u in range(m):
                new[base + (u << pos)] = mp[c.outs[u]]
        wires = new
        pos += c.bits
        fac *= c.factor
    if norm == 'exact' and fac != 1:
        for j in range(n):
            w = 't%d' % (len(gates) + 1)
            gates.append((w, [(1 / fac, wires[j])]))        # one multiplication for each output
            wires[j] = w
        fac = Fraction(1)
    return gates, wires, fac


def _counts(gates):
    G = O = 0
    for _, terms in gates:
        if len(terms) == 1:
            O += 1
        else:
            (a, _u), (b, _v) = terms
            G += 1
            O += 1 + (abs(a) != 1) + (abs(b) != 1) + (1 if (a == -1 and b == -1) else 0)
    return G, O


def _header(k, count, norm, plan, gates, fac):
    G, O = _counts(gates)
    n = 1 << k
    return [
        'Walsh-Hadamard transform on %d points, straight-line program.' % n,
        'Written by wht56/codegen.py from the circuit files in wht56/circuits/.  Do not edit.',
        'Units, lowest address bits first: %s.' % (', '.join(plan) if plan else '(none)'),
        'Output J = %s(row J of H) . x,  H[J][i] = (-1)^(number of 1-bits common to J and i).'
        % ('' if fac == 1 else '(%s) * ' % fac),
        'Operations: %d in count (O) (additions, subtractions, multiplications by constants);'
        % O,
        '%d in count (G) (gates a*u + b*v, constants free).  Textbook: %d.' % (G, k * n),
    ]


def python_source(k, count='O', norm='exact', plan=None, fname=None):
    """Python source of a function  fname(x) -> list  for 2^k points."""
    if plan is None:
        plan = plans.best_plan(k, count, norm)
    gates, outs, fac = straight_line(k, count, norm, plan)
    n = 1 << k
    fname = fname or 'wht%d' % n
    fr = _fraction_names(gates)
    args = ''.join(', %s=%r' % (_const_py(c), float(c)) for c in fr)
    out = ['# ' + h for h in _header(k, count, norm, plan, gates, fac)]
    if fr:
        out.append('# For exact arithmetic on integers pass %s.'
                   % ', '.join('%s=fractions.Fraction(%d, %d)' % (_const_py(c), c.numerator, c.denominator)
                               for c in fr))
    out.append('def %s(x%s):' % (fname, args))
    out.append('    if len(x) != %d:' % n)
    out.append("        raise ValueError('expected %d numbers')" % n)
    nm = lambda u: ('x[%s]' % u[1:]) if u[0] == 'x' else u
    for name, terms in gates:
        out.append('    %s = %s' % (name, _expr(terms, nm, _const_py)))
    out.append('    return [%s]' % ', '.join(nm(w) for w in outs))
    return '\n'.join(out) + '\n'


def c_source(k, count='O', norm='exact', plan=None, fname=None, ctype='double'):
    """C source of  void fname(const double *x, double *y)  for 2^k points (x and y distinct)."""
    if plan is None:
        plan = plans.best_plan(k, count, norm)
    gates, outs, fac = straight_line(k, count, norm, plan)
    n = 1 << k
    fname = fname or 'wht%d' % n
    out = ['/* ' + h for h in _header(k, count, norm, plan, gates, fac)]
    out = [h + ' */' for h in out]
    out.append('void %s(const %s *x, %s *y)' % (fname, ctype, ctype))
    out.append('{')
    nm = lambda u: ('x[%s]' % u[1:]) if u[0] == 'x' else u
    cc = _const_c if ctype in ('double', 'float') else _const_py
    for name, terms in gates:
        out.append('    const %s %s = %s;' % (ctype, name, _expr(terms, nm, cc)))
    for j, w in enumerate(outs):
        out.append('    y[%d] = %s;' % (j, nm(w)))
    out.append('}')
    return '\n'.join(out) + '\n'


# ---------------------------------------------------------------- kernels for reference.py

def python_kernel_source(key, fname):
    """def fname(x0, .., x7, c1_2): ... return (y0, .., y7): one unit on plain numbers."""
    c = unit(key)
    fr = _fraction_names(c.gates)
    args = ['x%d' % i for i in range(c.n)] + [_const_py(f) for f in fr]
    out = ['def %s(%s):' % (fname, ', '.join(args))]
    for name, terms in c.gates:
        out.append('    %s = %s' % (name, _expr(terms, lambda u: u, _const_py)))
    out.append('    return (%s,)' % ', '.join(c.outs))
    return '\n'.join(out) + '\n', fr


def python_kernel(key):
    """(function, list of the non-integer constants it takes after the inputs)."""
    src, fr = python_kernel_source(key, 'kern')
    ns = {}
    exec(compile(src, '<wht56 kernel %s>' % key, 'exec'), ns)
    return ns['kern'], fr


# ---------------------------------------------------------------- kernels for fast.py (numpy)

def numpy_kernel_source(key, fname, integer=False):
    """A unit as numpy calls with out= buffers.  Returns (source, temporaries, scratch).

        def fname(r, t, s, add, sub, mul, neg)
    r: the 2^bits row views (inputs; the outputs are left in them); t: temporaries;
    s: scratch buffers for scaled operands.  Each numpy call is one operation of count (O),
    apart from the copies at the end (an output is kept in a temporary while the input of
    its row is still needed)."""
    c = unit(key)
    last = {}
    for idx, (_n, terms) in enumerate(c.gates):
        for _c, u in terms:
            last[u] = idx
    out_row = {}
    for j, w in enumerate(c.outs):
        if w in out_row or w[0] == 'x':
            raise ValueError('unit %s: an output is an input or appears twice' % key)
        out_row[w] = j
    loc = {'x%d' % i: 'r[%d]' % i for i in range(c.n)}
    temp_of = {}
    free = []
    ntemp = [0]
    nscr = 0
    body = []
    deferred = []

    def const(a):
        if integer:
            if a.denominator != 1:
                raise ValueError('unit %s has the constant %s: not for integer arrays' % (key, a))
            return str(a.numerator)
        return repr(float(a))

    for idx, (name, terms) in enumerate(c.gates):
        srcs = [(cf, loc[u]) for cf, u in terms]
        for _cf, u in terms:                       # temporaries whose value dies here
            if last[u] == idx and u in temp_of and u not in out_row:
                t = temp_of.pop(u)
                if t not in free:
                    free.append(t)
        dest = None
        if name in out_row:
            j = out_row[name]
            if last.get('x%d' % j, -1) <= idx:
                dest = 'r[%d]' % j
        if dest is None:
            if free:
                t = free.pop()
            else:
                t = ntemp[0]
                ntemp[0] += 1
            temp_of[name] = t
            dest = 't[%d]' % t
            if name in out_row:
                deferred.append((out_row[name], t))
        loc[name] = dest
        if len(srcs) == 1:
            cf, a = srcs[0]
            if cf == -1:
                body.append('neg(%s, out=%s)' % (a, dest))
            else:
                body.append('mul(%s, %s%s, out=%s)' % (a, '-' if cf < 0 else '', const(abs(cf)), dest))
            continue
        (ca, a), (cb, b) = srcs
        if ca < 0 and cb > 0:
            (ca, a), (cb, b) = (cb, b), (ca, a)
        if ca < 0:
            _only_minus_one_twice(ca, cb)
        k = 0
        if abs(ca) != 1:
            body.append('mul(%s, %s, out=s[%d])' % (a, const(abs(ca)), k))
            a = 's[%d]' % k
            k += 1
        if abs(cb) != 1:
            body.append('mul(%s, %s, out=s[%d])' % (b, const(abs(cb)), k))
            b = 's[%d]' % k
            k += 1
        nscr = max(nscr, k)
        if ca > 0:
            body.append('%s(%s, %s, out=%s)' % ('add' if cb > 0 else 'sub', a, b, dest))
        else:
            body.append('add(%s, %s, out=%s)' % (a, b, dest))
            body.append('neg(%s, out=%s)' % (dest, dest))
    for j, t in deferred:
        body.append('r[%d][...] = t[%d]' % (j, t))
    src = 'def %s(r, t, s, add, sub, mul, neg):\n' % fname + ''.join('    %s\n' % b for b in body)
    return src, ntemp[0], nscr


def numpy_kernel(key, integer=False):
    """(function, number of temporaries, number of scratch buffers, bits)."""
    src, nt, ns_ = numpy_kernel_source(key, 'kern', integer)
    ns = {}
    exec(compile(src, '<wht56 numpy kernel %s>' % key, 'exec'), ns)
    return ns['kern'], nt, ns_, unit(key).bits


# ---------------------------------------------------------------- the C header

def _c_pass(key, fname, scaled):
    c = unit(key)
    m = c.n
    ptrs = ', '.join('double *restrict a%d' % i for i in range(m))
    out = ['static inline void %s(%s, size_t s%s)' % (fname, ptrs, ', double c' if scaled else ''),
           '{',
           '    for (size_t i = 0; i < s; i++) {',
           '        const double %s;' % ', '.join('x%d = a%d[i]' % (i, i) for i in range(m))]
    for name, terms in c.gates:
        out.append('        const double %s = %s;' % (name, _expr(terms, lambda u: u, _const_c)))
    for j in range(m):
        out.append('        a%d[i] = %s%s;' % (j, 'c * ' if scaled else '', c.outs[j]))
    out += ['    }', '}', '']
    return out


def c_kernels_header():
    """The text of c/kernels.h."""
    t8, o8 = unit('T8'), unit('O8')
    out = [
        '/* kernels.h -- written by wht56/codegen.py (python3 -m wht56 --gen kernels).  Do not edit.',
        ' *',
        ' * Each function applies one 8-point circuit to s columns: a0..a7 are 8 rows of s numbers,',
        ' * and column i of the rows is replaced by the circuit applied to it.',
        ' *',
        ' *   wht56_pass_t8         the textbook on 8 points: %d additions and subtractions; H x' % t8.O,
        ' *                         (from circuits/%s)' % t8.name,
        ' *   wht56_pass_o8         the %d-operation circuit: 19 additions and subtractions and one' % o8.O,
        ' *                         halving; (1/2) H x   (from circuits/%s)' % o8.name,
        ' *   wht56_pass_o8_scaled  the same, with every output multiplied by c: 8 more multiplications',
        ' */',
        '#ifndef WHT56_KERNELS_H',
        '#define WHT56_KERNELS_H',
        '#include <stddef.h>',
        '',
    ]
    out += _c_pass('T8', 'wht56_pass_t8', False)
    out += _c_pass('O8', 'wht56_pass_o8', False)
    out += _c_pass('O8', 'wht56_pass_o8_scaled', True)
    out.append('#endif')
    return '\n'.join(out) + '\n'
