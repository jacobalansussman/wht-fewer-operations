# graphs.py k maxm [maxedges]: the fine dial.  For every graph G on k bits (up to renaming the bits): the matrix
# "affine function + sum over the edges ij of G of c_ij y_i y_j, at all 2^k cube points" (rank k + 1 + edges),
# least gates over the two-element field by mincirc2 (m = helpers raised until YES, up to maxm).
import sys, subprocess, itertools
k=int(sys.argv[1]); maxm=int(sys.argv[2]); maxe=int(sys.argv[3]) if len(sys.argv)>3 else 99
pairs=list(itertools.combinations(range(k),2))
seen={}
for r in range(len(pairs)+1):
    for E in itertools.combinations(pairs,r):
        canon=min(tuple(sorted(tuple(sorted((p[a],p[b]))) for a,b in E)) for p in itertools.permutations(range(k)))
        if canon in seen: continue
        seen[canon]=1
        if len(E)>maxe: continue
        sets=[0]+[1<<i for i in range(k)]+[(1<<a)|(1<<b) for a,b in canon]
        pad=len(sets)%2
        rows='\n'.join(' '.join(str(1 if (s&y)==s else 0) for s in sets)+' 0'*pad for y in range(1<<k))+'\n'
        fn='g_k%d_%s.rows'%(k,'_'.join('%d%d'%e for e in canon) or 'empty')
        open(fn,'w').write(rows)
        deg=[sum(1 for e in canon if v in e) for v in range(k)]
        tri=sum(1 for a,b,c in itertools.combinations(range(k),3) if all(tuple(sorted(x)) in canon for x in ((a,b),(a,c),(b,c))))
        res='> %d helpers (not decided)'%maxm
        for m in range(0,maxm+1):
            out=subprocess.run(['./mincirc2','2',str(len(sets)+pad),str(m),fn],capture_output=True,text=True).stdout
            if 'YES' in out:
                res='%d helpers'%m; open(fn.replace('.rows','.sol'),'w').write(out); break
        print('k=%d edges=%d rank=%d graph=%s degrees=%s triangles=%d : gates = %d outputs + %s'%(k,len(canon),k+1+len(canon),' '.join('%d%d'%e for e in canon) or '-',sorted(deg,reverse=True),tri,(1<<k)-1,res),flush=True)
