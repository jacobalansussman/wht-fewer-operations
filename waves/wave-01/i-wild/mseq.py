#!/usr/bin/env python3
# i-wild, idea 7: in multiplicative coordinates the transform on the non-zero addresses is c[i+j], c a +-1 m-sequence.
# How many geometric sequences does one period need?  Exact rank of the Hankel matrix of one period (fractions).
from fractions import Fraction as F
def mseq(k,taps):
    s=[1]+[0]*(k-1); out=[]
    for _ in range((1<<k)-1):
        out.append(s[0]); nb=0
        for t in taps: nb^=s[t]
        s=s[1:]+[nb]
    return [(-1)**b for b in out]
def rank(M):
    M=[[F(x) for x in r] for r in M]; r=0
    for c in range(len(M[0])):
        p=next((i for i in range(r,len(M)) if M[i][c]!=0),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]
        for i in range(r+1,len(M)):
            if M[i][c]!=0:
                f=M[i][c]/M[r][c]; M[i]=[a-f*b for a,b in zip(M[i],M[r])]
        r+=1
    return r
for k,taps in ((4,(0,1)),(5,(0,2)),(6,(0,1)),(7,(0,1))):
    c=mseq(k,taps); L=len(c); assert sum(c)==-1
    # check: the non-zero block of H is a relabelled c[i+j]: autocorrelation two-valued
    assert all(sum(c[t]*c[(t+s)%L] for t in range(L))==-1 for s in range(1,L))
    h=(L+1)//2
    Hk=[[c[i+j] for j in range(h)] for i in range(h)]            # one period, not wrapped
    Cw=[[c[(i+j)%L] for j in range(L)] for i in range(L)]        # wrapped
    print("k=%d period %d: Hankel rank of one period %d of %d;  wrapped circulant rank %d of %d"%(k,L,rank(Hk),h,rank(Cw),L))
