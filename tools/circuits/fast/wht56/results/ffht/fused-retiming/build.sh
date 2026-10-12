#!/bin/sh
set -e
cd "$(dirname "$0")"
F=${FFHT_DIR:-../FFHT}                # the clone of FFHT, built by its own Makefile
SRC=../style-fused                   # the sources that are timed
J="-Wa,-mbranches-within-32B-boundaries"
mkdir -p b
gcc -std=gnu11 -O3 -march=native -fno-tree-reassoc $J -c $SRC/whtf.c -o b/whtf.o
gcc -std=gnu11 -O3 -march=native -fno-tree-reassoc $J -S $SRC/whtf.c -o b/whtf.s
gcc -std=gnu11 -O2 -march=native -fno-tree-reassoc $J -c $SRC/whtf.c -o b/whtf_O2.tmp.o
objcopy --prefix-symbols=O2_ b/whtf_O2.tmp.o b/whtf_O2.o
gcc -std=gnu11 -O3 -mavx2 -mfma -fno-tree-reassoc $J -c $SRC/whtf.c -o b/whtf_gen.tmp.o
objcopy --prefix-symbols=GEN_ b/whtf_gen.tmp.o b/whtf_gen.o
gcc -std=gnu11 -O3 -march=native -fno-tree-vectorize -fno-tree-slp-vectorize -fwrapv $J -c $SRC/whts.c -o b/whts.o
gcc -std=gnu11 -O2 -march=native -Wall -I$SRC -I$F mycheck.c b/whtf.o b/whtf_O2.o b/whtf_gen.o b/whts.o $F/fht.o $F/fast_copy.o -o b/mycheck -lm
gcc -std=gnu11 -O2 -march=native -Wall -I$SRC -I$F reftime.c b/whtf.o b/whtf_O2.o b/whtf_gen.o $F/fht.o $F/fast_copy.o -o b/reftime -lm
echo built
