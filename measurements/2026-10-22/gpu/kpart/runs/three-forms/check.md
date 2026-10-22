GPU: NVIDIA RTX PRO 6000 Blackwell Server Edition | torch 2.11.0+cu130
check cse  12N_12288  max |orig - cse| = 6.104e-05 (max |y| 4.938e+02)  PASS
check cse  20N_10240  max |orig - cse| = 9.155e-05 (max |y| 4.292e+02)  PASS
check cse  28N_14336  max |orig - cse| = 1.221e-04 (max |y| 5.630e+02)  PASS
check cse  28N_28672  max |orig - cse| = 1.831e-04 (max |y| 8.091e+02)  PASS
check cse  40N_20480  max |orig - cse| = 1.526e-04 (max |y| 6.523e+02)  PASS
check grp  12N_12288  max |orig - grp| = 9.155e-05 (max |y| 4.938e+02)  PASS
check grp  20N_10240  max |orig - grp| = 9.155e-05 (max |y| 4.292e+02)  PASS
check grp  28N_14336  max |orig - grp| = 1.221e-04 (max |y| 5.630e+02)  PASS
check grp  28N_28672  max |orig - grp| = 1.831e-04 (max |y| 8.091e+02)  PASS
check grp  40N_20480  max |orig - grp| = 1.831e-04 (max |y| 6.523e+02)  PASS
check mm   12N_12288  max |orig - mm| = 0.000e+00 (max |y| 4.938e+02)  PASS
check mm   20N_10240  max |orig - mm| = 0.000e+00 (max |y| 4.292e+02)  PASS
check mm   28N_14336  max |orig - mm| = 0.000e+00 (max |y| 5.630e+02)  PASS
check mm   28N_28672  max |orig - mm| = 0.000e+00 (max |y| 8.091e+02)  PASS
check mm   40N_20480  max |orig - mm| = 0.000e+00 (max |y| 6.523e+02)  PASS
| case | d | dtype | batch | orig us | cse us (x orig) | grp us (x orig) | mm us (x orig) | pow2 us (size) | copy us |
|---|---|---|---|---|---|---|---|---|---|
