# excess.py : for every orbit of 4 targets of height 1 on 4 inputs (from tallmin4 VERB output): determinant, connected pieces,
# the "one unit per gate" floor  n - c + log2|det|  and the least gates found (forms; and tall where a SAVE line exists).
import sys, re, math
from fractions import Fraction
def det(M):
    M=[[Fraction(x) for x in r] for r in M]; n=len(M); d=Fraction(1)
    for i in range(n):
        p=next((r for r in range(i,n) if M[r][i]!=0),None)
        if p is None: return 0
        if p!=i: M[i],M[p]=M[p],M[i]; d=-d
        d*=M[i][i]
        for r in range(i+1,n):
            f=M[r][i]/M[i][i]
            M[r]=[a-f*b for a,b in zip(M[r],M[i])]
    return int(d)
def comps(M):
    n=len(M[0]); par=list(range(n))
    def f(x):
        while par[x]!=x: x=par[x]
        return x
    for r in M:
        s=[i for i,x in enumerate(r) if x]
        for i in s[1:]: par[f(i)]=f(s[0])
    return len({f(i) for i in range(n)})
saves=set(); rows=[]
for line in open(sys.argv[1]):
    if line.startswith('SAVE'):
        t=re.findall(r'\(([-\d,]+)\)', line.split('forms:')[0]); saves.add(tuple(t))
    if line.startswith('ORBIT'):
        h1=int(re.search(r'h1=(-?\d+)',line).group(1)); t=re.findall(r'\(([-\d,]+)\)', line)
        rows.append((h1,tuple(t)))
neg=0; tot=0; hist={}
for h1,t in rows:
    M=[[int(x) for x in s.split(',')] for s in t]; d=det(M)
    if d==0: continue
    tot+=1; c=comps(M); n=len(M[0]); G=len(M)+h1-(1 if t in saves else 0)
    floor=n-c+math.log2(abs(d)); ex=G-floor
    key=(abs(d),G); hist[key]=hist.get(key,0)+1
    if ex<-1e-9:
        neg+=1; print('BELOW one-unit floor: det',d,'pieces',c,'gates',G,'floor %.3f'%floor,'tall' if t in saves else 'forms',t)
print('# nonsingular orbits',tot,' below the one-unit floor:',neg)
print('# (|det|, least gates): count ->',sorted(hist.items()))
