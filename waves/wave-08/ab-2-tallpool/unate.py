# unate.py : which of the target sets where a tall wire saves a gate are, after changing signs of inputs and of targets,
# matrices with entries 0 and 1 only (no minus sign at all, like the subset-sum matrix Z)?
import sys, re, itertools
tot=0; unate=0; ex=[]
for fn in sys.argv[1:]:
    for line in open(fn):
        if not line.startswith('SAVE '): continue
        T=[tuple(int(x) for x in s.split(',')) for s in re.findall(r'\(([-\d,]+)\)',line.split('forms:')[0])]
        tot+=1; n=len(T[0]); ok=False
        for cs in itertools.product((1,-1),repeat=n):
            if all(all(cs[i]*t[i]>=0 for i in range(n)) or all(cs[i]*t[i]<=0 for i in range(n)) for t in T): ok=True; break
        if ok: unate+=1; ex.append((fn,T))
print('# target sets with a tall saving: %d; equivalent to a matrix of zeros and ones: %d'%(tot,unate))
for fn,T in ex[:5]: print('  ',fn,T)
