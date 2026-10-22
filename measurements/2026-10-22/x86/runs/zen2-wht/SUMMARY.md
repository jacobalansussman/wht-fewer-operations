# x86-wht summary 

Figure = circuit median / fastest baseline median (textbook, pipe-balanced textbook, FFHT); < 1 is faster.

| test | baseline (ns/unit) | circuit: ratio ... |
|---|---|---|
| pass16_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16 0.0803 (tb16bal 1.430) | g52 0.868; g54d7 1.205; g56d6 1.377 |
| pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16 0.0790 (tb16bal 1.384) | g52 0.780; g54d7 0.799; g56d6 1.014 |
| pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB) | tb16 0.1582 (tb16bal 1.376) | g52 0.785; g54d7 0.800; g56d6 1.013 |
| pass16_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.1457 (tb16bal 1.208) | g52 0.983; g54d7 1.032; g56d6 0.981 |
| pass16_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.0902 (tb16bal 1.513) | g52 1.060; g54d7 0.912; g56d6 1.259 |
| pass16_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 2 S=96 (12 KB) | tb16 0.1816 (tb16bal 1.513) | g52 1.068; g54d7 0.912; g56d6 1.253 |
| pass16_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.1145 (tb16bal 1.153) | g52 1.275; g54d7 0.963; g56d6 1.038 |
| pass16_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.0850 (tb16bal 1.659) | g52 1.013; g54d7 0.953; g56d6 1.169 |
| pass16_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 3 S=96 (12 KB) | tb16 0.1699 (tb16bal 1.591) | g52 1.015; g54d7 0.968; g56d6 1.170 |
| pass16_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16 0.1502 (tb16bal 1.269) | g52 0.971; g54d7 1.138; g56d6 1.285 |
| pass16_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16 0.1600 (tb16bal 1.154) | g52 0.948; g54d7 0.935; g56d6 1.024 |
| pass16_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 4 S=96 (12 KB) | tb16 0.3236 (tb16bal 1.153) | g52 0.968; g54d7 0.931; g56d6 1.021 |
| pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB) | tb8 0.0589 (tb8bal 1.070) | g19 0.862; g20 0.842; g22d4 0.895; h20half 0.893 |
| pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB) | tb8 0.0588 (tb8bal 1.077) | g19 0.905; g20 0.830; g22d4 0.852; h20half 0.818 |
| pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB) | tb8 0.1187 (tb8bal 1.086) | g19 0.919; g20 0.842; g22d4 0.848; h20half 0.816 |
| pass8_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB) | tb8 0.0594 (tb8bal 1.382) | g19 1.530; g20 0.958; g22d4 1.175; h20half 1.631 |
| pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB) | tb8 0.0588 (tb8bal 1.474) | g19 0.990; g20 0.898; g22d4 0.986; h20half 0.913 |
| pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB) | tb8 0.1191 (tb8bal 1.490) | g19 1.002; g20 0.891; g22d4 0.997; h20half 0.919 |
| pass8_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB) | tb8 0.0632 (tb8bal 1.389) | g19 1.234; g20 1.169; g22d4 1.233; h20half 1.016 |
| pass8_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB) | tb8 0.0610 (tb8bal 1.618) | g19 1.138; g20 1.057; g22d4 1.138; h20half 1.046 |
| pass8_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 3 S=240 (15 KB) | tb8 0.1236 (tb8bal 1.605) | g19 1.147; g20 1.050; g22d4 1.138; h20half 1.049 |
| pass8_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB) | tb8 0.0813 (tb8bal 1.138) | g19 1.172; g20 1.075; g22d4 1.128; h20half 1.105 |
| pass8_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB) | tb8 0.0623 (tb8bal 1.687) | g19 1.204; g20 1.125; g22d4 1.194; h20half 1.112 |
| pass8_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 4 S=240 (15 KB) | tb8 0.1251 (tb8bal 1.686) | g19 1.210; g20 1.143; g22d4 1.197; h20half 1.116 |
| regs16_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1 | tb16 13.4730 (tb16bal 1.081) | g52 1.236; g54d7 1.131; g56d6 1.587 |
| regs16_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1 | tb16 13.7067 (tb16bal 1.025) | g52 1.069; g54d7 1.090; g56d6 1.245 |
| regs16_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 1 | tb16 13.7702 (tb16bal 1.025) | g52 1.067; g54d7 1.093; g56d6 1.246 |
| regs16_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2 | tb16 10.4039 (tb16bal 1.464) | g52 1.313; g54d7 1.155; g56d6 1.209 |
| regs16_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2 | tb16 13.9585 (tb16bal 1.296) | g52 1.124; g54d7 1.132; g56d6 1.132 |
| regs16_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 2 | tb16 13.6896 (tb16bal 1.321) | g52 1.129; g54d7 1.132; g56d6 1.145 |
| regs8_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1 | tb8bal 4.0216 (tb8 1.119) | g19 1.817; g20 1.714; g22d4 1.333; h20half 1.814 |
| regs8_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1 | tb8bal 3.9563 (tb8 1.094) | g19 1.830; g20 1.739; g22d4 1.352; h20half 1.708 |
| regs8_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 1 | tb8bal 3.9326 (tb8 1.100) | g19 1.834; g20 1.746; g22d4 1.364; h20half 1.710 |
| regs8_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2 | tb8 3.8338 (tb8bal 1.279) | g19 1.435; g20 1.504; g22d4 1.469; h20half 1.420 |
| regs8_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2 | tb8 4.1419 (tb8bal 1.023) | g19 1.332; g20 1.658; g22d4 1.480; h20half 1.316 |
| regs8_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 2 | tb8 4.0916 (tb8bal 1.025) | g19 1.342; g20 1.677; g22d4 1.479; h20half 1.320 |
| regs8_I3_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3 | tb8 4.0570 (tb8bal 1.143) | g19 1.355; g20 1.331; g22d4 1.187; h20half 1.239 |
| regs8_I3_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3 | tb8 5.1946 (tb8bal 1.335) | g19 1.196; g20 1.142; g22d4 1.109; h20half 1.101 |
| regs8_I3_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 3 | tb8 5.1790 (tb8bal 1.337) | g19 1.200; g20 1.143; g22d4 1.112; h20half 1.106 |
| regs8_I4_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4 | tb8 3.9261 (tb8bal 1.376) | g19 1.488; g20 1.428; g22d4 1.190; h20half 1.195 |
| regs8_I4_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4 | tb8 5.6950 (tb8bal 1.355) | g19 1.115; g20 1.038; g22d4 1.133; h20half 1.084 |
| regs8_I4_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 4 | tb8 5.7497 (tb8bal 1.339) | g19 1.116; g20 1.038; g22d4 1.125; h20half 1.071 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^6 same I=1 | FFHT 0.3648 (textbook 1.729, textbook-bal 2.008) | g52+tb8 1.973; g56d6+tb8 2.224; g52+g19 2.232; g56d6+g22d4 2.736 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^8 same I=1 | FFHT 0.3193 (textbook 1.396, textbook-bal 1.547) | g52+tb8 1.459; g56d6+tb8 1.613; g52+g19 1.522; g56d6+g22d4 1.766 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^10 same I=1 | textbook 0.4032 (textbook-bal 1.143, FFHT 1.056) | g52+tb8 1.027; g56d6+tb8 1.176; g52+g19 1.037; g56d6+g22d4 1.205 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^12 same I=1 | FFHT 0.3770 (textbook 1.196, textbook-bal 1.408) | g52+tb8 1.185; g56d6+tb8 1.444; g52+g19 1.191; g56d6+g22d4 1.461 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^14 same I=1 | FFHT 0.4353 (textbook 1.155, textbook-bal 1.347) | g52+tb8 1.159; g56d6+tb8 1.365; g52+g19 1.179; g56d6+g22d4 1.378 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^16 same I=1 | FFHT 0.4897 (textbook 1.065, textbook-bal 1.247) | g52+tb8 1.050; g56d6+tb8 1.241; g52+g19 1.061; g56d6+g22d4 1.256 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^18 same I=1 | FFHT 0.5216 (textbook 1.162, textbook-bal 1.326) | g52+tb8 1.275; g56d6+tb8 1.340; g52+g19 1.152; g56d6+g22d4 1.338 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^20 same I=1 | FFHT 0.5930 (textbook 1.150, textbook-bal 1.278) | g52+tb8 1.149; g56d6+tb8 1.288; g52+g19 1.125; g56d6+g22d4 1.294 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^6 same I=1 | FFHT 0.3648 (textbook 1.762, textbook-bal 2.071) | g52+tb8 2.042; g56d6+tb8 2.295; g52+g19 2.281; g56d6+g22d4 2.805 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^8 same I=1 | FFHT 0.3163 (textbook 1.297, textbook-bal 1.494) | g52+tb8 1.363; g56d6+tb8 1.466; g52+g19 1.433; g56d6+g22d4 1.621 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^10 same I=1 | textbook 0.3504 (textbook-bal 1.154, FFHT 1.016) | g52+tb8 1.013; g56d6+tb8 1.068; g52+g19 1.022; g56d6+g22d4 1.093 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^12 same I=1 | FFHT 0.3784 (textbook 1.049, textbook-bal 1.255) | g52+tb8 1.007; g56d6+tb8 1.090; g52+g19 1.026; g56d6+g22d4 1.100 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^14 same I=1 | FFHT 0.4307 (textbook 1.041, textbook-bal 1.195) | g52+tb8 0.994; g56d6+tb8 1.070; g52+g19 1.001; g56d6+g22d4 1.074 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^16 same I=1 | textbook 0.4619 (textbook-bal 1.152, FFHT 1.045) | g52+tb8 0.960; g56d6+tb8 1.173; g52+g19 0.987; g56d6+g22d4 1.036 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^18 same I=1 | FFHT 0.5155 (textbook 1.065, textbook-bal 1.199) | g52+tb8 1.023; g56d6+tb8 1.068; g52+g19 1.034; g56d6+g22d4 1.068 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^20 same I=1 | FFHT 0.5963 (textbook 1.021, textbook-bal 1.171) | g52+tb8 0.999; g56d6+tb8 1.064; g52+g19 1.019; g56d6+g22d4 1.098 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1 | FFHT 0.4793 (textbook 1.224, textbook-bal 1.374) | g52+tb8 1.236; g56d6+tb8 1.419; g52+g19 1.208; g56d6+g22d4 1.401 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1 | FFHT 0.6072 (textbook 1.097, textbook-bal 1.222) | g52+tb8 1.085; g56d6+tb8 1.242; g52+g19 1.107; g56d6+g22d4 1.260 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1 | FFHT 0.7074 (textbook 1.165, textbook-bal 1.292) | g52+tb8 1.169; g56d6+tb8 1.298; g52+g19 1.170; g56d6+g22d4 1.301 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1 | FFHT 0.9236 (textbook 1.543, textbook-bal 1.629) | g52+tb8 1.543; g56d6+tb8 1.625; g52+g19 1.544; g56d6+g22d4 1.669 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1 | FFHT 0.4645 (textbook 1.143, textbook-bal 1.284) | g52+tb8 1.111; g56d6+tb8 1.150; g52+g19 1.120; g56d6+g22d4 1.169 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1 | FFHT 0.5801 (textbook 1.045, textbook-bal 1.178) | g52+tb8 1.008; g56d6+tb8 1.075; g52+g19 1.014; g56d6+g22d4 1.071 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1 | FFHT 0.7244 (textbook 1.095, textbook-bal 1.183) | g52+tb8 1.086; g56d6+tb8 1.110; g52+g19 1.075; g56d6+g22d4 1.112 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1 | FFHT 0.9615 (textbook 1.487, textbook-bal 1.523) | g52+tb8 1.482; g56d6+tb8 1.483; g52+g19 1.404; g56d6+g22d4 1.501 |

## Port balancing alone (the textbook with half its adds as FMA by 1, against the plain textbook and FFHT)

A second lead, independent of the circuits: if the balanced textbook is 10 % or more faster than both the plain
textbook and FFHT in whole transforms, an x86 WHT library (FFHT, used by SpinQuant on x86) gains by balancing alone.

- pass16_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.430
- pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.384
- pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.376
- pass16_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.208
- pass16_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.513
- pass16_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 2 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.513
- pass16_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.153
- pass16_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.659
- pass16_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 3 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.591
- pass16_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.269
- pass16_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.154
- pass16_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 4 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.153
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.070
- pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.077
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.086
- pass8_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.382
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.474
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.490
- pass8_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.389
- pass8_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.618
- pass8_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 3 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.605
- pass8_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.138
- pass8_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.687
- pass8_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 4 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.686
- regs16_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 1.081
- regs16_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 1.025
- regs16_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 1.025
- regs16_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 1.464
- regs16_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 1.296
- regs16_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 1.321
- regs8_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.893
- regs8_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.914
- regs8_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.909
- regs8_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 1.279
- regs8_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 1.023
- regs8_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 1.025
- regs8_I3_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 1.143
- regs8_I3_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 1.335
- regs8_I3_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 1.337
- regs8_I4_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.376
- regs8_I4_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.355
- regs8_I4_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.339
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^6 same I=1: balanced / best other textbook-or-FFHT = 2.008 (FFHT 0.3648, plain textbook 0.6308, balanced 0.7327 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.547 (FFHT 0.3193, plain textbook 0.4456, balanced 0.4940 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^10 same I=1: balanced / best other textbook-or-FFHT = 1.143 (FFHT 0.4257, plain textbook 0.4032, balanced 0.4609 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^12 same I=1: balanced / best other textbook-or-FFHT = 1.408 (FFHT 0.3770, plain textbook 0.4509, balanced 0.5308 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^14 same I=1: balanced / best other textbook-or-FFHT = 1.347 (FFHT 0.4353, plain textbook 0.5028, balanced 0.5862 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^16 same I=1: balanced / best other textbook-or-FFHT = 1.247 (FFHT 0.4897, plain textbook 0.5213, balanced 0.6108 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^18 same I=1: balanced / best other textbook-or-FFHT = 1.326 (FFHT 0.5216, plain textbook 0.6060, balanced 0.6918 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^20 same I=1: balanced / best other textbook-or-FFHT = 1.278 (FFHT 0.5930, plain textbook 0.6818, balanced 0.7579 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^6 same I=1: balanced / best other textbook-or-FFHT = 2.071 (FFHT 0.3648, plain textbook 0.6427, balanced 0.7554 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.494 (FFHT 0.3163, plain textbook 0.4102, balanced 0.4725 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^10 same I=1: balanced / best other textbook-or-FFHT = 1.154 (FFHT 0.3561, plain textbook 0.3504, balanced 0.4042 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^12 same I=1: balanced / best other textbook-or-FFHT = 1.255 (FFHT 0.3784, plain textbook 0.3971, balanced 0.4750 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^14 same I=1: balanced / best other textbook-or-FFHT = 1.195 (FFHT 0.4307, plain textbook 0.4482, balanced 0.5146 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^16 same I=1: balanced / best other textbook-or-FFHT = 1.152 (FFHT 0.4826, plain textbook 0.4619, balanced 0.5323 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^18 same I=1: balanced / best other textbook-or-FFHT = 1.199 (FFHT 0.5155, plain textbook 0.5489, balanced 0.6181 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^20 same I=1: balanced / best other textbook-or-FFHT = 1.171 (FFHT 0.5963, plain textbook 0.6091, balanced 0.6983 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1: balanced / best other textbook-or-FFHT = 1.374 (FFHT 0.4793, plain textbook 0.5867, balanced 0.6584 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1: balanced / best other textbook-or-FFHT = 1.222 (FFHT 0.6072, plain textbook 0.6664, balanced 0.7418 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.292 (FFHT 0.7074, plain textbook 0.8243, balanced 0.9142 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.629 (FFHT 0.9236, plain textbook 1.4252, balanced 1.5049 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1: balanced / best other textbook-or-FFHT = 1.284 (FFHT 0.4645, plain textbook 0.5310, balanced 0.5965 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1: balanced / best other textbook-or-FFHT = 1.178 (FFHT 0.5801, plain textbook 0.6063, balanced 0.6833 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.183 (FFHT 0.7244, plain textbook 0.7935, balanced 0.8567 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.523 (FFHT 0.9615, plain textbook 1.4300, balanced 1.4648 ns)

## Cases at or below 0.90 of the fastest baseline (CHECK the whole-transform rows before believing a pass row)

- pass16_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g52 0.868 (baseline tb16)
- pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g52 0.780 (baseline tb16)
- pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g54d7 0.799 (baseline tb16)
- pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): g52 0.785 (baseline tb16)
- pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): g54d7 0.800 (baseline tb16)
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g19 0.862 (baseline tb8)
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g20 0.842 (baseline tb8)
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g22d4 0.895 (baseline tb8)
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): h20half 0.893 (baseline tb8)
- pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g20 0.830 (baseline tb8)
- pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g22d4 0.852 (baseline tb8)
- pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): h20half 0.818 (baseline tb8)
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): g20 0.842 (baseline tb8)
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): g22d4 0.848 (baseline tb8)
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): h20half 0.816 (baseline tb8)
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g20 0.898 (baseline tb8)
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): g20 0.891 (baseline tb8)
