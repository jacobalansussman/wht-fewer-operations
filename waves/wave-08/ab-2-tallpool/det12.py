# det12.py : the one 4 x 4 class below the "one unit per gate" floor: find its 6-gate circuit of forms and print the gates.
import itertools, math
from replay_lib import comb
T=[(1,-1,-1,-1),(0,1,-1,-1),(1,1,1,-1),(1,1,-1,1)]
n=4; inputs=[tuple(1 if i==j else 0 for j in range(n)) for i in range(n)]
forms=[]
for v in itertools.product((-1,0,1),repeat=n):
    nz=[x for x in v if x]
    if len(nz)>=2 and nz[0]>0 and v not in T: forms.append(v)
def derive(helpers):
    wires=list(inputs); names=['x%d'%(i+1) for i in range(n)]; todo=[('p%d'%(i+1),h) for i,h in enumerate(helpers)]+[('t%d'%(i+1),t) for i,t in enumerate(T)]; out=[]
    while todo:
        prog=False
        for nm,w in list(todo):
            for i in range(len(wires)):
                for j in range(i+1,len(wires)):
                    c=comb(wires[i],wires[j],w)
                    if c:
                        out.append('%s = (%d*%s + %d*%s)/%d = %s'%(nm,c[0],names[i],c[1],names[j],c[2],w)); wires.append(w); names.append(nm); todo.remove((nm,w)); prog=True; break
                if prog: break
            if prog: break
        if not prog: return None
    return out
cnt=0
for hs in itertools.combinations(forms,2):
    o=derive(hs)
    if o:
        cnt+=1
        if cnt==1: print('\n'.join(o))
print('# pairs of form helpers that give all four targets:',cnt,' (6 gates; one-unit floor 3 + log2 12 = %.3f)'%(3+math.log2(12)))
print('# with one helper:',sum(1 for h in forms if derive((h,))))
