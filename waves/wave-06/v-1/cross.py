# exact-sum version of u-2's bound: sum_j (j/k)^2 C(k,j) (2^(k-j)-1/2)^2 / (4N(1+ln N))   (float only in the logarithm)
import math
from math import comb
from fractions import Fraction
marks={}; prev=None
for k in range(2,131):
    N=2**k
    s=sum(Fraction(j*j,k*k)*comb(k,j)*(Fraction(2**(k-j))-Fraction(1,2))**2 for j in range(1,k+1))
    lb=float(s/(4*N))/(1+math.log(N))
    for name,thr in (("N",N),("3N",3*N),("Yates (N/2)k+1",N*k/2+1)):
        if name not in marks and lb>thr: marks[name]=k
    if k in (4,5,6,16,32,64,99,100): print("k=%d exact-sum bound = %.4g, per point %.4g%s"%(k,lb,lb/N,"" if prev is None else ", factor per bit %.3f"%(lb/prev)))
    prev=lb
print("exact-sum bound first exceeds:",marks)
