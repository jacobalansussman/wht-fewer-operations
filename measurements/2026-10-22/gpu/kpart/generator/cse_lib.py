"""cse_lib.py -- shared pieces for ax-13 (wave 16).

* parse_et_header(path): the K x K +-1 matrices exactly as executorch ships them in
  extension/llm/custom_ops/spinquant/fast_hadamard_transform_special.h (out[i] = +- x[j] ... lines).
* greedy(M, rng): Paar-style greedy signed-pair common-subexpression elimination (cancellation-free).
  Signs are handled inside the pair (t = x_u + s x_v), so the circuit computes M itself, not a
  sign-changed copy.  Returns (adds, defs, rows); defs = [(t, u, v, s)], rows[i] = {var: coef}.
* check_exact(M, defs, rows): exact integer check on all unit vectors and 50 random integer vectors.
* depth(defs, rows): depth when each output's final sum is a balanced tree.
"""
import re, random

def parse_et_header(path):
    src = open(path).read()
    mats = {}
    for m in re.finditer(r'void hadamard_mult_(\d+)_strided\(T\* input, int stride\) \{(.*?)\n\}', src, re.S):
        K = int(m.group(1)); body = m.group(2)
        M = [[0] * K for _ in range(K)]
        for i, expr in re.findall(r'out\[(\d+)\] = (.*?);', body):
            for sg, j in re.findall(r'([+-]) x\[(\d+)\]', expr):
                M[int(i)][int(j)] = 1 if sg == '+' else -1
        assert all(all(v != 0 for v in r) for r in M), K
        mats[K] = M
    return mats

def greedy(M, rng, pick='max'):
    K = len(M[0]); R = len(M)
    rows = [{j: M[i][j] for j in range(K) if M[i][j]} for i in range(R)]
    nvar = K; defs = []
    while True:
        cnt = {}
        for r in rows:
            ks = sorted(r)
            for a in range(len(ks)):
                ra = r[ks[a]]
                for b in range(a + 1, len(ks)):
                    key = (ks[a], ks[b], ra * r[ks[b]])
                    cnt[key] = cnt.get(key, 0) + 1
        if not cnt: break
        best = max(cnt.values())
        if best < 2: break
        cands = [k for k, c in cnt.items() if c == best]
        u, v, s = rng.choice(cands)
        t = nvar; nvar += 1; defs.append((t, u, v, s))
        for r in rows:
            if u in r and v in r and r[u] * r[v] == s:
                c = r[u]; del r[u]; del r[v]; r[t] = c
    adds = len(defs) + sum(len(r) - 1 for r in rows)
    return adds, defs, rows

def evaluate(defs, rows, x):
    val = dict(enumerate(x))
    for t, u, v, s in defs: val[t] = val[u] + s * val[v]
    return [sum(c * val[w] for w, c in r.items()) for r in rows]

def check_exact(M, defs, rows, rng=None):
    rng = rng or random.Random(7)
    K = len(M[0])
    vecs = [[1 if j == i else 0 for j in range(K)] for i in range(K)]
    vecs += [[rng.randint(-10**6, 10**6) for _ in range(K)] for _ in range(50)]
    for x in vecs:
        got = evaluate(defs, rows, x)
        want = [sum(M[i][j] * x[j] for j in range(K)) for i in range(len(M))]
        if got != want: return False
    return True

def depth(defs, rows):
    d = {}
    def dep(w): return d.get(w, 0)
    for t, u, v, s in defs: d[t] = max(dep(u), dep(v)) + 1
    worst = 0
    for r in rows:
        ds = sorted(dep(w) for w in r)
        # balanced combination: repeatedly join the two shallowest
        import heapq
        h = list(ds); heapq.heapify(h)
        while len(h) > 1:
            a = heapq.heappop(h); b = heapq.heappop(h); heapq.heappush(h, max(a, b) + 1)
        worst = max(worst, h[0] if h else 0)
    return worst

def best_greedy(M, tries, seed=1):
    rng = random.Random(seed); best = None
    for _ in range(tries):
        a, defs, rows = greedy(M, rng)
        if best is None or a < best[0]: best = (a, defs, rows)
    return best
