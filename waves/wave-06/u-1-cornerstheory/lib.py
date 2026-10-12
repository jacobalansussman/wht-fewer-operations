# u-1 corners-theory: shared helpers.  Whole numbers only.
def picture(rows, cols):
    n = len(rows); m = len(cols)
    return [[1 if (rows[a] & cols[b]) == cols[b] else 0 for b in range(m)] + [0] for a in range(n)] + [[0] * (m + 1)]
def second(A):
    n = len(A) - 1; m = len(A[0]) - 1
    return [[A[a][b] - A[a+1][b] - A[a][b+1] + A[a+1][b+1] for b in range(m)] for a in range(n)]
def corners(rows, cols):
    M = second(picture(rows, cols)); return sum(1 for r in M for v in r if v), M
def bonds_count(rows, cols):
    # reformulation 2: sum over bonds (T,T') (last input with the zero column too) of the changes of g(S)=[T in S]-[T' in S] along the outputs (0 after the last)
    n = len(rows); tot = 0
    for b in range(len(cols)):
        T = cols[b]; Tp = cols[b+1] if b + 1 < len(cols) else None
        g = [(1 if (S & T) == T else 0) - (1 if (Tp is not None and (S & Tp) == Tp) else 0) for S in rows] + [0]
        tot += sum(1 for a in range(n) if g[a] != g[a+1])
    return tot
def steps_count(rows, cols):
    # reformulation 1: sum over output steps of the changes of (row S - row S') along the inputs (0 after the last)
    n = len(rows); tot = 0; per = []
    for a in range(n):
        S = rows[a]; Sp = rows[a+1] if a + 1 < n else None
        d = [(1 if (S & T) == T else 0) - (1 if (Sp is not None and (Sp & T) == T) else 0) for T in cols] + [0]
        c = sum(1 for b in range(len(cols)) if d[b] != d[b+1]); per.append(c); tot += c
    return tot, per
