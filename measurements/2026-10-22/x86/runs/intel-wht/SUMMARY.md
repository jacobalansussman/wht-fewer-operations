# x86-wht summary 

Figure = circuit median / fastest baseline median (textbook, pipe-balanced textbook, FFHT); < 1 is faster.

| test | baseline (ns/unit) | circuit: ratio ... |
|---|---|---|
| pass16_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16 0.1287 (tb16bal 1.232) | g52 1.122; g54d7 1.305; g56d6 1.249 |
| pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16 0.1157 (tb16bal 1.327) | g52 1.087; g54d7 1.177; g56d6 1.123 |
| pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB) | tb16 0.2306 (tb16bal 1.311) | g52 1.091; g54d7 1.170; g56d6 1.108 |
| pass16_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.1774 (tb16bal 1.119) | g52 1.042; g54d7 1.149; g56d6 1.108 |
| pass16_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.1568 (tb16bal 1.314) | g52 1.105; g54d7 0.957; g56d6 1.117 |
| pass16_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 2 S=96 (12 KB) | tb16 0.3110 (tb16bal 1.320) | g52 1.080; g54d7 0.937; g56d6 1.129 |
| pass16_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.2077 (tb16bal 1.309) | g52 1.201; g54d7 1.187; g56d6 1.017 |
| pass16_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.1435 (tb16bal 1.328) | g52 1.041; g54d7 0.966; g56d6 1.072 |
| pass16_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 3 S=96 (12 KB) | tb16 0.2915 (tb16bal 1.350) | g52 1.052; g54d7 0.984; g56d6 1.092 |
| pass16_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16 0.2313 (tb16bal 1.145) | g52 1.091; g54d7 1.170; g56d6 1.154 |
| pass16_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16 0.2471 (tb16bal 1.112) | g52 1.043; g54d7 1.074; g56d6 1.069 |
| pass16_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 4 S=96 (12 KB) | tb16 0.5066 (tb16bal 1.093) | g52 1.046; g54d7 1.064; g56d6 1.065 |
| pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB) | tb8 0.0870 (tb8bal 1.075) | g19 1.094; g20 1.075; g22d4 0.982; h20half 1.193 |
| pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB) | tb8 0.0893 (tb8bal 1.156) | g19 1.093; g20 1.046; g22d4 1.011; h20half 1.094 |
| pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB) | tb8 0.1798 (tb8bal 1.132) | g19 1.080; g20 1.051; g22d4 1.007; h20half 1.095 |
| pass8_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB) | tb8 0.0915 (tb8bal 1.221) | g19 1.188; g20 1.074; g22d4 1.148; h20half 1.334 |
| pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB) | tb8 0.0908 (tb8bal 1.377) | g19 1.089; g20 1.036; g22d4 1.057; h20half 1.047 |
| pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB) | tb8 0.1813 (tb8bal 1.397) | g19 1.088; g20 1.043; g22d4 1.049; h20half 1.074 |
| pass8_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB) | tb8 0.1110 (tb8bal 1.050) | g19 1.051; g20 0.944; g22d4 1.077; h20half 1.118 |
| pass8_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB) | tb8 0.1049 (tb8bal 1.295) | g19 1.055; g20 1.016; g22d4 0.981; h20half 1.088 |
| pass8_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 3 S=240 (15 KB) | tb8 0.2116 (tb8bal 1.306) | g19 1.073; g20 1.041; g22d4 0.993; h20half 1.082 |
| pass8_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB) | tb8 0.1097 (tb8bal 1.084) | g19 1.095; g20 0.988; g22d4 1.121; h20half 1.125 |
| pass8_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB) | tb8 0.1152 (tb8bal 1.384) | g19 1.165; g20 1.122; g22d4 1.074; h20half 1.153 |
| pass8_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 4 S=240 (15 KB) | tb8 0.2167 (tb8bal 1.301) | g19 1.058; g20 1.016; g22d4 0.994; h20half 1.070 |
| regs16_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1 | tb16 14.0548 (tb16bal 1.077) | g52 1.474; g54d7 1.364; g56d6 1.769 |
| regs16_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1 | tb16 16.0663 (tb16bal 1.006) | g52 1.281; g54d7 1.207; g56d6 1.303 |
| regs16_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 1 | tb16 15.9906 (tb16bal 1.019) | g52 1.275; g54d7 1.211; g56d6 1.333 |
| regs16_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2 | tb16 30.3489 (tb16bal 1.412) | g52 1.125; g54d7 1.065; g56d6 0.982 |
| regs16_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2 | tb16 19.9275 (tb16bal 1.143) | g52 1.123; g54d7 1.162; g56d6 1.095 |
| regs16_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 2 | tb16 19.7238 (tb16bal 1.168) | g52 1.117; g54d7 1.173; g56d6 1.108 |
| regs8_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1 | tb8bal 7.0553 (tb8 1.015) | g19 1.756; g20 1.670; g22d4 1.272; h20half 1.855 |
| regs8_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1 | tb8 7.0586 (tb8bal 1.084) | g19 1.688; g20 1.595; g22d4 1.240; h20half 1.631 |
| regs8_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 1 | tb8 7.0103 (tb8bal 1.072) | g19 1.682; g20 1.596; g22d4 1.230; h20half 1.636 |
| regs8_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2 | tb8 5.4717 (tb8bal 1.036) | g19 1.393; g20 1.384; g22d4 1.285; h20half 1.531 |
| regs8_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2 | tb8 5.6050 (tb8bal 1.051) | g19 1.356; g20 1.485; g22d4 1.269; h20half 1.324 |
| regs8_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 2 | tb8 5.6439 (tb8bal 1.046) | g19 1.350; g20 1.477; g22d4 1.269; h20half 1.330 |
| regs8_I3_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3 | tb8 5.6674 (tb8bal 1.054) | g19 1.214; g20 1.129; g22d4 1.034; h20half 1.274 |
| regs8_I3_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3 | tb8 7.6329 (tb8bal 1.110) | g19 1.088; g20 1.041; g22d4 1.013; h20half 1.079 |
| regs8_I3_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 3 | tb8 8.4018 (tb8bal 1.042) | g19 1.032; g20 0.996; g22d4 0.943; h20half 1.074 |
| regs8_I4_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4 | tb8 12.4873 (tb8bal 1.016) | g19 1.139; g20 1.250; g22d4 1.025; h20half 1.182 |
| regs8_I4_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4 | tb8 8.3832 (tb8bal 1.073) | g19 1.043; g20 1.058; g22d4 0.978; h20half 1.030 |
| regs8_I4_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 4 | tb8 8.5331 (tb8bal 1.088) | g19 1.057; g20 1.064; g22d4 0.994; h20half 1.046 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^6 same I=1 | FFHT 0.6773 (textbook 1.923, textbook-bal 2.123) | g52+tb8 2.118; g56d6+tb8 2.373; g52+g19 2.331; g56d6+g22d4 2.834 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^8 same I=1 | FFHT 0.5890 (textbook 1.501, textbook-bal 1.607) | g52+tb8 1.636; g56d6+tb8 1.661; g52+g19 1.605; g56d6+g22d4 1.805 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^10 same I=1 | FFHT 0.6006 (textbook 1.233, textbook-bal 1.282) | g52+tb8 1.260; g56d6+tb8 1.305; g52+g19 1.294; g56d6+g22d4 1.338 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^12 same I=1 | FFHT 0.5821 (textbook 1.382, textbook-bal 1.450) | g52+tb8 1.406; g56d6+tb8 1.461; g52+g19 1.429; g56d6+g22d4 1.479 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^14 same I=1 | FFHT 0.6976 (textbook 1.283, textbook-bal 1.347) | g52+tb8 1.323; g56d6+tb8 1.348; g52+g19 1.323; g56d6+g22d4 1.353 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^16 same I=1 | FFHT 0.8271 (textbook 1.166, textbook-bal 1.214) | g52+tb8 1.192; g56d6+tb8 1.238; g52+g19 1.195; g56d6+g22d4 1.236 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^18 same I=1 | FFHT 0.9407 (textbook 1.177, textbook-bal 1.233) | g52+tb8 1.205; g56d6+tb8 1.255; g52+g19 1.221; g56d6+g22d4 1.249 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^20 same I=1 | FFHT 1.1494 (textbook 1.288, textbook-bal 1.342) | g52+tb8 1.305; g56d6+tb8 1.338; g52+g19 1.305; g56d6+g22d4 1.342 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^6 same I=1 | FFHT 0.7593 (textbook 2.253, textbook-bal 2.527) | g52+tb8 2.473; g56d6+tb8 2.684; g52+g19 2.682; g56d6+g22d4 3.095 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^8 same I=1 | FFHT 0.6120 (textbook 1.476, textbook-bal 1.573) | g52+tb8 1.554; g56d6+tb8 1.642; g52+g19 1.619; g56d6+g22d4 1.764 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^10 same I=1 | FFHT 0.5680 (textbook 1.171, textbook-bal 1.267) | g52+tb8 1.191; g56d6+tb8 1.245; g52+g19 1.228; g56d6+g22d4 1.273 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^12 same I=1 | FFHT 0.5828 (textbook 1.153, textbook-bal 1.284) | g52+tb8 1.184; g56d6+tb8 1.222; g52+g19 1.190; g56d6+g22d4 1.221 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^14 same I=1 | FFHT 0.6969 (textbook 1.129, textbook-bal 1.247) | g52+tb8 1.142; g56d6+tb8 1.193; g52+g19 1.158; g56d6+g22d4 1.198 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^16 same I=1 | FFHT 0.7992 (textbook 1.050, textbook-bal 1.146) | g52+tb8 1.073; g56d6+tb8 1.096; g52+g19 1.071; g56d6+g22d4 1.093 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^18 same I=1 | FFHT 0.9127 (textbook 1.078, textbook-bal 1.193) | g52+tb8 1.110; g56d6+tb8 1.128; g52+g19 1.098; g56d6+g22d4 1.130 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^20 same I=1 | FFHT 1.1343 (textbook 1.219, textbook-bal 1.298) | g52+tb8 1.223; g56d6+tb8 1.244; g52+g19 1.222; g56d6+g22d4 1.242 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1 | FFHT 0.7561 (textbook 1.440, textbook-bal 1.461) | g52+tb8 1.406; g56d6+tb8 1.440; g52+g19 1.402; g56d6+g22d4 1.412 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1 | FFHT 1.0414 (textbook 1.204, textbook-bal 1.269) | g52+tb8 1.191; g56d6+tb8 1.222; g52+g19 1.179; g56d6+g22d4 1.206 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1 | FFHT 1.4178 (textbook 1.313, textbook-bal 1.349) | g52+tb8 1.310; g56d6+tb8 1.347; g52+g19 1.284; g56d6+g22d4 1.286 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1 | FFHT 1.8124 (textbook 1.462, textbook-bal 1.476) | g52+tb8 1.432; g56d6+tb8 1.449; g52+g19 1.415; g56d6+g22d4 1.417 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1 | FFHT 0.7458 (textbook 1.284, textbook-bal 1.322) | g52+tb8 1.226; g56d6+tb8 1.255; g52+g19 1.225; g56d6+g22d4 1.247 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1 | FFHT 0.9932 (textbook 1.144, textbook-bal 1.160) | g52+tb8 1.076; g56d6+tb8 1.111; g52+g19 1.065; g56d6+g22d4 1.084 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1 | FFHT 1.3557 (textbook 1.269, textbook-bal 1.284) | g52+tb8 1.218; g56d6+tb8 1.234; g52+g19 1.222; g56d6+g22d4 1.230 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1 | FFHT 1.8102 (textbook 1.375, textbook-bal 1.392) | g52+tb8 1.345; g56d6+tb8 1.357; g52+g19 1.342; g56d6+g22d4 1.360 |

## Port balancing alone (the textbook with half its adds as FMA by 1, against the plain textbook and FFHT)

A second lead, independent of the circuits: if the balanced textbook is 10 % or more faster than both the plain
textbook and FFHT in whole transforms, an x86 WHT library (FFHT, used by SpinQuant on x86) gains by balancing alone.

- pass16_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.232
- pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.327
- pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.311
- pass16_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.119
- pass16_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.314
- pass16_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 2 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.320
- pass16_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.309
- pass16_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.328
- pass16_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 3 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.350
- pass16_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.145
- pass16_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.112
- pass16_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 4 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.093
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.075
- pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.156
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.132
- pass8_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.221
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.377
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.397
- pass8_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.050
- pass8_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.295
- pass8_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 3 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.306
- pass8_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.084
- pass8_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.384
- pass8_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 4 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.301
- regs16_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 1.077
- regs16_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 1.006
- regs16_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 1.019
- regs16_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 1.412
- regs16_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 1.143
- regs16_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 1.168
- regs8_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.986
- regs8_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 1.084
- regs8_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 1.072
- regs8_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 1.036
- regs8_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 1.051
- regs8_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 1.046
- regs8_I3_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 1.054
- regs8_I3_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 1.110
- regs8_I3_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 1.042
- regs8_I4_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.016
- regs8_I4_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.073
- regs8_I4_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.088
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^6 same I=1: balanced / best other textbook-or-FFHT = 2.123 (FFHT 0.6773, plain textbook 1.3024, balanced 1.4378 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.607 (FFHT 0.5890, plain textbook 0.8842, balanced 0.9466 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^10 same I=1: balanced / best other textbook-or-FFHT = 1.282 (FFHT 0.6006, plain textbook 0.7406, balanced 0.7698 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^12 same I=1: balanced / best other textbook-or-FFHT = 1.450 (FFHT 0.5821, plain textbook 0.8046, balanced 0.8440 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^14 same I=1: balanced / best other textbook-or-FFHT = 1.347 (FFHT 0.6976, plain textbook 0.8947, balanced 0.9397 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^16 same I=1: balanced / best other textbook-or-FFHT = 1.214 (FFHT 0.8271, plain textbook 0.9644, balanced 1.0039 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^18 same I=1: balanced / best other textbook-or-FFHT = 1.233 (FFHT 0.9407, plain textbook 1.1072, balanced 1.1602 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^20 same I=1: balanced / best other textbook-or-FFHT = 1.342 (FFHT 1.1494, plain textbook 1.4805, balanced 1.5429 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^6 same I=1: balanced / best other textbook-or-FFHT = 2.527 (FFHT 0.7593, plain textbook 1.7106, balanced 1.9191 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.573 (FFHT 0.6120, plain textbook 0.9033, balanced 0.9626 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^10 same I=1: balanced / best other textbook-or-FFHT = 1.267 (FFHT 0.5680, plain textbook 0.6650, balanced 0.7198 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^12 same I=1: balanced / best other textbook-or-FFHT = 1.284 (FFHT 0.5828, plain textbook 0.6718, balanced 0.7486 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^14 same I=1: balanced / best other textbook-or-FFHT = 1.247 (FFHT 0.6969, plain textbook 0.7871, balanced 0.8693 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^16 same I=1: balanced / best other textbook-or-FFHT = 1.146 (FFHT 0.7992, plain textbook 0.8390, balanced 0.9156 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^18 same I=1: balanced / best other textbook-or-FFHT = 1.193 (FFHT 0.9127, plain textbook 0.9842, balanced 1.0889 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^20 same I=1: balanced / best other textbook-or-FFHT = 1.298 (FFHT 1.1343, plain textbook 1.3828, balanced 1.4719 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1: balanced / best other textbook-or-FFHT = 1.461 (FFHT 0.7561, plain textbook 1.0887, balanced 1.1050 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1: balanced / best other textbook-or-FFHT = 1.269 (FFHT 1.0414, plain textbook 1.2534, balanced 1.3211 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.349 (FFHT 1.4178, plain textbook 1.8609, balanced 1.9133 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.476 (FFHT 1.8124, plain textbook 2.6496, balanced 2.6748 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1: balanced / best other textbook-or-FFHT = 1.322 (FFHT 0.7458, plain textbook 0.9576, balanced 0.9863 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1: balanced / best other textbook-or-FFHT = 1.160 (FFHT 0.9932, plain textbook 1.1360, balanced 1.1526 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.284 (FFHT 1.3557, plain textbook 1.7207, balanced 1.7410 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.392 (FFHT 1.8102, plain textbook 2.4895, balanced 2.5193 ns)

## No circuit reaches 0.90 of the fastest baseline in any test.
