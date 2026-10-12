#!/usr/bin/env python3
"""build16.py [ad-3]  16 points, exact fractions.  Build ONE product of two exchanges as a circuit and price it, count (G).
Checks, all exact:
 (1) the dictionary: for an exchange (u, T) of the outputs, Phi = H P H / N = I - 2 diag([u.x = 1]) Pi_T, where Pi_T is the
     convolution whose spectrum is the indicator of T; on the half u.x = 1 it is the reflection with spectrum -1 on T.
 (2) a path  start (hyperplane minus line) -> middle class -> quadric  with two single-flat exchanges, found by search;
 (3) the circuit  Phi2 Phi1 C_start Phi1 Phi2  replayed gate by gate on the 16 unit inputs: it equals the convolution with the
     quadric's signs, and that matrix times 4 is the transform up to signs of rows and columns and a relabelling of columns.
A gate is any a*u + b*v; scalings, signs and relabellings are free."""
from fractions import Fraction as F
from itertools import combinations
k = 4; N = 16
def dot(x, y): return bin(x & y).count("1") & 1
H = [[1 - 2 * dot(x, y) for y in range(N)] for x in range(N)]
def conv_from_spectrum(s):            # C[s] = H diag(s) H / N
    return [[sum(F(H[x][y] * s[y] * H[y][z]) for y in range(N)) / N for z in range(N)] for x in range(N)]
def mul(A, B): return [[sum(A[i][l] * B[l][j] for l in range(N)) for j in range(N)] for i in range(N)]
def is_flat(S):
    S = sorted(S); n = len(S)
    if n & (n - 1) or n == 0: return False
    a = S[0]; st = set(S)
    return all((x ^ y ^ a) in st for x in S for y in S)
flats = [frozenset(c) for d in (2, 4, 8) for c in combinations(range(N), d) if is_flat(c)]
def exchange(A, u, T): return frozenset((y ^ u) if y in T else y for y in A)
def bent(A):
    return all(abs(sum((-1 if y in A else 1) * H[a][y] for y in range(N))) == 4 for a in range(N))
# ---- (1) the dictionary, on every single-flat exchange
bad = 0; cnt = 0
for u in range(1, N):
    for T in flats:
        if frozenset(y ^ u for y in T) != T: continue
        P = [[0] * N for _ in range(N)]
        for y in range(N): P[(y ^ u) if y in T else y][y] = 1
        Phi = [[F(sum(H[x][a] * P[a][b] * H[b][z] for a in range(N) for b in range(N)), N) for z in range(N)] for x in range(N)]
        Pi = conv_from_spectrum([1 if y in T else 0 for y in range(N)])
        Phi2 = [[(1 if x == z else 0) - 2 * dot(u, x) * Pi[x][z] for z in range(N)] for x in range(N)]
        cnt += 1; bad += Phi != Phi2
        # on the half u.x = 0 it is the identity; the two halves do not mix
        bad += any(Phi[x][z] != (1 if x == z else 0) for x in range(N) if not dot(u, x) for z in range(N))
        bad += any(Phi[x][z] != 0 for x in range(N) if dot(u, x) for z in range(N) if not dot(u, z))
print("(1) Phi = H P H / N = I - 2 diag([u.x=1]) Pi_T, identity on the half u.x=0, halves not mixed: %d exchanges checked, %d failures" % (cnt, bad))
# ---- (2) a path
G0 = frozenset(y for y in range(N) if y & 1 == 0); W = frozenset([0, 2]); A0 = G0 - W
def cost_exch(T):                       # cosets of V-perp in the half: 2^(d-1) of them, each a reflection on m = N/|T| points
    m = N // len(T); return (len(T) // 2) * (0 if m == 2 else 2 * m - 1)
best = None
for u1 in range(1, N):
    for T1 in flats:
        if len(T1) == 8 or frozenset(y ^ u1 for y in T1) != T1: continue
        A1 = exchange(A0, u1, T1)
        for u2 in range(1, N):
            for T2 in flats:
                if len(T2) == 8 or frozenset(y ^ u2 for y in T2) != T2: continue
                A2 = exchange(A1, u2, T2)
                if bent(A2):
                    c = cost_exch(T1) + cost_exch(T2)
                    if best is None or c < best[0]: best = (c, u1, T1, u2, T2, A1, A2)
c, u1, T1, u2, T2, A1, A2 = best
print("(2) start %s\n    exchange 1: u=%d on T=%s -> %s\n    exchange 2: u=%d on T=%s -> %s  (bent: %s)" % (
    sorted(A0), u1, sorted(T1), sorted(A1), u2, sorted(T2), sorted(A2), bent(A2)))
# ---- (3) the circuit
class Circuit:
    def __init__(self):
        self.gates = 0
        self.w = [[F(1 if i == j else 0) for j in range(N)] for i in range(N)]   # wire at address x = a row vector over inputs
    def gate(self, a, p, b, q):
        self.gates += 1; return [a * p[i] + b * q[i] for i in range(N)]
    def scale(self, a, p): return [a * v for v in p]
    def exch(self, u, T):
        """Phi = I - 2 diag([u.x=1]) Pi_T for a flat T = a + V unchanged by u.  Pi_T g (x) = (|V|/N) sum_{w in Vperp} (-1)^(a.w) g(x+w)."""
        a = min(T); V = [y ^ a for y in T]; Vp = [x for x in range(N) if all(dot(x, v) == 0 for v in V)]
        m = len(Vp); done = set(); new = list(self.w)
        for x0 in range(N):
            if not dot(u, x0) or x0 in done: continue
            coset = [x0 ^ w for w in Vp]; done.update(coset)
            sg = {x0 ^ w: F(1 - 2 * dot(a, w)) for w in Vp}            # sign of g(x0+w) in the sum seen from x0
            if m == 2:                                                # g(x) - (g(x) + s g(x')) = -s g(x'): a signed swap, free
                x, y = coset; s = sg[y]; new[x] = self.scale(-s, self.w[y]); new[y] = self.scale(-s, self.w[x]); continue
            acc = self.gate(sg[coset[0]], self.w[coset[0]], sg[coset[1]], self.w[coset[1]])
            for x in coset[2:]: acc = self.gate(F(1), acc, sg[x], self.w[x])
            for x in coset:                                           # seen from x the sum is sg[x] * acc
                new[x] = self.gate(F(1), self.w[x], -F(2, m) * sg[x], acc)
        self.w = new
    def conv_start(self, G0, W):
        """C = I - 2 Pi_G0 + 2 Pi_W for the pattern -1 on G0 minus W (flats)."""
        new = []
        # Pi_G0: Vperp = {0, v}
        a = min(G0); V = [y ^ a for y in G0]; v = [x for x in range(1, N) if all(dot(x, t) == 0 for t in V)][0]
        aw = min(W); VW = [y ^ aw for y in W]; Vp = [x for x in range(N) if all(dot(x, t) == 0 for t in VW)]; m = len(Vp)
        sums = {}; done = set()
        for x0 in range(N):
            if x0 in done: continue
            coset = [x0 ^ w for w in Vp]; done.update(coset); sg = {x0 ^ w: F(1 - 2 * dot(aw, w)) for w in Vp}
            acc = self.gate(sg[coset[0]], self.w[coset[0]], sg[coset[1]], self.w[coset[1]])
            for x in coset[2:]: acc = self.gate(F(1), acc, sg[x], self.w[x])
            for x in coset: sums[x] = (sg[x], acc)
        for x in range(N):
            s = F(1 - 2 * dot(a, v))                                  # g(x) - (g(x) + s g(x+v)) = -s g(x+v)
            sx, acc = sums[x]
            new.append(self.gate(-s, self.w[x ^ v], F(2, m) * sx, acc))
        self.w = new
def phi_matrix(u, T):
    Pi = conv_from_spectrum([1 if y in T else 0 for y in range(N)])
    return [[(1 if x == z else 0) - 2 * dot(u, x) * Pi[x][z] for z in range(N)] for x in range(N)]
C = Circuit(); log = []
C.exch(u2, T2); log.append(C.gates)
C.exch(u1, T1); log.append(C.gates)
C.conv_start(G0, W); log.append(C.gates)
C.exch(u1, T1); log.append(C.gates)
C.exch(u2, T2); log.append(C.gates)
target = conv_from_spectrum([-1 if y in A2 else 1 for y in range(N)])
ok = C.w == target
Mx = [[4 * v for v in row] for row in target]
pm1 = all(v in (1, -1) for row in Mx for v in row)
# E[x][z] = M[x][z] M[x][0] M[0][z] M[0][0] must be (-1)^(x^T B z) with B invertible modulo 2
E = [[Mx[x][z] * Mx[x][0] * Mx[0][z] * Mx[0][0] for z in range(N)] for x in range(N)]
B = [[0 if E[1 << i][1 << j] == 1 else 1 for j in range(k)] for i in range(k)]
def bil(x, z): return sum(B[i][j] for i in range(k) for j in range(k) if x >> i & 1 and z >> j & 1) & 1
bilin = all(E[x][z] == 1 - 2 * bil(x, z) for x in range(N) for z in range(N))
rows = set(tuple(E[x]) for x in range(N))
print("(3) gates after each stage (Phi2, Phi1, C_start, Phi1, Phi2): %s ; total %d gates (G)" % (log, C.gates))
print("    circuit equals the convolution with the quadric's signs, all 256 entries: %s" % ok)
print("    4 x that matrix has entries +-1: %s ; it is (-1)^(q(x)+q(z)+B(x,z)) with B bilinear: %s ; B invertible (16 distinct rows): %s" % (pm1, bilin, len(rows) == N))
print("    so it is the 16-point transform up to free signs and one relabelling.  Textbook 64, night's best 52.")
print("    price law of this family: 2 x (sum over exchanges of the reflections on the half) + cost of the start;")
print("    a flat of dimension d costs 2^(d-1) reflections on N/2^d points, each 2m-1 gates (m = 2: free)")
for d in (1, 2, 3): print("      d=%d: %d gates per exchange per side" % (d, (1 << (d - 1)) * (0 if N >> d == 2 else 2 * (N >> d) - 1)))
