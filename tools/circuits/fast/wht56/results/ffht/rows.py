# rows.py -- print the tables of README.md in this folder from the raw timing outputs.
# Standard library only:  python3 -B rows.py
# It reads style-generator/out/time-float-run1.txt, time-double-run1.txt and time-redo-run1.txt
# (FFHT and FFHT with the step changed; a size that was timed a second time is taken from the
# second timing) and plain-c/time-run1.txt, time-run2.txt (my plain C beside FFHT).
# Times are nanoseconds per point, best (median).  ffht = FFHT as built by its own Makefile,
# gT = FFHT built a second time, g20x = 20 operations exact, g20s = 20 operations with the output
# left divided, g19f = 19 operations with fused multiply-add; t8, k8, k8raw = my plain C.
import os
B=os.path.join(os.path.dirname(os.path.abspath(__file__)),'')   # this folder
def parse(path):
    d={}
    for line in open(path):
        if line[:2] in ('T ','B '):
            kv=dict(x.split('=',1) for x in line.split()[1:] if '=' in x)
            if line[0]=='T': d[(kv['type'],int(kv['k']),kv['variant'])]=(float(kv['min']),float(kv['med']))
            else: d[(kv['type'],int(kv['k']),'_B')]=(int(kv['repeats']),int(kv['bytes']))
    return d
g={'float':parse(B+'style-generator/out/time-float-run1.txt'),'double':parse(B+'style-generator/out/time-double-run1.txt')}
redo=parse(B+'style-generator/out/time-redo-run1.txt')
rk={k for (t,k,v) in redo}
def size(b):
    for u,s in (('GiB',2**30),('MiB',2**20),('KiB',2**10)):
        if b>=s: return f"{b//s} {u}"
    return f"{b} B"
def src(t,k): return redo if (t=='float' and k in rk) else g[t]
for t in ('float','double'):
    print('\n###',t)
    print('| k | array | repeats | FFHT | FFHT built again | 20 operations, exact | 20 operations, output divided | 19 operations fused, exact | more time than "built again": 20 exact / divided / 19 fused | band |')
    print('|---|---|---|---|---|---|---|---|---|---|')
    for k in (3,6,9,12,15,18,21,24,26):
        s=src(t,k); gt=s[(t,k,'gT')][0]
        c=lambda v: f"{s[(t,k,v)][0]:.3f} ({s[(t,k,v)][1]:.3f})"
        d=lambda v: f"{100*(s[(t,k,v)][0]/gt-1):+.1f} %"
        if k==3: diff='step not used: all five run the same instructions (n.d.)'; band='±2 points'
        elif k>=20: diff='† no figure for one size'; band='±5 points'
        else: diff=f"{d('g20x')} / {d('g20s')} / {d('g19f')}"; band='±2 points'
        print(f"| {k} | {size(s[(t,k,'_B')][1])} | {s[(t,k,'_B')][0]} | {c('ffht')} | {c('gT')} | {c('g20x')} | {c('g20s')} | {c('g19f')} | {diff} | {band} |")
    # means
    for lo,hi in ((20,26),):
        out=[]
        for v in ('g20x','g20s','g19f'):
            xs=[100*(src(t,k)[(t,k,v)][0]/src(t,k)[(t,k,'gT')][0]-1) for k in range(lo,hi+1)]
            out.append(f"{v} mean {sum(xs)/len(xs):+.1f} ({min(xs):+.1f}..{max(xs):+.1f})")
        print('mean 2^20..2^26:',' ; '.join(out))
    lo=7 if t=='float' else 6
    for v in ('g20x','g20s','g19f'):
        xs=[100*(src(t,k)[(t,k,v)][0]/src(t,k)[(t,k,'gT')][0]-1) for k in range(lo,20)]
        print(f"  {v} 2^{lo}..2^19: {min(xs):+.1f}..{max(xs):+.1f}")
b1=parse(B+'plain-c/time-run1.txt'); b2=parse(B+'plain-c/time-run2.txt')
for t in ('float','double'):
    print('\n### plain C',t)
    print('| k | FFHT | my plain C, textbook step | new step, exact | new step, output divided | textbook C ÷ FFHT | new exact ÷ textbook | new divided ÷ textbook |')
    print('|---|---|---|---|---|---|---|---|')
    for k in (3,6,9,12,15,18,21,24,27):
        c=lambda v: f"{b1[(t,k,v)][0]:.3f} ({b1[(t,k,v)][1]:.3f})"
        r=lambda a,b_: ', '.join(f"{x[(t,k,a)][0]/x[(t,k,b_)][0]:.2f}" for x in (b1,b2))
        print(f"| {k} | {c('ffht')} | {c('t8')} | {c('k8')} | {c('k8raw')} | {r('t8','ffht')} | {r('k8','t8')} | {r('k8raw','t8')} |")
    for k in (10,11):
        print('  neighbours k=%d: k8/t8 %s ; k8raw/t8 %s'%(k, ', '.join(f"{x[(t,k,'k8')][0]/x[(t,k,'t8')][0]:.2f}" for x in (b1,b2)), ', '.join(f"{x[(t,k,'k8raw')][0]/x[(t,k,'t8')][0]:.2f}" for x in (b1,b2))))
