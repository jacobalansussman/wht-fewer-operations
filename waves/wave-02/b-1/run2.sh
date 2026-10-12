cd waves/wave-02/b-1 || exit 1
gcc -O2 -o cover cover.c
for p in 0 1 2 3 4 5 6 7; do ( PARTS=8 PART=$p timeout 400 ./cover 5 4 17 dual5.txt > t17_$p.out 2>&1 || echo "TIMEOUT part $p" >> t17_$p.out ) & done
wait
cat t17_*.out
