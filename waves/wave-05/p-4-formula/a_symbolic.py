# p-4-formula (a): hyb4.py's solve with the kernel's entries a,b,c,d as SYMBOLS.
# Every entry of a kernel power is a monomial a^i b^j c^k d^l, so exact symbolic work = arithmetic on exponent 4-vectors
# (Laurent monomials). No sympy needed. Count (G).
exc = {2:{7,1}, 3:{5,3}, 7:{7,6,3,4}, 1:{7,6,2,5}, 4:{7,1,2,3,4,5}, 5:{5,3,0,1,6,7}, 6:{5,4,1,6}, 0:{5,4,0,7}}
terms = [((1,2,4,7),(7,)), ((0,3,5,6),(5,)), ((1,7),(6,)), ((0,6),(4,)), ((3,5),(3,)), ((2,4),(1,)),
         ((0,),(0,7)), ((6,),(1,6)), ((1,),(2,5)), ((7,),(3,4)), ((5,),(0,1,6,7)), ((4,),(2,3,4,5))]
sig = (0, 1, 2, 3, 7, 6, 5, 4); pi = {2: 1, 3: 4, 7: 0, 1: 2, 6: 5, 0: 7, 4: 3, 5: 6}
E = {(0,0):(1,0,0,0), (0,1):(0,1,0,0), (1,0):(0,0,1,0), (1,1):(0,0,0,1)}
add = lambda u, v: tuple(x+y for x, y in zip(u, v)); sub = lambda u, v: tuple(x-y for x, y in zip(u, v))
def kp(y, x):
    m = (0,0,0,0)
    for b in range(3): m = add(m, E[(y>>b&1, x>>b&1)])
    return m
def show(m):
    s = "".join("%s^%d " % (n, e) for n, e in zip("abcd", m) if e) or "1"
    return s.strip()
Kp = [[kp(pi[j], sig[i]) for i in range(8)] for j in range(8)]
c = [None]*8
for i in range(8):
    if i not in (1,7): c[i] = Kp[2][i]
lam = sub(Kp[2][0], Kp[3][0]); c[1] = add(lam, Kp[3][1]); c[7] = add(lam, Kp[3][7])
a = []
for j in range(8):
    s = {sub(Kp[j][i], c[i]) for i in range(8) if i not in exc[j]}
    assert len(s) == 1, (j, s); a.append(s.pop())
print("centre c, by kernel column x = 0..7 :", [show(c[sig.index(x)]) for x in range(8)])
inv = {pi[j]: j for j in range(8)}
print("row scaling, by kernel row y = 0..7 :", [show(a[inv[y]]) for y in range(8)])
cov = {}
for (nu, mu) in terms:
    vals = {sub(sub(Kp[j][i], a[j]), c[i]) for j in nu for i in mu}
    assert len(vals) == 1, ("not one monomial on this rectangle", nu, mu, vals)
    v = vals.pop()
    for j in nu:
        for i in mu:
            assert (j,i) not in cov; cov[(j,i)] = v
    print("rectangle: kernel rows", sorted(pi[j] for j in nu), "x kernel columns", sorted(sig[i] for i in mu), ": K/(a c) =", show(v), " so the constant is (", show(v), ") - 1")
rest = {sub(sub(Kp[j][i], a[j]), c[i]) for j in range(8) for i in range(8) if (j,i) not in cov}
print("cells on rectangles:", len(cov), "; K/(a c) on the other", 64-len(cov), "cells:", [show(v) for v in rest])
print()
print("m(y,x) = exponent of rho = ad/(bc) in K/(a c), rows y = 0..7 (bits y3 y2 y1), columns x = 0..7:")
for y in range(8):
    print("  y=%s " % format(y,'03b'), " ".join("%2d" % (sub(sub(Kp[inv[y]][sig.index(x)], a[inv[y]]), c[sig.index(x)])[0]) for x in range(8)))
