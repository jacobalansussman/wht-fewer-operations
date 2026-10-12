# q-cross hybrid 1: exact replay of a "two chains" circuit for SUBSET SUMS found by cat3.py / cat3g.py.  Pure Python, whole numbers.
# Reads the BEST block of an output file (rows = order of the outputs, cols = order of the inputs), builds the gate list
#   F_0 = x_{c0};  F_b = F_{b-1} + x_{cb}                       (N - 1 gates: running sums of the inputs in the column order)
#   y_last = (terms of the last row);  y_a = y_{a+1} + sum_b M[a][b] F_b      (one gate per non-zero of M, minus one)
# and checks on all N basis vectors that output a equals the subset sum of row a.  Count (G).
import sys, ast
txt = open(sys.argv[1]).read().split('BEST')[-1]
rows = ast.literal_eval(txt.split('rows ')[1].split(' r ')[0]); cols = ast.literal_eval(txt.split('cols ')[1].split(' c ')[0])
N = len(rows); k = N.bit_length() - 1
Z = [[1 if (rows[a] & cols[b]) == cols[b] else 0 for b in range(N)] + [0] for a in range(N)] + [[0] * (N + 1)]
M = [[Z[a][b] - Z[a + 1][b] - Z[a][b + 1] + Z[a + 1][b + 1] for b in range(N)] for a in range(N)]
nz = sum(1 for a in range(N) for b in range(N) if M[a][b])
gates = 0; ok = True
for e in range(N):                       # basis vector: x_{cols[e]} = 1
    F = []; s = 0
    for b in range(N): s += (1 if b == e else 0); F.append(s)
    y = [0] * (N + 1)
    for a in range(N - 1, -1, -1): y[a] = y[a + 1] + sum(M[a][b] * F[b] for b in range(N) if M[a][b])
    for a in range(N):
        if y[a] != (1 if (rows[a] & cols[e]) == cols[e] else 0): ok = False
gates = (N - 1) + (nz - 1)
per_row = [sum(1 for b in range(N) if M[a][b]) for a in range(N)]
print(f"N={N}: non-zeros of M = {nz}; gates (G) = {gates}; Yates = {N//2*k}; 3N-4 = {3*N-4}; exact replay on {N} basis vectors: {ok}")
print("   non-zeros per output step (last row first):", per_row[::-1])
print("   steps with one changed interval or less (<= 2 non-zeros):", sum(1 for v in per_row if v <= 2), "of", N)
