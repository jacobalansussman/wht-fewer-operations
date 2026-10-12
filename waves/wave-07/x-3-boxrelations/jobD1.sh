cd waves/wave-07/x-3-boxrelations || exit 1; export OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3
( nice -n 19 python3 boxk.py 4 refl full 7 4 31 520 ) > k4D1.out 2>&1
