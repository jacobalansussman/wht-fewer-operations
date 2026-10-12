#!/usr/bin/env python3
"""cdepth.py -- for a drain.c result: clean gates (arguments with disjoint supports), cancelling gates, and the
cancellation depth of each gate = the largest number of cancelling gates on a path from an input to it.
Also the textbook saving N log2 N - size, to compare with (N/4) * depth.  Only circuits that finish all outputs (P = 0)."""
import sys, json, glob
from math import gcd, log2
def norm(x):
    g=0
    for v in x: g=gcd(g,abs(v))
    x=[v//g for v in x]; s=next(v for v in x if v)
    return x if s>0 else [-v for v in x]
def look(f):
    L=[json.loads(l) for l in open(f)]; N=L[0]['N']; best=L[-1]['best']
    if any(r['cost'] for r in best['reps']): return None
    F=[[int(i==j) for j in range(N)] for i in range(N)]; dep=[0]*N; clean=0
    for (u,v,a,b) in best['prog']:
        c=any(p and q for p,q in zip(F[u],F[v])); clean+=(not c)
        F.append(norm([a*p+b*q for p,q in zip(F[u],F[v])])); dep.append(max(dep[u],dep[v])+int(c))
    outs=[r['forms'][0] for r in best['reps']]
    return N,len(best['prog']),clean,sorted(dep[o] for o in outs)
if __name__=='__main__':
    from collections import Counter
    for pat in sys.argv[1:]:
        C=Counter()
        for f in sorted(glob.glob(pat)):
            r=look(f)
            if r: C[(r[0],r[1],r[2],max(r[3]),tuple(r[3]))]+=1
        for (N,g,cl,md,ds),n in sorted(C.items()):
            print(pat,'| N',N,'gates',g,'clean',cl,'cancelling',g-cl,'| saving vs N log2 N:',int(N*log2(N))-g,'| depth of each output',ds,'| max depth',md,'| (N/4)*max depth =',N*md//4,'| circuits:',n)
