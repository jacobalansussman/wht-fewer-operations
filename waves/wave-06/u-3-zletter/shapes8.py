# u-3-zletter/shapes8.py : the 8-point census by tree SHAPE (sizes of the internal nodes), rectangles tau and gates.
# Reads trees8z.txt (orbit size, masks), out8z_tau_p3.txt (exact tau, modulo 3), out8zg_all.txt (exact step gates, modulo 3).
import sys, collections
T = [l.split() for l in open('trees8z.txt')]
tau = [int(x) for x in open('out8z_tau_p3.txt')]
g = [int(x) for x in open('out8zg_all.txt')]
assert len(T) == len(tau) == len(g) == 23100
def shape(masks):
    return tuple(sorted((bin(int(m)).count('1') for m in masks), reverse=True))
by = collections.defaultdict(list)
for t, a, b in zip(T, tau, g):
    by[shape(t[1:8])].append((a, b + 7, int(t[0])))
print('exact census at 8 points, modulo 3, all %d classes (%d labelled trees)' % (len(T), sum(int(t[0]) for t in T)))
print('tau histogram (classes):', sorted(collections.Counter(tau).items()))
print('gates histogram (classes), gates = 7 + steps that cost a gate:', sorted(collections.Counter(x + 7 for x in g).items()))
lab = collections.Counter()
for t, b in zip(T, g): lab[b + 7] += int(t[0])
print('gates histogram (labelled trees):', sorted(lab.items()))
print('joint (tau, gates) histogram (classes):', sorted(collections.Counter(zip(tau, [x + 7 for x in g])).items()))
print('shape (internal node sizes) | classes | tau min..max | gates min..max | classes at tau 8 | classes at 12 gates')
for s, v in sorted(by.items()):
    print(s, '|', len(v), '|', min(a for a, _, _ in v), '..', max(a for a, _, _ in v), '|', min(b for _, b, _ in v), '..', max(b for _, b, _ in v),
          '|', sum(1 for a, _, _ in v if a == 8), '|', sum(1 for _, b, _ in v if b == 12))
