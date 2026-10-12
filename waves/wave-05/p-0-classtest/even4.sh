#!/bin/bash
# even4.sh: the 4 x 4 block of the THIRD kernel power on rows and columns of even weight (addresses 000, 011, 101, 110):
#   M_tau = [[1,1,1,1],[1,t^2,t,t],[1,t,t^2,t],[1,t,t,t^2]]   (entry tau^(common 1-bits)).  At tau = -1 it is the 4-point transform again,
# because the even-weight addresses are a subgroup and an invertible bit matrix (an "address map") carries it to a coordinate one.
# For other tau no address map exists.  Exact minimum over GF(p), every tau; gates = 4 + m (minus targets that are inputs: none here).
cd "$(dirname "$0")"
M=../d-0-zeta/mincirc
for p in $*; do
  for tau in $(seq 2 $((p-1))); do
    rows=$(python3 -c "
p=$p;t=$tau
E=[0,3,5,6]
for w in E: print(' '.join(str(pow(t,bin(w&x).count('1'),p)) for x in E))")
    res="more than 9"
    for m in 0 1 2 3 4 5; do
      r=$(echo "$rows" | $M $p 4 $m 2>/dev/null | grep RESULT | head -1)
      case "$r" in *YES*) res="$((4+m))"; break;; esac
    done
    echo "p=$p tau=$tau (1/tau=$(python3 -c "print(pow($tau,-1,$p))")): even-weight block costs $res gates"
  done
done
