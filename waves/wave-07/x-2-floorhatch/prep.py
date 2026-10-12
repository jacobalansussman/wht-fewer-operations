# x-2: turn a gate-list file of the night into the wire list that hatch.c reads, with the addresses renamed so that the circuit's
# own chain of subspaces becomes the cube tree (blocks of consecutive addresses).  Exact replay (Fractions) through u-8's parser.
import sys, os
os.chdir('waves/wave-06/u-8-compose'); exec(open('compose.py').read().split("if __name__ == '__main__':")[0])
src, dst = sys.argv[1], sys.argv[2]
g = parse(src); N = npts(g); W = replay(g, N); k = N.bit_length() - 1
vecs = [W[name] for (name, *_) in g]
sup = sorted({frozenset(i for i in range(N) if v[i] != 0) for v in vecs}, key=len)
basis = []; span = {0}
for s in sup:
    b = min(s)
    for x in s:
        if (x ^ b) not in span: basis.append(x ^ b); span = span | {y ^ x ^ b for y in span}
assert len(basis) == k, basis
new = {}
for c in range(N):
    x = 0
    for j in range(k):
        if c >> j & 1: x ^= basis[j]
    new[x] = c
out = []
for v in vecs:
    assert all(t.denominator == 1 for t in v)
    w = [0] * N
    for i in range(N): w[new[i]] = int(v[i])
    out.append(w)
open(dst, 'w').write('# from %s ; addresses renamed by the basis %s\n' % (src, basis) + ''.join(' '.join(map(str, w)) + '\n' for w in out))
print(dst, N, len(out), 'wires; basis', basis)
