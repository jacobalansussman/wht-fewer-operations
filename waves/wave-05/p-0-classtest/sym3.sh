#!/bin/bash
# sym3.sh: exact minimum (count G) of the 3 x 3 block S_tau = K (x) K on data symmetric in the two address bits,
# S_tau = [[1,2,1],[1,1+tau,tau],[1,2tau,tau^2]], for every tau over GF(p).  gates = 3 + m.  tool: g-5-k3/mincirc_odd (exhaustive).
cd "$(dirname "$0")"
M=../g-5-k3/mincirc_odd
for p in $*; do
  for tau in $(seq 2 $((p-1))); do
    python3 -c "
p=$p;t=$tau
S=[[1,2,1],[1,1+t,t],[1,2*t,t*t]]
for r in S: print(' '.join(str(x%p) for x in r))" > ./p0_sym3_rows.tmp 2>/dev/null || python3 -c "
p=$p;t=$tau
S=[[1,2,1],[1,1+t,t],[1,2*t,t*t]]
for r in S: print(' '.join(str(x%p) for x in r))" > rows_sym3_tmp.txt
    f=rows_sym3_tmp.txt; [ -s ./p0_sym3_rows.tmp ] && cp ./p0_sym3_rows.tmp $f
    for m in 0 1 2 3 4; do
      r=$($M $p 3 $m $f 2>/dev/null | grep RESULT | head -1)
      case "$r" in *YES*) echo "p=$p tau=$tau (1/tau=$(python3 -c "print(pow($tau,-1,$p))")): S_tau costs $((3+m)) gates"; break;; esac
    done
  done
done
