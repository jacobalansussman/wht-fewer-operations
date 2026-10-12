#!/usr/bin/env python3
"""h-6-classhub / solve19.py : carry g-1's 19-gate program from tau = -1 to other tau, keeping its wiring.
Step 1 (floats, a candidate only): continuation in tau from -1 with Gauss-Newton on the equations of deform.py, in a frame where
deform.py found a first-order motion.  Step 2 (EXACT): round every gate ratio theta to a simple rational, replay the program in
Fractions, and require every output to be proportional to its row of K^(tensor 3), K = [[1,1],[1,tau]].
usage: solve19.py programfile c0 c1 c2 shift tau_target [tau_target ...]      (c0 c1 c2 = columns of the address map A)"""
import sys, re
from fractions import Fraction as F
path = sys.argv[1]; cols = [int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])]; shift = int(sys.argv[5]); targets = [F(t) for t in sys.argv[6:]]
k = 3; N = 8
gates = []
for line in open(path):
    line = line.split('#')[0].strip()
    if not line or '=' not in line: continue
    nm, rhs = [s.strip() for s in line.split('=')]
    m = re.match(r'^(-?[\d/]*)\s*\*?\s*([a-z]+\d+)\s*([+-])\s*(-?[\d/]*)\s*\*?\s*([a-z]+\d+)$', rhs)
    def num(s): return F(1) if s == '' else F(-1) if s == '-' else F(s)
    gates.append((nm, num(m.group(1)), m.group(2), num(m.group(4)) * (1 if m.group(3) == '+' else -1), m.group(5)))
G = len(gates)
def bits(w): return bin(w).count('1')
img = []
for x in range(N):
    y = 0
    for j in range(k):
        if x >> j & 1: y ^= cols[j]
    img.append(y ^ shift)
def run(theta, zero, one):
    val = {'x%d' % j: [one if img[j] == i else zero for i in range(N)] for j in range(N)}
    for gi, (nm, a, u, b, v) in enumerate(gates): val[nm] = [(a if zero.__class__ is F else float(a)) * (s + theta[gi] * t) for s, t in zip(val[u], val[v])]   # keep the file's own scaling a of each wire
    return val
th0 = [b / a for _, a, _, b, _ in gates]
val = run(th0, F(0), F(1)); outs = {}
for nm, *_ in gates:
    y = val[nm]
    if all(t != 0 for t in y):
        for w in range(N):
            if all(y[x] * (-1) ** bits(w & x) == y[0] for x in range(N)): outs.setdefault(w, nm)
assert len(outs) == N, 'not a Walsh-Hadamard program in this frame'
print('frame: columns', cols, 'shift', shift, '| output wire of each row w:', outs)
def FJ(theta, tau):
    val = run(theta, 0.0, 1.0); res = []
    for w, nm in outs.items():
        y = val[nm]; r = [tau ** bits(w & x) for x in range(N)]
        res += [y[x] * r[0] - y[0] * r[x] for x in range(1, N)]
    return res
def newton(theta, tau, iters=12):
    theta = list(theta)
    for _ in range(iters):
        f = FJ(theta, tau); J = []
        for d in range(G):
            h = 1e-6; t2 = list(theta); t2[d] += h; f2 = FJ(t2, tau); J.append([(b - a) / h for a, b in zip(f, f2)])
        A = [[sum(J[i][e] * J[j][e] for e in range(len(f))) + (1e-12 if i == j else 0) for j in range(G)] for i in range(G)]
        rhs = [-sum(J[i][e] * f[e] for e in range(len(f))) for i in range(G)]
        M = [A[i] + [rhs[i]] for i in range(G)]
        for c in range(G):
            p = max(range(c, G), key=lambda i: abs(M[i][c])); M[c], M[p] = M[p], M[c]
            for i in range(G):
                if i != c and M[i][c] != 0:
                    fct = M[i][c] / M[c][c]
                    for j in range(c, G + 1): M[i][j] -= fct * M[c][j]
        theta = [t + M[i][G] / M[i][i] for i, t in enumerate(theta)]
    return theta, max(abs(x) for x in FJ(theta, tau))
for tgt in targets:
    theta = [float(t) for t in th0]; steps = 40; res = None
    for s in range(1, steps + 1):
        tau = -1.0 + (float(tgt) + 1.0) * s / steps
        theta, res = newton(theta, tau, 6)
    theta, res = newton(theta, float(tgt), 20)
    rat = [F(t).limit_denominator(64) for t in theta]
    val = run(rat, F(0), F(1)); good = 0
    for w, nm in outs.items():
        y = val[nm]; r = [tgt ** bits(w & x) for x in range(N)]
        good += all(y[x] * r[0] == y[0] * r[x] for x in range(N)) and any(y)
    print('tau = %s : float residual %.2e | ratios theta rounded: %s | EXACT replay: %d of %d outputs proportional to their rows%s'
          % (tgt, res, ' '.join(str(t) for t in rat), good, N, '  -> a %d-gate program (G) for this tau' % G if good == N else ''))
    if good == N:
        with open('%s_tau_%s.txt' % ('k19' if 'h8_19' in path else path.split('/')[-1].split('.')[0], str(tgt).replace('/', 'over')), 'w') as f:
            f.write('# program of %d gates, count (G): rows of K x K x K, K = [[1,1],[1,tau]], tau = %s, each output proportional to its row; wiring of %s in the frame columns %s shift %d (file input x_j is input x_(A j + shift) here)\n' % (G, tgt, path.split('/')[-1], cols, shift))
            for gi, (nm, a, u, b, v) in enumerate(gates):
                uu = ('x%d' % img[int(u[1:])]) if u[0] == 'x' else u; vv = ('x%d' % img[int(v[1:])]) if v[0] == 'x' else v
                f.write('%s = %s + %s * %s    # %s\n' % (nm, uu if a == 1 else '%s*%s' % (a, uu), rat[gi] * a, vv, ' '.join(str(t) for t in val[nm])))
