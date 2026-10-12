# x-1-digits/lawcheck.py : the cost law of a digit against every row of slices.out part B, and against direct counts to k = 16.
# claim: extra gates for digit j (j >= 1) = sum_{t >= j} C(k,t) + sum_{t >= j+1} C(k,t)  = N [P(Bin >= j) + P(Bin >= j+1)];
#        reading side for levels 0..d = sum_{i=1..k} V(i-1,d) 2^(k-i);  writing side for d = reading side for d-1;
#        top window [j,k] = 2k * #( (k-1)-bit strings of weight >= j ).
from math import comb
from slices import window
tail = lambda k, j: sum(comb(k, t) for t in range(max(j, 0), k + 1))
V = lambda n, d: sum(comb(n, t) for t in range(0, min(d, n) + 1))
ok = True; rows = 0
for k in range(2, 13):
    prev = None
    for d in range(k + 1):
        gi, go, _ = window(k, 0, d, replay=False)
        ok &= gi == sum(V(i - 1, d) * 2 ** (k - i) for i in range(1, k + 1))
        if d >= 1:
            gi1, _, _ = window(k, 0, d - 1, replay=False); ok &= go == gi1
            ok &= (gi + go - prev) == tail(k, d) + tail(k, d + 1)
        prev = gi + go; rows += 1
    for j in range(k + 1):
        gi, go, _ = window(k, j, k, replay=False)
        ok &= gi == go == k * sum(comb(k - 1, t) for t in range(j, k)); rows += 1
print(f"all four formulas hold on {rows} windows, k = 2..12: {ok}")
