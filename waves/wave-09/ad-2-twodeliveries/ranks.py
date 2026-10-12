# ad-2: for every minimum (12-gate) circuit for Z at 8 points over the TWO-ELEMENT FIELD (ab-4's list of 2,802 wire sets,
# every acyclic derivation), the rank of the consumer-slot transfers of each wire = the longest bus with no idle injection.
import sys, os, collections, itertools
sys.argv=[sys.argv[0],'8',sys.argv[1]]
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'deco.py')).read()
exec(src.split("proc=subprocess.Popen")[0])
tot=collections.Counter(); prof=collections.Counter(); nd=0; sets=0; best=[]
for circ in circuits():
    nd+=1
    wires,sig,slots=transfers(circ)
    rk=[]
    for w in wires:
        bs=[]
        for _,_,s in slots[w]:
            r=insert(bs,s)
            if r: bs.append(r)
        rk.append(len(bs))
    tot[max(rk)]+=1
    cap=sum(max(0,r-2) for r in rk)     # sum over wires of (rank - 2)+ : the most the buses could save net with one delivery each
    prof[(max(rk),cap)]+=1
    if max(rk)>=5 or cap>=4: best.append((max(rk),cap,circ))
print('derivations of minimum circuits for Z at 8 points:',nd)
print('largest slot rank of a wire -> number of derivations:',dict(sorted(tot.items())))
print('(largest rank, sum over wires of (rank-2)+) -> count:',dict(sorted(prof.items())))
best.sort(key=lambda t:(-t[1],-t[0]))
for mr,cap,circ in best[:4]:
    print('rank',mr,'capacity',cap,[(format(f,'08b')[::-1],format(u,'08b')[::-1],format(v,'08b')[::-1]) for f,(u,v) in circ])
