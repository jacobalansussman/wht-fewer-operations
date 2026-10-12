#!/bin/sh
# climb.sh p k d mmax : raise m until mincirc says YES
p=$1; k=$2; d=$3; mmax=$4; mmin=${5:-0}
n=$(head -1 rows_k${k}_d${d}.txt | wc -w | tr -d ' ')
m=$mmin
while [ $m -le $mmax ]; do
  ../d-0-zeta/mincirc $p $n $m rows_k${k}_d${d}.txt > out_p${p}_k${k}_d${d}_m${m}.txt
  r=$(grep RESULT out_p${p}_k${k}_d${d}_m${m}.txt)
  echo "k=$k d=$d p=$p m=$m : $r"
  case "$r" in *YES*) break;; esac
  m=$((m+1))
done
