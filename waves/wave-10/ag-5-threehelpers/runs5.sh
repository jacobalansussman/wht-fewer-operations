#!/bin/sh
L=not-in-this-repository/wht35/bin/light.py
run() { python3 -B $L ag5-k5 280 python3 -B balanced2.py $1 $2 $3 $4 $5 $6 2>&1 | grep -v "^LIGHT" ; }
echo "three helpers, degree 3, 32 points (two-helper optimum 30; rank bound 28; ag-5 bound 29)"
run 5 3 top2 5,5,5 400 1
run 5 3 top3 6,5,5 1500 1
run 5 3 top3 7,5,4 1500 2
run 5 3 top4 6,6,5 1500 1
run 5 3 top4 7,6,4 1500 2
run 5 3 top4 8,5,4 1500 3
