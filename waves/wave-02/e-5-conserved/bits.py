# Entropy made per operation by the cheapest "sum-type" unitary gates, on fresh (delta) inputs.
# Gate on q points: reflection I - (2/q) J  (J = all ones).  Count (O): (q-1) additions for the sum, 1 scaling, q subtractions = 2q.
# Count (G): 2q - 1.  Entropy of a unit vector p: -sum p_j^2 log2 p_j^2.  A gate on q fresh inputs makes q * h(q) bits.
# Butterfly (q = 2, the 45-degree rotation): 2 operations, 2 bits.  Final state of the N-point transform: N log2 N bits.
from math import log2
print("q  bits made  ops(O)  bits/op(O)  ops(G)  bits/op(G)")
print("%d  %.4f  %d  %.4f  %d  %.4f   (butterfly)" % (2, 2.0, 2, 1.0, 2, 1.0))
for q in range(3, 17):
    d = (1 - 2/q)**2; o = (2/q)**2
    h = -(d*log2(d) if d > 0 else 0) - (q-1)*o*log2(o)
    print("%d  %.4f  %d  %.4f  %d  %.4f" % (q, q*h, 2*q, q*h/(2*q), 2*q-1, q*h/(2*q-1)))
