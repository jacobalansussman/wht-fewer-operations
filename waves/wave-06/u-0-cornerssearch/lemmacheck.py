# u-0: check the steps of the packing lemma on a found picture, by brute force (whole numbers).
import sys, ast
txt = open(sys.argv[1]).read().split('BEST')[-1]
rows = ast.literal_eval(txt.split('rows ')[1].split(' r ')[0]); cols = ast.literal_eval(txt.split('cols ')[1].split(' c ')[0])
N = len(rows); k = N.bit_length() - 1
def rowvec(S): return [1 if (S is not None and (S & T) == T) else 0 for T in cols] + [0]
cost = []
for a in range(N):
    u = rowvec(rows[a]); v = rowvec(rows[a + 1] if a + 1 < N else None)
    d = [x - y for x, y in zip(u, v)]
    cost.append(sum(1 for b in range(N) if d[b] != d[b + 1]))
# longest block of consecutive inputs inside S
longest = {}
for S in range(N):
    best = cur = 0
    for T in cols:
        cur = cur + 1 if (S & T) == T else 0
        best = max(best, cur)
    longest[S] = best
okall = True
for c in range(1, max(cost) + 1):
    steps = sum(1 for x in cost if x <= c)
    good = [S for S in range(N) if longest[S] * c >= (1 << bin(S).count('1')) / 2]
    ok = steps <= 2 * len(good); okall &= ok
    print(f" c={c}: steps of cost <= c: {steps};  outputs owning a block of length >= 2^(|S|-1)/c: {len(good)};  steps <= 2*good: {ok}")
# each step individually: its charged output owns a block of the promised length
bad = 0
for a in range(N):
    S = rows[a]; S2 = rows[a + 1] if a + 1 < N else None
    cands = [S] if S2 is None else [X for X, Y in ((S, S2), (S2, S)) if (X & Y) != X]
    if not any(longest[X] * cost[a] >= (1 << bin(X).count('1')) / 2 for X in cands): bad += 1
print(" steps violating the block lemma:", bad, " all checks:", okall and bad == 0)
print(" corners:", sum(cost), " average longest block / 2^|S| by size:", {j: round(sum(longest[S] for S in range(N) if bin(S).count('1') == j) / (sum(1 for S in range(N) if bin(S).count('1') == j) * 2**j), 3) for j in range(k + 1)})
