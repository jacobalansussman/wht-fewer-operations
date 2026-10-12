# p-8-fibonacci/replay.py : turn sign-point Steiner trees (output of dws ... w) into an explicit circuit and replay it EXACTLY.
# Usage: replay.py K "<N-1 internal masks>" cmask witnessfile [witnessfile ...]     (one witness file per group of rows)
# Count (G): a gate is any a*u + b*v, scalings free.  Gates = (N - 1) merges on the inputs + one gate per edge of the trees.
import sys
K=int(sys.argv[1]); N=1<<K
internal=[int(m) for m in sys.argv[2].split()]; cm=int(sys.argv[3])
sgn=lambda mask,x: -1 if mask>>x&1 else 1
c=[sgn(cm,x) for x in range(N)]
nodes=set(internal)|{1<<i for i in range(N)}
# 1. laminar check and the input merge tree
ordered=sorted(internal,key=lambda m: bin(m).count('1'))
form={1<<i:[c[i] if j==i else 0 for j in range(N)] for i in range(N)}   # scaled inputs: free in count (G)
gates=0; lines=[]
for m in ordered:
    kids=[b for b in nodes if b!=m and b&m==b and not any(b2!=b and b2!=m and b&b2==b and b2&m==b2 for b2 in nodes)]
    assert len(kids)==2 and kids[0]|kids[1]==m and kids[0]&kids[1]==0, ("not a binary merge tree",m,kids)
    form[m]=[a+b for a,b in zip(form[kids[0]],form[kids[1]])]; gates+=1
    lines.append("f%d = f%d + f%d"%(m,kids[0],kids[1]))
assert form[(1<<N)-1]==c
# 2. the trees: values at points
vec=lambda p:[sgn(p,x) for x in range(N)]
val={cm:form[(1<<N)-1]}          # the point c' IS the root form: no gate
edges=[]; terms=[]
for fn in sys.argv[4:]:
    for l in open(fn):
        t=l.split()
        if t and t[0]=='edge': edges.append((int(t[1]),int(t[3]),int(t[5])))
        if t and t[0]=='terminal': terms.append(int(t[3]))
edges=list(dict.fromkeys(edges))
pending=edges[:]; used=0
while pending:
    prog=False
    for e in pending[:]:
        u,v,B=e
        for a,b in ((u,v),(v,u)):
            if a in val and b not in val:
                d=[q-p for p,q in zip(vec(a),vec(b))]
                lam=set(d[x]//c[x] for x in range(N) if B>>x&1)
                assert B in nodes and all(d[x]==0 for x in range(N) if not B>>x&1) and len(lam)==1 and 0 not in lam, ("bad edge",e)
                lam=lam.pop()
                val[b]=[p+lam*f for p,f in zip(val[a],form[B])]; gates+=1; used+=1
                lines.append("p%d = p%d %+d*f%d"%(b,a,lam,B)); pending.remove(e); prog=True; break
            elif a in val and b in val and e in pending:
                pending.remove(e); prog=True; break     # duplicate point reached twice: drop the edge (still a tree)
    assert prog, "tree not connected to the centre"
# 3. exact replay: the value at every point must be the point itself as a linear form, and every row must be present up to sign
for p,v in val.items(): assert v==vec(p)
rows={}
for y in range(N):
    h=[(-1)**bin(y&x).count('1') for x in range(N)]
    for p,v in val.items():
        if v==h: rows[y]=(+1,p)
        elif v==[-a for a in h]: rows.setdefault(y,(-1,p))
missing=[y for y in range(N) if y not in rows]
tau=1+used
print("points",N," edges used",used," tau = 1 + edges =",tau," gates (G) = N-1 + edges =",gates," [N-2+tau =",N-2+tau,"]")
print("all rows of the transform present up to sign:",not missing, " missing:",missing)
sizes={}
for l in lines:
    if l.startswith('p'):
        B=int(l.split('f')[-1]); s=bin(B).count('1'); sizes[s]=sizes.get(s,0)+1
print("edges by node size:",dict(sorted(sizes.items())), " internal nodes used:",len({int(l.split('f')[-1]) for l in lines if l.startswith('p') and bin(int(l.split('f')[-1])).count('1')>1}),"of",N-1)
if '--print' in sys.argv or True:
    open(sys.argv[4]+'.circuit.txt','w').write("\n".join(lines+["y%d = %+d * p%d"%(y,rows[y][0],rows[y][1]) for y in sorted(rows)])+"\n")
