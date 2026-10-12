# j-note: independent replay of e2-0's count-(G) programs (own parser, exact integers/fractions).
# Each line: name = a * u + b * v   # comment.  Inputs x0..x{N-1}.  Outputs: names starting with 'y'.
import sys, re
from fractions import Fraction as F
def run(path, N):
    val = {('x%d' % i): [F(int(i == j)) for j in range(N)] for i in range(N)}
    gates = 0; outs = []; coefs = set()
    for line in open(path):
        line = line.split('#')[0].strip()
        if not line: continue
        m = re.fullmatch(r'(\w+)\s*=\s*(\S+)\s*\*\s*(\w+)\s*\+\s*(\S+)\s*\*\s*(\w+)', line)
        assert m, line
        name, a, u, b, v = m.groups()
        a, b = F(a), F(b); coefs.add(abs(a)); coefs.add(abs(b))
        assert name not in val and u in val and v in val, line
        val[name] = [a * p + b * q for p, q in zip(val[u], val[v])]
        gates += 1
        if name.startswith('y'): outs.append(tuple(val[name]))
    k = N.bit_length() - 1
    rows = {tuple(F((-1) ** bin(r & c).count('1')) for c in range(N)) for r in range(N)}
    ok = (len(outs) == N and set(outs) == rows)
    target = 3 * N * k // 4 + N // 4
    print(path.split('/')[-1], 'N=%d' % N, 'gates=%d' % gates, 'formula(3/4 N k + N/4)=%d' % target,
          'outputs are exactly the %d rows of H: %s' % (N, ok), 'coefficient sizes:', sorted(map(str, coefs)))
    return ok and gates == target
allok = True
for N in (4, 8, 16, 32, 64):
    allok &= run('e2-0-pieces/slp_%d.txt' % N, N)
print('ALL PASS' if allok else 'FAIL')
