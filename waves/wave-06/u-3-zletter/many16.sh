#!/bin/sh
# 24 random-start anneals at 16 points for each objective (rectangles tau, then gates); prints the best value of each run
cd waves/wave-06/u-3-zletter || exit 1
for s in 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124; do ./zmst 4 $s 400000 1.0 2>/dev/null | head -1; done
for s in 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124; do GATES=1 ./zmst 4 $s 400000 1.0 2>/dev/null | head -1; done
