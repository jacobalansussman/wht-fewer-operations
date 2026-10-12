#!/usr/bin/env python3
"""wsolve.py (ag-8-bestbadcircuit): FIX THE WIRING of a circuit for the N-point transform, put another kernel in, decide whether
coefficients exist.  Count (G): a gate is any a*u + b*v, scalings free, so a wire is a point up to scale and a gate (u, v) -> g
says only "g lies in the span of u and v".
Kernel K_tau = [[1,1],[1,tau]] (every 2 x 2 kernel without a zero entry is this one after row and column scalings, tau = ps/(qr)
for rows (p,q),(r,s); the transform is tau = -1).  Target row w, column x: tau^(common ones of w and x).
Method (linear propagation of subspaces, modulo a large prime P at a random tau): every wire carries a subspace known to contain it;
inputs and outputs are known points; for a gate g = (u, v):  S_g <= S_u + S_v,  S_u <= S_g + S_v,  S_v <= S_g + S_u.  Iterate to a
fixpoint.  If some subspace becomes 0: NO coefficients exist (this is a proof modulo P at that tau, since the rules are necessary).
If every wire ends as one point and every gate is a true gate: YES (then confirmed exactly, in fractions, at rational tau by exact()).
If some subspace keeps dimension >= 2: UNDECIDED by this method (reported as such).
A FRAME renames inputs and outputs: the gate that made H-row w must make K-row rho(w), and input x_j is column sigma(j)."""
import sys, re, random, itertools
from fractions import Fraction as F
P = (1 << 61) - 1
MODE = {'q': False}
def _inv(x): return 1 / F(x) if MODE['q'] else pow(x % P, -1, P)
def _red(x): return x if MODE['q'] else x % P

def parse(path):
    """returns N, gates [(name,u,v)] in file order, exact integer vectors by replay."""
    lines = [l.split('#')[0].strip() for l in open(path)]
    lines = [l for l in lines if '=' in l]
    names = set(re.findall(r'x(\d+)', ' '.join(lines))); N = max(int(n) for n in names) + 1
    val = {'x%d' % i: tuple(F(int(i == j)) for j in range(N)) for i in range(N)}
    gates = []
    for l in lines:
        nm, ex = [s.strip() for s in l.split('=')]
        ids = re.findall(r'[A-Za-z_]+\d*', ex)
        assert len(ids) == 2, l
        # evaluate: replace names by placeholders
        toks = re.sub(r'\s+', '', ex).replace('+-', '-').replace('--', '+')
        m = re.fullmatch(r'([+-]?[\d/]*)\*?([A-Za-z_]+\d*)([+-][\d/]*)\*?([A-Za-z_]+\d*)', toks)
        assert m, l
        def co(s): return F(1) if s in ('', '+') else F(-1) if s == '-' else F(s)
        a, u, b, v = co(m.group(1)), m.group(2), co(m.group(3)), m.group(4)
        val[nm] = tuple(a * s + b * t for s, t in zip(val[u], val[v])); gates.append((nm, u, v))
    return N, gates, val

def hrow(w, N): return tuple((-1) ** bin(w & x).count('1') for x in range(N))
def outputs(N, gates, val):
    """gate name -> H-row index it is proportional to (first gate for each row)."""
    out = {}; seen = set()
    for nm, u, v in gates:
        vec = val[nm]
        for w in range(N):
            if w in seen: continue
            r = hrow(w, N); i0 = next(i for i in range(N) if r[i])
            if vec[i0] != 0 and all(vec[i] * r[i0] == r[i] * vec[i0] for i in range(N)): out[nm] = w; seen.add(w); break
    return out

# ---------- linear algebra modulo P ----------
def rref(rows, mod=P):
    M = [list(r) for r in rows]; r = 0; n = len(M[0]) if M else 0
    for c in range(n):
        pv = next((i for i in range(r, len(M)) if _red(M[i][c])), None)
        if pv is None: continue
        M[r], M[pv] = M[pv], M[r]; iv = _inv(M[r][c]); M[r] = [_red(x * iv) for x in M[r]]
        for i in range(len(M)):
            if i != r and _red(M[i][c]):
                f = M[i][c]; M[i] = [_red(a - f * b) for a, b in zip(M[i], M[r])]
        r += 1
        if r == len(M): break
    return [tuple(x) for x in M[:r]]
def ssum(U, W): return rref(list(U) + list(W))
def sint(U, W):
    """intersection of row spaces U, W (lists of rref rows)."""
    if not U or not W: return []
    n = len(U[0]); A = [list(u) for u in U] + [[_red(-x) for x in w] for w in W]
    m = len(A); M = [A[i] + [int(i == j) for j in range(m)] for i in range(m)]; r = 0
    for c in range(n):
        pv = next((i for i in range(r, m) if _red(M[i][c])), None)
        if pv is None: continue
        M[r], M[pv] = M[pv], M[r]; iv = _inv(M[r][c])
        for i in range(r + 1, m):
            if _red(M[i][c]):
                f = _red(M[i][c] * iv); M[i] = [_red(a - f * b) for a, b in zip(M[i], M[r])]
        r += 1
    res = []
    for i in range(r, m):
        c = M[i][n:]; v = [0] * n
        for j in range(len(U)):
            if c[j]: v = [_red(a + c[j] * b) for a, b in zip(v, U[j])]
        res.append(v)
    return rref(res) if res else []

def krow(w, N, tau, sigma, mod=P):
    if MODE['q']: return tuple(F(tau) ** bin(w & sigma[x]).count('1') for x in range(N))
    return tuple(pow(tau, bin(w & sigma[x]).count('1'), P) for x in range(N))

def solve(N, gates, out, tau, sigma=None, rho=None, verbose=False, fixed=None):
    """returns ('YES', points) | ('NO', gate) | ('UNDECIDED', dims)."""
    sigma = sigma or list(range(N)); rho = rho or list(range(N))
    S = {'x%d' % i: [tuple(int(i == j) for j in range(N))] for i in range(N)}
    for nm, w in out.items(): S[nm] = rref([krow(rho[w], N, tau, sigma)])
    for nm, u, v in gates:
        if nm not in S: S[nm] = None           # None = nothing known yet
    for nm, pt in (fixed or {}).items(): S[nm] = rref([pt])
    readers = {}
    changed = True; rounds = 0
    while changed:
        changed = False; rounds += 1
        for nm, u, v in gates:
            for tgt, a, b in ((nm, u, v), (u, nm, v), (v, nm, u)):
                if tgt.startswith('x'): continue
                if S[a] is None or S[b] is None: continue
                if S[tgt] is not None and len(S[tgt]) == 1 and len(S[a]) == 1 and len(S[b]) == 1:
                    # all three known: check dependence
                    if len(rref([S[tgt][0], S[a][0], S[b][0]])) > 2: return ('NO', nm)
                    continue
                bound = ssum(S[a], S[b])
                new = bound if S[tgt] is None else sint(S[tgt], bound)
                if not new: return ('NO', nm)
                if S[tgt] is None or len(new) < len(S[tgt]): S[tgt] = new; changed = True
    dims = {nm: (None if S[nm] is None else len(S[nm])) for nm, u, v in gates}
    if any(d != 1 for d in dims.values()): return ('UNDECIDED', {k: d for k, d in dims.items() if d != 1}, S)
    # every gate must be a true gate: g in span(u,v); also flag degenerate (g proportional to an operand, or u ~ v)
    deg = []
    for nm, u, v in gates:
        if len(rref([S[nm][0], S[u][0], S[v][0]])) > 2: return ('NO', nm)
        if len(rref([S[nm][0], S[u][0]])) < 2 or len(rref([S[nm][0], S[v][0]])) < 2 or len(rref([S[u][0], S[v][0]])) < 2: deg.append(nm)
    return ('YES' if not deg else 'YES-DEGENERATE', {'pts': {k: S[k][0] for k in S}, 'deg': deg})

def solve_branch(N, gates, out, tau, sigma=None, rho=None, depth=2, fixed=None):
    """solve, and where the linear propagation stalls on a wire known to lie on a LINE, try every point of that line (P must be a
    small prime).  Returns 'YES', 'NO' or 'UNDECIDED' (a stall on a subspace of dimension >= 3, or deeper than `depth`)."""
    r = solve(N, gates, out, tau, sigma, rho, fixed=fixed)
    if r[0] != 'UNDECIDED': return 'YES' if r[0] == 'YES' else 'NO'
    if depth == 0: return 'UNDECIDED'
    S = r[2]; cand = [k for k, d in r[1].items() if d == 2]
    if not cand: return 'UNDECIDED'
    k = cand[0]; u, v = S[k]; res = 'NO'
    for t in range(P + 1):
        pt = tuple((a + t * b) % P for a, b in zip(u, v)) if t < P else v
        f = dict(fixed or {}); f[k] = pt
        q = solve_branch(N, gates, out, tau, sigma, rho, depth - 1, f)
        if q == 'YES': return 'YES'
        if q == 'UNDECIDED': res = 'UNDECIDED'
    return res

def exact(N, gates, out, tau, sigma=None, rho=None):
    """the same propagation in exact fractions at a rational tau. Returns 'YES' / 'NO' / 'UNDECIDED' / 'YES-DEGENERATE'."""
    MODE['q'] = True
    try: r = solve(N, gates, out, F(tau), sigma, rho)
    finally: MODE['q'] = False
    return r[0]

def frames(N):
    k = N.bit_length() - 1
    if N == 4:
        for s in itertools.permutations(range(4)):
            for r in itertools.permutations(range(4)): yield list(s), list(r)
        return
    # all (A, b, c): inputs x -> A x + b, outputs w -> A^-T w + c  (the 2^k * |AGL(k,2)| frames that keep H up to signs)
    def mats():
        def rec(rows):
            if len(rows) == k: yield rows; return
            span = {0}
            for r in rows: span |= {s ^ r for s in span}
            for r in range(1, N):
                if r not in span: yield from rec(rows + [r])
        yield from rec([])
    def app(rows, x): return sum(((bin(rows[i] & x).count('1') & 1) << i) for i in range(k))
    for A in mats():
        img = [app(A, x) for x in range(N)]
        # A^-T: w -> the w' with w'.(A x) = w.x for all x
        inv = [0] * N
        for x in range(N): inv[img[x]] = x
        # (A^-T w).y = w.(A^-1 y): build rows of A^-T
        AT = [None] * N
        for w in range(N):
            wp = 0
            for i in range(k):
                y = 1 << i
                if bin(w & inv[y]).count('1') & 1: wp |= y
            AT[w] = wp
        for b in range(N):
            sig = [img[x] ^ b for x in range(N)]
            for c in range(N): yield sig, [AT[w] ^ c for w in range(N)]

if __name__ == '__main__':
    path = sys.argv[1]; mode = sys.argv[2] if len(sys.argv) > 2 else 'id'
    random.seed(8)
    N, gates, val = parse(path); out = outputs(N, gates, val)
    assert len(out) == N, ('outputs found', len(out))
    print('%s: N=%d gates=%d outputs=%d helpers=%d' % (path.split('/')[-1], N, len(gates), len(out), len(gates) - len(out)))
    # control: tau = -1 must say YES with the identity frame
    print('  control tau=-1, identity frame:', solve(N, gates, out, P - 1)[0])
    taus = [random.randrange(2, P - 2) for _ in range(2)]
    if mode == 'id':
        for t in taus:
            r = solve(N, gates, out, t); print('  random tau modulo 2^61-1, identity frame:', r[0], r[1] if r[0] != 'YES' and r[0] != 'YES-DEGENERATE' else '')
        for t in (3, F(5, 7), -2):
            print('  exact fractions, tau = %s, identity frame: %s' % (t, exact(N, gates, out, t)))
    else:
        n = 0; yes = []; und = 0
        for sig, rho in frames(N):
            n += 1
            r = solve(N, gates, out, taus[0], sig, rho)
            if r[0] == 'YES': yes.append((sig, rho))
            elif r[0] != 'NO': und += 1
        print('  frames tried: %d   YES: %d   undecided/degenerate: %d' % (n, len(yes), und))
        for sig, rho in yes[:3]:
            print('   e.g. inputs', sig, 'outputs', rho, '| second random tau:', solve(N, gates, out, taus[1], sig, rho)[0],
                  '| exact tau=3:', exact(N, gates, out, 3, sig, rho), ' tau=5/7:', exact(N, gates, out, F(5, 7), sig, rho))
