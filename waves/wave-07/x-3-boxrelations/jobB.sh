cd waves/wave-07/x-3-boxrelations || exit 1; export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
( for fam in gl so sym refl inv; do for r in 1 2 3 4; do nice -n 19 python3 tank.py 2 $fam $r 20 5 6; done; done
  for fam in gl so sym; do for r in 3 4 5 6; do nice -n 19 python3 tank.py 3 $fam $r 16 5 12; done; done
  for fam in so refl inv sym gl; do for r in 4 5 6 7 8; do nice -n 19 python3 tank.py 4 $fam $r 12 5 15; done; done ) > tan.out 2>&1
( for fam in generic sym inv; do
  for r in 4 5 6 7 8; do nice -n 19 python3 boxk.py 4 $fam skew $r 30 13 20; done
  for r in 5 6 7 8; do nice -n 19 python3 boxk.py 4 $fam sym $r 30 13 30; done
done ) > k4B.out 2>&1
