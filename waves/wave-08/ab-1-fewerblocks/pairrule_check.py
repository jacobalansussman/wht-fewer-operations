"""pairrule_check.py [ab-1-fewerblocks]  FLOATS.  Test of the pair rule on solutions the least-squares hunt found for the plain
pattern (4 arrays, 16 moves, m = 4, no scratch): the solver knows nothing of the rule.  With no scratch, R_i = v_i and L_j = u_j.
Tight characters of this pattern: Q(e_i) = 1 for exactly one i; active moves = the four copies of e_i.
Prediction: v_p.u_q = 0 for p earlier than q, same direction; v_p.u_p = 1.  Pairs of different directions are not constrained."""
import numpy as np, glob
for f in sorted(glob.glob("refl_lm_m4_W4_S0_try*.npy")):
    d = np.load(f); sq = d[:16].astype(int); x = d[16:]; U = x[:64].reshape(16, 4); V = x[64:].reshape(16, 4)
    U = U / np.einsum("jd,jd->j", V, U)[:, None]
    K = V @ U.T
    same = [abs(K[p, q]) for p in range(16) for q in range(16) if p < q and sq[p] == sq[q]]
    later = [abs(K[q, p]) for p in range(16) for q in range(16) if p < q and sq[p] == sq[q]]
    diff = [abs(K[p, q]) for p in range(16) for q in range(16) if p < q and sq[p] != sq[q]]
    print(f, ": largest |v_p.u_q|, p earlier, same direction (predicted 0): %.2e ; same pairs the other way round (free): largest %.2e ; pairs of different directions (free): largest %.2e ; rank of K: %d" % (max(same), max(later), max(diff), np.linalg.matrix_rank(K, tol=1e-8)))
