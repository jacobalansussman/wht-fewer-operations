#!/bin/sh
L=not-in-this-repository/wht35/bin/light.py
run() { python3 -B $L ag5-k7 590 python3 -B balanced2.py $1 $2 $3 $4 $5 $6 2>&1 | grep -v "^LIGHT" ; }
echo "three helpers, degree 5, 128 points (rank bound 122; ag-5 bound 123)"
run 7 5 top4 23,23,22 60 1
run 7 5 top5 23,23,23 120 1
