import sys, time, numpy as np
from twol import *
H = Hmat(8)
Tin = chain_tree(8, [7, 1, 2]); Tout = chain_tree(8, [6, 3, 1])
print(len(Tin), [t[0] for t in Tin[8:]]); print(len(Tout), [t[0] for t in Tout[8:]])
c = np.array([1, -1, -1, -1, 1, 1, -1, 1.0]); a = np.array([-1, 1, 1, 1, 1, -1, 1, 1.0])
import random
idT = [((i,), -1, -1) for i in range(8)] + random_tree(8, random.Random(1))[8:]
L2id = (idT, np.ones(8), idT, np.ones(8), [(i, i, Fr(1)) for i in range(8)])
for mode in ('tau', 'nor', 'full'):
    t0 = time.time(); r = solve_letter(Tout, a, Tin, c, None, None, H, tl=40, mode=mode)
    g, g2, ok, prog, mid = replay(8, L2id, (Tout, a, Tin, c, r['rect']))
    print(mode, "programme value", r['cost'], "rectangles", len(r['rect']), "status", r['status'], "bound", r['bound'], "replay gates", g, ok, "%.1f s" % (time.time() - t0), flush=True)
