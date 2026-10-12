#!/bin/sh
# kstep.sh -- time single passes (harness_k): the 3-level pass alone and the first pass alone, on
# 2^11 numbers (8 KiB of floats, 16 KiB of doubles: inside the first-level cache), 9 repeats.
#   sh kstep.sh [TAG]      writes out/kstep-TAG.txt
cd "$(dirname "$0")" || exit 1
export LABEL=style-intrinsics
B=${B:-build3}
python3 -B lockwait.py sh locked_run.sh out/kstep-${1:-1}.txt $B/harness_k time -t both -k 11 11 -r ${R:-9}
echo "kstep done $(date -u)"
