#!/usr/bin/env python3
# e-2-density/forest.py: part (b). Which 6-subsets T of the 16 addresses are information sets of the (-4)-eigenspace of the bent form
# G[v][w] = (-1)^f(v+w), f = x0x1 + x2x3, and what decides the number of entries of the encoder (30, 34, 39, 60).
# Exact rational arithmetic.
import itertools, collections
from fractions import Fraction as Fr
N=16
def f(v): return ((v&1)&((v>>1)&1))^(((v>>2)&1)&((v>>3)&1))
G=[[(-1)**f(v^w) for w in range(N)] for v in range(N)]
U1=[0,7,11,12]; U2=[0,3,13,14]
assert all((a^b) in U1 for a in U1 for b in U1) and all((a^b) in U2 for a in U2 for b in U2)
assert sorted(set(U1+U2)-{0})==[v for v in range(N) if f(v)]
rows=sorted({tuple(sorted(v^u for u in U1)) for v in range(N)}); cols=sorted({tuple(sorted(v^u for u in U2)) for v in range(N)})
row={v:i for i,c in enumerate(rows) for v in c}; col={v:i for i,c in enumerate(cols) for v in c}
assert len({(row[v],col[v]) for v in range(N)})==16
print("[ran] the 16 addresses form a 4 x 4 grid: rows = cosets of U1 =",U1,", columns = cosets of U2 =",U2)
A1=[[1 if (v^w) in U1 else 0 for w in range(N)] for v in range(N)]; A2=[[1 if (v^w) in U2 else 0 for w in range(N)] for v in range(N)]
assert all(G[v][w]==(4 if v==w else 0)+1-2*(A1[v][w]+A2[v][w]) for v in range(N) for w in range(N))
print("[ran] G = 4 I + J - 2 (row-sum matrix + column-sum matrix): output(cell) = 4 x(cell) + total - 2 (its row sum) - 2 (its column sum)")
gen=[]
for i in range(3): gen.append([ (1 if row[v]==i else 0)-(1 if row[v]==3 else 0) for v in range(N)])
for j in range(3): gen.append([ (1 if col[v]==j else 0)-(1 if col[v]==3 else 0) for v in range(N)])
for g in gen: assert [sum(G[v][w]*g[w] for w in range(N)) for v in range(N)]==[-4*x for x in g]
print("[ran] the (-4)-eigenspace (dimension 6) = all tables a(row) + b(column) with sum a = 0 = sum b")
def systematic(T):
    M=[[Fr(x) for x in r] for r in gen]
    for j,c in enumerate(T):
        p=next((i for i in range(j,6) if M[i][c]!=0),None)
        if p is None: return None
        M[j],M[p]=M[p],M[j]; inv=1/M[j][c]; M[j]=[x*inv for x in M[j]]
        for i in range(6):
            if i!=j and M[i][c]!=0:
                fct=M[i][c]; M[i]=[a-fct*b for a,b in zip(M[i],M[j])]
    return M
def comps(T):
    par=list(range(8))
    def find(a):
        while par[a]!=a: a=par[a]
        return a
    cyc=False
    for v in T:
        a,b=find(row[v]),find(4+col[v])
        if a==b: cyc=True
        else: par[a]=b
    cl=collections.defaultdict(list)
    for x in range(8): cl[find(x)].append(x)
    return cyc,sorted((sum(1 for x in c if x<4),sum(1 for x in c if x>=4)) for c in cl.values())
hist=collections.Counter(); agree=0; ninfo=0; detail=collections.defaultdict(collections.Counter)
colw=collections.defaultdict(collections.Counter)
for T in itertools.combinations(range(N),6):
    cyc,cs=comps(T)
    pred=(not cyc) and len(cs)==2 and cs[0][0]!=cs[0][1]
    S=systematic(T)
    assert pred==(S is not None)
    if S is None: continue
    ninfo+=1
    nz=sum(1 for r in S for x in r if x!=0)-6
    deg=collections.Counter()
    for v in T: deg[row[v]]+=1; deg[4+col[v]]+=1
    key=(tuple(cs), tuple(sorted(deg[x] for x in range(4))), tuple(sorted(deg[x] for x in range(4,8))))
    detail[key][nz]+=1; hist[nz]+=1
    colw[nz][tuple(sorted(sum(1 for x in r if x!=0) for r in S))]+=1
print("[ran] information sets:",ninfo,"; T is one  <=>  its 6 cells, read as edges between 4 row-nodes and 4 column-nodes, form two trees")
print("      covering all 8 nodes, and the first tree does not have as many rows as columns. (checked on all 8008 subsets)")
print("[ran] encoder sizes:",sorted(hist.items()))
print("[ran] by shape: (rows,columns) of the two trees | row degrees | column degrees -> sizes")
for k in sorted(detail): print("   ",k,dict(detail[k]))
print("[ran] weights of the 6 codewords of the systematic generator (1 + column weight of the encoder), by encoder size:")
for nz in sorted(colw): print("   ",nz,dict(colw[nz]))
