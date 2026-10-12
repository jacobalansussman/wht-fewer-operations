# w-cross hybrid 4, second try: walk over pairs (A, D) with A whole-number, det +-1, A D A^T = H, D diagonal,
# by two-column moves A -> A g^-1, D -> g D g^T with g a 2 x 2 whole-number matrix of determinant +-1 keeping D diagonal.
import itertools, time, sys
def pop(x): return bin(x).count("1")
def run(k, gmax, amax, depth, tlimit):
    N=1<<k
    Z=[[1 if (t&s)==t else 0 for t in range(N)] for s in range(N)]
    D0=tuple((-2)**pop(t) for t in range(N))
    Hm=[[1-2*(pop(x&y)%2) for y in range(N)] for x in range(N)]
    G=[]
    R=range(-gmax,gmax+1)
    for a,b,c,d in itertools.product(R,repeat=4):
        det=a*d-b*c
        if det not in (1,-1): continue
        if (b==0 and c==0): continue          # signs only
        G.append((a,b,c,d,det))
    def moves(A,D):
        for i in range(N):
            for j in range(i+1,N):
                di,dj=D[i],D[j]
                for (a,b,c,d,det) in G:
                    # g D g^T off-diagonal: a*c*di + b*d*dj
                    if a*c*di+b*d*dj!=0: continue
                    ndi=a*a*di+b*b*dj; ndj=c*c*di+d*d*dj
                    # g^-1 = det * [[d,-b],[-c,a]] ; new columns: (col_i, col_j) g^-1
                    ok=True; newA=[]
                    for row in A:
                        x,y=row[i],row[j]
                        nx=det*(x*d - y*c); ny=det*(-x*b + y*a)
                        if abs(nx)>amax or abs(ny)>amax: ok=False; break
                        r=list(row); r[i]=nx; r[j]=ny; newA.append(tuple(r))
                    if not ok: continue
                    nD=list(D); nD[i]=ndi; nD[j]=ndj
                    yield tuple(newA),tuple(nD)
    def key(A,D):
        cols=list(zip(*A)); items=[]
        for c,dv in zip(cols,D):
            f=next((e for e in c if e!=0),1)
            items.append((tuple(e if f>0 else -e for e in c),dv))
        return tuple(sorted(items))
    def nnz(A): return sum(1 for r in A for e in r if e!=0)
    A0=tuple(tuple(r) for r in Z)
    seen={key(A0,D0):(A0,D0)}; frontier=[(A0,D0)]; t0=time.time(); done=0
    for dep in range(1,depth+1):
        nxt=[]
        for A,D in frontier:
            for B,E in moves(A,D):
                kk=key(B,E)
                if kk in seen: continue
                seen[kk]=(B,E); nxt.append((B,E))
            if time.time()-t0>tlimit: break
        frontier=nxt; done=dep
        if time.time()-t0>tlimit: print("  (time limit inside depth",dep,")"); break
        if not frontier: break
    # verify
    bad=0
    for A,D in seen.values():
        if any(sum(A[x][t]*D[t]*A[y][t] for t in range(N))!=Hm[x][y] for x in range(N) for y in range(N)): bad+=1
    hist={}; diags={}
    for A,D in seen.values():
        hist[nnz(A)]=hist.get(nnz(A),0)+1
        dk=tuple(sorted(D)); diags[dk]=diags.get(dk,0)+1
    print(f"k={k} N={N}: moves with entries <= {gmax}, bases with entries <= {amax}, depth reached {done}: {len(seen)} pairs (A, D) up to column order and sign; wrong: {bad}")
    print("  non-zeros of Z:",nnz(Z),"; histogram of non-zeros:",sorted(hist.items())[:10])
    print("  diagonals met (sorted entries: count):",sorted(diags.items(),key=lambda kv:-kv[1])[:6])
    best=sorted(seen.values(),key=lambda ad:nnz(ad[0]))[:2]
    for A,D in best:
        print("  sparsest: D =",D," rows =",[r for r in A])
    return seen
s=run(2,3,3,6,30)
# x-8's alternating basis
tgt=[(0,0,0,1),(0,0,1,-1),(0,1,-1,1),(1,-1,0,1)]
def canon_rows(A):
    cols=list(zip(*A)); cc=[]
    for c in cols:
        f=next((e for e in c if e!=0),1); cc.append(tuple(e if f>0 else -e for e in c))
    return tuple(sorted(cc))
found=any(canon_rows(A)==canon_rows(tgt) for A,D in s.values())
print("  x-8's alternating basis (columns up to order and sign) among them:",found)
run(3,2,2,3,200)
