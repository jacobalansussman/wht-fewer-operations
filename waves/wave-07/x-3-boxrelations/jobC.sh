cd waves/wave-07/x-3-boxrelations || exit 1; export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
( for r in 8 7 6; do nice -n 19 python3 boxk.py 4 generic skew $r 30 21 35; done
  for r in 8 7; do nice -n 19 python3 boxk.py 4 refl skew $r 30 21 35; done
  for r in 8 7; do nice -n 19 python3 boxk.py 4 generic sym $r 30 21 50; done
  nice -n 19 python3 boxk.py 4 refl symtl 8 30 21 50
  for r in 8 6 4; do nice -n 19 python3 boxk.py 4 rot skew $r 30 21 35; done
  for r in 8 7 6; do nice -n 19 python3 boxk.py 4 rot symtl $r 30 21 50; done
  for r in 2 3 4; do nice -n 19 python3 boxk.py 2 rot full $r 30 21 10; nice -n 19 python3 boxk.py 2 oboth full $r 30 21 10; done
) > k4C.out 2>&1
( for fam in refl so; do for r in 8 7 6 5; do nice -n 19 python3 tank.py 4 $fam $r 12 9 60; done; done ) > tan4.out 2>&1
