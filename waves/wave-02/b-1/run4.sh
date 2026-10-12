cd waves/wave-02/b-1 || exit 1
echo "== designs in which every form selects at least W+1 moves: no tight form, so the clique lemma is silent =="
./cover 5 19 0 design $(python3 -c "print(' '.join(format(z,'05b')+':5' for z in range(32) if bin(z).count('1')&1))") | cut -c1-230
./cover 6 7 0 design $(python3 -c "print(' '.join(format(z,'06b')+':1' for z in range(64) if bin(z).count('1')&1))") | cut -c1-230
./cover 4 19 0 design $(python3 -c "print(' '.join(format(z,'04b')+':5' for z in range(1,16)))") | cut -c1-230
./cover 5 7 0 design $(python3 -c "print(' '.join(format(z,'05b')+':2' for z in range(32) if bin(z).count('1')&1))") | cut -c1-230
echo "== block size 5, 4 arrays, 19 moves =="
for p in 0 1 2 3 4 5 6 7; do ( PARTS=8 PART=$p timeout 480 ./cover 5 4 19 dual5.txt > t19_$p.out 2>&1 || echo "TIMEOUT part $p" >> t19_$p.out ) & done
wait
cat t19_*.out | cut -c1-400
