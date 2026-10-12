#!/bin/sh
# after the bent run: a design on which the pair bound is only 32 (found by lbdesign.py); exact-cover model, then overlapping model
cd waves/wave-05/p-1-letter16 || exit 1
while ps -eo args | grep -q "[r]fix.py dual16 gen 300 4 bent"; do sleep 2; done
sleep 3
while ps -eo args | grep -q "[r]fix.py dual16 tile 40 4 bent"; do sleep 2; done
R=1,-1,1,-1,-1,1,1,-1,-1,-1,-1,-1,1,1,-1,-1; C=1,-1,1,1,1,1,-1,1,1,1,1,-1,1,-1,-1,-1
nice -n 19 timeout 60 python3 rfix.py dual16 tile 40 4 bound32 $R $C > bound32.out 2>&1
nice -n 19 timeout 330 python3 rfix.py dual16 gen 300 4 bound32 $R $C >> bound32.out 2>&1
