# Not run (time box).  Finishes the one open case: block size 5, 4 arrays, 19 moves.  Parts 0, 1 and 4 of 8 hit the 480 s limit in run4.
# Same program, same split; give those three parts a longer limit (one job, 8 threads free -> about 3 at a time is enough).
cd waves/wave-02/b-1 || exit 1
for p in 0 1 4; do ( PARTS=8 PART=$p timeout 590 ./cover 5 4 19 dual5.txt > t19b_$p.out 2>&1 || echo "TIMEOUT part $p" >> t19b_$p.out ) & done
wait; cat t19b_*.out
