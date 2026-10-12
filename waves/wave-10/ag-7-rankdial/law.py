# law.py : what the private-wire lemma (ag-7.md section 3) gives in numbers.  Floating point; a table, not a proof.
# Two-element field.  N = 2^k outputs, degree at most d, shortest relation among outputs delta = 2^(d+1).
# Lemma: with V = number of wires that are not outputs (inputs included),
#   (A)  N - 1 <= edges of a graph on V + 1 vertices with no cycle shorter than delta - 2;
#   (B)  N - 1 <= V + edges of a graph on V vertices with no cycle shorter than delta.
# Bound used for the edges [RECALLED, Alon-Hoory-Linial 2002, not looked up]: a graph with v vertices, average degree
# D >= 2 and no cycle shorter than 2r has v >= 2 (1 + (D-1) + ... + (D-1)^(r-1)).
# Then helpers >= V - (rank - 1) and gates >= N - 1 + helpers.
from math import comb, log2
def n0(D,r):
    if abs(D-2)<1e-12: return 2.0*r
    x=D-1
    if r*log2(x)>1000: return float('inf')
    return 2*(x**r-1)/(x-1)
def emax(v,r):           # most edges of a graph on v vertices with girth >= 2r, by the bound
    if n0(2.0,r)>v: return v-1          # no room for average degree 2: (almost) a forest
    lo,hi=2.0,float(v)
    for _ in range(200):
        mid=(lo+hi)/2
        if n0(mid,r)<=v: lo=mid
        else: hi=mid
    return lo*v/2
def boundA(N,d):
    r=(2**(d+1)-2)//2
    lo,hi=1.0,float(N)
    for _ in range(200):
        mid=(lo+hi)/2
        if emax(mid+1,r)>=N-1: hi=mid
        else: lo=mid
    return hi
def boundB(N,d):
    r=2**d
    lo,hi=1.0,float(N)
    for _ in range(200):
        mid=(lo+hi)/2
        if mid+emax(mid,r)>=N-1: hi=mid
        else: lo=mid
    return hi
print("k   d   rank/N      V/N >= (A)   V/N >= (B)   helpers/N >=   gates/N >=   textbook d (large k)   outputs per non-output wire <=")
for k in (8,16,32,64,128):
    N=2**k
    for d in (2,3,4,5,6,7,8,10,12,16):
        if d>=k/2: continue
        R=sum(comb(k,j) for j in range(d+1))
        A=boundA(N,d); B=boundB(N,d); V=max(A,B)
        h=max(0.0,V-(R-1))
        print(f"{k:<3d} {d:<3d} {R/N:<11.3g} {A/N:<12.4f} {B/N:<12.4f} {h/N:<14.4f} {(N-1+h)/N:<12.4f} {d:<22d} {N/V:.3f}")
    print()
