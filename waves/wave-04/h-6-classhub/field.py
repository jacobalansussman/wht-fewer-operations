"""h-6-classhub / field.py : exact number types.  RF = rational functions of one symbol tau over Q (polynomial gcd, exact);
QF = Q[t]/(t^2 - p t - q) (Gaussian rationals: p=0,q=-1; cube root of unity: p=-1,q=-1; (-1+sqrt(-7))/2: p=-1,q=-2)."""
from fractions import Fraction as F
def ptrim(a):
    a = list(a)
    while a and a[-1] == 0: a.pop()
    return tuple(a)
def padd(a, b):
    n = max(len(a), len(b)); return ptrim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])
def pmul(a, b):
    if not a or not b: return ()
    r = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i + j] += x * y
    return ptrim(r)
def pdivmod(a, b):
    a = list(a); q = [F(0)] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b) and a:
        c = a[-1] / b[-1]; d = len(a) - len(b); q[d] = c
        for i, y in enumerate(b): a[i + d] -= c * y
        a = list(ptrim(a))
    return ptrim(q), ptrim(a)
def pgcd(a, b):
    while b: a, b = b, pdivmod(a, b)[1]
    return a
class RF:
    __slots__ = ('n', 'd')
    def __init__(s, n, d=(F(1),)):
        n = ptrim([F(x) for x in n]); d = ptrim([F(x) for x in d]); assert d
        if not n: s.n = (); s.d = (F(1),); return
        g = pgcd(n, d); n = pdivmod(n, g)[0]; d = pdivmod(d, g)[0]; c = d[-1]
        s.n = tuple(x / c for x in n); s.d = tuple(x / c for x in d)
    @staticmethod
    def of(x): return x if isinstance(x, RF) else RF((F(x),))
    def __add__(s, o): o = RF.of(o); return RF(padd(pmul(s.n, o.d), pmul(o.n, s.d)), pmul(s.d, o.d))
    __radd__ = __add__
    def __neg__(s): return RF(tuple(-x for x in s.n), s.d)
    def __sub__(s, o): return s + (-RF.of(o))
    def __rsub__(s, o): return RF.of(o) + (-s)
    def __mul__(s, o): o = RF.of(o); return RF(pmul(s.n, o.n), pmul(s.d, o.d))
    __rmul__ = __mul__
    def __truediv__(s, o): o = RF.of(o); assert o.n; return RF(pmul(s.n, o.d), pmul(s.d, o.n))
    def __rtruediv__(s, o): return RF.of(o) / s
    def __pow__(s, e):
        if e < 0: return (RF.of(1) / s) ** (-e)
        r = RF.of(1)
        for _ in range(e): r = r * s
        return r
    def __eq__(s, o): o = RF.of(o); return s.n == o.n and s.d == o.d
    def __hash__(s): return hash((s.n, s.d))
    def __bool__(s): return bool(s.n)
    def __abs__(s): return s
    def __lt__(s, o): return str(s) < str(o)
    def __str__(s):
        def fac(p):
            out = []; lead = F(1)
            for nm, f in (('t', (F(0), F(1))), ('(t-1)', (F(-1), F(1))), ('(t+1)', (F(1), F(1)))):
                e = 0
                while len(p) >= 2:
                    q, r = pdivmod(p, f)
                    if r: break
                    p = q; e += 1
                if e: out.append(nm + ('^%d' % e if e > 1 else ''))
            if len(p) == 1: lead = p[0]
            else: out.append('[' + ' '.join(str(x) for x in p) + ']')
            return lead, out
        if not s.n: return '0'
        ln, on = fac(s.n); ld, od = fac(s.d); c = ln / ld
        t = '*'.join(on) if on else ''
        r = (str(c) if (c != 1 or not t) else '') if c != -1 or not t else '-'
        r = r + ('*' if r not in ('', '-') and t else '') + t
        if od: r += '/' + ('(' + '*'.join(od) + ')' if len(od) > 1 else od[0])
        return r
    __repr__ = __str__
TAU = RF((0, 1))
def QFclass(p, q, name='t'):
    p = F(p); q = F(q)
    class QF:
        __slots__ = ('a', 'b')
        def __init__(s, a, b=0): s.a = F(a); s.b = F(b)
        @staticmethod
        def of(x): return x if isinstance(x, QF) else QF(x)
        def __add__(s, o): o = QF.of(o); return QF(s.a + o.a, s.b + o.b)
        __radd__ = __add__
        def __neg__(s): return QF(-s.a, -s.b)
        def __sub__(s, o): return s + (-QF.of(o))
        def __rsub__(s, o): return QF.of(o) + (-s)
        def __mul__(s, o): o = QF.of(o); return QF(s.a * o.a + q * s.b * o.b, s.a * o.b + s.b * o.a + p * s.b * o.b)
        __rmul__ = __mul__
        def conj(s): return QF(s.a + p * s.b, -s.b)      # the other root t' = p - t
        def __truediv__(s, o):
            o = QF.of(o); c = o.conj(); nrm = (o * c).a; assert nrm != 0; r = s * c; return QF(r.a / nrm, r.b / nrm)
        def __rtruediv__(s, o): return QF.of(o) / s
        def __pow__(s, e):
            if e < 0: return (QF(1) / s) ** (-e)
            r = QF(1)
            for _ in range(e): r = r * s
            return r
        def __eq__(s, o): o = QF.of(o); return s.a == o.a and s.b == o.b
        def __hash__(s): return hash((s.a, s.b))
        def __bool__(s): return bool(s.a or s.b)
        def __abs__(s): return s
        def __lt__(s, o): return str(s) < str(o)
        def __str__(s): return '%s' % s.a if not s.b else ('(%s%+s%s)' % (s.a, s.b, name) if s.a else '%s%s' % (s.b, name))
        __repr__ = __str__
    return QF
def parse_tau(spec):
    if spec == 'sym': return TAU
    if spec == 'i': return QFclass(0, -1, 'i')(0, 1)
    if spec == 'w3': return QFclass(-1, -1, 'w')(0, 1)          # w^2 + w + 1 = 0
    if spec == 'w6': Q = QFclass(-1, -1, 'w'); return Q(1, 1)   # 1 + w = primitive sixth root of unity
    if spec == 's7': return QFclass(-1, -2, 's')(0, 1)          # s^2 + s + 2 = 0, s = (-1 + sqrt(-7))/2
    return F(spec)
