# lines.py : for every SAVE line, how many lines through two TARGETS pass through each tall helper, and is the tall helper
# a plain sum or difference of two targets (the "two tails" picture)?
import sys, re, math, itertools
def comb(u,v,w):
    n=len(u)
    for i in range(n):
        for j in range(i+1,n):
            D=u[i]*v[j]-u[j]*v[i]
            if D:
                a=w[i]*v[j]-w[j]*v[i]; b=u[i]*w[j]-u[j]*w[i]
                if all(D*w[l]==a*u[l]+b*v[l] for l in range(n)):
                    g=math.gcd(math.gcd(abs(a),abs(b)),abs(D)); return a//g,b//g,D//g
                return None
    return None
tot=0; on_tt=0; pm=0; hist={}; zeros=0; nofull=0
for line in open(sys.argv[1]):
    if not line.startswith('SAVE '): continue
    a,b=line.split('forms:'); fpart,tpart=b.split('| tall:')
    T=[tuple(int(x) for x in s.split(',')) for s in re.findall(r'\(([-\d,]+)\)',a)]
    Hh=[tuple(int(x) for x in s.split(',')) for s in re.findall(r'\(([-\d,]+)\)',tpart)]
    tall=[h for h in Hh if max(abs(x) for x in h)>1]
    tot+=1; best=0; ispm=False
    for p in tall:
        c=0
        for u,v in itertools.combinations(T,2):
            r=comb(u,v,p)
            if r:
                c+=1
                if abs(r[0])==abs(r[1])==1 and abs(r[2])==1: ispm=True
        best=max(best,c)
    hist[best]=hist.get(best,0)+1
    if best: on_tt+=1
    if ispm: pm+=1
    if all(any(x==0 for x in t) for t in T): nofull+=1
print('# %s: examples %d; a tall helper lies on a line through two targets in %d; is a plain sum or difference of two targets in %d; number of target-target lines through the best tall helper: %s; examples in which EVERY target has a zero entry: %d'%(sys.argv[1],tot,on_tt,pm,sorted(hist.items()),nofull))
