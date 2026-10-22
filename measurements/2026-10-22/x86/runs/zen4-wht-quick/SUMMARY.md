# x86-wht summary 

Figure = circuit median / fastest baseline median (textbook, pipe-balanced textbook, FFHT); < 1 is faster.

| test | baseline (ns/unit) | circuit: ratio ... |
|---|---|---|
| pass16_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16 0.0763 (tb16bal 1.309) | g52 0.819; g54d7 1.007; g56d6 1.231 |
| pass16_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16bal 0.0648 (tb16 1.136) | g52 0.775; g54d7 0.840; g56d6 0.926 |
| pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16 0.0734 (tb16bal 1.153) | g52 0.715; g54d7 0.751; g56d6 0.824 |
| pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB) | tb16 0.1468 (tb16bal 1.154) | g52 0.713; g54d7 0.751; g56d6 0.825 |
| pass16_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16bal 0.0563 (tb16 1.302) | g52 0.902; g54d7 0.929; g56d6 0.947 |
| pass16_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16bal 0.0542 (tb16 1.354) | g52 0.876; g54d7 0.943; g56d6 1.033 |
| pass16_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 1 S=96 (12 KB) | tb16bal 0.1131 (tb16 1.317) | g52 0.844; g54d7 0.903; g56d6 0.992 |
| pass16_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.1032 (tb16bal 1.234) | g52 0.967; g54d7 1.046; g56d6 0.938 |
| pass16_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16bal 0.0723 (tb16 1.321) | g52 0.823; g54d7 0.964; g56d6 0.986 |
| pass16_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.0823 (tb16bal 1.330) | g52 0.938; g54d7 0.930; g56d6 1.162 |
| pass16_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 2 S=96 (12 KB) | tb16 0.1649 (tb16bal 1.329) | g52 0.936; g54d7 0.927; g56d6 1.159 |
| pass16_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.0746 (tb16bal 1.235) | g52 0.755; g54d7 0.832; g56d6 1.098 |
| pass16_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.0858 (tb16bal 1.047) | g52 0.713; g54d7 0.805; g56d6 0.853 |
| pass16_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB) | tb16bal 0.1813 (tb16 1.013) | g52 0.693; g54d7 0.760; g56d6 0.854 |
| pass16_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.2314 (tb16bal 1.082) | g52 0.584; g54d7 0.821; g56d6 0.741 |
| pass16_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16bal 0.0912 (tb16 1.175) | g52 0.899; g54d7 1.027; g56d6 0.941 |
| pass16_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.0752 (tb16bal 1.347) | g52 0.996; g54d7 0.874; g56d6 1.049 |
| pass16_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 3 S=96 (12 KB) | tb16 0.1536 (tb16bal 1.318) | g52 0.984; g54d7 0.867; g56d6 1.038 |
| pass16_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.0736 (tb16bal 1.060) | g52 0.842; g54d7 0.784; g56d6 0.886 |
| pass16_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.0832 (tb16bal 1.022) | g52 0.881; g54d7 0.840; g56d6 0.913 |
| pass16_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 3 S=96 (12 KB) | tb16 0.1663 (tb16bal 1.025) | g52 0.881; g54d7 0.839; g56d6 0.909 |
| pass16_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16 0.1386 (tb16bal 1.095) | g52 0.965; g54d7 1.068; g56d6 1.173 |
| pass16_I4_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16bal 0.1372 (tb16 1.090) | g52 0.923; g54d7 0.938; g56d6 0.980 |
| pass16_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16 0.1498 (tb16bal 1.064) | g52 0.923; g54d7 0.917; g56d6 0.941 |
| pass16_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 4 S=96 (12 KB) | tb16 0.3006 (tb16bal 1.059) | g52 0.923; g54d7 0.919; g56d6 0.943 |
| pass16_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16bal 0.1370 (tb16 1.091) | g52 1.008; g54d7 1.007; g56d6 1.002 |
| pass16_I4_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16bal 0.1391 (tb16 1.115) | g52 0.952; g54d7 0.974; g56d6 1.025 |
| pass16_I4_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 4 S=96 (12 KB) | tb16bal 0.2789 (tb16 1.114) | g52 0.950; g54d7 0.972; g56d6 1.023 |
| pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB) | tb8bal 0.0464 (tb8 1.185) | g19 0.825; g20 0.810; g22d4 0.832; h20half 1.045 |
| pass8_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB) | tb8bal 0.0520 (tb8 1.056) | g19 0.756; g20 0.856; g22d4 0.917; h20half 0.892 |
| pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB) | tb8bal 0.0468 (tb8 1.182) | g19 0.900; g20 0.814; g22d4 0.816; h20half 0.955 |
| pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB) | tb8bal 0.0977 (tb8 1.132) | g19 0.861; g20 0.781; g22d4 0.784; h20half 0.915 |
| pass8_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB) | tb8bal 0.0479 (tb8 1.146) | g19 0.879; g20 0.789; g22d4 0.793; h20half 0.933 |
| pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB) | tb8bal 0.0521 (tb8 1.054) | g19 0.868; g20 0.852; g22d4 0.883; h20half 0.866 |
| pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB) | tb8bal 0.1028 (tb8 1.068) | g19 0.851; g20 0.860; g22d4 0.865; h20half 0.846 |
| pass8_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB) | tb8 0.0554 (tb8bal 1.038) | g19 1.106; g20 0.774; g22d4 0.973; h20half 1.094 |
| pass8_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB) | tb8bal 0.0525 (tb8 1.046) | g19 0.821; g20 0.815; g22d4 0.893; h20half 0.910 |
| pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB) | tb8 0.0549 (tb8bal 1.129) | g19 0.829; g20 0.772; g22d4 0.818; h20half 0.862 |
| pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB) | tb8 0.1098 (tb8bal 1.134) | g19 0.838; g20 0.775; g22d4 0.822; h20half 0.867 |
| pass8_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB) | tb8bal 0.0472 (tb8 1.186) | g19 0.892; g20 0.801; g22d4 0.811; h20half 0.934 |
| pass8_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB) | tb8bal 0.0471 (tb8 1.168) | g19 0.928; g20 0.860; g22d4 0.949; h20half 0.949 |
| pass8_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB) | tb8bal 0.0947 (tb8 1.166) | g19 0.905; g20 0.864; g22d4 0.955; h20half 0.946 |
| pass8_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB) | tb8 0.0564 (tb8bal 1.099) | g19 1.142; g20 0.961; g22d4 1.074; h20half 1.055 |
| pass8_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB) | tb8bal 0.0551 (tb8 1.027) | g19 0.917; g20 0.897; g22d4 0.871; h20half 0.964 |
| pass8_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB) | tb8 0.0571 (tb8bal 1.275) | g19 0.972; g20 0.926; g22d4 0.951; h20half 0.998 |
| pass8_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 3 S=240 (15 KB) | tb8 0.1143 (tb8bal 1.276) | g19 0.997; g20 0.958; g22d4 0.964; h20half 1.017 |
| pass8_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB) | tb8bal 0.0492 (tb8 1.116) | g19 0.819; g20 0.776; g22d4 0.787; h20half 0.919 |
| pass8_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB) | tb8bal 0.0547 (tb8 1.007) | g19 0.867; g20 0.801; g22d4 0.828; h20half 0.910 |
| pass8_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB) | tb8bal 0.1076 (tb8 1.025) | g19 0.874; g20 0.810; g22d4 0.839; h20half 0.929 |
| pass8_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB) | tb8 0.0758 (tb8bal 1.059) | g19 1.157; g20 1.077; g22d4 1.119; h20half 1.112 |
| pass8_I4_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 4 S=384 (12 KB) | tb8bal 0.0642 (tb8 1.195) | g19 1.073; g20 0.819; g22d4 1.022; h20half 1.146 |
| pass8_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB) | tb8 0.0589 (tb8bal 1.353) | g19 1.039; g20 1.007; g22d4 1.022; h20half 1.070 |
| pass8_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 4 S=240 (15 KB) | tb8 0.1172 (tb8bal 1.340) | g19 1.044; g20 1.005; g22d4 1.022; h20half 1.078 |
| pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB) | tb8 0.0549 (tb8bal 1.107) | g19 0.829; g20 0.780; g22d4 0.770; h20half 0.887 |
| pass8_I4_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 4 S=384 (12 KB) | tb8 0.0565 (tb8bal 1.373) | g19 1.012; g20 0.995; g22d4 1.014; h20half 1.122 |
| pass8_I4_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 4 S=192 (12 KB) | tb8 0.1121 (tb8bal 1.199) | g19 1.019; g20 0.983; g22d4 1.002; h20half 1.128 |
| regs16_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1 | tb16 10.0048 (tb16bal 1.175) | g52 1.475; g54d7 1.374; g56d6 1.930 |
| regs16_I1_clang_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 1 | tb16bal 11.4536 (tb16 1.636) | g52 1.072; g54d7 1.294; g56d6 1.173 |
| regs16_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1 | tb16bal 13.1472 (tb16 1.016) | g52 1.026; g54d7 1.079; g56d6 1.196 |
| regs16_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 1 | tb16bal 13.1534 (tb16 1.016) | g52 1.025; g54d7 1.078; g56d6 1.195 |
| regs16_I1_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 1 | tb16bal 5.9539 (tb16 1.575) | g52 1.567; g54d7 1.606; g56d6 1.564 |
| regs16_I1_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 1 | tb16bal 9.9665 (tb16 1.880) | g52 1.291; g54d7 1.572; g56d6 1.345 |
| regs16_I1_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 1 | tb16bal 9.9681 (tb16 1.880) | g52 1.290; g54d7 1.572; g56d6 1.345 |
| regs16_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2 | tb16 9.6338 (tb16bal 1.143) | g52 1.161; g54d7 1.039; g56d6 1.043 |
| regs16_I2_clang_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2 | tb16bal 10.5900 (tb16 1.769) | g52 0.965; g54d7 0.984; g56d6 0.987 |
| regs16_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2 | tb16 12.2673 (tb16bal 1.156) | g52 1.111; g54d7 1.120; g56d6 1.074 |
| regs16_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 2 | tb16 12.2671 (tb16bal 1.156) | g52 1.111; g54d7 1.120; g56d6 1.074 |
| regs16_I2_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 2 | tb16bal 6.3853 (tb16 1.467) | g52 1.140; g54d7 1.182; g56d6 1.041 |
| regs16_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2 | tb16bal 12.0678 (tb16 1.553) | g52 0.887; g54d7 0.938; g56d6 0.890 |
| regs16_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 2 | tb16bal 12.0741 (tb16 1.553) | g52 0.887; g54d7 0.938; g56d6 0.890 |
| regs8_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1 | tb8bal 3.8928 (tb8 1.047) | g19 1.733; g20 1.602; g22d4 1.314; h20half 1.740 |
| regs8_I1_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 1 | tb8bal 5.1525 (tb8 1.363) | g19 1.535; g20 1.335; g22d4 1.333; h20half 1.567 |
| regs8_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1 | tb8bal 3.6993 (tb8 1.026) | g19 1.757; g20 1.746; g22d4 1.309; h20half 1.677 |
| regs8_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 1 | tb8bal 3.6952 (tb8 1.027) | g19 1.759; g20 1.747; g22d4 1.309; h20half 1.678 |
| regs8_I1_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 1 | tb8bal 3.7005 (tb8 1.026) | g19 1.819; g20 1.747; g22d4 1.312; h20half 1.602 |
| regs8_I1_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 1 | tb8bal 4.6649 (tb8 1.506) | g19 1.609; g20 1.537; g22d4 1.415; h20half 1.543 |
| regs8_I1_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 1 | tb8bal 4.6660 (tb8 1.506) | g19 1.608; g20 1.538; g22d4 1.415; h20half 1.544 |
| regs8_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2 | tb8 3.5161 (tb8bal 1.294) | g19 1.440; g20 1.507; g22d4 1.475; h20half 1.407 |
| regs8_I2_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 2 | tb8bal 4.3324 (tb8 1.621) | g19 0.945; g20 1.075; g22d4 0.949; h20half 1.354 |
| regs8_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2 | tb8bal 3.7230 (tb8 1.058) | g19 1.369; g20 1.705; g22d4 1.470; h20half 1.399 |
| regs8_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 2 | tb8bal 3.7131 (tb8 1.061) | g19 1.375; g20 1.710; g22d4 1.494; h20half 1.402 |
| regs8_I2_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 2 | tb8bal 2.1754 (tb8 1.617) | g19 1.595; g20 1.597; g22d4 1.307; h20half 1.672 |
| regs8_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 2 | tb8bal 4.0506 (tb8 1.735) | g19 1.013; g20 1.113; g22d4 1.084; h20half 1.391 |
| regs8_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 2 | tb8bal 4.0511 (tb8 1.734) | g19 1.013; g20 1.111; g22d4 1.084; h20half 1.391 |
| regs8_I3_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3 | tb8bal 8.4874 (tb8 1.000) | g19 1.579; g20 1.191; g22d4 1.557; h20half 1.577 |
| regs8_I3_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 3 | tb8bal 3.8392 (tb8 1.830) | g19 1.439; g20 0.933; g22d4 1.144; h20half 1.522 |
| regs8_I3_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3 | tb8 4.5827 (tb8bal 1.114) | g19 1.162; g20 1.149; g22d4 1.059; h20half 1.092 |
| regs8_I3_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 3 | tb8 4.5828 (tb8bal 1.114) | g19 1.161; g20 1.145; g22d4 1.059; h20half 1.097 |
| regs8_I3_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 3 | tb8bal 3.1331 (tb8 1.130) | g19 1.162; g20 1.130; g22d4 1.041; h20half 1.253 |
| regs8_I3_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 3 | tb8bal 6.0845 (tb8 1.174) | g19 0.986; g20 0.947; g22d4 0.967; h20half 1.016 |
| regs8_I3_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 3 | tb8bal 6.0856 (tb8 1.173) | g19 0.986; g20 0.947; g22d4 0.965; h20half 1.024 |
| regs8_I4_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4 | tb8 3.6467 (tb8bal 1.087) | g19 1.368; g20 1.253; g22d4 1.037; h20half 1.128 |
| regs8_I4_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 4 | tb8bal 5.3762 (tb8 1.307) | g19 1.252; g20 1.037; g22d4 0.971; h20half 1.124 |
| regs8_I4_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4 | tb8 5.2473 (tb8bal 1.111) | g19 1.039; g20 1.003; g22d4 1.018; h20half 1.061 |
| regs8_I4_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 4 | tb8 5.2457 (tb8bal 1.111) | g19 1.040; g20 1.002; g22d4 1.018; h20half 1.061 |
| regs8_I4_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 4 | tb8bal 3.4528 (tb8 1.029) | g19 0.993; g20 1.001; g22d4 0.867; h20half 1.030 |
| regs8_I4_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 4 | tb8 8.0491 (tb8bal 1.125) | g19 1.003; g20 0.972; g22d4 0.938; h20half 1.091 |
| regs8_I4_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 4 | tb8 8.0618 (tb8bal 1.125) | g19 1.000; g20 0.975; g22d4 0.937; h20half 1.091 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^6 same I=1 | FFHT 0.2941 (textbook 1.782, textbook-bal 2.154) | g52+tb8 2.091; g56d6+tb8 2.388; g52+g19 2.424; g56d6+g22d4 3.031 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^8 same I=1 | FFHT 0.3002 (textbook 1.185, textbook-bal 1.272) | g52+tb8 1.212; g56d6+tb8 1.349; g52+g19 1.255; g56d6+g22d4 1.395 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^10 same I=1 | textbook 0.3363 (textbook-bal 1.070, FFHT 1.034) | g52+tb8 1.022; g56d6+tb8 1.117; g52+g19 1.005; g56d6+g22d4 1.087 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^12 same I=1 | FFHT 0.3603 (textbook 1.084, textbook-bal 1.200) | g52+tb8 1.061; g56d6+tb8 1.200; g52+g19 1.077; g56d6+g22d4 1.206 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^14 same I=1 | FFHT 0.4014 (textbook 1.079, textbook-bal 1.195) | g52+tb8 1.088; g56d6+tb8 1.193; g52+g19 1.080; g56d6+g22d4 1.200 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^16 same I=1 | textbook 0.4496 (textbook-bal 1.092, FFHT 1.007) | g52+tb8 0.983; g56d6+tb8 1.094; g52+g19 0.977; g56d6+g22d4 1.083 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^18 same I=1 | FFHT 0.4798 (textbook 1.030, textbook-bal 1.128) | g52+tb8 1.042; g56d6+tb8 1.143; g52+g19 1.014; g56d6+g22d4 1.141 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^20 same I=1 | FFHT 0.5313 (textbook 1.068, textbook-bal 1.158) | g52+tb8 1.062; g56d6+tb8 1.173; g52+g19 1.055; g56d6+g22d4 1.156 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^6 same I=1 | FFHT 0.2931 (textbook 1.858, textbook-bal 2.264) | g52+tb8 2.170; g56d6+tb8 2.467; g52+g19 2.515; g56d6+g22d4 3.107 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^8 same I=1 | FFHT 0.3008 (textbook 1.131, textbook-bal 1.292) | g52+tb8 1.195; g56d6+tb8 1.291; g52+g19 1.266; g56d6+g22d4 1.434 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^10 same I=1 | textbook 0.3099 (textbook-bal 1.071, FFHT 1.095) | g52+tb8 1.004; g56d6+tb8 1.012; g52+g19 0.957; g56d6+g22d4 1.014 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^12 same I=1 | FFHT 0.3589 (textbook 1.002, textbook-bal 1.095) | g52+tb8 0.909; g56d6+tb8 0.964; g52+g19 0.913; g56d6+g22d4 0.974 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^14 same I=1 | FFHT 0.4012 (textbook 1.001, textbook-bal 1.091) | g52+tb8 0.928; g56d6+tb8 0.990; g52+g19 0.931; g56d6+g22d4 0.986 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^16 same I=1 | textbook 0.4146 (textbook-bal 1.072, FFHT 1.087) | g52+tb8 0.929; g56d6+tb8 0.973; g52+g19 0.909; g56d6+g22d4 0.974 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^18 same I=1 | textbook 0.4696 (textbook-bal 1.061, FFHT 1.020) | g52+tb8 0.921; g56d6+tb8 1.132; g52+g19 0.929; g56d6+g22d4 0.973 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^20 same I=1 | FFHT 0.5395 (textbook 1.024, textbook-bal 1.063) | g52+tb8 0.926; g56d6+tb8 0.967; g52+g19 0.942; g56d6+g22d4 0.989 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^6 same I=1 | FFHT 0.2927 (textbook 1.741, textbook-bal 1.918) | g52+tb8 1.920; g56d6+tb8 2.129; g52+g19 2.180; g56d6+g22d4 2.724 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^8 same I=1 | FFHT 0.2979 (textbook 1.107, textbook-bal 1.133) | g52+tb8 1.151; g56d6+tb8 1.192; g52+g19 1.187; g56d6+g22d4 1.266 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^10 same I=1 | textbook-bal 0.3259 (textbook 1.007, FFHT 1.042) | g52+tb8 0.977; g56d6+tb8 0.983; g52+g19 0.985; g56d6+g22d4 0.992 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^12 same I=1 | textbook-bal 0.3174 (textbook 1.102, FFHT 1.131) | g52+tb8 0.979; g56d6+tb8 1.005; g52+g19 0.974; g56d6+g22d4 1.016 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^14 same I=1 | textbook-bal 0.3981 (textbook 1.077, FFHT 1.008) | g52+tb8 0.985; g56d6+tb8 0.998; g52+g19 0.983; g56d6+g22d4 1.004 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^16 same I=1 | textbook-bal 0.4080 (textbook 1.081, FFHT 1.102) | g52+tb8 0.988; g56d6+tb8 1.009; g52+g19 0.970; g56d6+g22d4 0.994 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^18 same I=1 | textbook-bal 0.4565 (textbook 1.070, FFHT 1.057) | g52+tb8 0.987; g56d6+tb8 1.021; g52+g19 0.983; g56d6+g22d4 1.000 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^20 same I=1 | textbook-bal 0.5270 (textbook 1.053, FFHT 1.028) | g52+tb8 0.985; g56d6+tb8 0.997; g52+g19 0.980; g56d6+g22d4 0.992 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1 | FFHT 0.3705 (textbook 1.101, textbook-bal 1.194) | g52+tb8 1.084; g56d6+tb8 1.219; g52+g19 1.086; g56d6+g22d4 1.221 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1 | FFHT 0.5033 (textbook 1.010, textbook-bal 1.074) | g52+tb8 1.007; g56d6+tb8 1.099; g52+g19 0.993; g56d6+g22d4 1.089 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1 | FFHT 0.5679 (textbook 1.130, textbook-bal 1.188) | g52+tb8 1.126; g56d6+tb8 1.211; g52+g19 1.133; g56d6+g22d4 1.218 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1 | FFHT 0.7386 (textbook 1.371, textbook-bal 1.425) | g52+tb8 1.368; g56d6+tb8 1.427; g52+g19 1.373; g56d6+g22d4 1.439 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1 | FFHT 0.3704 (textbook 1.022, textbook-bal 1.120) | g52+tb8 0.945; g56d6+tb8 0.999; g52+g19 0.943; g56d6+g22d4 1.007 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1 | textbook 0.4784 (textbook-bal 1.062, FFHT 1.044) | g52+tb8 0.941; g56d6+tb8 0.979; g52+g19 0.925; g56d6+g22d4 0.978 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1 | FFHT 0.5667 (textbook 1.081, textbook-bal 1.155) | g52+tb8 1.041; g56d6+tb8 1.066; g52+g19 1.042; g56d6+g22d4 1.082 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1 | FFHT 0.7359 (textbook 1.336, textbook-bal 1.390) | g52+tb8 1.299; g56d6+tb8 1.323; g52+g19 1.287; g56d6+g22d4 1.329 |
| whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^12 separate I=1 | textbook-bal 0.3329 (textbook 1.085, FFHT 1.109) | g52+tb8 0.969; g56d6+tb8 1.005; g52+g19 0.969; g56d6+g22d4 1.005 |
| whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^16 separate I=1 | textbook-bal 0.4492 (textbook 1.072, FFHT 1.111) | g52+tb8 0.989; g56d6+tb8 1.006; g52+g19 0.972; g56d6+g22d4 0.992 |
| whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^20 separate I=1 | FFHT 0.5649 (textbook 1.079, textbook-bal 1.027) | g52+tb8 1.011; g56d6+tb8 1.025; g52+g19 1.015; g56d6+g22d4 1.025 |
| whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^24 separate I=1 | FFHT 0.7350 (textbook 1.315, textbook-bal 1.294) | g52+tb8 1.273; g56d6+tb8 1.281; g52+g19 1.285; g56d6+g22d4 1.289 |

## Port balancing alone (the textbook with half its adds as FMA by 1, against the plain textbook and FFHT)

A second lead, independent of the circuits: if the balanced textbook is 10 % or more faster than both the plain
textbook and FFHT in whole transforms, an x86 WHT library (FFHT, used by SpinQuant on x86) gains by balancing alone.

- pass16_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.309
- pass16_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.880
- pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.153
- pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.154
- pass16_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.768
- pass16_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.738
- pass16_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 1 S=96 (12 KB): balanced / best other textbook-or-FFHT = 0.760
- pass16_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.234
- pass16_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.757
- pass16_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.330
- pass16_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 2 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.329
- pass16_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.235
- pass16_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.047
- pass16_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB): balanced / best other textbook-or-FFHT = 0.987
- pass16_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.082
- pass16_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.851
- pass16_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.347
- pass16_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 3 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.318
- pass16_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.060
- pass16_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.022
- pass16_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 3 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.025
- pass16_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.095
- pass16_I4_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.918
- pass16_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.064
- pass16_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 4 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.059
- pass16_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.916
- pass16_I4_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.897
- pass16_I4_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 4 S=96 (12 KB): balanced / best other textbook-or-FFHT = 0.898
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.844
- pass8_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): balanced / best other textbook-or-FFHT = 0.947
- pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.846
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): balanced / best other textbook-or-FFHT = 0.883
- pass8_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.872
- pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): balanced / best other textbook-or-FFHT = 0.949
- pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.936
- pass8_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.038
- pass8_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): balanced / best other textbook-or-FFHT = 0.956
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.129
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.134
- pass8_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.843
- pass8_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): balanced / best other textbook-or-FFHT = 0.856
- pass8_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.858
- pass8_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.099
- pass8_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): balanced / best other textbook-or-FFHT = 0.973
- pass8_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.275
- pass8_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 3 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.276
- pass8_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.896
- pass8_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): balanced / best other textbook-or-FFHT = 0.993
- pass8_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.976
- pass8_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.059
- pass8_I4_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 4 S=384 (12 KB): balanced / best other textbook-or-FFHT = 0.837
- pass8_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.353
- pass8_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 4 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.340
- pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.107
- pass8_I4_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 4 S=384 (12 KB): balanced / best other textbook-or-FFHT = 1.373
- pass8_I4_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.199
- regs16_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 1.175
- regs16_I1_clang_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.611
- regs16_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.984
- regs16_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.985
- regs16_I1_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.635
- regs16_I1_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.532
- regs16_I1_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.532
- regs16_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 1.143
- regs16_I2_clang_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 0.565
- regs16_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 1.156
- regs16_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 1.156
- regs16_I2_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 0.682
- regs16_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 0.644
- regs16_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 0.644
- regs8_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.955
- regs8_I1_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.734
- regs8_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.974
- regs8_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.974
- regs8_I1_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.974
- regs8_I1_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.664
- regs8_I1_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.664
- regs8_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 1.294
- regs8_I2_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 0.617
- regs8_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 0.945
- regs8_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 0.943
- regs8_I2_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 0.618
- regs8_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 0.576
- regs8_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 0.577
- regs8_I3_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 1.000
- regs8_I3_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 0.546
- regs8_I3_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 1.114
- regs8_I3_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 1.114
- regs8_I3_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 0.885
- regs8_I3_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 0.852
- regs8_I3_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 0.852
- regs8_I4_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.087
- regs8_I4_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 0.765
- regs8_I4_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.111
- regs8_I4_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.111
- regs8_I4_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 0.972
- regs8_I4_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.125
- regs8_I4_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.125
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^6 same I=1: balanced / best other textbook-or-FFHT = 2.154 (FFHT 0.2941, plain textbook 0.5240, balanced 0.6335 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.272 (FFHT 0.3002, plain textbook 0.3556, balanced 0.3818 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^10 same I=1: balanced / best other textbook-or-FFHT = 1.070 (FFHT 0.3476, plain textbook 0.3363, balanced 0.3598 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^12 same I=1: balanced / best other textbook-or-FFHT = 1.200 (FFHT 0.3603, plain textbook 0.3905, balanced 0.4325 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^14 same I=1: balanced / best other textbook-or-FFHT = 1.195 (FFHT 0.4014, plain textbook 0.4332, balanced 0.4796 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^16 same I=1: balanced / best other textbook-or-FFHT = 1.092 (FFHT 0.4528, plain textbook 0.4496, balanced 0.4909 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^18 same I=1: balanced / best other textbook-or-FFHT = 1.128 (FFHT 0.4798, plain textbook 0.4941, balanced 0.5411 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^20 same I=1: balanced / best other textbook-or-FFHT = 1.158 (FFHT 0.5313, plain textbook 0.5674, balanced 0.6154 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^6 same I=1: balanced / best other textbook-or-FFHT = 2.264 (FFHT 0.2931, plain textbook 0.5445, balanced 0.6635 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.292 (FFHT 0.3008, plain textbook 0.3402, balanced 0.3885 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^10 same I=1: balanced / best other textbook-or-FFHT = 1.071 (FFHT 0.3394, plain textbook 0.3099, balanced 0.3318 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^12 same I=1: balanced / best other textbook-or-FFHT = 1.095 (FFHT 0.3589, plain textbook 0.3597, balanced 0.3929 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^14 same I=1: balanced / best other textbook-or-FFHT = 1.091 (FFHT 0.4012, plain textbook 0.4017, balanced 0.4379 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^16 same I=1: balanced / best other textbook-or-FFHT = 1.072 (FFHT 0.4505, plain textbook 0.4146, balanced 0.4446 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^18 same I=1: balanced / best other textbook-or-FFHT = 1.061 (FFHT 0.4792, plain textbook 0.4696, balanced 0.4982 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^20 same I=1: balanced / best other textbook-or-FFHT = 1.063 (FFHT 0.5395, plain textbook 0.5524, balanced 0.5737 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^6 same I=1: balanced / best other textbook-or-FFHT = 1.918 (FFHT 0.2927, plain textbook 0.5097, balanced 0.5613 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.133 (FFHT 0.2979, plain textbook 0.3298, balanced 0.3375 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^10 same I=1: balanced / best other textbook-or-FFHT = 0.993 (FFHT 0.3395, plain textbook 0.3282, balanced 0.3259 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^12 same I=1: balanced / best other textbook-or-FFHT = 0.908 (FFHT 0.3591, plain textbook 0.3497, balanced 0.3174 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^14 same I=1: balanced / best other textbook-or-FFHT = 0.993 (FFHT 0.4011, plain textbook 0.4286, balanced 0.3981 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^16 same I=1: balanced / best other textbook-or-FFHT = 0.925 (FFHT 0.4495, plain textbook 0.4412, balanced 0.4080 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^18 same I=1: balanced / best other textbook-or-FFHT = 0.946 (FFHT 0.4826, plain textbook 0.4884, balanced 0.4565 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^20 same I=1: balanced / best other textbook-or-FFHT = 0.973 (FFHT 0.5415, plain textbook 0.5547, balanced 0.5270 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1: balanced / best other textbook-or-FFHT = 1.194 (FFHT 0.3705, plain textbook 0.4079, balanced 0.4424 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1: balanced / best other textbook-or-FFHT = 1.074 (FFHT 0.5033, plain textbook 0.5081, balanced 0.5404 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.188 (FFHT 0.5679, plain textbook 0.6416, balanced 0.6745 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.425 (FFHT 0.7386, plain textbook 1.0127, balanced 1.0523 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1: balanced / best other textbook-or-FFHT = 1.120 (FFHT 0.3704, plain textbook 0.3786, balanced 0.4150 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1: balanced / best other textbook-or-FFHT = 1.062 (FFHT 0.4995, plain textbook 0.4784, balanced 0.5081 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.155 (FFHT 0.5667, plain textbook 0.6127, balanced 0.6546 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.390 (FFHT 0.7359, plain textbook 0.9829, balanced 1.0227 ns)
- whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^12 separate I=1: balanced / best other textbook-or-FFHT = 0.921 (FFHT 0.3691, plain textbook 0.3613, balanced 0.3329 ns)
- whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^16 separate I=1: balanced / best other textbook-or-FFHT = 0.933 (FFHT 0.4989, plain textbook 0.4814, balanced 0.4492 ns)
- whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.027 (FFHT 0.5649, plain textbook 0.6097, balanced 0.5804 ns)
- whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.294 (FFHT 0.7350, plain textbook 0.9664, balanced 0.9508 ns)

## Cases at or below 0.90 of the fastest baseline (CHECK the whole-transform rows before believing a pass row)

- pass16_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g52 0.819 (baseline tb16)
- pass16_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB): g52 0.775 (baseline tb16bal)
- pass16_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB): g54d7 0.840 (baseline tb16bal)
- pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g52 0.715 (baseline tb16)
- pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g54d7 0.751 (baseline tb16)
- pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g56d6 0.824 (baseline tb16)
- pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): g52 0.713 (baseline tb16)
- pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): g54d7 0.751 (baseline tb16)
- pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): g56d6 0.825 (baseline tb16)
- pass16_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB): g52 0.876 (baseline tb16bal)
- pass16_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 1 S=96 (12 KB): g52 0.844 (baseline tb16bal)
- pass16_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB): g52 0.823 (baseline tb16bal)
- pass16_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): g52 0.755 (baseline tb16)
- pass16_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): g54d7 0.832 (baseline tb16)
- pass16_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB): g52 0.713 (baseline tb16)
- pass16_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB): g54d7 0.805 (baseline tb16)
- pass16_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB): g56d6 0.853 (baseline tb16)
- pass16_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB): g52 0.693 (baseline tb16bal)
- pass16_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB): g54d7 0.760 (baseline tb16bal)
- pass16_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB): g56d6 0.854 (baseline tb16bal)
- pass16_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): g52 0.584 (baseline tb16)
- pass16_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): g54d7 0.821 (baseline tb16)
- pass16_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): g56d6 0.741 (baseline tb16)
- pass16_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB): g52 0.899 (baseline tb16bal)
- pass16_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): g54d7 0.874 (baseline tb16)
- pass16_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 3 S=96 (12 KB): g54d7 0.867 (baseline tb16)
- pass16_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): g52 0.842 (baseline tb16)
- pass16_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): g54d7 0.784 (baseline tb16)
- pass16_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): g56d6 0.886 (baseline tb16)
- pass16_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB): g52 0.881 (baseline tb16)
- pass16_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB): g54d7 0.840 (baseline tb16)
- pass16_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 3 S=96 (12 KB): g52 0.881 (baseline tb16)
- pass16_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 3 S=96 (12 KB): g54d7 0.839 (baseline tb16)
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g19 0.825 (baseline tb8bal)
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g20 0.810 (baseline tb8bal)
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g22d4 0.832 (baseline tb8bal)
- pass8_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): g19 0.756 (baseline tb8bal)
- pass8_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): g20 0.856 (baseline tb8bal)
- pass8_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): h20half 0.892 (baseline tb8bal)
- pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g19 0.900 (baseline tb8bal)
- pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g20 0.814 (baseline tb8bal)
- pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g22d4 0.816 (baseline tb8bal)
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): g19 0.861 (baseline tb8bal)
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): g20 0.781 (baseline tb8bal)
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): g22d4 0.784 (baseline tb8bal)
- pass8_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g19 0.879 (baseline tb8bal)
- pass8_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g20 0.789 (baseline tb8bal)
- pass8_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g22d4 0.793 (baseline tb8bal)
- pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): g19 0.868 (baseline tb8bal)
- pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): g20 0.852 (baseline tb8bal)
- pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): g22d4 0.883 (baseline tb8bal)
- pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): h20half 0.866 (baseline tb8bal)
- pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): g19 0.851 (baseline tb8bal)
- pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): g20 0.860 (baseline tb8bal)
- pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): g22d4 0.865 (baseline tb8bal)
- pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): h20half 0.846 (baseline tb8bal)
- pass8_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g20 0.774 (baseline tb8)
- pass8_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): g19 0.821 (baseline tb8bal)
- pass8_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): g20 0.815 (baseline tb8bal)
- pass8_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): g22d4 0.893 (baseline tb8bal)
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g19 0.829 (baseline tb8)
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g20 0.772 (baseline tb8)
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g22d4 0.818 (baseline tb8)
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): h20half 0.862 (baseline tb8)
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): g19 0.838 (baseline tb8)
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): g20 0.775 (baseline tb8)
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): g22d4 0.822 (baseline tb8)
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): h20half 0.867 (baseline tb8)
- pass8_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g19 0.892 (baseline tb8bal)
- pass8_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g20 0.801 (baseline tb8bal)
- pass8_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g22d4 0.811 (baseline tb8bal)
- pass8_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): g20 0.860 (baseline tb8bal)
- pass8_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB): g20 0.864 (baseline tb8bal)
- pass8_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): g20 0.897 (baseline tb8bal)
- pass8_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): g22d4 0.871 (baseline tb8bal)
- pass8_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g19 0.819 (baseline tb8bal)
- pass8_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g20 0.776 (baseline tb8bal)
- pass8_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g22d4 0.787 (baseline tb8bal)
- pass8_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): g19 0.867 (baseline tb8bal)
- pass8_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): g20 0.801 (baseline tb8bal)
- pass8_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): g22d4 0.828 (baseline tb8bal)
- pass8_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB): g19 0.874 (baseline tb8bal)
- pass8_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB): g20 0.810 (baseline tb8bal)
- pass8_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB): g22d4 0.839 (baseline tb8bal)
- pass8_I4_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 4 S=384 (12 KB): g20 0.819 (baseline tb8bal)
- pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): g19 0.829 (baseline tb8)
- pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): g20 0.780 (baseline tb8)
- pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): g22d4 0.770 (baseline tb8)
- pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): h20half 0.887 (baseline tb8)
- regs16_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2: g52 0.887 (baseline tb16bal)
- regs16_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2: g56d6 0.890 (baseline tb16bal)
- regs16_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 2: g52 0.887 (baseline tb16bal)
- regs16_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 2: g56d6 0.890 (baseline tb16bal)
- regs8_I4_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 4: g22d4 0.867 (baseline tb8bal)
