# u-4-zdz: run zdz.py's meter on a gate-list file ('name = a * u + b * v', inputs x0, x1, ...); outputs found by matching rows of H.
import sys, re
sys.path.insert(0, '.')
import zdz
for path in sys.argv[1:]:
    gates = []
    for line in open(path):
        line = line.split('#')[0].strip()
        if '=' not in line: continue
        nm, rhs = line.split('=', 1); m = re.fullmatch(r'\s*(-?\d+) \* (\w+) \+ (-?\d+) \* (\w+)\s*', rhs)
        gates.append((nm.strip(), int(m.group(1)), m.group(2), int(m.group(3)), m.group(4), '1'))
    N = 1 + max(int(t[1:]) for g in gates for t in (g[2], g[4]) if re.fullmatch(r'x\d+', t))
    W = {'x%d' % i: [int(i == j) for j in range(N)] for i in range(N)}
    for (nm, a, u, b, v, tag) in gates: W[nm] = [a * p + b * q for p, q in zip(W[u], W[v])]
    y = {}
    for nm, w in W.items():
        for s in range(N):
            for c in (1, -1):
                if [c * t for t in w] == [(-1) ** zdz.pop(s & x) for x in range(N)]: y[s] = (c, nm)
    assert len(y) == N, 'not all rows of H are held'
    zdz.meter(path, N, gates, y, 16, 'verbose' in sys.argv)
