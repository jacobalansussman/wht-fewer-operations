#!/usr/bin/env python3
"""h2_specperm.py [aa-cross]  Straightening the quadric.  Whole numbers only.
In the frame of the outputs (the 'spectrum') a convolution is a diagonal.  For even k the transform is, up to free signs and a
free relabelling, the convolution whose spectrum is the sign pattern sigma = (-1)^(y1 y2 + y3 y4 + ...) (w-cross hybrid 1;
any non-degenerate quadric will do).  Let sigma' = -1 exactly on (a hyperplane minus a subspace of dimension k/2 - 1): it has
the same number of -1 and its convolution costs about 2N gates.  Every permutation pi of the outputs with sigma(pi(y)) =
sigma'(y) gives  C_sigma = Phi C_sigma' Phi^T,  Phi = H P_pi H / N  (an orthogonal matrix).  How sparse can Phi be?"""
import random, sys, time
def dot(x, y): return bin(x & y).count("1") & 1
def run(k, secs, seed):
    N = 1 << k; rnd = random.Random(seed)
    H = [[1 - 2 * dot(x, y) for y in range(N)] for x in range(N)]
    quad = lambda y: sum(((y >> (2 * i)) & 1) * ((y >> (2 * i + 1)) & 1) for i in range(k // 2)) & 1
    Q = [y for y in range(N) if quad(y)]
    W = [y for y in range(N) if (y & 1) == 0 and (y >> (k // 2)) == 0 and True]       # subspace inside y0 = 0 ...
    W = [y for y in W if y < (1 << (k // 2))]; W = [y for y in range(N) if y & 1 == 0 and y < (1 << (k // 2))]   # bits 1..k/2-1 free: dimension k/2 - 1
    Sp = [y for y in range(N) if y & 1 == 0 and y not in W]
    assert len(Sp) == len(Q), (len(Sp), len(Q))
    # C_sigma' = -X_u + (2/|V|) * (sum over v in V of X_v), u = e0, V = W-perp : check in whole numbers (times N)
    V = [x for x in range(N) if all(dot(x, w) == 0 for w in W)]
    sp = [(-1 if y in set(Sp) else 1) for y in range(N)]
    okC = all(sum(H[x][y] * sp[y] * H[y][z] for y in range(N)) == (-N if x ^ z == 1 else 0) + (2 * N // len(V) if (x ^ z) in set(V) else 0) for x in range(N) for z in range(N))
    gates = (N // len(V)) * (len(V) - 1) + N
    print("k=%d N=%d : -1 on %d outputs in both patterns ; C_sigma' = -X_u + (2/|V|) sum_V : %s ; its cost at most %d gates (coset sums %d, then one gate per point)" % (k, N, len(Q), okC, gates, gates - N))
    comp_s = [y for y in range(N) if y not in set(Sp)]; comp_q = [y for y in range(N) if y not in set(Q)]
    def phi_nnz(pi):
        # N * Phi[x][z] = sum_y H[x][pi(y)] H[y][z]
        cnt = 0; mx = 0
        for x in range(N):
            hx = H[x]
            for z in range(N):
                s = 0
                for y in range(N): s += hx[pi[y]] * H[y][z]
                if s: cnt += 1; mx = max(mx, abs(s))
        return cnt, mx
    # walk on pi by exchanging two images inside one level set
    best = None; t0 = time.time(); evals = 0
    # fast evaluation with bit tricks: column y of H as +-1 ; use correlation counts
    def nnz(pi):
        cnt = 0
        for x in range(N):
            # g(y) = x . pi(y)  (a 0/1 function of y); Phi row = Walsh spectrum of (-1)^g
            g = [1 - 2 * dot(x, pi[y]) for y in range(N)]
            h = 1
            while h < N:                      # in-place Walsh transform
                for i in range(0, N, 2 * h):
                    for jx in range(i, i + h):
                        a, b = g[jx], g[jx + h]; g[jx] = a + b; g[jx + h] = a - b
                h *= 2
            cnt += sum(1 for v in g if v)
        return cnt
    while time.time() - t0 < secs:
        a = Sp[:]; b = comp_s[:]; qa = Q[:]; qb = comp_q[:]; rnd.shuffle(qa); rnd.shuffle(qb)
        pi = [0] * N
        for y, t in zip(a, qa): pi[y] = t
        for y, t in zip(b, qb): pi[y] = t
        cur = nnz(pi); evals += 1; stall = 0
        while stall < 300 and time.time() - t0 < secs:
            grp = a if rnd.random() < 0.5 else b; y1, y2 = rnd.sample(grp, 2)
            pi[y1], pi[y2] = pi[y2], pi[y1]; new = nnz(pi); evals += 1
            if new <= cur: stall = 0 if new < cur else stall + 1; cur = new
            else: pi[y1], pi[y2] = pi[y2], pi[y1]; stall += 1
        if best is None or cur < best[0]: best = (cur, pi[:])
    cnt, mx = phi_nnz(best[1]) if N <= 16 else (best[0], None)
    # check the conjugation exactly: N^2 * C_sigma = (N Phi) (N C_sigma') (N Phi)^T / N^2 ... compare spectra instead: sigma(pi(y)) = sigma'(y)
    okpi = all((-1 if quad(best[1][y]) else 1) == sp[y] for y in range(N)) and sorted(best[1]) == list(range(N))
    print("   least non-zeros of N*Phi found: %d of %d (walk, %d evaluations, %.0f s) ; N^1.5 = %d ; pattern condition and bijection: %s%s" % (
        best[0], N * N, evals, time.time() - t0, int(N ** 1.5), okpi, "" if mx is None else " ; largest entry of N*Phi %d" % mx))
    return best
run(4, float(sys.argv[1]), 1)
run(6, float(sys.argv[2]), 2)
