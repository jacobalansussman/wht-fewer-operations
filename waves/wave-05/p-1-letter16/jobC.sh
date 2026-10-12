#!/bin/sh
# first job slot after the free-sign run: (c) a chain pair perpendicular at some levels only, (d) a tree that is not a chain of subgroups; exact-cover model, free signs
cd waves/wave-05/p-1-letter16 || exit 1
while ps -eo args | grep -q "[r]f.py dual16 tile"; do sleep 3; done
nice -n 19 timeout 230 python3 rf.py half16a tile 200 > half16a_tile.out 2>&1
nice -n 19 timeout 230 python3 rf.py quaddual16 tile 200 > quaddual16_tile.out 2>&1
