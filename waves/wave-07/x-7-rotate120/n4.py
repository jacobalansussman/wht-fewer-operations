# x-7-rotate120 / n4.py : every pair of mirrors of the 4-point rotation R = D H / 2, over GF(p), priced with d-0-zeta/mincirc.
# usage: n4.py p [maxm]
# Definitions: H = 4-point transform with the two bits exchanged in the output address, D = diag((-1)^(x1 x2)), R = D H / 2.
# A "mirror" here is S with S^2 = 1 and S R S = R^-1.  The pair is (S, S R); the third mirror is S R^2.
# Count (G): cost(S) = least number of gates a*u+b*v that produce every row of S up to scale (mincirc, exhaustive over GF(p)).
import sys, itertools, subprocess, os, collections
p = int(sys.argv[1]); maxm = int(sys.argv[2]) if len(sys.argv) > 2 else 6
HERE = os.path.dirname(os.path.abspath(__file__))
MC = os.path.join(HERE, '..', 'd-0-zeta', 'mincirc')
N = 4
def pop(v): return bin(v).count('1')
def Q(x): return (x & 1) * ((x >> 1) & 1)
def sw(x): return ((x & 1) << 1) | ((x >> 1) & 1)
H = [[(-1) ** pop(x & sw(y)) for y in range(N)] for x in range(N)]
D = [(-1) ** Q(x) for x in range(N)]
inv2 = pow(2, p - 2, p)
def mul(A, B): return [[sum(A[i][t] * B[t][j] for t in range(N)) % p for j in range(N)] for i in range(N)]
I4 = [[int(i == j) for j in range(N)] for i in range(N)]
R = [[D[x] * H[x][y] * inv2 % p for y in range(N)] for x in range(N)]
R2 = mul(R, R); R3 = mul(R2, R)
assert R3 == I4, 'R^3 != 1'
Rinv = R2
# linear space L = {X : X R = R^-1 X}
rows = []
for i in range(N):
    for j in range(N):
        # (X R)[i][j] - (Rinv X)[i][j] = sum_t X[i][t] R[t][j] - sum_t Rinv[i][t] X[t][j]
        r = [0] * 16
        for t in range(N):
            r[i * 4 + t] = (r[i * 4 + t] + R[t][j]) % p
            r[t * 4 + j] = (r[t * 4 + j] - Rinv[i][t]) % p
        rows.append(r)
def nullspace(M, n):
    M = [r[:] for r in M]; piv = []; rr = 0
    for c in range(n):
        s = next((i for i in range(rr, len(M)) if M[i][c] % p), None)
        if s is None: continue
        M[rr], M[s] = M[s], M[rr]
        iv = pow(M[rr][c], p - 2, p); M[rr] = [x * iv % p for x in M[rr]]
        for i in range(len(M)):
            if i != rr and M[i][c]:
                f = M[i][c]; M[i] = [(a - f * b) % p for a, b in zip(M[i], M[rr])]
        piv.append(c); rr += 1
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = [0] * n; v[f] = 1
        for i, c in enumerate(piv): v[c] = (-M[i][f]) % p
        basis.append(v)
    return basis
B = nullspace(rows, 16)
print('p=%d: dimension of {X : X R = R^-1 X} = %d (expected 6 = 2^2 + 2*1^2)' % (p, len(B)))
mirrors = []
for co in itertools.product(range(p), repeat=len(B)):
    v = [sum(c * b[i] for c, b in zip(co, B)) % p for i in range(16)]
    X = [v[0:4], v[4:8], v[8:12], v[12:16]]
    if mul(X, X) == I4: mirrors.append(X)
print('mirrors (S^2 = 1, S R S = R^-1) over GF(%d): %d' % (p, len(mirrors)))
Dm = [[(D[i] % p) if i == j else 0 for j in range(N)] for i in range(N)]
assert Dm in mirrors
# check starting fact (i): S R is again a mirror and (S)(S R) = R
for S in mirrors:
    S2 = mul(S, R); assert mul(S2, S2) == I4 and mul(S, S2) == R and mul(mul(S2, R), S2) == Rinv
print('fact (i) checked on all of them: S R is an involution, S * (S R) = R, and S R inverts R too')
def canon_row(r):
    nz = next((x for x in r if x), None)
    if nz is None: return None
    iv = pow(nz, p - 2, p); return tuple(x * iv % p for x in r)
cache = {}
def cost(X):
    key = frozenset(canon_row(r) for r in X)
    if key in cache: return cache[key]
    txt = '\n'.join(' '.join(map(str, r)) for r in X) + '\n'
    c = None
    for m in range(0, maxm + 1):
        out = subprocess.run([MC, str(p), '4', str(m)], input=txt, capture_output=True, text=True).stdout
        t = int(out.split('non-input distinct targets=')[1].split()[0])
        if 'YES' in out: c = t + m; break
        if t == 0: c = 0; break
    cache[key] = c; return c
def tr(X): return sum(X[i][i] for i in range(N)) % p
def nnz(X): return sum(1 for r in X for x in r if x)
tri = collections.Counter(); pairmin = {}; ex = {}
for S in mirrors:
    c = (cost(S), cost(mul(S, R)), cost(mul(S, R2)))
    key = tuple(sorted(c)); tri[key] += 1
    ex.setdefault(key, S)
print('cost triples (cost S, cost S R, cost S R^2), sorted, with how many mirrors S have them, and one example S (rows), its trace mod p and non-zeros:')
for key in sorted(tri, key=lambda t: (t[0] + t[1], t)):
    S = ex[key]
    print('  triple %s  two cheapest sum to %d  count %d   example %s  trace %d  nnz %d / S R nnz %d / S R^2 nnz %d' % (key, key[0] + key[1], tri[key], S, tr(S), nnz(S), nnz(mul(S, R)), nnz(mul(S, R2))))
best = min(k[0] + k[1] for k in tri)
print('least cost(S) + cost(S R) over all pairs, GF(%d): %d   (the trivial pair D, H/2 gives 0 + 7)' % (p, best))
print('pairs by (cost S, cost S R) unsorted:')
pc = collections.Counter()
for S in mirrors: pc[(cost(S), cost(mul(S, R)))] += 1
for k in sorted(pc): print('  ', k, pc[k])
print('distinct matrices priced:', len(cache))
