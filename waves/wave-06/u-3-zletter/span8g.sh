#!/bin/sh
# spanning-model gate count (whole numbers, no junction points) on the 125 classes whose exact count is 12 gates, and on every 40th class
cd waves/wave-06/u-3-zletter || exit 1
: > span8g.txt
paste -d' ' out8zg_all.txt in8z.txt | awk '$1==5 || NR%40==0' | while read x a b c d e f g rest; do
  echo "$a $b $c $d $e $f $g" > span8g_tmp.txt
  s=$(GATES=1 ./zmst 3 1 0 1 span8g_tmp.txt 2>/dev/null | head -1 | awk '{gsub(/\)/,"",$8); print $8}')
  echo "$x $s" >> span8g.txt
done
