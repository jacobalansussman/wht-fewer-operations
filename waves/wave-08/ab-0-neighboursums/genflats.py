# genflats.py n : all affine flats of F_2^n as bit masks over the 2^n points, one per line (dimension, mask)
import sys
n = int(sys.argv[1]); P = 1 << n
subs = set(); stack = [frozenset([0])]
while stack:
    S = stack.pop()
    if S in subs: continue
    subs.add(S)
    for v in range(1, P):
        if v not in S: stack.append(S | frozenset(s ^ v for s in S))
out = []
for S in subs:
    seen = set()
    for b in range(P):
        if b in seen: continue
        co = [b ^ s for s in S]; seen |= set(co)
        out.append((len(S).bit_length() - 1, sum(1 << z for z in co)))
out.sort()
for d, m in out: print(d, m)
