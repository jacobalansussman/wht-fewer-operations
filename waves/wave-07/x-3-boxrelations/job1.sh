cd waves/wave-07/x-3-boxrelations || exit 1; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
for fam in generic inv sym refl orth syminvall; do for r in 1 2 3 4; do timeout 100 nice -n 19 python3 boxk.py 2 $fam full $r 40 7 60; done; done > k2.out 2>&1
