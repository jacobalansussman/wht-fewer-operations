# u-7-quotient, run C: Gaussian integers, exact (pairs of Python integers).  lam = 1 + i, 2 = -i lam^2.
#  C1. H S H = lam^k S^-1 H S^-1  and (H S)^3 = lam^k N,   S = diag(i^(number of ones of x))
#  C2. rows c_y of H S are product wires with factors (1, +-i).  (c_y - u c_y')/lam for the units u: when is it a wire with unit entries
#      (a 'complex hub'), and which real sign vectors are real parts of (1+-i) times such wires
#  C3. a step of half order: w - lam * (w restricted to a set D) = w with every entry on D multiplied by -i
import sys, itertools
N = int(sys.argv[1]); k = N.bit_length() - 1
def mul(a, b): return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])
def add(a, b): return (a[0] + b[0], a[1] + b[1])
I = [(1, 0), (0, 1), (-1, 0), (0, -1)]
lam = (1, 1)
def powg(a, n):
    r = (1, 0)
    for _ in range(n): r = mul(r, a)
    return r
def divlam(a):   # a / (1+i) = a (1-i)/2
    b = mul(a, (1, -1)); assert b[0] % 2 == 0 and b[1] % 2 == 0, a; return (b[0] // 2, b[1] // 2)
pc = lambda x: bin(x).count('1')
H = [[((-1)**pc(x & y), 0) for x in range(N)] for y in range(N)]
S = [I[pc(x) % 4] for x in range(N)]; Sinv = [I[(-pc(x)) % 4] for x in range(N)]
def matmul(A, B):
    n = len(A); C = [[(0, 0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = (0, 0)
            for t in range(n): s = add(s, mul(A[i][t], B[t][j]))
            C[i][j] = s
    return C
HS = [[mul(H[y][x], S[x]) for x in range(N)] for y in range(N)]
HSH = matmul(HS, H)
lk = powg(lam, k)
ok1 = all(HSH[y][x] == mul(lk, mul(Sinv[y], mul(H[y][x], Sinv[x]))) for y in range(N) for x in range(N))
T3 = matmul(matmul(HS, HS), HS)
ok2 = all(T3[y][x] == ((lk[0] * N, lk[1] * N) if x == y else (0, 0)) for y in range(N) for x in range(N))
print('N=%d  C1: H S H = lam^k S^-1 H S^-1: %s ;  (H S)^3 = lam^k N: %s' % (N, ok1, ok2))
# C2
unit = lambda a: a in I
hubs = {}; nres = 0
for y in range(N):
    for z in range(y):
        for u in I:
            d = [add(HS[y][x], mul((-u[0], -u[1]), HS[z][x])) for x in range(N)]
            try: q = [divlam(t) for t in d]
            except AssertionError: continue
            if all(unit(t) for t in q):
                nres += 1
                for c in ((1, 1), (1, -1)):
                    r = tuple(mul(c, t)[0] for t in q)
                    if all(abs(t) == 1 for t in r):
                        r = r if r[0] > 0 else tuple(-t for t in r)
                        hubs.setdefault(r, []).append((y, z, u, c))
Hn = {tuple(t[0] for t in H[y]) for y in range(N)}
print('  C2: (pair of rows of HS, unit u) with (c_y - u c_z)/lam a wire of unit entries: %d of %d' % (nres, N * (N - 1) // 2 * 4))
print('      distinct real sign vectors Re((1+-i) * that wire): %d ; of them outputs: %d' % (len(hubs), sum(1 for r in hubs if r in Hn or tuple(-t for t in r) in Hn)))
# direct: real parts of (1+-i) c_y
direct = set()
for y in range(N):
    for c in ((1, 1), (1, -1)):
        r = tuple(mul(c, t)[0] for t in HS[y]); r = r if r[0] > 0 else tuple(-t for t in r); direct.add(r)
print('      real parts of (1+-i) times a row of HS itself: %d sign vectors ; quotient hubs among them: %d' % (len(direct), len(set(hubs) & direct)))
if N == 8:
    for name, v in (('g7 centre', (1, -1, -1, -1, 1, 1, -1, 1)), ('g10', None), ('g11', None)):
        if v: print('      the 19: %s in quotient set: %s ; in direct set: %s' % (name, v in hubs, v in direct))
# distance of each such real hub from the outputs
def dist(r, h): return sum(1 for a, b in zip(r, h) if a != b)
prof = {}
for r in hubs:
    p = tuple(sorted(min(dist(r, h), N - dist(r, h)) for h in Hn)); prof[p] = prof.get(p, 0) + 1
print('      distance profiles of the quotient hubs to the N outputs (up to sign): %s' % sorted(prof.items())[:6])
