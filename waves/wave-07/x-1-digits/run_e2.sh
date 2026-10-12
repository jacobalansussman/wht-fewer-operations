#!/bin/bash
# usage: run_e2.sh rowsfile n "primes" "ms" seconds
M=waves/wave-01/d-0-zeta/mincirc
for p in $3; do for m in $4; do
  echo "== rows=$1 p=$p m=$m"
  python3 -B not-in-this-repository/wht35/bin/light.py x1-e2 $5 $M $p $2 $m $1 2>&1 | grep -v "^  example" | head -8
done; done
