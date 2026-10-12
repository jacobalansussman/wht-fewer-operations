#!/usr/bin/env python3
"""scan.py p size count seed [timeout_s]: for random invertible size x size matrices over GF(p), find by exhaustive search
(ds.c, count G over GF(p)) the fewest gates L1 for one copy, then ask whether two copies can be done in 2*L1 - 1 gates."""
import sys, random, subprocess, time
p, n, count, seed = map(int, sys.argv[1:5]); budget = float(sys.argv[5]) if len(sys.argv) > 5 else 150
random.seed(seed); t0 = time.time()
def det(M):
    M = [r[:] for r in M]; d = 1
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] % p), None)
        if piv is None: return 0
        if piv != c: M[c], M[piv] = M[piv], M[c]; d = -d
        d = d * M[c][c] % p; inv = pow(M[c][c], p - 2, p)
        for r in range(c + 1, n):
            f = M[r][c] * inv % p
            M[r] = [(a - f * b) % p for a, b in zip(M[r], M[c])]
    return d % p
def run(rows, nn, F):
    txt = f"{len(rows)}\n" + "\n".join(" ".join(map(str, r)) for r in rows) + "\n"
    out = subprocess.run(["./ds", str(p), str(nn), str(F), "0", "1"], input=txt, capture_output=True, text=True).stdout
    return out.startswith("FOUND"), out.splitlines()[0] if out else ""
tested = 0; discounts = 0; hist = {}
while tested < count and time.time() - t0 < budget:
    A = [[random.randrange(p) for _ in range(n)] for _ in range(n)]
    if det(A) == 0: continue
    F1 = None
    for F in range(0, 7):
        ok, line = run(A, n, F)
        if ok: F1 = int(line.split("nontarget=")[1].split()[0]); T1 = int(line.split("total_gates=")[1]) - F1; break
    if F1 is None or F1 == 0: continue          # F1 = 0: nothing to share
    if 2 * F1 - 1 > 5: continue                 # too deep for this time box
    AA = [r + [0] * n for r in A] + [[0] * n + r for r in A]
    ok, line = run(AA, 2 * n, 2 * F1 - 1)
    tested += 1; hist[(T1 + F1, ok)] = hist.get((T1 + F1, ok), 0) + 1
    if ok: discounts += 1; print("DISCOUNT", A, line, flush=True)
print(f"p={p} size={n}: tested {tested} matrices with at least one shared-able gate; two copies cheaper than twice one: {discounts}; "
      f"histogram (gates for one copy, discount found): {sorted(hist.items())}; {time.time()-t0:.0f}s")
