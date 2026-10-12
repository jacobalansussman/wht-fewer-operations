cd waves/wave-07/x-3-boxrelations || exit 1; export OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3
( nice -n 19 python3 boxk.py 4 perm full 7 6 41 110
  nice -n 19 python3 boxk.py 4 perm full 6 8 42 150
  nice -n 19 python3 boxk.py 4 perm full 5 6 43 80
  nice -n 19 python3 boxk.py 4 perm full 8 3 44 60 ) > k4E.out 2>&1
