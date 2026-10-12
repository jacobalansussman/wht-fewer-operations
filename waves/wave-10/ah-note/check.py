# ah-note/check.py: arithmetic for WAVE10-NOTE.md section 2.  Whole numbers only.
# textbook(d,k): Yates with only the inputs of size <= d kept, bits taken in order; a gate at stage i, address x
# (bit i set) is needed when the wire at x is not zero before the stage: weight of x on bits >= i is at most d.
from math import comb
def textbook(d, k):
    return sum(2**(i-1) * sum(comb(k-i, j) for j in range(d)) for i in range(1, k+1))
def rank(d, k):
    return sum(comb(k, j) for j in range(d+1))
# controls against ag-7's TABLE.txt and ai-0's table
ctrl = {(1,2):3,(2,2):4,(1,3):7,(2,3):11,(3,3):12,(1,4):15,(2,4):26,(3,4):31,(4,4):32,(3,11):6064,(3,13):24469,(3,15):98166,(3,17):393043}
for (d,k),v in ctrl.items():
    assert textbook(d,k) == v, (d,k,textbook(d,k),v)
print("controls: 13 of 13 textbook counts agree with ag-7's TABLE.txt and ai-0's table")
record = {4:52, 5:128, 6:304}
for k in (4,5,6):
    N = 2**k
    print(f"\n{N} points (k={k}); transform: textbook {N*k}, night's record {record[k]} (count G)")
    prev = 0
    for d in range(1, k+1):
        L = textbook(d,k); R = rank(d,k)
        route = 2*L + N - R   # M, a free diagonal, M turned round (gates change by outputs - inputs = N - R)
        print(f"  degree {d}: rank {R:3d}  textbook gates {L:4d}  step {L-prev:3d}  (N = {N})  "
              f"transform modulo {2**(d+1)} by M D M^T with textbook pieces: {route}")
        prev = L
print("\nlimit check: textbook(d,k)/N for fixed d tends to d:",
      [round(textbook(d,40)/2**40, 4) for d in (1,2,3,4)])
