# One branch of the best 16-point design, modulo 3, with points that are NOT sign vectors allowed on the wrong cherries
# (entries 0 = "3", numbers 1 = "4" or "-2").  Good cherries are kept proportional to c' (a restriction: see p-8.md).
# usage: branch3.py K cls [free]   -> input for dwg.   K = 3 or 4; cls = 0 (rows constant on cherries) or 1.
#   free: the good cherries get two digits too (no restriction), needs 3^(N) points: only for K = 3.
import sys
K=int(sys.argv[1]); cls=int(sys.argv[2]); free=len(sys.argv)>3; N=1<<K; top=K-1
c=[(-1)**((x&1)*(x>>top&1)) for x in range(N)]
ch=[(2*j,2*j+1) for j in range(N//2)]
good=[j for j,(a,b) in enumerate(ch) if (c[a]==c[b])==(cls==0)]
f3=lambda v: v%3
# digit layout
pos={}; D=0
for j,(a,b) in enumerate(ch):
    if j in good and not free: pos[j]=(D,); D+=1
    else: pos[j]=(D,D+1); D+=2
def vec(entries):          # entries: dict x -> value ; must be proportional to c' on restricted cherries
    v=[0]*D
    for j,(a,b) in enumerate(ch):
        if len(pos[j])==1:
            s=entries[a]*c[a]; assert entries[b]*c[b]==s; v[pos[j][0]]=f3(s)
        else: v[pos[j][0]]=f3(entries[a]); v[pos[j][1]]=f3(entries[b])
    return v
gens=[]
for j,(a,b) in enumerate(ch):
    if len(pos[j])==2:
        for x in (0,1):
            for m in (1,2):
                g=[0]*D; g[pos[j][x]]=m; gens.append(g)
nodes=[]; size=2
while size<=N:
    nodes+= [list(range(s,s+size)) for s in range(0,N,size)]; size*=2
for B in nodes:
    for m in (1,2):
        e={x:(m*c[x] if x in B else 0) for x in range(N)}; gens.append(vec(e))
rows=[y for y in range(N) if (y&1)==cls]
print(3,D,len(gens),len(rows))
for g in gens: print(*g)
for y in rows:
    h=[(-1)**bin(y&x).count('1') for x in range(N)]
    print(2,*vec({x:h[x] for x in range(N)}),*vec({x:-h[x] for x in range(N)}))
print(*vec({x:c[x] for x in range(N)}))
