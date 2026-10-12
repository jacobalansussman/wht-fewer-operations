#!/bin/sh
L=not-in-this-repository/wht35/bin/light.py
run() { python3 -B $L ag5-k5b 200 python3 -B balanced2.py $1 $2 $3 $4 $5 $6 2>&1 | grep -v "^LIGHT" ; }
echo "three helpers, degree 3, 32 points (two-helper optimum 30; rank bound 28; ag-5 bound 29). classes = 48 - (number of fours)"
run 5 3 top2 6,6,5 600 1
run 5 3 top3 6,6,6 1500 1
run 5 3 top3 7,6,5 1500 2
run 5 3 top3 8,6,4 1500 3
run 5 3 top4 7,6,6 1500 1
run 5 3 top4 8,6,5 1500 2
run 5 3 top4 8,7,4 1500 3
