# ae-note/check.py: recompute the formulas quoted as "mine" in WAVE9-NOTE.md. Floats where marked.
from fractions import Fraction as F
import math
print("== bar per block (FLOAT): a block standing for share beta pays for itself at saving e iff it skips >= 1 - beta^(e/(1-e))")
e = 0.1
for name, beta in [("half", 1/2), ("third", 1/3), ("fifth", 1/5), ("one move of 45", 1/45), ("44 of 45", 44/45)]:
    print(f"  {name:16s} {100*(1 - beta**(e/(1-e))):.2f} %")
print("== bar as moves per single-move block (FLOAT): m^e/(1-e) - 1")
for m in (45, 80, 110):
    print(f"  m = {m}: {m**e/(1-e) - 1:.3f}")
print("== rates of the fourth result from ad-0's exact counts")
data_moves, data_blocks, arrays = 480, 3810, 480
print("  data arrays per block", F(data_moves, data_blocks), float(F(data_moves, data_blocks)))
print("  data arrays per block beyond two per array", float(F(data_moves, data_blocks - 2*arrays)))
print("  helpers", F(0, 16980), " copies", F(-360, 40), " unit", float(F(120, 20830)))
print("  best stage block keeps 1/9 =", float(F(1, 9)))
print("  cascade product", 4.33*1.20*3.74*4.00, " ratio 6.82e-2/8.7625e-4 =", 6.82e-2/8.7625e-4)
print("== line sums (count G)")
T = {4: 7, 8: 19, 16: 52, 64: 304, 256: 1600}   # night's best counts; 1600 is a formula nobody replayed
for N in (16, 64, 256):
    q = math.isqrt(N); k = N.bit_length() - 1
    add = (N + q)*(q - 1); thr = T[N] + (q + 1)*T[q]; tgt = T[N] - (q + 1)*T[q]
    print(f"  N={N}: half log = {k/2}, floor {N+q} = {(N+q)/N:.2f}/pt, adding-only {add} = {add/N:.2f}/pt, through transform {thr} = {thr/N:.2f}/pt, (9/8)k+1/2 = {9*k/8+0.5:.2f}, target T(N)-(q+1)T(q) = {tgt}")
print("== af-2 family 2 N log2 N - 3N + 4")
print("  ", [2*N*(N.bit_length()-1) - 3*N + 4 for N in (4, 8, 16, 32, 64, 128)])
print("== textbook N log2 N and the 3/4 family (3/4) N k + N/4")
print("  ", [(N, N*(N.bit_length()-1), 3*N*(N.bit_length()-1)//4 + N//4) for N in (4, 16, 64, 256)])
