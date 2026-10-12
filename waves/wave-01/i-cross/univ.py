# i-cross hybrid 1: "one class". Exact rational check that the subset-sum kernel is a word of four 2-point
# transforms and five scalings, that a generic full kernel is a word of two, and H = Z D Z^T. Then the k = 3 tensor powers.
from fractions import Fraction as Fr
def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def dg(*v): return [[Fr(v[i]) if i==j else Fr(0) for j in range(len(v))] for i in range(len(v))]
def kron(A,B): return [[a*b for a in ra for b in rb] for ra in A for rb in B]
def kpow(A,k):
    R=[[Fr(1)]]
    for _ in range(k): R=kron(R,A)
    return R
def dpow(v,k):
    d=[Fr(1)]
    for _ in range(k): d=[a*Fr(b) for a in d for b in v]
    return dg(*d)
def prod(*Ms):
    R=Ms[0]
    for M in Ms[1:]: R=mm(R,M)
    return R
H=[[Fr(1),Fr(1)],[Fr(1),Fr(-1)]]; Z=[[Fr(1),Fr(0)],[Fr(1),Fr(1)]]; ZT=[[Fr(1),Fr(1)],[Fr(0),Fr(1)]]
print("H diag(3,1) H =", prod(H,dg(3,1),H), " (kernel with tau = 4)")
print("H diag(2,1) H =", prod(H,dg(2,1),H), " (kernel with tau = 9)")
w=[(Fr(1,32),Fr(1,10)),(3,1),(3,-2),(2,1),(1,Fr(-5,9))]
W=prod(dg(*w[0]),H,dg(*w[1]),H,dg(*w[2]),H,dg(*w[3]),H,dg(*w[4]))
print("Z as a word D H D H D H D H D:", W, " equals Z:", W==Z)
print("H = Z diag(1,-2) Z^T:", prod(Z,dg(1,-2),ZT)==H)
for k in (2,3,4):
    Hk,Zk=kpow(H,k),kpow(Z,k)
    Wk=prod(dpow(w[0],k),Hk,dpow(w[1],k),Hk,dpow(w[2],k),Hk,dpow(w[3],k),Hk,dpow(w[4],k))
    print("k=%d: Z^(x)k = D H D H D H D H D with product diagonals: %s ; H = Z D Z^T: %s" % (k, Wk==Zk, prod(Zk,dpow((1,-2),k),kpow(ZT,k))==Hk))
# which tau can two transforms reach from a kernel with a given tau?  A_t = [[1,1],[1,t]], A_t diag(1,d) A_t has tau' = (1+d)(1+d t^2)/(1+d t)^2
# H from the tau = 4 kernel needs 32 d^2 + 25 d + 2 = 0 (discriminant 369, not a square): two calls over Q(sqrt 41), not over Q.
t=Fr(4); print("discriminant for H from two tau=4 kernels:", 25*25-4*32*2)
