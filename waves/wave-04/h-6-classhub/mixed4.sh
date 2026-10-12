#!/bin/bash
# mixed4.sh: exact minimum (count G) of the 4-point matrix K_sigma x K_tau (two DIFFERENT kernels on the two address bits) over GF(p).
# gates = 4 + m (all four rows are non-input targets when sigma, tau are not 0).  Uses d-0-zeta/mincirc, exhaustive over GF(p).
M=waves/wave-01/d-0-zeta/mincirc
for p in $*; do
  for s in $(seq 2 $((p-1))); do for t in $(seq $s $((p-1))); do
    rows=$(python3 -c "
p=$p
A=[[1,1],[1,$s]];B=[[1,1],[1,$t]]
for a in range(2):
  for b in range(2):
    print(' '.join(str(A[a][x]*B[b][y]%p) for x in range(2) for y in range(2)))")
    r=$(echo "$rows" | $M $p 4 2 2>/dev/null | grep RESULT | head -1)
    inv=$(python3 -c "print(pow($t,-1,$p))")
    case "$r" in *YES*) echo "p=$p sigma=$s tau=$t (1/tau=$inv): 6 gates";; *) r3=$(echo "$rows" | $M $p 4 3 2>/dev/null | grep RESULT | head -1); case "$r3" in *YES*) echo "p=$p sigma=$s tau=$t (1/tau=$inv): 7 gates";; *) echo "p=$p sigma=$s tau=$t (1/tau=$inv): 8 gates or more";; esac;; esac
  done; done
done
