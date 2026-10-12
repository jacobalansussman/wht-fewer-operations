# reassoc.py : every circuit with a deep gate printed by the walker tj at 8 points: the anatomy of the deep gate, and the test of
# the reassociation lemma  (c + 2 e') + 4 v = c + 2 (e' + 2 v):  replace the tall parent u = c + 2 e' by the wire e = e' + 2 v
# and check, in whole numbers, that the result is a circuit of the same size in which every gate has coefficients 1 and 2.
import sys, re, math, itertools
from fractions import Fraction
def prim(v):
    g = 0
    for x in v: g = math.gcd(g, abs(x))
    if not g: return None
    s = next(x for x in v if x); s = 1 if s > 0 else -1
    return tuple(s * x // g for x in v)
def kind(u, v, w):
    # g*w = a*u + b*v ; returns (|a|,|b|,g) reduced, or None
    n = len(u)
    for i in range(n):
        for j in range(i + 1, n):
            D = u[i] * v[j] - u[j] * v[i]
            if D:
                a = w[i] * v[j] - w[j] * v[i]; b = u[i] * w[j] - u[j] * w[i]
                if any(D * w[l] != a * u[l] + b * v[l] for l in range(n)): return None
                if not a or not b: return None
                g0 = math.gcd(math.gcd(abs(a), abs(b)), abs(D)); return (abs(a) // g0, abs(b) // g0, abs(D) // g0)
    return None
def valid(wires, N, allowed):
    # can every wire be derived, in some order, from the inputs by gates whose kind is allowed?
    have = [tuple(1 if i == j else 0 for j in range(N)) for i in range(N)]; todo = [w for w in wires if w not in have]; ch = True
    while ch and todo:
        ch = False
        for w in list(todo):
            if any((k := kind(u, v, w)) and allowed(k) for u, v in itertools.combinations(have, 2)):
                have.append(w); todo.remove(w); ch = True
    return not todo
ok12 = lambda k: k[0] in (1, 2) and k[1] in (1, 2) and k[2] == 1
tot = 0; good = 0; tallused = 0; shapes = {}
for fn in sys.argv[1:]:
    cur = None; circs = []
    for line in open(fn, errors='ignore'):
        if line.startswith('CIRCUIT'):
            m = re.search(r'N=(\d+) gates=(\d+)', line); cur = {'N': int(m.group(1)), 'g': int(m.group(2)), 'w': [], 'l': []}; circs.append(cur)
        elif cur is not None and line.startswith('w') and '# [' in line:
            cur['w'].append(tuple(int(x) for x in line.split('# [')[1].split(']')[0].split())); cur['l'].append(line)
        elif line.startswith('SUMMARY'): cur = None
    for c in circs:
        N = c['N']
        if N != 8 or len(c['w']) != c['g']: continue
        name = {}; ins = [tuple(1 if i == j else 0 for j in range(N)) for i in range(N)]
        for i, x in enumerate(ins): name['x%d' % i] = x
        deep = []
        for w, l in zip(c['w'], c['l']):
            m = re.match(r'(w\d+) = (-?\d+)\*(\w+) \+ (-?\d+)\*(\w+)', l)
            if not m: name[l.split(' =')[0]] = prim(w); continue      # a gate with a division (kind (1,1)/2): never deep here
            name[m.group(1)] = prim(w); a, b = int(m.group(2)), int(m.group(4))
            if abs(a) % 4 == 0 or abs(b) % 4 == 0: deep.append((m.group(1), a, m.group(3), b, m.group(5)))
        if not deep: continue
        tot += 1; wires = [prim(w) for w in c['w']]
        (wn, a, p, b, q) = deep[0]
        # the parent with coefficient +-1 is u (tall), the other is v
        un, vn = (p, q) if abs(a) == 1 else (q, p); u, v, w = name[un], name[vn], name[wn]
        users = sum(1 for l in c['l'] if re.search(r'\*%s\b' % un, l)) ; hu = max(abs(x) for x in u)
        mu = re.match(r'(w\d+) = (-?\d+)\*(\w+) \+ (-?\d+)\*(\w+)', next(l for l in c['l'] if l.startswith(un + ' =')))
        ua, up, ub, uq = int(mu.group(2)), mu.group(3), int(mu.group(4)), mu.group(5)
        shape = 'deep wire height %d (an output: %s); tall parent u height %d, used by %d gate(s), made by coefficients (%d,%d); v height %d' % (max(abs(x) for x in w), max(abs(x) for x in w) == 1 and 0 not in w, hu, users, abs(ua), abs(ub), max(abs(x) for x in v))
        shapes[shape] = shapes.get(shape, 0) + 1
        if users > 1: tallused += 1
        # reassociate: u = s1*c + 2*s2*e' ; w = +-u +- 4 v = +-(c + 2 e),  e = (w -+ c)/2
        cn, en = (up, uq) if abs(ua) == 1 else (uq, up); cc = name[cn]; done = False
        for sg in (1, -1):
            e2 = tuple(x - sg * y for x, y in zip(w, cc))
            if all(x % 2 == 0 for x in e2):
                e = prim(tuple(x // 2 for x in e2))
                if e is None: continue
                new = [x for x in wires if x != u] + ([e] if e not in wires and e not in ins else [])
                if valid(new, N, ok12) and len(new) <= len(wires):
                    good += 1; done = True
                    if good <= 2: print('example %s %d gates: deep gate %s = %d*%s + %d*%s ; u = %s = %d*%s + %d*%s ; e = %s ; circuit with u replaced by e: %d gates, coefficients 1 and 2 only' % (fn.split('/')[-1], c['g'], wn, a, p, b, q, u, ua, up, ub, uq, e, len(new)))
                    break
        if not done: print('NOT reassociated:', fn, wn)
print('circuits with a deep gate: %d ; reassociated into a circuit with coefficients 1 and 2 of the same or smaller size: %d ; tall parent used by more than the deep gate: %d' % (tot, good, tallused))
for s, n in shapes.items(): print('  %d x %s' % (n, s))
