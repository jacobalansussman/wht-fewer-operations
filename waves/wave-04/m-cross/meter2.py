# m-cross: the 2-adic meter.  For every circuit file of tonight that replays as a Walsh-Hadamard transform:
# normalise each wire to be primitive at the prime 2 (entries with odd denominators, not all even), then
#   class of a wire = the wire modulo 2 (a 0/1 vector);
#   gate kind by its two parents u, v and result w:  J = three different classes,  S = w has the class of a parent,
#       Q = parents have one class and w another,  E = all three equal;
#   'new' = the class of w is not the class of any earlier wire (inputs included)  -> survivor;  otherwise 'dead';
#   order = largest m (up to 6) with  w == unit * p  modulo 2^m  for some earlier wire p;
#   over-limit = (non-zeros in the inputs) * (non-zeros in the outputs) > N.
import sys, re, glob, os
from fractions import Fraction as F
def val2(q):
    if q == 0: return 10**9
    n, d, v = q.numerator, q.denominator, 0
    while n % 2 == 0: n //= 2; v += 1
    while d % 2 == 0: d //= 2; v -= 1
    return v
def prim(w):
    m = min(val2(a) for a in w)
    if m > 10**8: return None
    return [a / F(2)**m for a in w]
def modv(w, m):
    M = 2**m
    return tuple((a.numerator * pow(a.denominator, -1, M)) % M for a in w)
def canon(w, m):
    M = 2**m; r = modv(w, m)
    lead = next(a for a in r if a % 2 == 1); inv = pow(lead, -1, M)
    return tuple((a * inv) % M for a in r)
pat = re.compile(r'([+-]?[\d/]*)\*?([A-Za-z_]\w*?)\+?([+-][\d/]*|[\d/]*)\*?([A-Za-z_]\w*)$')
def coef(s):
    if s in ('', '+'): return F(1)
    if s == '-': return F(-1)
    return F(s)
def parse(path):
    gates = []
    for line in open(path, errors='replace'):
        line = line.split('#')[0].strip()
        if '=' not in line: continue
        name, rhs = line.split('=', 1)
        name = name.strip(); rhs = rhs.replace(' ', '')
        if not re.fullmatch(r'[A-Za-z_]\w*', name): return None
        m = re.fullmatch(r'([+-]?[\d/]*)\*?([A-Za-z_]\w*)(\+-|\+|-)([\d/]*)\*?([A-Za-z_]\w*)', rhs)
        if not m: return None
        a = coef(m.group(1)); b = coef(m.group(4)) * (-1 if '-' in m.group(3) else 1)
        gates.append((name, a, m.group(2), b, m.group(5)))
    return gates
def had(N):
    return [[(-1)**bin(y & x).count('1') for x in range(N)] for y in range(N)]
def meter(label, gates, N):
    k = N.bit_length() - 1; H = had(N)
    W = {'x%d' % i: [F(int(i == j)) for j in range(N)] for i in range(N)}
    order_sets = {m: set() for m in range(1, 7)}
    for i in range(N):
        for m in range(1, 7): order_sets[m].add(canon(W['x%d' % i], m))
    kinds = dict(J=0, S=0, Q=0, E=0); new = 0; dead = 0; hist = {}; V = 0; so = 0
    rows = {}
    for (name, a, u, b, v) in gates:
        if u not in W or v not in W: return None
        w = [a * p + b * q for p, q in zip(W[u], W[v])]
        pw = prim(w)
        if pw is None: return None
        cu, cv, cw = canon(prim(W[u]), 1), canon(prim(W[v]), 1), canon(pw, 1)
        kd = 'E' if cu == cv == cw else 'Q' if cu == cv else 'S' if cw in (cu, cv) else 'J'
        kinds[kd] += 1
        o = 0
        for m in range(1, 7):
            if canon(pw, m) in order_sets[m]: o = m
            else: break
        if o == 0: new += 1
        else: dead += 1; hist[o] = hist.get(o, 0) + 1; so += o
        for m in range(1, 7): order_sets[m].add(canon(pw, m))
        s = sum(1 for t in w if t != 0)
        hw = [sum(H[y][x] * w[x] for x in range(N)) for y in range(N)]
        s2 = sum(1 for t in hw if t != 0)
        if s * s2 > N: V += 1
        W[name] = w
        if s == N:
            for y in range(N):
                if all(w[x] * H[y][0] == w[0] * H[y][x] for x in range(N)): rows[y] = name
    if len(rows) != N: return None
    G = len(gates)
    print('%-58s N=%3d gates=%4d  J/S/Q/E=%d/%d/%d/%d  new=%d dead=%d orders=%s sum=%d  overlimit=%d | gates+V-NlogN=%d  new+V-(N/2)logN=%d  dead-(N/2)logN=%d  new-(N-1)=%d'
          % (label[-58:], N, G, kinds['J'], kinds['S'], kinds['Q'], kinds['E'], new, dead, sorted(hist.items()), so, V, G + V - N * k, new + V - N * k // 2, dead - N * k // 2, new - (N - 1)))
    return True
def textbook(N):
    g = []; cur = ['x%d' % i for i in range(N)]; h = 1; c = 0
    while h < N:
        nxt = list(cur)
        for i in range(N):
            if not i & h:
                c += 1; a = 't%d' % c; c += 1; b = 't%d' % c
                g.append((a, F(1), cur[i], F(1), cur[i | h])); g.append((b, F(1), cur[i], F(-1), cur[i | h]))
                nxt[i] = a; nxt[i | h] = b
        cur = nxt; h *= 2
    return g
for N in (4, 8, 16, 32): meter('textbook', textbook(N), N)
seen = 0
for path in sorted(glob.glob(sys.argv[1] + '/*/*.txt')):
    if os.path.getsize(path) > 60000: continue
    try: g = parse(path)
    except Exception: g = None
    if not g or len(g) < 5 or len(g) > 400: continue
    xs = [int(t[1:]) for (_, _, u, _, v) in g for t in (u, v) if re.fullmatch(r'x\d+', t)]
    if not xs: continue
    N = max(xs) + 1
    if N & (N - 1) or N > 64: continue
    try:
        if meter(path.replace(sys.argv[1] + '/', ''), g, N): seen += 1
    except Exception as e: pass
print('circuits metered:', seen)
