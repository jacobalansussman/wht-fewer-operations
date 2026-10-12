#!/bin/sh
# spanning-tree model (no junction points, whole numbers) on every 8-point input tree class: tau and gates, to compare with the
# exact census (junction points allowed, modulo 3).  Output: span8.txt, one line per tree: "tau gates-(N-1)"
cd waves/wave-06/u-3-zletter || exit 1
: > span8.txt
while read a b c d e f g rest; do
  echo "$a $b $c $d $e $f $g" > span8_tmp.txt
  t=$(./zmst 3 1 0 1 span8_tmp.txt 2>/dev/null | head -1 | awk '{print $4}')
  s=$(GATES=1 ./zmst 3 1 0 1 span8_tmp.txt 2>/dev/null | head -1 | awk '{print $7}')
  echo "$t $s" >> span8.txt
done < in8z.txt
