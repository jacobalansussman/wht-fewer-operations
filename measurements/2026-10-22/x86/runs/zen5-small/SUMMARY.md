# x86-hybrid-small summary: the circuits at library sizes (64-512 points), many vectors per call

- Machine: AMD EPYC 9B45; AMD Zen 5
- BATCH: L2 per core 1024 KB (sysfs, cpu47); batch footprint BATCH_KB = 512 KB (B = BATCH_KB / (n x element size))
- Quiet gate: every timing passed az_quiet (or see quiet.log)
- Finite data: 610 of 610 timed (program, size) results ended every repeat finite and free of subnormals.
- One timed call (B vectors) took 9.3-51.8 us (median ns/vector x B); 269 of 610 results are below 20 us per call. Calls are timed in segments of K = 18-32 calls, so one clock read covers at least 168 us.
- Figures: ns per vector, median of >= 9 repeats (best of repeats in brackets); ratios are medians; below 1 = faster. All programs of one binary and one n ran in one process, taking turns.
- Layouts: hyb8 / hyb16 = FFHT's structure (8- or 16-vector steps), called once per vector like FFHT; sl4 / sl8 / sl16 = straight-line: one in-register step does the whole transform, one call runs it over the batch; x86wht = x86-wht's whole transform once per vector. h20half outputs H x / 2^p (p = its 8-point steps).

## Reading per binary (best circuit / best rival at each n; the circuit in brackets)

| binary | width | n=64 | n=128 | n=256 | n=512 | n=1024 | n=4096 | library sizes 2^6-2^9 |
|---|---|---|---|---|---|---|---|---|
| gcc_avx2_f32 | 256bit-f32 | 1.005 (sl8-g20) | 1.005 (sl16-g20x2) | 1.070 (hyb8-h20half) | 0.990 (hyb8-g20) | 0.969 (hyb8-g20) | 0.939 (hyb8-g20) | NO-GAIN (>= 0.95 at every n) |
| clang_avx2_f32 | 256bit-f32 | 1.006 (sl8-g20) | 1.005 (sl16-g52) | 1.044 (hyb8-g20) | 1.036 (hyb8-g20) | 0.993 (hyb8-g20) | 0.981 (hyb8-g20) | NO-GAIN (>= 0.95 at every n) |
| gcc_avx512_f32 | 512bit-f32 | no circuit layout (rival sl4-tb4) | 0.960 (sl8-g20) | **0.874** (sl16-g20x2) | 0.980 (hyb8-g20) | 1.000 (hyb8-g19) | 0.940 (hyb8-g20) | MIXED |
| clang_avx512_f32 | 512bit-f32 | no circuit layout (rival sl4-tb4) | 0.986 (sl8-g20) | 1.030 (sl16-g20x2) | 1.022 (hyb8-g20) | 1.018 (hyb8-g20) | 0.959 (hyb8-g20) | NO-GAIN (>= 0.95 at every n) |
| gcc_avx2_f64 | 256bit-f64 | 0.928 (sl16-g20x2) | 1.006 (hyb8-g20) | 0.972 (hyb8-g20) | 0.943 (hyb8-g20) | 0.945 (hyb8-g20) | 0.939 (hyb8-g20) | MIXED |
| clang_avx2_f64 | 256bit-f64 | 0.969 (sl16-g52) | 1.042 (hyb8-g20) | 1.039 (hyb8-g20) | 0.982 (hyb16-g52) | 0.976 (hyb8-g20) | 0.968 (hyb8-g20) | NO-GAIN (>= 0.95 at every n) |
| gcc_avx512_f64 | 512bit-f64 | 0.949 (sl8-g20) | 0.905 (sl16-g20x2) | 1.007 (hyb8-g20) | 0.993 (hyb8-g20) | 0.943 (hyb8-g20) | 0.950 (hyb8-g20) | MIXED |
| clang_avx512_f64 | 512bit-f64 | 0.987 (sl8-g20) | 1.029 (sl16-g52) | 1.013 (hyb8-g20) | 1.037 (hyb8-g20) | 1.015 (hyb16-g52) | 1.013 (hyb16-g52) | NO-GAIN (>= 0.95 at every n) |

g20 alone (the 3/4 family's 8-point step; hyb8-g20, and sl8-g20 where n is 8 vectors), circuit / best rival:

- gcc_avx2_f32: n=64 sl8-g20 1.005; n=64 hyb8-g20 1.019; n=128 hyb8-g20 1.079; n=128 sl16-g20x2 1.005; n=256 hyb8-g20 1.086; n=512 hyb8-g20 0.990; n=1024 hyb8-g20 0.969; n=4096 hyb8-g20 0.939
- clang_avx2_f32: n=64 sl8-g20 1.006; n=64 hyb8-g20 1.023; n=128 hyb8-g20 1.094; n=128 sl16-g20x2 1.028; n=256 hyb8-g20 1.044; n=512 hyb8-g20 1.036; n=1024 hyb8-g20 0.993; n=4096 hyb8-g20 0.981
- gcc_avx512_f32: n=128 sl8-g20 0.960; n=128 hyb8-g20 1.004; n=256 sl16-g20x2 0.874; n=512 hyb8-g20 0.980; n=1024 hyb8-g20 1.002; n=4096 hyb8-g20 0.940
- clang_avx512_f32: n=128 sl8-g20 0.986; n=128 hyb8-g20 1.024; n=256 sl16-g20x2 1.030; n=512 hyb8-g20 1.022; n=1024 hyb8-g20 1.018; n=4096 hyb8-g20 0.959
- gcc_avx2_f64: n=64 hyb8-g20 0.952; n=64 sl16-g20x2 0.928; n=128 hyb8-g20 1.006; n=256 hyb8-g20 0.972; n=512 hyb8-g20 0.943; n=1024 hyb8-g20 0.945; n=4096 hyb8-g20 0.939
- clang_avx2_f64: n=64 hyb8-g20 1.044; n=64 sl16-g20x2 1.027; n=128 hyb8-g20 1.042; n=256 hyb8-g20 1.039; n=512 hyb8-g20 0.996; n=1024 hyb8-g20 0.976; n=4096 hyb8-g20 0.968
- gcc_avx512_f64: n=64 sl8-g20 0.949; n=64 hyb8-g20 1.000; n=128 hyb8-g20 0.958; n=128 sl16-g20x2 0.905; n=256 hyb8-g20 1.007; n=512 hyb8-g20 0.993; n=1024 hyb8-g20 0.943; n=4096 hyb8-g20 0.950
- clang_avx512_f64: n=64 sl8-g20 0.987; n=64 hyb8-g20 1.019; n=128 hyb8-g20 1.161; n=128 sl16-g20x2 1.045; n=256 hyb8-g20 1.013; n=512 hyb8-g20 1.037; n=1024 hyb8-g20 1.097; n=4096 hyb8-g20 1.028

## gcc_avx2_f32 (256bit-f32)

| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |
|---|---|---|---|---|---|---|---|---|
| 64 | 2048 | FFHT 10.55 (22 us/call) | hyb8-g19 | 10.69 (10.69) | 1.014 (1.014) | 0.959 | 0.952 | yes |
| | | | hyb8-g20 | 10.75 (10.75) | 1.019 (1.019) | 0.964 | 0.958 | yes |
| | | | hyb8-h20half | 10.64 (10.63) | 1.008 (1.008) | 0.954 | 0.947 | yes |
| | | | sl8-g19 | 10.62 (10.61) | 1.007 (1.007) | 0.961 | 0.954 | yes |
| | | | sl8-g20 | 10.60 (10.59) | 1.005 (1.004) | 0.958 | 0.952 | yes |
| | | | sl8-h20half | 10.62 (10.61) | 1.007 (1.007) | 0.960 | 0.954 | yes |
| 128 | 1024 | FFHT 23.18 (24 us/call) | hyb8-g19 | 25.12 (25.10) | 1.084 (1.084) | 1.006 | 0.974 | yes |
| | | | hyb8-g20 | 25.00 (24.99) | 1.079 (1.079) | 1.001 | 0.969 | yes |
| | | | hyb8-h20half | 24.98 (24.96) | 1.077 (1.078) | 1.000 | 0.968 | yes |
| | | | sl16-g52 | 25.95 (25.94) | 1.119 (1.120) | 1.048 | 0.979 | yes |
| | | | sl16-g20x2 | 23.30 (23.29) | 1.005 (1.006) | 0.941 | 0.879 | yes |
| 256 | 512 | FFHT 51.46 (26 us/call) | hyb8-g19 | 55.44 (55.39) | 1.077 (1.078) | 1.026 | 1.008 | yes |
| | | | hyb8-g20 | 55.88 (55.83) | 1.086 (1.087) | 1.034 | 1.016 | yes |
| | | | hyb8-h20half | 55.07 (55.01) | 1.070 (1.071) | 1.019 | 1.001 | yes |
| 512 | 256 | FFHT 108.18 (28 us/call) | hyb8-g19 | 107.44 (107.40) | 0.993 (0.994) | 0.962 | 0.980 | yes |
| | | | hyb8-g20 | 107.13 (107.10) | 0.990 (0.991) | 0.959 | 0.977 | yes |
| | | | hyb8-h20half | 107.27 (107.24) | 0.992 (0.993) | 0.961 | 0.978 | yes |
| | | | hyb16-g52 | 124.07 (124.01) | 1.147 (1.148) | 1.054 | 0.996 | yes |
| 1024 | 128 | FFHT 235.31 (30 us/call) | hyb8-g19 | 229.31 (229.16) | 0.975 (0.975) | 0.937 | 0.954 | yes |
| | | | hyb8-g20 | 227.91 (227.67) | 0.969 (0.969) | 0.932 | 0.948 | yes |
| | | | hyb8-h20half | 229.39 (229.23) | 0.975 (0.975) | 0.938 | 0.954 | yes |
| | | | hyb16-g52 | 243.86 (243.64) | 1.036 (1.036) | 0.975 | 0.980 | yes |
| 4096 | 32 | hyb8-tb8balS 985.77 (32 us/call) | hyb8-g19 | 956.01 (953.35) | 0.970 (0.968) | 0.885 | 0.970 | yes |
| | | | hyb8-g20 | 925.28 (924.87) | 0.939 (0.939) | 0.857 | 0.939 | yes |
| | | | hyb8-h20half | 966.72 (965.82) | 0.981 (0.981) | 0.895 | 0.981 | yes |
| | | | hyb16-g52 | 1134.79 (1125.77) | 1.151 (1.143) | 0.963 | 0.921 | yes |

Every program at each n (ns/vector, median):

- n=64: FFHT 10.55, sl8-g20 10.60, sl8-h20half 10.62, sl8-g19 10.62, hyb8-h20half 10.64, hyb8-g19 10.69, hyb8-g20 10.75, sl8-tb8 11.05, sl8-tb8balS 11.13, hyb8-tb8 11.15, hyb8-tb8balS 11.23, sl8-tb8bal 11.74, hyb8-tb8bal 11.85, x86wht-tb 13.42, x86wht-tbbal 14.19
- n=128: FFHT 23.18, sl16-g20x2 23.30, sl16-tb16 24.77, hyb8-tb8 24.97, hyb8-h20half 24.98, hyb8-g20 25.00, hyb8-g19 25.12, hyb8-tb8balS 25.80, sl16-g52 25.95, sl16-tb16balS 26.50, hyb8-tb8bal 26.90, sl16-tb16bal 29.00, x86wht-tb 30.53, x86wht-tbbal 32.27
- n=256: FFHT 51.46, hyb8-tb8 54.05, hyb8-tb8balS 55.02, hyb8-h20half 55.07, hyb8-g19 55.44, hyb8-g20 55.88, hyb8-tb8bal 57.50, x86wht-tb 64.80, x86wht-tbbal 69.66
- n=512: hyb8-g20 107.13, hyb8-h20half 107.27, hyb8-g19 107.44, FFHT 108.18, hyb8-tb8balS 109.65, hyb8-tb8 111.66, hyb8-tb8bal 117.10, hyb16-tb16 117.66, hyb16-g52 124.07, hyb16-tb16balS 124.54, x86wht-tb 128.86, hyb16-tb16bal 134.43, x86wht-tbbal 141.89
- n=1024: hyb8-g20 227.91, hyb8-g19 229.31, hyb8-h20half 229.39, FFHT 235.31, hyb8-tb8balS 240.38, hyb16-g52 243.86, hyb8-tb8 244.66, hyb16-tb16balS 248.72, hyb16-tb16 250.00, hyb8-tb8bal 254.70, x86wht-tb 269.26, hyb16-tb16bal 273.33, x86wht-tbbal 291.13
- n=4096: hyb8-g20 925.28, hyb8-g19 956.01, hyb8-h20half 966.72, hyb8-tb8balS 985.77, FFHT 1047.91, hyb8-tb8bal 1062.76, hyb8-tb8 1079.97, hyb16-g52 1134.79, hyb16-tb16 1178.93, hyb16-tb16balS 1232.36, hyb16-tb16bal 1317.87, x86wht-tb 1395.48, x86wht-tbbal 1617.39

## clang_avx2_f32 (256bit-f32)

| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |
|---|---|---|---|---|---|---|---|---|
| 64 | 2048 | sl8-tb8balS 9.91 (20 us/call) | hyb8-g19 | 10.41 (10.40) | 1.050 (1.050) | 0.968 | 1.032 | yes |
| | | | hyb8-g20 | 10.14 (10.13) | 1.023 (1.023) | 0.943 | 1.005 | yes |
| | | | hyb8-h20half | 10.46 (10.44) | 1.055 (1.054) | 0.973 | 1.037 | yes |
| | | | sl8-g19 | 10.19 (10.18) | 1.028 (1.028) | 0.963 | 1.028 | yes |
| | | | sl8-g20 | 9.97 (9.96) | 1.006 (1.006) | 0.942 | 1.006 | yes |
| | | | sl8-h20half | 10.06 (10.05) | 1.015 (1.015) | 0.951 | 1.015 | yes |
| 128 | 1024 | sl16-tb16balS 21.48 (22 us/call) | hyb8-g19 | 24.06 (24.04) | 1.120 (1.120) | 0.984 | 1.029 | yes |
| | | | hyb8-g20 | 23.51 (23.49) | 1.094 (1.094) | 0.961 | 1.006 | yes |
| | | | hyb8-h20half | 24.37 (24.34) | 1.135 (1.134) | 0.997 | 1.043 | yes |
| | | | sl16-g52 | 21.58 (21.57) | 1.005 (1.005) | 0.961 | 1.005 | yes |
| | | | sl16-g20x2 | 22.08 (22.07) | 1.028 (1.028) | 0.983 | 1.028 | yes |
| 256 | 512 | FFHT 51.10 (26 us/call) | hyb8-g19 | 54.24 (54.18) | 1.062 (1.061) | 1.026 | 1.054 | yes |
| | | | hyb8-g20 | 53.35 (53.33) | 1.044 (1.045) | 1.010 | 1.036 | yes |
| | | | hyb8-h20half | 54.13 (54.08) | 1.059 (1.059) | 1.024 | 1.052 | yes |
| 512 | 256 | hyb8-tb8balS 97.98 (25 us/call) | hyb8-g19 | 103.57 (103.52) | 1.057 (1.057) | 0.956 | 1.057 | yes |
| | | | hyb8-g20 | 101.47 (101.44) | 1.036 (1.036) | 0.936 | 1.036 | yes |
| | | | hyb8-h20half | 104.74 (104.58) | 1.069 (1.068) | 0.966 | 1.069 | yes |
| | | | hyb16-g52 | 118.01 (117.94) | 1.204 (1.204) | 1.018 | 1.016 | yes |
| 1024 | 128 | hyb8-tb8balS 211.91 (27 us/call) | hyb8-g19 | 214.76 (214.71) | 1.013 (1.014) | 0.907 | 1.013 | yes |
| | | | hyb8-g20 | 210.39 (210.24) | 0.993 (0.993) | 0.888 | 0.993 | yes |
| | | | hyb8-h20half | 218.56 (218.44) | 1.031 (1.032) | 0.923 | 1.031 | yes |
| | | | hyb16-g52 | 230.77 (230.59) | 1.089 (1.089) | 0.965 | 1.016 | yes |
| 4096 | 32 | hyb8-tb8balS 890.50 (28 us/call) | hyb8-g19 | 891.55 (891.38) | 1.001 (1.002) | 0.848 | 1.001 | yes |
| | | | hyb8-g20 | 873.36 (872.44) | 0.981 (0.981) | 0.831 | 0.981 | yes |
| | | | hyb8-h20half | 946.93 (946.65) | 1.063 (1.064) | 0.901 | 1.063 | yes |
| | | | hyb16-g52 | 1029.51 (1028.99) | 1.156 (1.157) | 0.933 | 0.977 | yes |

Every program at each n (ns/vector, median):

- n=64: sl8-tb8balS 9.91, sl8-g20 9.97, sl8-h20half 10.06, hyb8-tb8balS 10.08, hyb8-g20 10.14, sl8-g19 10.19, sl8-tb8bal 10.36, hyb8-g19 10.41, hyb8-tb8bal 10.44, hyb8-h20half 10.46, sl8-tb8 10.58, FFHT 10.62, hyb8-tb8 10.75, x86wht-tb 12.11, x86wht-tbbal 12.40
- n=128: sl16-tb16balS 21.48, sl16-g52 21.58, sl16-tb16bal 21.88, sl16-g20x2 22.08, sl16-tb16 22.45, FFHT 23.17, hyb8-tb8balS 23.37, hyb8-g20 23.51, hyb8-g19 24.06, hyb8-tb8bal 24.25, hyb8-h20half 24.37, hyb8-tb8 24.45, x86wht-tb 24.52, x86wht-tbbal 25.99
- n=256: FFHT 51.10, hyb8-tb8balS 51.48, hyb8-tb8bal 52.21, x86wht-tb 52.61, hyb8-tb8 52.85, hyb8-g20 53.35, hyb8-h20half 54.13, hyb8-g19 54.24, x86wht-tbbal 56.25
- n=512: hyb8-tb8balS 97.98, hyb8-g20 101.47, hyb8-g19 103.57, hyb8-tb8bal 103.58, hyb8-h20half 104.74, FFHT 107.97, hyb8-tb8 108.39, x86wht-tb 109.00, x86wht-tbbal 115.52, hyb16-tb16 115.98, hyb16-tb16balS 116.11, hyb16-g52 118.01, hyb16-tb16bal 121.45
- n=1024: hyb8-g20 210.39, hyb8-tb8balS 211.91, hyb8-g19 214.76, hyb8-h20half 218.56, hyb16-tb16balS 227.12, hyb8-tb8bal 228.05, hyb16-g52 230.77, x86wht-tb 234.43, hyb8-tb8 236.88, x86wht-tbbal 238.82, hyb16-tb16 239.10, FFHT 243.71, hyb16-tb16bal 252.37
- n=4096: hyb8-g20 873.36, hyb8-tb8balS 890.50, hyb8-g19 891.55, hyb8-h20half 946.93, hyb8-tb8bal 981.82, hyb16-g52 1029.51, hyb8-tb8 1051.06, hyb16-tb16balS 1053.31, FFHT 1055.60, hyb16-tb16 1103.30, x86wht-tb 1108.00, hyb16-tb16bal 1112.83, x86wht-tbbal 1144.74

## gcc_avx512_f32 (512bit-f32)

| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |
|---|---|---|---|---|---|---|---|---|
| 64 | 2048 | sl4-tb4 7.20 (15 us/call) | (no circuit layout at this n) | | | | | yes |
| 128 | 1024 | sl8-tb8balS 15.05 (15 us/call) | hyb8-g19 | 15.49 (15.47) | 1.030 (1.029) | 0.941 | 0.978 | yes |
| | | | hyb8-g20 | 15.11 (15.09) | 1.004 (1.004) | 0.919 | 0.954 | yes |
| | | | hyb8-h20half | 15.95 (15.94) | 1.060 (1.061) | 0.969 | 1.007 | yes |
| | | | sl8-g19 | 14.76 (14.75) | 0.981 (0.981) | 0.928 | 0.981 | yes |
| | | | sl8-g20 | 14.44 (14.44) | 0.960 (0.960) | 0.908 | 0.960 | yes |
| | | | sl8-h20half | 15.34 (15.33) | 1.019 (1.020) | 0.965 | 1.019 | yes |
| 256 | 512 | sl16-tb16balS 36.29 (19 us/call) | sl16-g52 | 36.50 (36.48) | 1.006 (1.006) | 0.974 | 1.006 | yes |
| | | | sl16-g20x2 | 31.72 (31.71) | **0.874 (0.874)** | 0.847 | 0.874 | yes |
| 512 | 256 | hyb8-tb8balS 76.32 (20 us/call) | hyb8-g19 | 76.07 (76.05) | 0.997 (0.997) | 0.968 | 0.997 | yes |
| | | | hyb8-g20 | 74.83 (74.74) | 0.980 (0.980) | 0.952 | 0.980 | yes |
| | | | hyb8-h20half | 77.12 (77.01) | 1.011 (1.010) | 0.981 | 1.011 | yes |
| | | | hyb16-g52 | 93.18 (93.11) | 1.221 (1.221) | 1.053 | 1.043 | yes |
| 1024 | 128 | hyb8-tb8balS 151.32 (19 us/call) | hyb8-g19 | 151.37 (151.28) | 1.000 (1.000) | 0.953 | 1.000 | yes |
| | | | hyb8-g20 | 151.66 (151.60) | 1.002 (1.002) | 0.955 | 1.002 | yes |
| | | | hyb8-h20half | 155.89 (155.83) | 1.030 (1.030) | 0.982 | 1.030 | yes |
| | | | hyb16-g52 | 173.02 (172.93) | 1.143 (1.143) | 1.004 | 1.012 | yes |
| 4096 | 32 | hyb8-tb8balS 644.90 (21 us/call) | hyb8-g19 | 621.86 (620.99) | 0.964 (0.963) | 0.932 | 0.964 | yes |
| | | | hyb8-g20 | 606.08 (605.81) | 0.940 (0.940) | 0.908 | 0.940 | yes |
| | | | hyb8-h20half | 638.20 (637.91) | 0.990 (0.990) | 0.956 | 0.990 | yes |
| | | | hyb16-g52 | 687.83 (686.83) | 1.067 (1.066) | 0.976 | 0.996 | yes |

Every program at each n (ns/vector, median):

- n=64: sl4-tb4 7.20, hyb8-tb8 8.38, FFHT 10.55, x86wht-tbbal 12.23, x86wht-tb 12.24
- n=128: sl8-g20 14.44, sl8-g19 14.76, sl8-tb8balS 15.05, hyb8-g20 15.11, sl8-h20half 15.34, hyb8-g19 15.49, hyb8-tb8balS 15.83, sl8-tb8 15.90, hyb8-h20half 15.95, sl8-tb8bal 16.32, hyb8-tb8 16.45, hyb8-tb8bal 18.09, x86wht-tb 19.43, x86wht-tbbal 20.11, FFHT 23.20
- n=256: sl16-g20x2 31.72, sl16-tb16balS 36.29, sl16-g52 36.50, sl16-tb16bal 37.19, sl16-tb16 37.47, hyb8-tb8 39.05, x86wht-tb 49.02, x86wht-tbbal 50.19, FFHT 51.51
- n=512: hyb8-g20 74.83, hyb8-g19 76.07, hyb8-tb8balS 76.32, hyb8-h20half 77.12, hyb8-tb8 78.58, hyb8-tb8bal 79.99, hyb16-tb16 88.50, hyb16-tb16balS 89.34, hyb16-tb16bal 91.36, hyb16-g52 93.18, x86wht-tb 95.29, x86wht-tbbal 98.37, FFHT 108.07
- n=1024: hyb8-tb8balS 151.32, hyb8-g19 151.37, hyb8-g20 151.66, hyb8-h20half 155.89, hyb8-tb8 158.77, hyb8-tb8bal 165.93, hyb16-tb16balS 170.91, hyb16-tb16 172.36, hyb16-g52 173.02, hyb16-tb16bal 175.61, x86wht-tb 185.98, x86wht-tbbal 190.52, FFHT 236.62
- n=4096: hyb8-g20 606.08, hyb8-g19 621.86, hyb8-h20half 638.20, hyb8-tb8balS 644.90, hyb8-tb8 667.55, hyb16-g52 687.83, hyb8-tb8bal 690.03, hyb16-tb16balS 690.70, hyb16-tb16bal 695.24, hyb16-tb16 704.86, x86wht-tb 918.07, x86wht-tbbal 1001.56, FFHT 1046.90

## clang_avx512_f32 (512bit-f32)

| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |
|---|---|---|---|---|---|---|---|---|
| 64 | 2048 | sl4-tb4 5.66 (12 us/call) | (no circuit layout at this n) | | | | | yes |
| 128 | 1024 | sl8-tb8balS 12.13 (12 us/call) | hyb8-g19 | 12.63 (12.62) | 1.041 (1.041) | 0.996 | 1.001 | yes |
| | | | hyb8-g20 | 12.42 (12.41) | 1.024 (1.024) | 0.980 | 0.985 | yes |
| | | | hyb8-h20half | 12.81 (12.80) | 1.056 (1.056) | 1.011 | 1.016 | yes |
| | | | sl8-g19 | 12.27 (12.26) | 1.012 (1.011) | 1.010 | 1.012 | yes |
| | | | sl8-g20 | 11.96 (11.96) | 0.986 (0.987) | 0.984 | 0.986 | yes |
| | | | sl8-h20half | 12.34 (12.33) | 1.017 (1.017) | 1.015 | 1.017 | yes |
| 256 | 512 | sl16-tb16balS 24.34 (12 us/call) | sl16-g52 | 25.52 (25.52) | 1.049 (1.049) | 1.019 | 1.049 | yes |
| | | | sl16-g20x2 | 25.07 (25.05) | 1.030 (1.030) | 1.001 | 1.030 | yes |
| 512 | 256 | hyb8-tb8balS 60.16 (15 us/call) | hyb8-g19 | 62.86 (62.84) | 1.045 (1.046) | 1.038 | 1.045 | yes |
| | | | hyb8-g20 | 61.49 (61.44) | 1.022 (1.023) | 1.016 | 1.022 | yes |
| | | | hyb8-h20half | 62.70 (62.67) | 1.042 (1.043) | 1.036 | 1.042 | yes |
| | | | hyb16-g52 | 83.07 (83.04) | 1.381 (1.382) | 1.050 | 1.056 | yes |
| 1024 | 128 | hyb8-tb8 121.79 (16 us/call) | hyb8-g19 | 127.78 (127.71) | 1.049 (1.049) | 1.049 | 1.021 | yes |
| | | | hyb8-g20 | 123.97 (123.94) | 1.018 (1.018) | 1.018 | 0.990 | yes |
| | | | hyb8-h20half | 126.67 (126.59) | 1.040 (1.040) | 1.040 | 1.012 | yes |
| | | | hyb16-g52 | 154.55 (154.47) | 1.269 (1.269) | 1.042 | 1.063 | yes |
| 4096 | 32 | hyb8-tb8 546.65 (17 us/call) | hyb8-g19 | 540.12 (537.84) | 0.988 (0.996) | 0.988 | 0.985 | yes |
| | | | hyb8-g20 | 524.20 (523.57) | 0.959 (0.969) | 0.959 | 0.956 | yes |
| | | | hyb8-h20half | 545.16 (541.64) | 0.997 (1.003) | 0.997 | 0.994 | yes |
| | | | hyb16-g52 | 621.22 (620.81) | 1.136 (1.149) | 1.021 | 1.042 | yes |

Every program at each n (ns/vector, median):

- n=64: sl4-tb4 5.66, hyb8-tb8 6.06, x86wht-tbbal 8.91, x86wht-tb 8.93, FFHT 10.62
- n=128: sl8-g20 11.96, sl8-tb8balS 12.13, sl8-tb8 12.15, sl8-g19 12.27, sl8-h20half 12.34, hyb8-g20 12.42, sl8-tb8bal 12.54, hyb8-tb8balS 12.61, hyb8-g19 12.63, hyb8-tb8 12.67, hyb8-h20half 12.81, hyb8-tb8bal 12.95, x86wht-tb 15.07, x86wht-tbbal 15.75, FFHT 23.16
- n=256: sl16-tb16balS 24.34, sl16-tb16 25.05, sl16-g20x2 25.07, sl16-g52 25.52, sl16-tb16bal 25.54, x86wht-tb 29.41, x86wht-tbbal 29.69, hyb8-tb8 31.11, FFHT 51.11
- n=512: hyb8-tb8balS 60.16, hyb8-tb8 60.54, hyb8-g20 61.49, hyb8-tb8bal 61.54, hyb8-h20half 62.70, hyb8-g19 62.86, x86wht-tb 68.06, x86wht-tbbal 69.34, hyb16-tb16balS 78.65, hyb16-tb16 79.13, hyb16-tb16bal 80.53, hyb16-g52 83.07, FFHT 108.00
- n=1024: hyb8-tb8 121.79, hyb8-g20 123.97, hyb8-tb8balS 125.17, hyb8-h20half 126.67, hyb8-tb8bal 127.50, hyb8-g19 127.78, x86wht-tb 131.60, x86wht-tbbal 132.70, hyb16-tb16balS 145.38, hyb16-tb16bal 148.18, hyb16-tb16 148.39, hyb16-g52 154.55, FFHT 242.72
- n=4096: hyb8-g20 524.20, hyb8-g19 540.12, hyb8-h20half 545.16, hyb8-tb8 546.65, hyb8-tb8balS 548.49, hyb8-tb8bal 565.84, x86wht-tbbal 566.25, x86wht-tb 577.65, hyb16-tb16balS 596.33, hyb16-tb16 608.36, hyb16-tb16bal 616.29, hyb16-g52 621.22, FFHT 1048.17

## gcc_avx2_f64 (256bit-f64)

| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |
|---|---|---|---|---|---|---|---|---|
| 64 | 1024 | hyb8-tb8balS 17.32 (18 us/call) | hyb8-g19 | 16.82 (16.81) | 0.971 (0.971) | 0.940 | 0.971 | yes |
| | | | hyb8-g20 | 16.49 (16.48) | 0.952 (0.952) | 0.922 | 0.952 | yes |
| | | | hyb8-h20half | 17.01 (16.99) | 0.982 (0.982) | 0.950 | 0.982 | yes |
| | | | sl16-g52 | 19.07 (19.07) | 1.102 (1.102) | 1.068 | 0.989 | yes |
| | | | sl16-g20x2 | 16.08 (16.07) | 0.928 (0.929) | 0.900 | 0.833 | yes |
| 128 | 512 | hyb8-tb8balS 37.88 (19 us/call) | hyb8-g19 | 38.58 (38.54) | 1.018 (1.019) | 0.992 | 1.018 | yes |
| | | | hyb8-g20 | 38.09 (38.05) | 1.006 (1.006) | 0.979 | 1.006 | yes |
| | | | hyb8-h20half | 38.66 (38.62) | 1.021 (1.021) | 0.994 | 1.021 | yes |
| | | | hyb16-g52 | 46.91 (46.89) | 1.238 (1.239) | 1.077 | 1.007 | yes |
| 256 | 256 | hyb8-tb8balS 76.21 (20 us/call) | hyb8-g19 | 74.79 (74.76) | 0.981 (0.982) | 0.900 | 0.981 | yes |
| | | | hyb8-g20 | 74.05 (74.04) | 0.972 (0.972) | 0.891 | 0.972 | yes |
| | | | hyb8-h20half | 75.61 (75.58) | 0.992 (0.992) | 0.910 | 0.992 | yes |
| | | | hyb16-g52 | 95.66 (95.61) | 1.255 (1.255) | 1.077 | 1.005 | yes |
| 512 | 128 | hyb8-tb8balS 174.81 (22 us/call) | hyb8-g19 | 166.75 (166.65) | 0.954 (0.954) | 0.881 | 0.954 | yes |
| | | | hyb8-g20 | 164.84 (164.79) | 0.943 (0.943) | 0.871 | 0.943 | yes |
| | | | hyb8-h20half | 169.11 (169.07) | 0.967 (0.968) | 0.893 | 0.967 | yes |
| | | | hyb16-g52 | 188.15 (188.06) | 1.076 (1.076) | 0.993 | 0.984 | yes |
| 1024 | 64 | hyb8-tb8balS 354.88 (23 us/call) | hyb8-g19 | 343.85 (343.72) | 0.969 (0.969) | 0.872 | 0.969 | yes |
| | | | hyb8-g20 | 335.38 (335.32) | 0.945 (0.945) | 0.851 | 0.945 | yes |
| | | | hyb8-h20half | 348.52 (348.27) | 0.982 (0.982) | 0.884 | 0.982 | yes |
| | | | hyb16-g52 | 391.47 (390.91) | 1.103 (1.102) | 0.956 | 0.908 | yes |
| 4096 | 16 | hyb8-tb8balS 1705.88 (27 us/call) | hyb8-g19 | 1680.66 (1678.51) | 0.985 (0.986) | 0.859 | 0.985 | yes |
| | | | hyb8-g20 | 1602.22 (1601.28) | 0.939 (0.940) | 0.819 | 0.939 | yes |
| | | | hyb8-h20half | 1697.98 (1684.18) | 0.995 (0.989) | 0.868 | 0.995 | yes |
| | | | hyb16-g52 | 2077.62 (2075.74) | 1.218 (1.219) | 0.964 | 0.918 | yes |

Every program at each n (ns/vector, median):

- n=64: sl16-g20x2 16.08, hyb8-g20 16.49, hyb8-g19 16.82, hyb8-h20half 17.01, hyb8-tb8balS 17.32, FFHT 17.38, sl16-tb16 17.86, hyb8-tb8 17.89, hyb8-tb8bal 18.54, sl16-g52 19.07, sl16-tb16balS 19.29, sl16-tb16bal 21.30, x86wht-tb 25.25, x86wht-tbbal 27.95
- n=128: hyb8-tb8balS 37.88, hyb8-g20 38.09, hyb8-g19 38.58, hyb8-h20half 38.66, hyb8-tb8 38.90, FFHT 39.39, hyb8-tb8bal 40.41, hyb16-tb16 43.57, hyb16-tb16balS 46.57, hyb16-g52 46.91, hyb16-tb16bal 50.96, x86wht-tb 55.00, x86wht-tbbal 59.99
- n=256: hyb8-g20 74.05, hyb8-g19 74.79, hyb8-h20half 75.61, hyb8-tb8balS 76.21, hyb8-tb8bal 82.88, hyb8-tb8 83.12, FFHT 84.70, hyb16-tb16 88.83, hyb16-tb16balS 95.14, hyb16-g52 95.66, hyb16-tb16bal 103.12, x86wht-tb 108.20, x86wht-tbbal 119.56
- n=512: hyb8-g20 164.84, hyb8-g19 166.75, hyb8-h20half 169.11, hyb8-tb8balS 174.81, hyb8-tb8bal 187.66, hyb16-g52 188.15, hyb8-tb8 189.28, hyb16-tb16 189.56, FFHT 190.36, hyb16-tb16balS 191.12, hyb16-tb16bal 211.44, x86wht-tb 222.59, x86wht-tbbal 243.90
- n=1024: hyb8-g20 335.38, hyb8-g19 343.85, hyb8-h20half 348.52, hyb8-tb8balS 354.88, hyb8-tb8bal 389.37, hyb16-g52 391.47, hyb8-tb8 394.11, FFHT 402.20, hyb16-tb16 409.64, hyb16-tb16balS 431.03, hyb16-tb16bal 470.04, x86wht-tb 551.96, x86wht-tbbal 663.96
- n=4096: hyb8-g20 1602.22, hyb8-g19 1680.66, hyb8-h20half 1697.98, hyb8-tb8balS 1705.88, hyb8-tb8bal 1861.67, hyb8-tb8 1956.31, FFHT 1973.34, hyb16-g52 2077.62, hyb16-tb16 2156.20, hyb16-tb16balS 2262.61, hyb16-tb16bal 2396.26, x86wht-tb 2442.30, x86wht-tbbal 2889.37

## clang_avx2_f64 (256bit-f64)

| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |
|---|---|---|---|---|---|---|---|---|
| 64 | 1024 | sl16-tb16balS 16.07 (16 us/call) | hyb8-g19 | 16.96 (16.95) | 1.055 (1.056) | 0.966 | 1.009 | yes |
| | | | hyb8-g20 | 16.78 (16.78) | 1.044 (1.045) | 0.956 | 0.999 | yes |
| | | | hyb8-h20half | 17.40 (17.38) | 1.083 (1.083) | 0.991 | 1.036 | yes |
| | | | sl16-g52 | 15.58 (15.57) | 0.969 (0.970) | 0.927 | 0.969 | yes |
| | | | sl16-g20x2 | 16.50 (16.49) | 1.027 (1.027) | 0.981 | 1.027 | yes |
| 128 | 512 | hyb8-tb8balS 37.14 (19 us/call) | hyb8-g19 | 39.19 (39.14) | 1.055 (1.055) | 1.001 | 1.055 | yes |
| | | | hyb8-g20 | 38.70 (38.63) | 1.042 (1.041) | 0.988 | 1.042 | yes |
| | | | hyb8-h20half | 38.97 (38.90) | 1.049 (1.048) | 0.995 | 1.049 | yes |
| | | | hyb16-g52 | 39.82 (39.80) | 1.072 (1.073) | 1.022 | 1.007 | yes |
| 256 | 256 | hyb8-tb8balS 71.93 (18 us/call) | hyb8-g19 | 76.38 (76.31) | 1.062 (1.061) | 0.905 | 1.062 | yes |
| | | | hyb8-g20 | 74.74 (74.71) | 1.039 (1.039) | 0.886 | 1.039 | yes |
| | | | hyb8-h20half | 78.84 (78.81) | 1.096 (1.096) | 0.935 | 1.096 | yes |
| | | | hyb16-g52 | 80.92 (80.88) | 1.125 (1.125) | 0.978 | 0.991 | yes |
| 512 | 128 | hyb8-tb8balS 161.28 (21 us/call) | hyb8-g19 | 163.38 (163.23) | 1.013 (1.013) | 0.871 | 1.013 | yes |
| | | | hyb8-g20 | 160.66 (160.56) | 0.996 (0.996) | 0.857 | 0.996 | yes |
| | | | hyb8-h20half | 170.36 (170.19) | 1.056 (1.056) | 0.909 | 1.056 | yes |
| | | | hyb16-g52 | 158.42 (158.35) | 0.982 (0.982) | 0.876 | 0.970 | yes |
| 1024 | 64 | hyb8-tb8balS 342.88 (22 us/call) | hyb8-g19 | 341.44 (339.63) | 0.996 (1.006) | 0.851 | 0.996 | yes |
| | | | hyb8-g20 | 334.67 (334.40) | 0.976 (0.991) | 0.835 | 0.976 | yes |
| | | | hyb8-h20half | 361.55 (359.10) | 1.054 (1.064) | 0.902 | 1.054 | yes |
| | | | hyb16-g52 | 348.40 (340.92) | 1.016 (1.010) | 0.879 | 0.959 | yes |
| 4096 | 16 | hyb8-tb8balS 1543.26 (25 us/call) | hyb8-g19 | 1540.53 (1537.55) | 0.998 (0.997) | 0.808 | 0.998 | yes |
| | | | hyb8-g20 | 1493.17 (1492.13) | 0.968 (0.968) | 0.783 | 0.968 | yes |
| | | | hyb8-h20half | 1665.38 (1651.93) | 1.079 (1.071) | 0.874 | 1.079 | yes |
| | | | hyb16-g52 | 1681.28 (1679.60) | 1.089 (1.089) | 0.861 | 0.917 | yes |

Every program at each n (ns/vector, median):

- n=64: sl16-g52 15.58, sl16-tb16balS 16.07, sl16-tb16bal 16.27, sl16-g20x2 16.50, hyb8-g20 16.78, hyb8-tb8balS 16.80, sl16-tb16 16.81, hyb8-g19 16.96, hyb8-h20half 17.40, FFHT 17.47, hyb8-tb8 17.56, hyb8-tb8bal 17.78, x86wht-tb 18.37, x86wht-tbbal 19.88
- n=128: hyb8-tb8balS 37.14, hyb8-tb8bal 38.46, hyb8-g20 38.70, hyb16-tb16 38.95, hyb8-h20half 38.97, hyb8-tb8 39.17, hyb8-g19 39.19, FFHT 39.26, hyb16-tb16bal 39.56, hyb16-g52 39.82, hyb16-tb16balS 40.91, x86wht-tb 40.93, x86wht-tbbal 44.21
- n=256: hyb8-tb8balS 71.93, hyb8-g20 74.74, hyb8-g19 76.38, hyb8-tb8bal 78.36, hyb8-h20half 78.84, hyb16-g52 80.92, hyb16-tb16bal 81.65, hyb16-tb16 82.75, hyb16-tb16balS 83.05, hyb8-tb8 84.37, FFHT 84.74, x86wht-tb 84.86, x86wht-tbbal 90.91
- n=512: hyb16-g52 158.42, hyb8-g20 160.66, hyb8-tb8balS 161.28, hyb16-tb16balS 163.35, hyb8-g19 163.38, hyb16-tb16bal 168.56, hyb8-h20half 170.36, hyb8-tb8bal 175.42, hyb16-tb16 180.92, x86wht-tb 184.21, hyb8-tb8 187.51, x86wht-tbbal 188.40, FFHT 196.12
- n=1024: hyb8-g20 334.67, hyb8-g19 341.44, hyb8-tb8balS 342.88, hyb16-g52 348.40, hyb8-h20half 361.55, hyb16-tb16balS 363.22, hyb8-tb8bal 368.88, hyb16-tb16bal 379.75, hyb16-tb16 396.45, FFHT 401.01, hyb8-tb8 401.02, x86wht-tb 404.21, x86wht-tbbal 422.78
- n=4096: hyb8-g20 1493.17, hyb8-g19 1540.53, hyb8-tb8balS 1543.26, hyb8-h20half 1665.38, hyb16-g52 1681.28, hyb8-tb8bal 1726.99, hyb16-tb16balS 1833.48, hyb16-tb16bal 1848.25, x86wht-tb 1865.46, FFHT 1901.62, hyb8-tb8 1906.16, x86wht-tbbal 1929.41, hyb16-tb16 1953.09

## gcc_avx512_f64 (512bit-f64)

| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |
|---|---|---|---|---|---|---|---|---|
| 64 | 1024 | sl8-tb8balS 10.91 (11 us/call) | hyb8-g19 | 11.10 (11.10) | 1.017 (1.017) | 0.934 | 0.983 | yes |
| | | | hyb8-g20 | 10.91 (10.91) | 1.000 (1.000) | 0.918 | 0.966 | yes |
| | | | hyb8-h20half | 11.36 (11.35) | 1.041 (1.041) | 0.956 | 1.006 | yes |
| | | | sl8-g19 | 10.77 (10.76) | 0.986 (0.987) | 0.913 | 0.986 | yes |
| | | | sl8-g20 | 10.36 (10.35) | 0.949 (0.949) | 0.879 | 0.949 | yes |
| | | | sl8-h20half | 11.03 (11.02) | 1.011 (1.011) | 0.936 | 1.011 | yes |
| 128 | 512 | hyb8-tb8balS 26.52 (14 us/call) | hyb8-g19 | 25.95 (25.94) | 0.979 (0.979) | 0.967 | 0.979 | yes |
| | | | hyb8-g20 | 25.41 (25.40) | 0.958 (0.958) | 0.947 | 0.958 | yes |
| | | | hyb8-h20half | 26.77 (26.76) | 1.010 (1.010) | 0.997 | 1.010 | yes |
| | | | sl16-g52 | 27.84 (27.82) | 1.050 (1.050) | 1.008 | 1.041 | yes |
| | | | sl16-g20x2 | 24.00 (23.99) | 0.905 (0.905) | 0.869 | 0.898 | yes |
| 256 | 256 | hyb8-tb8balS 56.12 (14 us/call) | hyb8-g19 | 56.92 (56.89) | 1.014 (1.014) | 0.965 | 1.014 | yes |
| | | | hyb8-g20 | 56.50 (56.49) | 1.007 (1.007) | 0.958 | 1.007 | yes |
| | | | hyb8-h20half | 58.40 (58.39) | 1.041 (1.041) | 0.990 | 1.041 | yes |
| | | | hyb16-g52 | 73.53 (73.51) | 1.310 (1.311) | 1.052 | 1.047 | yes |
| 512 | 128 | hyb8-tb8balS 115.00 (15 us/call) | hyb8-g19 | 116.38 (116.35) | 1.012 (1.012) | 0.971 | 1.012 | yes |
| | | | hyb8-g20 | 114.22 (114.14) | 0.993 (0.993) | 0.953 | 0.993 | yes |
| | | | hyb8-h20half | 117.20 (117.16) | 1.019 (1.019) | 0.978 | 1.019 | yes |
| | | | hyb16-g52 | 137.98 (137.89) | 1.200 (1.200) | 1.025 | 1.052 | yes |
| 1024 | 64 | hyb8-tb8balS 257.56 (16 us/call) | hyb8-g19 | 250.40 (250.30) | 0.972 (0.972) | 0.930 | 0.972 | yes |
| | | | hyb8-g20 | 242.95 (242.91) | 0.943 (0.943) | 0.902 | 0.943 | yes |
| | | | hyb8-h20half | 255.21 (255.14) | 0.991 (0.991) | 0.947 | 0.991 | yes |
| | | | hyb16-g52 | 270.70 (270.38) | 1.051 (1.050) | 1.005 | 1.011 | yes |
| 4096 | 16 | hyb8-tb8balS 1163.42 (19 us/call) | hyb8-g19 | 1136.01 (1120.57) | 0.976 (0.965) | 0.936 | 0.976 | yes |
| | | | hyb8-g20 | 1104.68 (1103.06) | 0.950 (0.950) | 0.911 | 0.950 | yes |
| | | | hyb8-h20half | 1146.51 (1144.89) | 0.985 (0.986) | 0.945 | 0.985 | yes |
| | | | hyb16-g52 | 1229.50 (1227.79) | 1.057 (1.057) | 0.968 | 0.995 | yes |

Every program at each n (ns/vector, median):

- n=64: sl8-g20 10.36, sl8-g19 10.77, hyb8-g20 10.91, sl8-tb8balS 10.91, sl8-h20half 11.03, hyb8-g19 11.10, hyb8-tb8balS 11.29, hyb8-h20half 11.36, sl8-tb8bal 11.37, hyb8-tb8bal 11.75, sl8-tb8 11.79, hyb8-tb8 11.88, x86wht-tb 16.45, FFHT 17.55, x86wht-tbbal 17.55
- n=128: sl16-g20x2 24.00, hyb8-g20 25.41, hyb8-g19 25.95, hyb8-tb8balS 26.52, sl16-tb16balS 26.73, hyb8-h20half 26.77, hyb8-tb8 26.84, hyb8-tb8bal 27.60, sl16-tb16 27.62, sl16-g52 27.84, sl16-tb16bal 27.88, FFHT 39.46, x86wht-tb 41.09, x86wht-tbbal 42.62
- n=256: hyb8-tb8balS 56.12, hyb8-g20 56.50, hyb8-g19 56.92, hyb8-tb8bal 57.91, hyb8-h20half 58.40, hyb8-tb8 59.00, hyb16-tb16 69.87, hyb16-tb16balS 70.21, hyb16-tb16bal 73.11, hyb16-g52 73.53, x86wht-tb 80.86, FFHT 84.71, x86wht-tbbal 85.64
- n=512: hyb8-g20 114.22, hyb8-tb8balS 115.00, hyb8-g19 116.38, hyb8-h20half 117.20, hyb8-tb8 119.85, hyb8-tb8bal 120.96, hyb16-tb16balS 131.21, hyb16-tb16 134.62, hyb16-tb16bal 136.91, hyb16-g52 137.98, x86wht-tb 157.27, x86wht-tbbal 166.87, FFHT 189.19
- n=1024: hyb8-g20 242.95, hyb8-g19 250.40, hyb8-h20half 255.21, hyb8-tb8balS 257.56, hyb8-tb8bal 266.06, hyb16-tb16balS 267.73, hyb16-tb16 269.32, hyb8-tb8 269.37, hyb16-g52 270.70, hyb16-tb16bal 278.40, x86wht-tb 312.90, x86wht-tbbal 339.17, FFHT 400.33
- n=4096: hyb8-g20 1104.68, hyb8-g19 1136.01, hyb8-h20half 1146.51, hyb8-tb8balS 1163.42, hyb8-tb8bal 1200.49, hyb8-tb8 1213.05, hyb16-g52 1229.50, hyb16-tb16balS 1236.15, hyb16-tb16bal 1264.77, hyb16-tb16 1270.37, x86wht-tb 1748.96, x86wht-tbbal 1904.30, FFHT 1908.83

## clang_avx512_f64 (512bit-f64)

| n | B | best rival (ns/vector) | circuit | ns/vector | / best rival | / plain twin | / balanced twin | finite |
|---|---|---|---|---|---|---|---|---|
| 64 | 1024 | sl8-tb8balS 9.23 (9 us/call) | hyb8-g19 | 9.51 (9.50) | 1.029 (1.029) | 0.982 | 0.995 | yes |
| | | | hyb8-g20 | 9.41 (9.40) | 1.019 (1.019) | 0.972 | 0.985 | yes |
| | | | hyb8-h20half | 9.89 (9.89) | 1.071 (1.071) | 1.022 | 1.036 | yes |
| | | | sl8-g19 | 9.27 (9.26) | 1.004 (1.004) | 0.985 | 1.004 | yes |
| | | | sl8-g20 | 9.11 (9.11) | 0.987 (0.987) | 0.968 | 0.987 | yes |
| | | | sl8-h20half | 9.44 (9.43) | 1.022 (1.022) | 1.003 | 1.022 | yes |
| 128 | 512 | sl16-tb16balS 19.61 (10 us/call) | hyb8-g19 | 23.11 (23.10) | 1.178 (1.179) | 1.036 | 1.024 | yes |
| | | | hyb8-g20 | 22.76 (22.74) | 1.161 (1.160) | 1.020 | 1.009 | yes |
| | | | hyb8-h20half | 23.06 (23.05) | 1.176 (1.176) | 1.034 | 1.022 | yes |
| | | | sl16-g52 | 20.18 (20.17) | 1.029 (1.029) | 1.014 | 1.029 | yes |
| | | | sl16-g20x2 | 20.49 (20.49) | 1.045 (1.045) | 1.030 | 1.045 | yes |
| 256 | 256 | hyb8-tb8balS 47.91 (12 us/call) | hyb8-g19 | 48.94 (48.91) | 1.021 (1.022) | 1.011 | 1.021 | yes |
| | | | hyb8-g20 | 48.52 (48.48) | 1.013 (1.013) | 1.002 | 1.013 | yes |
| | | | hyb8-h20half | 50.00 (49.97) | 1.044 (1.043) | 1.033 | 1.044 | yes |
| | | | hyb16-g52 | 54.23 (54.22) | 1.132 (1.132) | 1.064 | 1.060 | yes |
| 512 | 128 | hyb16-tb16balS 97.87 (13 us/call) | hyb8-g19 | 101.58 (101.56) | 1.038 (1.038) | 1.022 | 1.018 | yes |
| | | | hyb8-g20 | 101.47 (101.45) | 1.037 (1.037) | 1.021 | 1.017 | yes |
| | | | hyb8-h20half | 103.64 (103.60) | 1.059 (1.059) | 1.042 | 1.039 | yes |
| | | | hyb16-g52 | 103.82 (103.78) | 1.061 (1.061) | 1.040 | 1.061 | yes |
| 1024 | 64 | hyb16-tb16balS 200.81 (13 us/call) | hyb8-g19 | 224.71 (224.63) | 1.119 (1.119) | 0.972 | 0.991 | yes |
| | | | hyb8-g20 | 220.38 (220.28) | 1.097 (1.097) | 0.953 | 0.972 | yes |
| | | | hyb8-h20half | 226.87 (226.79) | 1.130 (1.130) | 0.981 | 1.000 | yes |
| | | | hyb16-g52 | 203.84 (203.76) | 1.015 (1.015) | 0.994 | 1.015 | yes |
| 4096 | 16 | hyb16-tb16balS 982.04 (16 us/call) | hyb8-g19 | 1018.80 (1017.89) | 1.037 (1.042) | 0.962 | 0.983 | yes |
| | | | hyb8-g20 | 1009.60 (1008.59) | 1.028 (1.033) | 0.953 | 0.974 | yes |
| | | | hyb8-h20half | 1032.34 (1027.02) | 1.051 (1.051) | 0.975 | 0.996 | yes |
| | | | hyb16-g52 | 994.87 (994.44) | 1.013 (1.018) | 0.969 | 1.013 | yes |

Every program at each n (ns/vector, median):

- n=64: sl8-g20 9.11, sl8-tb8balS 9.23, sl8-g19 9.27, hyb8-g20 9.41, sl8-tb8 9.41, sl8-h20half 9.44, hyb8-g19 9.51, hyb8-tb8balS 9.55, hyb8-tb8 9.68, sl8-tb8bal 9.71, hyb8-h20half 9.89, hyb8-tb8bal 9.97, x86wht-tb 12.69, x86wht-tbbal 13.44, FFHT 17.45
- n=128: sl16-tb16balS 19.61, sl16-tb16 19.90, sl16-g52 20.18, sl16-g20x2 20.49, sl16-tb16bal 20.76, hyb8-tb8 22.31, hyb8-tb8balS 22.56, hyb8-g20 22.76, hyb8-h20half 23.06, hyb8-g19 23.11, hyb8-tb8bal 23.51, x86wht-tb 24.06, x86wht-tbbal 24.94, FFHT 39.30
- n=256: hyb8-tb8balS 47.91, hyb8-tb8 48.41, hyb8-g20 48.52, hyb8-g19 48.94, hyb8-h20half 50.00, hyb8-tb8bal 50.08, hyb16-tb16 50.96, hyb16-tb16balS 51.14, hyb16-tb16bal 52.52, hyb16-g52 54.23, x86wht-tbbal 58.06, x86wht-tb 58.66, FFHT 84.71
- n=512: hyb16-tb16balS 97.87, hyb8-tb8 99.42, hyb8-tb8balS 99.79, hyb16-tb16 99.83, hyb8-g20 101.47, hyb8-g19 101.58, hyb16-tb16bal 101.81, hyb8-h20half 103.64, hyb16-g52 103.82, hyb8-tb8bal 104.08, x86wht-tb 112.12, x86wht-tbbal 114.56, FFHT 198.03
- n=1024: hyb16-tb16balS 200.81, hyb16-g52 203.84, hyb16-tb16 205.14, hyb16-tb16bal 214.20, hyb8-g20 220.38, hyb8-g19 224.71, hyb8-tb8balS 226.77, hyb8-h20half 226.87, hyb8-tb8 231.15, x86wht-tb 231.40, x86wht-tbbal 237.26, hyb8-tb8bal 238.07, FFHT 401.27
- n=4096: hyb16-tb16balS 982.04, hyb16-g52 994.87, hyb8-g20 1009.60, hyb8-g19 1018.80, hyb16-tb16 1026.71, hyb8-h20half 1032.34, hyb8-tb8balS 1036.87, hyb16-tb16bal 1044.65, hyb8-tb8 1059.14, hyb8-tb8bal 1089.01, x86wht-tbbal 1102.53, x86wht-tb 1117.35, FFHT 1922.60

## Fastest code on this machine per precision and n (across binaries: SEPARATE processes, minutes apart)

| precision | n | fastest rival (binary, program, ns/vector) | fastest circuit (binary, program, ns/vector) | circuit / rival |
|---|---|---|---|---|
| f32 | 64 | clang_avx512_f32 sl4-tb4 5.66 | clang_avx2_f32 sl8-g20 9.97 | 1.760 |
| f32 | 128 | clang_avx512_f32 sl8-tb8balS 12.13 | clang_avx512_f32 sl8-g20 11.96 | 0.986 |
| f32 | 256 | clang_avx512_f32 sl16-tb16balS 24.34 | clang_avx512_f32 sl16-g20x2 25.07 | 1.030 |
| f32 | 512 | clang_avx512_f32 hyb8-tb8balS 60.16 | clang_avx512_f32 hyb8-g20 61.49 | 1.022 |
| f32 | 1024 | clang_avx512_f32 hyb8-tb8 121.79 | clang_avx512_f32 hyb8-g20 123.97 | 1.018 |
| f32 | 4096 | clang_avx512_f32 hyb8-tb8 546.65 | clang_avx512_f32 hyb8-g20 524.20 | 0.959 |
| f64 | 64 | clang_avx512_f64 sl8-tb8balS 9.23 | clang_avx512_f64 sl8-g20 9.11 | 0.987 |
| f64 | 128 | clang_avx512_f64 sl16-tb16balS 19.61 | clang_avx512_f64 sl16-g52 20.18 | 1.029 |
| f64 | 256 | clang_avx512_f64 hyb8-tb8balS 47.91 | clang_avx512_f64 hyb8-g20 48.52 | 1.013 |
| f64 | 512 | clang_avx512_f64 hyb16-tb16balS 97.87 | clang_avx512_f64 hyb8-g20 101.47 | 1.037 |
| f64 | 1024 | clang_avx512_f64 hyb16-tb16balS 200.81 | clang_avx512_f64 hyb16-g52 203.84 | 1.015 |
| f64 | 4096 | clang_avx512_f64 hyb16-tb16balS 982.04 | clang_avx512_f64 hyb16-g52 994.87 | 1.013 |

