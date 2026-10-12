#!/bin/sh
# batch.sh N firstseed lastseed K coefset maxgates maxsec dir
N=$1; d=$8
for s in $(seq $2 $3); do ./drain $N $s $4 $5 $6 $7 $d/r_H${N}_c$5_s$s.jsonl; done
