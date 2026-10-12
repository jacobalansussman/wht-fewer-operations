#!/bin/bash
# minimum circuits (count G) modulo p for the Pascal matrix, with subset sums (zeta) as the known-answer check
cd "$(dirname "$0")"
MC=../d-0-zeta/mincirc
L="python3 -B not-in-this-repository/wht35/bin/light.py"
run() { # label secs p n m rows
  for try in 1 2 3 4 5 6; do
    $L ab7-mc $1 $MC $2 $3 $4 $5 > .tmp.$$ 2>&1; rc=$?
    if [ $rc -ne 75 ]; then break; fi; sleep 7
  done
  grep -h "RESULT\|LIGHT" .tmp.$$ | cut -c1-200; rm -f .tmp.$$
}
for p in 3 5 7; do for m in 0 1; do echo "## zeta4 p=$p m=$m"; run 60 $p 4 $m ../d-0-zeta/rows_zeta2.txt; done; done
for p in 3 5 7 11; do for m in 0 1 2; do echo "## pascal4 p=$p m=$m"; run 60 $p 4 $m rows_pascal4.txt; done; done
for m in 2 3 4 5; do for p in 3 5; do echo "## pascal8 p=$p m=$m"; run 240 $p 8 $m rows_pascal8.txt; done; done
echo DONE
