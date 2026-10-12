#!/usr/bin/env python3
"""positive control for anyex.py: remove ONE helper of the 19 (and of the 20); the candidate list (points on two lines through
pairs of the remaining wires) must contain the removed wire, and adding it back must give a circuit; and count how many OTHER
single wires, with any coefficients, restore a circuit (same gate count)."""
import sys
src = open(__file__.rsplit('/', 1)[0] + '/anyex.py').read().split("name = sys.argv[1]")[0]
exec(src)
for name in ('c19', 'c20'):
    H = start(name); back = 0; others = 0; cheaper = 0; tot = 0
    for i in range(len(H)):
        keep = H[:i] + H[i + 1:]; cand = candidates(ins + keep + outs); tot += len(cand)
        if H[i] in cand and feasible(keep + [H[i]]): back += 1
        for w in cand:
            if w != H[i] and feasible(keep + [w]):
                others += 1
                if 1 + over(w) < 1 + over(H[i]): cheaper += 1
    print('%s: %d helpers; removed wire found among the candidates and restores the circuit: %d of %d; candidates in all %d; other single wires that restore a circuit: %d, of which cheaper (tight in place of over-limit): %d' % (name, len(H), back, len(H), tot, others, cheaper))
