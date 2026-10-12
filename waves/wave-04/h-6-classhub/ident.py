#!/usr/bin/env python3
"""h-6-classhub / ident.py : identities of the kernel K = [[1,1],[1,tau]] with tau a SYMBOL (exact rational functions)."""
from field import TAU as t, RF
one = RF.of(1); zero = RF.of(0)
def mm(A, B): return [[sum((A[i][l] * B[l][j] for l in range(len(B))), zero) for j in range(len(B[0]))] for i in range(len(A))]
def kron(A, B): return [[A[i][j] * B[p][q] for j in range(len(A)) for q in range(len(B))] for i in range(len(A)) for p in range(len(B))]
def show(M): return ' ; '.join(' '.join(str(x) for x in r) for r in M)
K = [[one, one], [one, t]]; KK = kron(K, K)
u = [one, one, one, t]
P = [[zero] * 4 for _ in range(4)]; P[1][1] = one; P[2][2] = one; P[0][3] = zero - one; P[3][0] = zero - one
print('1. K x K = u u^T + (tau-1) P :', all(KK[i][j] == u[i] * u[j] + (t - 1) * P[i][j] for i in range(4) for j in range(4)))
R = [[(mm(P, KK)[i][j]) / (t - 1) for j in range(4)] for i in range(4)]          # P^-1 = P
I4 = [[one if i == j else zero for j in range(4)] for i in range(4)]
print('2. R = P (K x K) / (tau-1) is an involution for EVERY tau (R R = I):', mm(R, R) == I4, '| R - I has rank one, R = I + v u^T/(tau-1) with v = P u =', [str(sum((P[i][j] * u[j] for j in range(4)), zero)) for i in range(4)])
v = [sum((P[i][j] * u[j] for j in range(4)), zero) for i in range(4)]
print('   R = I + v u^T/(tau-1):', all(R[i][j] == I4[i][j] + v[i] * u[j] / (t - 1) for i in range(4) for j in range(4)), '| u.v =', str(sum((a * b for a, b in zip(u, v)), zero)), '| v = u only if tau = -1 (then R is the orthogonal reflection I - u u^T/2)')
R2 = kron(R, R); I16 = [[one if i == j else zero for j in range(16)] for i in range(16)]
tr = sum((R2[i][i] for i in range(16)), zero)
print('   R x R (16 points): involution:', mm(R2, R2) == I16, '| trace =', str(tr), '=> its mirror (the -1 eigenspace) has dimension (16 - trace)/2 =', str((16 - tr) / 2), 'for every tau')
for name, D in (('diag(1,-1)', [[one, zero], [zero, zero - one]]), ('diag(1,-1/tau)', [[one, zero], [zero, zero - one / t]])):
    print('3. K * %s * K =' % name, show(mm(mm(K, D), K)))
print('4. K^2 =', show(mm(K, K)), '| K^3 =', show(mm(mm(K, K), K)))
print('   K^2 has a zero entry iff 1 + tau^2 = 0 (tau = i, -i) or tau = -1 ; K^3 is a multiple of the identity iff tau^2 + tau + 2 = 0')
