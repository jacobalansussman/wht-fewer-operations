cd waves/wave-07/x-3-boxrelations || exit 1; export OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3
( for r in 2 3 4; do nice -n 19 python3 boxk.py 2 rot full $r 20 21 6; nice -n 19 python3 boxk.py 2 oboth full $r 20 21 8; done
  nice -n 19 python3 boxk.py 4 refl full 6 4 32 480 ) > k4D2.out 2>&1
