# A4 check: J - 2I - 2*A(folded 5-cube) is a Hadamard matrix; A3 check: J - 2*A(rook 4x4) equals (J-2I) tensor (J-2I)
S = [1, 2, 4, 8, 15]
M = [[1 - 2*(1 if (y == z or (y ^ z) in S) else 0) for z in range(16)] for y in range(16)]
print("Clebsch form: M M^T = 16 I:", all(sum(M[i][t]*M[j][t] for t in range(16)) == (16 if i == j else 0) for i in range(16) for j in range(16)))
J2I = [[(-1 if i == j else 1) for j in range(4)] for i in range(4)]
K = [[J2I[a][b]*J2I[i][j] for b in range(4) for j in range(4)] for a in range(4) for i in range(4)]
R = [[1 - 2*(1 if ((a == b) != (i == j)) else 0) for b in range(4) for j in range(4)] for a in range(4) for i in range(4)]
print("rook form J - 2A equals (J-2I)x(J-2I):", K == R)
