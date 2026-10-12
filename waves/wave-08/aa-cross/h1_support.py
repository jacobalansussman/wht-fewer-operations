#!/usr/bin/env python3
"""h1_support.py [aa-cross]  Two facts used in the hand proof that 13 classes are impossible at 16 points, degree 2.
A function on the 4-cube is a real polynomial of degree <= 2 iff it is orthogonal to the 5 characters of weight 3 and 4.
(i) no non-zero such function is supported on 3 points or fewer; (ii) on 4 points only the constant multiples of the
indicator of a face (2 bits fixed).  Exact: rank over the rationals of a 5 x |S| matrix of +-1, by Fractions."""
import itertools
from fractions import Fraction
k = 4; N = 16
chars = [T for T in range(N) if bin(T).count("1") >= 3]
def kernel(S):
    M = [[Fraction((-1) ** bin(T & x).count("1")) for x in S] for T in chars]; n = len(S); rk = 0; piv = []
    for c in range(n):
        p = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]; inv = 1 / M[rk][c]; M[rk] = [v * inv for v in M[rk]]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        piv.append(c); rk += 1
    free = [c for c in range(n) if c not in piv]
    vecs = []
    for fc in free:
        v = [Fraction(0)] * n; v[fc] = Fraction(1)
        for r, pc in enumerate(piv): v[pc] = -M[r][fc]
        vecs.append(v)
    return vecs
bad = 0; faces = 0; other = 0
for size in (1, 2, 3, 4):
    cnt = 0
    for S in itertools.combinations(range(N), size):
        ker = kernel(S)
        if not ker: continue
        cnt += 1
        if size < 4: bad += 1
        else:
            x0 = S[0]; diffs = [x ^ x0 for x in S]; isface = (diffs[1] ^ diffs[2] == diffs[3]) and all(bin(d).count("1") == 1 for d in diffs[1:3])
            const = len(ker) == 1 and len(set(ker[0])) == 1
            if isface and const: faces += 1
            else: other += 1
    print("supports of size %d that carry a non-zero polynomial of degree <= 2: %d" % (size, cnt))
print("size <= 3: %d (claim 0) ; size 4: %d faces with constant value (there are 24 faces), %d of any other kind (claim 0)" % (bad, faces, other))
