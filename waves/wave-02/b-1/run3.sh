cd waves/wave-02/b-1 || exit 1
echo "== block size 6, 8 arrays: every odd-weight direction once (32 moves, plain 48), ALL forms =="
./cover 6 8 0 design $(python3 -c "print(' '.join(format(z,'06b')+':1' for z in range(64) if bin(z).count('1')&1))") | cut -c1-200
echo "== block size 5, 4 arrays, 18 moves =="
for p in 0 1 2 3 4 5 6 7; do ( PARTS=8 PART=$p timeout 400 ./cover 5 4 18 dual5.txt > t18_$p.out 2>&1 || echo "TIMEOUT part $p" >> t18_$p.out ) & done
wait
cat t18_*.out
echo "== block size 4, more arrays, up to one move below plain =="
for a in "9 35" "10 39" "11 43" "12 47" "13 51" "16 63"; do set -- $a; timeout 20 ./cover 4 $1 $2 dual4.txt || echo "TIMEOUT 4 $1 $2"; done
