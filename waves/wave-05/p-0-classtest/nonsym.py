#!/usr/bin/env python3
"""nonsym.py (p-0-classtest): e2-0's staircase for NON-symmetric kernels, by the one-line reduction
    [[a,b],[c,d]] = diag(1, c/a) . [[1,1],[1,tau]] . diag(a, b),   tau = a d / (b c)        (a, b, c non-zero)
so the k-th Kronecker power is (row scalings) . (power of [[1,1],[1,tau]]) . (column scalings), and scalings are free in count (G).
Takes h-6-classhub/gen_tau.py's program for tau (wave 4's generator, used as is), multiplies the coefficient of every gate that reads
an input x by its column scaling a^(zeros of x) b^(ones of x), and REPLAYS from scratch with exact fractions on the kernel's own
power: every output must be a non-zero multiple of its row (the multiple is the row scaling (a/c)^(ones of w)).
Prints gates, rate gates/(N log2 N), and the size of the coefficients in two normalisations:
  'ratio'  = |b/a| of a gate a*u + b*v in the symmetric normal form (scale-free part; this is what a bounded-coefficient wall sees)
  'own'    = largest numerator or denominator after the input scalings are folded in (grows like max(|a|,|b|)^k: a scaling, not a need).
usage: nonsym.py kmax a b c d"""
import sys
from fractions import Fraction as F
sys.path.insert(0, 'waves/wave-04/h-6-classhub')
from gen_tau import build
kmax = int(sys.argv[1]); a, b, c, d = [F(x) for x in sys.argv[2:6]]
tau = a * d / (b * c)
print('kernel [[%s,%s],[%s,%s]]  tau = ad/(bc) = %s' % (a, b, c, d, tau))
for k in range(2, kmax + 1):
    N = 1 << k
    prog, vec, ok = build(k, tau)
    ones = lambda x: bin(x).count('1')
    col = [a ** (k - ones(x)) * b ** ones(x) for x in range(N)]
    new = []
    for nm, ca, u, cb, v in prog:
        if u[0] == 'x': ca = ca * col[u[1]]
        if v[0] == 'x': cb = cb * col[v[1]]
        new.append((nm, ca, u, cb, v))
    val = {('x', i): [F(int(i == j)) for j in range(N)] for i in range(N)}
    for nm, ca, u, cb, v in new: val[nm] = [ca * s + cb * t for s, t in zip(val[u], val[v])]
    def krow(w):
        r = []
        for x in range(N):
            e = F(1)
            for j in range(k):
                e *= ((a, b), (c, d))[(w >> j) & 1][(x >> j) & 1]
            r.append(e)
        return r
    rows = [krow(w) for w in range(N)]
    got = set(); factors = set()
    for nm, *_ in new:
        if nm[0] == 'y':
            y = val[nm]
            for w in range(N):
                f = y[0] / rows[w][0]
                if f != 0 and all(y[x] == f * rows[w][x] for x in range(N)): got.add(w); factors.add(f); break
    ratios = sorted({abs(cb / ca) for _, ca, _, cb, _ in prog})
    own = max(max(abs(z.numerator), z.denominator) for _, ca, _, cb, _ in new for z in (ca, cb))
    print('  k=%d N=%-3d gates %-4d rate %.4f  textbook %-4d  all %d outputs proportional to their rows: %s  | distinct |ratio| %d, largest %s, smallest %s | own-scale largest integer: %d digits'
          % (k, N, len(new), len(new) / (N * k), N * k, N, got == set(range(N)), len(ratios), ratios[-1], ratios[0], len(str(own))))
