#!/bin/sh
L=not-in-this-repository/wht35/bin/light.py
run() { python3 -B $L ag5-top5 280 python3 -B balanced3.py $1 $2 $3 $4 $5 $6 2>&1 | grep -v "^LIGHT" ; }
echo "three helpers, degree 4, 64 points, 60 classes (= the ag-5 lower bound), no class shared by two partitions"
run 6 4 top5 12,12,12 2500 1
run 6 4 top5 13,12,11 2500 2
run 6 4 top5 14,12,10 2500 3
