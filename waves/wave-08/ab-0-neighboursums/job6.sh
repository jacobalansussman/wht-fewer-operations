#!/bin/sh
cd waves/wave-08/ab-0-neighboursums || exit 1
for t in d2p d4p; do timeout 540 nice -n 19 ./mincirc_top 3 8 6 rows_B4.txt top3_$t.txt > B4_p3_m6_$t.lin.out 2>&1; echo "exit $?" >> B4_p3_m6_$t.lin.out; done
echo done > job6.done
