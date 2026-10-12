# census_walks.py : the census of census.py on every circuit printed by the walker tj (x-0's runs and mine): for each
# circuit, how many tall sums or differences of two of its wires occur for two or more pairs?  Also: does the circuit hold a
# tall wire, and is a tall wire OF the circuit a sum or difference of two or more pairs of its other wires?
import sys, re, math, itertools
def prim(v):
    g=0
    for x in v: g=math.gcd(g,abs(x))
    if not g: return None
    s=next(x for x in v if x); s=1 if s>0 else -1
    return tuple(s*x//g for x in v)
tot={}; 
for fn in sys.argv[1:]:
    cur=None; circs=[]
    for line in open(fn, errors='ignore'):
        if line.startswith('CIRCUIT'):
            m=re.search(r'N=(\d+) gates=(\d+)',line); cur={'N':int(m.group(1)),'g':int(m.group(2)),'w':[]}; circs.append(cur)
        elif cur is not None and line.startswith('w') and '# [' in line:
            cur['w'].append(tuple(int(x) for x in line.split('# [')[1].split(']')[0].split()))
        elif line.startswith('SUMMARY'): cur=None
    for c in circs:
        N=c['N']; wires=[tuple(1 if i==j else 0 for j in range(N)) for i in range(N)]+[prim(w) for w in c['w']]
        wires=list(dict.fromkeys(wires))
        if len(c['w'])!=c['g']: continue
        cnt={}
        for u,v in itertools.combinations(wires,2):
            for sg in (1,-1):
                d=prim(tuple(a+sg*b for a,b in zip(u,v)))
                if d and max(abs(x) for x in d)>=2: cnt[d]=cnt.get(d,0)+1
        rep=sum(1 for d,k in cnt.items() if k>=2); mx=max(cnt.values()) if cnt else 0
        has_tall=sum(1 for w in wires if max(abs(x) for x in w)>=2)
        own=sum(1 for w in wires if max(abs(x) for x in w)>=2 and cnt.get(w,0)>=2)
        key=(N,c['g']); t=tot.setdefault(key,[0,0,0,0,0]); t[0]+=1; t[1]+=(rep>0); t[2]=max(t[2],mx); t[3]+=(has_tall>0); t[4]+=(own>0)
        if rep>0 and len(sys.argv)<40 and t[1]<=2:
            d=max(cnt,key=lambda k:cnt[k]); print('  example: %s N=%d gates=%d: tall %s occurs for %d pairs; circuit holds %d tall wires'%(fn.split('/')[-1],N,c['g'],d,cnt[d],has_tall))
for key in sorted(tot):
    t=tot[key]; print('N=%d, %d gates: circuits %d; with a tall sum or difference that occurs twice or more: %d (largest number of pairs %d); circuits that hold a tall wire: %d; circuits where a tall wire of the circuit itself is such a repeated difference: %d'%(key[0],key[1],t[0],t[1],t[2],t[3],t[4]))
