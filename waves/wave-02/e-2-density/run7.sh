#!/bin/bash
cd waves/wave-02/e-2-density || exit 1
gcc -O2 -o mincirc_pad mincirc_pad.c 2>/dev/null
for k in 6 7 8; do
  echo "== m7a k=$k"; NPAD=1 timeout 170 ./mincirc_pad 3 8 $k rows_m7a.txt | grep -E "RESULT|visited|non-input"; echo "rc=${PIPESTATUS[0]}"
done
echo DONE
