# ad-2: census of PAIRS of free forms at 8 points, TWO-ELEMENT FIELD, count (G).  s(W) = 12 - least gates for Z_8 given W free.
import collections, glob, os
here=os.path.dirname(os.path.abspath(__file__))
single={}
for l in open(os.path.join(here,'single8.txt')):
    if l[0]=='#': continue
    w,g=map(int,l.split()); single[w]=12-g
pair={}
for f in sorted(glob.glob(os.path.join(here,'p[ABC][12].txt'))):
    for l in open(f):
        if l[0]=='#': continue
        a,b,g=map(int,l.split()); pair[(a,b)]=12-g
print('singles',len(single),'pairs',len(pair))
name=lambda w:'+'.join('x%d'%i for i in range(8) if (w>>i)&1)
s1=lambda w: single.get(w,0)      # an input or 0 saves nothing
print('pair saving -> count:',dict(sorted(collections.Counter(pair.values()).items())))
# compare with the two singles and with the third form of the line (a+b), which one gate makes from the pair
tab=collections.Counter(); sup=[]; gen=[]
for (a,b),s in pair.items():
    add=s1(a)+s1(b); c=a^b
    best1=max(s1(a),s1(b),s1(c)-1)       # use one of the two, or spend a gate on the third form
    tab[(s-add)]+=1
    if s>add: sup.append((a,b,s))
    # "genuine": more than additive AND not explained by the third form alone or by third + one of the two
    expl=max(add, s1(c)-1, )
    if s>add:
        gen.append((a,b,s,s1(a),s1(b),s1(c)))
print('pair saving minus (sum of the two single savings) -> count:',dict(sorted(tab.items())))
print('pairs with saving above the sum of the two:',len(sup))
# explain: third form c=a+b costs one gate; its own saving s1(c); pairs (a,c),(b,c) too
kinds=collections.Counter()
unexpl=[]
for a,b,s,sa,sb,sc in gen:
    # the best one can say from singles plus the pair census on the line {a,b,c}: the pair spans the line, so
    # s(a,b) >= s(a,c)-1 and s(b,c)-1 when c is not an input; and s(a,b)>=s(c)-1
    kinds[(sa,sb,sc,s)]+=1
print('more-than-additive pairs by (s(a), s(b), s(a+b), s(pair)):')
for k,v in sorted(kinds.items()): print('  ',k,v)
print('max pair saving',max(pair.values()))
top=[(a,b) for (a,b),s in pair.items() if s==max(pair.values())]
print('pairs at the maximum:',len(top))
for a,b in top[:40]: print('   s=%d  [%d,%d,%d]  %s  |  %s   | third: %s'%(pair[(a,b)],s1(a),s1(b),s1(a^b),name(a),name(b),name(a^b)))
# line view: a 2-dimensional space {a,b,c}: saving of the line = max over its three pairs; is it more than the best "one form + its cost" story?
lines={}
for (a,b),s in pair.items():
    key=tuple(sorted((a,b,a^b))); lines[key]=max(lines.get(key,0),s)
cnt=collections.Counter()
for key,s in lines.items():
    m=max(s1(w) for w in key); cnt[(m,s)]+=1
print('planes spanned (three forms a,b,a+b): (best single saving in it, best pair saving) -> count')
for k,v in sorted(cnt.items()): print('  ',k,v)
# strict superadditivity not due to the third form: pairs where all three of a,b,a+b have s<=... and s(pair) > s(a)+s(b) and s(pair) > s(a^b)-1+max(s(a),s(b))... print the cleanest: both singles save 0 or 1, third saves <= 1
clean=[(a,b,s) for a,b,s,sa,sb,sc in gen if s>max(sa+sb, sc-1+max(sa,sb), sc)]
print('pairs whose saving beats  max(s(a)+s(b), s(a+b)-1+max(s(a),s(b)), s(a+b)) :',len(clean))
for a,b,s in clean[:30]: print('   s=%d  [%d,%d,%d]  %s  |  %s  | third: %s'%(s,s1(a),s1(b),s1(a^b),name(a),name(b),name(a^b)))
# NET worth of two deliveries in a cut: s(pair) - 2 (two cancelling gates) against best single net s-1
net=collections.Counter()
for (a,b),s in pair.items(): net[(max(s1(a),s1(b))-1, s-2)]+=1
print('(best single net = s-1, pair net = s-2) -> count:')
for k,v in sorted(net.items()): print('  ',k,v)
