#!/bin/zsh
# which single extra coefficient c pays against the reference {1,2}?  4 inputs, 4 to 7 targets, c = 4..9
cd waves/wave-10/ag-6-deepgates || exit 1
L=not-in-this-repository/wht35/bin/light.py
run() { out=$1; shift; for tries in 1 2 3 4 5 6; do python3 -B $L ag6c 590 "$@" > $out 2>&1; rc=$?; [ $rc -ne 75 ] && break; sleep 20; done }
for c in 4 5 6 7 8 9; do for m in 4 5 6 7; do run n4_m${m}_ref6_plus${c}.out ./deepmin4 $m 6 $((6 + (1<<c))) 3; done; done
run n4_m8_ref6_ch278_div3.out ./deepmin4 8 6 278 3
run n4_m8_ref6_ch14_div3.out ./deepmin4 8 6 14 3
echo done > runC.done
