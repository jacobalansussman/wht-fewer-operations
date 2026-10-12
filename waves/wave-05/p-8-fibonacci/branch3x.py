# 16 points, modulo 3, rows constant on cherries (class 0), centre c' = (-1)^(x0 x3 + extra), start at the ORIGIN.
# Optional second profiles ("alt forms") on the wrong half: bit 0..3 = alt cherry 4..7, bit 4 = alt quad (4,5), bit 5 = alt quad (6,7),
# bit 6 = alt half, bit 7 = alt root (c' on the good half, alt profile on the wrong half).  Each alt form costs one gate.
# usage: branch3x.py cfg [x1x3]    -> input for dwg; branch cost = (dwg result - 1) + number of alt forms.
import sys
cfg=int(sys.argv[1]); extra=len(sys.argv)>2; N=16
c=[(-1)**(((x&1)*(x>>3&1))+((x>>1&1)*(x>>3&1) if extra else 0)) for x in range(N)]
ch=[(2*j,2*j+1) for j in range(8)]
good=[j for j,(a,b) in enumerate(ch) if c[a]==c[b]]; wrong=[j for j in range(8) if j not in good]
assert wrong==[4,5,6,7]
alt=[c[x] if (x%2==0 or x<8) else -c[x] for x in range(N)]       # second profile: b-entry negated on wrong cherries
pos={}; D=0
for j in range(8):
    if j in good: pos[j]=(D,); D+=1
    else: pos[j]=(D,D+1); D+=2
def vec(e):
    v=[0]*D
    for j,(a,b) in enumerate(ch):
        if len(pos[j])==1:
            s=e[a]*c[a]; assert e[b]*c[b]==s; v[pos[j][0]]=s%3
        else: v[pos[j][0]]=e[a]%3; v[pos[j][1]]=e[b]%3
    return v
gens=[]
for j in wrong:
    for x in (0,1):
        for m in (1,2):
            g=[0]*D; g[pos[j][x]]=m; gens.append(g)
nodes=[]; size=2
while size<=N:
    nodes+=[list(range(s,s+size)) for s in range(0,N,size)]; size*=2
for B in nodes:
    for m in (1,2): gens.append(vec({x:(m*c[x] if x in B else 0) for x in range(N)}))
altnodes=[[8,9],[10,11],[12,13],[14,15],[8,9,10,11],[12,13,14,15],list(range(8,16)),list(range(16))]
for i,B in enumerate(altnodes):
    if cfg>>i&1:
        for m in (1,2): gens.append(vec({x:(m*alt[x] if x in B else 0) for x in range(N)}))
rows=list(range(0,16,2))
print(3,D,len(gens),len(rows))
for g in gens: print(*g)
for y in rows:
    h=[(-1)**bin(y&x).count('1') for x in range(N)]
    print(2,*vec({x:h[x] for x in range(N)}),*vec({x:-h[x] for x in range(N)}))
print(*([0]*D))
