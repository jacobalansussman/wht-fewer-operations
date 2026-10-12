# s-pick: exhaustive corners of the 4-point subset-sum matrix, plain (no signs) and signed; plus the plain "prefix-degree" identity check.
import itertools
N=4
Z=[[1 if (a&b)==b else 0 for b in range(N)] for a in range(N)]
def corners(rows,cols,r,c):
    A=[[Z[rows[a]][cols[b]]*r[a]*c[b] for b in range(N)]+[0] for a in range(N)]+[[0]*(N+1)]
    M=[[A[a][b]-A[a+1][b]-A[a][b+1]+A[a+1][b+1] for b in range(N)] for a in range(N)]
    return sum(1 for a in range(N) for b in range(N) if M[a][b]), M
best=(99,None); bests=(99,None)
for rows in itertools.permutations(range(N)):
    for cols in itertools.permutations(range(N)):
        v,M=corners(rows,cols,[1]*N,[1]*N)
        if v<best[0]: best=(v,(rows,cols,M))
        for r in itertools.product((1,-1),repeat=N):
            for c in itertools.product((1,-1),repeat=N):
                v,M=corners(rows,cols,r,c)
                if v<bests[0]: bests=(v,(rows,cols,r,c,M))
print('plain minimum',best); print('signed minimum',bests)
