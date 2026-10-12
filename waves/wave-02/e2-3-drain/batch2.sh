#!/bin/sh
# batch2.sh: 8 points, seeds 301..3300, results kept only when the size is 21 or less; then 16 points seeded with a bent centre's chain tree, 16 seeds
for s in $(seq 301 3300); do ./drain2 8 $s 2000 2 60 30 r8big/tmp.jsonl > r8big/tmp.log; cat r8big/tmp.log >> r8big/log.txt; if grep -q 'bestU=\(1[0-9]\|20\|21\) ' r8big/tmp.log; then cp r8big/tmp.jsonl r8big/r_H8_s$s.jsonl; fi; done
