# s-cross hybrid 1, exact check: with H(x,y) = (-1)^(polar form of Q) and D = diag((-1)^Q), is (D H)^3 a multiple of the identity?
def pop(v): return bin(v).count('1')
for n in (1, 2, 3):
    k = 2*n; N = 1 << k
    def Q(x): return sum(((x >> (2*i)) & 1) * ((x >> (2*i+1)) & 1) for i in range(n)) & 1
    def sw(x): return sum((((x >> (2*i)) & 1) << (2*i+1)) | (((x >> (2*i+1)) & 1) << (2*i)) for i in range(n))
    R = [[(-1)**Q(x) * (-1)**pop(x & sw(y)) for y in range(N)] for x in range(N)]
    def mul(A, B): return [[sum(A[i][t]*B[t][j] for t in range(N)) for j in range(N)] for i in range(N)]
    R3 = mul(mul(R, R), R); c = R3[0][0]
    ok = all(R3[i][j] == (c if i == j else 0) for i in range(N) for j in range(N))
    tr = sum(R[i][i] for i in range(N))
    print('N=%d: (D H)^3 = %d * identity: %s ; trace(D H) = %d ; so D H / sqrtN has order 3 with fixed space of dimension (N+2)/3 = %d and the two other eigenvalues (N-1)/3 = %d times each' % (N, c, ok, tr, (N+2)//3, (N-1)//3))
