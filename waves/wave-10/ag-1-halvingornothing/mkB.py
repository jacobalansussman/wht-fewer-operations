# ag-1: the block B (16 points): rows = odd-weight outputs, columns = even-weight inputs; entry 1 iff addresses differ in one bit.
# code of a form modulo 2 = row read as a binary number, first entry = highest bit (lift.c's convention).
import itertools, sys
E=[a for a in range(16) if bin(a).count('1')%2==0]
O=[a for a in range(16) if bin(a).count('1')%2==1]
rows=[[1 if bin(e^y).count('1')==1 else 0 for e in E] for y in O]
with open('rows_B4.txt','w') as f:
    for r in rows: f.write(' '.join(map(str,r))+'\n')
def code(r): 
    c=0
    for v in r: c=(c<<1)|(v&1)
    return c
T=[code(r) for r in rows]
print('targets',T)
# symmetry group acting on input positions
def permbits(a,p): return sum(((a>>i)&1)<<p[i] for i in range(4))
G=set()
for p in itertools.permutations(range(4)):
    for s in E:
        g=tuple(E.index(permbits(e,p)^s) for e in E)   # input i -> position g[i]
        G.add(g)
print('group order',len(G))
def act(g,w):
    r=0
    for i in range(8):
        if (w>>(7-i))&1: r|=1<<(7-g[i])
    return r
# check targets are permuted
for g in G: assert sorted(act(g,t) for t in T)==sorted(T)
seen={}; reps=[]
for w in range(1,256):
    if w in seen: continue
    orb={act(g,w) for g in G}
    for x in orb: seen[x]=w
    reps.append((w,len(orb)))
print('orbits of non-zero forms:',len(reps))
with open('w_orbits.txt','w') as f:
    for w,l in reps: f.write(f'{w} {l} {bin(w).count("1")} {"T" if w in T else ""}\n')
print(open('w_orbits.txt').read())
