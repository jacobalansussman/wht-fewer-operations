# v-0: the PARTNER-FREE game on the cube tree has value exactly N - 1 + (N/2) log2 N.
# Build: one wire per node below the root (N - 2), one join at the root, then a tree of flips T_k through all N rows.
# T_1: flip leaf 1.  T_(k+1): for every edge p -> c of T_k (flip on node m): (p,p) -> (c,p) by m in the left half, -> (c,c) by m in
# the right half; then for each of the 2^k rows a of the half: (a,a) -> (a,-a) by a flip of the whole right half.
# Replay: every edge is "parent XOR a node of the cube tree"; the vertices contain all N rows up to sign.
# Then count what the agreement rule would ask of THIS tree: distinct (node, pattern of the parent on that node) with node not a leaf.
import sys
def rows(k):
    N=1<<k; out=[]
    for y in range(N):
        m=0
        for x in range(N):
            if bin(x&y).count('1')&1: m|=1<<x
        out.append(m)
    return out
def nrm(m,N): return m^((1<<N)-1) if m&1 else m
def build(k):
    if k==1: return [(0,2,2)]
    n=1<<(k-1); full=(1<<n)-1; E=[]; T=build(k-1)
    for p,c,m in T:
        E.append((p|(p<<n), c|(p<<n), m)); E.append((c|(p<<n), c|(c<<n), m<<n))
    for a in rows(k-1):
        a=nrm(a,n); E.append((a|(a<<n), a|((a^full)<<n), full<<n))
    return E
def isnode(m,N):
    lo=(m&-m).bit_length()-1; sz=bin(m).count('1')
    return sz&(sz-1)==0 and lo%sz==0 and m==((1<<sz)-1)<<lo
for k in range(1,8):
    N=1<<k; E=build(k); held={0}; ok=True; partners={}
    for p,c,m in E:
        if nrm(p,N) not in held or not isnode(m,N) or (p^m)!=c: ok=False
        held.add(nrm(c,N))
        sz=bin(m).count('1')
        if 1<sz<N:
            lo=(m&-m).bit_length()-1; pat=(p>>lo)&((1<<sz)-1); pat=nrm(pat,sz)
            partners.setdefault((lo,sz),set()).add(pat)
    allrows=all(nrm(r,N) in held for r in rows(k))
    need=sum(len(s) for s in partners.values()); nodes_used=len(partners)
    f=N-1+(N//2)*k
    print(f"N={N}: flips {len(E)} (=(N/2)log2N: {len(E)==(N//2)*k}); all flips on nodes, each from a held wire: {ok}; all {N} rows reached: {allrows}; "
          f"wires = (N-2) + 1 + flips = {N-2+1+len(E)}; floor {f}; partner patterns this tree would need: {need} on {nodes_used} of {N-2} nodes (one wire per node would be {N-2})")
