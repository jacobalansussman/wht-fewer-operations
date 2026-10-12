#!/usr/bin/env python3
"""replay.py -- exact check (Fractions) of a drain.c result.  Rebuilds every stored form from the gate list, then for each
output checks that it lies in the span of the stored forms and inputs its representation names, and recounts:
size = gates + sum over outputs of (forms + inputs - 1).   usage: replay.py <result file> [H|Z]"""
import sys, json
from fractions import Fraction as Fr
def rank(rows):
    M=[[Fr(x) for x in r] for r in rows]; r=0
    if not M: return 0
    for c in range(len(M[0])):
        p=next((i for i in range(r,len(M)) if M[i][c]!=0),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]
        for i in range(r+1,len(M)):
            if M[i][c]!=0:
                f=M[i][c]/M[r][c]; M[i]=[a-f*b for a,b in zip(M[i],M[r])]
        r+=1
    return r
L=[json.loads(l) for l in open(sys.argv[1])]; hd=L[0]; N=hd['N']; best=L[-1]['best']
tg=hd.get('target','H')
T=[[(1 if (x&y)==y else 0) if tg=='Z' else (-1)**bin(x&y).count('1') for y in range(N)] for x in range(N)]
F=[[int(i==j) for j in range(N)] for i in range(N)]
from math import gcd
def norm(x):
    # same convention as drain.c: forms are kept up to scale (scalings are free in count G): divide by the gcd, first non-zero positive
    g=0
    for v in x: g=gcd(g,abs(v))
    x=[v//g for v in x]; s=next(v for v in x if v)
    return x if s>0 else [-v for v in x]
for (u,v,a,b) in best['prog']: F.append(norm([a*p+b*q for p,q in zip(F[u],F[v])]))
tot=len(best['prog']); ok=True
for t,rep in enumerate(best['reps']):
    S=[F[j] for j in set(rep['forms'])]+[F[i] for i in rep['inputs']]
    r0=rank(S); r1=rank(S+[T[t]]); ok&=(r1==r0); tot+=max(len(rep['forms'])+len(rep['inputs'])-1,0)
    assert len(rep['forms'])+len(rep['inputs'])-1==rep['cost'] or (len(rep['forms'])+len(rep['inputs'])==0)
print('replay',sys.argv[1],'N',N,'target',tg,'gates',len(best['prog']),'exact size',tot,'claimed U',best['U'],'all outputs in their spans:',ok)
