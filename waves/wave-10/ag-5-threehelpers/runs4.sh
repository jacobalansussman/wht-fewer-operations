#!/bin/sh
L=not-in-this-repository/wht35/bin/light.py
run() { python3 -B $L ag5-cal 240 python3 -B balanced2.py $1 $2 $3 $4 $5 1 2>&1 | grep -v "^LIGHT" ; }
echo "CALIBRATION 1b: two helpers, degree 2, 16 points, known optimum 14 = 8 + 6 classes"
run 4 2 top2 0,2 300
echo "CALIBRATION 2b: two helpers, degree 3, 32 points, known optimum 30 = 16 + 14 classes"
run 5 3 top2 0,2 300
echo "two helpers, degree 4, 64 points: 62 = 32 + 30"
run 6 4 top2 0,2 300
echo "two helpers, degree 4, 64 points: 61 with the kernel of dimension 4"
run 6 4 top3 0,3 600
run 6 4 top3 1,2 600
