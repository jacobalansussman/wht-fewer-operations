# fam3.py  (g-3-illconditioned): exact replay over the rationals, count (G).
# The 4 x 4 matrices that are flat on both sides form one family (up to scalings and relabellings):
#   M_a = rows (1,1,1,1), (1,1,-1,-1), (1,-1,a,-a), (1,-1,-a,a).      a = 1: Walsh-Hadamard.  a = i: 4-point Fourier.
# Census (mincirc, exhaustive modulo 13 and modulo 37): a 7-gate circuit exists exactly for a in {1, -1, 3, -3, 1/3, -1/3}.
# Here: the 7-gate circuit for a = 3 replayed exactly; the table L of M_a for several a; why 3.
from fractions import Fraction as Fr
import math, sys
sys.path.insert(0, '.')
from profile import ltable, pot, mass, cond_rows
def M(a): return [[1, 1, 1, 1], [1, 1, -1, -1], [1, -1, a, -a], [1, -1, -a, a]]
x = [[Fr(int(i == j)) for j in range(4)] for i in range(4)]
def gate(a, u, b, v): return [a * p + b * q for p, q in zip(u, v)]
s23 = gate(1, x[2], 1, x[3])            # gate 1   (0,0,1,1)
s123 = gate(1, x[1], 1, s23)            # gate 2   (0,1,1,1)
y0 = gate(1, x[0], 1, s123)             # gate 3   (1,1,1,1)      output
y1 = gate(1, y0, -2, s23)               # gate 4   (1,1,-1,-1)    output
r = gate(1, y1, -2, s123)               # gate 5   (1,-1,-3,-3)   helper: built by "overshoot", coefficient -2 on a running sum
y2 = gate(1, r, 6, x[2])                # gate 6   (1,-1,3,-3)    output
y3 = gate(1, r, 6, x[3])                # gate 7   (1,-1,-3,3)    output
print("a = 3: 7 gates give exactly M_3:", [y0, y1, y2, y3] == [[Fr(v) for v in row] for row in M(3)])
print("helper r =", [int(v) for v in r], " (not an output; r - y1 = -2*(0,1,1,1) is a running sum, which happens only for a = 3)")
for a in (Fr(1), Fr(3), Fr(1, 3), Fr(2), Fr(5)):
    Ma = [[Fr(v) for v in row] for row in M(a)]; L = ltable(Ma)
    flat = all(v == Fr(1, 4) for row in L for v in row)
    G = [[sum(p * q for p, q in zip(r1, r2)) for r2 in Ma] for r1 in Ma]
    orth = all(G[i][j] == 0 for i in range(4) for j in range(4) if i != j)
    print(f"a = {a}: table L flat (every entry 1/4): {flat}; potential {pot(L):.3f} bits; rows orthogonal: {orth}; cond with rows scaled [float]: {cond_rows(Ma):.3f}")
