# brick7.py: exact replay of the 7-gate program for K(x)K, K = [[1,1],[1,2]], coefficients 1, -1, 2 only, outputs exact.
e = [[int(i == j) for j in range(4)] for i in range(4)]
L = lambda a, u, b, v: [a*x + b*y for x, y in zip(u, v)]
g1 = L(1, e[0], 1, e[1]); g2 = L(1, e[2], 2, e[3]); h = L(1, g1, 1, g2)
y = [L(1, h, -1, e[3]), L(1, h, 1, e[1]), L(1, h, 1, e[2]), L(2, h, -1, e[0])]
K = [[1,1],[1,2]]; T = [[a*b for a in ra for b in rb] for ra in K for rb in K]
print("7 gates, coefficients in {1,-1,2}; outputs equal K(x)K exactly:", y == T, y)
