#!/bin/sh
L=not-in-this-repository/wht35/bin/light.py
run() { python3 -B $L ag5-$3 200 python3 -B balanced.py $1 $2 $3 $4 $5 1 2>&1 | grep -v "^LIGHT" ; }
run 6 4 top3 12,11,11 300
run 6 4 top4 12,12,11 300
run 6 4 top5 12,12,12 300
run 6 4 top5 12,12,11 300
run 6 4 top6 13,12,12 100
