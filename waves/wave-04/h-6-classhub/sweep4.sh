#!/bin/bash
# sweep4.sh: exact minimum (count G, projective) of the 4-point kernel K x K, K = [[1,1],[1,tau]], over GF(p), every tau.
# uses d-0-zeta/mincirc (exhaustive over GF(p)); m = number of helper wires; gates = (targets that are not inputs) + m.
M=waves/wave-01/d-0-zeta/mincirc
for p in $*; do
  for tau in $(seq 0 $((p-1))); do
    rows=$(python3 -c "
p=$p;t=$tau
K=[[1,1],[1,t]]
for a in range(2):
  for b in range(2):
    print(' '.join(str(K[a][x]*K[b][y]%p) for x in range(2) for y in range(2)))")
    line="p=$p tau=$tau:"
    for m in 0 1 2 3; do
      r=$(echo "$rows" | $M $p 4 $m 2>/dev/null | grep RESULT | head -1)
      line="$line m=$m [$r]"
      case "$r" in *YES*|*yes*|*found*) break;; esac
    done
    echo "$line"
  done
done
