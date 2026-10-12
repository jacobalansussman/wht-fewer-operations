# a-0, part (a): the "one class" claim, my own code. Exact rationals (fractions.Fraction) throughout.
# 1. i-cross's four-call word for Z at k = 1..5.   2. a THREE-call word for Z (mine).   3. no two-call word exists (why).
# 4. H = Z D Z^T and Z^T = X Z X (X = complement relabelling), k = 1..5.
# 5. class lemma over Q: for random rational non-monomial M: Z from two calls of M, M from two calls of Z (LDU), hence
#    cost(H) <= 4 cost(M) + O(N), cost(M) <= 6 cost(H) + O(N).
# 6. "two calls of H" reaches exactly the kernels whose tau is a square in the field.
from fractions import Fraction as Fr
import random, sys
def mm(A, B):
    n, m, l = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(m) if A[i][t]) for j in range(l)] for i in range(n)]
def dg(v): return [[Fr(v[i]) if i == j else Fr(0) for j in range(len(v))] for i in range(len(v))]
def kron(A, B): return [[a * b for a in ra for b in rb] for ra in A for rb in B]
def kpow(A, k):
    R = [[Fr(1)]]
    for _ in range(k): R = kron(R, A)
    return R
def word(*Ms):
    R = Ms[0]
    for M in Ms[1:]: R = mm(R, M)
    return R
def F(M): return [[Fr(x) for x in r] for r in M]
H = F([[1, 1], [1, -1]]); Z = F([[1, 0], [1, 1]]); ZT = F([[1, 1], [0, 1]]); X = F([[0, 1], [1, 0]])

four = [(Fr(1, 32), Fr(1, 10)), (3, 1), (3, -2), (2, 1), (1, Fr(-5, 9))]
three = [(Fr(1, 4), Fr(1, 5)), (Fr(3, 2), Fr(-1, 2)), (2, 1), (1, Fr(5, 3))]
print("k=1  four-call word equals Z:", word(dg(four[0]), H, dg(four[1]), H, dg(four[2]), H, dg(four[3]), H, dg(four[4])) == Z)
print("k=1  THREE-call word diag(1/4,1/5) H diag(3/2,-1/2) H diag(2,1) H diag(1,5/3) equals Z:",
      word(dg(three[0]), H, dg(three[1]), H, dg(three[2]), H, dg(three[3])) == Z)
for k in range(1, 6):
    Hk, Zk, ZTk, Xk = kpow(H, k), kpow(Z, k), kpow(ZT, k), kpow(X, k)
    D4 = [kpow(dg(d), k) for d in four]; D3 = [kpow(dg(d), k) for d in three]
    a = word(D4[0], Hk, D4[1], Hk, D4[2], Hk, D4[3], Hk, D4[4]) == Zk
    b = word(D3[0], Hk, D3[1], Hk, D3[2], Hk, D3[3]) == Zk
    c = word(Zk, kpow(dg((1, -2)), k), ZTk) == Hk
    d = word(Xk, Zk, Xk) == ZTk
    # Z really is "sum over subsets": (Zk x)[T] = sum of x[S], S subset of T
    e = all(Zk[T][S] == (1 if (S & T) == S else 0) for T in range(1 << k) for S in range(1 << k))
    print("k=%d N=%2d  four-call:%s  three-call:%s  H = Z D Z^T:%s  Z^T = X Z X:%s  Z is the subset-sum matrix:%s" % (k, 1 << k, a, b, c, d, e))
    sys.stdout.flush()

# 3. two calls cannot give Z: D1 H diag(a,b) H D5 = D1 [[a+b,a-b],[a-b,a+b]] D5 has a zero only if a = +-b, and then two zeros.
print("two-call words D H D H D: entries (a+b, a-b; a-b, a+b) up to scalings; exactly one zero is impossible [derived]")

# 5. class lemma, random rational M with no zero entry and tau != 1, -1
random.seed(7); ok1 = ok2 = ok3 = True; tried = 0
def tau(M): return M[0][0] * M[1][1] / (M[0][1] * M[1][0])
def is_monomial_times(A, T):
    # is A = P1 D1 T D2 P2 with D diagonal invertible and P in {I, X}?  compare zero patterns and the cross ratio when defined
    for P1 in (None, X):
        for P2 in (None, X):
            B = A
            if P1: B = mm(P1, B)
            if P2: B = mm(B, P2)
            if all((B[i][j] == 0) == (T[i][j] == 0) for i in range(2) for j in range(2)):
                if all(T[i][j] != 0 for i in range(2) for j in range(2)):
                    if tau(B) == tau(T): return True
                else: return True
    return False
while tried < 2000:
    M = [[Fr(random.randint(-9, 9), random.randint(1, 9)) for _ in range(2)] for _ in range(2)]
    if any(x == 0 for r in M for x in r): continue
    t = tau(M)
    if t in (1, -1): continue
    tried += 1
    a, b, c, d = M[0][0], M[0][1], M[1][0], M[1][1]
    # Z from two calls of M: M diag(1, delta) M with delta = -a^2/(bc) has zero top-left, all three others non-zero
    A = word(M, dg((1, -a * a / (b * c))), M)
    ok1 &= (A[0][0] == 0 and A[0][1] != 0 and A[1][0] != 0 and A[1][1] != 0)        # = X * triangular, a relabelled scaled Z
    ok1 &= is_monomial_times(A, mm(X, Z)) or is_monomial_times(A, Z)
    # M from two calls of Z: M = L D U with L = diag(1,c/a) Z diag(1,a/c), U = diag(b/a,1)... written out and checked
    L = word(dg((1, c / a)), Z, dg((1, a / c))); U = word(dg((b / a, 1)), ZT, dg((a / b, 1)))
    ok2 &= word(L, dg((a, d - b * c / a)), U) == M
    # tensor check at k = 3 of the first identity pattern (mixed-product property), one in fifty
    if tried % 50 == 0:
        k = 3; Mk = kpow(M, k); Ak = word(Mk, kpow(dg((1, -a * a / (b * c))), k), Mk); ok3 &= Ak == kpow(A, k)
print("class lemma over Q, %d random M (no zero entry, tau not 1 or -1): Z-shape from two calls of M: %s ; M = L D U from two calls of Z: %s ; k=3 tensor form: %s" % (tried, ok1, ok2, ok3))

# 6. which kernels are two calls of H over Q?  D1 H diag(a,b) H D5 has tau = ((a+b)/(a-b))^2: a rational square.
#    brute force confirmation on a grid: every tau reached is a square; and tau = 2 is never reached with small rationals.
from math import isqrt
def is_sq(q):
    n, d = abs(q.numerator), q.denominator
    return q >= 0 and isqrt(n) ** 2 == n and isqrt(d) ** 2 == d
allsq = True; seen = set()
for an in range(-12, 13):
    for bn in range(-12, 13):
        if an == 0 or bn == 0 or an == bn or an == -bn: continue
        K = word(H, dg((an, bn)), H); t = tau(K); allsq &= is_sq(t); seen.add(t)
print("two calls of H over Q: every tau reached on the grid is a rational square: %s ; tau = 2 reached: %s ; tau = -1 (H itself) reached: %s" % (allsq, Fr(2) in seen, Fr(-1) in seen))
