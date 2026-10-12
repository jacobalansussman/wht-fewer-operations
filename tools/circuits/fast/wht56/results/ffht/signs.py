# signs.py -- the sign of every comparison between FFHT and FFHT with the step changed.
# Standard library only:  python3 -B signs.py
# For the 129 combinations of size and form (2^6 to 2^26 points in single precision, 2^5 to 2^26
# in double precision; three forms) it prints the smallest and the largest difference in per
# cent, and the list of combinations in which the changed FFHT did NOT take more time:
#   "best vs gT"     best time against the best time of FFHT built a second time (the comparison
#                    of README.md: the list is empty)
#   "median vs gT"   the same with medians
#   "best vs ffht", "median vs ffht"   against the first build of FFHT
import os
B=os.path.join(os.path.dirname(os.path.abspath(__file__)),'')   # this folder
def parse(path):
    d={}
    for line in open(path):
        if line.startswith('T '):
            kv=dict(x.split('=',1) for x in line.split()[1:] if '=' in x)
            d[(kv['type'],int(kv['k']),kv['variant'])]=(float(kv['min']),float(kv['med']))
    return d
g={'float':parse(B+'style-generator/out/time-float-run1.txt'),'double':parse(B+'style-generator/out/time-double-run1.txt')}
redo=parse(B+'style-generator/out/time-redo-run1.txt'); rk={k for (t,k,v) in redo}
n=0; bb=[]; mm=[]; mf=[]; bf=[]
for t,lo in (('float',6),('double',5)):
    for k in range(lo,27):
        s=redo if (t=='float' and k in rk) else g[t]
        for v in ('g20x','g20s','g19f'):
            n+=1
            bb.append((100*(s[(t,k,v)][0]/s[(t,k,'gT')][0]-1),t,k,v))
            mm.append((100*(s[(t,k,v)][1]/s[(t,k,'gT')][1]-1),t,k,v))
            bf.append((100*(s[(t,k,v)][0]/s[(t,k,'ffht')][0]-1),t,k,v))
            mf.append((100*(s[(t,k,v)][1]/s[(t,k,'ffht')][1]-1),t,k,v))
print(n,'cells')
for name,x in (('best vs gT',bb),('median vs gT',mm),('best vs ffht',bf),('median vs ffht',mf)):
    print(name,'min',min(x),'max',max(x),'cells <= 0:',[c for c in x if c[0]<=0.0])
