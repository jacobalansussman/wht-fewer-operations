# k19_bounded.py: the 19-gate circuit for the third power of K = [[1,1],[1,2]] rewritten with whole coefficients of size <= 2
# and EXACT outputs (count B 2). Replayed on the 8 basis vectors. Input x_i is kernel column sig[i]; output y_j is kernel row rowof[j].
K = [[1,1],[1,2]]
P = [[K[a >> 2 & 1][x >> 2 & 1] * K[a >> 1 & 1][x >> 1 & 1] * K[a & 1][x & 1] for x in range(8)] for a in range(8)]
sig = [0, 1, 2, 3, 7, 6, 5, 4]; rowof = [7, 2, 1, 4, 3, 6, 5, 0]
W = {'x%d' % i: [int(i == j) for j in range(8)] for i in range(8)}; n = 0; mx = 0
def g(nm, a, u, b, v):
    global n, mx
    W[nm] = [a*x + b*y for x, y in zip(W[u], W[v])]; n += 1; mx = max(mx, abs(a), abs(b))
g('g1', 1, 'x0', 2, 'x7'); g('g2', 1, 'x1', 2, 'x6'); g('g3', 1, 'x2', 1, 'x5'); g('h4', 1, 'x3', 1, 'x4')   # h4 = g4 / 2
g('g5', 1, 'g1', 1, 'g2'); g('g6', 1, 'g3', 2, 'h4'); g('g7', 1, 'g5', 1, 'g6')
g('g8', 1, 'g7', -1, 'x7'); g('g9', 1, 'g7', 1, 'x5'); g('g10', 1, 'g8', -1, 'x6'); g('g11', 1, 'g9', 2, 'x4')
g('y7', 1, 'g10', -1, 'h4'); g('y1', 1, 'g10', 1, 'g3'); g('y6', 1, 'g11', 1, 'g2'); g('y0', 2, 'g11', -1, 'g1')
g('y2', 1, 'g8', 1, 'x1'); g('y4', 1, 'y2', 1, 'g6'); g('y3', 1, 'g9', -1, 'x3'); g('y5', 2, 'y3', -1, 'g5')
ok = all(W['y%d' % j] == [P[rowof[j]][sig[i]] for i in range(8)] for j in range(8))
print("gates", n, "; largest coefficient", mx, "; every output equals its row of the third power of K exactly:", ok)
