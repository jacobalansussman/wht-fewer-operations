# s-cross hybrid 3: the product-formula meter. Every wire is scaled to a primitive whole-number vector (free in count G).
# A gate then reads w = (a u + b v) / g with a, b coprime whole numbers and g the common factor of the result.
# Morgenstern's volume argument in this scaling: every N x N minor of the held wires is at most the product of (|a|+|b|)/g
# over the gates so far, so  sum over gates of log2((|a|+|b|)/g) >= log2 |det of the primitive outputs| = (N/2) log2 N for H.
# g > 1 is exactly m-cross's Q gate (a difference quotient): it LOWERS the budget.
import sys, re, math
from fractions import Fraction as Fr
from math import gcd
from functools import reduce
def prim(w):
    den = reduce(lambda a, b: a*b//gcd(a, b), [t.denominator for t in w], 1)
    iv = [int(t*den) for t in w]; g = reduce(gcd, [abs(t) for t in iv], 0)
    return [t//g for t in iv] if g else iv
def term(s):
    m = re.fullmatch(r'([+-]?)(?:([\d/]+)\*)?([A-Za-z_]\w*)', s)
    c = Fr(m.group(2)) if m.group(2) else Fr(1)
    return (-c if m.group(1) == '-' else c), m.group(3)
def load(path):
    W = {}; gates = []
    for line in open(path):
        line = line.split('#')[0].strip()
        if '=' not in line: continue
        nm, rhs = line.split('=', 1); rhs = rhs.replace(' ', '')
        m = re.fullmatch(r'([+-]?(?:[\d/]+\*)?[A-Za-z_]\w*)([+-])(-?(?:[\d/]+\*)?[A-Za-z_]\w*)', rhs)
        if not m: return None
        a, u = term(m.group(1)); b, v = term(m.group(3))
        if m.group(2) == '-': b = -b
        gates.append((nm.strip(), a, u, b, v))
    return gates
def pop(v): return bin(v).count('1')
for path in sys.argv[1:]:
    gates = load(path)
    if not gates: print(path.split('/')[-1], ': not parsed'); continue
    N = 1 + max(int(t[1:]) for g in gates for t in (g[2], g[4]) if re.fullmatch(r'x\d+', t))
    W = {'x%d' % i: [Fr(int(i == j)) for j in range(N)] for i in range(N)}
    tot = 0.0; kinds = {}; q = 0; big = 1
    for (nm, a, u, b, v) in gates:
        w = [a*p + b*r for p, r in zip(W[u], W[v])]; W[nm] = w
        pu, pv, pw = prim(W[u]), prim(W[v]), prim(w)
        # w = alpha*pu + beta*pv ; find alpha, beta as fractions from the scalings
        iu = next(i for i in range(N) if pu[i]); iv = next(i for i in range(N) if pv[i])
        alpha = a*W[u][iu]/pu[iu]; beta = b*W[v][iv]/pv[iv]
        iw = next((i for i in range(N) if pw[i]), None)
        if iw is None: continue
        s = w[iw]/pw[iw]; alpha /= s; beta /= s      # pw = alpha*pu + beta*pv
        den = alpha.denominator*beta.denominator//gcd(alpha.denominator, beta.denominator)
        A, B = abs(int(alpha*den)), abs(int(beta*den)); gg = gcd(A, B); A //= gg; B //= gg; g = den//gg if den % gg == 0 else Fr(den, gg)
        c = (A + B)/g; tot += math.log2(c); key = '(%d,%d)/%s' % (min(A, B), max(A, B), g); kinds[key] = kinds.get(key, 0) + 1
        q += g > 1; big = max(big, A, B)
    rows = set(); 
    for nm, w in W.items():
        p = prim(w)
        for sgn in (1, -1): rows.add(tuple(sgn*t for t in p))
    isH = all(tuple((-1)**pop(s & x) for x in range(N)) in rows for s in range(N))
    k = N.bit_length() - 1
    print('%-34s N=%3d gates=%4d  budget=%8.2f  needed (N/2)log2N=%4d  slack=%8.2f  Q gates=%d  largest coefficient=%d  holds all rows of H: %s' % (path.split('/')[-1], N, len(gates), tot, N*k//2, tot - N*k/2, q, big, isH))
    print('      gate kinds (a,b)/g : count  ', dict(sorted(kinds.items(), key=lambda t: -t[1])))
