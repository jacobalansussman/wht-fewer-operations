# x86-hybrid-small summary: the circuits at library sizes (64-512 points), many vectors per call

- Machine: AMD EPYC 9B14; AMD Zen 4 Genoa (2 FADD + 2 FMA pipes; AVX-512 on 256-bit units)
- BATCH: L2 per core 1024 KB (sysfs, cpu43); batch footprint BATCH_KB = 512 KB (B = BATCH_KB / (n x element size))
- Quiet gate: every timing passed az_quiet (or see quiet.log)
- Finite data: 610 of 610 timed (program, size) results ended every repeat finite and free of subnormals.
- One timed call (B vectors) took 21.4-76.0 us (median ns/vector x B); 0 of 610 results are below 20 us per call. Calls are timed in segments of K = 18-32 calls, so one clock read covers at least 384 us.
- Figures: ns per vector, median of >= 9 repeats (best of repeats in brackets); ratios are medians; below 1 = faster. All programs of one binary and one n ran in one process, taking turns.
- Layouts: hyb8 / hyb16 = FFHT's structure (8- or 16-vector steps), called once per vector like FFHT; sl4 / sl8 / sl16 = straight-line: one in-register step does the whole transform, one call runs it over the batch; x86wht = x86-wht's whole transform once per vector. h20half outputs H x / 2^p (p = its 8-point steps).

## Reading per binary (best circuit / best rival at each n; the circuit in brackets)

| binary | width | n=64 | n=128 | n=256 | n=512 | n=1024 | n=4096 | library sizes 2^6-2^9 |
|---|---|---|---|---|---|---|---|---|
| gcc_avx2_f32 | 256bit-f32 | 1.008 (sl8-g19) | 1.016 (sl16-g20x2) | 1.054 (hyb8-g19) | 0.992 (hyb8-g20) | 0.996 (hyb8-g20) | 0.965 (hyb8-g20) | NO-GAIN (>= 0.95 at every n) |
| clang_avx2_f32 | 256bit-f32 | 0.988 (sl8-g20) | 1.027 (sl16-g52) | 1.035 (hyb8-g20) | 0.989 (hyb8-g20) | 0.978 (hyb8-g20) | 0.938 (hyb8-g20) | NO-GAIN (>= 0.95 at every n) |
| gcc_avx512_f32 | 512bit-f32 | no circuit layout (rival sl4-tb4) | 0.976 (sl8-g20) | **0.861** (sl16-g20x2) | 1.005 (hyb8-g20) | 0.987 (hyb8-g20) | 0.970 (hyb8-g20) | MIXED |
| clang_avx512_f32 | 512bit-f32 | no circuit layout (rival sl4-tb4) | 0.994 (sl8-g20) | 1.004 (sl16-g52) | 1.011 (hyb8-g20) | 0.983 (hyb8-g20) | 0.967 (hyb8-g20) | NO-GAIN (>= 0.95 at every n) |
| gcc_avx2_f64 | 256bit-f64 | 0.935 (sl16-g20x2) | 1.026 (hyb8-g19) | 0.979 (hyb8-g19) | 0.973 (hyb8-g19) | 0.966 (hyb8-g20) | 0.956 (hyb8-g20) | MIXED |
| clang_avx2_f64 | 256bit-f64 | 0.959 (sl16-g52) | 1.022 (hyb8-g20) | 0.970 (hyb8-g20) | 0.943 (hyb16-g52) | 0.953 (hyb8-g20) | 0.939 (hyb8-g19) | MIXED |
| gcc_avx512_f64 | 512bit-f64 | 0.958 (sl8-g20) | 0.905 (sl16-g20x2) | 1.000 (hyb8-g20) | 0.974 (hyb8-g20) | 0.955 (hyb8-g20) | 0.953 (hyb8-g20) | MIXED |
| clang_avx512_f64 | 512bit-f64 | 0.979 (sl8-g20) | 1.013 (sl16-g52) | 1.010 (hyb8-g20) | 0.998 (hyb8-g20) | 0.979 (hyb16-g52) | 0.981 (hyb16-g52) | NO-GAIN (>= 0.95 at every n) |

g20 alone (the 3/4 family's 8-point step; hyb8-g20, and sl8-g20 where n is 8 vectors), circuit / best rival:

- gcc_avx2_f32: n=64 sl8-g20 1.013; n=64 hyb8-g20 1.047; n=128 hyb8-g20 1.141; n=128 sl16-g20x2 1.016; n=256 hyb8-g20 1.059; n=512 hyb8-g20 0.992; n=1024 hyb8-g20 0.996; n=4096 hyb8-g20 0.965
- clang_avx2_f32: n=64 sl8-g20 0.988; n=64 hyb8-g20 1.025; n=128 hyb8-g20 1.220; n=128 sl16-g20x2 1.055; n=256 hyb8-g20 1.035; n=512 hyb8-g20 0.989; n=1024 hyb8-g20 0.978; n=4096 hyb8-g20 0.938
- gcc_avx512_f32: n=128 sl8-g20 0.976; n=128 hyb8-g20 1.014; n=256 sl16-g20x2 0.861; n=512 hyb8-g20 1.005; n=1024 hyb8-g20 0.987; n=4096 hyb8-g20 0.970
- clang_avx512_f32: n=128 sl8-g20 0.994; n=128 hyb8-g20 1.035; n=256 sl16-g20x2 1.024; n=512 hyb8-g20 1.011; n=1024 hyb8-g20 0.983; n=4096 hyb8-g20 0.967
- gcc_avx2_f64: n=64 hyb8-g20 1.083; n=64 sl16-g20x2 0.935; n=128 hyb8-g20 1.044; n=256 hyb8-g20 0.994; n=512 hyb8-g20 0.975; n=1024 hyb8-g20 0.966; n=4096 hyb8-g20 0.956
- clang_avx2_f64: n=64 hyb8-g20 1.217; n=64 sl16-g20x2 1.079; n=128 hyb8-g20 1.022; n=256 hyb8-g20 0.970; n=512 hyb8-g20 0.995; n=1024 hyb8-g20 0.953; n=4096 hyb8-g20 0.945
- gcc_avx512_f64: n=64 sl8-g20 0.958; n=64 hyb8-g20 1.010; n=128 hyb8-g20 1.025; n=128 sl16-g20x2 0.905; n=256 hyb8-g20 1.000; n=512 hyb8-g20 0.974; n=1024 hyb8-g20 0.955; n=4096 hyb8-g20 0.953
- clang_avx512_f64: n=64 sl8-g20 0.979; n=64 hyb8-g20 1.014; n=128 hyb8-g20 1.196; n=128 sl16-g20x2 1.064; n=256 hyb8-g20 1.010; n=512 hyb8-g20 0.998; n=1024 hyb8-g20 1.092; n=4096 hyb8-g20 1.016

## gcc_avx2_f32 (256bit-f32)

| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |
|---|---|---|---|---|---|---|---|---|
| 64 | 2048 | sl8-tb8balS 15.51 (32 us/call) | hyb8-g19 | 16.24 (16.23) | 1.047 (1.047) | 0.977 | 1.037 | yes |
| | | | hyb8-g20 | 16.23 (16.22) | 1.047 (1.047) | 0.977 | 1.037 | yes |
| | | | hyb8-h20half | 16.49 (16.48) | 1.063 (1.063) | 0.992 | 1.054 | yes |
| | | | sl8-g19 | 15.63 (15.62) | 1.008 (1.008) | 0.945 | 1.008 | yes |
| | | | sl8-g20 | 15.71 (15.70) | 1.013 (1.013) | 0.950 | 1.013 | yes |
| | | | sl8-h20half | 16.18 (16.17) | 1.043 (1.043) | 0.978 | 1.043 | yes |
| 128 | 1024 | FFHT 35.23 (36 us/call) | hyb8-g19 | 39.93 (39.91) | 1.133 (1.133) | 1.020 | 1.052 | yes |
| | | | hyb8-g20 | 40.19 (40.17) | 1.141 (1.141) | 1.026 | 1.058 | yes |
| | | | hyb8-h20half | 40.10 (40.05) | 1.138 (1.138) | 1.024 | 1.056 | yes |
| | | | sl16-g52 | 40.77 (40.75) | 1.157 (1.157) | 1.016 | 1.021 | yes |
| | | | sl16-g20x2 | 35.79 (35.77) | 1.016 (1.016) | 0.892 | 0.897 | yes |
| 256 | 512 | FFHT 77.43 (40 us/call) | hyb8-g19 | 81.63 (81.61) | 1.054 (1.055) | 1.011 | 1.046 | yes |
| | | | hyb8-g20 | 81.98 (81.96) | 1.059 (1.059) | 1.015 | 1.050 | yes |
| | | | hyb8-h20half | 82.08 (82.04) | 1.060 (1.060) | 1.017 | 1.051 | yes |
| 512 | 256 | hyb8-tb8bal 157.28 (40 us/call) | hyb8-g19 | 156.35 (156.26) | 0.994 (0.994) | 0.960 | 0.994 | yes |
| | | | hyb8-g20 | 156.04 (155.97) | 0.992 (0.992) | 0.958 | 0.992 | yes |
| | | | hyb8-h20half | 161.35 (161.31) | 1.026 (1.026) | 0.991 | 1.026 | yes |
| | | | hyb16-g52 | 187.20 (187.14) | 1.190 (1.190) | 1.034 | 1.012 | yes |
| 1024 | 128 | hyb8-tb8balS 332.77 (43 us/call) | hyb8-g19 | 332.86 (332.26) | 1.000 (0.999) | 0.936 | 1.000 | yes |
| | | | hyb8-g20 | 331.36 (331.16) | 0.996 (0.996) | 0.932 | 0.996 | yes |
| | | | hyb8-h20half | 342.45 (342.14) | 1.029 (1.029) | 0.963 | 1.029 | yes |
| | | | hyb16-g52 | 371.71 (371.39) | 1.117 (1.117) | 0.992 | 0.991 | yes |
| 4096 | 32 | hyb8-tb8balS 1368.17 (44 us/call) | hyb8-g19 | 1344.08 (1343.45) | 0.982 (0.982) | 0.888 | 0.982 | yes |
| | | | hyb8-g20 | 1320.67 (1320.03) | 0.965 (0.965) | 0.873 | 0.965 | yes |
| | | | hyb8-h20half | 1405.16 (1404.18) | 1.027 (1.027) | 0.929 | 1.027 | yes |
| | | | hyb16-g52 | 1685.37 (1684.44) | 1.232 (1.232) | 0.968 | 0.936 | yes |

Every program at each n (ns/vector, median):

- n=64: sl8-tb8balS 15.51, sl8-tb8bal 15.58, sl8-g19 15.63, hyb8-tb8balS 15.65, sl8-g20 15.71, hyb8-tb8bal 15.74, FFHT 16.06, sl8-h20half 16.18, hyb8-g20 16.23, hyb8-g19 16.24, hyb8-h20half 16.49, sl8-tb8 16.54, hyb8-tb8 16.62, x86wht-tb 20.07, x86wht-tbbal 20.66
- n=128: FFHT 35.23, sl16-g20x2 35.79, hyb8-tb8bal 37.97, hyb8-tb8balS 38.75, hyb8-tb8 39.16, sl16-tb16balS 39.91, hyb8-g19 39.93, hyb8-h20half 40.10, sl16-tb16 40.11, hyb8-g20 40.19, sl16-g52 40.77, sl16-tb16bal 41.64, x86wht-tb 44.77, x86wht-tbbal 48.56
- n=256: FFHT 77.43, hyb8-tb8balS 78.07, hyb8-tb8bal 78.50, hyb8-tb8 80.74, hyb8-g19 81.63, hyb8-g20 81.98, hyb8-h20half 82.08, x86wht-tb 97.40, x86wht-tbbal 104.46
- n=512: hyb8-g20 156.04, hyb8-g19 156.35, hyb8-tb8bal 157.28, FFHT 157.68, hyb8-tb8balS 158.44, hyb8-h20half 161.35, hyb8-tb8 162.87, hyb16-tb16 181.02, hyb16-tb16balS 184.97, hyb16-g52 187.20, x86wht-tb 190.95, hyb16-tb16bal 190.98, x86wht-tbbal 206.20
- n=1024: hyb8-g20 331.36, hyb8-tb8balS 332.77, hyb8-g19 332.86, hyb8-tb8bal 336.23, hyb8-h20half 342.45, FFHT 346.05, hyb8-tb8 355.65, hyb16-g52 371.71, hyb16-tb16 374.78, hyb16-tb16balS 375.20, hyb16-tb16bal 391.26, x86wht-tb 397.66, x86wht-tbbal 420.45
- n=4096: hyb8-g20 1320.67, hyb8-g19 1344.08, hyb8-tb8balS 1368.17, hyb8-tb8bal 1384.99, hyb8-h20half 1405.16, FFHT 1475.96, hyb8-tb8 1513.31, hyb16-g52 1685.37, hyb16-tb16 1740.34, hyb16-tb16balS 1800.03, hyb16-tb16bal 1835.12, x86wht-tb 2173.20, x86wht-tbbal 2376.33

## clang_avx2_f32 (256bit-f32)

| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |
|---|---|---|---|---|---|---|---|---|
| 64 | 2048 | sl8-tb8balS 15.23 (31 us/call) | hyb8-g19 | 15.84 (15.83) | 1.040 (1.040) | 0.968 | 1.020 | yes |
| | | | hyb8-g20 | 15.61 (15.60) | 1.025 (1.025) | 0.954 | 1.005 | yes |
| | | | hyb8-h20half | 16.69 (16.68) | 1.096 (1.096) | 1.020 | 1.075 | yes |
| | | | sl8-g19 | 15.20 (15.20) | 0.998 (0.999) | 0.923 | 0.998 | yes |
| | | | sl8-g20 | 15.05 (15.04) | 0.988 (0.988) | 0.914 | 0.988 | yes |
| | | | sl8-h20half | 16.41 (16.40) | 1.078 (1.078) | 0.997 | 1.078 | yes |
| 128 | 1024 | sl16-tb16bal 32.11 (33 us/call) | hyb8-g19 | 39.59 (39.57) | 1.233 (1.233) | 1.031 | 1.053 | yes |
| | | | hyb8-g20 | 39.17 (39.15) | 1.220 (1.220) | 1.020 | 1.042 | yes |
| | | | hyb8-h20half | 40.91 (40.88) | 1.274 (1.274) | 1.065 | 1.088 | yes |
| | | | sl16-g52 | 32.98 (32.97) | 1.027 (1.027) | 0.972 | 1.027 | yes |
| | | | sl16-g20x2 | 33.88 (33.86) | 1.055 (1.055) | 0.999 | 1.055 | yes |
| 256 | 512 | FFHT 76.40 (39 us/call) | hyb8-g19 | 80.07 (80.02) | 1.048 (1.048) | 1.018 | 1.043 | yes |
| | | | hyb8-g20 | 79.10 (79.08) | 1.035 (1.036) | 1.005 | 1.030 | yes |
| | | | hyb8-h20half | 82.75 (82.70) | 1.083 (1.083) | 1.052 | 1.078 | yes |
| 512 | 256 | hyb8-tb8balS 153.70 (39 us/call) | hyb8-g19 | 154.46 (154.39) | 1.005 (1.005) | 0.958 | 1.005 | yes |
| | | | hyb8-g20 | 152.00 (151.94) | 0.989 (0.989) | 0.942 | 0.989 | yes |
| | | | hyb8-h20half | 165.71 (165.67) | 1.078 (1.078) | 1.027 | 1.078 | yes |
| | | | hyb16-g52 | 187.15 (187.08) | 1.218 (1.218) | 1.070 | 1.035 | yes |
| 1024 | 128 | hyb8-tb8balS 328.88 (42 us/call) | hyb8-g19 | 327.91 (327.68) | 0.997 (0.997) | 0.929 | 0.997 | yes |
| | | | hyb8-g20 | 321.62 (321.50) | 0.978 (0.978) | 0.911 | 0.978 | yes |
| | | | hyb8-h20half | 350.52 (350.20) | 1.066 (1.065) | 0.993 | 1.066 | yes |
| | | | hyb16-g52 | 365.99 (365.83) | 1.113 (1.113) | 1.019 | 0.995 | yes |
| 4096 | 32 | hyb8-tb8balS 1363.68 (44 us/call) | hyb8-g19 | 1294.36 (1293.95) | 0.949 (0.950) | 0.867 | 0.949 | yes |
| | | | hyb8-g20 | 1279.26 (1278.90) | 0.938 (0.939) | 0.857 | 0.938 | yes |
| | | | hyb8-h20half | 1449.41 (1449.00) | 1.063 (1.063) | 0.971 | 1.063 | yes |
| | | | hyb16-g52 | 1726.15 (1725.09) | 1.266 (1.266) | 1.026 | 0.966 | yes |

Every program at each n (ns/vector, median):

- n=64: sl8-g20 15.05, sl8-g19 15.20, sl8-tb8balS 15.23, sl8-tb8bal 15.23, hyb8-tb8balS 15.53, hyb8-tb8bal 15.59, hyb8-g20 15.61, hyb8-g19 15.84, FFHT 15.87, hyb8-tb8 16.37, sl8-h20half 16.41, sl8-tb8 16.47, hyb8-h20half 16.69, x86wht-tb 18.04, x86wht-tbbal 18.36
- n=128: sl16-tb16bal 32.11, sl16-tb16balS 32.37, sl16-g52 32.98, sl16-g20x2 33.88, sl16-tb16 33.93, x86wht-tb 35.46, FFHT 35.93, hyb8-tb8balS 37.60, hyb8-tb8bal 37.92, x86wht-tbbal 38.28, hyb8-tb8 38.39, hyb8-g20 39.17, hyb8-g19 39.59, hyb8-h20half 40.91
- n=256: FFHT 76.40, hyb8-tb8bal 76.78, hyb8-tb8balS 76.85, hyb8-tb8 78.69, hyb8-g20 79.10, hyb8-g19 80.07, x86wht-tb 81.22, hyb8-h20half 82.75, x86wht-tbbal 85.82
- n=512: hyb8-g20 152.00, hyb8-tb8balS 153.70, hyb8-g19 154.46, hyb8-tb8bal 154.67, FFHT 158.28, x86wht-tb 160.40, hyb8-tb8 161.31, hyb8-h20half 165.71, x86wht-tbbal 170.81, hyb16-tb16 174.90, hyb16-tb16balS 180.77, hyb16-tb16bal 181.63, hyb16-g52 187.15
- n=1024: hyb8-g20 321.62, hyb8-g19 327.91, hyb8-tb8balS 328.88, hyb8-tb8bal 332.49, x86wht-tb 336.61, hyb8-h20half 350.52, FFHT 352.90, hyb8-tb8 353.01, x86wht-tbbal 354.11, hyb16-tb16 359.20, hyb16-g52 365.99, hyb16-tb16balS 367.92, hyb16-tb16bal 370.44
- n=4096: hyb8-g20 1279.26, hyb8-g19 1294.36, hyb8-tb8balS 1363.68, hyb8-tb8bal 1366.88, hyb8-h20half 1449.41, FFHT 1473.83, hyb8-tb8 1492.40, x86wht-tb 1578.89, hyb16-tb16 1681.91, x86wht-tbbal 1705.46, hyb16-g52 1726.15, hyb16-tb16balS 1787.27, hyb16-tb16bal 1812.50

## gcc_avx512_f32 (512bit-f32)

| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |
|---|---|---|---|---|---|---|---|---|
| 64 | 2048 | sl4-tb4 14.91 (31 us/call) | (no circuit layout at this n) | | | | | yes |
| 128 | 1024 | sl8-tb8bal 29.81 (31 us/call) | hyb8-g19 | 30.84 (30.83) | 1.035 (1.035) | 0.911 | 1.006 | yes |
| | | | hyb8-g20 | 30.22 (30.20) | 1.014 (1.014) | 0.892 | 0.985 | yes |
| | | | hyb8-h20half | 32.18 (32.17) | 1.080 (1.080) | 0.950 | 1.049 | yes |
| | | | sl8-g19 | 29.52 (29.51) | 0.990 (0.990) | 0.906 | 0.990 | yes |
| | | | sl8-g20 | 29.08 (29.07) | 0.976 (0.976) | 0.893 | 0.976 | yes |
| | | | sl8-h20half | 30.81 (30.80) | 1.034 (1.034) | 0.946 | 1.034 | yes |
| 256 | 512 | FFHT 76.22 (39 us/call) | sl16-g52 | 79.89 (79.86) | 1.048 (1.049) | 1.028 | 1.030 | yes |
| | | | sl16-g20x2 | 65.66 (65.64) | **0.861 (0.862)** | 0.844 | 0.846 | yes |
| 512 | 256 | hyb8-tb8bal 149.35 (38 us/call) | hyb8-g19 | 152.16 (152.00) | 1.019 (1.018) | 0.961 | 1.019 | yes |
| | | | hyb8-g20 | 150.12 (149.99) | 1.005 (1.005) | 0.948 | 1.005 | yes |
| | | | hyb8-h20half | 156.31 (156.21) | 1.047 (1.046) | 0.987 | 1.047 | yes |
| | | | hyb16-g52 | 186.62 (186.52) | 1.250 (1.249) | 0.953 | 1.015 | yes |
| 1024 | 128 | hyb8-tb8bal 297.45 (38 us/call) | hyb8-g19 | 300.53 (300.35) | 1.010 (1.011) | 0.940 | 1.010 | yes |
| | | | hyb8-g20 | 293.60 (293.46) | 0.987 (0.987) | 0.919 | 0.987 | yes |
| | | | hyb8-h20half | 304.74 (304.56) | 1.025 (1.025) | 0.954 | 1.025 | yes |
| | | | hyb16-g52 | 364.27 (363.91) | 1.225 (1.224) | 0.971 | 1.012 | yes |
| 4096 | 32 | hyb8-tb8balS 1315.16 (42 us/call) | hyb8-g19 | 1301.17 (1300.67) | 0.989 (0.990) | 0.914 | 0.989 | yes |
| | | | hyb8-g20 | 1276.35 (1275.61) | 0.970 (0.970) | 0.897 | 0.970 | yes |
| | | | hyb8-h20half | 1331.41 (1330.70) | 1.012 (1.012) | 0.935 | 1.012 | yes |
| | | | hyb16-g52 | 1471.42 (1471.01) | 1.119 (1.119) | 0.909 | 0.999 | yes |

Every program at each n (ns/vector, median):

- n=64: sl4-tb4 14.91, hyb8-tb8 15.78, FFHT 15.79, x86wht-tbbal 21.00, x86wht-tb 21.58
- n=128: sl8-g20 29.08, sl8-g19 29.52, sl8-tb8bal 29.81, sl8-tb8balS 30.14, hyb8-g20 30.22, hyb8-tb8bal 30.67, sl8-h20half 30.81, hyb8-g19 30.84, hyb8-tb8balS 30.86, hyb8-h20half 32.18, sl8-tb8 32.59, hyb8-tb8 33.86, FFHT 35.26, x86wht-tb 36.72, x86wht-tbbal 37.02
- n=256: sl16-g20x2 65.66, FFHT 76.22, sl16-tb16bal 77.57, sl16-tb16 77.75, sl16-tb16balS 77.81, sl16-g52 79.89, hyb8-tb8 84.15, x86wht-tb 96.33, x86wht-tbbal 97.70
- n=512: hyb8-tb8bal 149.35, hyb8-tb8balS 149.75, hyb8-g20 150.12, hyb8-g19 152.16, hyb8-h20half 156.31, FFHT 157.53, hyb8-tb8 158.36, hyb16-tb16bal 183.95, hyb16-tb16balS 184.26, hyb16-g52 186.62, hyb16-tb16 195.79, x86wht-tbbal 206.32, x86wht-tb 207.22
- n=1024: hyb8-g20 293.60, hyb8-tb8bal 297.45, hyb8-tb8balS 299.23, hyb8-g19 300.53, hyb8-h20half 304.74, hyb8-tb8 319.58, FFHT 344.50, hyb16-tb16balS 359.98, hyb16-tb16bal 360.41, hyb16-g52 364.27, hyb16-tb16 375.08, x86wht-tbbal 407.91, x86wht-tb 416.21
- n=4096: hyb8-g20 1276.35, hyb8-g19 1301.17, hyb8-tb8balS 1315.16, hyb8-tb8bal 1315.23, hyb8-h20half 1331.41, hyb8-tb8 1423.64, hyb16-g52 1471.42, hyb16-tb16bal 1473.55, FFHT 1474.91, hyb16-tb16balS 1492.98, hyb16-tb16 1619.20, x86wht-tbbal 2029.96, x86wht-tb 2113.28

## clang_avx512_f32 (512bit-f32)

| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |
|---|---|---|---|---|---|---|---|---|
| 64 | 2048 | sl4-tb4 13.60 (28 us/call) | (no circuit layout at this n) | | | | | yes |
| 128 | 1024 | sl8-tb8balS 27.93 (29 us/call) | hyb8-g19 | 29.08 (29.08) | 1.041 (1.042) | 0.967 | 1.010 | yes |
| | | | hyb8-g20 | 28.90 (28.87) | 1.035 (1.035) | 0.961 | 1.004 | yes |
| | | | hyb8-h20half | 29.79 (29.79) | 1.067 (1.067) | 0.991 | 1.035 | yes |
| | | | sl8-g19 | 27.97 (27.93) | 1.001 (1.001) | 0.958 | 1.001 | yes |
| | | | sl8-g20 | 27.75 (27.73) | 0.994 (0.994) | 0.950 | 0.994 | yes |
| | | | sl8-h20half | 28.67 (28.63) | 1.026 (1.026) | 0.982 | 1.026 | yes |
| 256 | 512 | sl16-tb16bal 57.62 (30 us/call) | sl16-g52 | 57.85 (57.81) | 1.004 (1.005) | 0.917 | 1.004 | yes |
| | | | sl16-g20x2 | 59.03 (58.84) | 1.024 (1.023) | 0.936 | 1.024 | yes |
| 512 | 256 | hyb8-tb8bal 135.70 (35 us/call) | hyb8-g19 | 141.06 (140.96) | 1.039 (1.040) | 1.010 | 1.039 | yes |
| | | | hyb8-g20 | 137.23 (137.09) | 1.011 (1.011) | 0.983 | 1.011 | yes |
| | | | hyb8-h20half | 142.61 (142.54) | 1.051 (1.051) | 1.021 | 1.051 | yes |
| | | | hyb16-g52 | 183.05 (182.98) | 1.349 (1.350) | 1.018 | 1.044 | yes |
| 1024 | 128 | hyb8-tb8bal 278.49 (36 us/call) | hyb8-g19 | 279.32 (279.14) | 1.003 (1.003) | 0.961 | 1.003 | yes |
| | | | hyb8-g20 | 273.77 (273.54) | 0.983 (0.983) | 0.942 | 0.983 | yes |
| | | | hyb8-h20half | 286.62 (286.45) | 1.029 (1.029) | 0.986 | 1.029 | yes |
| | | | hyb16-g52 | 358.45 (358.19) | 1.287 (1.287) | 1.004 | 1.043 | yes |
| 4096 | 32 | hyb8-tb8bal 1260.02 (40 us/call) | hyb8-g19 | 1225.16 (1224.30) | 0.972 (0.974) | 0.934 | 0.972 | yes |
| | | | hyb8-g20 | 1219.03 (1216.10) | 0.967 (0.967) | 0.929 | 0.967 | yes |
| | | | hyb8-h20half | 1267.42 (1266.67) | 1.006 (1.007) | 0.966 | 1.006 | yes |
| | | | hyb16-g52 | 1479.36 (1479.09) | 1.174 (1.176) | 0.958 | 0.995 | yes |

Every program at each n (ns/vector, median):

- n=64: sl4-tb4 13.60, hyb8-tb8 14.33, FFHT 15.88, x86wht-tbbal 18.25, x86wht-tb 18.36
- n=128: sl8-g20 27.75, sl8-tb8balS 27.93, sl8-g19 27.97, sl8-tb8bal 28.11, sl8-h20half 28.67, hyb8-tb8bal 28.78, hyb8-tb8balS 28.84, hyb8-g20 28.90, hyb8-g19 29.08, sl8-tb8 29.20, hyb8-h20half 29.79, hyb8-tb8 30.07, x86wht-tbbal 31.41, x86wht-tb 31.93, FFHT 35.52
- n=256: sl16-tb16bal 57.62, sl16-tb16balS 57.82, sl16-g52 57.85, sl16-g20x2 59.03, sl16-tb16 63.07, x86wht-tbbal 66.57, x86wht-tb 68.35, hyb8-tb8 71.12, FFHT 76.57
- n=512: hyb8-tb8bal 135.70, hyb8-tb8balS 137.05, hyb8-g20 137.23, hyb8-tb8 139.66, hyb8-g19 141.06, hyb8-h20half 142.61, x86wht-tbbal 154.13, x86wht-tb 157.49, FFHT 158.22, hyb16-tb16bal 175.25, hyb16-tb16balS 175.99, hyb16-tb16 179.82, hyb16-g52 183.05
- n=1024: hyb8-g20 273.77, hyb8-tb8bal 278.49, hyb8-g19 279.32, hyb8-tb8balS 280.30, hyb8-h20half 286.62, hyb8-tb8 290.57, x86wht-tbbal 307.87, x86wht-tb 311.65, hyb16-tb16bal 343.53, hyb16-tb16balS 349.84, FFHT 352.75, hyb16-tb16 356.95, hyb16-g52 358.45
- n=4096: hyb8-g20 1219.03, hyb8-g19 1225.16, hyb8-tb8bal 1260.02, hyb8-h20half 1267.42, hyb8-tb8balS 1273.22, hyb8-tb8 1311.61, x86wht-tbbal 1321.95, x86wht-tb 1400.52, FFHT 1473.85, hyb16-g52 1479.36, hyb16-tb16bal 1487.08, hyb16-tb16balS 1502.28, hyb16-tb16 1543.49

## gcc_avx2_f64 (256bit-f64)

| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |
|---|---|---|---|---|---|---|---|---|
| 64 | 1024 | FFHT 26.34 (27 us/call) | hyb8-g19 | 28.40 (28.35) | 1.078 (1.077) | 0.998 | 1.031 | yes |
| | | | hyb8-g20 | 28.51 (28.48) | 1.083 (1.082) | 1.002 | 1.035 | yes |
| | | | hyb8-h20half | 29.12 (29.08) | 1.106 (1.105) | 1.023 | 1.057 | yes |
| | | | sl16-g52 | 29.12 (29.08) | 1.106 (1.105) | 1.028 | 1.029 | yes |
| | | | sl16-g20x2 | 24.62 (24.60) | 0.935 (0.935) | 0.870 | 0.870 | yes |
| 128 | 512 | hyb8-tb8balS 55.74 (29 us/call) | hyb8-g19 | 57.21 (57.14) | 1.026 (1.026) | 0.959 | 1.026 | yes |
| | | | hyb8-g20 | 58.18 (58.13) | 1.044 (1.044) | 0.976 | 1.044 | yes |
| | | | hyb8-h20half | 59.33 (59.30) | 1.064 (1.065) | 0.995 | 1.064 | yes |
| | | | hyb16-g52 | 72.81 (72.75) | 1.306 (1.306) | 1.063 | 1.026 | yes |
| 256 | 256 | hyb8-tb8balS 114.11 (29 us/call) | hyb8-g19 | 111.67 (111.61) | 0.979 (0.980) | 0.916 | 0.979 | yes |
| | | | hyb8-g20 | 113.43 (113.35) | 0.994 (0.995) | 0.930 | 0.994 | yes |
| | | | hyb8-h20half | 117.16 (117.09) | 1.027 (1.028) | 0.961 | 1.027 | yes |
| | | | hyb16-g52 | 142.85 (142.77) | 1.252 (1.253) | 1.047 | 1.030 | yes |
| 512 | 128 | hyb8-tb8balS 250.83 (32 us/call) | hyb8-g19 | 244.07 (243.99) | 0.973 (0.974) | 0.888 | 0.973 | yes |
| | | | hyb8-g20 | 244.46 (244.32) | 0.975 (0.975) | 0.889 | 0.975 | yes |
| | | | hyb8-h20half | 252.14 (251.96) | 1.005 (1.006) | 0.917 | 1.005 | yes |
| | | | hyb16-g52 | 279.50 (279.39) | 1.114 (1.115) | 0.977 | 0.989 | yes |
| 1024 | 64 | hyb8-tb8balS 508.24 (33 us/call) | hyb8-g19 | 492.57 (491.96) | 0.969 (0.969) | 0.879 | 0.969 | yes |
| | | | hyb8-g20 | 491.05 (490.63) | 0.966 (0.967) | 0.876 | 0.966 | yes |
| | | | hyb8-h20half | 515.04 (514.90) | 1.013 (1.014) | 0.919 | 1.013 | yes |
| | | | hyb16-g52 | 579.50 (579.19) | 1.140 (1.141) | 0.938 | 0.902 | yes |
| 4096 | 16 | hyb8-tb8balS 2399.15 (38 us/call) | hyb8-g19 | 2301.05 (2300.12) | 0.959 (0.959) | 0.854 | 0.959 | yes |
| | | | hyb8-g20 | 2293.23 (2291.60) | 0.956 (0.956) | 0.851 | 0.956 | yes |
| | | | hyb8-h20half | 2404.21 (2402.28) | 1.002 (1.002) | 0.892 | 1.002 | yes |
| | | | hyb16-g52 | 2933.31 (2930.96) | 1.223 (1.222) | 0.960 | 0.925 | yes |

Every program at each n (ns/vector, median):

- n=64: sl16-g20x2 24.62, FFHT 26.34, hyb8-tb8balS 27.55, hyb8-tb8bal 27.65, sl16-tb16balS 28.31, sl16-tb16 28.32, hyb8-g19 28.40, hyb8-tb8 28.47, hyb8-g20 28.51, sl16-g52 29.12, hyb8-h20half 29.12, sl16-tb16bal 30.11, x86wht-tb 38.00, x86wht-tbbal 41.08
- n=128: hyb8-tb8balS 55.74, hyb8-tb8bal 56.25, hyb8-g19 57.21, FFHT 57.47, hyb8-g20 58.18, hyb8-h20half 59.33, hyb8-tb8 59.63, hyb16-tb16 68.48, hyb16-tb16balS 70.95, hyb16-g52 72.81, hyb16-tb16bal 74.57, x86wht-tb 82.38, x86wht-tbbal 88.83
- n=256: hyb8-g19 111.67, hyb8-g20 113.43, hyb8-tb8balS 114.11, hyb8-tb8bal 115.62, hyb8-h20half 117.16, FFHT 121.95, hyb8-tb8 121.97, hyb16-tb16 136.50, hyb16-tb16balS 138.67, hyb16-g52 142.85, hyb16-tb16bal 146.48, x86wht-tb 161.34, x86wht-tbbal 176.14
- n=512: hyb8-g19 244.07, hyb8-g20 244.46, hyb8-tb8balS 250.83, hyb8-h20half 252.14, hyb8-tb8bal 253.51, FFHT 270.33, hyb8-tb8 274.90, hyb16-g52 279.50, hyb16-tb16balS 282.60, hyb16-tb16 285.98, hyb16-tb16bal 298.05, x86wht-tb 337.05, x86wht-tbbal 361.82
- n=1024: hyb8-g20 491.05, hyb8-g19 492.57, hyb8-tb8balS 508.24, hyb8-tb8bal 512.43, hyb8-h20half 515.04, FFHT 554.91, hyb8-tb8 560.44, hyb16-g52 579.50, hyb16-tb16 617.59, hyb16-tb16balS 642.77, hyb16-tb16bal 662.82, x86wht-tb 888.69, x86wht-tbbal 980.00
- n=4096: hyb8-g20 2293.23, hyb8-g19 2301.05, hyb8-tb8balS 2399.15, hyb8-h20half 2404.21, hyb8-tb8bal 2448.35, FFHT 2639.78, hyb8-tb8 2694.30, hyb16-g52 2933.31, hyb16-tb16 3055.72, hyb16-tb16balS 3172.59, hyb16-tb16bal 3481.17, x86wht-tb 3904.41, x86wht-tbbal 4267.78

## clang_avx2_f64 (256bit-f64)

| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |
|---|---|---|---|---|---|---|---|---|
| 64 | 1024 | sl16-tb16bal 24.25 (25 us/call) | hyb8-g19 | 29.34 (29.32) | 1.210 (1.210) | 0.992 | 1.033 | yes |
| | | | hyb8-g20 | 29.50 (29.48) | 1.217 (1.216) | 0.998 | 1.039 | yes |
| | | | hyb8-h20half | 31.07 (31.06) | 1.281 (1.281) | 1.051 | 1.094 | yes |
| | | | sl16-g52 | 23.25 (23.24) | 0.959 (0.959) | 0.901 | 0.959 | yes |
| | | | sl16-g20x2 | 26.17 (26.17) | 1.079 (1.080) | 1.014 | 1.079 | yes |
| 128 | 512 | hyb8-tb8balS 56.73 (29 us/call) | hyb8-g19 | 58.53 (58.48) | 1.032 (1.031) | 0.978 | 1.032 | yes |
| | | | hyb8-g20 | 57.98 (57.94) | 1.022 (1.022) | 0.969 | 1.022 | yes |
| | | | hyb8-h20half | 61.48 (61.42) | 1.084 (1.083) | 1.027 | 1.084 | yes |
| | | | hyb16-g52 | 59.44 (59.38) | 1.048 (1.047) | 0.996 | 0.985 | yes |
| 256 | 256 | hyb8-tb8balS 116.89 (30 us/call) | hyb8-g19 | 116.78 (116.71) | 0.999 (1.000) | 0.954 | 0.999 | yes |
| | | | hyb8-g20 | 113.34 (113.31) | 0.970 (0.971) | 0.926 | 0.970 | yes |
| | | | hyb8-h20half | 123.84 (123.77) | 1.060 (1.060) | 1.012 | 1.060 | yes |
| | | | hyb16-g52 | 118.19 (118.14) | 1.011 (1.012) | 0.969 | 0.994 | yes |
| 512 | 128 | hyb16-tb16bal 247.51 (32 us/call) | hyb8-g19 | 249.06 (248.93) | 1.006 (1.006) | 0.902 | 0.973 | yes |
| | | | hyb8-g20 | 246.26 (246.13) | 0.995 (0.995) | 0.892 | 0.962 | yes |
| | | | hyb8-h20half | 267.15 (266.93) | 1.079 (1.079) | 0.968 | 1.044 | yes |
| | | | hyb16-g52 | 233.36 (233.28) | 0.943 (0.943) | 0.895 | 0.943 | yes |
| 1024 | 64 | hyb8-tb8balS 515.83 (33 us/call) | hyb8-g19 | 497.81 (497.47) | 0.965 (0.965) | 0.891 | 0.965 | yes |
| | | | hyb8-g20 | 491.81 (491.56) | 0.953 (0.953) | 0.880 | 0.953 | yes |
| | | | hyb8-h20half | 537.53 (537.07) | 1.042 (1.042) | 0.962 | 1.042 | yes |
| | | | hyb16-g52 | 519.34 (519.10) | 1.007 (1.007) | 0.902 | 0.906 | yes |
| 4096 | 16 | hyb8-tb8balS 2463.94 (39 us/call) | hyb8-g19 | 2312.71 (2312.19) | 0.939 (0.939) | 0.858 | 0.939 | yes |
| | | | hyb8-g20 | 2328.87 (2326.47) | 0.945 (0.945) | 0.864 | 0.945 | yes |
| | | | hyb8-h20half | 2546.92 (2546.13) | 1.034 (1.034) | 0.945 | 1.034 | yes |
| | | | hyb16-g52 | 2674.00 (2673.27) | 1.085 (1.086) | 0.928 | 0.916 | yes |

Every program at each n (ns/vector, median):

- n=64: sl16-g52 23.25, sl16-tb16bal 24.25, sl16-tb16balS 24.93, sl16-tb16 25.80, sl16-g20x2 26.17, FFHT 26.30, hyb8-tb8bal 28.40, x86wht-tb 28.41, hyb8-tb8balS 28.53, hyb8-g19 29.34, hyb8-g20 29.50, hyb8-tb8 29.57, x86wht-tbbal 30.91, hyb8-h20half 31.07
- n=128: hyb8-tb8balS 56.73, hyb8-tb8bal 56.90, hyb8-g20 57.98, FFHT 58.19, hyb8-g19 58.53, hyb16-g52 59.44, hyb16-tb16 59.67, hyb8-tb8 59.85, hyb16-tb16bal 60.33, hyb8-h20half 61.48, hyb16-tb16balS 61.55, x86wht-tb 64.61, x86wht-tbbal 70.98
- n=256: hyb8-g20 113.34, hyb8-g19 116.78, hyb8-tb8balS 116.89, hyb16-g52 118.19, hyb8-tb8bal 118.51, hyb16-tb16bal 118.91, FFHT 121.05, hyb16-tb16 122.00, hyb8-tb8 122.41, hyb16-tb16balS 123.22, hyb8-h20half 123.84, x86wht-tb 127.99, x86wht-tbbal 138.96
- n=512: hyb16-g52 233.36, hyb8-g20 246.26, hyb16-tb16bal 247.51, hyb8-g19 249.06, hyb16-tb16balS 255.66, hyb8-tb8balS 255.92, hyb8-tb8bal 257.44, hyb16-tb16 260.81, hyb8-h20half 267.15, x86wht-tb 272.11, FFHT 275.98, hyb8-tb8 276.06, x86wht-tbbal 289.99
- n=1024: hyb8-g20 491.81, hyb8-g19 497.81, hyb8-tb8balS 515.83, hyb16-g52 519.34, hyb8-tb8bal 533.99, hyb8-h20half 537.53, FFHT 553.67, hyb8-tb8 558.76, hyb16-tb16bal 573.09, hyb16-tb16 575.52, hyb16-tb16balS 585.87, x86wht-tb 597.19, x86wht-tbbal 652.71
- n=4096: hyb8-g19 2312.71, hyb8-g20 2328.87, hyb8-tb8balS 2463.94, hyb8-tb8bal 2497.57, hyb8-h20half 2546.92, x86wht-tb 2651.01, FFHT 2655.22, hyb16-g52 2674.00, hyb8-tb8 2694.70, hyb16-tb16 2881.35, hyb16-tb16bal 2919.89, x86wht-tbbal 2936.73, hyb16-tb16balS 2965.75

## gcc_avx512_f64 (512bit-f64)

| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |
|---|---|---|---|---|---|---|---|---|
| 64 | 1024 | sl8-tb8balS 21.78 (22 us/call) | hyb8-g19 | 22.20 (22.19) | 1.019 (1.019) | 0.875 | 0.970 | yes |
| | | | hyb8-g20 | 21.98 (21.98) | 1.010 (1.010) | 0.867 | 0.961 | yes |
| | | | hyb8-h20half | 23.88 (23.87) | 1.096 (1.097) | 0.941 | 1.043 | yes |
| | | | sl8-g19 | 20.97 (20.96) | 0.963 (0.963) | 0.855 | 0.963 | yes |
| | | | sl8-g20 | 20.86 (20.85) | 0.958 (0.958) | 0.850 | 0.958 | yes |
| | | | sl8-h20half | 22.49 (22.48) | 1.033 (1.033) | 0.917 | 1.033 | yes |
| 128 | 512 | hyb8-tb8bal 53.96 (28 us/call) | hyb8-g19 | 55.99 (55.96) | 1.038 (1.038) | 0.976 | 1.038 | yes |
| | | | hyb8-g20 | 55.29 (55.27) | 1.025 (1.025) | 0.964 | 1.025 | yes |
| | | | hyb8-h20half | 56.38 (56.36) | 1.045 (1.045) | 0.983 | 1.045 | yes |
| | | | sl16-g52 | 63.98 (63.94) | 1.186 (1.186) | 0.985 | 1.056 | yes |
| | | | sl16-g20x2 | 48.83 (48.82) | 0.905 (0.905) | 0.751 | 0.806 | yes |
| 256 | 256 | hyb8-tb8balS 115.93 (30 us/call) | hyb8-g19 | 117.43 (117.38) | 1.013 (1.013) | 0.936 | 1.013 | yes |
| | | | hyb8-g20 | 115.96 (115.92) | 1.000 (1.001) | 0.924 | 1.000 | yes |
| | | | hyb8-h20half | 120.19 (120.16) | 1.037 (1.037) | 0.958 | 1.037 | yes |
| | | | hyb16-g52 | 155.63 (155.56) | 1.342 (1.343) | 1.028 | 1.042 | yes |
| 512 | 128 | hyb8-tb8balS 231.38 (30 us/call) | hyb8-g19 | 229.78 (229.68) | 0.993 (0.993) | 0.902 | 0.993 | yes |
| | | | hyb8-g20 | 225.35 (225.23) | 0.974 (0.974) | 0.884 | 0.974 | yes |
| | | | hyb8-h20half | 235.85 (235.75) | 1.019 (1.019) | 0.926 | 1.019 | yes |
| | | | hyb16-g52 | 303.64 (303.50) | 1.312 (1.312) | 1.025 | 1.042 | yes |
| 1024 | 64 | hyb8-tb8balS 534.00 (34 us/call) | hyb8-g19 | 516.10 (515.96) | 0.966 (0.967) | 0.875 | 0.966 | yes |
| | | | hyb8-g20 | 510.14 (509.94) | 0.955 (0.956) | 0.864 | 0.955 | yes |
| | | | hyb8-h20half | 537.26 (536.97) | 1.006 (1.006) | 0.910 | 1.006 | yes |
| | | | hyb16-g52 | 615.79 (615.57) | 1.153 (1.153) | 1.002 | 1.030 | yes |
| 4096 | 16 | hyb8-tb8balS 2435.36 (39 us/call) | hyb8-g19 | 2349.34 (2348.55) | 0.965 (0.965) | 0.886 | 0.965 | yes |
| | | | hyb8-g20 | 2322.03 (2319.23) | 0.953 (0.953) | 0.876 | 0.953 | yes |
| | | | hyb8-h20half | 2433.89 (2432.93) | 0.999 (0.999) | 0.918 | 0.999 | yes |
| | | | hyb16-g52 | 2878.01 (2876.15) | 1.182 (1.181) | 0.982 | 1.049 | yes |

Every program at each n (ns/vector, median):

- n=64: sl8-g20 20.86, sl8-g19 20.97, sl8-tb8balS 21.78, sl8-tb8bal 21.82, hyb8-g20 21.98, hyb8-g19 22.20, sl8-h20half 22.49, hyb8-tb8balS 22.89, hyb8-tb8bal 22.94, hyb8-h20half 23.88, sl8-tb8 24.53, hyb8-tb8 25.37, FFHT 26.53, x86wht-tb 31.21, x86wht-tbbal 31.53
- n=128: sl16-g20x2 48.83, hyb8-tb8bal 53.96, hyb8-tb8balS 53.97, hyb8-g20 55.29, hyb8-g19 55.99, hyb8-h20half 56.38, hyb8-tb8 57.36, FFHT 57.67, sl16-tb16balS 60.59, sl16-tb16bal 61.07, sl16-g52 63.98, sl16-tb16 64.98, x86wht-tb 80.18, x86wht-tbbal 82.97
- n=256: hyb8-tb8balS 115.93, hyb8-g20 115.96, hyb8-tb8bal 116.77, hyb8-g19 117.43, hyb8-h20half 120.19, FFHT 121.96, hyb8-tb8 125.45, hyb16-tb16bal 149.41, hyb16-tb16 151.32, hyb16-tb16balS 152.03, hyb16-g52 155.63, x86wht-tb 176.17, x86wht-tbbal 176.23
- n=512: hyb8-g20 225.35, hyb8-g19 229.78, hyb8-tb8balS 231.38, hyb8-tb8bal 232.30, hyb8-h20half 235.85, hyb8-tb8 254.82, FFHT 269.63, hyb16-tb16bal 291.35, hyb16-tb16balS 294.75, hyb16-tb16 296.29, hyb16-g52 303.64, x86wht-tbbal 347.71, x86wht-tb 353.10
- n=1024: hyb8-g20 510.14, hyb8-g19 516.10, hyb8-tb8balS 534.00, hyb8-tb8bal 536.78, hyb8-h20half 537.26, FFHT 553.36, hyb8-tb8 590.11, hyb16-tb16balS 597.95, hyb16-tb16bal 602.10, hyb16-tb16 614.47, hyb16-g52 615.79, x86wht-tbbal 707.48, x86wht-tb 722.38
- n=4096: hyb8-g20 2322.03, hyb8-g19 2349.34, hyb8-h20half 2433.89, hyb8-tb8balS 2435.36, hyb8-tb8bal 2444.85, FFHT 2639.69, hyb8-tb8 2650.25, hyb16-tb16bal 2744.83, hyb16-tb16balS 2793.51, hyb16-g52 2878.01, hyb16-tb16 2930.50, x86wht-tbbal 3902.03, x86wht-tb 4049.53

## clang_avx512_f64 (512bit-f64)

| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |
|---|---|---|---|---|---|---|---|---|
| 64 | 1024 | sl8-tb8balS 21.46 (22 us/call) | hyb8-g19 | 21.94 (21.92) | 1.022 (1.023) | 0.929 | 1.004 | yes |
| | | | hyb8-g20 | 21.76 (21.75) | 1.014 (1.015) | 0.921 | 0.996 | yes |
| | | | hyb8-h20half | 23.22 (23.21) | 1.082 (1.083) | 0.983 | 1.063 | yes |
| | | | sl8-g19 | 21.40 (21.38) | 0.997 (0.998) | 0.929 | 0.997 | yes |
| | | | sl8-g20 | 21.02 (20.99) | 0.979 (0.979) | 0.913 | 0.979 | yes |
| | | | sl8-h20half | 22.55 (22.55) | 1.051 (1.052) | 0.980 | 1.051 | yes |
| 128 | 512 | sl16-tb16bal 44.73 (23 us/call) | hyb8-g19 | 54.65 (54.58) | 1.222 (1.224) | 1.018 | 1.063 | yes |
| | | | hyb8-g20 | 53.49 (53.30) | 1.196 (1.196) | 0.996 | 1.040 | yes |
| | | | hyb8-h20half | 54.77 (54.68) | 1.224 (1.227) | 1.020 | 1.065 | yes |
| | | | sl16-g52 | 45.32 (45.26) | 1.013 (1.015) | 0.888 | 1.013 | yes |
| | | | sl16-g20x2 | 47.60 (47.57) | 1.064 (1.067) | 0.933 | 1.064 | yes |
| 256 | 256 | hyb8-tb8bal 109.24 (28 us/call) | hyb8-g19 | 112.45 (112.40) | 1.029 (1.029) | 0.991 | 1.029 | yes |
| | | | hyb8-g20 | 110.29 (110.26) | 1.010 (1.010) | 0.972 | 1.010 | yes |
| | | | hyb8-h20half | 115.87 (115.85) | 1.061 (1.061) | 1.021 | 1.061 | yes |
| | | | hyb16-g52 | 117.56 (117.51) | 1.076 (1.076) | 0.937 | 1.033 | yes |
| 512 | 128 | hyb16-tb16bal 221.06 (28 us/call) | hyb8-g19 | 225.94 (225.65) | 1.022 (1.021) | 0.937 | 0.996 | yes |
| | | | hyb8-g20 | 220.66 (220.56) | 0.998 (0.998) | 0.915 | 0.973 | yes |
| | | | hyb8-h20half | 238.22 (238.07) | 1.078 (1.077) | 0.988 | 1.051 | yes |
| | | | hyb16-g52 | 227.18 (227.10) | 1.028 (1.028) | 0.926 | 1.028 | yes |
| 1024 | 64 | hyb16-tb16bal 466.85 (30 us/call) | hyb8-g19 | 514.53 (514.21) | 1.102 (1.102) | 0.919 | 0.970 | yes |
| | | | hyb8-g20 | 509.60 (509.16) | 1.092 (1.091) | 0.910 | 0.961 | yes |
| | | | hyb8-h20half | 543.58 (543.38) | 1.164 (1.164) | 0.971 | 1.025 | yes |
| | | | hyb16-g52 | 456.86 (456.65) | 0.979 (0.979) | 0.869 | 0.979 | yes |
| 4096 | 16 | hyb16-tb16balS 2299.74 (37 us/call) | hyb8-g19 | 2326.08 (2323.35) | 1.011 (1.011) | 0.915 | 0.959 | yes |
| | | | hyb8-g20 | 2337.13 (2335.17) | 1.016 (1.017) | 0.919 | 0.964 | yes |
| | | | hyb8-h20half | 2489.96 (2488.04) | 1.083 (1.083) | 0.979 | 1.027 | yes |
| | | | hyb16-g52 | 2256.03 (2253.13) | 0.981 (0.981) | 0.877 | 0.981 | yes |

Every program at each n (ns/vector, median):

- n=64: sl8-g20 21.02, sl8-g19 21.40, sl8-tb8balS 21.46, sl8-tb8bal 21.52, hyb8-g20 21.76, hyb8-tb8bal 21.85, hyb8-g19 21.94, hyb8-tb8balS 22.22, sl8-h20half 22.55, sl8-tb8 23.03, hyb8-h20half 23.22, hyb8-tb8 23.62, x86wht-tbbal 25.50, x86wht-tb 25.85, FFHT 26.94
- n=128: sl16-tb16bal 44.73, sl16-tb16balS 44.76, sl16-g52 45.32, sl16-g20x2 47.60, sl16-tb16 51.04, hyb8-tb8bal 51.42, hyb8-tb8balS 51.66, x86wht-tbbal 51.68, hyb8-g20 53.49, hyb8-tb8 53.69, x86wht-tb 54.28, hyb8-g19 54.65, hyb8-h20half 54.77, FFHT 57.69
- n=256: hyb8-tb8bal 109.24, hyb8-tb8balS 109.39, hyb8-g20 110.29, hyb8-g19 112.45, hyb8-tb8 113.51, hyb16-tb16bal 113.77, hyb16-tb16balS 114.53, hyb8-h20half 115.87, hyb16-g52 117.56, FFHT 121.31, hyb16-tb16 125.52, x86wht-tbbal 125.81, x86wht-tb 135.17
- n=512: hyb8-g20 220.66, hyb16-tb16bal 221.06, hyb16-tb16balS 221.68, hyb8-g19 225.94, hyb8-tb8bal 226.73, hyb16-g52 227.18, hyb8-tb8balS 228.75, hyb8-h20half 238.22, hyb8-tb8 241.20, hyb16-tb16 245.44, x86wht-tbbal 255.91, x86wht-tb 262.61, FFHT 278.96
- n=1024: hyb16-g52 456.86, hyb16-tb16bal 466.85, hyb16-tb16balS 477.09, hyb8-g20 509.60, hyb8-g19 514.53, hyb16-tb16 525.93, hyb8-tb8bal 530.40, hyb8-tb8balS 536.66, x86wht-tbbal 543.16, hyb8-h20half 543.58, FFHT 553.83, x86wht-tb 558.68, hyb8-tb8 559.82
- n=4096: hyb16-g52 2256.03, hyb16-tb16balS 2299.74, hyb8-g19 2326.08, hyb8-g20 2337.13, hyb16-tb16bal 2338.48, hyb8-tb8bal 2424.60, hyb8-tb8balS 2455.00, hyb8-h20half 2489.96, hyb8-tb8 2542.84, x86wht-tbbal 2551.02, hyb16-tb16 2573.81, FFHT 2644.16, x86wht-tb 2728.77

## Fastest code on this machine per precision and n (across binaries: SEPARATE processes, minutes apart)

| precision | n | fastest rival (binary, program, ns/vector) | fastest circuit (binary, program, ns/vector) | circuit / rival |
|---|---|---|---|---|
| f32 | 64 | clang_avx512_f32 sl4-tb4 13.60 | clang_avx2_f32 sl8-g20 15.05 | 1.107 |
| f32 | 128 | clang_avx512_f32 sl8-tb8balS 27.93 | clang_avx512_f32 sl8-g20 27.75 | 0.994 |
| f32 | 256 | clang_avx512_f32 sl16-tb16bal 57.62 | clang_avx512_f32 sl16-g52 57.85 | 1.004 |
| f32 | 512 | clang_avx512_f32 hyb8-tb8bal 135.70 | clang_avx512_f32 hyb8-g20 137.23 | 1.011 |
| f32 | 1024 | clang_avx512_f32 hyb8-tb8bal 278.49 | clang_avx512_f32 hyb8-g20 273.77 | 0.983 |
| f32 | 4096 | clang_avx512_f32 hyb8-tb8bal 1260.02 | clang_avx512_f32 hyb8-g20 1219.03 | 0.967 |
| f64 | 64 | clang_avx512_f64 sl8-tb8balS 21.46 | gcc_avx512_f64 sl8-g20 20.86 | 0.972 |
| f64 | 128 | clang_avx512_f64 sl16-tb16bal 44.73 | clang_avx512_f64 sl16-g52 45.32 | 1.013 |
| f64 | 256 | clang_avx512_f64 hyb8-tb8bal 109.24 | clang_avx512_f64 hyb8-g20 110.29 | 1.010 |
| f64 | 512 | clang_avx512_f64 hyb16-tb16bal 221.06 | clang_avx512_f64 hyb8-g20 220.66 | 0.998 |
| f64 | 1024 | clang_avx512_f64 hyb16-tb16bal 466.85 | clang_avx512_f64 hyb16-g52 456.86 | 0.979 |
| f64 | 4096 | clang_avx512_f64 hyb16-tb16balS 2299.74 | clang_avx512_f64 hyb16-g52 2256.03 | 0.981 |

