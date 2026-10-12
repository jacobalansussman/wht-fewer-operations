# 3-point Fourier matrix = (rank one) + (diagonal), exactly, in Z[w], w^2 = -1 - w ; element (a, b) = a + b w
def mul(x, y): return (x[0]*y[0] - x[1]*y[1], x[0]*y[1] + x[1]*y[0] - x[1]*y[1])
one, w, w2, zero = (1,0), (0,1), (-1,-1), (0,0)
F3 = [[one, one, one],[one, w, w2],[one, w2, w]]
c = [w, one, one]; r = [one, w2, w2]
diff = [[(F3[i][j][0]-mul(r[i], c[j])[0], F3[i][j][1]-mul(r[i], c[j])[1]) for j in range(3)] for i in range(3)]
print("F3 - r c^T =", diff, "| off-diagonal all zero:", all(diff[i][j] == zero for i in range(3) for j in range(3) if i != j))
print("so y_i = r_i * (w x0 + x1 + x2) + d_i x_i : 2 gates for the sum, 3 for the outputs = 5 gates against 6")
