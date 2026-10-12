# Is the 8-gate, 3-repeat circuit of hybrid 1 an identity of the class of 2 x 2 kernels? Exact fractions.
# Wiring: g1 = (a,b), g2 = (c,d), g3 = (g1,g2), g4 = (b,d), g5 = (g3,g4), g6 = (g3,g2), g7 = (b,c), g8 = (g3,g7); outputs g3,g5,g6,g8.
# For a kernel K = [[p,q],[r,s]] the outputs must be the rows of K (x) K up to scale. A gate (u,v) can make a target t
# exactly when t lies in the span of u and v.
from fractions import Fraction as F
def rank(rows):
    M=[list(map(F,r)) for r in rows]; rk=0
    for c in range(len(M[0])):
        piv=next((r for r in range(rk,len(M)) if M[r][c]!=0),None)
        if piv is None: continue
        M[rk],M[piv]=M[piv],M[rk]
        for r in range(rk+1,len(M)):
            if M[r][c]!=0:
                f=M[r][c]/M[rk][c]; M[r]=[x-f*y for x,y in zip(M[r],M[rk])]
        rk+=1
    return rk
def inspan(t,u,v): return rank([u,v,t])==rank([u,v])
def test(p,q,r,s):
    row=lambda A,B:[A[0]*B[0],A[0]*B[1],A[1]*B[0],A[1]*B[1]]
    R=[row((p,q),(p,q)),row((p,q),(r,s)),row((r,s),(p,q)),row((r,s),(r,s))]
    a,b,c,d=[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]
    g1=[p,q,0,0]; g2=[0,0,p,q]                  # the only pairs on (a,b) and (c,d) that can serve row 1
    ok3=inspan(R[0],g1,g2); g3=R[0]
    # g4 on (b,d): free ratio; g5 = row 2 needs row2 - x*g3 on the support {b,d}
    def via(t,support):
        # is t = x*g3 + (a wire supported on the two given inputs)?  solve x from an input outside the support
        outside=[i for i in range(4) if i not in support]
        x=F(t[outside[0]],g3[outside[0]]) if g3[outside[0]]!=0 else None
        if x is None: return False
        return all(t[i]-x*g3[i]==0 for i in outside)
    ok5=via(R[1],(1,3)); ok6=inspan(R[2],g3,g2); ok8=via(R[3],(1,2))
    return ok3,ok5,ok6,ok8
for K in [(1,1,1,-1),(1,2,3,-6),(2,3,5,F(-15,2)),(1,2,3,5),(1,1,1,-2),(2,1,1,3)]:
    p,q,r,s=K
    print("kernel",K,"permanent p*s+q*r =",p*s+q*r,"| gates g3,g5,g6,g8 possible:",test(*K))
