#!/bin/sh
cd waves/wave-08/ab-0-neighboursums || exit 1
L=not-in-this-repository/wht35/bin/light.py
for t in d2m d4m; do
  for try in 1 2 3 4 5 6; do python3 -B $L ab0-B4-p3-m6-$t 590 ./mincirc_top 3 8 6 rows_B4.txt top3_$t.txt > B4_p3_m6_$t.out 2>&1; rc=$?; [ $rc = 75 ] || break; sleep 20; done
  echo "exit $rc" >> B4_p3_m6_$t.out
done
echo done > chainB.done
