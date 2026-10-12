# k19.py: the 19-gate class circuit (k-cross/hyb4.py, copied verbatim up to 'def kpow') built for K = [[1,1],[1,2]] and [[2,1],[1,1]].
# Question: how large are its constants for THIS kernel, and what does it cost when every gate must be +-u +-v (doublings charged)?
import re, io, sys
src = open('hyb4_copy.py').read().split("def kpow")[0]
exec(src)
def kpow(k):
    return [[Fr(k[a >> 2 & 1][x >> 2 & 1]) * k[a >> 1 & 1][x >> 1 & 1] * k[a & 1][x & 1] for x in range(8)] for a in range(8)]
sig = (0, 1, 2, 3, 7, 6, 5, 4); pi = {2: 1, 3: 4, 7: 0, 1: 2, 6: 5, 0: 7, 4: 3, 5: 6}
for nm, k in [("[[1,1],[1,2]]", [[1,1],[1,2]]), ("[[2,1],[1,1]]", [[2,1],[1,1]]), ("[[1,1],[1,3]]", [[1,1],[1,3]])]:
    fh = io.StringIO()
    try:
        build("kernel " + nm + " cubed", kpow(k), sig, pi, fh)
        print(fh.getvalue())
    except AssertionError as ex: print("kernel", nm, ": this wiring fails:", ex)
