"""cse.py -- how many additions do the non-power-of-two Hadamard blocks (12, 20, 28, 40) used by
LLM rotation kernels really need?  Dense (what Dao's fast-hadamard-transform and executorch's special
kernels write: K(K-1) adds) against a greedy signed-pair common-subexpression circuit (Paar-style),
best over random tie-breaks and random row/column sign choices (H stays a Hadamard matrix of the same
class; a column sign = an input sign folded into the previous op / the weights, a row sign = an output
sign folded into the next op).  Every circuit is checked exactly on random integer vectors.
Usage: cse.py PATH_TO_code_gen.py [tries]"""
import re, sys, random
src = open(sys.argv[1]).read()
tries = int(sys.argv[2]) if len(sys.argv) > 2 else 200
mats = {}
for name, body in re.findall(r'(had_\w+)\s*=\s*"""(.*?)"""', src, re.S):
    rows = [r.strip() for r in body.strip().splitlines() if r.strip()]
    mats[name] = [[1 if ch == '+' else -1 for ch in r] for r in rows]

def greedy(M, rng):
    K = len(M)
    rows = [{j: M[i][j] for j in range(K)} for i in range(K)]   # var -> coef (+-1)
    nvar = K; defs = []
    while True:
        cnt = {}
        for r in rows:
            ks = sorted(r)
            for a in range(len(ks)):
                for b in range(a + 1, len(ks)):
                    u, v = ks[a], ks[b]; s = r[u] * r[v]
                    cnt[(u, v, s)] = cnt.get((u, v, s), 0) + 1
        if not cnt: break
        best = max(cnt.values())
        if best < 2: break
        cands = [k for k, c in cnt.items() if c == best]
        u, v, s = rng.choice(cands)
        t = nvar; nvar += 1; defs.append((t, u, v, s))          # t = x_u + s*x_v
        for r in rows:
            if u in r and v in r and r[u] * r[v] == s:
                c = r[u]; del r[u]; del r[v]; r[t] = c
    ops = len(defs) + sum(len(r) - 1 for r in rows)
    return ops, defs, rows

def check(M, defs, rows, rng):
    K = len(M)
    for _ in range(20):
        x = [rng.randint(-1000, 1000) for _ in range(K)]
        val = dict(enumerate(x))
        for t, u, v, s in defs: val[t] = val[u] + s * val[v]
        for i in range(K):
            got = sum(c * val[w] for w, c in rows[i].items())
            want = sum(M[i][j] * x[j] for j in range(K))
            if got != want: return False
    return True

rng = random.Random(1)
print('| matrix | K | dense adds K(K-1) | greedy CSE adds (best of %d) | adds per point dense -> CSE | checked |' % tries)
print('|---|---|---|---|---|---|')
for name, M in mats.items():
    K = len(M)
    if any(len(r) != K for r in M): continue
    best = None
    for t in range(tries):
        rs = [rng.choice((1, -1)) for _ in range(K)] if t else [1] * K
        cs = [rng.choice((1, -1)) for _ in range(K)] if t else [1] * K
        Ms = [[M[i][j] * rs[i] * cs[j] for j in range(K)] for i in range(K)]
        ops, defs, rows = greedy(Ms, rng)
        if best is None or ops < best[0]: best = (ops, Ms, defs, rows)
    ok = check(best[1], best[2], best[3], rng)
    print('| %s | %d | %d | %d | %.1f -> %.2f | %s |' % (name, K, K * (K - 1), best[0], K - 1, best[0] / K, 'exact' if ok else 'FAIL'))
