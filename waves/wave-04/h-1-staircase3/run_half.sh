#!/bin/sh
# least gate count found (count G, 0/+-1 wires, annealing: an upper bound) for each half problem on 8 points
cd waves/wave-04/h-1-staircase3 || exit 1
for t in tg8_e*_f*.txt; do
  r=$(./sa2 3 seed8_textbook.txt 4 9 0.45 sol_$t 1 3 $t | tail -1 | sed 's/.*best \([0-9]*\) gates.*/\1/')
  echo "$t best $r"
done
