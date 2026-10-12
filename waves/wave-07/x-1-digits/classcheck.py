# x-1-digits/classcheck.py : the window circuits are identities of the whole class of 2 x 2 kernels.
# Kernel [[1,1],[1,s]], k-th Kronecker power T_s, entry s^m (m = common ones).  With (s-1)^|U| on the diagonal the window [0,d]
# must equal sum_{j<=d} (s-1)^j C(m,j), congruent to T_s modulo (s-1)^(d+1), and equal to T_s at d = k.  Whole numbers.
from math import comb
from slices import window, pc
for s in (4, -2, 3, 0, 7):
    q = s - 1; allok = True; line = []
    for k in (3, 4, 5, 6):
        N = 1 << k
        for d in range(k + 1):
            gi, go, out = window(k, 0, d, q=q)
            T = [[s ** pc(y & x) for x in range(N)] for y in range(N)]
            want = [[sum(q ** j * comb(pc(y & x), j) for j in range(d + 1)) for x in range(N)] for y in range(N)]
            ok = all(out[y] == want[y] for y in range(N)) and all((out[y][x] - T[y][x]) % (abs(q) ** (d + 1)) == 0 for y in range(N) for x in range(N))
            if d == k: ok &= all(out[y] == T[y] for y in range(N))
            allok &= ok
        line.append(f"k={k}:{gi + go}")
    print(f"s={s:3d} (s-1={q:3d}): every window [0,d], k=3..6, congruent to T_s modulo (s-1)^(d+1) and exact at d=k: {allok} ; gates at d=k: " + " ".join(line))
