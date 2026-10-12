import random
from lib import *
adj = lambda x, y: bin(x ^ y).count('1') == 1
walkr = walkc = arcs = 0; n = 0
for line in open('opt8.txt'):
    p = line.split('|'); rows = list(map(int, p[1].split())); cols = list(map(int, p[2].split())); n += 1
    mr = [x for x in rows if x not in (0, 7)]; mc = [x for x in cols if x not in (0, 7)]
    walkr += all(adj(mr[i], mr[i+1]) for i in range(5)); walkc += all(adj(mc[i], mc[i+1]) for i in range(5))
    arcs += sum(1 for i in range(7) if rows[i] not in (0, 7) and rows[i+1] not in (0, 7) and not adj(rows[i], rows[i+1]))
print("optimal 8-point pairs:", n, "; middle outputs form one hexagon walk (0 and 7 skipped):", walkr, "; middle inputs:", walkc, "; neighbouring middle outputs that are not hexagon neighbours (total):", arcs)
# deleting rows or columns never increases the corner count
random.seed(7); bad = 0; tests = 0
for k in (2, 3, 4, 5):
    N = 1 << k
    for t in range(300):
        r = list(range(N)); c = list(range(N)); random.shuffle(r); random.shuffle(c)
        full = sum(1 for row in second(picture(r, c)) for v in row if v)
        r2 = [x for x in r if random.random() < 0.7] or r[:1]; c2 = [x for x in c if random.random() < 0.7] or c[:1]
        sub = sum(1 for row in second(picture(r2, c2)) for v in row if v); tests += 1
        if sub > full: bad += 1
print("deletion never increases corners:", tests, "random tests, violations:", bad)
