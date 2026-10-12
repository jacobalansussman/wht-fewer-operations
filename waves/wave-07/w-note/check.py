# w-note/check.py : arithmetic re-checks for WAVE7-NOTE.md (formulas only; no circuit is replayed here)
from fractions import Fraction as F
from math import comb, log, log2, ceil
print("1. x-1 digit law: digit 0 = N-1 gates, digit j>=1 = N*(P(Bin>=j)+P(Bin>=j+1))")
for k in range(2, 9):
    N = 2**k
    tail = lambda j: F(sum(comb(k, i) for i in range(j, k+1)), N) if j <= k else F(0)
    d = [F(N-1)] + [N*(tail(j)+tail(j+1)) for j in range(1, k+1)]
    assert all(x.denominator == 1 for x in d)
    d = [int(x) for x in d]
    m4 = d[0]+d[1]; m8 = m4 + (d[2] if k >= 2 else 0); m16 = m8 + (d[3] if k >= 3 else 0)
    print(f"  N={N:4d} mod4={m4:4d} (3N-k-3={3*N-k-3}) mod8={m8:5d} (5N-(k^2+5k+10)/2={5*N-(k*k+5*k+10)//2}) mod16={m16:5d} third digit={d[2]:4d} all digits={sum(d)} N*k={N*k}")
print("2. x-6 closed form: saving = L/(ln k + L), L = ln(1/(1-rho))")
for kk, rho in [(2, .074), (3, .115), (6, .18), (2, .1), (16.5, .0021)]:
    L = -log(1-rho); print(f"  blocks={kk} rho={rho}: {L/(log(kk)+L):.5f}")
print("3. height lemma L3 at small sizes: N-1 + ((N/2)log2N-(N-1)log2M)/log2(4M^2); M=1 uses log2 3")
for k in (3, 4, 10, 14, 20):
    N = 2**k; row = []
    for M in (1, 2, 3, 16):
        b = N-1 + ((N/2)*k)/log2(3) if M == 1 else N-1 + max(0.0, (N/2)*k-(N-1)*log2(M))/log2(4*M*M)
        row.append(f"M={M}: {ceil(b-1e-9)}")
    print(f"  N=2^{k} trivial 2N-2={2*N-2}  " + "  ".join(row))
print("   digits per gate needed on average for C*N gates: (log2 N)/(4C) - 1")
for k in (20, 40, 100, 1000):
    print(f"   log2 N={k}: " + ", ".join(f"C={C}: {k/(4*C)-1:.2f}" for C in (1, 2, 3, 5)))
print("4. x-4 lemma D: least r with r >= 2^(ceil(k/r)-2)")
for k in (4, 6, 8, 16, 64, 1024, 4096, 65536, 2**20):
    r = 1
    while r < 2**(ceil(k/r)-2): r += 1
    print(f"  k={k}: r>={r}  r*log2(k)/k={r*log2(k)/k:.2f}  known program k/2={k//2}")
print("5. adding-only neighbour sums: N(k-1-floor(k/2)/2)")
print("  ", [int(2**k*(F(k-1)-F(k//2, 2))) for k in range(2, 11)])
print("6. x-9 hub family: (3/4)N log2 N + N/4 and (5/4)N log2 N - N/4")
print("  ", [(3*2**k*k)//4 + 2**k//4 for k in range(2, 7)], [(5*2**k*k)//4 - 2**k//4 for k in range(3, 7)])
print("7. floors: N-1+(N/2)log2N =", [2**k-1+2**(k-1)*k for k in range(1, 7)])
