#!/bin/sh
L=not-in-this-repository/wht35/bin/light.py
run() { python3 -B $L ag5-$3 240 python3 -B balanced2.py $1 $2 $3 $4 $5 1 2>&1 | grep -v "^LIGHT" ; }
run 6 4 top4 12,12,11 200
run 6 4 top5 12,12,12 200
run 6 3 sup2 14,14,13 200
run 6 3 sup1 16,15,15 200
