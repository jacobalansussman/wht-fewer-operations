#!/bin/bash
# count (G) minimum circuits modulo p: the cyclic Fourier matrix at 4 points (i = 2 mod 5, 5 mod 13, 4 mod 17) against H at 4 points (known: 7)
cd "$(dirname "$0")"
MC=../d-0-zeta/mincirc
L="python3 -B not-in-this-repository/wht35/bin/light.py"
run() { for try in 1 2 3 4 5 6; do $L ab7-mc2 $1 $MC $2 $3 $4 $5 > .tmp2.$$ 2>&1; rc=$?; [ $rc -ne 75 ] && break; sleep 7; done; grep -h "RESULT" .tmp2.$$ | cut -c1-120; rm -f .tmp2.$$; }
python3 - <<'PY'
for p,i in ((5,2),(13,5),(17,4)):
    open(f"rows_f4_p{p}.txt","w").write("\n".join(" ".join(str(pow(i,s*t,p)) for t in range(4)) for s in range(4))+"\n")
open("rows_h4.txt","w").write("1 1 1 1\n1 -1 1 -1\n1 1 -1 -1\n1 -1 -1 1\n")
PY
for p in 5 13; do for m in 2 3; do echo "## H4 p=$p gates=$((4+m))"; run 60 $p 4 $m rows_h4.txt; done; done
for p in 5 13 17; do for m in 1 2 3 4; do echo "## Fourier4 p=$p gates=$((4+m))"; run 100 $p 4 $m rows_f4_p$p.txt; done; done
echo DONE
