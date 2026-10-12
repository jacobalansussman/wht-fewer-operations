#!/usr/bin/env python3
"""check.py -- every number and every construction of the paper explicit-wht-circuits.tex, recomputed.

Written on 11 October 2026 for the paper, from the text of the paper (not from the programs of
tools/circuits).  Needs numpy and the folder tools/circuits of the repository (for the comparison with its
generator and its expected output).  Run it in the top folder of the repository:

    python3 -B paper/check.py 12 tools/circuits

The first argument is the largest k (N = 2^k points; default 12).  The second is the path to tools/circuits;
without it the program takes the environment variable WHT_CIRCUITS, or else the folder tools/circuits of the
repository that this file is in.

PART 1  the 19 lines at 8 points: every wire as eight coefficients; outputs = rows of H; the "centre" remark.
PART 2  the 20 operations that give H x / 2 (19 additions or subtractions, one halving).
PART 3  Theorem A: layers of the 20-operation circuit, replayed for k = 3..kmax (exact H x), counts, the table,
        and the comparison with tools/circuits/expected-output.txt.
PART 4  Theorem B: the construction exactly as the proof in the paper states it, k = 2..kmax: every line is
        checked against the identity the proof claims, outputs = rows of H, count = (3/4) N k + N/4; then the
        wires are compared with those of the generator tools/circuits/gen.py (same set of values, same count).
PART 5  thresholds quoted in the paper (Alman and Rao against the textbook; mine against both).
PART 6  the two older papers: every line of the count-(G) circuits is one multiply/add in the sense of
        Coppersmith, Feig and Linzer (1994); their 4-point circuit and their formulas; and the count stated by
        Grigoryan and Agaian (2000) beside the count of the recursion that their algorithm follows.
It is a Python check, not a proof.
"""
import sys, os, re, hashlib
import numpy as np

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12
# The folder tools/circuits of the repository: second argument, or the environment variable WHT_CIRCUITS,
# or the folder tools/circuits of the repository that this file is in (this file is paper/check.py there).
REL = sys.argv[2] if len(sys.argv) > 2 else os.environ.get(
    'WHT_CIRCUITS', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools', 'circuits'))
if not os.path.isdir(REL):
    sys.exit('check.py needs the folder tools/circuits of the repository; in the top folder of the repository run: python3 -B paper/check.py 12 tools/circuits')
OK = True


def bad(msg):
    global OK
    OK = False
    print('  FAILED: ' + msg)


def hadamard(k):
    H = np.array([[1]], dtype=np.int64)
    for _ in range(k):
        H = np.block([[H, H], [H, -H]])
    return H            # H[j][c] = (-1)^(common 1-bits of j and c): Sylvester order


def check_def(k):
    H = hadamard(k)
    N = 1 << k
    for j in range(N):
        for c in range(N):
            assert H[j, c] == (-1) ** bin(j & c).count('1')


for k in range(1, 7):
    check_def(k)

# ------------------------------------------------------------------ PART 1
print('PART 1.  The 19 lines at 8 points (count (G): one line a*u + b*v = one operation).')
G19 = """
g1 = x0 + x7
g2 = x1 + x6
g3 = x2 - x5
g4 = x3 - x4
g5 = g1 - g2
g6 = g3 + g4
g7 = g5 - g6
g8 = g7 - 2*x7
g9 = g7 - 2*x5
g10 = g8 + 2*x6
g11 = g9 - 2*x4
y7 = g10 + 2*g4
y1 = g10 + 2*g3
y6 = g11 + 2*g2
y0 = -g11 + 2*g1
y2 = g8 + 2*x1
y3 = g9 + 2*x3
y4 = y2 + 2*g6
y5 = -y3 + 2*g5
"""


def parse(text):
    lines = []
    for ln in text.strip().splitlines():
        name, rhs = [s.strip() for s in ln.split('=')]
        rhs = rhs.replace(' - ', ' + -')
        terms = []
        for t in rhs.split(' + '):
            t = t.strip()
            sign = 1
            if t.startswith('-'):
                sign, t = -1, t[1:]
            if '*' in t:
                c, w = t.split('*')
                num = c.split('/')
                c = float(num[0]) / float(num[1]) if len(num) == 2 else float(c)
            else:
                c, w = 1.0, t
            terms.append((sign * c, w))
        lines.append((name, terms))
    return lines


def run(lines, n):
    W = {'x%d' % i: np.eye(n)[i] for i in range(n)}
    for name, terms in lines:
        assert name not in W
        W[name] = sum(c * W[w] for c, w in terms)
    return W


L19 = parse(G19)
W = run(L19, 8)
H8 = hadamard(3)
assert len(L19) == 19 and all(len(t) == 2 for _, t in L19)
for j in range(8):
    if not np.array_equal(W['y%d' % j], H8[j]):
        bad('y%d is not row %d of H' % (j, j))
pat = lambda v: ' '.join('+' if e == 1 else '-' if e == -1 else '.' for e in v)
tex_rows = []
for name, terms in L19:
    v = W[name]
    assert set(np.unique(v)) <= {-1.0, 0.0, 1.0}
    print('  %-4s %s' % (name, pat(v)))
print('  19 lines, each with two terms; y0..y7 are rows 0..7 of H: %s' % ('yes' if OK else 'NO'))
print('  constants used: %s' % sorted(set(abs(c) for _, t in L19 for c, _ in t)))
print('  lines with a minus sign on the first term: %s' % [n for n, t in L19 if t[0][0] < 0])
print('  lines in which no operand has the constant +1: %s' % [n for n, t in L19 if all(c != 1 for c, _ in t)])
print('  priced line by line in count (O): %d additions or subtractions and %d doublings = %d' % (
    len(L19), sum(1 for _, t in L19 for c, _ in t if abs(c) != 1), len(L19) + sum(1 for _, t in L19 for c, _ in t if abs(c) != 1)))
c = W['g7']
print('  the centre g7 = %s ; it reads all eight inputs: %s' % (pat(c), bool(np.all(c != 0))))
print('  every output is  s*g7 + 2*(a sum of inputs with signs):')
for j in range(8):
    best = None
    for s in (1, -1):
        d = (W['y%d' % j] - s * c) / 2
        if best is None or np.count_nonzero(d) < np.count_nonzero(best[1]):
            best = (s, d)
    s, d = best
    assert set(np.unique(d)) <= {-1.0, 0.0, 1.0}
    print('    y%d = %sg7 + 2*( %s )   %d inputs' % (j, '+' if s > 0 else '-', pat(d), np.count_nonzero(d)))
print('  supports of the wires that are not outputs: %s' %
      [int(np.count_nonzero(W[n])) for n, _ in L19 if n.startswith('g')])

# ------------------------------------------------------------------ PART 2
print()
print('PART 2.  The same circuit with the centre halved once: H x / 2 in 20 operations of count (O).')
O20 = """
g1 = x0 + x7
g2 = x1 + x6
g3 = x2 - x5
g4 = x3 - x4
g5 = g1 - g2
g6 = g3 + g4
g7 = g5 - g6
h = 1/2*g7
h8 = h - x7
h9 = h - x5
h10 = h8 + x6
h11 = h9 - x4
z7 = h10 + g4
z1 = h10 + g3
z6 = h11 + g2
z0 = g1 - h11
z2 = h8 + x1
z3 = h9 + x3
z4 = z2 + g6
z5 = g5 - z3
"""
L20 = parse(O20)
W2 = run(L20, 8)
adds = sum(1 for _, t in L20 if len(t) == 2 and t[0][0] == 1 and t[1][0] == 1)
subs = sum(1 for _, t in L20 if len(t) == 2 and t[0][0] == 1 and t[1][0] == -1)
muls = sum(1 for _, t in L20 if len(t) == 1)
assert adds + subs + muls == len(L20) == 20
for j in range(8):
    if not np.array_equal(2 * W2['z%d' % j], H8[j]):
        bad('z%d is not half of row %d' % (j, j))
print('  20 lines: %d additions u+v, %d subtractions u-v, %d multiplication (by 1/2); no other kind of line.' % (adds, subs, muls))
print('  z0..z7 are rows 0..7 of H divided by 2: %s' % ('yes' if OK else 'NO'))
# the same 20 operations as the file of tools/circuits that the Lean data file is written from
rel = open(os.path.join(REL, 'programs', 'h8_half_20ops.txt')).read()
rel_lines = parse('\n'.join(l for l in rel.splitlines() if l.strip() and not l.startswith('#') and not re.match(r'^y\d+ = g\d+$', l.strip())))
Wr = run(rel_lines, 8)
mine = sorted(tuple(W2[n]) for n, _ in L20)
theirs = sorted(tuple(Wr[n]) for n, _ in rel_lines)
print('  the 20 values are the 20 values of tools/circuits/programs/h8_half_20ops.txt: %s' % (mine == theirs))
if mine != theirs:
    bad('20-operation program differs from tools/circuits/programs/h8_half_20ops.txt')

# ------------------------------------------------------------------ PART 3
print()
print('PART 3.  Theorem A.  m layers of the 20-operation circuit on three address bits each, r = k - 3m textbook')
print('layers, then N multiplications by 2^m.  Replayed on the identity matrix (so on every unit vector), k = 3..%d.' % KMAX)


def unit8(x):
    """x: list of 8 arrays.  Returns (list of 8 arrays = (1/2) H8 x, number of operations)."""
    g1 = x[0] + x[7]; g2 = x[1] + x[6]; g3 = x[2] - x[5]; g4 = x[3] - x[4]
    g5 = g1 - g2; g6 = g3 + g4; g7 = g5 - g6
    h = 0.5 * g7
    h8 = h - x[7]; h9 = h - x[5]; h10 = h8 + x[6]; h11 = h9 - x[4]
    z7 = h10 + g4; z1 = h10 + g3; z6 = h11 + g2; z0 = g1 - h11
    z2 = h8 + x[1]; z3 = h9 + x[3]; z4 = z2 + g6; z5 = g5 - z3
    return [z0, z1, z2, z3, z4, z5, z6, z7], 20


def layered(k):
    N = 1 << k
    m, r = divmod(k, 3)
    X = np.eye(N)
    ops = 0
    pos = 0
    for _ in range(m):                       # the 20-operation circuit on bits pos, pos+1, pos+2
        lo, hi = 1 << pos, N >> (pos + 3)
        Y = X.reshape(hi, 8, lo, N)
        out, c = unit8([Y[:, u] for u in range(8)])
        ops += c * hi * lo
        X = np.stack(out, axis=1).reshape(N, N)
        pos += 3
    for _ in range(r):                       # a textbook layer on bit pos
        lo, hi = 1 << pos, N >> (pos + 1)
        Y = X.reshape(hi, 2, lo, N)
        a, b = Y[:, 0] + Y[:, 1], Y[:, 0] - Y[:, 1]
        ops += 2 * hi * lo
        X = np.stack([a, b], axis=1).reshape(N, N)
        pos += 1
    before = ops
    X = X * float(1 << m)                    # N multiplications
    ops += N
    return X, before, ops


def AR_exact(k):
    N = 1 << k
    v = 23 * N * k + N * (k % 3) + 24 * (N - 1)
    assert v % 24 == 0
    return v // 24


def mine_O(k):
    N = 1 << k
    m, r = divmod(k, 3)
    return 20 * m * N // 8 + r * N + N


exp = open(os.path.join(REL, 'expected-output.txt')).read()
expO = {}
blk = exp.split('TABLE (O).')[1].split('Below the textbook')[0]
for ln in blk.splitlines():
    f = ln.split()
    if len(f) > 6 and f[0].isdigit():
        expO[int(f[0])] = (int(f[2]), float(f[3]), float(f[4]), int(f[5]))
expG = {}
blk = exp.split('TABLE (G).')[1].split('The family is below')[0]
for ln in blk.splitlines():
    f = ln.split()
    if len(f) > 6 and f[0].isdigit():
        expG[int(f[0])] = (int(f[2]), int(f[3]), int(f[4]), int(f[5]))

print('   k      N  textbook  Alman-Rao  this paper  5/6 N k + lin  replay   expected-output.txt')
tableA = []
for k in range(3, KMAX + 1):
    N = 1 << k
    X, before, ops = layered(k)
    m, r = divmod(k, 3)
    good = np.array_equal(X, hadamard(k))
    lin = {0: N, 1: 7 * N // 6 if (7 * N) % 6 == 0 else None, 2: 4 * N // 3 if (4 * N) % 3 == 0 else None}[r]
    f = 5 * N * k / 6 + N * (1 + r / 6)
    same = (ops == mine_O(k) == round(f)) and abs(f - round(f)) < 1e-9
    e = expO.get(k)
    agree = e is not None and e[0] == N * k and int(e[2]) == AR_exact(k) and e[3] == min(N * k, ops)
    if not (good and same and agree):
        bad('Theorem A at k=%d' % k)
    tableA.append((k, N, N * k, AR_exact(k), ops))
    ratios = globals().setdefault('ratios', [])
    ratios.append('%d: %.3f' % (N, ops / (N * k)))
    print('  %2d %6d %9d %10d %11d %14.1f  %s   %s' % (k, N, N * k, AR_exact(k), ops, f, 'H x exact' if good else 'WRONG', 'agrees' if agree else 'DIFFERS'))
for j in range(1, 8):
    N = 8 ** j
    assert mine_O(3 * j) == 20 * j * 8 ** (j - 1) + 8 ** j and 6 * mine_O(3 * j) == 5 * N * 3 * j + 6 * N
print('  ratio of this paper to the textbook (the last column of the table in the paper): ' + ', '.join(ratios))
print('  for N = 8^j, j = 1..7: the count is 20 j 8^(j-1) + 8^j = (5/6) N log2 N + N.')
print('  at 512 points: %d against the textbook %d; ratio %.4f' % (mine_O(9), 512 * 9, mine_O(9) / (512 * 9)))

# ------------------------------------------------------------------ PART 4
print()
print('PART 4.  Theorem B.  The construction as stated in the proof, k = 2..%d (count (G)).' % KMAX)


class Fam:
    """Wires are int8 vectors of length N.  piece[(lo, m, a)] = wire index of the piece (block lo..lo+m-1, a)."""

    def __init__(self, k):
        self.k, self.N = k, 1 << k
        self.H = {}
        self.vec = []
        self.piece = {}
        self.gates = 0
        self.noplus = 0          # lines in which no operand has the constant +1  (-u + 2v or 2u - v)
        self.plain = 0           # lines +-u +- v
        self.doubling = 0        # lines +-u +- 2v: one multiplication by a constant
        self.notma = 0           # lines that are neither (there must be none)
        self.maxabs = 0
        self.consts = set()
        for i in range(self.N):
            v = np.zeros(self.N, dtype=np.int8)
            v[i] = 1
            self.vec.append(v)
            self.piece[(i, 1, 0)] = i

    def target(self, lo, m, a):
        """The piece (block, a) from its definition: sum over t < m of (-1)^(common bits of a and t) x_(lo+t)."""
        j = m.bit_length() - 1
        if j not in self.H:
            self.H[j] = hadamard(j).astype(np.int8)
        v = np.zeros(self.N, dtype=np.int8)
        v[lo:lo + m] = self.H[j][a]
        return v

    def gate(self, a, u, b, v):
        w = a * self.vec[u].astype(np.int16) + b * self.vec[v].astype(np.int16)
        self.maxabs = max(self.maxabs, int(np.abs(w).max()))
        self.consts.add(abs(a)); self.consts.add(abs(b))
        if a != 1 and b != 1:
            self.noplus += 1
        shape = sorted((abs(a), abs(b)))
        if shape == [1, 1]:
            self.plain += 1
        elif shape == [1, 2]:
            self.doubling += 1
        else:
            self.notma += 1
        self.vec.append(w.astype(np.int8))
        self.gates += 1
        return len(self.vec) - 1

    def want(self, w, lo, m, a):
        if not np.array_equal(self.vec[w], self.target(lo, m, a)):
            raise AssertionError('piece (%d,%d,%d) wrong' % (lo, m, a))
        assert (lo, m, a) not in self.piece
        self.piece[(lo, m, a)] = w

    def E(self, lo, m, s):
        """Makes the pieces (block, a) with a < m/2 (s = +1) or a >= m/2 (s = -1)."""
        g0 = self.gates
        P = self.piece
        if m == 2:
            w = self.gate(1, P[(lo, 1, 0)], s, P[(lo + 1, 1, 0)])
            self.want(w, lo, 2, 0 if s > 0 else 1)
        else:
            h, q = m // 2, m // 4
            self.E(lo, h, 1)
            self.E(lo + h, h, -1)
            off = 0 if s > 0 else h
            for d in range(q):
                A, B = P[(lo, h, d)], P[(lo + h, h, d + q)]
                if 8 * d < m:                                   # d < m/8: quarter pieces on L0 and R0
                    M = self.gate(1, A, -s, B)                  # hub, c = -s
                    P1 = self.gate(1, M, 2 * s, P[(lo + h, q, d)])        # M + 2s q(R0)
                    P2 = self.gate(-1, M, 2, P[(lo, q, d)])               # -M + 2 q(L0)
                else:                                           # d >= m/8: quarter pieces on L1 and R1
                    M = self.gate(1, A, s, B)                   # hub, c = s
                    P1 = self.gate(1, M, 2 * s, P[(lo + h + q, q, d)])    # M + 2s q(R1)
                    P2 = self.gate(1, M, -2, P[(lo + q, q, d)])           # M - 2 q(L1)
                self.want(P1, lo, m, d + off)
                self.want(P2, lo, m, d + q + off)
        j = m.bit_length() - 1
        assert self.gates - g0 == m * (3 * j - 1) // 4 and (m * (3 * j - 1)) % 4 == 0      # E(m) = m (3 log2 m - 1)/4
        for a in range(m // 2):                                 # what E promises
            assert (lo, m, a + (0 if s > 0 else m // 2)) in P

    def top(self):
        N, P = self.N, self.piece
        h, q = N // 2, N // 4
        self.E(0, h, 1)
        self.E(h, h, -1)
        for d in range(q):
            A, B = P[(0, h, d)], P[(h, h, d + q)]
            M = self.gate(1, A, 1, B)                           # hub, c = +1
            if 8 * d < N:                                       # d < N/8: s = -1 first
                Pm = self.gate(1, M, -2, P[(h, q, d)])          # (N, d + N/2)       = M - 2 q(R0)
                Qm = self.gate(-1, M, 2, P[(0, q, d)])          # (N, d + N/4 + N/2) = -M + 2 q(L0)
                Pp = self.gate(2, A, -1, Pm)                    # (N, d)             = 2A - Pm
                Qp = self.gate(1, Qm, 2, B)                     # (N, d + N/4)       = Qm + 2B
            else:                                               # d >= N/8: s = +1 first
                Pp = self.gate(1, M, 2, P[(h + q, q, d)])       # (N, d)             = M + 2 q(R1)
                Qp = self.gate(1, M, -2, P[(q, q, d)])          # (N, d + N/4)       = M - 2 q(L1)
                Pm = self.gate(2, A, -1, Pp)                    # (N, d + N/2)       = 2A - Pp
                Qm = self.gate(1, Qp, -2, B)                    # (N, d + N/4 + N/2) = Qp - 2B
            self.want(Pp, 0, N, d)
            self.want(Qp, 0, N, d + q)
            self.want(Pm, 0, N, d + h)
            self.want(Qm, 0, N, d + q + h)
        return self


def digest(v):
    return hashlib.sha1(np.asarray(v, dtype=np.int8).tobytes()).hexdigest()


sys.path.insert(0, REL)
try:
    import gen as relgen
except Exception as e:                                           # the comparison is skipped, and said so
    relgen = None
    print('  (tools/circuits/gen.py not importable here: %s; the comparison column is skipped)' % e)

print('   k      N   gates  (3/4)Nk+N/4  outputs = rows of H  entries of all wires  constants  tools/circuits/gen.py     expected-output.txt')
famcounts = {}
for k in range(2, KMAX + 1):
    N = 1 << k
    F = Fam(k).top()
    Hk = hadamard(k).astype(np.int8)
    good = all(np.array_equal(F.vec[F.piece[(0, N, j)]], Hk[j]) for j in range(N))
    formula = (3 * N * k + N) // 4
    cnt = (F.gates == formula) and (3 * N * k + N) % 4 == 0
    famcounts[k] = F.gates
    famshape = globals().setdefault('famshape', {})
    famshape[k] = (F.plain, F.doubling, F.notma)
    if k <= 5:
        noplus_txt = getattr(sys.modules[__name__], 'noplus_txt', '') + '  N=%d: %d of %d;' % (N, F.noplus, F.gates)
    cmp_txt = 'skipped'
    if relgen is not None:
        lines, fac = relgen.family(k, 'G')
        R = {'x%d' % i: F.vec[i] for i in range(N)}
        rg = 0
        rel_d = set()
        for name, terms in lines:
            if len(terms) == 1 and terms[0][0] == 1:
                R[name] = R[terms[0][1]]
                continue
            assert len(terms) == 2
            w = sum(int(c) * R[u].astype(np.int16) for c, u in terms)
            R[name] = w.astype(np.int8)
            rel_d.add(digest(R[name]))
            rg += 1
        my_d = set(digest(F.vec[i]) for i in range(N, len(F.vec)))
        same = (rg == F.gates) and (rel_d == my_d) and all(np.array_equal(R['y%d' % j], Hk[j]) for j in range(N))
        cmp_txt = 'same values, same count' if same else 'DIFFERS'
        if not same:
            bad('family differs from tools/circuits/gen.py at k=%d' % k)
    e = expG.get(k)
    agree = e is not None and e[3] == F.gates
    if not (good and cnt and agree):
        bad('Theorem B at k=%d' % k)
    print('  %2d %6d %7d %12d  %-19s  within -%d..%d %10s  %-4s %-24s %s' % (
        k, N, F.gates, formula, 'yes' if good else 'NO', F.maxabs, F.maxabs, '', sorted(F.consts), cmp_txt, 'agrees' if agree else 'DIFFERS'))
    del F
print('  Every line was compared, when made, with the piece that the proof says it is (Fam.want).')
print('  lines of the family in which no operand has the constant +1 (-u + 2v or 2u - v):' + noplus_txt)

# ------------------------------------------------------------------ PART 5
print()
print('PART 5.  Thresholds and small facts quoted in the paper.')
first = next(k for k in range(3, 200) if all(AR_exact(kk) < (1 << kk) * kk for kk in range(k, k + 30)))
print('  Alman and Rao, exact count (23/24)Nk + (N/24)(k mod 3) + N - 1: below the textbook at every k >= %d; at k = %d by %d operation(s).' % (first, first, (1 << first) * first - AR_exact(first)))
assert all(AR_exact(k) >= (1 << k) * k for k in range(1, first))
firstb = next(k for k in range(3, 200) if all(23 * kk / 24 + 13 / 12 < kk for kk in range(k, k + 30)))
print('  Alman and Rao, stated bound (23/24)Nk + (13/12)N: below the textbook at every k >= %d.' % firstb)
below = [k for k in range(1, 200) if k >= 3 and mine_O(k) < (1 << k) * k]
print('  this paper, count (O): below the textbook exactly for k >= %d (checked to k = 199); equal at k = 6, 7, 8: %s; above at k = 3, 4, 5: %s' % (
    below[0], all(mine_O(k) == (1 << k) * k for k in (6, 7, 8)), all(mine_O(k) > (1 << k) * k for k in (3, 4, 5))))
assert below == list(range(9, 200))
assert all(AR_exact(k) - mine_O(k) == 3 * (k // 3) * (1 << k) // 8 - 1 for k in range(3, 200))
print('  Alman and Rao exact count minus this paper = (3/8) m N - 1 with m = floor(k/3), for k = 3..199: positive.')
print('  count (G) family against the textbook and the 7/8 count (even k: (7/8)Nk; odd k: (7/8)Nk + N/8, which is (7/8)N(k-1) + N):')
for k in range(2, KMAX + 1):
    N = 1 << k
    p78 = 7 * N * k // 8 if k % 2 == 0 else 7 * N * (k - 1) // 8 + N
    assert 8 * p78 == 7 * N * k + (N if k % 2 else 0)          # the two formulas of Coppersmith, Feig and Linzer
    e = expG[k]
    assert e[0] == N * k and e[1] == p78 and e[3] == famcounts[k]
    lay = e[2]
    print('    k=%2d N=%5d textbook %6d  7/8 count %6d  layers of small circuits %6d  family %6d' % (k, N, N * k, p78, lay, famcounts[k]))
m19 = [(k, 19 * (k // 3) * (1 << k) // 8) for k in (3, 6, 9, 12)]
print('  layers of the 19-line circuit alone, 3 | k: %s  = (19/24) N k' % m19)
print('  lower bound 2N - 1 of the paper: 7 at 4 points, 15 at 8, 31 at 16.')

# ------------------------------------------------------------------ PART 6
print()
print('PART 6.  The two older papers.')
print('  (a) Coppersmith, Feig and Linzer (1994).  One operation there is  +-a +- b*c  (a multiply/add), or a plain')
print('      addition, or a plain multiplication.  So a line  +-u +- v  or  +-u +- 2v  is one operation there, and a')
print('      line with a constant other than +-1 on both operands would not be.')
shape19 = [sorted(abs(c) for c, _ in t) for _, t in L19]
if not all(len(t) == 2 for _, t in L19) or not all(sh in ([1.0, 1.0], [1.0, 2.0]) for sh in shape19):
    bad('a line of the 19 is not one multiply/add')
print('      the 19 lines at 8 points: %d lines +-u +- v, %d lines +-u +- 2v, %d other lines' % (
    shape19.count([1.0, 1.0]), shape19.count([1.0, 2.0]), len(shape19) - shape19.count([1.0, 1.0]) - shape19.count([1.0, 2.0])))
if any(v[2] for v in famshape.values()):
    bad('a line of the family is not one multiply/add')
print('      the family of Theorem B, every line tested when it is made:')
for k in range(2, KMAX + 1):
    pl, db, other = famshape[k]
    assert pl + db + other == famcounts[k]
    if k <= 6 or k == KMAX:
        print('        N=%5d: %6d lines +-u +- v, %6d lines +-u +- 2v, %d other lines' % (1 << k, pl, db, other))
print('      their 4-point circuit (page 969), 7 operations:')
CFL4 = """
z0 = x1 + x2
z1 = z0 + x3
z2 = x0 - z1
y0 = x0 + z1
y1 = z2 + 2*x2
y2 = z2 + 2*x1
y3 = z2 + 2*x3
"""
LC = parse(CFL4)
WC = run(LC, 4)
H4 = hadamard(2)
shapeC = [sorted(abs(c) for c, _ in t) for _, t in LC]
okC = all(np.array_equal(WC['y%d' % j], H4[j]) for j in range(4))
if not okC or len(LC) != 7:
    bad('the 4-point circuit of the 1994 paper')
print('        y0..y3 are rows 0..3 of H: %s; %d lines +-u +- v and %d lines +-u +- 2v' % (
    'yes' if okC else 'NO', shapeC.count([1.0, 1.0]), shapeC.count([1.0, 2.0])))
near = [int(np.count_nonzero(WC['z2'] != H4[j])) for j in range(4)]
print('        the value z2 = x0 - x1 - x2 - x3 differs from the rows 0..3 of H in %s places' % near)
print('        the family at 4 points: %d lines +-u +- v and %d lines +-u +- 2v' % famshape[2][:2])
if famshape[2] != (3, 4, 0) or (shapeC.count([1.0, 1.0]), shapeC.count([1.0, 2.0])) != (4, 3) or near != [3, 1, 1, 1]:
    bad('the comparison of the two 4-point circuits is not as the paper says')
cfl = lambda k: (7 * (1 << k) * k + ((1 << k) if k % 2 else 0)) // 8
print('      their formulas, (7/8) n log2 n for a power of four and n/8 more for an odd power of two: ' +
      ', '.join('%d at %d' % (cfl(k), 1 << k) for k in range(2, 7)))
assert [cfl(k) for k in range(2, 7)] == [7, 22, 56, 144, 336]
assert cfl(3) == 8 + 2 * 7                    # one textbook layer and two 4-point circuits
print('      this paper against them: 19 against %d at 8 points, %d against %d at 16; rate 3/4 against 7/8.' % (cfl(3), famcounts[4], cfl(4)))
if not (19 < cfl(3) and famcounts[4] < cfl(4) and all(famcounts[k] < cfl(k) for k in range(3, KMAX + 1)) and famcounts[2] == cfl(2)):
    bad('comparison with the 1994 formulas')

print('  (b) Grigoryan and Agaian (2000).  Stated count for N = 2^r points (page 181): 6*2^r - r^2 - 3r - 6 additions and')
print('      subtractions.  Their algorithm: a paired transform of length N, 2N - 2 additions and subtractions, then the')
print('      transforms of lengths N/2, N/4, ..., 2, 1, computed the same way.  So its count obeys')
print('      T(N) = (2N - 2) + T(N/2) + T(N/4) + ... + T(1), T(1) = 0.')
T = [0]
for r in range(1, 41):
    T.append(2 * 2 ** r - 2 + sum(T))
stated = lambda r: 6 * 2 ** r - r * r - 3 * r - 6
if not all(T[r] == r * 2 ** r for r in range(41)):
    bad('the recursion is not N log2 N')
print('      T(N) = N log2 N exactly, for r = 1..40: %s' % all(T[r] == r * 2 ** r for r in range(41)))


# The same count, taken stage by stage from the loops of the program that the paper prints on page 181: stage I
# (I = 1..r) applies the paired transform to the blocks of length L = N / 2^(I-1) that start at the positions
# 1, 1 + 2L, 1 + 4L, ... up to N.  That is one block of length N, one of length N/2, two of length N/4, four of
# length N/8, and so on; each costs 2L - 2.
def by_stages(r):
    N = 2 ** r
    return sum(len(range(1, N + 1, 2 * (N >> (I - 1)))) * (2 * (N >> (I - 1)) - 2) for I in range(1, r + 1))


if not all(by_stages(r) == T[r] for r in range(1, 41)):
    bad('the count by stages differs from the recursion')
print('      the same count stage by stage (one paired transform of length N, one of length N/2, two of length N/4,')
print('      four of length N/8, ..., as in the loops of the program on page 181), for r = 1..40: %s' % all(
    by_stages(r) == T[r] for r in range(1, 41)))
print('       r       N   stated count   recursion T(N)   N log2 N   (N/2) log2 N')
for r in range(1, 15):
    N = 2 ** r
    note = ''
    if stated(r) < T[r]:
        note = '   stated count below N log2 N'
    if 2 * stated(r) < N * r:
        note = '   stated count below (N/2) log2 N'
    print('      %2d %7d %14d %16d %10d %14d%s' % (r, N, stated(r), T[r], N * r, N * r // 2, note))
first_below = next(r for r in range(1, 41) if stated(r) < T[r])
first_below_half = next(r for r in range(1, 41) if 2 * stated(r) < 2 ** r * r)
print('      the stated count equals N log2 N at 2, 4 and 8 points: %s' % all(stated(r) == T[r] for r in (1, 2, 3)))
print('      it is first below N log2 N at %d points (%d against %d), and below it at every larger size to 2^40: %s' % (
    2 ** first_below, stated(first_below), T[first_below], all(stated(r) < T[r] for r in range(first_below, 41))))
print('      it is first below (N/2) log2 N at %d points (%d against %d), and below it at every larger size to 2^40: %s' % (
    2 ** first_below_half, stated(first_below_half), 2 ** first_below_half * first_below_half // 2,
    all(2 * stated(r) < 2 ** r * r for r in range(first_below_half, 41))))
if not (first_below == 4 and first_below_half == 12 and stated(4) == 62 and stated(12) == 24390
        and all(stated(r) == T[r] for r in (1, 2, 3))
        and all(stated(r) < T[r] for r in range(4, 41)) and all(2 * stated(r) < 2 ** r * r for r in range(12, 41))):
    bad('the numbers on the count of the 2000 paper')

print()
print('ALL CHECKS PASSED.' if OK else 'SOME CHECK FAILED.')
sys.exit(0 if OK else 1)
