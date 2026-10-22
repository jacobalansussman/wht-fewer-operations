# x86-wht summary 

Figure = circuit median / fastest baseline median (textbook, pipe-balanced textbook, FFHT); < 1 is faster.

| test | baseline (ns/unit) | circuit: ratio ... |
|---|---|---|
| pass16_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16bal 0.0566 (tb16 1.069) | g52 0.749; g54d7 0.864; g56d6 0.993 |
| pass16_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16bal 0.0285 (tb16 1.070) | g52 0.916; g54d7 0.912; g56d6 0.944 |
| pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16 0.0605 (tb16bal 1.028) | g52 0.669; g54d7 0.737; g56d6 0.788 |
| pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB) | tb16 0.1210 (tb16bal 1.029) | g52 0.662; g54d7 0.743; g56d6 0.788 |
| pass16_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16bal 0.0489 (tb16 1.237) | g52 0.791; g54d7 0.924; g56d6 0.935 |
| pass16_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB) | tb16bal 0.0270 (tb16 1.122) | g52 0.815; g54d7 0.874; g56d6 0.889 |
| pass16_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 1 S=96 (12 KB) | tb16bal 0.0547 (tb16 1.106) | g52 0.834; g54d7 0.846; g56d6 0.876 |
| pass16_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.0622 (tb16bal 1.042) | g52 0.944; g54d7 0.955; g56d6 0.949 |
| pass16_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.0325 (tb16bal 1.006) | g52 0.942; g54d7 1.071; g56d6 1.385 |
| pass16_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.0607 (tb16bal 1.329) | g52 0.893; g54d7 0.946; g56d6 0.995 |
| pass16_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 2 S=96 (12 KB) | tb16 0.1213 (tb16bal 1.333) | g52 0.908; g54d7 0.958; g56d6 1.000 |
| pass16_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.0607 (tb16bal 1.069) | g52 0.697; g54d7 0.758; g56d6 0.761 |
| pass16_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB) | tb16 0.0304 (tb16bal 1.487) | g52 0.839; g54d7 0.941; g56d6 1.234 |
| pass16_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB) | tb16 0.0613 (tb16bal 1.445) | g52 0.845; g54d7 0.866; g56d6 1.181 |
| pass16_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.0640 (tb16bal 1.034) | g52 1.327; g54d7 0.923; g56d6 0.905 |
| pass16_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.0410 (tb16bal 1.010) | g52 1.105; g54d7 1.041; g56d6 1.037 |
| pass16_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.0605 (tb16bal 1.238) | g52 0.869; g54d7 0.899; g56d6 0.912 |
| pass16_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 3 S=96 (12 KB) | tb16 0.1210 (tb16bal 1.234) | g52 0.867; g54d7 0.886; g56d6 0.912 |
| pass16_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16bal 0.0604 (tb16 1.002) | g52 0.781; g54d7 0.737; g56d6 0.801 |
| pass16_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB) | tb16 0.0310 (tb16bal 1.323) | g52 1.065; g54d7 0.955; g56d6 1.058 |
| pass16_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 3 S=96 (12 KB) | tb16 0.0619 (tb16bal 1.326) | g52 1.063; g54d7 0.956; g56d6 1.044 |
| pass16_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16bal 0.0980 (tb16 1.002) | g52 0.888; g54d7 0.945; g56d6 1.015 |
| pass16_I4_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16 0.0627 (tb16bal 1.077) | g52 1.010; g54d7 0.989; g56d6 0.997 |
| pass16_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16 0.1074 (tb16bal 1.068) | g52 0.920; g54d7 0.918; g56d6 0.950 |
| pass16_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 4 S=96 (12 KB) | tb16 0.2157 (tb16bal 1.066) | g52 0.916; g54d7 0.908; g56d6 0.942 |
| pass16_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16bal 0.1046 (tb16 1.012) | g52 0.900; g54d7 0.956; g56d6 0.916 |
| pass16_I4_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 4 S=192 (12 KB) | tb16 0.0682 (tb16bal 1.085) | g52 0.997; g54d7 1.018; g56d6 1.029 |
| pass16_I4_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 4 S=96 (12 KB) | tb16 0.1374 (tb16bal 1.087) | g52 0.990; g54d7 1.020; g56d6 1.028 |
| pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB) | tb8bal 0.0384 (tb8 1.182) | g19 0.753; g20 0.724; g22d4 0.734; h20half 0.945 |
| pass8_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB) | tb8 0.0228 (tb8bal 1.061) | g19 0.873; g20 0.846; g22d4 0.816; h20half 0.890 |
| pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB) | tb8bal 0.0369 (tb8 1.230) | g19 0.946; g20 0.846; g22d4 0.856; h20half 0.932 |
| pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB) | tb8bal 0.0776 (tb8 1.170) | g19 0.857; g20 0.776; g22d4 0.798; h20half 0.871 |
| pass8_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB) | tb8bal 0.0378 (tb8 1.201) | g19 0.947; g20 0.786; g22d4 0.839; h20half 0.910 |
| pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB) | tb8 0.0227 (tb8bal 1.075) | g19 0.859; g20 0.802; g22d4 0.793; h20half 0.846 |
| pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB) | tb8 0.0454 (tb8bal 1.081) | g19 0.885; g20 0.811; g22d4 0.769; h20half 0.846 |
| pass8_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB) | tb8bal 0.0428 (tb8 1.061) | g19 0.942; g20 0.729; g22d4 0.825; h20half 1.012 |
| pass8_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB) | tb8 0.0227 (tb8bal 1.070) | g19 0.833; g20 0.806; g22d4 0.793; h20half 0.885 |
| pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB) | tb8 0.0454 (tb8bal 1.057) | g19 0.833; g20 0.718; g22d4 0.767; h20half 0.874 |
| pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB) | tb8 0.0908 (tb8bal 1.076) | g19 0.839; g20 0.699; g22d4 0.761; h20half 0.877 |
| pass8_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB) | tb8bal 0.0376 (tb8 1.207) | g19 0.907; g20 0.827; g22d4 0.795; h20half 0.926 |
| pass8_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB) | tb8 0.0227 (tb8bal 1.026) | g19 0.863; g20 0.824; g22d4 0.819; h20half 0.899 |
| pass8_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB) | tb8 0.0453 (tb8bal 1.015) | g19 0.863; g20 0.823; g22d4 0.826; h20half 0.885 |
| pass8_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB) | tb8bal 0.0446 (tb8 1.018) | g19 0.892; g20 0.827; g22d4 0.834; h20half 0.910 |
| pass8_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB) | tb8 0.0227 (tb8bal 1.084) | g19 0.868; g20 0.833; g22d4 0.819; h20half 0.912 |
| pass8_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB) | tb8 0.0453 (tb8bal 1.201) | g19 0.914; g20 0.828; g22d4 0.830; h20half 0.945 |
| pass8_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 3 S=240 (15 KB) | tb8 0.0906 (tb8bal 1.209) | g19 0.916; g20 0.837; g22d4 0.831; h20half 0.945 |
| pass8_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB) | tb8bal 0.0418 (tb8 1.086) | g19 0.801; g20 0.763; g22d4 0.756; h20half 0.821 |
| pass8_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB) | tb8 0.0229 (tb8bal 1.170) | g19 0.987; g20 0.882; g22d4 0.869; h20half 0.882 |
| pass8_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB) | tb8 0.0453 (tb8bal 1.183) | g19 0.980; g20 0.909; g22d4 0.896; h20half 0.918 |
| pass8_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB) | tb8 0.0621 (tb8bal 1.087) | g19 1.106; g20 1.066; g22d4 1.055; h20half 1.058 |
| pass8_I4_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 4 S=384 (12 KB) | tb8 0.0241 (tb8bal 1.149) | g19 1.029; g20 0.880; g22d4 0.996; h20half 1.033 |
| pass8_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB) | tb8 0.0455 (tb8bal 1.193) | g19 0.998; g20 0.912; g22d4 0.910; h20half 1.002 |
| pass8_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 4 S=240 (15 KB) | tb8 0.0912 (tb8bal 1.217) | g19 1.020; g20 0.928; g22d4 0.923; h20half 1.026 |
| pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB) | tb8 0.0454 (tb8bal 1.051) | g19 0.793; g20 0.703; g22d4 0.733; h20half 0.784 |
| pass8_I4_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 4 S=384 (12 KB) | tb8 0.0227 (tb8bal 1.467) | g19 1.084; g20 1.084; g22d4 1.031; h20half 1.106 |
| pass8_I4_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 4 S=192 (12 KB) | tb8 0.0455 (tb8bal 1.398) | g19 1.044; g20 0.960; g22d4 0.927; h20half 1.064 |
| regs16_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1 | tb16 8.2432 (tb16bal 1.156) | g52 1.498; g54d7 1.321; g56d6 1.791 |
| regs16_I1_clang_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 1 | tb16bal 5.8118 (tb16 1.331) | g52 1.480; g54d7 1.340; g56d6 1.363 |
| regs16_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1 | tb16 9.6243 (tb16bal 1.190) | g52 1.206; g54d7 1.079; g56d6 1.242 |
| regs16_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 1 | tb16 9.6266 (tb16bal 1.190) | g52 1.206; g54d7 1.079; g56d6 1.242 |
| regs16_I1_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 1 | tb16bal 7.0942 (tb16 1.090) | g52 1.285; g54d7 1.164; g56d6 1.233 |
| regs16_I1_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 1 | tb16bal 7.1533 (tb16 1.082) | g52 1.275; g54d7 1.157; g56d6 1.230 |
| regs16_I1_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 1 | tb16bal 7.1297 (tb16 1.084) | g52 1.278; g54d7 1.160; g56d6 1.234 |
| regs16_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2 | tb16 7.8931 (tb16bal 1.171) | g52 1.335; g54d7 1.126; g56d6 1.094 |
| regs16_I2_clang_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2 | tb16bal 7.4904 (tb16 1.042) | g52 1.148; g54d7 0.981; g56d6 0.937 |
| regs16_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2 | tb16 8.4142 (tb16bal 1.227) | g52 1.052; g54d7 1.126; g56d6 1.056 |
| regs16_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 2 | tb16 8.4181 (tb16bal 1.228) | g52 1.051; g54d7 1.121; g56d6 1.052 |
| regs16_I2_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 2 | tb16bal 6.7422 (tb16 1.148) | g52 0.925; g54d7 0.872; g56d6 0.841 |
| regs16_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2 | tb16bal 6.7028 (tb16 1.156) | g52 0.988; g54d7 0.967; g56d6 0.878 |
| regs16_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 2 | tb16bal 6.7064 (tb16 1.154) | g52 0.987; g54d7 0.969; g56d6 0.880 |
| regs8_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1 | tb8 2.9149 (tb8bal 1.183) | g19 1.973; g20 1.914; g22d4 1.411; h20half 1.543 |
| regs8_I1_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 1 | tb8 2.9151 (tb8bal 1.190) | g19 1.973; g20 1.915; g22d4 1.413; h20half 1.545 |
| regs8_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1 | tb8 2.9014 (tb8bal 1.430) | g19 1.850; g20 1.962; g22d4 1.307; h20half 1.686 |
| regs8_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 1 | tb8 2.9000 (tb8bal 1.430) | g19 1.850; g20 1.964; g22d4 1.306; h20half 1.686 |
| regs8_I1_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 1 | tb8 3.3579 (tb8bal 1.272) | g19 1.694; g20 1.621; g22d4 1.146; h20half 1.512 |
| regs8_I1_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 1 | tb8 3.3610 (tb8bal 1.282) | g19 1.688; g20 1.620; g22d4 1.150; h20half 1.512 |
| regs8_I1_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 1 | tb8 3.3576 (tb8bal 1.282) | g19 1.689; g20 1.620; g22d4 1.150; h20half 1.512 |
| regs8_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2 | tb8 2.9193 (tb8bal 1.337) | g19 1.398; g20 1.533; g22d4 1.427; h20half 1.406 |
| regs8_I2_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 2 | tb8bal 2.2000 (tb8 1.318) | g19 1.462; g20 1.491; g22d4 1.178; h20half 1.342 |
| regs8_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2 | tb8 2.9354 (tb8bal 1.154) | g19 1.387; g20 1.653; g22d4 1.321; h20half 1.308 |
| regs8_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 2 | tb8 2.9347 (tb8bal 1.157) | g19 1.386; g20 1.654; g22d4 1.321; h20half 1.307 |
| regs8_I2_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 2 | tb8 2.8993 (tb8bal 1.015) | g19 1.186; g20 1.156; g22d4 0.965; h20half 1.014 |
| regs8_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 2 | tb8bal 2.9028 (tb8 1.001) | g19 1.193; g20 1.153; g22d4 0.959; h20half 0.995 |
| regs8_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 2 | tb8 2.9032 (tb8bal 1.003) | g19 1.193; g20 1.152; g22d4 0.958; h20half 0.993 |
| regs8_I3_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3 | tb8bal 2.6593 (tb8 1.096) | g19 1.314; g20 1.403; g22d4 1.101; h20half 1.285 |
| regs8_I3_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 3 | tb8bal 2.1832 (tb8 1.328) | g19 1.391; g20 1.102; g22d4 0.986; h20half 1.130 |
| regs8_I3_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3 | tb8 3.2274 (tb8bal 1.207) | g19 1.232; g20 1.176; g22d4 1.073; h20half 1.131 |
| regs8_I3_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 3 | tb8 3.2273 (tb8bal 1.207) | g19 1.234; g20 1.176; g22d4 1.073; h20half 1.130 |
| regs8_I3_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 3 | tb8 2.9160 (tb8bal 1.015) | g19 1.087; g20 1.095; g22d4 0.982; h20half 1.024 |
| regs8_I3_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 3 | tb8 2.9609 (tb8bal 1.172) | g19 1.174; g20 1.184; g22d4 1.066; h20half 1.095 |
| regs8_I3_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 3 | tb8 2.9642 (tb8bal 1.170) | g19 1.172; g20 1.182; g22d4 1.064; h20half 1.095 |
| regs8_I4_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4 | tb8bal 2.9160 (tb8 1.028) | g19 1.341; g20 1.420; g22d4 1.049; h20half 1.321 |
| regs8_I4_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 4 | tb8bal 2.2906 (tb8 1.268) | g19 1.084; g20 1.034; g22d4 0.978; h20half 1.078 |
| regs8_I4_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4 | tb8 3.2667 (tb8bal 1.184) | g19 1.114; g20 1.065; g22d4 1.014; h20half 1.082 |
| regs8_I4_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 4 | tb8 3.2701 (tb8bal 1.183) | g19 1.111; g20 1.064; g22d4 1.013; h20half 1.082 |
| regs8_I4_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 4 | tb8 2.9140 (tb8bal 1.033) | g19 0.933; g20 0.941; g22d4 0.782; h20half 0.943 |
| regs8_I4_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 4 | tb8 3.3140 (tb8bal 1.221) | g19 1.080; g20 1.034; g22d4 0.963; h20half 1.082 |
| regs8_I4_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 4 | tb8 3.3146 (tb8bal 1.221) | g19 1.080; g20 1.033; g22d4 0.961; h20half 1.081 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^6 same I=1 | FFHT 0.2252 (textbook 1.501, textbook-bal 1.777) | g52+tb8 1.689; g56d6+tb8 1.881; g52+g19 1.882; g56d6+g22d4 2.265 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^8 same I=1 | FFHT 0.2049 (textbook 1.203, textbook-bal 1.339) | g52+tb8 1.237; g56d6+tb8 1.331; g52+g19 1.306; g56d6+g22d4 1.427 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^10 same I=1 | FFHT 0.2442 (textbook 1.051, textbook-bal 1.111) | g52+tb8 0.981; g56d6+tb8 1.078; g52+g19 1.002; g56d6+g22d4 1.076 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^12 same I=1 | FFHT 0.2569 (textbook 1.086, textbook-bal 1.109) | g52+tb8 1.009; g56d6+tb8 1.092; g52+g19 1.049; g56d6+g22d4 1.090 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^14 same I=1 | FFHT 0.2877 (textbook 1.055, textbook-bal 1.076) | g52+tb8 0.987; g56d6+tb8 1.063; g52+g19 1.017; g56d6+g22d4 1.061 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^16 same I=1 | textbook-bal 0.3241 (textbook 1.005, FFHT 1.030) | g52+tb8 0.943; g56d6+tb8 1.007; g52+g19 0.895; g56d6+g22d4 0.956 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^18 same I=1 | FFHT 0.3519 (textbook 1.014, textbook-bal 1.018) | g52+tb8 0.961; g56d6+tb8 1.018; g52+g19 0.923; g56d6+g22d4 0.971 |
| whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^20 same I=1 | FFHT 0.3860 (textbook 1.048, textbook-bal 1.031) | g52+tb8 0.999; g56d6+tb8 1.051; g52+g19 0.949; g56d6+g22d4 1.002 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^6 same I=1 | FFHT 0.2253 (textbook 1.479, textbook-bal 1.668) | g52+tb8 1.660; g56d6+tb8 1.838; g52+g19 1.810; g56d6+g22d4 2.149 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^8 same I=1 | FFHT 0.2035 (textbook 1.123, textbook-bal 1.258) | g52+tb8 1.135; g56d6+tb8 1.324; g52+g19 1.226; g56d6+g22d4 1.281 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^10 same I=1 | FFHT 0.2354 (textbook 1.010, textbook-bal 1.049) | g52+tb8 0.967; g56d6+tb8 1.011; g52+g19 0.972; g56d6+g22d4 1.020 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^12 same I=1 | FFHT 0.2559 (textbook 1.046, textbook-bal 1.139) | g52+tb8 0.939; g56d6+tb8 1.009; g52+g19 0.943; g56d6+g22d4 1.014 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^14 same I=1 | FFHT 0.2873 (textbook 1.024, textbook-bal 1.092) | g52+tb8 0.923; g56d6+tb8 0.975; g52+g19 0.922; g56d6+g22d4 0.977 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^16 same I=1 | textbook 0.3144 (textbook-bal 1.040, FFHT 1.027) | g52+tb8 0.904; g56d6+tb8 0.954; g52+g19 0.868; g56d6+g22d4 0.912 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^18 same I=1 | textbook 0.3471 (textbook-bal 1.039, FFHT 1.005) | g52+tb8 0.916; g56d6+tb8 0.964; g52+g19 0.899; g56d6+g22d4 0.922 |
| whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^20 same I=1 | FFHT 0.3812 (textbook 1.033, textbook-bal 1.057) | g52+tb8 0.955; g56d6+tb8 0.996; g52+g19 1.006; g56d6+g22d4 0.952 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^6 same I=1 | FFHT 0.2254 (textbook 1.612, textbook-bal 1.507) | g52+tb8 1.511; g56d6+tb8 1.748; g52+g19 1.782; g56d6+g22d4 2.034 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^8 same I=1 | textbook-bal 0.1834 (textbook 1.008, FFHT 1.116) | g52+tb8 0.933; g56d6+tb8 1.040; g52+g19 1.061; g56d6+g22d4 1.110 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^10 same I=1 | textbook 0.1474 (textbook-bal 1.017, FFHT 1.596) | g52+tb8 0.991; g56d6+tb8 1.043; g52+g19 1.014; g56d6+g22d4 1.062 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^12 same I=1 | textbook 0.1510 (textbook-bal 1.015, FFHT 1.693) | g52+tb8 0.930; g56d6+tb8 0.944; g52+g19 0.951; g56d6+g22d4 0.972 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^14 same I=1 | textbook-bal 0.1812 (textbook 1.022, FFHT 1.586) | g52+tb8 0.949; g56d6+tb8 0.963; g52+g19 0.955; g56d6+g22d4 0.969 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^16 same I=1 | textbook-bal 0.1860 (textbook 1.019, FFHT 1.738) | g52+tb8 0.948; g56d6+tb8 0.959; g52+g19 0.940; g56d6+g22d4 0.947 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^18 same I=1 | textbook-bal 0.2216 (textbook 1.023, FFHT 1.571) | g52+tb8 0.946; g56d6+tb8 0.935; g52+g19 0.946; g56d6+g22d4 0.918 |
| whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^20 same I=1 | textbook-bal 0.2683 (textbook 1.012, FFHT 1.422) | g52+tb8 0.963; g56d6+tb8 0.971; g52+g19 0.967; g56d6+g22d4 1.039 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1 | FFHT 0.2839 (textbook 1.201, textbook-bal 1.180) | g52+tb8 1.042; g56d6+tb8 1.157; g52+g19 1.033; g56d6+g22d4 1.150 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1 | textbook-bal 0.3435 (textbook 1.016, FFHT 1.026) | g52+tb8 0.953; g56d6+tb8 1.003; g52+g19 0.908; g56d6+g22d4 0.957 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1 | textbook 0.4601 (textbook-bal 1.002, FFHT 1.062) | g52+tb8 0.968; g56d6+tb8 1.010; g52+g19 0.940; g56d6+g22d4 0.987 |
| whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1 | FFHT 0.5929 (textbook 1.236, textbook-bal 1.255) | g52+tb8 1.190; g56d6+tb8 1.232; g52+g19 1.196; g56d6+g22d4 1.234 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1 | FFHT 0.3114 (textbook 1.039, textbook-bal 1.096) | g52+tb8 0.929; g56d6+tb8 0.989; g52+g19 0.917; g56d6+g22d4 0.980 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1 | textbook 0.3409 (textbook-bal 1.039, FFHT 1.005) | g52+tb8 0.908; g56d6+tb8 0.945; g52+g19 0.873; g56d6+g22d4 0.908 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1 | FFHT 0.4330 (textbook 1.047, textbook-bal 1.106) | g52+tb8 0.994; g56d6+tb8 1.027; g52+g19 0.981; g56d6+g22d4 0.999 |
| whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1 | FFHT 0.5579 (textbook 1.281, textbook-bal 1.348) | g52+tb8 1.234; g56d6+tb8 1.262; g52+g19 1.224; g56d6+g22d4 1.253 |
| whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^12 separate I=1 | textbook 0.1728 (textbook-bal 1.113, FFHT 1.805) | g52+tb8 0.985; g56d6+tb8 1.050; g52+g19 0.991; g56d6+g22d4 1.115 |
| whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^16 separate I=1 | textbook-bal 0.2246 (textbook 1.015, FFHT 1.533) | g52+tb8 0.939; g56d6+tb8 0.956; g52+g19 0.933; g56d6+g22d4 0.944 |
| whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^20 separate I=1 | textbook 0.3430 (textbook-bal 1.025, FFHT 1.266) | g52+tb8 0.988; g56d6+tb8 0.990; g52+g19 0.994; g56d6+g22d4 0.988 |
| whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^24 separate I=1 | FFHT 0.5579 (textbook 1.137, textbook-bal 1.133) | g52+tb8 1.114; g56d6+tb8 1.124; g52+g19 1.123; g56d6+g22d4 1.126 |

## Port balancing alone (the textbook with half its adds as FMA by 1, against the plain textbook and FFHT)

A second lead, independent of the circuits: if the balanced textbook is 10 % or more faster than both the plain
textbook and FFHT in whole transforms, an x86 WHT library (FFHT, used by SpinQuant on x86) gains by balancing alone.

- pass16_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.936
- pass16_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.934
- pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.028
- pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.029
- pass16_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.808
- pass16_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.891
- pass16_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 1 S=96 (12 KB): balanced / best other textbook-or-FFHT = 0.904
- pass16_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.042
- pass16_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.006
- pass16_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.329
- pass16_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 2 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.333
- pass16_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.069
- pass16_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.487
- pass16_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.445
- pass16_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.034
- pass16_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.010
- pass16_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.238
- pass16_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 3 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.234
- pass16_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.998
- pass16_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.323
- pass16_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 3 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.326
- pass16_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.998
- pass16_I4_clang_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.077
- pass16_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.068
- pass16_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 4 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.066
- pass16_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 0.988
- pass16_I4_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.085
- pass16_I4_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 4 S=96 (12 KB): balanced / best other textbook-or-FFHT = 1.087
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.846
- pass8_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): balanced / best other textbook-or-FFHT = 1.061
- pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.813
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): balanced / best other textbook-or-FFHT = 0.855
- pass8_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.833
- pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): balanced / best other textbook-or-FFHT = 1.075
- pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.081
- pass8_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.943
- pass8_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): balanced / best other textbook-or-FFHT = 1.070
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.057
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.076
- pass8_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.828
- pass8_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): balanced / best other textbook-or-FFHT = 1.026
- pass8_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.015
- pass8_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.982
- pass8_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): balanced / best other textbook-or-FFHT = 1.084
- pass8_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.201
- pass8_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 3 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.209
- pass8_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): balanced / best other textbook-or-FFHT = 0.921
- pass8_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): balanced / best other textbook-or-FFHT = 1.170
- pass8_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.183
- pass8_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.087
- pass8_I4_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 4 S=384 (12 KB): balanced / best other textbook-or-FFHT = 1.149
- pass8_I4_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.193
- pass8_I4_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 4 S=240 (15 KB): balanced / best other textbook-or-FFHT = 1.217
- pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): balanced / best other textbook-or-FFHT = 1.051
- pass8_I4_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 4 S=384 (12 KB): balanced / best other textbook-or-FFHT = 1.467
- pass8_I4_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 4 S=192 (12 KB): balanced / best other textbook-or-FFHT = 1.398
- regs16_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 1.156
- regs16_I1_clang_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.751
- regs16_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 1.190
- regs16_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 1.190
- regs16_I1_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.917
- regs16_I1_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.924
- regs16_I1_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 1: balanced / best other textbook-or-FFHT = 0.922
- regs16_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 1.171
- regs16_I2_clang_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 0.959
- regs16_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 1.227
- regs16_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 1.228
- regs16_I2_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 0.871
- regs16_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 0.865
- regs16_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 2: balanced / best other textbook-or-FFHT = 0.866
- regs8_I1_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 1.183
- regs8_I1_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 1.190
- regs8_I1_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 1.430
- regs8_I1_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 1.430
- regs8_I1_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 1.272
- regs8_I1_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 1.282
- regs8_I1_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 1: balanced / best other textbook-or-FFHT = 1.282
- regs8_I2_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 1.337
- regs8_I2_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 0.759
- regs8_I2_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 1.154
- regs8_I2_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 1.157
- regs8_I2_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 1.015
- regs8_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 0.999
- regs8_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 2: balanced / best other textbook-or-FFHT = 1.003
- regs8_I3_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 0.912
- regs8_I3_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 0.753
- regs8_I3_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 1.207
- regs8_I3_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 1.207
- regs8_I3_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 1.015
- regs8_I3_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 1.172
- regs8_I3_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 3: balanced / best other textbook-or-FFHT = 1.170
- regs8_I4_clang_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 0.973
- regs8_I4_clang_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 0.789
- regs8_I4_gcc_avx2_f32: x86 regs 256bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.184
- regs8_I4_gcc_avx2_f64: x86 regs 256bit-f64 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.183
- regs8_I4_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.033
- regs8_I4_gcc_avx512_f32: x86 regs 512bit-f32 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.221
- regs8_I4_gcc_avx512_f64: x86 regs 512bit-f64 radix-8 interleave 4: balanced / best other textbook-or-FFHT = 1.221
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^6 same I=1: balanced / best other textbook-or-FFHT = 1.777 (FFHT 0.2252, plain textbook 0.3381, balanced 0.4001 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.339 (FFHT 0.2049, plain textbook 0.2465, balanced 0.2744 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^10 same I=1: balanced / best other textbook-or-FFHT = 1.111 (FFHT 0.2442, plain textbook 0.2567, balanced 0.2714 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^12 same I=1: balanced / best other textbook-or-FFHT = 1.109 (FFHT 0.2569, plain textbook 0.2791, balanced 0.2849 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^14 same I=1: balanced / best other textbook-or-FFHT = 1.076 (FFHT 0.2877, plain textbook 0.3036, balanced 0.3097 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^16 same I=1: balanced / best other textbook-or-FFHT = 0.995 (FFHT 0.3338, plain textbook 0.3257, balanced 0.3241 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^18 same I=1: balanced / best other textbook-or-FFHT = 1.018 (FFHT 0.3519, plain textbook 0.3568, balanced 0.3582 ns)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^20 same I=1: balanced / best other textbook-or-FFHT = 1.031 (FFHT 0.3860, plain textbook 0.4047, balanced 0.3979 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^6 same I=1: balanced / best other textbook-or-FFHT = 1.668 (FFHT 0.2253, plain textbook 0.3333, balanced 0.3759 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^8 same I=1: balanced / best other textbook-or-FFHT = 1.258 (FFHT 0.2035, plain textbook 0.2286, balanced 0.2561 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^10 same I=1: balanced / best other textbook-or-FFHT = 1.049 (FFHT 0.2354, plain textbook 0.2378, balanced 0.2469 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^12 same I=1: balanced / best other textbook-or-FFHT = 1.139 (FFHT 0.2559, plain textbook 0.2677, balanced 0.2914 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^14 same I=1: balanced / best other textbook-or-FFHT = 1.092 (FFHT 0.2873, plain textbook 0.2942, balanced 0.3138 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^16 same I=1: balanced / best other textbook-or-FFHT = 1.040 (FFHT 0.3230, plain textbook 0.3144, balanced 0.3271 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^18 same I=1: balanced / best other textbook-or-FFHT = 1.039 (FFHT 0.3489, plain textbook 0.3471, balanced 0.3605 ns)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^20 same I=1: balanced / best other textbook-or-FFHT = 1.057 (FFHT 0.3812, plain textbook 0.3936, balanced 0.4028 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^6 same I=1: balanced / best other textbook-or-FFHT = 1.507 (FFHT 0.2254, plain textbook 0.3634, balanced 0.3397 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^8 same I=1: balanced / best other textbook-or-FFHT = 0.992 (FFHT 0.2046, plain textbook 0.1849, balanced 0.1834 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^10 same I=1: balanced / best other textbook-or-FFHT = 1.017 (FFHT 0.2352, plain textbook 0.1474, balanced 0.1499 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^12 same I=1: balanced / best other textbook-or-FFHT = 1.015 (FFHT 0.2557, plain textbook 0.1510, balanced 0.1533 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^14 same I=1: balanced / best other textbook-or-FFHT = 0.979 (FFHT 0.2873, plain textbook 0.1851, balanced 0.1812 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^16 same I=1: balanced / best other textbook-or-FFHT = 0.981 (FFHT 0.3232, plain textbook 0.1896, balanced 0.1860 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^18 same I=1: balanced / best other textbook-or-FFHT = 0.977 (FFHT 0.3482, plain textbook 0.2268, balanced 0.2216 ns)
- whole_same_gcc_avx512_f32: x86 whole 512bit-f32 2^20 same I=1: balanced / best other textbook-or-FFHT = 0.988 (FFHT 0.3816, plain textbook 0.2716, balanced 0.2683 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1: balanced / best other textbook-or-FFHT = 1.180 (FFHT 0.2839, plain textbook 0.3410, balanced 0.3350 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1: balanced / best other textbook-or-FFHT = 0.985 (FFHT 0.3526, plain textbook 0.3489, balanced 0.3435 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.002 (FFHT 0.4884, plain textbook 0.4601, balanced 0.4609 ns)
- whole_sep_clang_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.255 (FFHT 0.5929, plain textbook 0.7327, balanced 0.7439 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^12 separate I=1: balanced / best other textbook-or-FFHT = 1.096 (FFHT 0.3114, plain textbook 0.3237, balanced 0.3412 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1: balanced / best other textbook-or-FFHT = 1.039 (FFHT 0.3426, plain textbook 0.3409, balanced 0.3543 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.106 (FFHT 0.4330, plain textbook 0.4535, balanced 0.4787 ns)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.348 (FFHT 0.5579, plain textbook 0.7148, balanced 0.7521 ns)
- whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^12 separate I=1: balanced / best other textbook-or-FFHT = 1.113 (FFHT 0.3119, plain textbook 0.1728, balanced 0.1924 ns)
- whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^16 separate I=1: balanced / best other textbook-or-FFHT = 0.985 (FFHT 0.3444, plain textbook 0.2280, balanced 0.2246 ns)
- whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^20 separate I=1: balanced / best other textbook-or-FFHT = 1.025 (FFHT 0.4341, plain textbook 0.3430, balanced 0.3516 ns)
- whole_sep_gcc_avx512_f32: x86 whole 512bit-f32 2^24 separate I=1: balanced / best other textbook-or-FFHT = 1.133 (FFHT 0.5579, plain textbook 0.6345, balanced 0.6323 ns)

## Cases at or below 0.90 of the fastest baseline (CHECK the whole-transform rows before believing a pass row)

- pass16_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g52 0.749 (baseline tb16bal)
- pass16_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g54d7 0.864 (baseline tb16bal)
- pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g52 0.669 (baseline tb16)
- pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g54d7 0.737 (baseline tb16)
- pass16_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g56d6 0.788 (baseline tb16)
- pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): g52 0.662 (baseline tb16)
- pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): g54d7 0.743 (baseline tb16)
- pass16_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 1 S=96 (12 KB): g56d6 0.788 (baseline tb16)
- pass16_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 1 S=192 (12 KB): g52 0.791 (baseline tb16bal)
- pass16_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB): g52 0.815 (baseline tb16bal)
- pass16_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB): g54d7 0.874 (baseline tb16bal)
- pass16_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 1 S=192 (12 KB): g56d6 0.889 (baseline tb16bal)
- pass16_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 1 S=96 (12 KB): g52 0.834 (baseline tb16bal)
- pass16_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 1 S=96 (12 KB): g54d7 0.846 (baseline tb16bal)
- pass16_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 1 S=96 (12 KB): g56d6 0.876 (baseline tb16bal)
- pass16_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): g52 0.893 (baseline tb16)
- pass16_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): g52 0.697 (baseline tb16)
- pass16_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): g54d7 0.758 (baseline tb16)
- pass16_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 2 S=192 (12 KB): g56d6 0.761 (baseline tb16)
- pass16_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-16 interleave 2 S=192 (12 KB): g52 0.839 (baseline tb16)
- pass16_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB): g52 0.845 (baseline tb16)
- pass16_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-16 interleave 2 S=96 (12 KB): g54d7 0.866 (baseline tb16)
- pass16_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): g52 0.869 (baseline tb16)
- pass16_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): g54d7 0.899 (baseline tb16)
- pass16_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 3 S=96 (12 KB): g52 0.867 (baseline tb16)
- pass16_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-16 interleave 3 S=96 (12 KB): g54d7 0.886 (baseline tb16)
- pass16_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): g52 0.781 (baseline tb16bal)
- pass16_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): g54d7 0.737 (baseline tb16bal)
- pass16_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 3 S=192 (12 KB): g56d6 0.801 (baseline tb16bal)
- pass16_I4_clang_avx2_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB): g52 0.888 (baseline tb16bal)
- pass16_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-16 interleave 4 S=192 (12 KB): g52 0.900 (baseline tb16bal)
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g19 0.753 (baseline tb8bal)
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g20 0.724 (baseline tb8bal)
- pass8_I1_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g22d4 0.734 (baseline tb8bal)
- pass8_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): g19 0.873 (baseline tb8)
- pass8_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): g20 0.846 (baseline tb8)
- pass8_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): g22d4 0.816 (baseline tb8)
- pass8_I1_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): h20half 0.890 (baseline tb8)
- pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g20 0.846 (baseline tb8bal)
- pass8_I1_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g22d4 0.856 (baseline tb8bal)
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): g19 0.857 (baseline tb8bal)
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): g20 0.776 (baseline tb8bal)
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): g22d4 0.798 (baseline tb8bal)
- pass8_I1_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 1 S=240 (15 KB): h20half 0.871 (baseline tb8bal)
- pass8_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g20 0.786 (baseline tb8bal)
- pass8_I1_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 1 S=480 (15 KB): g22d4 0.839 (baseline tb8bal)
- pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): g19 0.859 (baseline tb8)
- pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): g20 0.802 (baseline tb8)
- pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): g22d4 0.793 (baseline tb8)
- pass8_I1_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 1 S=384 (12 KB): h20half 0.846 (baseline tb8)
- pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): g19 0.885 (baseline tb8)
- pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): g20 0.811 (baseline tb8)
- pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): g22d4 0.769 (baseline tb8)
- pass8_I1_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 1 S=192 (12 KB): h20half 0.846 (baseline tb8)
- pass8_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g20 0.729 (baseline tb8bal)
- pass8_I2_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g22d4 0.825 (baseline tb8bal)
- pass8_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): g19 0.833 (baseline tb8)
- pass8_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): g20 0.806 (baseline tb8)
- pass8_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): g22d4 0.793 (baseline tb8)
- pass8_I2_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): h20half 0.885 (baseline tb8)
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g19 0.833 (baseline tb8)
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g20 0.718 (baseline tb8)
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g22d4 0.767 (baseline tb8)
- pass8_I2_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): h20half 0.874 (baseline tb8)
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): g19 0.839 (baseline tb8)
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): g20 0.699 (baseline tb8)
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): g22d4 0.761 (baseline tb8)
- pass8_I2_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 2 S=240 (15 KB): h20half 0.877 (baseline tb8)
- pass8_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g20 0.827 (baseline tb8bal)
- pass8_I2_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 2 S=480 (15 KB): g22d4 0.795 (baseline tb8bal)
- pass8_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): g19 0.863 (baseline tb8)
- pass8_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): g20 0.824 (baseline tb8)
- pass8_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): g22d4 0.819 (baseline tb8)
- pass8_I2_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 2 S=384 (12 KB): h20half 0.899 (baseline tb8)
- pass8_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB): g19 0.863 (baseline tb8)
- pass8_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB): g20 0.823 (baseline tb8)
- pass8_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB): g22d4 0.826 (baseline tb8)
- pass8_I2_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 2 S=192 (12 KB): h20half 0.885 (baseline tb8)
- pass8_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g19 0.892 (baseline tb8bal)
- pass8_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g20 0.827 (baseline tb8bal)
- pass8_I3_clang_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g22d4 0.834 (baseline tb8bal)
- pass8_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): g19 0.868 (baseline tb8)
- pass8_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): g20 0.833 (baseline tb8)
- pass8_I3_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): g22d4 0.819 (baseline tb8)
- pass8_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g20 0.828 (baseline tb8)
- pass8_I3_gcc_avx2_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g22d4 0.830 (baseline tb8)
- pass8_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 3 S=240 (15 KB): g20 0.837 (baseline tb8)
- pass8_I3_gcc_avx2_f64: x86 pass 256bit-f64 radix-8 interleave 3 S=240 (15 KB): g22d4 0.831 (baseline tb8)
- pass8_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g19 0.801 (baseline tb8bal)
- pass8_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g20 0.763 (baseline tb8bal)
- pass8_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): g22d4 0.756 (baseline tb8bal)
- pass8_I3_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 3 S=480 (15 KB): h20half 0.821 (baseline tb8bal)
- pass8_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): g20 0.882 (baseline tb8)
- pass8_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): g22d4 0.869 (baseline tb8)
- pass8_I3_gcc_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 3 S=384 (12 KB): h20half 0.882 (baseline tb8)
- pass8_I3_gcc_avx512_f64: x86 pass 512bit-f64 radix-8 interleave 3 S=192 (12 KB): g22d4 0.896 (baseline tb8)
- pass8_I4_clang_avx512_f32: x86 pass 512bit-f32 radix-8 interleave 4 S=384 (12 KB): g20 0.880 (baseline tb8)
- pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): g19 0.793 (baseline tb8)
- pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): g20 0.703 (baseline tb8)
- pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): g22d4 0.733 (baseline tb8)
- pass8_I4_gcc_avx2r32_f32: x86 pass 256bit-f32 radix-8 interleave 4 S=480 (15 KB): h20half 0.784 (baseline tb8)
- regs16_I2_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 2: g54d7 0.872 (baseline tb16bal)
- regs16_I2_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-16 interleave 2: g56d6 0.841 (baseline tb16bal)
- regs16_I2_gcc_avx512_f32: x86 regs 512bit-f32 radix-16 interleave 2: g56d6 0.878 (baseline tb16bal)
- regs16_I2_gcc_avx512_f64: x86 regs 512bit-f64 radix-16 interleave 2: g56d6 0.880 (baseline tb16bal)
- regs8_I4_gcc_avx2r32_f32: x86 regs 256bit-f32 radix-8 interleave 4: g22d4 0.782 (baseline tb8)
- whole_same_clang_avx2_f32: x86 whole 256bit-f32 2^16 same I=1: g52+g19 0.895 (baseline textbook-bal)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^16 same I=1: g52+g19 0.868 (baseline textbook)
- whole_same_gcc_avx2_f32: x86 whole 256bit-f32 2^18 same I=1: g52+g19 0.899 (baseline textbook)
- whole_sep_gcc_avx2_f32: x86 whole 256bit-f32 2^16 separate I=1: g52+g19 0.873 (baseline textbook)
