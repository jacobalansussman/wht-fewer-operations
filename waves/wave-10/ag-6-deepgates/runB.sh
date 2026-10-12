#!/bin/zsh
# 5 inputs with 4 targets; then "3 is free, does 4 add anything" (reference {1,2,3} = 14, challenger {1,2,3,4,8} = 286); full sign vectors
cd waves/wave-10/ag-6-deepgates || exit 1
L=not-in-this-repository/wht35/bin/light.py
run() { out=$1; shift; for tries in 1 2 3 4 5 6; do python3 -B $L ag6b 590 "$@" > $out 2>&1; rc=$?; [ $rc -ne 75 ] && break; sleep 20; done }
run n5_m4_ref6_ch278_div3.out ./deepmin5 4 6 278 3
run n5_m4_ref6_ch14_div3.out ./deepmin5 4 6 14 3
for m in 4 5 6; do run n4_m${m}_ref14_ch286_div3.out ./deepmin4 $m 14 286 3; done
for m in 1 2 3 4 5 6 7 8; do run n4_full_m${m}_ref6_ch278_div3.out ./deepmin4 $m 6 278 3 1 6; done
for m in 4 5 6; do run n4_m${m}_ref6_ch278_div0.out ./deepmin4 $m 6 278 0; done
run n5_m3_ref6_ch278_div3.out ./deepmin5 3 6 278 3
echo done > runB.done
