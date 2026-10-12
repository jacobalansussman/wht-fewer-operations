#!/usr/bin/env python3
"""slp.py -- reader, counter and exact checker for straight-line programs
that compute the Walsh-Hadamard transform.  Standard library only.

THE TRANSFORM.  N = 2^k points.  H is the N by N matrix with entries
    H[j][i] = (-1)^(number of 1-bits common to j and i),
so every entry is +1 or -1.  Output j of "the transform of x" is
    sum over i of H[j][i] * x_i.
A program is checked against "f * H" for a factor f: f = 1 is the exact
transform, f = 1/sqrt(N) the orthonormal one.

THE FORMAT (one text file per program).
    # anything after a hash is a comment
    name = term                 a renaming (coefficient 1) or a scaling
    name = term + term          one gate
    name = term - term
  where  term = [-] [number *] name   and  number = an integer or p/q.
  Inputs are x0 .. x(N-1); N is one more than the largest index used.
  Every name is defined once, before it is used.
  Outputs are the names that start with the letter y.  (For files of
  other authors that list the outputs in a comment line "# OUT a b c",
  that list is used instead.)  In the files written by gen.py the output
  called yJ is row J of H times the factor.

THE TWO COUNTS.
  Count (G): a gate is any a*u + b*v with constants a, b.  Scalings are
    free.  A line with two terms costs 1, a line with one term costs 0.
  Count (O): every addition, every subtraction and every multiplication
    by a constant costs 1.  A line a*u + b*v costs
        1                           for the addition or subtraction
      + 1 for each of a, b whose absolute value is not 1
      + 1 more if a = b = -1       (the value -(u+v): add, then negate).
    A line c*u costs 1, except that c = 1 is a renaming and costs 0.
    This is the gate set of OpenAI's preprint of 25 September 2026
    (gates u+v, u-v, c*u, one each).
  Count (O'), Alman and Rao's convention: the same, except that a
    multiplication by -1 is free.  So "-1 * u" costs 0 and "-u - v"
    costs 1.  In both conventions a multiplication by 2 or by 1/2 costs 1.
  A program is "strict" when every line is u+v, u-v or c*u with c not 1
  or -1 (or a renaming).  For a strict program (O) = (O').

THE CHECKS (all exact, integers only).
  packed:  the program is run once on the inputs x_i = Z * B^i for a
    large power of two B.  Every value is then one big integer whose
    base-B digits are its N coefficients.  The program first bounds
    every coefficient (sum of absolute values through the gates) and
    takes B more than twice the bound times Z, so two different
    coefficient vectors cannot give the same integer.  Equality with the
    packed row of f * H is therefore the same as equality on all N unit
    vectors.  Z clears the denominators.
  dense:   for N <= 64, the coefficient vector of every value is kept as
    a list and each output is compared with H entry by entry.
  random:  the program is run on random integer vectors (dense for
    N <= 256, sparse above) and compared with the definition of H.
"""
import re, sys, random
from fractions import Fraction as Fr
from math import gcd

TOK = re.compile(r'\s*(?:(\d+(?:/\d+)?)|([A-Za-z_]\w*)|([-+*]))')


class Program:
    def __init__(self, lines, outs=None, title=''):
        self.lines = lines            # list of (name, [(coef, operand)])
        self.title = title
        defined = set()
        mx = -1
        for name, terms in lines:
            if name in defined or re.fullmatch(r'x\d+', name):
                raise ValueError('name defined twice: ' + name)
            if not 1 <= len(terms) <= 2:
                raise ValueError('a line has one or two terms: ' + name)
            for c, u in terms:
                if c == 0:
                    raise ValueError('zero coefficient in ' + name)
                if re.fullmatch(r'x\d+', u):
                    mx = max(mx, int(u[1:]))
                elif u not in defined:
                    raise ValueError('%s uses %s before it is defined' % (name, u))
            defined.add(name)
        self.N = mx + 1
        if self.N < 2 or self.N & (self.N - 1):
            raise ValueError('number of inputs is not a power of two: %d' % self.N)
        self.k = self.N.bit_length() - 1
        if outs is None:
            outs = [name for name, _ in lines if name.startswith('y')]
        self.outs = outs

    # ---- the counts -------------------------------------------------
    def counts(self):
        G = O = OAR = 0
        add = sub = mul = neg = ren = 0
        strict = True
        for name, terms in self.lines:
            if len(terms) == 1:
                c = terms[0][0]
                if c == 1:
                    ren += 1
                elif c == -1:
                    neg += 1; O += 1; strict = False
                else:
                    mul += 1; O += 1; OAR += 1
            else:
                (a, _), (b, _) = terms
                G += 1
                m = (abs(a) != 1) + (abs(b) != 1)
                n = 1 if (a == -1 and b == -1) else 0
                O += 1 + m + n
                OAR += 1 + m
                mul += m; neg += n
                if m or n:
                    strict = False
                if (a > 0) == (b > 0):
                    add += 1
                else:
                    sub += 1
        return dict(G=G, O=O, OAR=OAR, add=add, sub=sub, mul=mul, neg=neg,
                    renamings=ren, strict=strict)

    # ---- check 1: packed, equivalent to all N unit vectors ----------
    def packed_check(self):
        """Returns the list of (output name, row j, factor f) or raises."""
        N, k = self.N, self.k
        M = {}; D = {}
        for i in range(N):
            M['x%d' % i] = Fr(1); D['x%d' % i] = 1
        Z = 1
        last = {}
        for idx, (name, terms) in enumerate(self.lines):
            m = Fr(0); d = 1
            for c, u in terms:
                m += abs(c) * M[u]
                dd = D[u] * c.denominator
                d = d * dd // gcd(d, dd)
                last[u] = idx
            M[name] = m; D[name] = d
            Z = Z * d // gcd(Z, d)
        outset = set(self.outs)
        bound = max(M[o] for o in self.outs) * 2 * Z + 1
        b = (int(bound) + 1).bit_length() + 2          # B = 2^b > 2 * bound
        B = 1 << b
        half = B >> 1
        val = {}
        for i in range(N):
            val['x%d' % i] = Z << (b * i)
        for idx, (name, terms) in enumerate(self.lines):
            v = 0
            for c, u in terms:
                t = val[u] * c.numerator
                if c.denominator != 1:
                    t, r = divmod(t, c.denominator)
                    if r:
                        raise AssertionError('inexact division at ' + name)
                v += t
            val[name] = v
            for c, u in terms:
                if last.get(u) == idx and u not in outset:
                    val.pop(u, None)
        # the rows of H, packed: row j = product over t of (1 +- B^(2^t))
        ref = [1]
        for t in range(k):
            sh = b * (1 << t)
            ref = [r + (r << sh) for r in ref] + [r - (r << sh) for r in ref]
        OFF = half * (((1 << (b * N)) - 1) // (B - 1))
        res = []
        for o in self.outs:
            V = val[o]
            W = V + OFF
            d0 = (W & (B - 1)) - half
            if d0 == 0:
                raise AssertionError('output %s has coefficient 0 at x0' % o)
            j = 0
            for t in range(k):
                dt = ((W >> (b * (1 << t))) & (B - 1)) - half
                if dt == -d0:
                    j |= 1 << t
                elif dt != d0:
                    raise AssertionError('output %s is not a multiple of a row of H' % o)
            if V != d0 * ref[j]:
                raise AssertionError('output %s differs from %s * row %d' % (o, Fr(d0, Z), j))
            res.append((o, j, Fr(d0, Z)))
        return res

    # ---- check 2: dense coefficient vectors, N <= 64 ----------------
    def dense_check(self):
        N = self.N
        vec = {}
        for i in range(N):
            e = [Fr(0)] * N; e[i] = Fr(1); vec['x%d' % i] = e
        for name, terms in self.lines:
            v = [Fr(0)] * N
            for c, u in terms:
                w = vec[u]
                v = [p + c * q for p, q in zip(v, w)]
            vec[name] = v
        res = []
        for o in self.outs:
            v = vec[o]
            f = v[0]
            found = None
            for j in range(N):
                if all(v[i] == (f if bin(i & j).count('1') % 2 == 0 else -f) for i in range(N)):
                    found = j; break
            if f == 0 or found is None:
                raise AssertionError('dense: output %s is not a multiple of a row of H' % o)
            res.append((o, found, f))
        return res

    # ---- check 3: random integer inputs against the definition ------
    def random_check(self, rows, seed=1, trials=4):
        """rows: the (name, j, f) list from packed_check."""
        N = self.N
        rnd = random.Random(seed + N)
        Z = 1
        for _, terms in self.lines:
            for c, _u in terms:
                Z = Z * c.denominator        # crude but sufficient
                if Z > 1 << 4000:
                    break
        # a smaller sufficient multiplier: 2^(number of scalings with a denominator) is
        # too big for long programs, so use Fractions when Z would be huge
        use_fr = Z > 1 << 512
        done = 0
        for trial in range(trials):
            if N <= 256 and trial % 2 == 0:
                x = {i: rnd.randint(-10**6, 10**6) for i in range(N)}
            else:
                supp = rnd.sample(range(N), min(N, 12))
                x = {i: rnd.randint(-10**6, 10**6) for i in supp}
            val = {}
            for i in range(N):
                xi = x.get(i, 0)
                val['x%d' % i] = Fr(xi) if use_fr else xi * Z
            for name, terms in self.lines:
                v = 0
                for c, u in terms:
                    if c.denominator == 1:
                        v += val[u] * c.numerator
                    elif use_fr:
                        v += val[u] * c
                    else:
                        t, r = divmod(val[u] * c.numerator, c.denominator)
                        assert r == 0
                        v += t
                val[name] = v
            for o, j, f in rows:
                want = 0
                for i, xi in x.items():
                    want += xi if bin(i & j).count('1') % 2 == 0 else -xi
                got = val[o] if use_fr else Fr(val[o], Z)
                if got != f * want:
                    raise AssertionError('random: output %s wrong' % o)
            done += 1
        return done


def parse_text(text, title=''):
    lines = []
    outs = None
    for raw in text.splitlines():
        if raw.startswith('# OUT '):
            outs = raw[6:].split()
        s = raw.split('#', 1)[0].strip()
        if not s:
            continue
        if '=' not in s:
            raise ValueError('no "=" in line: ' + raw)
        lhs, rhs = s.split('=', 1)
        name = lhs.strip()
        toks = []
        pos = 0
        rhs = rhs.rstrip()
        while pos < len(rhs):
            m = TOK.match(rhs, pos)
            if not m:
                raise ValueError('cannot read: ' + raw)
            if m.group(1):
                toks.append(('n', m.group(1)))
            elif m.group(2):
                toks.append(('w', m.group(2)))
            else:
                toks.append(('o', m.group(3)))
            pos = m.end()
        terms = []
        i = 0
        while i < len(toks):
            sign = 1
            if terms and not (toks[i][0] == 'o' and toks[i][1] in '+-'):
                raise ValueError('expected + or -: ' + raw)
            while i < len(toks) and toks[i][0] == 'o' and toks[i][1] in '+-':
                if toks[i][1] == '-':
                    sign = -sign
                i += 1
            coef = Fr(1)
            if toks[i][0] == 'n':
                coef = Fr(toks[i][1]); i += 1
                if toks[i] != ('o', '*'):
                    raise ValueError('expected *: ' + raw)
                i += 1
            if toks[i][0] != 'w':
                raise ValueError('expected a name: ' + raw)
            terms.append((sign * coef, toks[i][1])); i += 1
        lines.append((name, terms))
    return Program(lines, outs, title)


def parse_file(path):
    with open(path) as f:
        return parse_text(f.read(), path)


def verify(prog, labelled=False, quick=False):
    """Run every check that the size allows.  Returns a summary dict.
    labelled: require that the output called yJ is row J."""
    c = prog.counts()
    rows = prog.packed_check()
    N = prog.N
    js = sorted(j for _, j, _ in rows)
    if js != list(range(N)):
        raise AssertionError('the outputs are not the N rows of H, each once')
    facs = sorted(set(f for _, _, f in rows))
    if labelled:
        for o, j, _ in rows:
            if o != 'y%d' % j:
                raise AssertionError('output %s is row %d' % (o, j))
    how = ['packed (all %d unit vectors)' % N]
    if N <= 64:
        rows2 = prog.dense_check()
        if rows2 != rows:
            raise AssertionError('dense and packed checks disagree')
        how.append('dense')
    if not quick:
        n = prog.random_check(rows)
        how.append('%d random vectors' % n)
    c.update(N=N, k=prog.k, factors=facs, how=how,
             labels_are_rows=all(o == 'y%d' % j for o, j, _ in rows))
    return c


def fmt_fac(facs):
    return ', '.join(str(f) for f in facs)


if __name__ == '__main__':
    for path in sys.argv[1:]:
        p = parse_file(path)
        r = verify(p)
        print('%s: N=%d  (G)=%d  (O)=%d  (O\')=%d  [add %d, sub %d, mul %d, neg %d]  strict=%s  outputs = (%s) * rows of H, each row once; labels are rows: %s; checks: %s'
              % (path, r['N'], r['G'], r['O'], r['OAR'], r['add'], r['sub'], r['mul'], r['neg'],
                 r['strict'], fmt_fac(r['factors']), r['labels_are_rows'], '; '.join(r['how'])))
