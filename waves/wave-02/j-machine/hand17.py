#!/usr/bin/env python3
"""hand17.py -- exact replay (integers) of the hand circuits of ideas 3 and 6, count (G), 8 points, target J4 x H2
(a relabelling and rescaling of the 8-point transform).  Input index 2*j + b.  Prints gates used and outputs matched."""
J4=[[1-2*(i==j) for j in range(4)] for i in range(4)]; H2=[[1,1],[1,-1]]
T={(i,a):[J4[i][j]*H2[a][b] for j in range(4) for b in range(2)] for i in range(4) for a in range(2)}
x=[[int(k==l) for l in range(8)] for k in range(8)]
gates=0
def g(a,u,b,v):
    global gates; gates+=1; return [a*p+b*q for p,q in zip(u,v)]
u=[g(1,x[2*j],1,x[2*j+1]) for j in range(4)]
s01=g(1,u[0],1,u[1]); s23=g(1,u[2],1,u[3]); c=g(1,s01,1,s23)
out={}
for i in range(4): out[(i,0)]=g(1,c,-2,u[i])
print('half (4 outputs):',gates,'gates')
A=g(1,x[0],1,x[3]); B=g(1,x[5],1,x[7]); m=g(1,c,-2,B); out[(0,1)]=g(1,m,-2,A); print('5 outputs:',gates)
A2=g(1,x[1],1,x[2]); out[(1,1)]=g(1,m,-2,A2); print('6 outputs:',gates)
C=g(1,x[1],1,x[3]); D=g(1,x[4],1,x[7]); m2=g(1,c,-2,C); out[(2,1)]=g(1,m2,-2,D); print('7 outputs:',gates)
D2=g(1,x[5],1,x[6]); out[(3,1)]=g(1,m2,-2,D2); print('8 outputs by this route:',gates)
ok=all(out[k]==T[k] or out[k]==[-v for v in T[k]] for k in out)
print('all', len(out), 'outputs equal the target rows up to sign:', ok)
