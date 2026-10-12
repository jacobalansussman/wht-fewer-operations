#!/bin/sh
L=not-in-this-repository/wht35/bin/light.py
run() { python3 -B $L ag5-cal 240 python3 -B balanced2.py $1 $2 $3 $4 $5 1 2>&1 | grep -v "^LIGHT" ; }
echo "CALIBRATION 1: two helpers, degree 2, 16 points, known optimum 14 (ad-6 / aa-cross)"
run 4 2 top2 1,1 300
echo "CALIBRATION 2: two helpers, degree 3, 32 points, known optimum 30 (ad-6)"
run 5 3 top2 1,1 300
echo "two helpers, degree 4, 64 points: 62 (ad-6 has 62), then 61"
run 6 4 top2 1,1 300
run 6 4 top3 2,1 300
run 6 4 top3 3,0 300
