#!/bin/zsh
# "3 is free, does 4 or 8 add anything" (reference {1,2,3} = 14, challenger {1,2,3,4,8} = 286); full sign vectors; no division
cd waves/wave-10/ag-6-deepgates || exit 1
L=not-in-this-repository/wht35/bin/light.py
run() { out=$1; shift; for tries in 1 2 3 4 5 6; do python3 -B $L ag6b 590 "$@" > $out 2>&1; rc=$?; [ $rc -ne 75 ] && break; sleep 20; done }
for m in 4 5 6 7; do run n4_m${m}_ref14_ch286_div3.out ./deepmin4 $m 14 286 3; done
for m in 4 5 6 7; do run n4_m${m}_ref6_ch278_div0.out ./deepmin4 $m 6 278 0; done
for m in 4 5 6 7; do run n4_m${m}_ref6_ch14_div0.out ./deepmin4 $m 6 14 0; done
for m in 1 2 3 4 5 6 7 8; do run n4_full_m${m}_ref6_ch278_div3.out ./deepmin4 $m 6 278 3 1 6; done
for m in 4 5 6 7; do run n4_m${m}_ref6_ch1022.out ./deepmin4 $m 6 1022 3; done
for m in 4 5 6 7; do run n4_m${m}_ref14_ch1022.out ./deepmin4 $m 14 1022 3; done
echo done > runB2.done
