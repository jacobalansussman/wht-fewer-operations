# x-1-digits/rowdeg.py   count (G).  A polynomial of degree d at the N points 0..N-1 of a row, exact fractions, replayed.
# p(s - n) - p(n) = (s - 2n) * Q_s(m),  m = (s/2 - n)^2,  Q_s of degree E = floor((d-1)/2) in m  (the odd part about s/2).
# Walk 0, N-1, 1, N-2, ... with the two centres s = N-1 and s = N; each step: E Horner gates for Q_s(m), one gate for the value.
from fractions import Fraction as F
from math import comb
def run(d, N):
    gates = 0
    def gate(a, u, b, v):
        nonlocal gates; gates += 1; return tuple(a * p + b * q for p, q in zip(u, v))
    c = [tuple(F(int(i == j)) for j in range(d + 1)) for i in range(d + 1)]      # inputs: the coefficients
    E = (d - 1) // 2; odd = {}
    for s in (N - 1, N):
        h = F(s, 2)
        for e in range(E + 1):
            i = 2 * e + 1; terms = [(F(comb(l, i)) * h ** (l - i), c[l]) for l in range(i, d + 1)]
            w = None
            for (a, v) in terms:
                if w is None: w = tuple(a * t for t in v)          # a scaling: free
                else: w = gate(1, w, a, v)
            odd[(s, e)] = w
    val = {0: c[0]}; n = 0; s = N - 1
    while len(val) < N:
        m2 = s - n
        if 0 <= m2 < N and m2 not in val:
            mm = (F(s, 2) - n) ** 2; q = odd[(s, E)]
            for e in range(E - 1, -1, -1): q = gate(1, odd[(s, e)], mm, q)
            val[m2] = gate(1, val[n], s - 2 * n, q)
        n = m2; s = (2 * N - 1) - s
    ok = all(val[t] == tuple(F(t) ** i for i in range(d + 1)) for t in range(N))
    return gates, ok
for d in (2, 3, 4, 5, 6, 8):
    print(f"degree {d}: " + " ; ".join(f"N={N}: {run(d, N)[0]} gates, exact {run(d, N)[1]}, finite differences {d * (N - 1)}" for N in (16, 64, 256)))
