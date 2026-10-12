# hub.py: entropy made by ONE hub on s wires (floats; a measurement of exact matrices).
#  orthogonal hub: the reflection I - (2/s) J (J = all ones), every p known in closed form: p_ii = (1-2/s)^2, p_ij = 4/s^2.
#  non-orthogonal hub: W_s = (t-1) I + J with t + 1/t = 2 - s (g-3): every p = 1/s, entropy s log2 s.
#  cost of either in count (G): s-1 gates for the sum, s gates for the outputs = 2s-1.
#  bound for a reflection I - 2Q, Q a projection of rank r:  Phi <= N + 4 r log2 N   (hand proof in x-8.md section 4).
from math import log2
print("s | orthogonal hub: Phi, Phi/(2s-1) | non-orthogonal hub: Phi = s log2 s, Phi/(2s-1) | bound s + 4 log2 s")
for s in (2, 4, 8, 16, 32, 64, 256, 1024, 4096):
    d = (1 - 2/s)**2; o = 4/s**2
    phi = s * ((-d*log2(d) if d > 0 else 0.0) + (s-1) * (-o*log2(o)))
    print("%5d | %8.3f  %.3f | %10.1f  %.3f | %.1f" % (s, phi, phi/(2*s-1), s*log2(s), s*log2(s)/(2*s-1), s + 4*log2(s)))
