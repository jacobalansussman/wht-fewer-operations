# e-6-shifts: for the Clebsch program, sparse embedding, is "strict collapse = 7" exactly "the line K meets the five
# zero points {1,2,4,8,15} of the quadratic form in 0 or 2 points", and "8" exactly "in 1 point (tangent)"?
# Same question for the two-pass program and the first digit {1,2,3}, and the rook program and split subgroups.
import sys
sys.path.insert(0, "waves/wave-02/e-6-shifts")
import collapse as C
S = {1, 2, 4, 8, 15}; D1 = {1, 2, 3}; D2 = {4, 8, 12}
tab = {}; tab2 = {}; tab3 = {}
pgs = [C.clebsch(i) for i in range(4)]; tp = C.twopass(); rk = C.rook(False)
for K in C.subspaces2():
    E, outs = C.emb_sparse(K)
    for pg in pgs:
        r = C.collapse(pg, E, C.H4rows, maxh_strict=4, maxh_pool=None)
        tab.setdefault((len(S & set(K)), r["strict"]), 0); tab[(len(S & set(K)), r["strict"])] += 1
    r = C.collapse(tp, E, C.H4rows, maxh_strict=4, maxh_pool=None)
    k = (len(D1 & set(K)), r["strict"]); tab2[k] = tab2.get(k, 0) + 1
    r = C.collapse(rk, E, C.H4rows, maxh_strict=4, maxh_pool=None)
    k = ((len(D1 & set(K)), len(D2 & set(K))), r["strict"]); tab3[k] = tab3.get(k, 0) + 1
print("Clebsch (4 pairings x 35 lines): (zero points on the line, strict collapse) -> count:", sorted(tab.items()))
print("two-pass: (points of the first digit on the line, strict collapse) -> count:", sorted(tab2.items()))
print("rook: ((points of digit 1, points of digit 2) on the line, strict collapse) -> count:", sorted(tab3.items()))
