# d-1-plane play 2: N=16. (a) D^2 in the group ring of C_15. (b) radial matrices per angular frequency, exact in Z[zeta5].
k=4; N=16; q=4; POLY=0b10011
ex=[0]*30; lg=[None]*16; x=1
for i in range(15):
    ex[i]=x; lg[x]=i; x<<=1
    if x>>4: x^=POLY
for i in range(15,30): ex[i]=ex[i-15]
mul=lambda a,b: 0 if (a==0 or b==0) else ex[lg[a]+lg[b]]
def trace2(v):
    r=0; y=v
    for _ in range(4): r^=y; y=mul(y,y)
    return r
psi=lambda v: -1 if trace2(v) else 1
D=[1,2,4,8]
sq=[0]*15
for a in D:
    for b in D: sq[(a+b)%15]+=1
rhs=[0]*15
for a in D: rhs[a]+=1
rhs[0]-=4
for i in range(0,15,3): rhs[i]+=2      # the circle through 1 (norm-one group, order 5)
for i in range(0,15,5): rhs[i]+=2      # the ray through 1 (F_4^*, order 3)
print("(a) D*D = D - 4 + 2*(circle sum) + 2*(ray sum) in Z[C_15]:",sq==rhs)
# (b) u = theta^(3b) on the circle, rho = theta^(5a) on the ray
def red(v):   # reduce a length-5 integer vector modulo 1+z+z^2+z^3+z^4 to basis 1,z,z^2,z^3
    return tuple(v[i]-v[4] for i in range(4))
for j in range(5):
    row=[]
    for a in range(3):
        v=[0]*5
        for b in range(5): v[(j*b)%5]+=psi(ex[(5*a+3*b)%15])
        row.append(red(v))
    print("(b) angular frequency %d: kappa(s) for s = theta^0, theta^5, theta^10, as coefficients of 1,z,z^2,z^3: %s"%(j,row))
# c1 = z+z^4 = (-1+sqrt5)/2, so 1 - c1 + c2 = 1 - (c1 - c2) with c1-c2 = sqrt5 ; in the basis above c1 = z + z^4 = (-1, 0, -1, -1), c2 = z^2+z^3 = (0,0,1,1)
# check row norms: sum over s of kappa(s)*conj(kappa(s)) = 16 for every j (numerically, as a cross-check only)
import cmath
for j in range(5):
    tot=0; vals=[]
    for a in range(3):
        s=sum(cmath.exp(2j*cmath.pi*((j*b)%5)/5)*psi(ex[(5*a+3*b)%15]) for b in range(5)); tot+=abs(s)**2; vals.append(round(s.real,6))
    print("    frequency %d numeric values %s ; sum of squares %.6f (float cross-check only)"%(j,vals,tot))
# the frequency-0 block with the origin: input (x0, c_rho) = value at origin and common value on each circle
M=[[1,5,5,5]]+[[1]+[sum(psi(ex[(5*((a+a2)%3)+3*b)%15]) for b in range(5)) for a2 in range(3)] for a in range(3)]
print("(c) angular frequency 0 with the origin, 4x4:",M)
