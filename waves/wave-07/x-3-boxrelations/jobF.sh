cd waves/wave-07/x-3-boxrelations || exit 1; export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
( for r in 2 3 4; do nice -n 19 python3 boxk.py 4 perm skew $r 40 51 25; done
  for r in 2 3 4; do nice -n 19 python3 boxk.py 4 perm sym $r 40 52 25; done ) > k4F.out 2>&1
