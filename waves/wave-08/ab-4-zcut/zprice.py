# ab-4-zcut/zprice.py : the price of a return at 8 points.  For every optimal 12-gate circuit for Z and every plain cut:
#   G0 = gates living on L alone (zero on R);  rho = least number of RETURNS at the root over all valid derivations
#   (a return: a gate living on L alone with a parent that touches R), found by trying every subset of the L-alone gates;
#   saved = c(4) - G0 = 4 - G0 (gates the off-half group is short of a half-circuit); the gates touching R are then 8 + saved.
# Count (G). Exact.
import sys, re, itertools
from fractions import Fraction as F
src = open('zreturn.py').read()
exec(src.split('p = int(sys.argv[1])')[0])
p = int(sys.argv[1]); tab = {}
for line in open(sys.argv[2]):
    if 'example' not in line: continue
    hs = [lift([int(ch) for ch in h], p) for h in re.findall(r'\[(\d+)\]', line)]
    wires = list(hs) + list(targets); allp = inputs + wires; G = 12
    pairs = [[] for _ in range(G)]
    for g, w in enumerate(wires):
        for i, j in itertools.combinations(range(len(allp)), 2):
            if i - N == g or j - N == g: continue
            ab = coef(w, allp[i], allp[j])
            if ab is None or ab[0] == 0 or ab[1] == 0: continue
            m = (1 << (i - N) if i >= N else 0) | (1 << (j - N) if j >= N else 0)
            pairs[g].append((m, allp[i], allp[j]))
    if not derivable(G, [[q[0] for q in pairs[g]] for g in range(G)]): continue
    for c in range(3):
        R = [x for x in range(N) if x >> c & 1]
        def onL(v): return not any(v[i] for i in R)
        A = [g for g in range(G) if onL(wires[g])]; best = None
        for r in range(len(A) + 1):
            for Rset in itertools.combinations(A, r):
                allowed = [[q[0] for q in pairs[g] if not (g in A and g not in Rset) or (onL(q[1]) and onL(q[2]))] for g in range(G)]
                if derivable(G, allowed): best = r; break
            if best is not None: break
        nR = len({prim([w[i] for i in R]) for w in wires if sum(1 for i in R if w[i]) > 1})
        key = (len(A), best, nR); tab[key] = tab.get(key, 0) + 1
print('(gates on L alone, least number of returns at the root, n(R)) : count over 2,748 circuits x 3 cuts')
for k in sorted(tab): print('   G0=%d returns=%d n(R)=%d  [off-half group short by %d; gates touching R = %d] : %d' % (*k, 4 - k[0], 12 - k[0], tab[k]))
