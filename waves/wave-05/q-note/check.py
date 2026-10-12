# q-note/check.py : small exact checks for WAVE5-NOTE.md. Whole numbers and fractions only. Count (G).
import re, ast, sys
from fractions import Fraction as F
D = 'waves/wave-05/'

def orders(path):
    rows = cols = None
    best = None
    for line in open(path):
        if line.startswith('BEST'):
            best = line.strip()
        m = re.match(r'(rows|cols) (\[[^\]]*\])', line)
        if m:
            v = ast.literal_eval(m.group(2))
            if m.group(1) == 'rows': rows = v
            else: cols = v
    return rows, cols, best

def corners(rows, cols):
    # subset-sum matrix: output S reads input T when T is inside S
    N = len(rows)
    A = [[1 if (t & s) == t else 0 for t in cols] for s in rows]
    def a(i, j):
        return A[i][j] if i < N and j < N else 0
    M = [[a(i, j) - a(i, j+1) - a(i+1, j) + a(i+1, j+1) for j in range(N)] for i in range(N)]
    nnz = sum(1 for i in range(N) for j in range(N) if M[i][j])
    # replay the circuit: running sums of the inputs, then output after output from the end
    gates = 0
    ok = True
    Fs = []                       # Fs[j] = sum of inputs cols[0..j]  (running sums from the start)
    acc = [0]*N
    for j in range(N):
        acc = acc[:]; acc[cols[j]] += 1
        Fs.append(acc)
        if j > 0: gates += 1
    prev = None
    for i in range(N-1, -1, -1):
        y = [0]*N if prev is None else prev[:]
        terms = [(j, M[i][j]) for j in range(N) if M[i][j]]
        for j, c in terms:
            y = [y[t] + c*Fs[j][t] for t in range(N)]
        gates += len(terms) - (1 if prev is None else 0)
        want = [1 if (t & rows[i]) == t else 0 for t in range(N)]
        ok = ok and (y == want)
        prev = y
    small = sum(1 for i in range(N) if sum(1 for j in range(N) if M[i][j]) <= 2)
    vals = sorted(set(M[i][j] for i in range(N) for j in range(N) if M[i][j]))
    return nnz, gates, ok, small, vals

print('1. Two-chain circuits for subset sums (corners = non-zero second differences), my own counter and replay')
for f in ['q-cross/cat3_4.out', 'q-cross/cat3_8.out', 'q-cross/cat3_16.out', 'q-cross/cat3g_32.out',
          'u-0-cornerssearch/a16.out', 'u-0-cornerssearch/r32.out', 'u-0-cornerssearch/r64.out']:
    try:
        r, c, best = orders(D + f)
        N = len(r)
        assert sorted(r) == list(range(N)) and sorted(c) == list(range(N))
        nnz, gates, ok, small, vals = corners(r, c)
        k = N.bit_length() - 1
        print(f'  {f}: N={N} corners={nnz} gates={gates} (N-2+corners={N-2+nnz}) replay={ok} '
              f'rows with <=2: {small}/{N} values={vals} Yates={(N//2)*k} per point={nnz/N:.3f} vs (k/2)={k/2}')
    except Exception as e:
        print('  ', f, 'FAILED', repr(e))

print('2. p-0 hub-free 7-gate circuit for K=[[1,1],[1,2]] squared')
def lin(*c): return list(c)
x = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
add = lambda a, u, b, v: [a*p + b*q for p, q in zip(u, v)]
h0 = add(1, x[2], 1, x[3]); h1 = add(1, x[1], 1, x[3]); h2 = add(1, x[0], 2, h0)
r10 = add(1, x[1], 1, h2); r00 = add(1, r10, -1, h0); r01 = add(1, h1, 1, r00); r11 = add(2, h1, 1, h2)
K = [[1, 1], [1, 2]]
KK = {(a, b): [K[a][c]*K[b][d] for c in (0, 1) for d in (0, 1)] for a in (0, 1) for b in (0, 1)}
print('  ', r00 == KK[0, 0], r01 == KK[0, 1], r10 == KK[1, 0], r11 == KK[1, 1], '(7 gates; helpers read 2, 2, 3 inputs)')

print('3. p-0 weight-only block at k=2: 5 gates for every tau, 4 at tau=-1')
allok = True
for tau in [F(-1), F(2), F(1, 2), F(3), F(-2), F(5, 7), F(-7, 3)]:
    a, b, c = [1, 0, 0], [0, 1, 0], [0, 0, 1]
    h1 = add(1, a, 2, b); h2 = add(1, h1, tau, c)
    r0 = add(1, h1, 1, c); r1 = add(1, h2, tau - 1, b); r2 = add(tau, h2, 1 - tau, a)
    allok = allok and r0 == [1, 2, 1] and r1 == [1, 1 + tau, tau] and r2 == [1, 2*tau, tau*tau]
print('   5-gate circuit right at seven values of tau:', allok)
a, b, c = [1, 0, 0], [0, 1, 0], [0, 0, 1]
u = add(1, a, 1, c); r1 = add(1, a, -1, c); r0 = add(1, u, 2, b); r2 = add(1, u, -2, b)
print('   4-gate circuit at tau=-1:', r0 == [1, 2, 1] and r1 == [1, 0, -1] and r2 == [1, -2, 1])

print('4. Arithmetic of the laws')
Ns = [4, 8, 16, 32, 64, 128]
ks = [2, 3, 4, 5, 6, 7]
print('   textbook gates      ', [n*k for n, k in zip(Ns, ks)])
print('   textbook rectangles ', [n*k - n + 2 for n, k in zip(Ns, ks)])
print('   (N^2+14)/6          ', [F(n*n + 14, 6) for n in Ns])
t = [5]; [t.append(4*t[-1] - 7) for _ in range(5)]; print('   4t-7                ', t)
T = [5, 13]; [T.append(8*T[-2] - 3) for _ in range(4)]; print('   T(k)=8T(k-2)-3      ', T)
print('   floor N+(19/256)N^2 ', [(n, F(n) + F(19*n*n, 256)) for n in Ns[3:]])
print('   (N/2)log2N+1        ', [n*k//2 + 1 for n, k in zip(Ns, ks)])
print('   N-1+(N/2)log2N      ', [n - 1 + n*k//2 for n, k in zip(Ns, ks)])
print('   Yates               ', [n*k//2 for n, k in zip(Ns, ks)])
print('   2N-2 ; 3N-4         ', [2*n - 2 for n in Ns], [3*n - 4 for n in Ns])
print('   beat Yates below    ', [n*k//2 - n + 2 for n, k in zip(Ns, ks)], '(corners at or below value-1.. i.e. N-2+c < Yates)')
rec = [7, 19, 52, 128, 304]
print('   records/(N log2 N)  ', [round(g/(n*k), 4) for g, n, k in zip(rec, Ns, ks)])
two = [7, 19, 52, 132, 304]
print('   two letters/(NlogN) ', [round(g/(n*k), 4) for g, n, k in zip(two, Ns, ks)])
one = [5, 13, 45, 173, 685]
print('   one letter gates    ', [n - 2 + t for n, t in zip(Ns, one)], [round((n - 2 + t)/(n*k), 4) for n, t, k in zip(Ns, one, ks)])
cor = [5, 13, 30, 80, 239]
print('   corner gates        ', [n - 2 + t for n, t in zip(Ns, cor)], 'over Yates', [round((n - 2 + t)/(n*k/2), 3) for n, t, k in zip(Ns, cor, ks)])
print('   p-2 5(N-3^m)+mid    ', [5*(4**m - 3**m) + mid for m, mid in zip([2, 3, 4], [10, 121, 971])], 'Yates', [4**m*m for m in [2, 3, 4]])
print('   p-2 route floors/Yates', [round(a/b, 3) for a, b in zip([5, 34, 156, 644], [4, 32, 192, 1024])])
print('   (O) any one factor / textbook', [round(a/b, 4) for a, b in zip([8, 20, 56, 144, 320], [8, 24, 64, 160, 384])])
