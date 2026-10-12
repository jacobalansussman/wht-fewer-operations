#!/bin/zsh
# the 7-gate circuits of the two deep kernels at 4 points, listed, with examples that no shallow class can build
cd waves/wave-10/ag-6-deepgates || exit 1
L=not-in-this-repository/wht35/bin/light.py
run() { out=$1; shift; for tries in 1 2 3 4 5 6 7 8; do python3 -B $L ag6e 400 "$@" > $out 2>&1; rc=$?; [ $rc -ne 75 ] && break; sleep 15; done }
run k3x2_enum3_class.out ./deepmin4f 4 766 0 3 -T k3x2.txt -E 3 16777482
run km3x2_enum3_4958.out ./deepmin4f 4 750 0 3 -T km3x2.txt -E 3 4958
echo done > runE.done
