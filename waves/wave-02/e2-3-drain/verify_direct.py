#!/usr/bin/env python3
"""verify_direct.py -- independent exact check of a gate list, count (G), with NO normalisation tricks:
every gate is n_k = a*n_u + b*v with rational a, b computed here so that the stored vector equals drain.c's normalised
form; the vectors are carried as exact Fractions.  Then: every row of the N-point Walsh-Hadamard matrix (Sylvester order)
must be a non-zero rational multiple of one of the vectors computed.  Prints the program in full.
usage: verify_direct.py <result file>"""
import sys, json
from fractions import Fraction as Fr
from math import gcd
L=[json.loads(l) for l in open(sys.argv[1])]; N=L[0]['N']; best=L[-1]['best']
H=[[(-1)**bin(x&y).count('1') for y in range(N)] for x in range(N)]
V=[[Fr(int(i==j)) for j in range(N)] for i in range(N)]
lines=[]
for k,(u,v,a,b) in enumerate(best['prog']):
    raw=[a*p+b*q for p,q in zip(V[u],V[v])]
    g=0
    for z in raw: g=gcd(g,abs(int(z)))
    s=next(z for z in raw if z); lam=Fr(1,g)*(1 if s>0 else -1)      # the free scaling of count (G)
    V.append([lam*z for z in raw]); lines.append('n%d = (%s)*n%d + (%s)*n%d   = %s'%(N+k,lam*a,u,lam*b,v,[int(z) for z in V[-1]]))
def mult(row,vec):
    i=next((i for i in range(N) if vec[i]!=0),None)
    if i is None: return None
    c=Fr(row[i])/vec[i]
    return c if all(c*vec[j]==row[j] for j in range(N)) else None
found={}
for t in range(N):
    for j in range(N,len(V)):
        c=mult(H[t],V[j])
        if c is not None: found[t]=(j,c); break
print('\n'.join(lines))
for t in range(N): print('output row',t,H[t],'=', ('(%s)*n%d'%(found[t][1],found[t][0])) if t in found else 'NOT FOUND')
print('N =',N,'| gates =',len(best['prog']),'| outputs found as stored forms (up to scale):',len(found),'of',N,'| VERDICT:', 'PASS' if len(found)==N else 'FAIL')
