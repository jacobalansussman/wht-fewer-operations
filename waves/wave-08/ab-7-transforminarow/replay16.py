# replay16.py (ab-7): explicit replay of "the 16-point transform is a convolution on Z/8 x Z/2".
# Kernel c from torus.out. Builds M[g][h] = c(g - h), finds signs r, s and relabellings pi, sigma of rows and columns with
#   M[g][h] = r[g] * s[h] * (-1)^(common ones of pi(g) and sigma(h))     for all 256 entries,
# then looks at "add one along the 8-cycle" as a map on the 4-bit addresses pi(g): is it an invertible bit matrix plus a shift,
# what is its order, and is its matrix a single Jordan block (Pascal's rule)?
import itertools
shape=[8,2]; els=list(itertools.product(range(8),range(2))); idx={e:i for i,e in enumerate(els)}; N=16
c=[1 if ch=='+' else -1 for ch in "+--+--++-+-+++++"]
sub=lambda g,h: idx[((els[g][0]-els[h][0])%8,(els[g][1]-els[h][1])%2)]
M=[[c[sub(g,h)] for h in range(N)] for g in range(N)]
assert all(sum(a*b for a,b in zip(M[g],M[g2]))==(N if g==g2 else 0) for g in range(N) for g2 in range(N))
s=[M[0][h] for h in range(N)]
M1=[[M[g][h]*s[h] for h in range(N)] for g in range(N)]
r=[M1[g][0] for g in range(N)]
M2=[[M1[g][h]*r[g] for h in range(N)] for g in range(N)]
rows=[tuple(x) for x in M2]; pos={x:i for i,x in enumerate(rows)}
# basis of the row group
basis=[]; span={tuple([1]*N):0}
for g in range(N):
    if rows[g] not in span:
        j=len(basis); basis.append(g)
        for v,code in list(span.items()):
            span[tuple(a*b for a,b in zip(v,rows[g]))]=code|(1<<j)
assert len(basis)==4 and len(span)==16
pi=[span[rows[g]] for g in range(N)]
sigma=[sum((1<<j) for j,b in enumerate(basis) if rows[b][h]==-1) for h in range(N)]
assert sorted(pi)==list(range(16)) and sorted(sigma)==list(range(16))
ok=all(M[g][h]==r[g]*s[h]*(-1)**bin(pi[g]&sigma[h]).count("1") for g in range(N) for h in range(N))
print("M[g][h] = r[g] s[h] (-1)^(pi(g).sigma(h)) on all 256 entries:",ok)
print("pi (address of group element (a,b), a on the 8-cycle):",{els[g]:format(pi[g],'04b') for g in range(N)})
# add one along the 8-cycle, as a map on addresses
inv={pi[g]:g for g in range(N)}
tau=[pi[idx[((els[inv[a]][0]+1)%8,els[inv[a]][1])]] for a in range(16)]
aff=all(tau[a]^tau[b]^tau[d]^tau[a^b^d]==0 for a in range(16) for b in range(16) for d in range(16))
order=1; cur=tau[:]
while cur!=list(range(16)): cur=[tau[x] for x in cur]; order+=1
lin=[tau[1<<j]^tau[0] for j in range(4)]   # columns of the bit matrix
def app(v): 
    out=0
    for j in range(4):
        if v>>j&1: out^=lin[j]
    return out
# nilpotent part n = lin + identity; rank of n^3
def npow(v,times):
    for _ in range(times): v=app(v)^v
    return v
n3=[npow(1<<j,3) for j in range(4)]; n4=[npow(1<<j,4) for j in range(4)]
n2=[npow(1<<j,2) for j in range(4)]
print("add-one on the 8-cycle is (bit matrix) x address + shift:",aff,"; shift",format(tau[0],'04b'),"; bit matrix columns",[format(x,'04b') for x in lin],"; order of the map",order)
print("(matrix - identity)^2 non-zero:",any(n2),"; ^3 non-zero:",any(n3),"; ^4 non-zero:",any(n4))
# same for the second generator
tau2=[pi[idx[(els[inv[a]][0],(els[inv[a]][1]+1)%2)]] for a in range(16)]
print("second generator: shift only:",all(tau2[a]==a^tau2[0] for a in range(16)),"; shift",format(tau2[0],'04b'))
