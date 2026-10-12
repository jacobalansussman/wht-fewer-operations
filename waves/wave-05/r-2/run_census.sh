#!/bin/bash
# r-2: number of 3-helper sets (7 gates, count G) for the 4-point kernel power, by r2_brute (independent of mincirc).
# usage: run_census.sh B p tau...     (tau = "all" for 2..p-1)
cd "$(dirname "$0")"
B=$1; p=$2; shift; shift
taus="$*"; [ "$taus" = "all" ] && taus=$(seq 2 $((p-1)))
for tau in $taus; do
  printf "tau=%s (1/tau=%s): " $tau $(python3 -c "print(pow($tau,-1,$p))")
  python3 -c "
p=$p;t=$tau
for w in range(4): print(' '.join(str(pow(t,bin(w&x).count('1'),p)) for x in range(4)))" | ./r2_brute $p 4 3 $B
done
