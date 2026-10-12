#!/bin/sh
# usage: batch.sh p W seedfile pool T0 moves firstseed lastseed   (run under timeout; one line per run)
p=$1; W=$2; sf=$3; pool=$4; T0=$5; mv=$6; a=$7; b=$8
s=$a
while [ $s -le $b ]; do ./fpgame $p 8 $W $mv $s $T0 $pool $sf; s=$((s+1)); done
