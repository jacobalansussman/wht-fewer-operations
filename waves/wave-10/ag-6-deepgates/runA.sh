#!/bin/zsh
# experiment (a), 4 inputs: reference {1,2} (mask 6) against {1,2,4,8} (mask 278); control {1,2,3} (mask 14)
cd waves/wave-10/ag-6-deepgates || exit 1
L=not-in-this-repository/wht35/bin/light.py
for m in 2 3 5 6 7; do
  for tries in 1 2 3 4 5 6; do python3 -B $L ag6a 590 ./deepmin4 $m 6 278 3 > n4_m${m}_ref6_ch278_div3.out 2>&1; rc=$?; [ $rc -ne 75 ] && break; sleep 20; done
  for tries in 1 2 3 4 5 6; do python3 -B $L ag6a 590 ./deepmin4 $m 6 14 3 > n4_m${m}_ref6_ch14_div3.out 2>&1; rc=$?; [ $rc -ne 75 ] && break; sleep 20; done
done
echo done > runA.done
