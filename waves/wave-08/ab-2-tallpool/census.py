# census.py : in a known circuit for the transform, which TALL wires are a sum or difference of two wires of the circuit,
# and how many pairs of wires does each such tall wire connect?  (Section 3 of ab-2.md: a tall "translation" pays only when
# it serves two or more pairs.)  Input: the helper list of x-0-twojobs (one wire per line); inputs and outputs are added.
import sys, math, itertools
def prim(v):
    g=0
    for x in v: g=math.gcd(g,abs(x))
    if not g: return None
    s=next(x for x in v if x); s=1 if s>0 else -1
    return tuple(s*x//g for x in v)
H=[tuple(int(x) for x in l.split()) for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
N=len(H[0]); wires=[tuple(1 if i==j else 0 for j in range(N)) for i in range(N)]+[prim(h) for h in H]
wires+=[tuple((-1)**bin(j&x).count('1') for x in range(N)) for j in range(N)]
wires=list(dict.fromkeys(wires))
cnt={}
for u,v in itertools.combinations(wires,2):
    for sg in (1,-1):
        d=prim(tuple(a+sg*b for a,b in zip(u,v)))
        if d and max(abs(x) for x in d)>=2: cnt.setdefault(d,[]).append((u,v,sg))
mult={}
for d,l in cnt.items(): mult[len(l)]=mult.get(len(l),0)+1
print('# %s: N=%d, %d wires; tall wires that are a sum or difference of two wires of the circuit: %d; by number of pairs they connect: %s'%(sys.argv[1],N,len(wires),len(cnt),sorted(mult.items())))
best=sorted(cnt.items(),key=lambda kv:(-len(kv[1]),sum(1 for x in kv[0] if x)))[:6]
for d,l in best:
    print('  tall %s  support %d  connects %d pairs; first two: %s'%(d,sum(1 for x in d if x),len(l),[(u,v,sg) for u,v,sg in l[:2]]))
# the same count for differences that are NOT tall (a form, or twice a form: the flips), for contrast
cf={}
for u,v in itertools.combinations(wires,2):
    for sg in (1,-1):
        d=prim(tuple(a+sg*b for a,b in zip(u,v)))
        if d and max(abs(x) for x in d)==1: cf.setdefault(d,[]).append((u,v,sg))
mf={}
for d,l in cf.items(): mf[len(l)]=mf.get(len(l),0)+1
print('# forms that are a sum or difference of two wires of the circuit: %d; by number of pairs they connect: %s'%(len(cf),sorted(mf.items())))
