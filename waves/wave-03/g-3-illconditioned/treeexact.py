# treeexact.py  (g-3-illconditioned): exact integers.
# A tree letter for a bit order: B[x][y] = g[depth of the lowest common ancestor of x and y] for x != y, B[x][x] = h[x],
# where the tree splits the addresses by the bits in the given order (first bit = top split).  Here g depends on the depth only.
# Check: butterfly layers and brick layers are tree letters, and their products are the transform up to relabelling:
#   8 points  = letter(order 0,1,2; g = 0,0,1; h = +1/-1 by bit 2)  x  letter(order 2,1,0; g = 0,1,1; h = -1)
#   16 points = letter(order 0,1,2,3; g = 0,0,1,1; h = -1)          x  letter(order 2,3,0,1; g = 0,0,1,1; h = -1)
def letter(k, order, g, h):
    N = 1 << k; B = [[0] * N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            if x == y: B[x][y] = h(x); continue
            for depth, b in enumerate(order):
                if (x >> b & 1) != (y >> b & 1): B[x][y] = g[depth]; break
    return B
def mul(A, B): return [[sum(a * b for a, b in zip(r, c)) for c in zip(*B)] for r in A]
def is_hadamard(M):
    N = len(M)
    return all(abs(v) == 1 for r in M for v in r) and all(sum(a * b for a, b in zip(M[i], M[j])) == (N if i == j else 0) for i in range(N) for j in range(N))
def sylvester_equiv(M):   # equivalent to the Walsh-Hadamard matrix: normalise first row and column, compare the set of rows with the characters
    N = len(M); k = N.bit_length() - 1
    R = [[M[i][j] * M[i][0] * M[0][j] * M[0][0] for j in range(N)] for i in range(N)]
    rows = set(tuple(r) for r in R)
    # the rows must form a group under entry-by-entry product (then they are the characters of some group structure on the columns)
    return len(rows) == N and all(tuple(a * b for a, b in zip(r1, r2)) in rows for r1 in rows for r2 in rows)
K8 = mul(letter(3, (0, 1, 2), (0, 0, 1), lambda x: -1 if x >> 2 & 1 else 1), letter(3, (2, 1, 0), (0, 1, 1), lambda x: -1))
K16 = mul(letter(4, (0, 1, 2, 3), (0, 0, 1, 1), lambda x: -1), letter(4, (2, 3, 0, 1), (0, 0, 1, 1), lambda x: -1))
for name, K in (("8 points, two tree letters", K8), ("16 points, two tree letters", K16)):
    print(f"{name}: a +-1 matrix with orthogonal rows: {is_hadamard(K)}; rows closed under entry-by-entry product after normalising (so it is the Walsh-Hadamard matrix up to relabelling and signs): {sylvester_equiv(K)}")

# A one-parameter family at 16 points [derived after treejac.py measured one free direction]: the all-ones vector is an
# eigenvector of both brick layers (eigenvalue 2), so (B1 + c*J)(B2 - c/(1+8c)*J) = B1*B2 for every c, J = all ones.
# Both factors are still tree letters (every g and h shifted by a constant).  As c -> -1/8 the first factor becomes
# singular and the second blows up, while the product stays the transform: badly conditioned steps, perfectly conditioned product.
from fractions import Fraction as Fr
B1 = letter(4, (0, 1, 2, 3), (0, 0, 1, 1), lambda x: -1); B2 = letter(4, (2, 3, 0, 1), (0, 0, 1, 1), lambda x: -1)
for c in (Fr(1), Fr(1, 3), Fr(-1, 9), Fr(-1001, 8000)):
    c2 = c / (1 + 8 * c)
    A1 = [[Fr(v) + c for v in r] for r in B1]; A2 = [[Fr(v) - c2 for v in r] for r in B2]
    print(f"c = {c}: second shift {c2}; (B1 + c J)(B2 - c' J) equals B1 B2 exactly: {mul(A1, A2) == [[Fr(v) for v in r] for r in K16]}")
