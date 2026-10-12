# ab-5: d-0's tying 8-point circuit with one signed helper, replayed in whole numbers and read through the cut along the
# middle address bit (lower half = addresses 0,1,4,5 ; upper half = 2,3,6,7).
N = 8
def e(i): v = [0]*N; v[i] = 1; return v
def lin(a, u, b, v): return [a*p + b*q for p, q in zip(u, v)]
x = [e(i) for i in range(N)]
W = {}; order = []
def gate(name, a, u, b, v):
    W[name] = (lin(a, u, b, v), u, v); order.append(name); return W[name][0]
y1 = gate('y001', 1, x[0], 1, x[1]); y2 = gate('y010', 1, x[0], 1, x[2]); u = gate('u', 1, x[2], 1, x[3])
y3 = gate('y011', 1, y1, 1, u); y4 = gate('y100', 1, x[0], 1, x[4]); b = gate('b', 1, x[4], 1, x[6])
y6 = gate('y110', 1, y2, 1, b); w = gate('w', 1, b, 1, x[5]); z = gate('z', 1, w, 1, x[7]); y7 = gate('y111', 1, y3, 1, z)
h = gate('h', 1, y1, -1, x[6]); y5 = gate('y101', 1, w, 1, h)
Z = [[1 if (t & s) == t else 0 for t in range(N)] for s in range(N)]
outs = {0: x[0], 1: y1, 2: y2, 3: y3, 4: y4, 5: y5, 6: y6, 7: y7}
assert all(outs[s] == Z[s] for s in range(N)); print('12 gates, all 8 subset sums exact:', True)
upper = [2, 3, 6, 7]
has = lambda v: any(v[i] != 0 for i in upper)
cls = {}
for name in order:
    r, a, c = W[name]
    k = ('P_int' if not has(a) and not has(c) else 'P_c') if not has(r) else ('M3' if has(a) != has(c) else 'M2')
    cls.setdefault(k, []).append(name)
for k in ('P_int', 'P_c', 'M3', 'M2'): print(k, len(cls.get(k, [])), cls.get(k, []))
print('pure gates', len(cls['P_int']) + len(cls['P_c']), 'against 4 for the lower half alone; injections', len(cls['M3']), 'against the 4 that are forced; M2', len(cls['M2']))
