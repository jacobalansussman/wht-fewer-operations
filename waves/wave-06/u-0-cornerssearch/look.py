# u-0: look at a picture: prints it, the cost of every output step and input step, the runs, and replays exactly (whole numbers).
import sys, ast
txt = open(sys.argv[1]).read().split('BEST')[-1]
rows = ast.literal_eval(txt.split('rows ')[1].split(' r ')[0]); cols = ast.literal_eval(txt.split('cols ')[1].split(' c ')[0])
N = len(rows); k = N.bit_length() - 1
A = [[1 if (rows[a] & cols[b]) == cols[b] else 0 for b in range(N)] + [0] for a in range(N)] + [[0] * (N + 1)]
M = [[A[a][b] - A[a + 1][b] - A[a][b + 1] + A[a + 1][b + 1] for b in range(N)] for a in range(N)]
nz = sum(1 for a in range(N) for b in range(N) if M[a][b])
ok = True
for e in range(N):
    F = [1 if b >= e else 0 for b in range(N)]
    y = [0] * (N + 1)
    for a in range(N - 1, -1, -1): y[a] = y[a + 1] + sum(M[a][b] * F[b] for b in range(N) if M[a][b])
    for a in range(N):
        if y[a] != (1 if (rows[a] & cols[e]) == cols[e] else 0): ok = False
pr = [sum(1 for b in range(N) if M[a][b]) for a in range(N)]
pc = [sum(1 for a in range(N) if M[a][b]) for b in range(N)]
print(f"N={N}: corners={nz} per point={nz/N:.4f} gates(G)={N-2+nz} Yates={N//2*k} 2N-2={2*N-2}; exact replay on {N} basis vectors: {ok}")
print(" non-zeros per output step (first row first):", pr)
print(" non-zeros per input step (first col first):", pc)
import collections
print(" histogram rows:", sorted(collections.Counter(pr).items()), " cols:", sorted(collections.Counter(pc).items()))
print(" prefix steps (rows with one non-zero):", pr.count(1), " (cols):", pc.count(1))
comp = sum(1 for a in range(N-1) if (rows[a] & rows[a+1]) in (rows[a], rows[a+1]))
gray = sum(1 for a in range(N-1) if bin(rows[a] ^ rows[a+1]).count('1') == 1)
compc = sum(1 for a in range(N-1) if (cols[a] & cols[a+1]) in (cols[a], cols[a+1]))
grayc = sum(1 for a in range(N-1) if bin(cols[a] ^ cols[a+1]).count('1') == 1)
print(f" row steps: comparable {comp} of {N-1}, one-bit {gray};  col steps: comparable {compc}, one-bit {grayc}")
print(" values of M:", sorted(collections.Counter(v for r in M for v in r if v).items()))
# cost by size of the smaller set of the step, and by Hamming distance
bys = collections.defaultdict(list)
for a in range(N-1):
    bys[bin(rows[a]^rows[a+1]).count('1')].append(pr[a])
print(" row step cost by number of bits changed:", {h:(len(v), sum(v)) for h,v in sorted(bys.items())})
byw = collections.defaultdict(list)
for a in range(N-1): byw[max(bin(rows[a]).count('1'), bin(rows[a+1]).count('1'))].append(pr[a])
print(" row step cost by size of the larger output set: ", {h:(len(v), sum(v), round(sum(v)/len(v),2)) for h,v in sorted(byw.items())})
if N <= 64 and len(sys.argv) > 2:
    for a in range(N):
        print(format(rows[a], '0%db' % k), ''.join('#' if A[a][b] else '.' for b in range(N)), pr[a])
    for i in range(k-1, -1, -1): print(' ' * k, ''.join(str((cols[b] >> i) & 1) for b in range(N)))
