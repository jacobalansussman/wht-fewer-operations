cd waves/wave-07/x-3-boxrelations || exit 1; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
( for fam in gl so sym refl inv; do for r in 1 2 3 4; do timeout 40 nice -n 19 python3 tank.py 2 $fam $r 20 5 20; done; done
  for fam in gl so sym; do for r in 3 4 5 6; do timeout 60 nice -n 19 python3 tank.py 3 $fam $r 12 5 30; done; done ) > tan23.out 2>&1
