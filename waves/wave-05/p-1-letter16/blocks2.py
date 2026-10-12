# p-1-letter16: census of the 2 x 2 blocks for named designs (exact), to state precisely how many checkerboards a bent centre has.
from blocks import census, par
N = 16
def dual(c): return [sum((-1) ** par(y & x) * c[x] for x in range(N)) // 4 for y in range(N)]
b = lambda x, i: x >> i & 1
q = lambda f: [(-1) ** f(x) for x in range(N)]
c1 = [1,1,1,-1,1,1,-1,1,1,1,-1,1,-1,-1,-1,1]; c2 = [1,-1,1,-1,-1,-1,1,1,1,-1,-1,1,-1,-1,-1,-1]
print("k-cross design 1 (49 rectangles): row pairs along 5, column pairs along 13:", census(N, 5, 13, dual(c1), c1))
print("k-cross design 2 (49 rectangles): row pairs along 15, column pairs along 12:", census(N, 15, 12, dual(c2), c2))
f = q(lambda x: b(x, 0) & b(x, 3) ^ b(x, 1) & b(x, 2))
print("bent x0x3+x1x2 on both sides, standard chains (73 rectangles):", census(N, 1, 8, f, f), " its transform equals itself:", dual(f) == f)
g = q(lambda x: b(x, 0) & b(x, 1) ^ b(x, 2) & b(x, 3))
print("bent x0x1+x2x3 with its transform, standard chains:", census(N, 1, 8, dual(g), g))
r = [1,-1,1,-1,-1,1,1,-1,-1,-1,-1,-1,1,1,-1,-1]; c = [1,-1,1,1,1,1,-1,1,1,1,1,-1,1,-1,-1,-1]
print("the design with pair bound 32 (exact cover 49):", census(N, 1, 8, r, c))
import itertools
# all 28*... bent quadratic forms without linear part, with their transforms, standard chains: which checkerboard counts occur
seen = {}
mons = [m for m in range(1, N) if bin(m).count('1') == 2]
for bits in itertools.product([0, 1], repeat=6):
    ch = [m for m, t in zip(mons, bits) if t]; c = [(-1) ** (sum(1 for m in ch if (x & m) == m) & 1) for x in range(N)]
    tr = [sum((-1) ** par(y & x) * c[x] for x in range(N)) for y in range(N)]
    if all(abs(t) == 4 for t in tr):
        k = census(N, 1, 8, [t // 4 for t in tr], c)['checker']; seen[k] = seen.get(k, 0) + 1
print("the 28 bent quadratic forms (no linear part) with their transforms, standard chains: checkerboard count -> how many forms:", sorted(seen.items()))
