# all centres c' in (GF(5)*)^8 for the chain tree (halves 15|240, pairs 3,12,48,192), up to: the affine relabellings that keep the tree,
# multiplication by a character, and one overall scalar.  One representative per class -> in8_p5_chain_*.txt
from itertools import product
tree={255,15,240,3,12,48,192}
def bits(x): return [(x>>i)&1 for i in range(3)]
maps=[]
for cols in product(range(1,8),repeat=3):
    # linear map: basis e_i -> cols[i]; invertible iff images independent
    img=[0]*8
    for x in range(8):
        v=0
        for i in range(3):
            if x>>i&1: v^=cols[i]
        img[x]=v
    if len(set(img))<8: continue
    for t in range(8):
        perm=[img[x]^t for x in range(8)]
        if all(sum(1<<perm[i] for i in range(8) if m>>i&1) in tree for m in tree): maps.append(perm)
print("affine maps keeping the tree:",len(maps))
chars=[[(-1)**bin(a&x).count('1') for x in range(8)] for a in (1,2,4)]
def norm(c):
    inv={1:1,2:3,3:2,4:4}[c[0]]; return tuple((x*inv)%5 for x in c)
allc=[(1,)+r for r in product(range(1,5),repeat=7)]
idx={c:i for i,c in enumerate(allc)}; par=list(range(len(allc)))
def find(a):
    while par[a]!=a: par[a]=par[par[a]]; a=par[a]
    return a
for i,c in enumerate(allc):
    for perm in maps:
        d=[0]*8
        for x in range(8): d[perm[x]]=c[x]
        j=idx[norm(d)]; a,b=find(i),find(j)
        if a!=b: par[a]=b
    for ch in chars:
        d=[(c[x]*(1 if ch[x]==1 else 4))%5 for x in range(8)]
        j=idx[norm(d)]; a,b=find(i),find(j)
        if a!=b: par[a]=b
reps={}
for i,c in enumerate(allc): reps.setdefault(find(i),c)
R=sorted(reps.values()); print("classes of centres:",len(R))
h=(len(R)+1)//2
for name,part in (("in8_p5_chain_a.txt",R[:h]),("in8_p5_chain_b.txt",R[h:])):
    with open(name,"w") as f:
        for c in part: print("255 15 240 3 12 48 192 ",*c,file=f)
