# v-0: replay a gate list exactly; is every wire a sign vector on an affine set; are the sets one tree; chain or branch-dependent?
import re,sys
from fractions import Fraction as Fr
path=sys.argv[1]; W={}; order=[]
lines=[l.split('#')[0].strip() for l in open(path)]
lines=[l for l in lines if '=' in l]
names=set(re.findall(r'x(\d+)',' '.join(lines))); N=max(int(i) for i in names)+1
for i in range(N): W['x%d'%i]=[Fr(int(i==j)) for j in range(N)]
for l in lines:
    nm,ex=[s.strip() for s in l.split('=')]
    terms=re.findall(r'([+-]?)\s*(?:(\d+(?:/\d+)?)\s*\*\s*)?([a-zA-Z_]\w*)',ex)
    assert len(terms)<=2, l
    v=[Fr(0)]*N
    for sg,co,w in terms:
        c=Fr(co) if co else Fr(1)
        if sg=='-': c=-c
        v=[a+c*b for a,b in zip(v,W[w])]
    W[nm]=v; order.append(nm)
k=N.bit_length()-1
rows=[[(-1)**bin(x&y).count('1') for x in range(N)] for y in range(N)]
okrows=all(W['y%d'%y]==[Fr(t) for t in rows[y]] for y in range(N))
sets=set(); form=True; affine=True
for nm in order:
    v=W[nm]; nz=[a for a in v if a]; 
    if len(set(abs(a) for a in nz))!=1: form=False
    S=frozenset(i for i,a in enumerate(v) if a); sets.add(S)
    b=min(S); D={i^b for i in S}
    if not all((p^q) in D for p in D for q in D): affine=False
nested=all(A<=B or B<=A or not(A&B) for A in sets for B in sets)
print(path.split('/')[-1],": N",N,"gates",len(order),"| exact transform:",okrows,"| all wires sign vectors:",form,"| all sets affine:",affine,"| nested or disjoint:",nested)
for sz in sorted({len(S) for S in sets}):
    ss=[sorted(S) for S in sets if len(S)==sz]
    dirs={frozenset(i^min(S) for i in S) for S in sets if len(S)==sz}
    print("  sets of size",sz,":",sorted(ss),"| distinct directions (subspaces):",len(dirs), "-> chain at this level" if len(dirs)==1 else "-> branch-dependent")
