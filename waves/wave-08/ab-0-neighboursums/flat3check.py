# flat3check.py: sign-level check of the support triples that flat3 let through (k = 7, three signed flats).
# Lemma [derived]: on a flat G of dimension >= 3, a combination a*chi + b*chi' of two sign patterns that takes only the
# values 0 and 1, with its ones affinely independent, is identically 0.  (If chi*chi' is constant on G the function is
# c*chi on all of G; otherwise it is c*chi on one half and c'*chi on the other; a half or the whole that is all ones has
# 2^(g-1) >= 4 points, which are not affinely independent unless g <= 2.)
# So a triple is dead when every point is covered by exactly 0 or 2 of the supports and every region "in S_i and S_j only"
# is empty or a flat of dimension >= 3: the three regions then carry the zero function and E would be empty.
import itertools
E = 1
for j in range(6): E |= 1 << (1 << j)
def pts(m): return [z for z in range(64) if m >> z & 1]
def is_flat(P):
    if not P: return True, -1
    b = P[0]; S = {p ^ b for p in P}
    ok = all((u ^ v) in S for u in S for v in S)
    return ok, len(S).bit_length() - 1
dead = alive = 0; shapes = {}
for line in open('flat3_k7.out'):
    if not line.startswith('T'): continue
    f = line.split(); S = [int(f[4]), int(f[5]), int(f[6])]
    once = (S[0] ^ S[1] ^ S[2]) & ~(S[0] & S[1] & S[2]); thrice = S[0] & S[1] & S[2]
    regs = [S[i] & S[j] & ~S[l] for i, j, l in ((0, 1, 2), (0, 2, 1), (1, 2, 0))]
    info = [is_flat(pts(r)) for r in regs]
    ok = once == 0 and thrice == 0 and all(fl and (d == -1 or d >= 3) for fl, d in info)
    key = (f[1], f[2], f[3], bin(once).count('1'), bin(thrice).count('1'), tuple(sorted(d for fl, d in info)), all(fl for fl, d in info))
    shapes[key] = shapes.get(key, 0) + 1
    if ok: dead += 1
    else: alive += 1
for k, v in sorted(shapes.items()): print('dims', k[0:3], 'points covered once', k[3], 'thrice', k[4], 'dimensions of the three twice-covered regions', k[5], 'all flats', k[6], ':', v, 'triples')
print('support triples', dead + alive, 'dead by the lemma', dead, 'left', alive)
