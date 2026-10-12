#!/bin/sh
# full.sh -- the runs of this folder, one after the other, each under the shared lock
cd "$(dirname "$0")" || exit 1
LABEL=style-fused sh locked_run.sh out/time-float.txt  build/harness time -t float  -k 3 26 -r 9 -v ffht,ffhtB,Tp,G19p,G19ap
LABEL=style-fused sh locked_run.sh out/time-double.txt build/harness time -t double -k 3 26 -r 9 -v ffht,ffhtB,Tp,G19p,G19ap
LABEL=style-fused sh locked_run.sh out/time-int32.txt  build/harness time -t int32  -k 3 26 -r 9 -v Tp,G19sp,G19ap
LABEL=style-fused sh locked_run.sh out/uarch-3.txt build/uarch 9
for k in 6 9 12 15 18 21 24; do
  LABEL=style-fused sh locked_run.sh out/time-scalar-k$k.txt build/harness time -t int32 -k $k $k -r 9 -v Tp,sT,sG19
done
date -u > out/full.done
