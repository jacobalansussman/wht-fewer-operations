#!/bin/sh
# second job slot: waits for the sampler to finish, then growth of the rank-2 family (4, 8, 32 points), then general (overlapping) mode on two sign designs
cd waves/wave-05/p-1-letter16 || exit 1
while ps -eo args | grep -q "[s]amp.py dual16 quad"; do sleep 3; done
sig() { python3 -c "
k=$1; N=1<<k
print(','.join(str((-1)**((y&1)*(1^(y>>(k-1)&1)))) for y in range(N)), ','.join(str((-1)**((x&1)*(x>>(k-1)&1))) for x in range(N)))"; }
for k in 2 3 5; do set -- $(sig $k); nice -n 19 timeout 200 python3 rfix.py dual$((1<<k)) tile 150 4 rank2family $1 $2; done > family.out 2>&1
# bent x0x3+x1x2 on both sides (the design that minimises the row-pair bound), overlapping mode
B=$(python3 -c "print(','.join(str((-1)**(((x&1)*(x>>3&1))^((x>>1&1)*(x>>2&1)))) for x in range(16)))")
nice -n 19 timeout 330 python3 rfix.py dual16 gen 300 4 bent_x0x3+x1x2 $B $B > bentgen.out 2>&1
nice -n 19 timeout 60 python3 rfix.py dual16 tile 40 4 bent_x0x3+x1x2 $B $B >> bentgen.out 2>&1
