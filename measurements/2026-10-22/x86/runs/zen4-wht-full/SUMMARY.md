# x86-wht summary 

Figure = circuit median / fastest baseline median (textbook, pipe-balanced textbook, FFHT); < 1 is faster.

| test | baseline (ns/unit) | circuit: ratio ... |
|---|---|---|
| pass16_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16 0.0741 (tb16bal 1.259) | g52 0.776; g54d7 1.020; g56d6 1.179 |
| pass16_I1_clang_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB) | tb16 0.1489 (tb16bal 1.255) | g52 0.778; g54d7 1.058; g56d6 1.191 |
| pass16_I1_clang_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16bal 0.0603 (tb16 1.214) | g52 0.892; g54d7 0.915; g56d6 0.929 |
| pass16_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16bal 0.0648 (tb16 1.136) | g52 0.773; g54d7 0.841; g56d6 0.924 |
| pass16_I1_clang_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 1 S=96 (12 KB) | tb16bal 0.1284 (tb16 1.153) | g52 0.789; g54d7 0.846; g56d6 0.940 |
| pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16 0.0734 (tb16bal 1.151) | g52 0.718; g54d7 0.751; g56d6 0.827 |
| pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB) | tb16 0.1467 (tb16bal 1.156) | g52 0.714; g54d7 0.754; g56d6 0.823 |
| pass16_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16bal 0.0556 (tb16 1.318) | g52 0.915; g54d7 0.941; g56d6 0.959 |
| pass16_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16bal 0.0542 (tb16 1.352) | g52 0.876; g54d7 0.943; g56d6 1.031 |
| pass16_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 1 S=96 (12 KB) | tb16bal 0.1127 (tb16 1.321) | g52 0.846; g54d7 0.906; g56d6 0.996 |
| pass16_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.1055 (tb16bal 1.209) | g52 0.955; g54d7 1.041; g56d6 0.946 |
| pass16_I2_clang_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 2 S=96 (12 KB) | tb16 0.1795 (tb16bal 1.119) | g52 0.862; g54d7 1.076; g56d6 1.070 |
| pass16_I2_clang_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16bal 0.0698 (tb16 1.067) | g52 0.788; g54d7 0.928; g56d6 0.914 |
| pass16_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16bal 0.0783 (tb16 1.246) | g52 0.771; g54d7 1.008; g56d6 1.075 |
| pass16_I2_clang_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB) | tb16bal 0.1461 (tb16 1.318) | g52 0.839; g54d7 0.969; g56d6 0.985 |
| pass16_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.0825 (tb16bal 1.330) | g52 0.936; g54d7 0.928; g56d6 1.159 |
| pass16_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 2 S=96 (12 KB) | tb16 0.1653 (tb16bal 1.335) | g52 0.941; g54d7 0.943; g56d6 1.170 |
| pass16_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.0747 (tb16bal 1.150) | g52 0.681; g54d7 0.754; g56d6 1.023 |
| pass16_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.0856 (tb16bal 1.049) | g52 0.710; g54d7 0.804; g56d6 0.855 |
| pass16_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB) | tb16 0.1702 (tb16bal 1.060) | g52 0.722; g54d7 0.808; g56d6 0.857 |
| pass16_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.1016 (tb16bal 1.033) | g52 1.742; g54d7 0.962; g56d6 1.011 |
| pass16_I3_clang_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 3 S=96 (12 KB) | tb16 0.2029 (tb16bal 1.016) | g52 1.340; g54d7 0.966; g56d6 0.957 |
| pass16_I3_clang_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.0783 (tb16bal 1.041) | g52 1.637; g54d7 0.935; g56d6 0.944 |
| pass16_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16bal 0.0842 (tb16 1.248) | g52 0.885; g54d7 0.966; g56d6 0.937 |
| pass16_I3_clang_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 3 S=96 (12 KB) | tb16bal 0.1701 (tb16 1.245) | g52 0.878; g54d7 0.954; g56d6 0.929 |
| pass16_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.0777 (tb16bal 1.322) | g52 0.995; g54d7 0.871; g56d6 1.026 |
| pass16_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 3 S=96 (12 KB) | tb16 0.1551 (tb16bal 1.331) | g52 0.979; g54d7 0.868; g56d6 1.037 |
| pass16_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.0736 (tb16bal 1.058) | g52 0.842; g54d7 0.784; g56d6 0.880 |
| pass16_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.0831 (tb16bal 1.024) | g52 0.886; g54d7 0.834; g56d6 0.909 |
| pass16_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 3 S=96 (12 KB) | tb16 0.1790 (tb16bal 1.105) | g52 0.934; g54d7 0.944; g56d6 0.972 |
| pass16_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16 0.1391 (tb16bal 1.089) | g52 0.965; g54d7 1.063; g56d6 1.168 |
| pass16_I4_clang_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 4 S=96 (12 KB) | tb16 0.2770 (tb16bal 1.094) | g52 0.966; g54d7 1.067; g56d6 1.173 |
| pass16_I4_clang_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16bal 0.1368 (tb16 1.009) | g52 0.956; g54d7 0.950; g56d6 0.942 |
| pass16_I4_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16bal 0.1372 (tb16 1.087) | g52 0.921; g54d7 0.937; g56d6 0.978 |
| pass16_I4_clang_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 4 S=96 (12 KB) | tb16bal 0.2739 (tb16 1.091) | g52 0.922; g54d7 0.939; g56d6 0.980 |
| pass16_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16 0.1493 (tb16bal 1.065) | g52 0.922; g54d7 0.918; g56d6 0.940 |
| pass16_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 4 S=96 (12 KB) | tb16 0.2987 (tb16bal 1.065) | g52 0.922; g54d7 0.918; g56d6 0.941 |
| pass16_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16bal 0.1361 (tb16 1.093) | g52 1.012; g54d7 1.010; g56d6 1.004 |
| pass16_I4_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16bal 0.1403 (tb16 1.107) | g52 0.948; g54d7 0.967; g56d6 1.023 |
| pass16_I4_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 4 S=96 (12 KB) | tb16bal 0.2911 (tb16 1.092) | g52 0.946; g54d7 0.969; g56d6 1.002 |
| pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB) | tb8bal 0.0465 (tb8 1.181) | g19 0.824; g20 0.811; g22d4 0.830; h20half 1.043 |
| pass8_I1_clang_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB) | tb8bal 0.0930 (tb8 1.182) | g19 0.833; g20 0.812; g22d4 0.830; h20half 1.046 |
| pass8_I1_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB) | tb8bal 0.0464 (tb8 1.185) | g19 0.825; g20 0.812; g22d4 0.828; h20half 1.039 |
| pass8_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB) | tb8bal 0.0520 (tb8 1.056) | g19 0.756; g20 0.856; g22d4 0.917; h20half 0.894 |
| pass8_I1_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB) | tb8bal 0.1040 (tb8 1.057) | g19 0.763; g20 0.857; g22d4 0.919; h20half 0.895 |
| pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB) | tb8bal 0.0467 (tb8 1.184) | g19 0.901; g20 0.816; g22d4 0.820; h20half 0.964 |
| pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB) | tb8bal 0.0983 (tb8 1.125) | g19 0.855; g20 0.770; g22d4 0.770; h20half 0.908 |
| pass8_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB) | tb8bal 0.0479 (tb8 1.148) | g19 0.877; g20 0.793; g22d4 0.800; h20half 0.933 |
| pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB) | tb8bal 0.0514 (tb8 1.068) | g19 0.852; g20 0.866; g22d4 0.885; h20half 0.850 |
| pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB) | tb8bal 0.1029 (tb8 1.068) | g19 0.850; g20 0.859; g22d4 0.865; h20half 0.846 |
| pass8_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB) | tb8 0.0551 (tb8bal 1.163) | g19 1.372; g20 0.860; g22d4 1.042; h20half 1.356 |
| pass8_I2_clang_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB) | tb8 0.1113 (tb8bal 1.115) | g19 1.319; g20 0.828; g22d4 0.998; h20half 1.282 |
| pass8_I2_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB) | tb8bal 0.0495 (tb8 1.113) | g19 0.814; g20 0.768; g22d4 0.808; h20half 0.966 |
| pass8_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB) | tb8bal 0.0526 (tb8 1.044) | g19 0.821; g20 0.816; g22d4 0.899; h20half 0.913 |
| pass8_I2_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB) | tb8bal 0.1058 (tb8 1.039) | g19 0.817; g20 0.806; g22d4 0.890; h20half 0.910 |
| pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB) | tb8 0.0549 (tb8bal 1.131) | g19 0.834; g20 0.772; g22d4 0.825; h20half 0.871 |
| pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB) | tb8 0.1099 (tb8bal 1.132) | g19 0.829; g20 0.773; g22d4 0.820; h20half 0.863 |
| pass8_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB) | tb8bal 0.0469 (tb8 1.194) | g19 0.906; g20 0.808; g22d4 0.821; h20half 0.945 |
| pass8_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB) | tb8bal 0.0480 (tb8 1.158) | g19 0.942; g20 0.906; g22d4 0.990; h20half 0.973 |
| pass8_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB) | tb8bal 0.0951 (tb8 1.161) | g19 0.903; g20 0.850; g22d4 0.948; h20half 0.945 |
| pass8_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB) | tb8 0.0696 (tb8bal 1.109) | g19 1.142; g20 0.990; g22d4 1.102; h20half 1.093 |
| pass8_I3_clang_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 3 S=240 (15 KB) | tb8 0.1125 (tb8bal 1.100) | g19 1.147; g20 0.964; g22d4 1.076; h20half 1.056 |
| pass8_I3_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB) | tb8bal 0.0510 (tb8 1.082) | g19 0.847; g20 0.786; g22d4 0.831; h20half 0.978 |
| pass8_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB) | tb8bal 0.0550 (tb8 1.024) | g19 0.918; g20 0.900; g22d4 0.871; h20half 0.967 |
| pass8_I3_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB) | tb8bal 0.1096 (tb8 1.030) | g19 0.916; g20 0.889; g22d4 0.879; h20half 0.972 |
| pass8_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB) | tb8 0.0571 (tb8bal 1.271) | g19 0.977; g20 0.930; g22d4 0.954; h20half 1.007 |
| pass8_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 3 S=240 (15 KB) | tb8 0.1140 (tb8bal 1.276) | g19 0.964; g20 0.927; g22d4 0.954; h20half 0.999 |
| pass8_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB) | tb8bal 0.0493 (tb8 1.114) | g19 0.817; g20 0.775; g22d4 0.785; h20half 0.915 |
| pass8_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB) | tb8bal 0.0538 (tb8 1.026) | g19 0.888; g20 0.812; g22d4 0.842; h20half 0.924 |
| pass8_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB) | tb8bal 0.1074 (tb8 1.026) | g19 0.887; g20 0.811; g22d4 0.841; h20half 0.924 |
| pass8_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB) | tb8 0.0581 (tb8bal 1.117) | g19 1.155; g20 1.074; g22d4 1.126; h20half 1.091 |
| pass8_I4_clang_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 4 S=240 (15 KB) | tb8 0.1517 (tb8bal 1.059) | g19 1.156; g20 1.074; g22d4 1.118; h20half 1.107 |
| pass8_I4_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB) | tb8 0.0552 (tb8bal 1.007) | g19 0.929; g20 0.759; g22d4 0.897; h20half 0.989 |
| pass8_I4_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 4 S=384 (12 KB) | tb8bal 0.0680 (tb8 1.109) | g19 1.021; g20 0.807; g22d4 1.069; h20half 1.101 |
| pass8_I4_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 4 S=192 (12 KB) | tb8bal 0.1244 (tb8 1.204) | g19 0.986; g20 0.806; g22d4 1.009; h20half 1.098 |
| pass8_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB) | tb8 0.0584 (tb8bal 1.377) | g19 1.036; g20 1.007; g22d4 1.022; h20half 1.063 |
| pass8_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 4 S=240 (15 KB) | tb8 0.1168 (tb8bal 1.360) | g19 1.041; g20 1.009; g22d4 1.026; h20half 1.063 |
| pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB) | tb8 0.0550 (tb8bal 1.093) | g19 0.818; g20 0.775; g22d4 0.756; h20half 0.873 |
| pass8_I4_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 4 S=384 (12 KB) | tb8 0.0572 (tb8bal 1.175) | g19 1.014; g20 0.965; g22d4 0.981; h20half 1.105 |
| pass8_I4_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 4 S=192 (12 KB) | tb8 0.1127 (tb8bal 1.207) | g19 1.020; g20 0.981; g22d4 0.999; h20half 1.123 |
| regs16_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1 | tb16 10.0042 (tb16bal 1.174) | g52 1.474; g54d7 1.374; g56d6 1.929 |
| regs16_I1_clang_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 1 | tb16 10.5486 (tb16bal 1.174) | g52 1.454; g54d7 1.331; g56d6 1.854 |
| regs16_I1_clang_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 1 | tb16bal 6.0144 (tb16 1.558) | g52 1.548; g54d7 1.500; g56d6 1.543 |
| regs16_I1_clang_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 1 | tb16bal 11.4488 (tb16 1.636) | g52 1.072; g54d7 1.294; g56d6 1.173 |
| regs16_I1_clang_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 1 | tb16bal 11.4500 (tb16 1.636) | g52 1.072; g54d7 1.294; g56d6 1.173 |
| regs16_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1 | tb16bal 13.1463 (tb16 1.016) | g52 1.025; g54d7 1.078; g56d6 1.196 |
| regs16_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 1 | tb16bal 13.1513 (tb16 1.015) | g52 1.025; g54d7 1.078; g56d6 1.195 |
| regs16_I1_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 1 | tb16bal 5.9516 (tb16 1.574) | g52 1.566; g54d7 1.606; g56d6 1.564 |
| regs16_I1_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 1 | tb16bal 9.9684 (tb16 1.879) | g52 1.291; g54d7 1.572; g56d6 1.345 |
| regs16_I1_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 1 | tb16bal 9.9678 (tb16 1.879) | g52 1.291; g54d7 1.572; g56d6 1.345 |
| regs16_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2 | tb16 13.4303 (tb16bal 1.345) | g52 1.454; g54d7 1.271; g56d6 1.187 |
| regs16_I2_clang_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 2 | tb16 13.4294 (tb16bal 1.351) | g52 1.456; g54d7 1.274; g56d6 1.189 |
| regs16_I2_clang_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 2 | tb16bal 5.4426 (tb16 1.721) | g52 1.239; g54d7 1.277; g56d6 1.297 |
| regs16_I2_clang_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2 | tb16bal 12.9194 (tb16 1.450) | g52 1.282; g54d7 1.110; g56d6 1.159 |
| regs16_I2_clang_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 2 | tb16bal 12.8951 (tb16 1.453) | g52 1.284; g54d7 1.532; g56d6 1.164 |
| regs16_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2 | tb16 12.2667 (tb16bal 1.155) | g52 1.111; g54d7 1.119; g56d6 1.073 |
| regs16_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 2 | tb16 12.2586 (tb16bal 1.156) | g52 1.112; g54d7 1.121; g56d6 1.074 |
| regs16_I2_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 2 | tb16bal 6.3743 (tb16 1.470) | g52 1.143; g54d7 1.184; g56d6 1.043 |
| regs16_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2 | tb16bal 12.0716 (tb16 1.552) | g52 0.887; g54d7 0.938; g56d6 0.890 |
| regs16_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 2 | tb16bal 12.0805 (tb16 1.552) | g52 0.886; g54d7 0.937; g56d6 0.890 |
| regs8_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1 | tb8bal 3.8916 (tb8 1.047) | g19 1.732; g20 1.602; g22d4 1.314; h20half 1.740 |
| regs8_I1_clang_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 1 | tb8bal 3.8930 (tb8 1.047) | g19 1.731; g20 1.601; g22d4 1.313; h20half 1.739 |
| regs8_I1_clang_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 1 | tb8bal 3.8919 (tb8 1.047) | g19 1.732; g20 1.602; g22d4 1.314; h20half 1.739 |
| regs8_I1_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 1 | tb8bal 5.1518 (tb8 1.364) | g19 1.535; g20 1.334; g22d4 1.332; h20half 1.566 |
| regs8_I1_clang_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 1 | tb8bal 5.1531 (tb8 1.363) | g19 1.535; g20 1.334; g22d4 1.332; h20half 1.566 |
| regs8_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1 | tb8bal 3.6969 (tb8 1.027) | g19 1.758; g20 1.747; g22d4 1.309; h20half 1.677 |
| regs8_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 1 | tb8bal 3.6962 (tb8 1.028) | g19 1.759; g20 1.748; g22d4 1.309; h20half 1.679 |
| regs8_I1_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 1 | tb8bal 3.7015 (tb8 1.026) | g19 1.819; g20 1.747; g22d4 1.312; h20half 1.602 |
| regs8_I1_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 1 | tb8bal 4.6662 (tb8 1.505) | g19 1.609; g20 1.538; g22d4 1.415; h20half 1.544 |
| regs8_I1_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 1 | tb8bal 4.6662 (tb8 1.506) | g19 1.608; g20 1.538; g22d4 1.415; h20half 1.543 |
| regs8_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2 | tb8 3.5153 (tb8bal 1.376) | g19 1.519; g20 1.530; g22d4 1.543; h20half 1.527 |
| regs8_I2_clang_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 2 | tb8 3.5147 (tb8bal 1.374) | g19 1.483; g20 1.597; g22d4 1.537; h20half 1.508 |
| regs8_I2_clang_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 2 | tb8bal 2.0463 (tb8 1.717) | g19 1.696; g20 1.698; g22d4 1.350; h20half 1.987 |
| regs8_I2_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 2 | tb8bal 4.3332 (tb8 1.622) | g19 0.945; g20 1.075; g22d4 0.949; h20half 1.354 |
| regs8_I2_clang_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 2 | tb8bal 4.3327 (tb8 1.621) | g19 0.946; g20 1.075; g22d4 0.948; h20half 1.354 |
| regs8_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2 | tb8bal 3.7133 (tb8 1.061) | g19 1.373; g20 1.709; g22d4 1.468; h20half 1.402 |
| regs8_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 2 | tb8bal 3.7087 (tb8 1.063) | g19 1.376; g20 1.713; g22d4 1.496; h20half 1.407 |
| regs8_I2_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 2 | tb8bal 2.1750 (tb8 1.616) | g19 1.596; g20 1.597; g22d4 1.306; h20half 1.671 |
| regs8_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 2 | tb8bal 4.0514 (tb8 1.735) | g19 1.013; g20 1.108; g22d4 1.084; h20half 1.391 |
| regs8_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 2 | tb8bal 4.0513 (tb8 1.735) | g19 1.013; g20 1.112; g22d4 1.084; h20half 1.391 |
| regs8_I3_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3 | tb8bal 3.7578 (tb8 1.007) | g19 1.276; g20 1.331; g22d4 1.084; h20half 1.247 |
| regs8_I3_clang_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 3 | tb8bal 3.7575 (tb8 1.005) | g19 1.276; g20 1.331; g22d4 1.086; h20half 1.248 |
| regs8_I3_clang_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 3 | tb8bal 1.7862 (tb8 1.968) | g19 1.817; g20 1.310; g22d4 1.392; h20half 1.800 |
| regs8_I3_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 3 | tb8bal 3.8412 (tb8 1.829) | g19 1.090; g20 0.933; g22d4 1.092; h20half 1.521 |
| regs8_I3_clang_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 3 | tb8bal 3.8395 (tb8 1.830) | g19 1.090; g20 0.933; g22d4 1.091; h20half 1.522 |
| regs8_I3_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3 | tb8 4.5821 (tb8bal 1.114) | g19 1.162; g20 1.150; g22d4 1.059; h20half 1.097 |
| regs8_I3_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 3 | tb8 4.5815 (tb8bal 1.115) | g19 1.161; g20 1.146; g22d4 1.059; h20half 1.092 |
| regs8_I3_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 3 | tb8bal 3.1318 (tb8 1.129) | g19 1.163; g20 1.130; g22d4 1.041; h20half 1.253 |
| regs8_I3_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 3 | tb8bal 6.0789 (tb8 1.175) | g19 0.987; g20 0.949; g22d4 0.968; h20half 1.017 |
| regs8_I3_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 3 | tb8bal 6.0826 (tb8 1.174) | g19 0.986; g20 0.944; g22d4 0.961; h20half 1.027 |
| regs8_I4_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4 | tb8 3.6516 (tb8bal 1.087) | g19 1.367; g20 1.252; g22d4 1.036; h20half 1.128 |
| regs8_I4_clang_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 4 | tb8 3.6458 (tb8bal 1.079) | g19 1.368; g20 1.254; g22d4 1.037; h20half 1.129 |
| regs8_I4_clang_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 4 | tb8bal 2.3844 (tb8 1.474) | g19 3.841; g20 1.067; g22d4 1.098; h20half 1.274 |
| regs8_I4_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 4 | tb8bal 3.8538 (tb8 1.823) | g19 1.048; g20 0.974; g22d4 1.064; h20half 1.498 |
| regs8_I4_clang_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 4 | tb8bal 6.5713 (tb8 1.069) | g19 1.246; g20 1.033; g22d4 0.996; h20half 1.061 |
| regs8_I4_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4 | tb8 5.2456 (tb8bal 1.111) | g19 1.039; g20 1.003; g22d4 1.018; h20half 1.061 |
| regs8_I4_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 4 | tb8 5.2463 (tb8bal 1.111) | g19 1.039; g20 1.003; g22d4 1.018; h20half 1.062 |
| regs8_I4_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 4 | tb8bal 3.4522 (tb8 1.028) | g19 0.993; g20 1.000; g22d4 0.866; h20half 1.029 |
| regs8_I4_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 4 | tb8 8.0560 (tb8bal 1.122) | g19 1.005; g20 0.975; g22d4 0.937; h20half 1.094 |
| regs8_I4_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 4 | tb8 8.0648 (tb8bal 1.124) | g19 1.002; g20 0.972; g22d4 0.933; h20half 1.084 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^6 same I=2 | FFHT 0.2931 (textbook 1.814, textbook-bal 2.128) | g52+tb8 2.139; g56d6+tb8 2.437; g52+g19 2.435; g56d6+g22d4 3.031 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^7 same I=2 | FFHT 0.3097 (textbook 1.152, textbook-bal 1.305) | g52+tb8 1.251; g56d6+tb8 1.366; g52+g19 1.334; g56d6+g22d4 1.646 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^8 same I=2 | FFHT 0.3026 (textbook 1.167, textbook-bal 1.256) | g52+tb8 1.202; g56d6+tb8 1.319; g52+g19 1.247; g56d6+g22d4 1.379 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^9 same I=2 | FFHT 0.3077 (textbook 1.070, textbook-bal 1.153) | g52+tb8 1.113; g56d6+tb8 1.205; g52+g19 1.129; g56d6+g22d4 1.232 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^10 same I=2 | textbook 0.3489 (textbook-bal 1.058, FFHT 1.112) | g52+tb8 1.009; g56d6+tb8 1.082; g52+g19 1.049; g56d6+g22d4 1.083 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^11 same I=2 | FFHT 0.3443 (textbook 1.099, textbook-bal 1.268) | g52+tb8 1.144; g56d6+tb8 1.203; g52+g19 1.147; g56d6+g22d4 1.223 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^12 same I=2 | FFHT 0.3598 (textbook 1.222, textbook-bal 1.311) | g52+tb8 1.218; g56d6+tb8 1.234; g52+g19 1.212; g56d6+g22d4 1.222 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^13 same I=2 | FFHT 0.3848 (textbook 1.138, textbook-bal 1.229) | g52+tb8 1.118; g56d6+tb8 1.257; g52+g19 1.111; g56d6+g22d4 1.156 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^14 same I=2 | FFHT 0.4007 (textbook 1.170, textbook-bal 1.345) | g52+tb8 1.184; g56d6+tb8 1.223; g52+g19 1.179; g56d6+g22d4 1.219 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^15 same I=2 | FFHT 0.4342 (textbook 1.058, textbook-bal 1.201) | g52+tb8 1.079; g56d6+tb8 1.128; g52+g19 1.081; g56d6+g22d4 1.115 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^16 same I=2 | textbook 0.4855 (textbook-bal 1.125, FFHT 1.558) | g52+tb8 1.011; g56d6+tb8 1.058; g52+g19 1.048; g56d6+g22d4 1.066 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^17 same I=2 | FFHT 0.4582 (textbook 1.143, textbook-bal 1.289) | g52+tb8 1.353; g56d6+tb8 1.212; g52+g19 1.195; g56d6+g22d4 1.225 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^18 same I=2 | FFHT 0.4768 (textbook 1.230, textbook-bal 1.249) | g52+tb8 1.146; g56d6+tb8 1.199; g52+g19 1.172; g56d6+g22d4 1.186 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^19 same I=2 | FFHT 0.5149 (textbook 1.110, textbook-bal 1.244) | g52+tb8 1.128; g56d6+tb8 1.161; g52+g19 1.180; g56d6+g22d4 1.187 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^20 same I=2 | FFHT 0.5302 (textbook 1.167, textbook-bal 1.297) | g52+tb8 1.187; g56d6+tb8 1.224; g52+g19 1.242; g56d6+g22d4 1.243 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^21 same I=2 | FFHT 0.5822 (textbook 1.068, textbook-bal 1.189) | g52+tb8 1.085; g56d6+tb8 1.125; g52+g19 1.135; g56d6+g22d4 1.132 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^22 same I=2 | FFHT 0.5896 (textbook 1.122, textbook-bal 1.256) | g52+tb8 1.137; g56d6+tb8 1.179; g52+g19 1.233; g56d6+g22d4 1.200 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^23 same I=2 | FFHT 0.6845 (textbook 1.228, textbook-bal 1.318) | g52+tb8 1.226; g56d6+tb8 1.251; g52+g19 1.282; g56d6+g22d4 1.275 |
| whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^24 same I=2 | FFHT 0.7303 (textbook 1.326, textbook-bal 1.402) | g52+tb8 1.328; g56d6+tb8 1.343; g52+g19 1.351; g56d6+g22d4 1.361 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^6 same I=2 | FFHT 0.4913 (textbook 1.295, textbook-bal 1.510) | g52+tb8 1.481; g56d6+tb8 1.659; g52+g19 1.648; g56d6+g22d4 1.994 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^7 same I=2 | FFHT 0.4536 (textbook 1.359, textbook-bal 1.537) | g52+tb8 1.425; g56d6+tb8 1.557; g52+g19 1.498; g56d6+g22d4 1.741 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^8 same I=2 | FFHT 0.4788 (textbook 1.104, textbook-bal 1.228) | g52+tb8 1.154; g56d6+tb8 1.278; g52+g19 1.175; g56d6+g22d4 1.343 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^9 same I=2 | FFHT 0.5462 (textbook 1.045, textbook-bal 1.503) | g52+tb8 1.070; g56d6+tb8 1.156; g52+g19 1.467; g56d6+g22d4 1.155 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^10 same I=2 | FFHT 0.5413 (textbook 1.123, textbook-bal 1.261) | g52+tb8 1.109; g56d6+tb8 1.249; g52+g19 1.112; g56d6+g22d4 1.263 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^11 same I=2 | FFHT 0.5732 (textbook 1.189, textbook-bal 1.301) | g52+tb8 1.189; g56d6+tb8 1.323; g52+g19 1.188; g56d6+g22d4 1.320 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^12 same I=2 | FFHT 0.6464 (textbook 1.069, textbook-bal 1.185) | g52+tb8 1.067; g56d6+tb8 1.166; g52+g19 1.099; g56d6+g22d4 1.177 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^13 same I=2 | FFHT 0.6549 (textbook 1.193, textbook-bal 1.287) | g52+tb8 1.196; g56d6+tb8 1.283; g52+g19 1.179; g56d6+g22d4 1.282 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^14 same I=2 | FFHT 0.7236 (textbook 1.074, textbook-bal 1.173) | g52+tb8 1.064; g56d6+tb8 1.149; g52+g19 1.053; g56d6+g22d4 1.156 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^15 same I=2 | FFHT 0.7550 (textbook 1.086, textbook-bal 1.516) | g52+tb8 1.088; g56d6+tb8 1.179; g52+g19 1.421; g56d6+g22d4 1.185 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^16 same I=2 | FFHT 0.7692 (textbook 1.180, textbook-bal 1.582) | g52+tb8 1.168; g56d6+tb8 1.257; g52+g19 1.502; g56d6+g22d4 1.265 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^17 same I=2 | FFHT 0.8057 (textbook 1.145, textbook-bal 1.531) | g52+tb8 1.161; g56d6+tb8 1.241; g52+g19 1.461; g56d6+g22d4 1.237 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^18 same I=2 | FFHT 0.8882 (textbook 1.127, textbook-bal 1.738) | g52+tb8 1.119; g56d6+tb8 1.200; g52+g19 1.671; g56d6+g22d4 1.208 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^19 same I=2 | FFHT 0.9272 (textbook 1.193, textbook-bal 1.775) | g52+tb8 1.189; g56d6+tb8 1.255; g52+g19 1.713; g56d6+g22d4 1.268 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^20 same I=2 | textbook 1.1124 (textbook-bal 1.477, FFHT 1.027) | g52+tb8 0.992; g56d6+tb8 1.051; g52+g19 1.427; g56d6+g22d4 1.057 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^21 same I=2 | FFHT 1.0769 (textbook 1.095, textbook-bal 1.812) | g52+tb8 1.091; g56d6+tb8 1.154; g52+g19 1.771; g56d6+g22d4 1.169 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^22 same I=2 | FFHT 1.1653 (textbook 1.305, textbook-bal 1.855) | g52+tb8 1.304; g56d6+tb8 1.367; g52+g19 1.820; g56d6+g22d4 1.354 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^23 same I=2 | FFHT 1.3094 (textbook 1.373, textbook-bal 1.741) | g52+tb8 1.371; g56d6+tb8 1.410; g52+g19 1.701; g56d6+g22d4 1.415 |
| whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^24 same I=2 | FFHT 1.4738 (textbook 1.370, textbook-bal 1.709) | g52+tb8 1.355; g56d6+tb8 1.411; g52+g19 1.681; g56d6+g22d4 1.433 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^6 same I=2 | FFHT 0.2930 (textbook 1.782, textbook-bal 2.156) | g52+tb8 2.048; g56d6+tb8 2.360; g52+g19 2.394; g56d6+g22d4 3.013 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^7 same I=2 | FFHT 0.3093 (textbook 1.156, textbook-bal 1.265) | g52+tb8 1.232; g56d6+tb8 1.345; g52+g19 1.326; g56d6+g22d4 1.632 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^8 same I=2 | FFHT 0.2990 (textbook 1.182, textbook-bal 1.262) | g52+tb8 1.203; g56d6+tb8 1.282; g52+g19 1.264; g56d6+g22d4 1.429 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^9 same I=2 | FFHT 0.3078 (textbook 1.061, textbook-bal 1.104) | g52+tb8 1.094; g56d6+tb8 1.091; g52+g19 1.114; g56d6+g22d4 1.129 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^10 same I=2 | textbook 0.3323 (textbook-bal 1.031, FFHT 1.046) | g52+tb8 1.014; g56d6+tb8 1.011; g52+g19 1.000; g56d6+g22d4 1.016 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^11 same I=2 | FFHT 0.3446 (textbook 1.015, textbook-bal 1.029) | g52+tb8 0.985; g56d6+tb8 0.993; g52+g19 0.991; g56d6+g22d4 1.000 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^12 same I=2 | FFHT 0.3605 (textbook 1.069, textbook-bal 1.088) | g52+tb8 1.023; g56d6+tb8 1.048; g52+g19 1.027; g56d6+g22d4 1.053 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^13 same I=2 | FFHT 0.3860 (textbook 1.006, textbook-bal 1.023) | g52+tb8 0.978; g56d6+tb8 0.997; g52+g19 0.992; g56d6+g22d4 1.006 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^14 same I=2 | FFHT 0.4015 (textbook 1.073, textbook-bal 1.090) | g52+tb8 1.037; g56d6+tb8 1.065; g52+g19 1.051; g56d6+g22d4 1.067 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^15 same I=2 | textbook 0.4274 (textbook-bal 1.022, FFHT 1.019) | g52+tb8 0.966; g56d6+tb8 0.995; g52+g19 0.972; g56d6+g22d4 0.994 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^16 same I=2 | textbook 0.4433 (textbook-bal 1.015, FFHT 1.021) | g52+tb8 0.977; g56d6+tb8 0.997; g52+g19 0.976; g56d6+g22d4 0.992 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^17 same I=2 | FFHT 0.4588 (textbook 1.052, textbook-bal 1.070) | g52+tb8 1.022; g56d6+tb8 1.045; g52+g19 1.030; g56d6+g22d4 1.048 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^18 same I=2 | FFHT 0.4819 (textbook 1.021, textbook-bal 1.056) | g52+tb8 1.008; g56d6+tb8 1.017; g52+g19 1.011; g56d6+g22d4 1.021 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^19 same I=2 | textbook 0.5162 (textbook-bal 1.030, FFHT 1.014) | g52+tb8 0.976; g56d6+tb8 0.995; g52+g19 0.998; g56d6+g22d4 1.010 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^20 same I=2 | FFHT 0.5409 (textbook 1.040, textbook-bal 1.075) | g52+tb8 1.029; g56d6+tb8 1.033; g52+g19 1.040; g56d6+g22d4 1.048 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^21 same I=2 | textbook 0.5673 (textbook-bal 1.026, FFHT 1.035) | g52+tb8 0.984; g56d6+tb8 0.986; g52+g19 0.986; g56d6+g22d4 1.007 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^22 same I=2 | textbook 0.5903 (textbook-bal 1.035, FFHT 1.000) | g52+tb8 0.996; g56d6+tb8 1.023; g52+g19 1.001; g56d6+g22d4 1.010 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^23 same I=2 | FFHT 0.6861 (textbook 1.150, textbook-bal 1.151) | g52+tb8 1.129; g56d6+tb8 1.142; g52+g19 1.127; g56d6+g22d4 1.138 |
| whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^24 same I=2 | FFHT 0.7188 (textbook 1.286, textbook-bal 1.297) | g52+tb8 1.270; g56d6+tb8 1.277; g52+g19 1.248; g56d6+g22d4 1.267 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^6 same I=2 | FFHT 0.2932 (textbook 1.703, textbook-bal 1.982) | g52+tb8 2.014; g56d6+tb8 2.311; g52+g19 2.329; g56d6+g22d4 2.947 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^7 same I=2 | FFHT 0.3157 (textbook 1.082, textbook-bal 1.125) | g52+tb8 1.190; g56d6+tb8 1.219; g52+g19 1.243; g56d6+g22d4 1.501 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^8 same I=2 | textbook 0.2962 (textbook-bal 1.035, FFHT 1.007) | g52+tb8 1.072; g56d6+tb8 1.085; g52+g19 1.090; g56d6+g22d4 1.377 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^9 same I=2 | FFHT 0.3077 (textbook 1.066, textbook-bal 1.040) | g52+tb8 1.077; g56d6+tb8 1.064; g52+g19 1.077; g56d6+g22d4 1.101 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^10 same I=2 | textbook-bal 0.3059 (textbook 1.041, FFHT 1.135) | g52+tb8 1.023; g56d6+tb8 1.020; g52+g19 1.027; g56d6+g22d4 1.035 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^11 same I=2 | textbook-bal 0.3140 (textbook 1.032, FFHT 1.095) | g52+tb8 1.018; g56d6+tb8 1.018; g52+g19 1.010; g56d6+g22d4 1.009 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^12 same I=2 | textbook-bal 0.3335 (textbook 1.089, FFHT 1.079) | g52+tb8 0.966; g56d6+tb8 1.010; g52+g19 0.986; g56d6+g22d4 1.009 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^13 same I=2 | textbook-bal 0.3773 (textbook 1.074, FFHT 1.020) | g52+tb8 0.968; g56d6+tb8 0.999; g52+g19 0.968; g56d6+g22d4 0.999 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^14 same I=2 | FFHT 0.4009 (textbook 1.118, textbook-bal 1.037) | g52+tb8 1.017; g56d6+tb8 1.044; g52+g19 1.020; g56d6+g22d4 1.042 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^15 same I=2 | textbook-bal 0.4120 (textbook 1.075, FFHT 1.054) | g52+tb8 0.976; g56d6+tb8 1.009; g52+g19 0.976; g56d6+g22d4 1.006 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^16 same I=2 | textbook-bal 0.4254 (textbook 1.079, FFHT 1.059) | g52+tb8 0.984; g56d6+tb8 1.025; g52+g19 0.969; g56d6+g22d4 0.999 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^17 same I=2 | FFHT 0.4576 (textbook 1.088, textbook-bal 1.018) | g52+tb8 1.001; g56d6+tb8 1.034; g52+g19 0.985; g56d6+g22d4 1.018 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^18 same I=2 | FFHT 0.4776 (textbook 1.077, textbook-bal 1.004) | g52+tb8 0.973; g56d6+tb8 0.999; g52+g19 0.974; g56d6+g22d4 1.022 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^19 same I=2 | textbook-bal 0.5075 (textbook 1.039, FFHT 1.106) | g52+tb8 0.966; g56d6+tb8 0.984; g52+g19 0.973; g56d6+g22d4 1.004 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^20 same I=2 | FFHT 0.5314 (textbook 1.081, textbook-bal 1.043) | g52+tb8 1.022; g56d6+tb8 1.032; g52+g19 1.016; g56d6+g22d4 1.045 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^21 same I=2 | textbook-bal 0.5562 (textbook 1.046, FFHT 1.052) | g52+tb8 0.967; g56d6+tb8 0.990; g52+g19 0.977; g56d6+g22d4 1.003 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^22 same I=2 | textbook-bal 0.5817 (textbook 1.032, FFHT 1.013) | g52+tb8 0.964; g56d6+tb8 0.993; g52+g19 0.973; g56d6+g22d4 1.011 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^23 same I=2 | FFHT 0.6891 (textbook 1.146, textbook-bal 1.108) | g52+tb8 1.084; g56d6+tb8 1.109; g52+g19 1.093; g56d6+g22d4 1.105 |
| whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^24 same I=2 | FFHT 0.7214 (textbook 1.279, textbook-bal 1.232) | g52+tb8 1.222; g56d6+tb8 1.233; g52+g19 1.213; g56d6+g22d4 1.223 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^6 same I=2 | FFHT 0.4961 (textbook 1.088, textbook-bal 1.275) | g52+tb8 1.258; g56d6+tb8 1.428; g52+g19 1.418; g56d6+g22d4 1.764 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^7 same I=2 | FFHT 0.4548 (textbook 1.097, textbook-bal 1.102) | g52+tb8 1.126; g56d6+tb8 1.166; g52+g19 1.178; g56d6+g22d4 1.253 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^8 same I=2 | FFHT 0.4716 (textbook 1.170, textbook-bal 1.148) | g52+tb8 1.164; g56d6+tb8 1.176; g52+g19 1.190; g56d6+g22d4 1.214 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^9 same I=2 | textbook-bal 0.5140 (textbook 1.038, FFHT 1.065) | g52+tb8 1.017; g56d6+tb8 1.019; g52+g19 1.029; g56d6+g22d4 1.040 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^10 same I=2 | textbook-bal 0.5313 (textbook 1.043, FFHT 1.018) | g52+tb8 1.025; g56d6+tb8 1.019; g52+g19 0.991; g56d6+g22d4 1.008 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^11 same I=2 | textbook-bal 0.5634 (textbook 1.122, FFHT 1.017) | g52+tb8 0.973; g56d6+tb8 1.018; g52+g19 0.974; g56d6+g22d4 1.084 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^12 same I=2 | FFHT 0.6472 (textbook 1.102, textbook-bal 1.009) | g52+tb8 0.993; g56d6+tb8 1.036; g52+g19 0.978; g56d6+g22d4 1.041 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^13 same I=2 | FFHT 0.6553 (textbook 1.226, textbook-bal 1.127) | g52+tb8 1.096; g56d6+tb8 1.137; g52+g19 1.099; g56d6+g22d4 1.138 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^14 same I=2 | FFHT 0.7248 (textbook 1.091, textbook-bal 1.005) | g52+tb8 0.980; g56d6+tb8 1.011; g52+g19 0.991; g56d6+g22d4 1.018 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^15 same I=2 | FFHT 0.7543 (textbook 1.089, textbook-bal 1.004) | g52+tb8 0.983; g56d6+tb8 1.020; g52+g19 0.966; g56d6+g22d4 1.003 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^16 same I=2 | FFHT 0.7696 (textbook 1.170, textbook-bal 1.082) | g52+tb8 1.074; g56d6+tb8 1.106; g52+g19 1.055; g56d6+g22d4 1.089 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^17 same I=2 | FFHT 0.8156 (textbook 1.124, textbook-bal 1.054) | g52+tb8 1.046; g56d6+tb8 1.068; g52+g19 1.047; g56d6+g22d4 1.063 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^18 same I=2 | FFHT 0.8875 (textbook 1.087, textbook-bal 1.030) | g52+tb8 0.993; g56d6+tb8 1.024; g52+g19 1.014; g56d6+g22d4 1.040 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^19 same I=2 | FFHT 0.9131 (textbook 1.156, textbook-bal 1.111) | g52+tb8 1.073; g56d6+tb8 1.099; g52+g19 1.080; g56d6+g22d4 1.127 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^20 same I=2 | textbook-bal 1.0167 (textbook 1.043, FFHT 1.123) | g52+tb8 0.977; g56d6+tb8 0.992; g52+g19 0.972; g56d6+g22d4 0.998 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^21 same I=2 | FFHT 1.0744 (textbook 1.053, textbook-bal 1.009) | g52+tb8 0.957; g56d6+tb8 0.982; g52+g19 0.967; g56d6+g22d4 0.999 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^22 same I=2 | FFHT 1.1686 (textbook 1.317, textbook-bal 1.272) | g52+tb8 1.258; g56d6+tb8 1.284; g52+g19 1.259; g56d6+g22d4 1.273 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^23 same I=2 | FFHT 1.3307 (textbook 1.341, textbook-bal 1.304) | g52+tb8 1.294; g56d6+tb8 1.307; g52+g19 1.297; g56d6+g22d4 1.296 |
| whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^24 same I=2 | FFHT 1.4982 (textbook 1.310, textbook-bal 1.269) | g52+tb8 1.246; g56d6+tb8 1.262; g52+g19 1.251; g56d6+g22d4 1.273 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^6 same I=2 | FFHT 0.2929 (textbook 1.875, textbook-bal 2.281) | g52+tb8 2.187; g56d6+tb8 2.485; g52+g19 2.531; g56d6+g22d4 3.124 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^7 same I=2 | FFHT 0.3112 (textbook 1.397, textbook-bal 1.345) | g52+tb8 1.270; g56d6+tb8 1.413; g52+g19 1.406; g56d6+g22d4 1.693 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^8 same I=2 | FFHT 0.2982 (textbook 1.151, textbook-bal 1.307) | g52+tb8 1.220; g56d6+tb8 1.307; g52+g19 1.284; g56d6+g22d4 1.452 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^9 same I=2 | FFHT 0.3076 (textbook 1.005, textbook-bal 1.107) | g52+tb8 1.008; g56d6+tb8 1.045; g52+g19 1.044; g56d6+g22d4 1.121 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^10 same I=2 | textbook 0.3109 (textbook-bal 1.129, FFHT 1.087) | g52+tb8 1.006; g56d6+tb8 1.016; g52+g19 0.970; g56d6+g22d4 1.018 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^11 same I=2 | FFHT 0.3441 (textbook 1.054, textbook-bal 1.118) | g52+tb8 0.926; g56d6+tb8 1.027; g52+g19 0.931; g56d6+g22d4 1.022 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^12 same I=2 | FFHT 0.3592 (textbook 1.034, textbook-bal 1.161) | g52+tb8 0.979; g56d6+tb8 1.086; g52+g19 0.982; g56d6+g22d4 1.074 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^13 same I=2 | textbook 0.3719 (textbook-bal 1.135, FFHT 1.023) | g52+tb8 0.967; g56d6+tb8 1.042; g52+g19 0.958; g56d6+g22d4 1.036 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^14 same I=2 | FFHT 0.4014 (textbook 1.040, textbook-bal 1.158) | g52+tb8 0.999; g56d6+tb8 1.068; g52+g19 0.995; g56d6+g22d4 1.064 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^15 same I=2 | textbook 0.4115 (textbook-bal 1.122, FFHT 1.056) | g52+tb8 0.965; g56d6+tb8 1.026; g52+g19 0.977; g56d6+g22d4 1.028 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^16 same I=2 | textbook 0.4297 (textbook-bal 1.181, FFHT 1.047) | g52+tb8 0.966; g56d6+tb8 1.027; g52+g19 0.978; g56d6+g22d4 1.060 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^17 same I=2 | FFHT 0.4619 (textbook 1.025, textbook-bal 1.177) | g52+tb8 0.992; g56d6+tb8 1.042; g52+g19 1.002; g56d6+g22d4 1.052 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^18 same I=2 | textbook 0.4812 (textbook-bal 1.144, FFHT 1.002) | g52+tb8 0.977; g56d6+tb8 1.023; g52+g19 0.998; g56d6+g22d4 1.028 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^19 same I=2 | textbook 0.5106 (textbook-bal 1.179, FFHT 1.006) | g52+tb8 0.977; g56d6+tb8 1.020; g52+g19 0.999; g56d6+g22d4 1.049 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^20 same I=2 | FFHT 0.5330 (textbook 1.053, textbook-bal 1.220) | g52+tb8 1.025; g56d6+tb8 1.071; g52+g19 1.071; g56d6+g22d4 1.101 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^21 same I=2 | FFHT 0.5458 (textbook 1.032, textbook-bal 1.207) | g52+tb8 1.010; g56d6+tb8 1.056; g52+g19 1.025; g56d6+g22d4 1.085 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^22 same I=2 | FFHT 0.5869 (textbook 1.015, textbook-bal 1.196) | g52+tb8 0.993; g56d6+tb8 1.028; g52+g19 1.016; g56d6+g22d4 1.062 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^23 same I=2 | FFHT 0.6470 (textbook 1.217, textbook-bal 1.332) | g52+tb8 1.194; g56d6+tb8 1.213; g52+g19 1.186; g56d6+g22d4 1.226 |
| whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^24 same I=2 | FFHT 0.7277 (textbook 1.257, textbook-bal 1.358) | g52+tb8 1.244; g56d6+tb8 1.287; g52+g19 1.250; g56d6+g22d4 1.292 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^6 same I=2 | FFHT 0.4931 (textbook 1.229, textbook-bal 1.482) | g52+tb8 1.420; g56d6+tb8 1.606; g52+g19 1.587; g56d6+g22d4 1.951 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^7 same I=2 | FFHT 0.4531 (textbook 1.309, textbook-bal 1.487) | g52+tb8 1.325; g56d6+tb8 1.448; g52+g19 1.499; g56d6+g22d4 1.634 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^8 same I=2 | FFHT 0.4725 (textbook 1.033, textbook-bal 1.195) | g52+tb8 1.039; g56d6+tb8 1.119; g52+g19 1.080; g56d6+g22d4 1.160 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^9 same I=2 | textbook 0.5000 (textbook-bal 1.148, FFHT 1.068) | g52+tb8 0.977; g56d6+tb8 1.025; g52+g19 1.038; g56d6+g22d4 1.019 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^10 same I=2 | FFHT 0.5403 (textbook 1.029, textbook-bal 1.204) | g52+tb8 0.963; g56d6+tb8 1.065; g52+g19 0.992; g56d6+g22d4 1.079 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^11 same I=2 | FFHT 0.5720 (textbook 1.087, textbook-bal 1.255) | g52+tb8 1.023; g56d6+tb8 1.144; g52+g19 1.028; g56d6+g22d4 1.124 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^12 same I=2 | textbook 0.6248 (textbook-bal 1.159, FFHT 1.035) | g52+tb8 0.959; g56d6+tb8 1.041; g52+g19 0.974; g56d6+g22d4 1.039 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^13 same I=2 | FFHT 0.6565 (textbook 1.078, textbook-bal 1.229) | g52+tb8 1.037; g56d6+tb8 1.117; g52+g19 1.048; g56d6+g22d4 1.117 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^14 same I=2 | textbook 0.6987 (textbook-bal 1.145, FFHT 1.036) | g52+tb8 0.965; g56d6+tb8 1.041; g52+g19 0.965; g56d6+g22d4 1.056 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^15 same I=2 | textbook 0.7355 (textbook-bal 1.214, FFHT 1.025) | g52+tb8 0.970; g56d6+tb8 1.038; g52+g19 0.981; g56d6+g22d4 1.052 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^16 same I=2 | FFHT 0.7683 (textbook 1.064, textbook-bal 1.255) | g52+tb8 1.037; g56d6+tb8 1.097; g52+g19 1.047; g56d6+g22d4 1.111 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^17 same I=2 | FFHT 0.8064 (textbook 1.055, textbook-bal 1.224) | g52+tb8 1.029; g56d6+tb8 1.096; g52+g19 1.034; g56d6+g22d4 1.084 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^18 same I=2 | textbook 0.9022 (textbook-bal 1.207, FFHT 1.068) | g52+tb8 0.966; g56d6+tb8 1.028; g52+g19 0.993; g56d6+g22d4 1.058 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^19 same I=2 | FFHT 0.9169 (textbook 1.080, textbook-bal 1.299) | g52+tb8 1.088; g56d6+tb8 1.117; g52+g19 1.077; g56d6+g22d4 1.146 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^20 same I=2 | FFHT 0.9990 (textbook 1.011, textbook-bal 1.202) | g52+tb8 0.975; g56d6+tb8 1.029; g52+g19 1.018; g56d6+g22d4 1.056 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^21 same I=2 | FFHT 1.0457 (textbook 1.032, textbook-bal 1.267) | g52+tb8 1.014; g56d6+tb8 1.043; g52+g19 1.049; g56d6+g22d4 1.114 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^22 same I=2 | FFHT 1.1547 (textbook 1.280, textbook-bal 1.491) | g52+tb8 1.261; g56d6+tb8 1.309; g52+g19 1.270; g56d6+g22d4 1.359 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^23 same I=2 | FFHT 1.3096 (textbook 1.328, textbook-bal 1.508) | g52+tb8 1.299; g56d6+tb8 1.341; g52+g19 1.322; g56d6+g22d4 1.378 |
| whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^24 same I=2 | FFHT 1.4839 (textbook 1.314, textbook-bal 1.544) | g52+tb8 1.326; g56d6+tb8 1.365; g52+g19 1.328; g56d6+g22d4 1.374 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^6 same I=2 | FFHT 0.2930 (textbook 1.713, textbook-bal 1.999) | g52+tb8 1.983; g56d6+tb8 2.231; g52+g19 2.280; g56d6+g22d4 2.858 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^7 same I=2 | FFHT 0.3104 (textbook 1.119, textbook-bal 1.217) | g52+tb8 1.254; g56d6+tb8 1.276; g52+g19 1.300; g56d6+g22d4 1.545 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^8 same I=2 | FFHT 0.2981 (textbook 1.133, textbook-bal 1.174) | g52+tb8 1.415; g56d6+tb8 1.177; g52+g19 1.488; g56d6+g22d4 1.282 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^9 same I=2 | textbook 0.3032 (textbook-bal 1.057, FFHT 1.016) | g52+tb8 1.150; g56d6+tb8 1.011; g52+g19 1.165; g56d6+g22d4 1.043 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^10 same I=2 | textbook 0.3087 (textbook-bal 1.007, FFHT 1.095) | g52+tb8 1.043; g56d6+tb8 0.983; g52+g19 1.020; g56d6+g22d4 0.961 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^11 same I=2 | textbook 0.3253 (textbook-bal 1.044, FFHT 1.057) | g52+tb8 0.926; g56d6+tb8 0.974; g52+g19 0.927; g56d6+g22d4 0.978 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^12 same I=2 | textbook 0.3589 (textbook-bal 1.036, FFHT 1.001) | g52+tb8 0.919; g56d6+tb8 0.976; g52+g19 0.922; g56d6+g22d4 0.982 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^13 same I=2 | textbook 0.3586 (textbook-bal 1.052, FFHT 1.061) | g52+tb8 0.923; g56d6+tb8 0.974; g52+g19 0.918; g56d6+g22d4 0.977 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^14 same I=2 | FFHT 0.4014 (textbook 1.001, textbook-bal 1.045) | g52+tb8 0.939; g56d6+tb8 0.985; g52+g19 0.923; g56d6+g22d4 0.981 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^15 same I=2 | textbook 0.3999 (textbook-bal 1.040, FFHT 1.087) | g52+tb8 0.926; g56d6+tb8 0.972; g52+g19 0.925; g56d6+g22d4 0.974 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^16 same I=2 | textbook 0.4139 (textbook-bal 1.043, FFHT 1.086) | g52+tb8 0.924; g56d6+tb8 0.979; g52+g19 0.914; g56d6+g22d4 0.965 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^17 same I=2 | textbook 0.4531 (textbook-bal 1.075, FFHT 1.010) | g52+tb8 0.933; g56d6+tb8 0.980; g52+g19 0.925; g56d6+g22d4 0.970 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^18 same I=2 | textbook 0.4701 (textbook-bal 1.041, FFHT 1.025) | g52+tb8 0.938; g56d6+tb8 0.981; g52+g19 0.913; g56d6+g22d4 0.988 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^19 same I=2 | textbook 0.4875 (textbook-bal 1.054, FFHT 1.051) | g52+tb8 0.937; g56d6+tb8 0.979; g52+g19 0.927; g56d6+g22d4 0.975 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^20 same I=2 | FFHT 0.5303 (textbook 1.009, textbook-bal 1.054) | g52+tb8 0.948; g56d6+tb8 0.990; g52+g19 0.934; g56d6+g22d4 1.028 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^21 same I=2 | textbook 0.5377 (textbook-bal 1.045, FFHT 1.020) | g52+tb8 0.950; g56d6+tb8 0.984; g52+g19 0.942; g56d6+g22d4 0.984 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^22 same I=2 | textbook 0.5632 (textbook-bal 1.059, FFHT 1.037) | g52+tb8 0.941; g56d6+tb8 0.976; g52+g19 0.958; g56d6+g22d4 0.977 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^23 same I=2 | FFHT 0.6568 (textbook 1.157, textbook-bal 1.207) | g52+tb8 1.118; g56d6+tb8 1.141; g52+g19 1.086; g56d6+g22d4 1.127 |
| whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^24 same I=2 | FFHT 0.7232 (textbook 1.225, textbook-bal 1.261) | g52+tb8 1.166; g56d6+tb8 1.207; g52+g19 1.180; g56d6+g22d4 1.233 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^6 same I=2 | FFHT 0.3062 (textbook 1.665, textbook-bal 1.830) | g52+tb8 2.529; g56d6+tb8 2.020; g52+g19 2.018; g56d6+g22d4 2.586 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^7 same I=2 | FFHT 0.3102 (textbook 1.264, textbook-bal 1.352) | g52+tb8 1.332; g56d6+tb8 1.400; g52+g19 1.449; g56d6+g22d4 1.549 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^8 same I=2 | FFHT 0.2979 (textbook 1.130, textbook-bal 1.131) | g52+tb8 1.239; g56d6+tb8 1.187; g52+g19 1.186; g56d6+g22d4 1.254 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^9 same I=2 | FFHT 0.3070 (textbook 1.127, textbook-bal 1.097) | g52+tb8 1.141; g56d6+tb8 1.120; g52+g19 1.106; g56d6+g22d4 1.146 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^10 same I=2 | textbook-bal 0.3229 (textbook 1.020, FFHT 1.046) | g52+tb8 0.981; g56d6+tb8 0.996; g52+g19 0.988; g56d6+g22d4 1.032 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^11 same I=2 | textbook-bal 0.3167 (textbook 1.069, FFHT 1.084) | g52+tb8 1.024; g56d6+tb8 1.020; g52+g19 0.991; g56d6+g22d4 0.997 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^12 same I=2 | textbook-bal 0.3535 (textbook 1.027, FFHT 1.015) | g52+tb8 0.910; g56d6+tb8 0.947; g52+g19 0.911; g56d6+g22d4 0.952 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^13 same I=2 | FFHT 0.3809 (textbook 1.052, textbook-bal 1.039) | g52+tb8 0.955; g56d6+tb8 0.983; g52+g19 0.957; g56d6+g22d4 0.985 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^14 same I=2 | FFHT 0.4012 (textbook 1.103, textbook-bal 1.090) | g52+tb8 1.022; g56d6+tb8 1.049; g52+g19 1.010; g56d6+g22d4 1.041 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^15 same I=2 | FFHT 0.4341 (textbook 1.015, textbook-bal 1.015) | g52+tb8 0.928; g56d6+tb8 0.956; g52+g19 0.930; g56d6+g22d4 0.959 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^16 same I=2 | FFHT 0.4491 (textbook 1.011, textbook-bal 1.010) | g52+tb8 0.928; g56d6+tb8 0.954; g52+g19 0.916; g56d6+g22d4 0.940 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^17 same I=2 | FFHT 0.4580 (textbook 1.077, textbook-bal 1.065) | g52+tb8 0.997; g56d6+tb8 1.019; g52+g19 0.984; g56d6+g22d4 1.011 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^18 same I=2 | FFHT 0.4810 (textbook 1.044, textbook-bal 1.044) | g52+tb8 0.962; g56d6+tb8 1.001; g52+g19 1.043; g56d6+g22d4 0.993 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^19 same I=2 | FFHT 0.5148 (textbook 1.020, textbook-bal 1.050) | g52+tb8 0.942; g56d6+tb8 0.958; g52+g19 0.951; g56d6+g22d4 0.968 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^20 same I=2 | FFHT 0.5314 (textbook 1.090, textbook-bal 1.077) | g52+tb8 1.008; g56d6+tb8 1.026; g52+g19 1.009; g56d6+g22d4 1.032 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^21 same I=2 | FFHT 0.5442 (textbook 1.052, textbook-bal 1.061) | g52+tb8 0.982; g56d6+tb8 1.011; g52+g19 0.994; g56d6+g22d4 1.014 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^22 same I=2 | textbook 0.5926 (textbook-bal 1.036, FFHT 1.009) | g52+tb8 0.940; g56d6+tb8 0.964; g52+g19 0.953; g56d6+g22d4 0.964 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^23 same I=2 | FFHT 0.6517 (textbook 1.184, textbook-bal 1.187) | g52+tb8 1.132; g56d6+tb8 1.146; g52+g19 1.137; g56d6+g22d4 1.139 |
| whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^24 same I=2 | FFHT 0.7214 (textbook 1.239, textbook-bal 1.237) | g52+tb8 1.175; g56d6+tb8 1.189; g52+g19 1.193; g56d6+g22d4 1.207 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^6 same I=2 | FFHT 0.4992 (textbook 1.369, textbook-bal 1.430) | g52+tb8 1.420; g56d6+tb8 1.493; g52+g19 1.567; g56d6+g22d4 1.750 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^7 same I=2 | FFHT 0.4533 (textbook 1.171, textbook-bal 1.221) | g52+tb8 1.255; g56d6+tb8 1.284; g52+g19 1.293; g56d6+g22d4 1.376 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^8 same I=2 | FFHT 0.4712 (textbook 1.219, textbook-bal 1.166) | g52+tb8 1.187; g56d6+tb8 1.214; g52+g19 1.197; g56d6+g22d4 1.250 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^9 same I=2 | textbook-bal 0.5207 (textbook 1.038, FFHT 1.022) | g52+tb8 0.993; g56d6+tb8 1.003; g52+g19 1.002; g56d6+g22d4 1.019 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^10 same I=2 | textbook-bal 0.5163 (textbook 1.077, FFHT 1.046) | g52+tb8 1.010; g56d6+tb8 1.026; g52+g19 0.977; g56d6+g22d4 1.008 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^11 same I=2 | FFHT 0.5712 (textbook 1.071, textbook-bal 1.026) | g52+tb8 0.935; g56d6+tb8 1.001; g52+g19 0.937; g56d6+g22d4 0.976 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^12 same I=2 | FFHT 0.6472 (textbook 1.061, textbook-bal 1.069) | g52+tb8 0.941; g56d6+tb8 0.983; g52+g19 0.936; g56d6+g22d4 0.991 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^13 same I=2 | FFHT 0.6571 (textbook 1.172, textbook-bal 1.182) | g52+tb8 1.054; g56d6+tb8 1.094; g52+g19 1.056; g56d6+g22d4 1.106 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^14 same I=2 | FFHT 0.7256 (textbook 1.055, textbook-bal 1.061) | g52+tb8 0.947; g56d6+tb8 0.988; g52+g19 0.950; g56d6+g22d4 0.988 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^15 same I=2 | FFHT 0.7538 (textbook 1.053, textbook-bal 1.037) | g52+tb8 0.949; g56d6+tb8 0.987; g52+g19 0.934; g56d6+g22d4 0.971 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^16 same I=2 | FFHT 0.7686 (textbook 1.132, textbook-bal 1.120) | g52+tb8 1.033; g56d6+tb8 1.070; g52+g19 1.058; g56d6+g22d4 1.060 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^17 same I=2 | FFHT 0.8128 (textbook 1.110, textbook-bal 1.108) | g52+tb8 1.011; g56d6+tb8 1.026; g52+g19 1.007; g56d6+g22d4 1.030 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^18 same I=2 | FFHT 0.8999 (textbook 1.034, textbook-bal 1.032) | g52+tb8 0.951; g56d6+tb8 0.976; g52+g19 0.964; g56d6+g22d4 0.971 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^19 same I=2 | FFHT 0.9273 (textbook 1.102, textbook-bal 1.107) | g52+tb8 1.024; g56d6+tb8 1.052; g52+g19 1.031; g56d6+g22d4 1.055 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^20 same I=2 | FFHT 1.0193 (textbook 1.011, textbook-bal 1.011) | g52+tb8 0.943; g56d6+tb8 0.965; g52+g19 0.941; g56d6+g22d4 0.964 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^21 same I=2 | FFHT 1.0453 (textbook 1.028, textbook-bal 1.037) | g52+tb8 0.956; g56d6+tb8 0.978; g52+g19 0.989; g56d6+g22d4 0.982 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^22 same I=2 | FFHT 1.1762 (textbook 1.237, textbook-bal 1.247) | g52+tb8 1.153; g56d6+tb8 1.194; g52+g19 1.175; g56d6+g22d4 1.185 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^23 same I=2 | FFHT 1.3038 (textbook 1.292, textbook-bal 1.297) | g52+tb8 1.229; g56d6+tb8 1.236; g52+g19 1.236; g56d6+g22d4 1.260 |
| whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^24 same I=2 | FFHT 1.4629 (textbook 1.263, textbook-bal 1.257) | g52+tb8 1.211; g56d6+tb8 1.262; g52+g19 1.251; g56d6+g22d4 1.251 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^6 same I=1 | FFHT 0.2930 (textbook 1.828, textbook-bal 2.126) | g52+tb8 2.140; g56d6+tb8 2.436; g52+g19 2.427; g56d6+g22d4 3.044 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^7 same I=1 | FFHT 0.3094 (textbook 1.154, textbook-bal 1.307) | g52+tb8 1.208; g56d6+tb8 1.367; g52+g19 1.335; g56d6+g22d4 1.647 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^8 same I=1 | FFHT 0.2984 (textbook 1.219, textbook-bal 1.279) | g52+tb8 1.223; g56d6+tb8 1.334; g52+g19 1.250; g56d6+g22d4 1.400 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^9 same I=1 | FFHT 0.3076 (textbook 1.069, textbook-bal 1.179) | g52+tb8 1.117; g56d6+tb8 1.208; g52+g19 1.130; g56d6+g22d4 1.236 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^10 same I=1 | textbook 0.3364 (textbook-bal 1.080, FFHT 1.032) | g52+tb8 1.025; g56d6+tb8 1.095; g52+g19 1.001; g56d6+g22d4 1.108 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^11 same I=1 | FFHT 0.3441 (textbook 1.024, textbook-bal 1.160) | g52+tb8 1.025; g56d6+tb8 1.164; g52+g19 1.075; g56d6+g22d4 1.174 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^12 same I=1 | FFHT 0.3599 (textbook 1.082, textbook-bal 1.220) | g52+tb8 1.082; g56d6+tb8 1.210; g52+g19 1.121; g56d6+g22d4 1.204 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^13 same I=1 | FFHT 0.3845 (textbook 1.015, textbook-bal 1.150) | g52+tb8 1.014; g56d6+tb8 1.131; g52+g19 1.033; g56d6+g22d4 1.146 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^14 same I=1 | FFHT 0.4006 (textbook 1.077, textbook-bal 1.202) | g52+tb8 1.078; g56d6+tb8 1.194; g52+g19 1.070; g56d6+g22d4 1.243 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^15 same I=1 | textbook 0.4297 (textbook-bal 1.117, FFHT 1.010) | g52+tb8 0.995; g56d6+tb8 1.105; g52+g19 0.987; g56d6+g22d4 1.110 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^16 same I=1 | textbook 0.4434 (textbook-bal 1.110, FFHT 1.016) | g52+tb8 1.010; g56d6+tb8 1.108; g52+g19 0.982; g56d6+g22d4 1.099 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^17 same I=1 | FFHT 0.4576 (textbook 1.057, textbook-bal 1.165) | g52+tb8 1.055; g56d6+tb8 1.162; g52+g19 1.044; g56d6+g22d4 1.151 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^18 same I=1 | FFHT 0.4756 (textbook 1.057, textbook-bal 1.141) | g52+tb8 1.032; g56d6+tb8 1.134; g52+g19 1.036; g56d6+g22d4 1.316 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^19 same I=1 | FFHT 0.5157 (textbook 1.004, textbook-bal 1.101) | g52+tb8 1.085; g56d6+tb8 1.093; g52+g19 0.990; g56d6+g22d4 1.092 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^20 same I=1 | FFHT 0.5298 (textbook 1.109, textbook-bal 1.164) | g52+tb8 1.061; g56d6+tb8 1.157; g52+g19 1.065; g56d6+g22d4 1.162 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^21 same I=1 | textbook 0.5688 (textbook-bal 1.085, FFHT 1.022) | g52+tb8 0.997; g56d6+tb8 1.099; g52+g19 0.988; g56d6+g22d4 1.080 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^22 same I=1 | FFHT 0.5863 (textbook 1.010, textbook-bal 1.126) | g52+tb8 1.015; g56d6+tb8 1.125; g52+g19 1.005; g56d6+g22d4 1.101 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^23 same I=1 | FFHT 0.6865 (textbook 1.158, textbook-bal 1.236) | g52+tb8 1.155; g56d6+tb8 1.227; g52+g19 1.157; g56d6+g22d4 1.238 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^24 same I=1 | FFHT 0.7271 (textbook 1.277, textbook-bal 1.353) | g52+tb8 1.265; g56d6+tb8 1.329; g52+g19 1.259; g56d6+g22d4 1.345 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^6 same I=1 | FFHT 0.4913 (textbook 1.296, textbook-bal 1.519) | g52+tb8 1.481; g56d6+tb8 1.658; g52+g19 1.650; g56d6+g22d4 2.001 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^7 same I=1 | FFHT 0.4635 (textbook 1.325, textbook-bal 1.502) | g52+tb8 1.395; g56d6+tb8 1.535; g52+g19 1.468; g56d6+g22d4 1.714 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^8 same I=1 | FFHT 0.4719 (textbook 1.127, textbook-bal 1.256) | g52+tb8 1.180; g56d6+tb8 1.308; g52+g19 1.200; g56d6+g22d4 1.381 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^9 same I=1 | textbook 0.5447 (textbook-bal 1.088, FFHT 1.110) | g52+tb8 1.033; g56d6+tb8 1.121; g52+g19 1.006; g56d6+g22d4 1.111 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^10 same I=1 | FFHT 0.5409 (textbook 1.069, textbook-bal 1.225) | g52+tb8 1.068; g56d6+tb8 1.255; g52+g19 1.060; g56d6+g22d4 1.251 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^11 same I=1 | FFHT 0.5731 (textbook 1.137, textbook-bal 1.296) | g52+tb8 1.124; g56d6+tb8 1.297; g52+g19 1.134; g56d6+g22d4 1.316 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^12 same I=1 | FFHT 0.6462 (textbook 1.015, textbook-bal 1.151) | g52+tb8 1.010; g56d6+tb8 1.162; g52+g19 1.000; g56d6+g22d4 1.156 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^13 same I=1 | FFHT 0.6547 (textbook 1.130, textbook-bal 1.266) | g52+tb8 1.115; g56d6+tb8 1.274; g52+g19 1.117; g56d6+g22d4 1.356 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^14 same I=1 | FFHT 0.7230 (textbook 1.011, textbook-bal 1.143) | g52+tb8 1.004; g56d6+tb8 1.140; g52+g19 0.996; g56d6+g22d4 1.145 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^15 same I=1 | FFHT 0.7536 (textbook 1.012, textbook-bal 1.135) | g52+tb8 1.010; g56d6+tb8 1.135; g52+g19 0.988; g56d6+g22d4 1.124 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^16 same I=1 | FFHT 0.7701 (textbook 1.099, textbook-bal 1.210) | g52+tb8 1.120; g56d6+tb8 1.215; g52+g19 1.071; g56d6+g22d4 1.216 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^17 same I=1 | FFHT 0.8056 (textbook 1.084, textbook-bal 1.203) | g52+tb8 1.063; g56d6+tb8 1.176; g52+g19 1.072; g56d6+g22d4 1.193 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^18 same I=1 | FFHT 0.8848 (textbook 1.036, textbook-bal 1.141) | g52+tb8 1.034; g56d6+tb8 1.152; g52+g19 1.013; g56d6+g22d4 1.129 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^19 same I=1 | FFHT 0.9112 (textbook 1.115, textbook-bal 1.216) | g52+tb8 1.097; g56d6+tb8 1.208; g52+g19 1.086; g56d6+g22d4 1.247 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^20 same I=1 | textbook 1.0190 (textbook-bal 1.085, FFHT 1.118) | g52+tb8 1.005; g56d6+tb8 1.080; g52+g19 0.979; g56d6+g22d4 1.082 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^21 same I=1 | FFHT 1.0695 (textbook 1.007, textbook-bal 1.086) | g52+tb8 1.007; g56d6+tb8 1.083; g52+g19 0.990; g56d6+g22d4 1.088 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^22 same I=1 | FFHT 1.1744 (textbook 1.270, textbook-bal 1.351) | g52+tb8 1.271; g56d6+tb8 1.328; g52+g19 1.255; g56d6+g22d4 1.350 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^23 same I=1 | FFHT 1.3137 (textbook 1.347, textbook-bal 1.417) | g52+tb8 1.333; g56d6+tb8 1.394; g52+g19 1.308; g56d6+g22d4 1.404 |
| whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^24 same I=1 | FFHT 1.4735 (textbook 1.336, textbook-bal 1.388) | g52+tb8 1.315; g56d6+tb8 1.402; g52+g19 1.323; g56d6+g22d4 1.400 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^6 same I=1 | FFHT 0.2935 (textbook 1.783, textbook-bal 2.159) | g52+tb8 2.104; g56d6+tb8 2.411; g52+g19 2.460; g56d6+g22d4 3.080 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^7 same I=1 | FFHT 0.3101 (textbook 1.160, textbook-bal 1.279) | g52+tb8 1.242; g56d6+tb8 1.378; g52+g19 1.365; g56d6+g22d4 1.676 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^8 same I=1 | FFHT 0.3037 (textbook 1.165, textbook-bal 1.251) | g52+tb8 1.206; g56d6+tb8 1.296; g52+g19 1.263; g56d6+g22d4 1.431 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^9 same I=1 | FFHT 0.3094 (textbook 1.067, textbook-bal 1.101) | g52+tb8 1.095; g56d6+tb8 1.085; g52+g19 1.156; g56d6+g22d4 1.119 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^10 same I=1 | textbook 0.3324 (textbook-bal 1.026, FFHT 1.044) | g52+tb8 1.018; g56d6+tb8 1.011; g52+g19 0.998; g56d6+g22d4 1.002 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^11 same I=1 | FFHT 0.3442 (textbook 1.005, textbook-bal 1.005) | g52+tb8 0.969; g56d6+tb8 0.969; g52+g19 0.992; g56d6+g22d4 0.978 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^12 same I=1 | FFHT 0.3605 (textbook 1.059, textbook-bal 1.060) | g52+tb8 1.024; g56d6+tb8 1.023; g52+g19 1.028; g56d6+g22d4 1.045 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^13 same I=1 | textbook 0.3829 (textbook-bal 1.000, FFHT 1.008) | g52+tb8 0.977; g56d6+tb8 0.973; g52+g19 0.983; g56d6+g22d4 0.979 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^14 same I=1 | FFHT 0.4016 (textbook 1.060, textbook-bal 1.060) | g52+tb8 1.037; g56d6+tb8 1.044; g52+g19 1.035; g56d6+g22d4 1.033 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^15 same I=1 | textbook-bal 0.4249 (textbook 1.003, FFHT 1.025) | g52+tb8 0.973; g56d6+tb8 0.971; g52+g19 0.977; g56d6+g22d4 0.971 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^16 same I=1 | textbook-bal 0.4345 (textbook 1.012, FFHT 1.040) | g52+tb8 0.986; g56d6+tb8 0.988; g52+g19 0.970; g56d6+g22d4 0.974 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^17 same I=1 | FFHT 0.4579 (textbook 1.044, textbook-bal 1.041) | g52+tb8 1.021; g56d6+tb8 1.022; g52+g19 1.004; g56d6+g22d4 1.012 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^18 same I=1 | FFHT 0.4772 (textbook 1.021, textbook-bal 1.042) | g52+tb8 0.992; g56d6+tb8 1.111; g52+g19 1.011; g56d6+g22d4 1.012 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^19 same I=1 | textbook 0.5153 (textbook-bal 1.023, FFHT 1.001) | g52+tb8 0.973; g56d6+tb8 0.975; g52+g19 0.970; g56d6+g22d4 0.971 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^20 same I=1 | FFHT 0.5306 (textbook 1.071, textbook-bal 1.054) | g52+tb8 1.027; g56d6+tb8 1.038; g52+g19 1.028; g56d6+g22d4 1.029 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^21 same I=1 | textbook-bal 0.5619 (textbook 1.003, FFHT 1.037) | g52+tb8 0.976; g56d6+tb8 0.994; g52+g19 0.977; g56d6+g22d4 0.982 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^22 same I=1 | textbook 0.5870 (textbook-bal 1.002, FFHT 1.002) | g52+tb8 0.979; g56d6+tb8 0.984; g52+g19 0.978; g56d6+g22d4 1.016 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^23 same I=1 | FFHT 0.6939 (textbook 1.129, textbook-bal 1.118) | g52+tb8 1.101; g56d6+tb8 1.103; g52+g19 1.108; g56d6+g22d4 1.117 |
| whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^24 same I=1 | FFHT 0.7211 (textbook 1.273, textbook-bal 1.274) | g52+tb8 1.253; g56d6+tb8 1.236; g52+g19 1.233; g56d6+g22d4 1.240 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^6 same I=1 | FFHT 0.2930 (textbook 1.704, textbook-bal 1.984) | g52+tb8 2.028; g56d6+tb8 2.316; g52+g19 2.328; g56d6+g22d4 2.945 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^7 same I=1 | FFHT 0.3112 (textbook 1.067, textbook-bal 1.144) | g52+tb8 1.148; g56d6+tb8 1.202; g52+g19 1.260; g56d6+g22d4 1.415 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^8 same I=1 | textbook 0.2958 (textbook-bal 1.037, FFHT 1.052) | g52+tb8 1.056; g56d6+tb8 1.087; g52+g19 1.092; g56d6+g22d4 1.259 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^9 same I=1 | FFHT 0.3075 (textbook 1.065, textbook-bal 1.041) | g52+tb8 1.063; g56d6+tb8 1.071; g52+g19 1.086; g56d6+g22d4 1.104 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^10 same I=1 | textbook-bal 0.3062 (textbook 1.027, FFHT 1.140) | g52+tb8 1.017; g56d6+tb8 1.021; g52+g19 1.030; g56d6+g22d4 1.034 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^11 same I=1 | textbook-bal 0.3151 (textbook 1.022, FFHT 1.091) | g52+tb8 1.006; g56d6+tb8 1.008; g52+g19 1.004; g56d6+g22d4 0.995 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^12 same I=1 | textbook-bal 0.3258 (textbook 1.047, FFHT 1.107) | g52+tb8 0.958; g56d6+tb8 1.017; g52+g19 0.977; g56d6+g22d4 0.991 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^13 same I=1 | textbook-bal 0.3645 (textbook 1.048, FFHT 1.055) | g52+tb8 0.984; g56d6+tb8 0.990; g52+g19 0.983; g56d6+g22d4 0.993 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^14 same I=1 | FFHT 0.4008 (textbook 1.058, textbook-bal 1.003) | g52+tb8 0.992; g56d6+tb8 1.007; g52+g19 0.995; g56d6+g22d4 1.009 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^15 same I=1 | textbook-bal 0.3983 (textbook 1.052, FFHT 1.090) | g52+tb8 0.987; g56d6+tb8 1.000; g52+g19 0.988; g56d6+g22d4 1.003 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^16 same I=1 | textbook-bal 0.4151 (textbook 1.047, FFHT 1.086) | g52+tb8 0.984; g56d6+tb8 1.000; g52+g19 0.974; g56d6+g22d4 0.987 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^17 same I=1 | textbook-bal 0.4543 (textbook 1.046, FFHT 1.007) | g52+tb8 0.985; g56d6+tb8 0.997; g52+g19 0.981; g56d6+g22d4 0.990 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^18 same I=1 | textbook-bal 0.4642 (textbook 1.036, FFHT 1.025) | g52+tb8 0.983; g56d6+tb8 1.006; g52+g19 1.003; g56d6+g22d4 1.005 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^19 same I=1 | textbook-bal 0.4940 (textbook 1.014, FFHT 1.047) | g52+tb8 0.965; g56d6+tb8 1.002; g52+g19 0.967; g56d6+g22d4 0.989 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^20 same I=1 | FFHT 0.5293 (textbook 1.040, textbook-bal 1.026) | g52+tb8 0.991; g56d6+tb8 1.002; g52+g19 0.989; g56d6+g22d4 1.014 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^21 same I=1 | textbook-bal 0.5401 (textbook 1.030, FFHT 1.074) | g52+tb8 0.975; g56d6+tb8 0.982; g52+g19 0.979; g56d6+g22d4 0.993 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^22 same I=1 | textbook-bal 0.5612 (textbook 1.030, FFHT 1.042) | g52+tb8 0.972; g56d6+tb8 0.984; g52+g19 0.974; g56d6+g22d4 1.001 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^23 same I=1 | FFHT 0.6867 (textbook 1.098, textbook-bal 1.065) | g52+tb8 1.048; g56d6+tb8 1.071; g52+g19 1.051; g56d6+g22d4 1.066 |
| whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^24 same I=1 | FFHT 0.7233 (textbook 1.218, textbook-bal 1.197) | g52+tb8 1.180; g56d6+tb8 1.185; g52+g19 1.172; g56d6+g22d4 1.178 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^6 same I=1 | FFHT 0.4951 (textbook 1.090, textbook-bal 1.275) | g52+tb8 1.257; g56d6+tb8 1.432; g52+g19 1.428; g56d6+g22d4 1.762 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^7 same I=1 | FFHT 0.4537 (textbook 1.191, textbook-bal 1.131) | g52+tb8 1.127; g56d6+tb8 1.171; g52+g19 1.181; g56d6+g22d4 1.255 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^8 same I=1 | FFHT 0.4717 (textbook 1.168, textbook-bal 1.157) | g52+tb8 1.161; g56d6+tb8 1.169; g52+g19 1.180; g56d6+g22d4 1.212 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^9 same I=1 | textbook-bal 0.5132 (textbook 1.034, FFHT 1.062) | g52+tb8 1.019; g56d6+tb8 1.018; g52+g19 1.028; g56d6+g22d4 1.037 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^10 same I=1 | textbook-bal 0.5295 (textbook 1.033, FFHT 1.020) | g52+tb8 1.022; g56d6+tb8 1.036; g52+g19 0.985; g56d6+g22d4 1.003 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^11 same I=1 | textbook-bal 0.5465 (textbook 1.078, FFHT 1.049) | g52+tb8 0.987; g56d6+tb8 1.009; g52+g19 0.987; g56d6+g22d4 1.009 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^12 same I=1 | textbook-bal 0.6318 (textbook 1.056, FFHT 1.025) | g52+tb8 0.973; g56d6+tb8 1.008; g52+g19 0.970; g56d6+g22d4 0.994 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^13 same I=1 | FFHT 0.6550 (textbook 1.149, textbook-bal 1.085) | g52+tb8 1.082; g56d6+tb8 1.082; g52+g19 1.066; g56d6+g22d4 1.084 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^14 same I=1 | textbook-bal 0.7018 (textbook 1.060, FFHT 1.031) | g52+tb8 0.992; g56d6+tb8 1.006; g52+g19 0.999; g56d6+g22d4 1.007 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^15 same I=1 | textbook-bal 0.7372 (textbook 1.051, FFHT 1.023) | g52+tb8 0.988; g56d6+tb8 0.998; g52+g19 0.978; g56d6+g22d4 0.988 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^16 same I=1 | FFHT 0.7718 (textbook 1.104, textbook-bal 1.054) | g52+tb8 1.047; g56d6+tb8 1.056; g52+g19 1.036; g56d6+g22d4 1.045 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^17 same I=1 | FFHT 0.8135 (textbook 1.084, textbook-bal 1.038) | g52+tb8 1.026; g56d6+tb8 1.019; g52+g19 1.023; g56d6+g22d4 1.042 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^18 same I=1 | textbook-bal 0.8832 (textbook 1.039, FFHT 1.007) | g52+tb8 0.979; g56d6+tb8 1.011; g52+g19 0.982; g56d6+g22d4 0.995 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^19 same I=1 | FFHT 0.9119 (textbook 1.104, textbook-bal 1.087) | g52+tb8 1.056; g56d6+tb8 1.060; g52+g19 1.051; g56d6+g22d4 1.067 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^20 same I=1 | textbook-bal 0.9898 (textbook 1.031, FFHT 1.138) | g52+tb8 0.977; g56d6+tb8 0.982; g52+g19 0.980; g56d6+g22d4 0.989 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^21 same I=1 | textbook-bal 1.0353 (textbook 1.021, FFHT 1.029) | g52+tb8 0.984; g56d6+tb8 0.979; g52+g19 0.981; g56d6+g22d4 1.001 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^22 same I=1 | FFHT 1.1608 (textbook 1.232, textbook-bal 1.200) | g52+tb8 1.193; g56d6+tb8 1.208; g52+g19 1.214; g56d6+g22d4 1.205 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^23 same I=1 | FFHT 1.3093 (textbook 1.286, textbook-bal 1.265) | g52+tb8 1.257; g56d6+tb8 1.255; g52+g19 1.250; g56d6+g22d4 1.247 |
| whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^24 same I=1 | FFHT 1.4799 (textbook 1.255, textbook-bal 1.226) | g52+tb8 1.211; g56d6+tb8 1.237; g52+g19 1.237; g56d6+g22d4 1.247 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^6 same I=1 | FFHT 0.2975 (textbook 1.833, textbook-bal 2.223) | g52+tb8 2.142; g56d6+tb8 2.433; g52+g19 2.479; g56d6+g22d4 3.063 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^7 same I=1 | FFHT 0.3103 (textbook 1.166, textbook-bal 1.348) | g52+tb8 1.262; g56d6+tb8 1.408; g52+g19 1.402; g56d6+g22d4 1.689 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^8 same I=1 | FFHT 0.2983 (textbook 1.145, textbook-bal 1.307) | g52+tb8 1.209; g56d6+tb8 1.301; g52+g19 1.278; g56d6+g22d4 1.451 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^9 same I=1 | textbook 0.3074 (textbook-bal 1.141, FFHT 1.001) | g52+tb8 0.996; g56d6+tb8 1.100; g52+g19 1.019; g56d6+g22d4 1.127 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^10 same I=1 | textbook 0.3173 (textbook-bal 1.066, FFHT 1.065) | g52+tb8 0.968; g56d6+tb8 0.990; g52+g19 0.930; g56d6+g22d4 0.987 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^11 same I=1 | textbook 0.3256 (textbook-bal 1.103, FFHT 1.055) | g52+tb8 0.899; g56d6+tb8 0.971; g52+g19 0.913; g56d6+g22d4 0.971 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^12 same I=1 | FFHT 0.3590 (textbook 1.002, textbook-bal 1.096) | g52+tb8 0.915; g56d6+tb8 0.965; g52+g19 0.916; g56d6+g22d4 0.976 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^13 same I=1 | textbook 0.3590 (textbook-bal 1.103, FFHT 1.059) | g52+tb8 0.919; g56d6+tb8 0.977; g52+g19 0.932; g56d6+g22d4 0.976 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^14 same I=1 | FFHT 0.4011 (textbook 1.002, textbook-bal 1.087) | g52+tb8 0.924; g56d6+tb8 0.980; g52+g19 0.939; g56d6+g22d4 0.978 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^15 same I=1 | textbook 0.3985 (textbook-bal 1.092, FFHT 1.090) | g52+tb8 0.931; g56d6+tb8 0.995; g52+g19 1.214; g56d6+g22d4 0.979 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^16 same I=1 | textbook 0.4133 (textbook-bal 1.159, FFHT 1.087) | g52+tb8 0.928; g56d6+tb8 0.976; g52+g19 0.909; g56d6+g22d4 0.979 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^17 same I=1 | textbook 0.4545 (textbook-bal 1.068, FFHT 1.007) | g52+tb8 0.939; g56d6+tb8 0.976; g52+g19 0.920; g56d6+g22d4 0.973 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^18 same I=1 | textbook 0.4673 (textbook-bal 1.080, FFHT 1.019) | g52+tb8 0.947; g56d6+tb8 0.981; g52+g19 0.944; g56d6+g22d4 0.973 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^19 same I=1 | textbook 0.4852 (textbook-bal 1.085, FFHT 1.059) | g52+tb8 0.940; g56d6+tb8 0.976; g52+g19 0.935; g56d6+g22d4 0.993 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^20 same I=1 | textbook 0.5325 (textbook-bal 1.075, FFHT 1.001) | g52+tb8 0.936; g56d6+tb8 0.992; g52+g19 0.940; g56d6+g22d4 0.992 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^21 same I=1 | textbook 0.5346 (textbook-bal 1.082, FFHT 1.028) | g52+tb8 0.944; g56d6+tb8 0.982; g52+g19 0.943; g56d6+g22d4 1.003 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^22 same I=1 | textbook 0.5575 (textbook-bal 1.074, FFHT 1.054) | g52+tb8 0.946; g56d6+tb8 0.983; g52+g19 0.955; g56d6+g22d4 1.016 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^23 same I=1 | FFHT 0.6432 (textbook 1.194, textbook-bal 1.247) | g52+tb8 1.126; g56d6+tb8 1.148; g52+g19 1.116; g56d6+g22d4 1.170 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^24 same I=1 | FFHT 0.7307 (textbook 1.245, textbook-bal 1.309) | g52+tb8 1.200; g56d6+tb8 1.235; g52+g19 1.199; g56d6+g22d4 1.239 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^6 same I=1 | FFHT 0.4929 (textbook 1.267, textbook-bal 1.486) | g52+tb8 1.422; g56d6+tb8 1.608; g52+g19 1.590; g56d6+g22d4 1.960 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^7 same I=1 | FFHT 0.4532 (textbook 1.237, textbook-bal 1.448) | g52+tb8 1.318; g56d6+tb8 1.443; g52+g19 1.408; g56d6+g22d4 1.623 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^8 same I=1 | FFHT 0.4731 (textbook 1.046, textbook-bal 1.185) | g52+tb8 1.046; g56d6+tb8 1.103; g52+g19 1.114; g56d6+g22d4 1.138 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^9 same I=1 | textbook 0.4963 (textbook-bal 1.105, FFHT 1.094) | g52+tb8 0.975; g56d6+tb8 1.020; g52+g19 0.946; g56d6+g22d4 1.013 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^10 same I=1 | textbook 0.5291 (textbook-bal 1.122, FFHT 1.022) | g52+tb8 0.896; g56d6+tb8 0.951; g52+g19 0.887; g56d6+g22d4 0.966 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^11 same I=1 | FFHT 0.5728 (textbook 1.042, textbook-bal 1.151) | g52+tb8 0.928; g56d6+tb8 1.003; g52+g19 0.942; g56d6+g22d4 1.010 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^12 same I=1 | textbook 0.5947 (textbook-bal 1.127, FFHT 1.086) | g52+tb8 0.907; g56d6+tb8 0.986; g52+g19 0.913; g56d6+g22d4 0.978 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^13 same I=1 | FFHT 0.6565 (textbook 1.039, textbook-bal 1.152) | g52+tb8 0.958; g56d6+tb8 1.022; g52+g19 0.961; g56d6+g22d4 1.025 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^14 same I=1 | textbook 0.6744 (textbook-bal 1.113, FFHT 1.073) | g52+tb8 0.917; g56d6+tb8 0.988; g52+g19 0.918; g56d6+g22d4 0.983 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^15 same I=1 | textbook 0.7444 (textbook-bal 1.025, FFHT 1.013) | g52+tb8 0.868; g56d6+tb8 0.922; g52+g19 0.849; g56d6+g22d4 0.923 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^16 same I=1 | FFHT 0.7686 (textbook 1.048, textbook-bal 1.099) | g52+tb8 0.942; g56d6+tb8 0.996; g52+g19 0.926; g56d6+g22d4 1.031 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^17 same I=1 | textbook 0.8192 (textbook-bal 1.067, FFHT 1.087) | g52+tb8 0.929; g56d6+tb8 0.966; g52+g19 0.917; g56d6+g22d4 0.955 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^18 same I=1 | textbook 0.8501 (textbook-bal 1.091, FFHT 1.035) | g52+tb8 0.986; g56d6+tb8 0.970; g52+g19 0.924; g56d6+g22d4 0.987 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^19 same I=1 | FFHT 0.9151 (textbook 1.056, textbook-bal 1.107) | g52+tb8 0.957; g56d6+tb8 1.015; g52+g19 0.967; g56d6+g22d4 1.020 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^20 same I=1 | textbook 0.9453 (textbook-bal 1.081, FFHT 1.052) | g52+tb8 0.939; g56d6+tb8 1.001; g52+g19 0.938; g56d6+g22d4 0.997 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^21 same I=1 | textbook 0.9884 (textbook-bal 1.133, FFHT 1.059) | g52+tb8 0.964; g56d6+tb8 1.000; g52+g19 0.940; g56d6+g22d4 1.017 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^22 same I=1 | FFHT 1.1461 (textbook 1.269, textbook-bal 1.335) | g52+tb8 1.233; g56d6+tb8 1.228; g52+g19 1.170; g56d6+g22d4 1.221 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^23 same I=1 | FFHT 1.3278 (textbook 1.291, textbook-bal 1.361) | g52+tb8 1.248; g56d6+tb8 1.293; g52+g19 1.254; g56d6+g22d4 1.313 |
| whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^24 same I=1 | FFHT 1.4826 (textbook 1.291, textbook-bal 1.361) | g52+tb8 1.257; g56d6+tb8 1.298; g52+g19 1.251; g56d6+g22d4 1.295 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^6 same I=1 | FFHT 0.2930 (textbook 1.714, textbook-bal 2.015) | g52+tb8 1.937; g56d6+tb8 2.218; g52+g19 2.298; g56d6+g22d4 2.890 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^7 same I=1 | FFHT 0.3118 (textbook 1.115, textbook-bal 1.213) | g52+tb8 1.238; g56d6+tb8 1.268; g52+g19 1.499; g56d6+g22d4 1.556 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^8 same I=1 | FFHT 0.3012 (textbook 1.101, textbook-bal 1.169) | g52+tb8 1.402; g56d6+tb8 1.141; g52+g19 1.480; g56d6+g22d4 1.281 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^9 same I=1 | textbook 0.3021 (textbook-bal 1.051, FFHT 1.018) | g52+tb8 1.134; g56d6+tb8 1.014; g52+g19 1.157; g56d6+g22d4 1.086 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^10 same I=1 | textbook 0.3074 (textbook-bal 1.010, FFHT 1.098) | g52+tb8 1.061; g56d6+tb8 0.975; g52+g19 1.015; g56d6+g22d4 0.964 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^11 same I=1 | textbook-bal 0.3100 (textbook 1.033, FFHT 1.109) | g52+tb8 0.965; g56d6+tb8 0.943; g52+g19 0.967; g56d6+g22d4 0.950 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^12 same I=1 | textbook-bal 0.3405 (textbook 1.044, FFHT 1.054) | g52+tb8 0.957; g56d6+tb8 0.958; g52+g19 0.963; g56d6+g22d4 0.974 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^13 same I=1 | textbook-bal 0.3457 (textbook 1.033, FFHT 1.100) | g52+tb8 0.945; g56d6+tb8 0.946; g52+g19 0.940; g56d6+g22d4 0.948 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^14 same I=1 | textbook-bal 0.3896 (textbook 1.028, FFHT 1.030) | g52+tb8 0.944; g56d6+tb8 0.951; g52+g19 0.944; g56d6+g22d4 0.950 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^15 same I=1 | textbook-bal 0.3880 (textbook 1.026, FFHT 1.119) | g52+tb8 0.939; g56d6+tb8 0.947; g52+g19 0.943; g56d6+g22d4 0.950 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^16 same I=1 | textbook-bal 0.4002 (textbook 1.030, FFHT 1.122) | g52+tb8 0.945; g56d6+tb8 0.953; g52+g19 0.923; g56d6+g22d4 0.954 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^17 same I=1 | textbook-bal 0.4394 (textbook 1.025, FFHT 1.045) | g52+tb8 0.948; g56d6+tb8 0.960; g52+g19 0.933; g56d6+g22d4 0.958 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^18 same I=1 | textbook-bal 0.4507 (textbook 1.019, FFHT 1.069) | g52+tb8 0.954; g56d6+tb8 0.972; g52+g19 0.939; g56d6+g22d4 0.961 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^19 same I=1 | textbook-bal 0.4754 (textbook 1.011, FFHT 1.082) | g52+tb8 0.940; g56d6+tb8 0.952; g52+g19 0.946; g56d6+g22d4 0.966 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^20 same I=1 | textbook 0.5297 (textbook-bal 1.002, FFHT 1.001) | g52+tb8 0.931; g56d6+tb8 0.944; g52+g19 0.930; g56d6+g22d4 0.973 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^21 same I=1 | textbook-bal 0.5276 (textbook 1.013, FFHT 1.040) | g52+tb8 0.952; g56d6+tb8 0.954; g52+g19 0.941; g56d6+g22d4 0.966 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^22 same I=1 | textbook 0.5564 (textbook-bal 1.030, FFHT 1.067) | g52+tb8 0.937; g56d6+tb8 0.950; g52+g19 0.988; g56d6+g22d4 0.973 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^23 same I=1 | FFHT 0.6505 (textbook 1.171, textbook-bal 1.177) | g52+tb8 1.106; g56d6+tb8 1.122; g52+g19 1.100; g56d6+g22d4 1.164 |
| whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^24 same I=1 | FFHT 0.7214 (textbook 1.231, textbook-bal 1.219) | g52+tb8 1.176; g56d6+tb8 1.188; g52+g19 1.184; g56d6+g22d4 1.206 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^6 same I=1 | FFHT 0.2924 (textbook 1.744, textbook-bal 1.997) | g52+tb8 1.915; g56d6+tb8 2.114; g52+g19 2.115; g56d6+g22d4 2.709 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^7 same I=1 | FFHT 0.3101 (textbook 1.265, textbook-bal 1.352) | g52+tb8 1.376; g56d6+tb8 1.402; g52+g19 1.452; g56d6+g22d4 1.552 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^8 same I=1 | FFHT 0.2980 (textbook 1.103, textbook-bal 1.131) | g52+tb8 1.239; g56d6+tb8 1.188; g52+g19 1.186; g56d6+g22d4 1.254 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^9 same I=1 | FFHT 0.3070 (textbook 1.126, textbook-bal 1.091) | g52+tb8 1.091; g56d6+tb8 1.114; g52+g19 1.110; g56d6+g22d4 1.150 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^10 same I=1 | textbook-bal 0.3197 (textbook 1.026, FFHT 1.056) | g52+tb8 0.991; g56d6+tb8 0.997; g52+g19 0.997; g56d6+g22d4 1.018 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^11 same I=1 | textbook-bal 0.3316 (textbook 1.009, FFHT 1.037) | g52+tb8 0.963; g56d6+tb8 0.966; g52+g19 0.941; g56d6+g22d4 0.955 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^12 same I=1 | textbook-bal 0.3167 (textbook 1.104, FFHT 1.133) | g52+tb8 0.974; g56d6+tb8 1.009; g52+g19 0.975; g56d6+g22d4 1.017 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^13 same I=1 | textbook-bal 0.3569 (textbook 1.086, FFHT 1.069) | g52+tb8 0.986; g56d6+tb8 1.001; g52+g19 0.976; g56d6+g22d4 1.008 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^14 same I=1 | FFHT 0.4012 (textbook 1.069, textbook-bal 1.003) | g52+tb8 0.973; g56d6+tb8 0.993; g52+g19 0.972; g56d6+g22d4 1.000 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^15 same I=1 | textbook-bal 0.4028 (textbook 1.059, FFHT 1.077) | g52+tb8 0.964; g56d6+tb8 0.979; g52+g19 0.963; g56d6+g22d4 0.980 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^16 same I=1 | textbook-bal 0.4134 (textbook 1.068, FFHT 1.087) | g52+tb8 0.972; g56d6+tb8 0.989; g52+g19 0.955; g56d6+g22d4 0.973 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^17 same I=1 | textbook-bal 0.4522 (textbook 1.060, FFHT 1.012) | g52+tb8 0.972; g56d6+tb8 1.149; g52+g19 0.959; g56d6+g22d4 0.974 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^18 same I=1 | FFHT 0.4766 (textbook 1.021, textbook-bal 1.055) | g52+tb8 0.952; g56d6+tb8 0.973; g52+g19 0.936; g56d6+g22d4 0.963 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^19 same I=1 | textbook-bal 0.4790 (textbook 1.091, FFHT 1.069) | g52+tb8 0.978; g56d6+tb8 0.994; g52+g19 0.982; g56d6+g22d4 0.996 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^20 same I=1 | textbook-bal 0.5247 (textbook 1.058, FFHT 1.010) | g52+tb8 0.989; g56d6+tb8 1.000; g52+g19 0.985; g56d6+g22d4 0.998 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^21 same I=1 | textbook-bal 0.5333 (textbook 1.045, FFHT 1.018) | g52+tb8 0.971; g56d6+tb8 0.996; g52+g19 0.974; g56d6+g22d4 0.983 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^22 same I=1 | textbook-bal 0.5606 (textbook 1.036, FFHT 1.070) | g52+tb8 0.960; g56d6+tb8 0.976; g52+g19 0.966; g56d6+g22d4 0.974 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^23 same I=1 | FFHT 0.6562 (textbook 1.159, textbook-bal 1.129) | g52+tb8 1.099; g56d6+tb8 1.123; g52+g19 1.109; g56d6+g22d4 1.098 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^24 same I=1 | FFHT 0.7276 (textbook 1.217, textbook-bal 1.175) | g52+tb8 1.145; g56d6+tb8 1.165; g52+g19 1.178; g56d6+g22d4 1.191 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^6 same I=1 | FFHT 0.4934 (textbook 1.334, textbook-bal 1.938) | g52+tb8 1.437; g56d6+tb8 1.518; g52+g19 1.581; g56d6+g22d4 1.762 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^7 same I=1 | FFHT 0.4685 (textbook 1.132, textbook-bal 1.182) | g52+tb8 1.207; g56d6+tb8 1.375; g52+g19 1.261; g56d6+g22d4 1.332 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^8 same I=1 | FFHT 0.4767 (textbook 1.203, textbook-bal 1.179) | g52+tb8 1.170; g56d6+tb8 1.203; g52+g19 1.174; g56d6+g22d4 1.236 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^9 same I=1 | textbook-bal 0.5174 (textbook 1.048, FFHT 1.030) | g52+tb8 0.995; g56d6+tb8 1.014; g52+g19 1.005; g56d6+g22d4 1.027 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^10 same I=1 | textbook-bal 0.5213 (textbook 1.056, FFHT 1.037) | g52+tb8 0.999; g56d6+tb8 1.008; g52+g19 0.966; g56d6+g22d4 0.996 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^11 same I=1 | textbook-bal 0.5204 (textbook 1.123, FFHT 1.099) | g52+tb8 0.960; g56d6+tb8 1.005; g52+g19 0.958; g56d6+g22d4 1.010 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^12 same I=1 | textbook-bal 0.5972 (textbook 1.108, FFHT 1.083) | g52+tb8 0.971; g56d6+tb8 1.011; g52+g19 0.970; g56d6+g22d4 1.002 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^13 same I=1 | FFHT 0.6566 (textbook 1.132, textbook-bal 1.039) | g52+tb8 1.011; g56d6+tb8 1.043; g52+g19 1.011; g56d6+g22d4 1.037 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^14 same I=1 | textbook-bal 0.6808 (textbook 1.085, FFHT 1.064) | g52+tb8 0.969; g56d6+tb8 0.996; g52+g19 0.972; g56d6+g22d4 0.996 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^15 same I=1 | textbook-bal 0.7025 (textbook 1.094, FFHT 1.075) | g52+tb8 0.983; g56d6+tb8 1.005; g52+g19 0.960; g56d6+g22d4 0.988 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^16 same I=1 | FFHT 0.7694 (textbook 1.102, textbook-bal 1.014) | g52+tb8 1.001; g56d6+tb8 1.022; g52+g19 0.981; g56d6+g22d4 1.004 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^17 same I=1 | textbook-bal 0.8044 (textbook 1.085, FFHT 1.051) | g52+tb8 1.003; g56d6+tb8 0.993; g52+g19 0.982; g56d6+g22d4 0.987 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^18 same I=1 | textbook-bal 0.8445 (textbook 1.068, FFHT 1.046) | g52+tb8 0.978; g56d6+tb8 1.004; g52+g19 0.984; g56d6+g22d4 0.996 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^19 same I=1 | FFHT 0.9116 (textbook 1.096, textbook-bal 1.041) | g52+tb8 1.011; g56d6+tb8 1.030; g52+g19 1.010; g56d6+g22d4 1.025 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^20 same I=1 | textbook-bal 0.9460 (textbook 1.061, FFHT 1.055) | g52+tb8 0.977; g56d6+tb8 0.995; g52+g19 0.979; g56d6+g22d4 0.999 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^21 same I=1 | textbook-bal 0.9878 (textbook 1.068, FFHT 1.067) | g52+tb8 0.979; g56d6+tb8 0.999; g52+g19 0.990; g56d6+g22d4 1.044 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^22 same I=1 | FFHT 1.1765 (textbook 1.195, textbook-bal 1.161) | g52+tb8 1.150; g56d6+tb8 1.138; g52+g19 1.161; g56d6+g22d4 1.174 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^23 same I=1 | FFHT 1.3022 (textbook 1.282, textbook-bal 1.236) | g52+tb8 1.205; g56d6+tb8 1.215; g52+g19 1.219; g56d6+g22d4 1.241 |
| whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^24 same I=1 | FFHT 1.4617 (textbook 1.251, textbook-bal 1.212) | g52+tb8 1.210; g56d6+tb8 1.219; g52+g19 1.218; g56d6+g22d4 1.232 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^10 separate I=1 | textbook 0.3481 (textbook-bal 1.078, FFHT 1.073) | g52+tb8 1.030; g56d6+tb8 1.096; g52+g19 1.012; g56d6+g22d4 1.088 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1 | FFHT 0.3689 (textbook 1.106, textbook-bal 1.237) | g52+tb8 1.089; g56d6+tb8 1.233; g52+g19 1.094; g56d6+g22d4 1.235 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^14 separate I=1 | FFHT 0.4280 (textbook 1.139, textbook-bal 1.257) | g52+tb8 1.132; g56d6+tb8 1.248; g52+g19 1.133; g56d6+g22d4 1.250 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1 | FFHT 0.4971 (textbook 1.006, textbook-bal 1.108) | g52+tb8 1.007; g56d6+tb8 1.108; g52+g19 0.994; g56d6+g22d4 1.101 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^18 separate I=1 | FFHT 0.5037 (textbook 1.122, textbook-bal 1.232) | g52+tb8 1.114; g56d6+tb8 1.199; g52+g19 1.076; g56d6+g22d4 1.181 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1 | FFHT 0.5617 (textbook 1.127, textbook-bal 1.221) | g52+tb8 1.125; g56d6+tb8 1.211; g52+g19 1.118; g56d6+g22d4 1.210 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^22 separate I=1 | FFHT 0.6289 (textbook 1.124, textbook-bal 1.212) | g52+tb8 1.120; g56d6+tb8 1.199; g52+g19 1.106; g56d6+g22d4 1.199 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1 | FFHT 0.7267 (textbook 1.363, textbook-bal 1.433) | g52+tb8 1.345; g56d6+tb8 1.435; g52+g19 1.366; g56d6+g22d4 1.444 |
| whole_sep_clang_avx2_f64: x86 whole 256bit-f64 2^10 separate I=1 | FFHT 0.5866 (textbook 1.043, textbook-bal 1.158) | g52+tb8 1.024; g56d6+tb8 1.182; g52+g19 1.018; g56d6+g22d4 1.190 |
| whole_sep_clang_avx2_f64: x86 whole 256bit-f64 2^12 separate I=1 | FFHT 0.7509 (textbook 1.045, textbook-bal 1.136) | g52+tb8 1.036; g56d6+tb8 1.161; g52+g19 1.033; g56d6+g22d4 1.160 |
| whole_sep_clang_avx2_f64: x86 whole 256bit-f64 2^14 separate I=1 | FFHT 0.8473 (textbook 1.049, textbook-bal 1.133) | g52+tb8 1.044; g56d6+tb8 1.153; g52+g19 1.042; g56d6+g22d4 1.153 |
| whole_sep_clang_avx2_f64: x86 whole 256bit-f64 2^16 separate I=1 | FFHT 0.8243 (textbook 1.178, textbook-bal 1.259) | g52+tb8 1.174; g56d6+tb8 1.287; g52+g19 1.158; g56d6+g22d4 1.276 |
| whole_sep_clang_avx2_f64: x86 whole 256bit-f64 2^18 separate I=1 | FFHT 1.0005 (textbook 1.072, textbook-bal 1.140) | g52+tb8 1.072; g56d6+tb8 1.165; g52+g19 1.068; g56d6+g22d4 1.161 |
| whole_sep_clang_avx2_f64: x86 whole 256bit-f64 2^20 separate I=1 | FFHT 1.2149 (textbook 1.001, textbook-bal 1.059) | g52+tb8 0.994; g56d6+tb8 1.071; g52+g19 0.980; g56d6+g22d4 1.057 |
| whole_sep_clang_avx2_f64: x86 whole 256bit-f64 2^22 separate I=1 | FFHT 1.1679 (textbook 1.413, textbook-bal 1.492) | g52+tb8 1.419; g56d6+tb8 1.494; g52+g19 1.393; g56d6+g22d4 1.481 |
| whole_sep_clang_avx2_f64: x86 whole 256bit-f64 2^24 separate I=1 | FFHT 1.4700 (textbook 1.360, textbook-bal 1.412) | g52+tb8 1.371; g56d6+tb8 1.433; g52+g19 1.365; g56d6+g22d4 1.439 |
| whole_sep_clang_avx2r32_f32: x86 whole 256bit-f32 2^10 separate I=1 | textbook 0.3425 (textbook-bal 1.028, FFHT 1.094) | g52+tb8 1.023; g56d6+tb8 1.018; g52+g19 1.005; g56d6+g22d4 1.010 |
| whole_sep_clang_avx2r32_f32: x86 whole 256bit-f32 2^12 separate I=1 | FFHT 0.3686 (textbook 1.087, textbook-bal 1.085) | g52+tb8 1.055; g56d6+tb8 1.049; g52+g19 1.058; g56d6+g22d4 1.063 |
| whole_sep_clang_avx2r32_f32: x86 whole 256bit-f32 2^14 separate I=1 | FFHT 0.4282 (textbook 1.119, textbook-bal 1.117) | g52+tb8 1.095; g56d6+tb8 1.094; g52+g19 1.095; g56d6+g22d4 1.093 |
| whole_sep_clang_avx2r32_f32: x86 whole 256bit-f32 2^16 separate I=1 | textbook-bal 0.4897 (textbook 1.008, FFHT 1.004) | g52+tb8 0.984; g56d6+tb8 0.985; g52+g19 0.970; g56d6+g22d4 0.972 |
| whole_sep_clang_avx2r32_f32: x86 whole 256bit-f32 2^18 separate I=1 | FFHT 0.5001 (textbook 1.113, textbook-bal 1.094) | g52+tb8 1.080; g56d6+tb8 1.068; g52+g19 1.058; g56d6+g22d4 1.051 |
| whole_sep_clang_avx2r32_f32: x86 whole 256bit-f32 2^20 separate I=1 | FFHT 0.5585 (textbook 1.117, textbook-bal 1.113) | g52+tb8 1.099; g56d6+tb8 1.094; g52+g19 1.094; g56d6+g22d4 1.091 |
| whole_sep_clang_avx2r32_f32: x86 whole 256bit-f32 2^22 separate I=1 | FFHT 0.6281 (textbook 1.108, textbook-bal 1.106) | g52+tb8 1.092; g56d6+tb8 1.086; g52+g19 1.093; g56d6+g22d4 1.081 |
| whole_sep_clang_avx2r32_f32: x86 whole 256bit-f32 2^24 separate I=1 | FFHT 0.7208 (textbook 1.357, textbook-bal 1.357) | g52+tb8 1.326; g56d6+tb8 1.338; g52+g19 1.351; g56d6+g22d4 1.349 |
| whole_sep_clang_avx512_f32: x86 whole 512bit-f32 2^10 separate I=1 | textbook-bal 0.3170 (textbook 1.025, FFHT 1.192) | g52+tb8 1.018; g56d6+tb8 1.020; g52+g19 1.028; g56d6+g22d4 1.037 |
| whole_sep_clang_avx512_f32: x86 whole 512bit-f32 2^12 separate I=1 | textbook-bal 0.3380 (textbook 1.054, FFHT 1.092) | g52+tb8 0.970; g56d6+tb8 1.004; g52+g19 0.971; g56d6+g22d4 1.009 |
| whole_sep_clang_avx512_f32: x86 whole 512bit-f32 2^14 separate I=1 | FFHT 0.4294 (textbook 1.082, textbook-bal 1.035) | g52+tb8 1.023; g56d6+tb8 1.036; g52+g19 1.025; g56d6+g22d4 1.038 |
| whole_sep_clang_avx512_f32: x86 whole 512bit-f32 2^16 separate I=1 | textbook-bal 0.4594 (textbook 1.044, FFHT 1.078) | g52+tb8 0.988; g56d6+tb8 0.998; g52+g19 0.974; g56d6+g22d4 0.986 |
| whole_sep_clang_avx512_f32: x86 whole 512bit-f32 2^18 separate I=1 | FFHT 0.5012 (textbook 1.085, textbook-bal 1.036) | g52+tb8 1.020; g56d6+tb8 1.022; g52+g19 1.006; g56d6+g22d4 1.003 |
| whole_sep_clang_avx512_f32: x86 whole 512bit-f32 2^20 separate I=1 | FFHT 0.5589 (textbook 1.086, textbook-bal 1.060) | g52+tb8 1.041; g56d6+tb8 1.049; g52+g19 1.042; g56d6+g22d4 1.052 |
| whole_sep_clang_avx512_f32: x86 whole 512bit-f32 2^22 separate I=1 | FFHT 0.6302 (textbook 1.067, textbook-bal 1.045) | g52+tb8 1.025; g56d6+tb8 1.031; g52+g19 1.033; g56d6+g22d4 1.037 |
| whole_sep_clang_avx512_f32: x86 whole 512bit-f32 2^24 separate I=1 | FFHT 0.7295 (textbook 1.301, textbook-bal 1.273) | g52+tb8 1.253; g56d6+tb8 1.276; g52+g19 1.282; g56d6+g22d4 1.292 |
| whole_sep_clang_avx512_f64: x86 whole 512bit-f64 2^10 separate I=1 | textbook-bal 0.5562 (textbook 1.028, FFHT 1.024) | g52+tb8 1.019; g56d6+tb8 1.015; g52+g19 0.986; g56d6+g22d4 1.001 |
| whole_sep_clang_avx512_f64: x86 whole 512bit-f64 2^12 separate I=1 | textbook-bal 0.7267 (textbook 1.047, FFHT 1.033) | g52+tb8 0.988; g56d6+tb8 1.004; g52+g19 0.989; g56d6+g22d4 1.005 |
| whole_sep_clang_avx512_f64: x86 whole 512bit-f64 2^14 separate I=1 | textbook-bal 0.8268 (textbook 1.046, FFHT 1.035) | g52+tb8 0.986; g56d6+tb8 1.007; g52+g19 0.988; g56d6+g22d4 1.005 |
| whole_sep_clang_avx512_f64: x86 whole 512bit-f64 2^16 separate I=1 | FFHT 0.8250 (textbook 1.147, textbook-bal 1.105) | g52+tb8 1.086; g56d6+tb8 1.106; g52+g19 1.074; g56d6+g22d4 1.098 |
| whole_sep_clang_avx512_f64: x86 whole 512bit-f64 2^18 separate I=1 | FFHT 0.9953 (textbook 1.043, textbook-bal 1.018) | g52+tb8 0.992; g56d6+tb8 1.015; g52+g19 0.994; g56d6+g22d4 1.020 |
| whole_sep_clang_avx512_f64: x86 whole 512bit-f64 2^20 separate I=1 | textbook-bal 1.1451 (textbook 1.022, FFHT 1.053) | g52+tb8 0.979; g56d6+tb8 0.994; g52+g19 0.986; g56d6+g22d4 0.995 |
| whole_sep_clang_avx512_f64: x86 whole 512bit-f64 2^22 separate I=1 | FFHT 1.1859 (textbook 1.360, textbook-bal 1.322) | g52+tb8 1.308; g56d6+tb8 1.330; g52+g19 1.325; g56d6+g22d4 1.313 |
| whole_sep_clang_avx512_f64: x86 whole 512bit-f64 2^24 separate I=1 | FFHT 1.4787 (textbook 1.294, textbook-bal 1.260) | g52+tb8 1.265; g56d6+tb8 1.274; g52+g19 1.269; g56d6+g22d4 1.277 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^10 separate I=1 | textbook 0.3226 (textbook-bal 1.067, FFHT 1.081) | g52+tb8 0.973; g56d6+tb8 1.016; g52+g19 0.957; g56d6+g22d4 1.011 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1 | FFHT 0.3691 (textbook 1.025, textbook-bal 1.118) | g52+tb8 0.938; g56d6+tb8 0.996; g52+g19 0.941; g56d6+g22d4 1.005 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^14 separate I=1 | FFHT 0.4302 (textbook 1.072, textbook-bal 1.158) | g52+tb8 1.004; g56d6+tb8 1.054; g52+g19 1.006; g56d6+g22d4 1.057 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1 | textbook 0.4754 (textbook-bal 1.066, FFHT 1.049) | g52+tb8 0.942; g56d6+tb8 0.986; g52+g19 0.926; g56d6+g22d4 0.987 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^18 separate I=1 | FFHT 0.5060 (textbook 1.068, textbook-bal 1.106) | g52+tb8 0.989; g56d6+tb8 1.025; g52+g19 0.976; g56d6+g22d4 1.028 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1 | FFHT 0.5655 (textbook 1.069, textbook-bal 1.140) | g52+tb8 1.015; g56d6+tb8 1.050; g52+g19 1.011; g56d6+g22d4 1.066 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^22 separate I=1 | FFHT 0.6263 (textbook 1.091, textbook-bal 1.167) | g52+tb8 1.054; g56d6+tb8 1.089; g52+g19 1.044; g56d6+g22d4 1.106 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1 | FFHT 0.7328 (textbook 1.318, textbook-bal 1.394) | g52+tb8 1.298; g56d6+tb8 1.319; g52+g19 1.287; g56d6+g22d4 1.326 |
| whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^10 separate I=1 | textbook 0.5586 (textbook-bal 1.130, FFHT 1.005) | g52+tb8 0.897; g56d6+tb8 0.972; g52+g19 0.900; g56d6+g22d4 0.979 |
| whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^12 separate I=1 | textbook 0.7391 (textbook-bal 1.107, FFHT 1.026) | g52+tb8 0.931; g56d6+tb8 0.986; g52+g19 0.927; g56d6+g22d4 0.986 |
| whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^14 separate I=1 | textbook 0.8511 (textbook-bal 1.092, FFHT 1.013) | g52+tb8 0.937; g56d6+tb8 0.990; g52+g19 0.938; g56d6+g22d4 0.990 |
| whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^16 separate I=1 | FFHT 0.8279 (textbook 1.120, textbook-bal 1.197) | g52+tb8 1.054; g56d6+tb8 1.104; g52+g19 1.038; g56d6+g22d4 1.107 |
| whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^18 separate I=1 | textbook 1.0214 (textbook-bal 1.075, FFHT 1.013) | g52+tb8 0.945; g56d6+tb8 0.991; g52+g19 0.959; g56d6+g22d4 1.048 |
| whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^20 separate I=1 | FFHT 1.1231 (textbook 1.045, textbook-bal 1.119) | g52+tb8 0.995; g56d6+tb8 1.036; g52+g19 0.986; g56d6+g22d4 1.040 |
| whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^22 separate I=1 | FFHT 1.1866 (textbook 1.394, textbook-bal 1.459) | g52+tb8 1.346; g56d6+tb8 1.366; g52+g19 1.308; g56d6+g22d4 1.362 |
| whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^24 separate I=1 | FFHT 1.4857 (textbook 1.325, textbook-bal 1.394) | g52+tb8 1.290; g56d6+tb8 1.323; g52+g19 1.285; g56d6+g22d4 1.334 |
| whole_sep_gcc_avx2r32_f32: x86 whole 256bit-f32 2^10 separate I=1 | textbook 0.3181 (textbook-bal 1.017, FFHT 1.095) | g52+tb8 0.975; g56d6+tb8 0.985; g52+g19 0.961; g56d6+g22d4 0.978 |
| whole_sep_gcc_avx2r32_f32: x86 whole 256bit-f32 2^12 separate I=1 | textbook-bal 0.3570 (textbook 1.045, FFHT 1.034) | g52+tb8 0.949; g56d6+tb8 0.970; g52+g19 0.957; g56d6+g22d4 0.973 |
| whole_sep_gcc_avx2r32_f32: x86 whole 256bit-f32 2^14 separate I=1 | FFHT 0.4282 (textbook 1.061, textbook-bal 1.034) | g52+tb8 0.987; g56d6+tb8 0.996; g52+g19 0.987; g56d6+g22d4 0.997 |
| whole_sep_gcc_avx2r32_f32: x86 whole 256bit-f32 2^16 separate I=1 | textbook-bal 0.4538 (textbook 1.026, FFHT 1.091) | g52+tb8 0.959; g56d6+tb8 0.963; g52+g19 0.944; g56d6+g22d4 0.964 |
| whole_sep_gcc_avx2r32_f32: x86 whole 256bit-f32 2^18 separate I=1 | FFHT 0.5043 (textbook 1.051, textbook-bal 1.021) | g52+tb8 0.963; g56d6+tb8 0.957; g52+g19 0.952; g56d6+g22d4 0.970 |
| whole_sep_gcc_avx2r32_f32: x86 whole 256bit-f32 2^20 separate I=1 | FFHT 0.5671 (textbook 1.050, textbook-bal 1.042) | g52+tb8 0.995; g56d6+tb8 0.998; g52+g19 0.986; g56d6+g22d4 1.010 |
| whole_sep_gcc_avx2r32_f32: x86 whole 256bit-f32 2^22 separate I=1 | FFHT 0.6209 (textbook 1.076, textbook-bal 1.069) | g52+tb8 1.023; g56d6+tb8 1.015; g52+g19 1.021; g56d6+g22d4 1.054 |
| whole_sep_gcc_avx2r32_f32: x86 whole 256bit-f32 2^24 separate I=1 | FFHT 0.7223 (textbook 1.315, textbook-bal 1.298) | g52+tb8 1.280; g56d6+tb8 1.286; g52+g19 1.277; g56d6+g22d4 1.294 |
| whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^10 separate I=1 | textbook-bal 0.3307 (textbook 1.020, FFHT 1.053) | g52+tb8 0.990; g56d6+tb8 0.995; g52+g19 0.999; g56d6+g22d4 1.011 |
| whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^12 separate I=1 | textbook-bal 0.3316 (textbook 1.089, FFHT 1.113) | g52+tb8 0.965; g56d6+tb8 1.000; g52+g19 0.971; g56d6+g22d4 1.006 |
| whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^14 separate I=1 | FFHT 0.4282 (textbook 1.078, textbook-bal 1.010) | g52+tb8 0.992; g56d6+tb8 1.006; g52+g19 0.992; g56d6+g22d4 1.009 |
| whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^16 separate I=1 | textbook-bal 0.4449 (textbook 1.069, FFHT 1.110) | g52+tb8 0.983; g56d6+tb8 1.000; g52+g19 0.968; g56d6+g22d4 0.986 |
| whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^18 separate I=1 | FFHT 0.5056 (textbook 1.069, textbook-bal 1.009) | g52+tb8 0.975; g56d6+tb8 0.971; g52+g19 0.962; g56d6+g22d4 0.979 |
| whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^20 separate I=1 | FFHT 0.5635 (textbook 1.075, textbook-bal 1.025) | g52+tb8 1.003; g56d6+tb8 1.017; g52+g19 1.005; g56d6+g22d4 1.023 |
| whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^22 separate I=1 | FFHT 0.6239 (textbook 1.071, textbook-bal 1.031) | g52+tb8 1.006; g56d6+tb8 1.016; g52+g19 1.019; g56d6+g22d4 1.043 |
| whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^24 separate I=1 | FFHT 0.7288 (textbook 1.296, textbook-bal 1.246) | g52+tb8 1.247; g56d6+tb8 1.279; g52+g19 1.283; g56d6+g22d4 1.283 |
| whole_sep_gcc_avx512_f64: x86 whole 512bit-f64 2^10 separate I=1 | textbook-bal 0.5462 (textbook 1.043, FFHT 1.023) | g52+tb8 0.983; g56d6+tb8 0.997; g52+g19 0.963; g56d6+g22d4 0.984 |
| whole_sep_gcc_avx512_f64: x86 whole 512bit-f64 2^12 separate I=1 | textbook-bal 0.6843 (textbook 1.079, FFHT 1.096) | g52+tb8 0.965; g56d6+tb8 0.992; g52+g19 0.966; g56d6+g22d4 0.996 |
| whole_sep_gcc_avx512_f64: x86 whole 512bit-f64 2^14 separate I=1 | textbook-bal 0.7808 (textbook 1.079, FFHT 1.087) | g52+tb8 0.973; g56d6+tb8 0.996; g52+g19 0.973; g56d6+g22d4 0.995 |
| whole_sep_gcc_avx512_f64: x86 whole 512bit-f64 2^16 separate I=1 | FFHT 0.8238 (textbook 1.120, textbook-bal 1.038) | g52+tb8 1.019; g56d6+tb8 1.040; g52+g19 1.005; g56d6+g22d4 1.027 |
| whole_sep_gcc_avx512_f64: x86 whole 512bit-f64 2^18 separate I=1 | textbook-bal 0.9573 (textbook 1.058, FFHT 1.048) | g52+tb8 0.978; g56d6+tb8 0.998; g52+g19 0.982; g56d6+g22d4 1.000 |
| whole_sep_gcc_avx512_f64: x86 whole 512bit-f64 2^20 separate I=1 | textbook-bal 1.0930 (textbook 1.047, FFHT 1.014) | g52+tb8 0.974; g56d6+tb8 0.989; g52+g19 0.977; g56d6+g22d4 0.999 |
| whole_sep_gcc_avx512_f64: x86 whole 512bit-f64 2^22 separate I=1 | FFHT 1.1852 (textbook 1.329, textbook-bal 1.281) | g52+tb8 1.250; g56d6+tb8 1.260; g52+g19 1.258; g56d6+g22d4 1.264 |
| whole_sep_gcc_avx512_f64: x86 whole 512bit-f64 2^24 separate I=1 | FFHT 1.4646 (textbook 1.277, textbook-bal 1.244) | g52+tb8 1.236; g56d6+tb8 1.246; g52+g19 1.240; g56d6+g22d4 1.252 |

## Port balancing alone (the textbook with half its adds as FMA by 1, against the plain textbook and FFHT)

A second lead, independent of the circuits: if the balanced textbook is 10 % or more faster than both the plain
textbook and FFHT in whole transforms, an x86 WHT library (FFHT, used by SpinQuant on x86) gains by balancing alone.

- pass16_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.259
- pass16_I1_clang_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.255
- pass16_I1_clang_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.824
- pass16_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.880
- pass16_I1_clang_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 1 S=96 (12 KB): balanced / best other textbook-or-FFHT = 0.868
- pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.151
- pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.156
- pass16_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.759
- pass16_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.739
- pass16_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 1 S=96 (12 KB): balanced / best other textbook-or-FFHT = 0.757
- pass16_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.209
- pass16_I2_clang_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 2 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.119
- pass16_I2_clang_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.937
- pass16_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.802
- pass16_I2_clang_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB): balanced / best other textbook-or-FFHT = 0.759
- pass16_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.330
- pass16_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 2 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.335
- pass16_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.150
- pass16_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.049
- pass16_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.060
- pass16_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.033
- pass16_I3_clang_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 3 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.016
- pass16_I3_clang_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.041
- pass16_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.801
- pass16_I3_clang_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 3 S=96 (12 KB): balanced / best other textbook-or-FFHT = 0.803
- pass16_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.322
- pass16_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 3 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.331
- pass16_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.058
- pass16_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.024
- pass16_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 3 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.105
- pass16_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.089
- pass16_I4_clang_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 4 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.094
- pass16_I4_clang_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.991
- pass16_I4_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.920
- pass16_I4_clang_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 4 S=96 (12 KB): balanced / best other textbook-or-FFHT = 0.917
- pass16_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.065
- pass16_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 4 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.065
- pass16_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.915
- pass16_I4_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.903
- pass16_I4_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 4 S=96 (12 KB): balanced / best other textbook-or-FFHT = 0.916
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.847
- pass8_I1_clang_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): balanced / best other textbook-or-FFHT = 0.846
- pass8_I1_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.844
- pass8_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): balanced / best other textbook-or-FFHT = 0.947
- pass8_I1_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.946
- pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.844
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): balanced / best other textbook-or-FFHT = 0.889
- pass8_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.871
- pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): balanced / best other textbook-or-FFHT = 0.936
- pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.936
- pass8_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.163
- pass8_I2_clang_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.115
- pass8_I2_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.898
- pass8_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): balanced / best other textbook-or-FFHT = 0.958
- pass8_I2_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.963
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.131
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.132
- pass8_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.837
- pass8_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): balanced / best other textbook-or-FFHT = 0.863
- pass8_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.861
- pass8_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.109
- pass8_I3_clang_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 3 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.100
- pass8_I3_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.924
- pass8_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): balanced / best other textbook-or-FFHT = 0.977
- pass8_I3_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.971
- pass8_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.271
- pass8_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 3 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.276
- pass8_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.898
- pass8_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): balanced / best other textbook-or-FFHT = 0.975
- pass8_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.975
- pass8_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.117
- pass8_I4_clang_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 4 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.059
- pass8_I4_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.007
- pass8_I4_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 4 S=384 (12 KB): balanced / best other textbook-or-FFHT = 0.902
- pass8_I4_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.830
- pass8_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.377
- pass8_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 4 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.360
- pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.093
- pass8_I4_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 4 S=384 (12 KB): balanced / best other textbook-or-FFHT = 1.175
- pass8_I4_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.207
- regs16_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 1.174
- regs16_I1_clang_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 1.174
- regs16_I1_clang_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.642
- regs16_I1_clang_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.611
- regs16_I1_clang_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.611
- regs16_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.984
- regs16_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.985
- regs16_I1_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.635
- regs16_I1_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.532
- regs16_I1_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.532
- regs16_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 1.345
- regs16_I2_clang_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 1.351
- regs16_I2_clang_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 0.581
- regs16_I2_clang_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 0.690
- regs16_I2_clang_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 0.688
- regs16_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 1.155
- regs16_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 1.156
- regs16_I2_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 0.680
- regs16_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 0.644
- regs16_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 0.644
- regs8_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.955
- regs8_I1_clang_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.955
- regs8_I1_clang_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.955
- regs8_I1_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.733
- regs8_I1_clang_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.733
- regs8_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.974
- regs8_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.973
- regs8_I1_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.975
- regs8_I1_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.664
- regs8_I1_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 0.664
- regs8_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 1.376
- regs8_I2_clang_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 1.374
- regs8_I2_clang_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 0.582
- regs8_I2_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 0.617
- regs8_I2_clang_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 0.617
- regs8_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 0.942
- regs8_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 0.941
- regs8_I2_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 0.619
- regs8_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 0.577
- regs8_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 0.576
- regs8_I3_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 0.993
- regs8_I3_clang_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 0.995
- regs8_I3_clang_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 0.508
- regs8_I3_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 0.547
- regs8_I3_clang_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 0.547
- regs8_I3_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 1.114
- regs8_I3_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 1.115
- regs8_I3_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 0.886
- regs8_I3_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 0.851
- regs8_I3_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 0.852
- regs8_I4_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.087
- regs8_I4_clang_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.079
- regs8_I4_clang_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 0.679
- regs8_I4_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 0.549
- regs8_I4_clang_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 0.935
- regs8_I4_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.111
- regs8_I4_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.111
- regs8_I4_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 0.973
- regs8_I4_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.122
- regs8_I4_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.124
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^6 same I=2: balanced / best other textbook-or-FFHT = 2.128 (FFHT 0.2931, plain textbook 0.5317, balanced 0.6238 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^7 same I=2: balanced / best other textbook-or-FFHT = 1.305 (FFHT 0.3097, plain textbook 0.3568, balanced 0.4043 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^8 same I=2: balanced / best other textbook-or-FFHT = 1.256 (FFHT 0.3026, plain textbook 0.3531, balanced 0.3800 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^9 same I=2: balanced / best other textbook-or-FFHT = 1.153 (FFHT 0.3077, plain textbook 0.3293, balanced 0.3548 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^10 same I=2: balanced / best other textbook-or-FFHT = 1.058 (FFHT 0.3879, plain textbook 0.3489, balanced 0.3690 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^11 same I=2: balanced / best other textbook-or-FFHT = 1.268 (FFHT 0.3443, plain textbook 0.3784, balanced 0.4365 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^12 same I=2: balanced / best other textbook-or-FFHT = 1.311 (FFHT 0.3598, plain textbook 0.4397, balanced 0.4717 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^13 same I=2: balanced / best other textbook-or-FFHT = 1.229 (FFHT 0.3848, plain textbook 0.4380, balanced 0.4729 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^14 same I=2: balanced / best other textbook-or-FFHT = 1.345 (FFHT 0.4007, plain textbook 0.4689, balanced 0.5388 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^15 same I=2: balanced / best other textbook-or-FFHT = 1.201 (FFHT 0.4342, plain textbook 0.4595, balanced 0.5213 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^16 same I=2: balanced / best other textbook-or-FFHT = 1.125 (FFHT 0.7563, plain textbook 0.4855, balanced 0.5462 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^17 same I=2: balanced / best other textbook-or-FFHT = 1.289 (FFHT 0.4582, plain textbook 0.5239, balanced 0.5907 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^18 same I=2: balanced / best other textbook-or-FFHT = 1.249 (FFHT 0.4768, plain textbook 0.5866, balanced 0.5953 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^19 same I=2: balanced / best other textbook-or-FFHT = 1.244 (FFHT 0.5149, plain textbook 0.5713, balanced 0.6407 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^20 same I=2: balanced / best other textbook-or-FFHT = 1.297 (FFHT 0.5302, plain textbook 0.6186, balanced 0.6879 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^21 same I=2: balanced / best other textbook-or-FFHT = 1.189 (FFHT 0.5822, plain textbook 0.6217, balanced 0.6920 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^22 same I=2: balanced / best other textbook-or-FFHT = 1.256 (FFHT 0.5896, plain textbook 0.6614, balanced 0.7404 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^23 same I=2: balanced / best other textbook-or-FFHT = 1.318 (FFHT 0.6845, plain textbook 0.8404, balanced 0.9024 ns)
- whole_same_I2_clang_avx2_f32: x86 whole 256bit-f32 2^24 same I=2: balanced / best other textbook-or-FFHT = 1.402 (FFHT 0.7303, plain textbook 0.9683, balanced 1.0242 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^6 same I=2: balanced / best other textbook-or-FFHT = 1.510 (FFHT 0.4913, plain textbook 0.6364, balanced 0.7420 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^7 same I=2: balanced / best other textbook-or-FFHT = 1.537 (FFHT 0.4536, plain textbook 0.6163, balanced 0.6974 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^8 same I=2: balanced / best other textbook-or-FFHT = 1.228 (FFHT 0.4788, plain textbook 0.5288, balanced 0.5880 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^9 same I=2: balanced / best other textbook-or-FFHT = 1.503 (FFHT 0.5462, plain textbook 0.5706, balanced 0.8212 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^10 same I=2: balanced / best other textbook-or-FFHT = 1.261 (FFHT 0.5413, plain textbook 0.6080, balanced 0.6828 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^11 same I=2: balanced / best other textbook-or-FFHT = 1.301 (FFHT 0.5732, plain textbook 0.6815, balanced 0.7459 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^12 same I=2: balanced / best other textbook-or-FFHT = 1.185 (FFHT 0.6464, plain textbook 0.6909, balanced 0.7659 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^13 same I=2: balanced / best other textbook-or-FFHT = 1.287 (FFHT 0.6549, plain textbook 0.7815, balanced 0.8429 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^14 same I=2: balanced / best other textbook-or-FFHT = 1.173 (FFHT 0.7236, plain textbook 0.7768, balanced 0.8486 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^15 same I=2: balanced / best other textbook-or-FFHT = 1.516 (FFHT 0.7550, plain textbook 0.8202, balanced 1.1443 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^16 same I=2: balanced / best other textbook-or-FFHT = 1.582 (FFHT 0.7692, plain textbook 0.9074, balanced 1.2169 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^17 same I=2: balanced / best other textbook-or-FFHT = 1.531 (FFHT 0.8057, plain textbook 0.9227, balanced 1.2335 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^18 same I=2: balanced / best other textbook-or-FFHT = 1.738 (FFHT 0.8882, plain textbook 1.0008, balanced 1.5438 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^19 same I=2: balanced / best other textbook-or-FFHT = 1.775 (FFHT 0.9272, plain textbook 1.1060, balanced 1.6459 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^20 same I=2: balanced / best other textbook-or-FFHT = 1.477 (FFHT 1.1427, plain textbook 1.1124, balanced 1.6428 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^21 same I=2: balanced / best other textbook-or-FFHT = 1.812 (FFHT 1.0769, plain textbook 1.1796, balanced 1.9513 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^22 same I=2: balanced / best other textbook-or-FFHT = 1.855 (FFHT 1.1653, plain textbook 1.5206, balanced 2.1612 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^23 same I=2: balanced / best other textbook-or-FFHT = 1.741 (FFHT 1.3094, plain textbook 1.7972, balanced 2.2802 ns)
- whole_same_I2_clang_avx2_f64: x86 whole 256bit-f64 2^24 same I=2: balanced / best other textbook-or-FFHT = 1.709 (FFHT 1.4738, plain textbook 2.0187, balanced 2.5184 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^6 same I=2: balanced / best other textbook-or-FFHT = 2.156 (FFHT 0.2930, plain textbook 0.5220, balanced 0.6316 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^7 same I=2: balanced / best other textbook-or-FFHT = 1.265 (FFHT 0.3093, plain textbook 0.3577, balanced 0.3914 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^8 same I=2: balanced / best other textbook-or-FFHT = 1.262 (FFHT 0.2990, plain textbook 0.3534, balanced 0.3772 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^9 same I=2: balanced / best other textbook-or-FFHT = 1.104 (FFHT 0.3078, plain textbook 0.3266, balanced 0.3397 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^10 same I=2: balanced / best other textbook-or-FFHT = 1.031 (FFHT 0.3476, plain textbook 0.3323, balanced 0.3427 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^11 same I=2: balanced / best other textbook-or-FFHT = 1.029 (FFHT 0.3446, plain textbook 0.3497, balanced 0.3545 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^12 same I=2: balanced / best other textbook-or-FFHT = 1.088 (FFHT 0.3605, plain textbook 0.3854, balanced 0.3921 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^13 same I=2: balanced / best other textbook-or-FFHT = 1.023 (FFHT 0.3860, plain textbook 0.3882, balanced 0.3950 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^14 same I=2: balanced / best other textbook-or-FFHT = 1.090 (FFHT 0.4015, plain textbook 0.4310, balanced 0.4378 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^15 same I=2: balanced / best other textbook-or-FFHT = 1.022 (FFHT 0.4354, plain textbook 0.4274, balanced 0.4368 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^16 same I=2: balanced / best other textbook-or-FFHT = 1.015 (FFHT 0.4524, plain textbook 0.4433, balanced 0.4501 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^17 same I=2: balanced / best other textbook-or-FFHT = 1.070 (FFHT 0.4588, plain textbook 0.4827, balanced 0.4911 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^18 same I=2: balanced / best other textbook-or-FFHT = 1.056 (FFHT 0.4819, plain textbook 0.4918, balanced 0.5089 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^19 same I=2: balanced / best other textbook-or-FFHT = 1.030 (FFHT 0.5232, plain textbook 0.5162, balanced 0.5317 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^20 same I=2: balanced / best other textbook-or-FFHT = 1.075 (FFHT 0.5409, plain textbook 0.5623, balanced 0.5813 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^21 same I=2: balanced / best other textbook-or-FFHT = 1.026 (FFHT 0.5869, plain textbook 0.5673, balanced 0.5821 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^22 same I=2: balanced / best other textbook-or-FFHT = 1.035 (FFHT 0.5903, plain textbook 0.5903, balanced 0.6109 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^23 same I=2: balanced / best other textbook-or-FFHT = 1.151 (FFHT 0.6861, plain textbook 0.7892, balanced 0.7895 ns)
- whole_same_I2_clang_avx2r32_f32: x86 whole 256bit-f32 2^24 same I=2: balanced / best other textbook-or-FFHT = 1.297 (FFHT 0.7188, plain textbook 0.9241, balanced 0.9324 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^6 same I=2: balanced / best other textbook-or-FFHT = 1.982 (FFHT 0.2932, plain textbook 0.4993, balanced 0.5811 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^7 same I=2: balanced / best other textbook-or-FFHT = 1.125 (FFHT 0.3157, plain textbook 0.3416, balanced 0.3553 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^8 same I=2: balanced / best other textbook-or-FFHT = 1.035 (FFHT 0.2983, plain textbook 0.2962, balanced 0.3067 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^9 same I=2: balanced / best other textbook-or-FFHT = 1.040 (FFHT 0.3077, plain textbook 0.3279, balanced 0.3199 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^10 same I=2: balanced / best other textbook-or-FFHT = 0.961 (FFHT 0.3471, plain textbook 0.3184, balanced 0.3059 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^11 same I=2: balanced / best other textbook-or-FFHT = 0.969 (FFHT 0.3437, plain textbook 0.3241, balanced 0.3140 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^12 same I=2: balanced / best other textbook-or-FFHT = 0.927 (FFHT 0.3599, plain textbook 0.3632, balanced 0.3335 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^13 same I=2: balanced / best other textbook-or-FFHT = 0.981 (FFHT 0.3847, plain textbook 0.4051, balanced 0.3773 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^14 same I=2: balanced / best other textbook-or-FFHT = 1.037 (FFHT 0.4009, plain textbook 0.4482, balanced 0.4157 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^15 same I=2: balanced / best other textbook-or-FFHT = 0.949 (FFHT 0.4341, plain textbook 0.4430, balanced 0.4120 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^16 same I=2: balanced / best other textbook-or-FFHT = 0.944 (FFHT 0.4507, plain textbook 0.4589, balanced 0.4254 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^17 same I=2: balanced / best other textbook-or-FFHT = 1.018 (FFHT 0.4576, plain textbook 0.4977, balanced 0.4657 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^18 same I=2: balanced / best other textbook-or-FFHT = 1.004 (FFHT 0.4776, plain textbook 0.5142, balanced 0.4797 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^19 same I=2: balanced / best other textbook-or-FFHT = 0.962 (FFHT 0.5614, plain textbook 0.5274, balanced 0.5075 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^20 same I=2: balanced / best other textbook-or-FFHT = 1.043 (FFHT 0.5314, plain textbook 0.5747, balanced 0.5541 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^21 same I=2: balanced / best other textbook-or-FFHT = 0.956 (FFHT 0.5852, plain textbook 0.5816, balanced 0.5562 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^22 same I=2: balanced / best other textbook-or-FFHT = 0.987 (FFHT 0.5894, plain textbook 0.6005, balanced 0.5817 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^23 same I=2: balanced / best other textbook-or-FFHT = 1.108 (FFHT 0.6891, plain textbook 0.7900, balanced 0.7637 ns)
- whole_same_I2_clang_avx512_f32: x86 whole 512bit-f32 2^24 same I=2: balanced / best other textbook-or-FFHT = 1.232 (FFHT 0.7214, plain textbook 0.9224, balanced 0.8890 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^6 same I=2: balanced / best other textbook-or-FFHT = 1.275 (FFHT 0.4961, plain textbook 0.5399, balanced 0.6325 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^7 same I=2: balanced / best other textbook-or-FFHT = 1.102 (FFHT 0.4548, plain textbook 0.4990, balanced 0.5010 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^8 same I=2: balanced / best other textbook-or-FFHT = 1.148 (FFHT 0.4716, plain textbook 0.5517, balanced 0.5416 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^9 same I=2: balanced / best other textbook-or-FFHT = 0.963 (FFHT 0.5475, plain textbook 0.5336, balanced 0.5140 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^10 same I=2: balanced / best other textbook-or-FFHT = 0.982 (FFHT 0.5410, plain textbook 0.5539, balanced 0.5313 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^11 same I=2: balanced / best other textbook-or-FFHT = 0.983 (FFHT 0.5730, plain textbook 0.6319, balanced 0.5634 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^12 same I=2: balanced / best other textbook-or-FFHT = 1.009 (FFHT 0.6472, plain textbook 0.7132, balanced 0.6530 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^13 same I=2: balanced / best other textbook-or-FFHT = 1.127 (FFHT 0.6553, plain textbook 0.8032, balanced 0.7385 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^14 same I=2: balanced / best other textbook-or-FFHT = 1.005 (FFHT 0.7248, plain textbook 0.7907, balanced 0.7285 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^15 same I=2: balanced / best other textbook-or-FFHT = 1.004 (FFHT 0.7543, plain textbook 0.8216, balanced 0.7576 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^16 same I=2: balanced / best other textbook-or-FFHT = 1.082 (FFHT 0.7696, plain textbook 0.9002, balanced 0.8327 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^17 same I=2: balanced / best other textbook-or-FFHT = 1.054 (FFHT 0.8156, plain textbook 0.9171, balanced 0.8599 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^18 same I=2: balanced / best other textbook-or-FFHT = 1.030 (FFHT 0.8875, plain textbook 0.9647, balanced 0.9139 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^19 same I=2: balanced / best other textbook-or-FFHT = 1.111 (FFHT 0.9131, plain textbook 1.0553, balanced 1.0142 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^20 same I=2: balanced / best other textbook-or-FFHT = 0.959 (FFHT 1.1421, plain textbook 1.0607, balanced 1.0167 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^21 same I=2: balanced / best other textbook-or-FFHT = 1.009 (FFHT 1.0744, plain textbook 1.1313, balanced 1.0837 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^22 same I=2: balanced / best other textbook-or-FFHT = 1.272 (FFHT 1.1686, plain textbook 1.5393, balanced 1.4860 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^23 same I=2: balanced / best other textbook-or-FFHT = 1.304 (FFHT 1.3307, plain textbook 1.7849, balanced 1.7346 ns)
- whole_same_I2_clang_avx512_f64: x86 whole 512bit-f64 2^24 same I=2: balanced / best other textbook-or-FFHT = 1.269 (FFHT 1.4982, plain textbook 1.9631, balanced 1.9015 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^6 same I=2: balanced / best other textbook-or-FFHT = 2.281 (FFHT 0.2929, plain textbook 0.5491, balanced 0.6681 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^7 same I=2: balanced / best other textbook-or-FFHT = 1.345 (FFHT 0.3112, plain textbook 0.4346, balanced 0.4187 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^8 same I=2: balanced / best other textbook-or-FFHT = 1.307 (FFHT 0.2982, plain textbook 0.3431, balanced 0.3898 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^9 same I=2: balanced / best other textbook-or-FFHT = 1.107 (FFHT 0.3076, plain textbook 0.3090, balanced 0.3406 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^10 same I=2: balanced / best other textbook-or-FFHT = 1.129 (FFHT 0.3379, plain textbook 0.3109, balanced 0.3509 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^11 same I=2: balanced / best other textbook-or-FFHT = 1.118 (FFHT 0.3441, plain textbook 0.3628, balanced 0.3846 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^12 same I=2: balanced / best other textbook-or-FFHT = 1.161 (FFHT 0.3592, plain textbook 0.3715, balanced 0.4171 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^13 same I=2: balanced / best other textbook-or-FFHT = 1.135 (FFHT 0.3805, plain textbook 0.3719, balanced 0.4221 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^14 same I=2: balanced / best other textbook-or-FFHT = 1.158 (FFHT 0.4014, plain textbook 0.4175, balanced 0.4650 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^15 same I=2: balanced / best other textbook-or-FFHT = 1.122 (FFHT 0.4346, plain textbook 0.4115, balanced 0.4615 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^16 same I=2: balanced / best other textbook-or-FFHT = 1.181 (FFHT 0.4500, plain textbook 0.4297, balanced 0.5075 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^17 same I=2: balanced / best other textbook-or-FFHT = 1.177 (FFHT 0.4619, plain textbook 0.4736, balanced 0.5436 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^18 same I=2: balanced / best other textbook-or-FFHT = 1.144 (FFHT 0.4823, plain textbook 0.4812, balanced 0.5505 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^19 same I=2: balanced / best other textbook-or-FFHT = 1.179 (FFHT 0.5139, plain textbook 0.5106, balanced 0.6018 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^20 same I=2: balanced / best other textbook-or-FFHT = 1.220 (FFHT 0.5330, plain textbook 0.5613, balanced 0.6502 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^21 same I=2: balanced / best other textbook-or-FFHT = 1.207 (FFHT 0.5458, plain textbook 0.5630, balanced 0.6586 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^22 same I=2: balanced / best other textbook-or-FFHT = 1.196 (FFHT 0.5869, plain textbook 0.5957, balanced 0.7022 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^23 same I=2: balanced / best other textbook-or-FFHT = 1.332 (FFHT 0.6470, plain textbook 0.7877, balanced 0.8620 ns)
- whole_same_I2_gcc_avx2_f32: x86 whole 256bit-f32 2^24 same I=2: balanced / best other textbook-or-FFHT = 1.358 (FFHT 0.7277, plain textbook 0.9144, balanced 0.9881 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^6 same I=2: balanced / best other textbook-or-FFHT = 1.482 (FFHT 0.4931, plain textbook 0.6059, balanced 0.7309 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^7 same I=2: balanced / best other textbook-or-FFHT = 1.487 (FFHT 0.4531, plain textbook 0.5933, balanced 0.6738 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^8 same I=2: balanced / best other textbook-or-FFHT = 1.195 (FFHT 0.4725, plain textbook 0.4879, balanced 0.5647 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^9 same I=2: balanced / best other textbook-or-FFHT = 1.148 (FFHT 0.5339, plain textbook 0.5000, balanced 0.5742 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^10 same I=2: balanced / best other textbook-or-FFHT = 1.204 (FFHT 0.5403, plain textbook 0.5559, balanced 0.6504 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^11 same I=2: balanced / best other textbook-or-FFHT = 1.255 (FFHT 0.5720, plain textbook 0.6215, balanced 0.7181 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^12 same I=2: balanced / best other textbook-or-FFHT = 1.159 (FFHT 0.6468, plain textbook 0.6248, balanced 0.7240 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^13 same I=2: balanced / best other textbook-or-FFHT = 1.229 (FFHT 0.6565, plain textbook 0.7074, balanced 0.8070 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^14 same I=2: balanced / best other textbook-or-FFHT = 1.145 (FFHT 0.7240, plain textbook 0.6987, balanced 0.8002 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^15 same I=2: balanced / best other textbook-or-FFHT = 1.214 (FFHT 0.7538, plain textbook 0.7355, balanced 0.8931 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^16 same I=2: balanced / best other textbook-or-FFHT = 1.255 (FFHT 0.7683, plain textbook 0.8177, balanced 0.9641 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^17 same I=2: balanced / best other textbook-or-FFHT = 1.224 (FFHT 0.8064, plain textbook 0.8509, balanced 0.9870 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^18 same I=2: balanced / best other textbook-or-FFHT = 1.207 (FFHT 0.9636, plain textbook 0.9022, balanced 1.0892 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^19 same I=2: balanced / best other textbook-or-FFHT = 1.299 (FFHT 0.9169, plain textbook 0.9899, balanced 1.1910 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^20 same I=2: balanced / best other textbook-or-FFHT = 1.202 (FFHT 0.9990, plain textbook 1.0102, balanced 1.2010 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^21 same I=2: balanced / best other textbook-or-FFHT = 1.267 (FFHT 1.0457, plain textbook 1.0792, balanced 1.3245 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^22 same I=2: balanced / best other textbook-or-FFHT = 1.491 (FFHT 1.1547, plain textbook 1.4785, balanced 1.7217 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^23 same I=2: balanced / best other textbook-or-FFHT = 1.508 (FFHT 1.3096, plain textbook 1.7393, balanced 1.9753 ns)
- whole_same_I2_gcc_avx2_f64: x86 whole 256bit-f64 2^24 same I=2: balanced / best other textbook-or-FFHT = 1.544 (FFHT 1.4839, plain textbook 1.9498, balanced 2.2904 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^6 same I=2: balanced / best other textbook-or-FFHT = 1.999 (FFHT 0.2930, plain textbook 0.5020, balanced 0.5856 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^7 same I=2: balanced / best other textbook-or-FFHT = 1.217 (FFHT 0.3104, plain textbook 0.3474, balanced 0.3779 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^8 same I=2: balanced / best other textbook-or-FFHT = 1.174 (FFHT 0.2981, plain textbook 0.3376, balanced 0.3499 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^9 same I=2: balanced / best other textbook-or-FFHT = 1.057 (FFHT 0.3080, plain textbook 0.3032, balanced 0.3204 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^10 same I=2: balanced / best other textbook-or-FFHT = 1.007 (FFHT 0.3379, plain textbook 0.3087, balanced 0.3110 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^11 same I=2: balanced / best other textbook-or-FFHT = 1.044 (FFHT 0.3440, plain textbook 0.3253, balanced 0.3396 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^12 same I=2: balanced / best other textbook-or-FFHT = 1.036 (FFHT 0.3591, plain textbook 0.3589, balanced 0.3718 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^13 same I=2: balanced / best other textbook-or-FFHT = 1.052 (FFHT 0.3806, plain textbook 0.3586, balanced 0.3772 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^14 same I=2: balanced / best other textbook-or-FFHT = 1.045 (FFHT 0.4014, plain textbook 0.4017, balanced 0.4193 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^15 same I=2: balanced / best other textbook-or-FFHT = 1.040 (FFHT 0.4346, plain textbook 0.3999, balanced 0.4160 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^16 same I=2: balanced / best other textbook-or-FFHT = 1.043 (FFHT 0.4493, plain textbook 0.4139, balanced 0.4319 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^17 same I=2: balanced / best other textbook-or-FFHT = 1.075 (FFHT 0.4576, plain textbook 0.4531, balanced 0.4871 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^18 same I=2: balanced / best other textbook-or-FFHT = 1.041 (FFHT 0.4819, plain textbook 0.4701, balanced 0.4894 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^19 same I=2: balanced / best other textbook-or-FFHT = 1.054 (FFHT 0.5125, plain textbook 0.4875, balanced 0.5138 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^20 same I=2: balanced / best other textbook-or-FFHT = 1.054 (FFHT 0.5303, plain textbook 0.5351, balanced 0.5587 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^21 same I=2: balanced / best other textbook-or-FFHT = 1.045 (FFHT 0.5487, plain textbook 0.5377, balanced 0.5619 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^22 same I=2: balanced / best other textbook-or-FFHT = 1.059 (FFHT 0.5838, plain textbook 0.5632, balanced 0.5964 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^23 same I=2: balanced / best other textbook-or-FFHT = 1.207 (FFHT 0.6568, plain textbook 0.7596, balanced 0.7926 ns)
- whole_same_I2_gcc_avx2r32_f32: x86 whole 256bit-f32 2^24 same I=2: balanced / best other textbook-or-FFHT = 1.261 (FFHT 0.7232, plain textbook 0.8856, balanced 0.9121 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^6 same I=2: balanced / best other textbook-or-FFHT = 1.830 (FFHT 0.3062, plain textbook 0.5098, balanced 0.5604 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^7 same I=2: balanced / best other textbook-or-FFHT = 1.352 (FFHT 0.3102, plain textbook 0.3921, balanced 0.4193 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^8 same I=2: balanced / best other textbook-or-FFHT = 1.131 (FFHT 0.2979, plain textbook 0.3367, balanced 0.3370 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^9 same I=2: balanced / best other textbook-or-FFHT = 1.097 (FFHT 0.3070, plain textbook 0.3460, balanced 0.3368 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^10 same I=2: balanced / best other textbook-or-FFHT = 0.980 (FFHT 0.3376, plain textbook 0.3294, balanced 0.3229 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^11 same I=2: balanced / best other textbook-or-FFHT = 0.935 (FFHT 0.3433, plain textbook 0.3387, balanced 0.3167 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^12 same I=2: balanced / best other textbook-or-FFHT = 0.985 (FFHT 0.3589, plain textbook 0.3632, balanced 0.3535 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^13 same I=2: balanced / best other textbook-or-FFHT = 1.039 (FFHT 0.3809, plain textbook 0.4006, balanced 0.3957 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^14 same I=2: balanced / best other textbook-or-FFHT = 1.090 (FFHT 0.4012, plain textbook 0.4424, balanced 0.4373 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^15 same I=2: balanced / best other textbook-or-FFHT = 1.015 (FFHT 0.4341, plain textbook 0.4406, balanced 0.4407 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^16 same I=2: balanced / best other textbook-or-FFHT = 1.010 (FFHT 0.4491, plain textbook 0.4542, balanced 0.4536 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^17 same I=2: balanced / best other textbook-or-FFHT = 1.065 (FFHT 0.4580, plain textbook 0.4931, balanced 0.4879 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^18 same I=2: balanced / best other textbook-or-FFHT = 1.044 (FFHT 0.4810, plain textbook 0.5022, balanced 0.5022 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^19 same I=2: balanced / best other textbook-or-FFHT = 1.050 (FFHT 0.5148, plain textbook 0.5250, balanced 0.5403 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^20 same I=2: balanced / best other textbook-or-FFHT = 1.077 (FFHT 0.5314, plain textbook 0.5791, balanced 0.5721 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^21 same I=2: balanced / best other textbook-or-FFHT = 1.061 (FFHT 0.5442, plain textbook 0.5725, balanced 0.5774 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^22 same I=2: balanced / best other textbook-or-FFHT = 1.036 (FFHT 0.5978, plain textbook 0.5926, balanced 0.6138 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^23 same I=2: balanced / best other textbook-or-FFHT = 1.187 (FFHT 0.6517, plain textbook 0.7718, balanced 0.7733 ns)
- whole_same_I2_gcc_avx512_f32: x86 whole 512bit-f32 2^24 same I=2: balanced / best other textbook-or-FFHT = 1.237 (FFHT 0.7214, plain textbook 0.8938, balanced 0.8921 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^6 same I=2: balanced / best other textbook-or-FFHT = 1.430 (FFHT 0.4992, plain textbook 0.6832, balanced 0.7139 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^7 same I=2: balanced / best other textbook-or-FFHT = 1.221 (FFHT 0.4533, plain textbook 0.5309, balanced 0.5533 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^8 same I=2: balanced / best other textbook-or-FFHT = 1.166 (FFHT 0.4712, plain textbook 0.5743, balanced 0.5493 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^9 same I=2: balanced / best other textbook-or-FFHT = 0.979 (FFHT 0.5320, plain textbook 0.5407, balanced 0.5207 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^10 same I=2: balanced / best other textbook-or-FFHT = 0.956 (FFHT 0.5402, plain textbook 0.5561, balanced 0.5163 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^11 same I=2: balanced / best other textbook-or-FFHT = 1.026 (FFHT 0.5712, plain textbook 0.6117, balanced 0.5862 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^12 same I=2: balanced / best other textbook-or-FFHT = 1.069 (FFHT 0.6472, plain textbook 0.6870, balanced 0.6918 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^13 same I=2: balanced / best other textbook-or-FFHT = 1.182 (FFHT 0.6571, plain textbook 0.7701, balanced 0.7770 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^14 same I=2: balanced / best other textbook-or-FFHT = 1.061 (FFHT 0.7256, plain textbook 0.7658, balanced 0.7702 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^15 same I=2: balanced / best other textbook-or-FFHT = 1.037 (FFHT 0.7538, plain textbook 0.7938, balanced 0.7817 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^16 same I=2: balanced / best other textbook-or-FFHT = 1.120 (FFHT 0.7686, plain textbook 0.8703, balanced 0.8607 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^17 same I=2: balanced / best other textbook-or-FFHT = 1.108 (FFHT 0.8128, plain textbook 0.9022, balanced 0.9007 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^18 same I=2: balanced / best other textbook-or-FFHT = 1.032 (FFHT 0.8999, plain textbook 0.9304, balanced 0.9290 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^19 same I=2: balanced / best other textbook-or-FFHT = 1.107 (FFHT 0.9273, plain textbook 1.0223, balanced 1.0264 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^20 same I=2: balanced / best other textbook-or-FFHT = 1.011 (FFHT 1.0193, plain textbook 1.0303, balanced 1.0304 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^21 same I=2: balanced / best other textbook-or-FFHT = 1.037 (FFHT 1.0453, plain textbook 1.0749, balanced 1.0840 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^22 same I=2: balanced / best other textbook-or-FFHT = 1.247 (FFHT 1.1762, plain textbook 1.4553, balanced 1.4671 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^23 same I=2: balanced / best other textbook-or-FFHT = 1.297 (FFHT 1.3038, plain textbook 1.6849, balanced 1.6907 ns)
- whole_same_I2_gcc_avx512_f64: x86 whole 512bit-f64 2^24 same I=2: balanced / best other textbook-or-FFHT = 1.257 (FFHT 1.4629, plain textbook 1.8478, balanced 1.8388 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^6 same I=1: balanced / best other textbook-or-FFHT = 2.126 (FFHT 0.2930, plain textbook 0.5355, balanced 0.6230 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^7 same I=1: balanced / best other textbook-or-FFHT = 1.307 (FFHT 0.3094, plain textbook 0.3571, balanced 0.4043 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.279 (FFHT 0.2984, plain textbook 0.3637, balanced 0.3816 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^9 same I=1: balanced / best other textbook-or-FFHT = 1.179 (FFHT 0.3076, plain textbook 0.3289, balanced 0.3626 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^10 same I=1: balanced / best other textbook-or-FFHT = 1.080 (FFHT 0.3473, plain textbook 0.3364, balanced 0.3634 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^11 same I=1: balanced / best other textbook-or-FFHT = 1.160 (FFHT 0.3441, plain textbook 0.3525, balanced 0.3992 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^12 same I=1: balanced / best other textbook-or-FFHT = 1.220 (FFHT 0.3599, plain textbook 0.3894, balanced 0.4391 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^13 same I=1: balanced / best other textbook-or-FFHT = 1.150 (FFHT 0.3845, plain textbook 0.3901, balanced 0.4421 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^14 same I=1: balanced / best other textbook-or-FFHT = 1.202 (FFHT 0.4006, plain textbook 0.4315, balanced 0.4814 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^15 same I=1: balanced / best other textbook-or-FFHT = 1.117 (FFHT 0.4342, plain textbook 0.4297, balanced 0.4799 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^16 same I=1: balanced / best other textbook-or-FFHT = 1.110 (FFHT 0.4506, plain textbook 0.4434, balanced 0.4922 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^17 same I=1: balanced / best other textbook-or-FFHT = 1.165 (FFHT 0.4576, plain textbook 0.4839, balanced 0.5330 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^18 same I=1: balanced / best other textbook-or-FFHT = 1.141 (FFHT 0.4756, plain textbook 0.5028, balanced 0.5428 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^19 same I=1: balanced / best other textbook-or-FFHT = 1.101 (FFHT 0.5157, plain textbook 0.5179, balanced 0.5677 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^20 same I=1: balanced / best other textbook-or-FFHT = 1.164 (FFHT 0.5298, plain textbook 0.5875, balanced 0.6167 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^21 same I=1: balanced / best other textbook-or-FFHT = 1.085 (FFHT 0.5815, plain textbook 0.5688, balanced 0.6173 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^22 same I=1: balanced / best other textbook-or-FFHT = 1.126 (FFHT 0.5863, plain textbook 0.5920, balanced 0.6599 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^23 same I=1: balanced / best other textbook-or-FFHT = 1.236 (FFHT 0.6865, plain textbook 0.7951, balanced 0.8483 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^24 same I=1: balanced / best other textbook-or-FFHT = 1.353 (FFHT 0.7271, plain textbook 0.9286, balanced 0.9836 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^6 same I=1: balanced / best other textbook-or-FFHT = 1.519 (FFHT 0.4913, plain textbook 0.6365, balanced 0.7461 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^7 same I=1: balanced / best other textbook-or-FFHT = 1.502 (FFHT 0.4635, plain textbook 0.6143, balanced 0.6960 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.256 (FFHT 0.4719, plain textbook 0.5319, balanced 0.5926 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^9 same I=1: balanced / best other textbook-or-FFHT = 1.088 (FFHT 0.6048, plain textbook 0.5447, balanced 0.5928 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^10 same I=1: balanced / best other textbook-or-FFHT = 1.225 (FFHT 0.5409, plain textbook 0.5783, balanced 0.6626 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^11 same I=1: balanced / best other textbook-or-FFHT = 1.296 (FFHT 0.5731, plain textbook 0.6515, balanced 0.7427 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^12 same I=1: balanced / best other textbook-or-FFHT = 1.151 (FFHT 0.6462, plain textbook 0.6562, balanced 0.7436 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^13 same I=1: balanced / best other textbook-or-FFHT = 1.266 (FFHT 0.6547, plain textbook 0.7395, balanced 0.8288 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^14 same I=1: balanced / best other textbook-or-FFHT = 1.143 (FFHT 0.7230, plain textbook 0.7307, balanced 0.8266 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^15 same I=1: balanced / best other textbook-or-FFHT = 1.135 (FFHT 0.7536, plain textbook 0.7623, balanced 0.8553 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^16 same I=1: balanced / best other textbook-or-FFHT = 1.210 (FFHT 0.7701, plain textbook 0.8465, balanced 0.9318 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^17 same I=1: balanced / best other textbook-or-FFHT = 1.203 (FFHT 0.8056, plain textbook 0.8735, balanced 0.9690 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^18 same I=1: balanced / best other textbook-or-FFHT = 1.141 (FFHT 0.8848, plain textbook 0.9169, balanced 1.0094 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^19 same I=1: balanced / best other textbook-or-FFHT = 1.216 (FFHT 0.9112, plain textbook 1.0160, balanced 1.1080 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^20 same I=1: balanced / best other textbook-or-FFHT = 1.085 (FFHT 1.1397, plain textbook 1.0190, balanced 1.1053 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^21 same I=1: balanced / best other textbook-or-FFHT = 1.086 (FFHT 1.0695, plain textbook 1.0770, balanced 1.1618 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^22 same I=1: balanced / best other textbook-or-FFHT = 1.351 (FFHT 1.1744, plain textbook 1.4911, balanced 1.5867 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^23 same I=1: balanced / best other textbook-or-FFHT = 1.417 (FFHT 1.3137, plain textbook 1.7701, balanced 1.8611 ns)
- whole_same_clang_avx2_f64: x86 whole 256bit-f64 2^24 same I=1: balanced / best other textbook-or-FFHT = 1.388 (FFHT 1.4735, plain textbook 1.9681, balanced 2.0455 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^6 same I=1: balanced / best other textbook-or-FFHT = 2.159 (FFHT 0.2935, plain textbook 0.5234, balanced 0.6336 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^7 same I=1: balanced / best other textbook-or-FFHT = 1.279 (FFHT 0.3101, plain textbook 0.3596, balanced 0.3967 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.251 (FFHT 0.3037, plain textbook 0.3538, balanced 0.3798 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^9 same I=1: balanced / best other textbook-or-FFHT = 1.101 (FFHT 0.3094, plain textbook 0.3302, balanced 0.3407 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^10 same I=1: balanced / best other textbook-or-FFHT = 1.026 (FFHT 0.3471, plain textbook 0.3324, balanced 0.3409 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^11 same I=1: balanced / best other textbook-or-FFHT = 1.005 (FFHT 0.3442, plain textbook 0.3460, balanced 0.3460 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^12 same I=1: balanced / best other textbook-or-FFHT = 1.060 (FFHT 0.3605, plain textbook 0.3818, balanced 0.3820 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^13 same I=1: balanced / best other textbook-or-FFHT = 1.000 (FFHT 0.3858, plain textbook 0.3829, balanced 0.3830 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^14 same I=1: balanced / best other textbook-or-FFHT = 1.060 (FFHT 0.4016, plain textbook 0.4257, balanced 0.4258 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^15 same I=1: balanced / best other textbook-or-FFHT = 0.997 (FFHT 0.4355, plain textbook 0.4260, balanced 0.4249 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^16 same I=1: balanced / best other textbook-or-FFHT = 0.988 (FFHT 0.4518, plain textbook 0.4397, balanced 0.4345 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^17 same I=1: balanced / best other textbook-or-FFHT = 1.041 (FFHT 0.4579, plain textbook 0.4780, balanced 0.4768 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^18 same I=1: balanced / best other textbook-or-FFHT = 1.042 (FFHT 0.4772, plain textbook 0.4873, balanced 0.4971 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^19 same I=1: balanced / best other textbook-or-FFHT = 1.023 (FFHT 0.5157, plain textbook 0.5153, balanced 0.5274 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^20 same I=1: balanced / best other textbook-or-FFHT = 1.054 (FFHT 0.5306, plain textbook 0.5683, balanced 0.5590 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^21 same I=1: balanced / best other textbook-or-FFHT = 0.997 (FFHT 0.5827, plain textbook 0.5634, balanced 0.5619 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^22 same I=1: balanced / best other textbook-or-FFHT = 1.002 (FFHT 0.5879, plain textbook 0.5870, balanced 0.5883 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^23 same I=1: balanced / best other textbook-or-FFHT = 1.118 (FFHT 0.6939, plain textbook 0.7833, balanced 0.7759 ns)
- whole_same_clang_avx2r32_f32: x86 whole 256bit-f32 2^24 same I=1: balanced / best other textbook-or-FFHT = 1.274 (FFHT 0.7211, plain textbook 0.9183, balanced 0.9186 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^6 same I=1: balanced / best other textbook-or-FFHT = 1.984 (FFHT 0.2930, plain textbook 0.4994, balanced 0.5812 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^7 same I=1: balanced / best other textbook-or-FFHT = 1.144 (FFHT 0.3112, plain textbook 0.3321, balanced 0.3561 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.037 (FFHT 0.3112, plain textbook 0.2958, balanced 0.3067 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^9 same I=1: balanced / best other textbook-or-FFHT = 1.041 (FFHT 0.3075, plain textbook 0.3276, balanced 0.3201 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^10 same I=1: balanced / best other textbook-or-FFHT = 0.973 (FFHT 0.3492, plain textbook 0.3146, balanced 0.3062 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^11 same I=1: balanced / best other textbook-or-FFHT = 0.979 (FFHT 0.3439, plain textbook 0.3219, balanced 0.3151 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^12 same I=1: balanced / best other textbook-or-FFHT = 0.955 (FFHT 0.3605, plain textbook 0.3411, balanced 0.3258 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^13 same I=1: balanced / best other textbook-or-FFHT = 0.954 (FFHT 0.3846, plain textbook 0.3819, balanced 0.3645 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^14 same I=1: balanced / best other textbook-or-FFHT = 1.003 (FFHT 0.4008, plain textbook 0.4240, balanced 0.4022 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^15 same I=1: balanced / best other textbook-or-FFHT = 0.951 (FFHT 0.4341, plain textbook 0.4189, balanced 0.3983 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^16 same I=1: balanced / best other textbook-or-FFHT = 0.955 (FFHT 0.4508, plain textbook 0.4346, balanced 0.4151 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^17 same I=1: balanced / best other textbook-or-FFHT = 0.993 (FFHT 0.4574, plain textbook 0.4752, balanced 0.4543 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^18 same I=1: balanced / best other textbook-or-FFHT = 0.976 (FFHT 0.4756, plain textbook 0.4810, balanced 0.4642 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^19 same I=1: balanced / best other textbook-or-FFHT = 0.986 (FFHT 0.5170, plain textbook 0.5008, balanced 0.4940 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^20 same I=1: balanced / best other textbook-or-FFHT = 1.026 (FFHT 0.5293, plain textbook 0.5506, balanced 0.5428 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^21 same I=1: balanced / best other textbook-or-FFHT = 0.971 (FFHT 0.5800, plain textbook 0.5564, balanced 0.5401 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^22 same I=1: balanced / best other textbook-or-FFHT = 0.971 (FFHT 0.5847, plain textbook 0.5782, balanced 0.5612 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^23 same I=1: balanced / best other textbook-or-FFHT = 1.065 (FFHT 0.6867, plain textbook 0.7537, balanced 0.7316 ns)
- whole_same_clang_avx512_f32: x86 whole 512bit-f32 2^24 same I=1: balanced / best other textbook-or-FFHT = 1.197 (FFHT 0.7233, plain textbook 0.8812, balanced 0.8659 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^6 same I=1: balanced / best other textbook-or-FFHT = 1.275 (FFHT 0.4951, plain textbook 0.5395, balanced 0.6315 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^7 same I=1: balanced / best other textbook-or-FFHT = 1.131 (FFHT 0.4537, plain textbook 0.5403, balanced 0.5133 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.157 (FFHT 0.4717, plain textbook 0.5508, balanced 0.5458 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^9 same I=1: balanced / best other textbook-or-FFHT = 0.967 (FFHT 0.5451, plain textbook 0.5307, balanced 0.5132 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^10 same I=1: balanced / best other textbook-or-FFHT = 0.981 (FFHT 0.5399, plain textbook 0.5470, balanced 0.5295 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^11 same I=1: balanced / best other textbook-or-FFHT = 0.953 (FFHT 0.5734, plain textbook 0.5892, balanced 0.5465 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^12 same I=1: balanced / best other textbook-or-FFHT = 0.976 (FFHT 0.6476, plain textbook 0.6670, balanced 0.6318 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^13 same I=1: balanced / best other textbook-or-FFHT = 1.085 (FFHT 0.6550, plain textbook 0.7528, balanced 0.7110 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^14 same I=1: balanced / best other textbook-or-FFHT = 0.970 (FFHT 0.7234, plain textbook 0.7440, balanced 0.7018 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^15 same I=1: balanced / best other textbook-or-FFHT = 0.978 (FFHT 0.7540, plain textbook 0.7749, balanced 0.7372 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^16 same I=1: balanced / best other textbook-or-FFHT = 1.054 (FFHT 0.7718, plain textbook 0.8522, balanced 0.8136 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^17 same I=1: balanced / best other textbook-or-FFHT = 1.038 (FFHT 0.8135, plain textbook 0.8821, balanced 0.8445 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^18 same I=1: balanced / best other textbook-or-FFHT = 0.993 (FFHT 0.8897, plain textbook 0.9178, balanced 0.8832 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^19 same I=1: balanced / best other textbook-or-FFHT = 1.087 (FFHT 0.9119, plain textbook 1.0069, balanced 0.9913 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^20 same I=1: balanced / best other textbook-or-FFHT = 0.970 (FFHT 1.1261, plain textbook 1.0200, balanced 0.9898 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^21 same I=1: balanced / best other textbook-or-FFHT = 0.980 (FFHT 1.0657, plain textbook 1.0567, balanced 1.0353 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^22 same I=1: balanced / best other textbook-or-FFHT = 1.200 (FFHT 1.1608, plain textbook 1.4298, balanced 1.3934 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^23 same I=1: balanced / best other textbook-or-FFHT = 1.265 (FFHT 1.3093, plain textbook 1.6839, balanced 1.6557 ns)
- whole_same_clang_avx512_f64: x86 whole 512bit-f64 2^24 same I=1: balanced / best other textbook-or-FFHT = 1.226 (FFHT 1.4799, plain textbook 1.8570, balanced 1.8144 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^6 same I=1: balanced / best other textbook-or-FFHT = 2.223 (FFHT 0.2975, plain textbook 0.5454, balanced 0.6614 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^7 same I=1: balanced / best other textbook-or-FFHT = 1.348 (FFHT 0.3103, plain textbook 0.3619, balanced 0.4182 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.307 (FFHT 0.2983, plain textbook 0.3417, balanced 0.3899 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^9 same I=1: balanced / best other textbook-or-FFHT = 1.141 (FFHT 0.3077, plain textbook 0.3074, balanced 0.3508 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^10 same I=1: balanced / best other textbook-or-FFHT = 1.066 (FFHT 0.3378, plain textbook 0.3173, balanced 0.3384 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^11 same I=1: balanced / best other textbook-or-FFHT = 1.103 (FFHT 0.3435, plain textbook 0.3256, balanced 0.3591 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^12 same I=1: balanced / best other textbook-or-FFHT = 1.096 (FFHT 0.3590, plain textbook 0.3596, balanced 0.3936 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^13 same I=1: balanced / best other textbook-or-FFHT = 1.103 (FFHT 0.3803, plain textbook 0.3590, balanced 0.3961 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^14 same I=1: balanced / best other textbook-or-FFHT = 1.087 (FFHT 0.4011, plain textbook 0.4018, balanced 0.4360 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^15 same I=1: balanced / best other textbook-or-FFHT = 1.092 (FFHT 0.4344, plain textbook 0.3985, balanced 0.4350 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^16 same I=1: balanced / best other textbook-or-FFHT = 1.159 (FFHT 0.4493, plain textbook 0.4133, balanced 0.4791 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^17 same I=1: balanced / best other textbook-or-FFHT = 1.068 (FFHT 0.4577, plain textbook 0.4545, balanced 0.4853 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^18 same I=1: balanced / best other textbook-or-FFHT = 1.080 (FFHT 0.4764, plain textbook 0.4673, balanced 0.5049 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^19 same I=1: balanced / best other textbook-or-FFHT = 1.085 (FFHT 0.5140, plain textbook 0.4852, balanced 0.5265 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^20 same I=1: balanced / best other textbook-or-FFHT = 1.075 (FFHT 0.5328, plain textbook 0.5325, balanced 0.5722 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^21 same I=1: balanced / best other textbook-or-FFHT = 1.082 (FFHT 0.5497, plain textbook 0.5346, balanced 0.5783 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^22 same I=1: balanced / best other textbook-or-FFHT = 1.074 (FFHT 0.5875, plain textbook 0.5575, balanced 0.5987 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^23 same I=1: balanced / best other textbook-or-FFHT = 1.247 (FFHT 0.6432, plain textbook 0.7679, balanced 0.8018 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^24 same I=1: balanced / best other textbook-or-FFHT = 1.309 (FFHT 0.7307, plain textbook 0.9094, balanced 0.9567 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^6 same I=1: balanced / best other textbook-or-FFHT = 1.486 (FFHT 0.4929, plain textbook 0.6247, balanced 0.7324 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^7 same I=1: balanced / best other textbook-or-FFHT = 1.448 (FFHT 0.4532, plain textbook 0.5607, balanced 0.6563 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.185 (FFHT 0.4731, plain textbook 0.4947, balanced 0.5608 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^9 same I=1: balanced / best other textbook-or-FFHT = 1.105 (FFHT 0.5431, plain textbook 0.4963, balanced 0.5483 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^10 same I=1: balanced / best other textbook-or-FFHT = 1.122 (FFHT 0.5408, plain textbook 0.5291, balanced 0.5935 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^11 same I=1: balanced / best other textbook-or-FFHT = 1.151 (FFHT 0.5728, plain textbook 0.5969, balanced 0.6593 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^12 same I=1: balanced / best other textbook-or-FFHT = 1.127 (FFHT 0.6457, plain textbook 0.5947, balanced 0.6700 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^13 same I=1: balanced / best other textbook-or-FFHT = 1.152 (FFHT 0.6565, plain textbook 0.6821, balanced 0.7562 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^14 same I=1: balanced / best other textbook-or-FFHT = 1.113 (FFHT 0.7236, plain textbook 0.6744, balanced 0.7506 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^15 same I=1: balanced / best other textbook-or-FFHT = 1.025 (FFHT 0.7539, plain textbook 0.7444, balanced 0.7633 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^16 same I=1: balanced / best other textbook-or-FFHT = 1.099 (FFHT 0.7686, plain textbook 0.8053, balanced 0.8444 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^17 same I=1: balanced / best other textbook-or-FFHT = 1.067 (FFHT 0.8906, plain textbook 0.8192, balanced 0.8737 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^18 same I=1: balanced / best other textbook-or-FFHT = 1.091 (FFHT 0.8802, plain textbook 0.8501, balanced 0.9277 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^19 same I=1: balanced / best other textbook-or-FFHT = 1.107 (FFHT 0.9151, plain textbook 0.9659, balanced 1.0132 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^20 same I=1: balanced / best other textbook-or-FFHT = 1.081 (FFHT 0.9940, plain textbook 0.9453, balanced 1.0218 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^21 same I=1: balanced / best other textbook-or-FFHT = 1.133 (FFHT 1.0468, plain textbook 0.9884, balanced 1.1194 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^22 same I=1: balanced / best other textbook-or-FFHT = 1.335 (FFHT 1.1461, plain textbook 1.4542, balanced 1.5299 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^23 same I=1: balanced / best other textbook-or-FFHT = 1.361 (FFHT 1.3278, plain textbook 1.7145, balanced 1.8074 ns)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^24 same I=1: balanced / best other textbook-or-FFHT = 1.361 (FFHT 1.4826, plain textbook 1.9147, balanced 2.0173 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^6 same I=1: balanced / best other textbook-or-FFHT = 2.015 (FFHT 0.2930, plain textbook 0.5022, balanced 0.5903 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^7 same I=1: balanced / best other textbook-or-FFHT = 1.213 (FFHT 0.3118, plain textbook 0.3476, balanced 0.3781 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.169 (FFHT 0.3012, plain textbook 0.3317, balanced 0.3521 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^9 same I=1: balanced / best other textbook-or-FFHT = 1.051 (FFHT 0.3075, plain textbook 0.3021, balanced 0.3174 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^10 same I=1: balanced / best other textbook-or-FFHT = 1.010 (FFHT 0.3375, plain textbook 0.3074, balanced 0.3106 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^11 same I=1: balanced / best other textbook-or-FFHT = 0.968 (FFHT 0.3437, plain textbook 0.3201, balanced 0.3100 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^12 same I=1: balanced / best other textbook-or-FFHT = 0.958 (FFHT 0.3589, plain textbook 0.3556, balanced 0.3405 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^13 same I=1: balanced / best other textbook-or-FFHT = 0.968 (FFHT 0.3803, plain textbook 0.3570, balanced 0.3457 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^14 same I=1: balanced / best other textbook-or-FFHT = 0.973 (FFHT 0.4011, plain textbook 0.4005, balanced 0.3896 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^15 same I=1: balanced / best other textbook-or-FFHT = 0.975 (FFHT 0.4341, plain textbook 0.3979, balanced 0.3880 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^16 same I=1: balanced / best other textbook-or-FFHT = 0.971 (FFHT 0.4490, plain textbook 0.4123, balanced 0.4002 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^17 same I=1: balanced / best other textbook-or-FFHT = 0.975 (FFHT 0.4591, plain textbook 0.4505, balanced 0.4394 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^18 same I=1: balanced / best other textbook-or-FFHT = 0.981 (FFHT 0.4816, plain textbook 0.4593, balanced 0.4507 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^19 same I=1: balanced / best other textbook-or-FFHT = 0.989 (FFHT 0.5142, plain textbook 0.4808, balanced 0.4754 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^20 same I=1: balanced / best other textbook-or-FFHT = 1.002 (FFHT 0.5304, plain textbook 0.5297, balanced 0.5305 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^21 same I=1: balanced / best other textbook-or-FFHT = 0.988 (FFHT 0.5487, plain textbook 0.5342, balanced 0.5276 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^22 same I=1: balanced / best other textbook-or-FFHT = 1.030 (FFHT 0.5936, plain textbook 0.5564, balanced 0.5731 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^23 same I=1: balanced / best other textbook-or-FFHT = 1.177 (FFHT 0.6505, plain textbook 0.7616, balanced 0.7655 ns)
- whole_same_gcc_avx2r32_f32: x86 whole 256bit-f32 2^24 same I=1: balanced / best other textbook-or-FFHT = 1.219 (FFHT 0.7214, plain textbook 0.8880, balanced 0.8793 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^6 same I=1: balanced / best other textbook-or-FFHT = 1.997 (FFHT 0.2924, plain textbook 0.5098, balanced 0.5840 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^7 same I=1: balanced / best other textbook-or-FFHT = 1.352 (FFHT 0.3101, plain textbook 0.3924, balanced 0.4192 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.131 (FFHT 0.2980, plain textbook 0.3287, balanced 0.3370 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^9 same I=1: balanced / best other textbook-or-FFHT = 1.091 (FFHT 0.3070, plain textbook 0.3456, balanced 0.3350 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^10 same I=1: balanced / best other textbook-or-FFHT = 0.975 (FFHT 0.3375, plain textbook 0.3279, balanced 0.3197 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^11 same I=1: balanced / best other textbook-or-FFHT = 0.991 (FFHT 0.3439, plain textbook 0.3346, balanced 0.3316 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^12 same I=1: balanced / best other textbook-or-FFHT = 0.906 (FFHT 0.3589, plain textbook 0.3495, balanced 0.3167 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^13 same I=1: balanced / best other textbook-or-FFHT = 0.936 (FFHT 0.3815, plain textbook 0.3877, balanced 0.3569 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^14 same I=1: balanced / best other textbook-or-FFHT = 1.003 (FFHT 0.4012, plain textbook 0.4289, balanced 0.4026 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^15 same I=1: balanced / best other textbook-or-FFHT = 0.944 (FFHT 0.4339, plain textbook 0.4267, balanced 0.4028 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^16 same I=1: balanced / best other textbook-or-FFHT = 0.937 (FFHT 0.4495, plain textbook 0.4414, balanced 0.4134 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^17 same I=1: balanced / best other textbook-or-FFHT = 0.988 (FFHT 0.4576, plain textbook 0.4792, balanced 0.4522 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^18 same I=1: balanced / best other textbook-or-FFHT = 1.055 (FFHT 0.4766, plain textbook 0.4865, balanced 0.5029 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^19 same I=1: balanced / best other textbook-or-FFHT = 0.935 (FFHT 0.5122, plain textbook 0.5225, balanced 0.4790 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^20 same I=1: balanced / best other textbook-or-FFHT = 0.990 (FFHT 0.5302, plain textbook 0.5550, balanced 0.5247 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^21 same I=1: balanced / best other textbook-or-FFHT = 0.983 (FFHT 0.5427, plain textbook 0.5575, balanced 0.5333 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^22 same I=1: balanced / best other textbook-or-FFHT = 0.965 (FFHT 0.6001, plain textbook 0.5808, balanced 0.5606 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^23 same I=1: balanced / best other textbook-or-FFHT = 1.129 (FFHT 0.6562, plain textbook 0.7606, balanced 0.7410 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^24 same I=1: balanced / best other textbook-or-FFHT = 1.175 (FFHT 0.7276, plain textbook 0.8853, balanced 0.8548 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^6 same I=1: balanced / best other textbook-or-FFHT = 1.938 (FFHT 0.4934, plain textbook 0.6580, balanced 0.9563 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^7 same I=1: balanced / best other textbook-or-FFHT = 1.182 (FFHT 0.4685, plain textbook 0.5302, balanced 0.5540 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.179 (FFHT 0.4767, plain textbook 0.5733, balanced 0.5618 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^9 same I=1: balanced / best other textbook-or-FFHT = 0.971 (FFHT 0.5330, plain textbook 0.5421, balanced 0.5174 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^10 same I=1: balanced / best other textbook-or-FFHT = 0.965 (FFHT 0.5404, plain textbook 0.5507, balanced 0.5213 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^11 same I=1: balanced / best other textbook-or-FFHT = 0.910 (FFHT 0.5721, plain textbook 0.5844, balanced 0.5204 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^12 same I=1: balanced / best other textbook-or-FFHT = 0.923 (FFHT 0.6469, plain textbook 0.6615, balanced 0.5972 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^13 same I=1: balanced / best other textbook-or-FFHT = 1.039 (FFHT 0.6566, plain textbook 0.7430, balanced 0.6819 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^14 same I=1: balanced / best other textbook-or-FFHT = 0.940 (FFHT 0.7245, plain textbook 0.7386, balanced 0.6808 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^15 same I=1: balanced / best other textbook-or-FFHT = 0.930 (FFHT 0.7552, plain textbook 0.7683, balanced 0.7025 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^16 same I=1: balanced / best other textbook-or-FFHT = 1.014 (FFHT 0.7694, plain textbook 0.8476, balanced 0.7803 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^17 same I=1: balanced / best other textbook-or-FFHT = 0.951 (FFHT 0.8455, plain textbook 0.8730, balanced 0.8044 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^18 same I=1: balanced / best other textbook-or-FFHT = 0.956 (FFHT 0.8837, plain textbook 0.9017, balanced 0.8445 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^19 same I=1: balanced / best other textbook-or-FFHT = 1.041 (FFHT 0.9116, plain textbook 0.9990, balanced 0.9491 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^20 same I=1: balanced / best other textbook-or-FFHT = 0.948 (FFHT 0.9981, plain textbook 1.0039, balanced 0.9460 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^21 same I=1: balanced / best other textbook-or-FFHT = 0.938 (FFHT 1.0536, plain textbook 1.0546, balanced 0.9878 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^22 same I=1: balanced / best other textbook-or-FFHT = 1.161 (FFHT 1.1765, plain textbook 1.4060, balanced 1.3658 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^23 same I=1: balanced / best other textbook-or-FFHT = 1.236 (FFHT 1.3022, plain textbook 1.6696, balanced 1.6094 ns)
- whole_same_gcc_avx512_f64: x86 whole 512bit-f64 2^24 same I=1: balanced / best other textbook-or-FFHT = 1.212 (FFHT 1.4617, plain textbook 1.8285, balanced 1.7722 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^10 separate I=1: balanced / best other textbook-or-FFHT = 1.078 (FFHT 0.3736, plain textbook 0.3481, balanced 0.3754 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1: balanced / best other textbook-or-FFHT = 1.237 (FFHT 0.3689, plain textbook 0.4079, balanced 0.4565 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^14 separate I=1: balanced / best other textbook-or-FFHT = 1.257 (FFHT 0.4280, plain textbook 0.4876, balanced 0.5380 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1: balanced / best other textbook-or-FFHT = 1.108 (FFHT 0.4971, plain textbook 0.5002, balanced 0.5507 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^18 separate I=1: balanced / best other textbook-or-FFHT = 1.232 (FFHT 0.5037, plain textbook 0.5650, balanced 0.6205 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.221 (FFHT 0.5617, plain textbook 0.6333, balanced 0.6859 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^22 separate I=1: balanced / best other textbook-or-FFHT = 1.212 (FFHT 0.6289, plain textbook 0.7071, balanced 0.7623 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.433 (FFHT 0.7267, plain textbook 0.9904, balanced 1.0413 ns)
- whole_sep_clang_avx2_f64: x86 whole 256bit-f64 2^10 separate I=1: balanced / best other textbook-or-FFHT = 1.158 (FFHT 0.5866, plain textbook 0.6117, balanced 0.6795 ns)
- whole_sep_clang_avx2_f64: x86 whole 256bit-f64 2^12 separate I=1: balanced / best other textbook-or-FFHT = 1.136 (FFHT 0.7509, plain textbook 0.7844, balanced 0.8528 ns)
- whole_sep_clang_avx2_f64: x86 whole 256bit-f64 2^14 separate I=1: balanced / best other textbook-or-FFHT = 1.133 (FFHT 0.8473, plain textbook 0.8890, balanced 0.9599 ns)
- whole_sep_clang_avx2_f64: x86 whole 256bit-f64 2^16 separate I=1: balanced / best other textbook-or-FFHT = 1.259 (FFHT 0.8243, plain textbook 0.9714, balanced 1.0381 ns)
- whole_sep_clang_avx2_f64: x86 whole 256bit-f64 2^18 separate I=1: balanced / best other textbook-or-FFHT = 1.140 (FFHT 1.0005, plain textbook 1.0730, balanced 1.1407 ns)
- whole_sep_clang_avx2_f64: x86 whole 256bit-f64 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.059 (FFHT 1.2149, plain textbook 1.2158, balanced 1.2861 ns)
- whole_sep_clang_avx2_f64: x86 whole 256bit-f64 2^22 separate I=1: balanced / best other textbook-or-FFHT = 1.492 (FFHT 1.1679, plain textbook 1.6498, balanced 1.7427 ns)
- whole_sep_clang_avx2_f64: x86 whole 256bit-f64 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.412 (FFHT 1.4700, plain textbook 1.9998, balanced 2.0752 ns)
- whole_sep_clang_avx2r32_f32: x86 whole 256bit-f32 2^10 separate I=1: balanced / best other textbook-or-FFHT = 1.028 (FFHT 0.3747, plain textbook 0.3425, balanced 0.3522 ns)
- whole_sep_clang_avx2r32_f32: x86 whole 256bit-f32 2^12 separate I=1: balanced / best other textbook-or-FFHT = 1.085 (FFHT 0.3686, plain textbook 0.4005, balanced 0.4001 ns)
- whole_sep_clang_avx2r32_f32: x86 whole 256bit-f32 2^14 separate I=1: balanced / best other textbook-or-FFHT = 1.117 (FFHT 0.4282, plain textbook 0.4791, balanced 0.4782 ns)
- whole_sep_clang_avx2r32_f32: x86 whole 256bit-f32 2^16 separate I=1: balanced / best other textbook-or-FFHT = 0.996 (FFHT 0.4918, plain textbook 0.4938, balanced 0.4897 ns)
- whole_sep_clang_avx2r32_f32: x86 whole 256bit-f32 2^18 separate I=1: balanced / best other textbook-or-FFHT = 1.094 (FFHT 0.5001, plain textbook 0.5566, balanced 0.5472 ns)
- whole_sep_clang_avx2r32_f32: x86 whole 256bit-f32 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.113 (FFHT 0.5585, plain textbook 0.6239, balanced 0.6217 ns)
- whole_sep_clang_avx2r32_f32: x86 whole 256bit-f32 2^22 separate I=1: balanced / best other textbook-or-FFHT = 1.106 (FFHT 0.6281, plain textbook 0.6959, balanced 0.6944 ns)
- whole_sep_clang_avx2r32_f32: x86 whole 256bit-f32 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.357 (FFHT 0.7208, plain textbook 0.9781, balanced 0.9782 ns)
- whole_sep_clang_avx512_f32: x86 whole 512bit-f32 2^10 separate I=1: balanced / best other textbook-or-FFHT = 0.975 (FFHT 0.3778, plain textbook 0.3250, balanced 0.3170 ns)
- whole_sep_clang_avx512_f32: x86 whole 512bit-f32 2^12 separate I=1: balanced / best other textbook-or-FFHT = 0.949 (FFHT 0.3690, plain textbook 0.3563, balanced 0.3380 ns)
- whole_sep_clang_avx512_f32: x86 whole 512bit-f32 2^14 separate I=1: balanced / best other textbook-or-FFHT = 1.035 (FFHT 0.4294, plain textbook 0.4644, balanced 0.4443 ns)
- whole_sep_clang_avx512_f32: x86 whole 512bit-f32 2^16 separate I=1: balanced / best other textbook-or-FFHT = 0.958 (FFHT 0.4951, plain textbook 0.4794, balanced 0.4594 ns)
- whole_sep_clang_avx512_f32: x86 whole 512bit-f32 2^18 separate I=1: balanced / best other textbook-or-FFHT = 1.036 (FFHT 0.5012, plain textbook 0.5436, balanced 0.5190 ns)
- whole_sep_clang_avx512_f32: x86 whole 512bit-f32 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.060 (FFHT 0.5589, plain textbook 0.6070, balanced 0.5925 ns)
- whole_sep_clang_avx512_f32: x86 whole 512bit-f32 2^22 separate I=1: balanced / best other textbook-or-FFHT = 1.045 (FFHT 0.6302, plain textbook 0.6722, balanced 0.6588 ns)
- whole_sep_clang_avx512_f32: x86 whole 512bit-f32 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.273 (FFHT 0.7295, plain textbook 0.9488, balanced 0.9290 ns)
- whole_sep_clang_avx512_f64: x86 whole 512bit-f64 2^10 separate I=1: balanced / best other textbook-or-FFHT = 0.976 (FFHT 0.5697, plain textbook 0.5717, balanced 0.5562 ns)
- whole_sep_clang_avx512_f64: x86 whole 512bit-f64 2^12 separate I=1: balanced / best other textbook-or-FFHT = 0.968 (FFHT 0.7509, plain textbook 0.7607, balanced 0.7267 ns)
- whole_sep_clang_avx512_f64: x86 whole 512bit-f64 2^14 separate I=1: balanced / best other textbook-or-FFHT = 0.966 (FFHT 0.8555, plain textbook 0.8646, balanced 0.8268 ns)
- whole_sep_clang_avx512_f64: x86 whole 512bit-f64 2^16 separate I=1: balanced / best other textbook-or-FFHT = 1.105 (FFHT 0.8250, plain textbook 0.9463, balanced 0.9118 ns)
- whole_sep_clang_avx512_f64: x86 whole 512bit-f64 2^18 separate I=1: balanced / best other textbook-or-FFHT = 1.018 (FFHT 0.9953, plain textbook 1.0379, balanced 1.0131 ns)
- whole_sep_clang_avx512_f64: x86 whole 512bit-f64 2^20 separate I=1: balanced / best other textbook-or-FFHT = 0.979 (FFHT 1.2059, plain textbook 1.1701, balanced 1.1451 ns)
- whole_sep_clang_avx512_f64: x86 whole 512bit-f64 2^22 separate I=1: balanced / best other textbook-or-FFHT = 1.322 (FFHT 1.1859, plain textbook 1.6132, balanced 1.5681 ns)
- whole_sep_clang_avx512_f64: x86 whole 512bit-f64 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.260 (FFHT 1.4787, plain textbook 1.9138, balanced 1.8632 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^10 separate I=1: balanced / best other textbook-or-FFHT = 1.067 (FFHT 0.3487, plain textbook 0.3226, balanced 0.3442 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1: balanced / best other textbook-or-FFHT = 1.118 (FFHT 0.3691, plain textbook 0.3783, balanced 0.4126 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^14 separate I=1: balanced / best other textbook-or-FFHT = 1.158 (FFHT 0.4302, plain textbook 0.4612, balanced 0.4983 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1: balanced / best other textbook-or-FFHT = 1.066 (FFHT 0.4989, plain textbook 0.4754, balanced 0.5070 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^18 separate I=1: balanced / best other textbook-or-FFHT = 1.106 (FFHT 0.5060, plain textbook 0.5406, balanced 0.5596 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.140 (FFHT 0.5655, plain textbook 0.6044, balanced 0.6445 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^22 separate I=1: balanced / best other textbook-or-FFHT = 1.167 (FFHT 0.6263, plain textbook 0.6833, balanced 0.7307 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.394 (FFHT 0.7328, plain textbook 0.9660, balanced 1.0215 ns)
- whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^10 separate I=1: balanced / best other textbook-or-FFHT = 1.130 (FFHT 0.5613, plain textbook 0.5586, balanced 0.6310 ns)
- whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^12 separate I=1: balanced / best other textbook-or-FFHT = 1.107 (FFHT 0.7586, plain textbook 0.7391, balanced 0.8183 ns)
- whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^14 separate I=1: balanced / best other textbook-or-FFHT = 1.092 (FFHT 0.8619, plain textbook 0.8511, balanced 0.9294 ns)
- whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^16 separate I=1: balanced / best other textbook-or-FFHT = 1.197 (FFHT 0.8279, plain textbook 0.9270, balanced 0.9911 ns)
- whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^18 separate I=1: balanced / best other textbook-or-FFHT = 1.075 (FFHT 1.0351, plain textbook 1.0214, balanced 1.0980 ns)
- whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.119 (FFHT 1.1231, plain textbook 1.1735, balanced 1.2562 ns)
- whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^22 separate I=1: balanced / best other textbook-or-FFHT = 1.459 (FFHT 1.1866, plain textbook 1.6536, balanced 1.7316 ns)
- whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.394 (FFHT 1.4857, plain textbook 1.9682, balanced 2.0712 ns)
- whole_sep_gcc_avx2r32_f32: x86 whole 256bit-f32 2^10 separate I=1: balanced / best other textbook-or-FFHT = 1.017 (FFHT 0.3482, plain textbook 0.3181, balanced 0.3235 ns)
- whole_sep_gcc_avx2r32_f32: x86 whole 256bit-f32 2^12 separate I=1: balanced / best other textbook-or-FFHT = 0.967 (FFHT 0.3691, plain textbook 0.3732, balanced 0.3570 ns)
- whole_sep_gcc_avx2r32_f32: x86 whole 256bit-f32 2^14 separate I=1: balanced / best other textbook-or-FFHT = 1.034 (FFHT 0.4282, plain textbook 0.4545, balanced 0.4426 ns)
- whole_sep_gcc_avx2r32_f32: x86 whole 256bit-f32 2^16 separate I=1: balanced / best other textbook-or-FFHT = 0.975 (FFHT 0.4950, plain textbook 0.4654, balanced 0.4538 ns)
- whole_sep_gcc_avx2r32_f32: x86 whole 256bit-f32 2^18 separate I=1: balanced / best other textbook-or-FFHT = 1.021 (FFHT 0.5043, plain textbook 0.5302, balanced 0.5151 ns)
- whole_sep_gcc_avx2r32_f32: x86 whole 256bit-f32 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.042 (FFHT 0.5671, plain textbook 0.5953, balanced 0.5909 ns)
- whole_sep_gcc_avx2r32_f32: x86 whole 256bit-f32 2^22 separate I=1: balanced / best other textbook-or-FFHT = 1.069 (FFHT 0.6209, plain textbook 0.6682, balanced 0.6640 ns)
- whole_sep_gcc_avx2r32_f32: x86 whole 256bit-f32 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.298 (FFHT 0.7223, plain textbook 0.9500, balanced 0.9375 ns)
- whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^10 separate I=1: balanced / best other textbook-or-FFHT = 0.981 (FFHT 0.3483, plain textbook 0.3372, balanced 0.3307 ns)
- whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^12 separate I=1: balanced / best other textbook-or-FFHT = 0.918 (FFHT 0.3690, plain textbook 0.3612, balanced 0.3316 ns)
- whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^14 separate I=1: balanced / best other textbook-or-FFHT = 1.010 (FFHT 0.4282, plain textbook 0.4614, balanced 0.4324 ns)
- whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^16 separate I=1: balanced / best other textbook-or-FFHT = 0.935 (FFHT 0.4938, plain textbook 0.4758, balanced 0.4449 ns)
- whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^18 separate I=1: balanced / best other textbook-or-FFHT = 1.009 (FFHT 0.5056, plain textbook 0.5406, balanced 0.5099 ns)
- whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.025 (FFHT 0.5635, plain textbook 0.6055, balanced 0.5774 ns)
- whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^22 separate I=1: balanced / best other textbook-or-FFHT = 1.031 (FFHT 0.6239, plain textbook 0.6684, balanced 0.6435 ns)
- whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.246 (FFHT 0.7288, plain textbook 0.9446, balanced 0.9083 ns)
- whole_sep_gcc_avx512_f64: x86 whole 512bit-f64 2^10 separate I=1: balanced / best other textbook-or-FFHT = 0.978 (FFHT 0.5585, plain textbook 0.5695, balanced 0.5462 ns)
- whole_sep_gcc_avx512_f64: x86 whole 512bit-f64 2^12 separate I=1: balanced / best other textbook-or-FFHT = 0.927 (FFHT 0.7502, plain textbook 0.7381, balanced 0.6843 ns)
- whole_sep_gcc_avx512_f64: x86 whole 512bit-f64 2^14 separate I=1: balanced / best other textbook-or-FFHT = 0.927 (FFHT 0.8488, plain textbook 0.8423, balanced 0.7808 ns)
- whole_sep_gcc_avx512_f64: x86 whole 512bit-f64 2^16 separate I=1: balanced / best other textbook-or-FFHT = 1.038 (FFHT 0.8238, plain textbook 0.9227, balanced 0.8555 ns)
- whole_sep_gcc_avx512_f64: x86 whole 512bit-f64 2^18 separate I=1: balanced / best other textbook-or-FFHT = 0.954 (FFHT 1.0031, plain textbook 1.0127, balanced 0.9573 ns)
- whole_sep_gcc_avx512_f64: x86 whole 512bit-f64 2^20 separate I=1: balanced / best other textbook-or-FFHT = 0.986 (FFHT 1.1087, plain textbook 1.1442, balanced 1.0930 ns)
- whole_sep_gcc_avx512_f64: x86 whole 512bit-f64 2^22 separate I=1: balanced / best other textbook-or-FFHT = 1.281 (FFHT 1.1852, plain textbook 1.5750, balanced 1.5187 ns)
- whole_sep_gcc_avx512_f64: x86 whole 512bit-f64 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.244 (FFHT 1.4646, plain textbook 1.8702, balanced 1.8214 ns)

## Cases at or below 0.90 of the fastest baseline (CHECK the whole-transform rows before believing a pass row)

- pass16_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g52 0.776 (baseline tb16)
- pass16_I1_clang_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): g52 0.778 (baseline tb16)
- pass16_I1_clang_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g52 0.892 (baseline tb16bal)
- pass16_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB): g52 0.773 (baseline tb16bal)
- pass16_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB): g54d7 0.841 (baseline tb16bal)
- pass16_I1_clang_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 1 S=96 (12 KB): g52 0.789 (baseline tb16bal)
- pass16_I1_clang_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 1 S=96 (12 KB): g54d7 0.846 (baseline tb16bal)
- pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g52 0.718 (baseline tb16)
- pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g54d7 0.751 (baseline tb16)
- pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g56d6 0.827 (baseline tb16)
- pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): g52 0.714 (baseline tb16)
- pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): g54d7 0.754 (baseline tb16)
- pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): g56d6 0.823 (baseline tb16)
- pass16_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB): g52 0.876 (baseline tb16bal)
- pass16_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 1 S=96 (12 KB): g52 0.846 (baseline tb16bal)
- pass16_I2_clang_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 2 S=96 (12 KB): g52 0.862 (baseline tb16)
- pass16_I2_clang_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): g52 0.788 (baseline tb16bal)
- pass16_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB): g52 0.771 (baseline tb16bal)
- pass16_I2_clang_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB): g52 0.839 (baseline tb16bal)
- pass16_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): g52 0.681 (baseline tb16)
- pass16_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): g54d7 0.754 (baseline tb16)
- pass16_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB): g52 0.710 (baseline tb16)
- pass16_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB): g54d7 0.804 (baseline tb16)
- pass16_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB): g56d6 0.855 (baseline tb16)
- pass16_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB): g52 0.722 (baseline tb16)
- pass16_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB): g54d7 0.808 (baseline tb16)
- pass16_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB): g56d6 0.857 (baseline tb16)
- pass16_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB): g52 0.885 (baseline tb16bal)
- pass16_I3_clang_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 3 S=96 (12 KB): g52 0.878 (baseline tb16bal)
- pass16_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): g54d7 0.871 (baseline tb16)
- pass16_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 3 S=96 (12 KB): g54d7 0.868 (baseline tb16)
- pass16_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): g52 0.842 (baseline tb16)
- pass16_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): g54d7 0.784 (baseline tb16)
- pass16_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): g56d6 0.880 (baseline tb16)
- pass16_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB): g52 0.886 (baseline tb16)
- pass16_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB): g54d7 0.834 (baseline tb16)
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g19 0.824 (baseline tb8bal)
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g20 0.811 (baseline tb8bal)
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g22d4 0.830 (baseline tb8bal)
- pass8_I1_clang_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): g19 0.833 (baseline tb8bal)
- pass8_I1_clang_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): g20 0.812 (baseline tb8bal)
- pass8_I1_clang_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): g22d4 0.830 (baseline tb8bal)
- pass8_I1_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g19 0.825 (baseline tb8bal)
- pass8_I1_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g20 0.812 (baseline tb8bal)
- pass8_I1_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g22d4 0.828 (baseline tb8bal)
- pass8_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): g19 0.756 (baseline tb8bal)
- pass8_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): g20 0.856 (baseline tb8bal)
- pass8_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): h20half 0.894 (baseline tb8bal)
- pass8_I1_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): g19 0.763 (baseline tb8bal)
- pass8_I1_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): g20 0.857 (baseline tb8bal)
- pass8_I1_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): h20half 0.895 (baseline tb8bal)
- pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g20 0.816 (baseline tb8bal)
- pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g22d4 0.820 (baseline tb8bal)
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): g19 0.855 (baseline tb8bal)
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): g20 0.770 (baseline tb8bal)
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): g22d4 0.770 (baseline tb8bal)
- pass8_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g19 0.877 (baseline tb8bal)
- pass8_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g20 0.793 (baseline tb8bal)
- pass8_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g22d4 0.800 (baseline tb8bal)
- pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): g19 0.852 (baseline tb8bal)
- pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): g20 0.866 (baseline tb8bal)
- pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): g22d4 0.885 (baseline tb8bal)
- pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): h20half 0.850 (baseline tb8bal)
- pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): g19 0.850 (baseline tb8bal)
- pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): g20 0.859 (baseline tb8bal)
- pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): g22d4 0.865 (baseline tb8bal)
- pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): h20half 0.846 (baseline tb8bal)
- pass8_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g20 0.860 (baseline tb8)
- pass8_I2_clang_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): g20 0.828 (baseline tb8)
- pass8_I2_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g19 0.814 (baseline tb8bal)
- pass8_I2_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g20 0.768 (baseline tb8bal)
- pass8_I2_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g22d4 0.808 (baseline tb8bal)
- pass8_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): g19 0.821 (baseline tb8bal)
- pass8_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): g20 0.816 (baseline tb8bal)
- pass8_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): g22d4 0.899 (baseline tb8bal)
- pass8_I2_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB): g19 0.817 (baseline tb8bal)
- pass8_I2_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB): g20 0.806 (baseline tb8bal)
- pass8_I2_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB): g22d4 0.890 (baseline tb8bal)
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g19 0.834 (baseline tb8)
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g20 0.772 (baseline tb8)
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g22d4 0.825 (baseline tb8)
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): h20half 0.871 (baseline tb8)
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): g19 0.829 (baseline tb8)
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): g20 0.773 (baseline tb8)
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): g22d4 0.820 (baseline tb8)
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): h20half 0.863 (baseline tb8)
- pass8_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g20 0.808 (baseline tb8bal)
- pass8_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g22d4 0.821 (baseline tb8bal)
- pass8_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB): g20 0.850 (baseline tb8bal)
- pass8_I3_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g19 0.847 (baseline tb8bal)
- pass8_I3_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g20 0.786 (baseline tb8bal)
- pass8_I3_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g22d4 0.831 (baseline tb8bal)
- pass8_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): g20 0.900 (baseline tb8bal)
- pass8_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): g22d4 0.871 (baseline tb8bal)
- pass8_I3_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB): g20 0.889 (baseline tb8bal)
- pass8_I3_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB): g22d4 0.879 (baseline tb8bal)
- pass8_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g19 0.817 (baseline tb8bal)
- pass8_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g20 0.775 (baseline tb8bal)
- pass8_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g22d4 0.785 (baseline tb8bal)
- pass8_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): g19 0.888 (baseline tb8bal)
- pass8_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): g20 0.812 (baseline tb8bal)
- pass8_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): g22d4 0.842 (baseline tb8bal)
- pass8_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB): g19 0.887 (baseline tb8bal)
- pass8_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB): g20 0.811 (baseline tb8bal)
- pass8_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB): g22d4 0.841 (baseline tb8bal)
- pass8_I4_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): g20 0.759 (baseline tb8)
- pass8_I4_clang_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): g22d4 0.897 (baseline tb8)
- pass8_I4_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 4 S=384 (12 KB): g20 0.807 (baseline tb8bal)
- pass8_I4_clang_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 4 S=192 (12 KB): g20 0.806 (baseline tb8bal)
- pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): g19 0.818 (baseline tb8)
- pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): g20 0.775 (baseline tb8)
- pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): g22d4 0.756 (baseline tb8)
- pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): h20half 0.873 (baseline tb8)
- regs16_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2: g52 0.887 (baseline tb16bal)
- regs16_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2: g56d6 0.890 (baseline tb16bal)
- regs16_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 2: g52 0.886 (baseline tb16bal)
- regs16_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 2: g56d6 0.890 (baseline tb16bal)
- regs8_I4_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 4: g22d4 0.866 (baseline tb8bal)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^11 same I=1: g52+tb8 0.899 (baseline textbook)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^10 same I=1: g52+tb8 0.896 (baseline textbook)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^10 same I=1: g52+g19 0.887 (baseline textbook)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^15 same I=1: g52+tb8 0.868 (baseline textbook)
- whole_same_gcc_avx2_f64: x86 whole 256bit-f64 2^15 same I=1: g52+g19 0.849 (baseline textbook)
- whole_sep_gcc_avx2_f64: x86 whole 256bit-f64 2^10 separate I=1: g52+tb8 0.897 (baseline textbook)
