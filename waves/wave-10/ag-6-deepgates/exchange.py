# exchange.py : for every 8-point circuit with a deep gate printed by the walker: take out its tall wires one at a time and ask
# whether ONE other wire in its place gives a circuit of the same size in which every gate has coefficients 1 and 2 and no
# division (whole numbers throughout).  "yes" = the deep gate was a way of writing two shallow gates; "no" = the tall wire does
# something there that no single wire with shallow gates does.
import sys, re, math, itertools
sys.path.insert(0, '.')
def prim(v):
    g = 0
    for x in v: g = math.gcd(g, abs(x))
    if not g: return None
    s = next(x for x in v if x); s = 1 if s > 0 else -1
    return tuple(s * x // g for x in v)
def kind(u, v, w):
    n = len(u)
    for i in range(n):
        if not u[i] and not v[i]: continue
        for j in range(i + 1, n):
            D = u[i] * v[j] - u[j] * v[i]
            if D:
                a = w[i] * v[j] - w[j] * v[i]; b = u[i] * w[j] - u[j] * w[i]
                if any(D * w[l] != a * u[l] + b * v[l] for l in range(n)): return None
                if not a or not b: return None
                g0 = math.gcd(math.gcd(abs(a), abs(b)), abs(D)); return (abs(a) // g0, abs(b) // g0, abs(D) // g0)
    return None
ok12 = lambda k: k is not None and k[0] in (1, 2) and k[1] in (1, 2) and k[2] == 1
def valid(wires, N):
    have = [tuple(1 if i == j else 0 for j in range(N)) for i in range(N)]; todo = [w for w in wires if w not in have]; ch = True
    while ch and todo:
        ch = False
        for w in list(todo):
            if any(ok12(kind(u, v, w)) for u, v in itertools.combinations(have, 2)): have.append(w); todo.remove(w); ch = True
    return not todo
N = 8; ins = [tuple(1 if i == j else 0 for j in range(N)) for i in range(N)]
res = {}
for fn in sys.argv[1:]:
    cur = None; circs = []
    for line in open(fn, errors='ignore'):
        if line.startswith('CIRCUIT'):
            m = re.search(r'N=(\d+) gates=(\d+)', line); cur = {'N': int(m.group(1)), 'g': int(m.group(2)), 'w': [], 'k': []}; circs.append(cur)
        elif cur is not None and line.startswith('w') and '# [' in line:
            cur['w'].append(prim(tuple(int(x) for x in line.split('# [')[1].split(']')[0].split()))); cur['k'].append(re.search(r'kind \((\d+),(\d+)\)/(\d+)', line).groups())
        elif line.startswith('SUMMARY'): cur = None
    for c in circs:
        if c['N'] != 8 or len(c['w']) != c['g']: continue
        if not any(int(a) % 4 == 0 or int(b) % 4 == 0 for a, b, g in c['k']): continue
        wires = c['w']; tall = [w for w in wires if max(abs(x) for x in w) > 1]
        outs = [w for w in wires if 0 not in w and max(abs(x) for x in w) == 1]
        verdict = 'no'
        if valid([w for w in wires if w not in tall], N): verdict = 'the tall wire can simply be dropped'
        else:
            for t in tall:
                rest = [w for w in wires if w != t]; pool = ins + rest; cand = set()
                for u, v in itertools.combinations(pool, 2):
                    for a, b in ((1, 1), (1, -1), (1, 2), (1, -2), (2, 1), (2, -1)):
                        e = tuple(a * x + b * y for x, y in zip(u, v))
                        if any(e) and math.gcd(*[abs(x) for x in e]) == 1:
                            e = prim(e)
                            if e not in pool and max(abs(x) for x in e) == 1: cand.add(e)
                for e in cand:
                    if valid(rest + [e], N): verdict = 'yes: one form in its place'; break
                if verdict != 'no': break
        key = (c['g'], len(tall), verdict); res[key] = res.get(key, 0) + 1
for k in sorted(res): print('%d gates, %d tall wire(s): exchange for one form with shallow gates only: %s  -- %d circuits' % (k[0], k[1], k[2], res[k]))
