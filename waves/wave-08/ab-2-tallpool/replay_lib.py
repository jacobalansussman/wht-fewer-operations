import math
def comb(u,v,w):
    n=len(u)
    for i in range(n):
        for j in range(i+1,n):
            D=u[i]*v[j]-u[j]*v[i]
            if D:
                a=w[i]*v[j]-w[j]*v[i]; b=u[i]*w[j]-u[j]*w[i]
                if all(D*w[l]==a*u[l]+b*v[l] for l in range(n)):
                    g=math.gcd(math.gcd(abs(a),abs(b)),abs(D)); return a//g,b//g,D//g
                return None
    return None
