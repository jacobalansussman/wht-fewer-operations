cd waves/wave-07/x-3-boxrelations || exit 1; export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
( for fam in orth refl; do
  for r in 2 3 4 5 6; do nice -n 19 python3 boxk.py 4 $fam skew $r 30 11 25; done
  for r in 3 4 5 6 7; do nice -n 19 python3 boxk.py 4 $fam symtl $r 30 11 40; done
done ) > k4A.out 2>&1
