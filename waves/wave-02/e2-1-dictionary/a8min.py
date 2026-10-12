# e2-1-dictionary / a8min.py : least gate count (G) of the bridge for one representative of every coarse class, with ../d-0-zeta/mincirc over GF(p).
# D4 (rational entries): p = 5 and 7.  Q8 (Gaussian entries): p = 5 with i -> 2.   A YES is a candidate circuit modulo p; a NO is exhaustive modulo p only.
import json, subprocess, sys, time
MC="waves/wave-01/d-0-zeta/mincirc"
def run(rows,p,m,tmo):
    fn=f"rows_tmp_{p}.txt"
    open(fn,"w").write("\n".join(" ".join(str(v) for v in r) for r in rows)+"\n")
    try:
        o=subprocess.run([MC,str(p),"8",str(m),fn],capture_output=True,text=True,timeout=tmo).stdout
    except subprocess.TimeoutExpired:
        return "TIMEOUT",""
    hdr=[l for l in o.splitlines() if l.startswith("p=")]
    res=[l for l in o.splitlines() if l.startswith("RESULT")]
    return (res[0] if res else "??"), (hdr[0] if hdr else "")
for name,primes in (("D4",(5,7)),("Q8",(5,))):
    cl=json.load(open(f"a8_{name}_classes.json"))
    for idx in sorted(cl,key=int):
        c=cl[idx]
        for ri,rep in enumerate(c["reps"][: (2 if int(idx)<2 else 1)]):
            B=rep["B"]
            for p in primes:
                im={5:2,7:None}[p]
                rows=[[ (a+(im or 0)*b)%p for (a,b) in row] for row in B]
                nonunit=sum(1 for r in rows if sum(1 for v in r if v)>1)
                # rank check mod p (the bridge must stay invertible)
                M=[r[:] for r in rows]; rk=0
                for col in range(8):
                    piv=next((i for i in range(rk,8) if M[i][col]),None)
                    if piv is None: continue
                    M[rk],M[piv]=M[piv],M[rk]; inv=pow(M[rk][col],p-2,p)
                    M[rk]=[v*inv%p for v in M[rk]]
                    for i in range(8):
                        if i!=rk and M[i][col]: f=M[i][col]; M[i]=[(a-f*b)%p for a,b in zip(M[i],M[rk])]
                    rk+=1
                line=f"{name} class {idx} {c['key']} rep {ri} sigma={rep['sigma']} p={p} rank={rk} non-unit rows={nonunit}:"
                got=None
                for m in range(0,7):
                    t=time.time(); res,hdr=run(rows,p,m,40)
                    line+=f" m={m}:{'YES' if 'YES' in res else ('NO' if 'NO' in res else res)}({time.time()-t:.1f}s)"
                    if "YES" in res: got=(hdr,res); break
                    if res=="TIMEOUT": break
                print(line); 
                if got: print("     ",got[0]," -> ",got[1])
                sys.stdout.flush()
