/* plans.inc -- written by gen.py from plans.json.  Do not edit.  See gen.py. */
#ifdef PLAN_FLOAT
/* float 2^3: P = 0; base block 2^3 */
TOP FN(k3_d3)(ELT *buf) { FIRST1(buf, 8); }
/* float 2^4: P = 0; base block 2^4 */
TOP FN(k4_d4)(ELT *buf) { FIRST2(buf, 16); }
/* float 2^5: P = 0; base block 2^5 */
TOP FN(k5_d5)(ELT *buf) { FIRST4(buf, 32); }
/* float 2^6: P = 1; base block 2^6 */
TOP FN(k6_d6)(ELT *buf) { FIRST8L(buf, 64, 1); SWEEP(buf, 64, 1); }
/* float 2^7: P = 1; base block 2^7 */
TOP FN(k7_d7)(ELT *buf) { FIRST8L(buf, 128, 1); PASS1(buf, 128, 64); SWEEP(buf, 128, 1); }
/* float 2^8: P = 1; base block 2^6 */
BLOCK FN(k8_d6)(ELT *buf) { FIRST8L(buf, 64, 1); }
TOP FN(k8_d8)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k8_d6)(buf + (size_t)i * 64); PASS2(buf, 256, 64); SWEEP(buf, 256, 1); }
/* float 2^9: P = 2; base block 2^9 */
TOP FN(k9_d9)(ELT *buf) { FIRST8(buf, 512); PASS3L(buf, 512, 64, 2); SWEEP(buf, 512, 2); }
/* float 2^10: P = 2; base block 2^10 */
TOP FN(k10_d10)(ELT *buf) { FIRST8(buf, 1024); PASS3L(buf, 1024, 64, 2); PASS1(buf, 1024, 512); SWEEP(buf, 1024, 2); }
/* float 2^11: P = 2; base block 2^11 */
TOP FN(k11_d11)(ELT *buf) { FIRST8(buf, 2048); PASS3L(buf, 2048, 64, 2); PASS2(buf, 2048, 512); SWEEP(buf, 2048, 2); }
/* float 2^12: P = 3; base block 2^12 */
TOP FN(k12_d12)(ELT *buf) { FIRST8(buf, 4096); PASS3(buf, 4096, 64); PASS3L(buf, 4096, 512, 3); SWEEP(buf, 4096, 3); }
/* float 2^13: P = 2; base block 2^11 */
BLOCK FN(k13_d11)(ELT *buf) { FIRST8(buf, 2048); PASS3L(buf, 2048, 64, 2); PASS2(buf, 2048, 512); }
TOP FN(k13_d13)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k13_d11)(buf + (size_t)i * 2048); PASS2(buf, 8192, 2048); SWEEP(buf, 8192, 2); }
/* float 2^14: P = 3; base block 2^12 */
BLOCK FN(k14_d12)(ELT *buf) { FIRST8(buf, 4096); PASS3(buf, 4096, 64); PASS3L(buf, 4096, 512, 3); }
TOP FN(k14_d14)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k14_d12)(buf + (size_t)i * 4096); PASS2(buf, 16384, 4096); SWEEP(buf, 16384, 3); }
/* float 2^15: P = 3; base block 2^13 */
BLOCK FN(k15_d13)(ELT *buf) { FIRST8(buf, 8192); PASS3(buf, 8192, 64); PASS3L(buf, 8192, 512, 3); PASS1(buf, 8192, 4096); }
TOP FN(k15_d15)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k15_d13)(buf + (size_t)i * 8192); PASS2(buf, 32768, 8192); SWEEP(buf, 32768, 3); }
/* float 2^16: P = 4; base block 2^13 */
BLOCK FN(k16_d13)(ELT *buf) { FIRST8(buf, 8192); PASS3(buf, 8192, 64); PASS3(buf, 8192, 512); PASS1(buf, 8192, 4096); }
TOP FN(k16_d16)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k16_d13)(buf + (size_t)i * 8192); PASS3L(buf, 65536, 8192, 4); SWEEP(buf, 65536, 4); }
/* float 2^17: P = 4; base block 2^12 */
BLOCK FN(k17_d12)(ELT *buf) { FIRST8(buf, 4096); PASS3(buf, 4096, 64); PASS3(buf, 4096, 512); }
BLOCK FN(k17_d15)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k17_d12)(buf + (size_t)i * 4096); PASS3L(buf, 32768, 4096, 4); }
TOP FN(k17_d17)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k17_d15)(buf + (size_t)i * 32768); PASS2(buf, 131072, 32768); SWEEP(buf, 131072, 4); }
/* float 2^18: P = 5; base block 2^12 */
BLOCK FN(k18_d12)(ELT *buf) { FIRST8(buf, 4096); PASS3(buf, 4096, 64); PASS3(buf, 4096, 512); }
BLOCK FN(k18_d15)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k18_d12)(buf + (size_t)i * 4096); PASS3(buf, 32768, 4096); }
TOP FN(k18_d18)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k18_d15)(buf + (size_t)i * 32768); PASS3L(buf, 262144, 32768, 5); SWEEP(buf, 262144, 5); }
/* float 2^19: P = 5; base block 2^13 */
BLOCK FN(k19_d13)(ELT *buf) { FIRST8(buf, 8192); PASS3(buf, 8192, 64); PASS3(buf, 8192, 512); PASS1(buf, 8192, 4096); }
BLOCK FN(k19_d16)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k19_d13)(buf + (size_t)i * 8192); PASS3(buf, 65536, 8192); }
TOP FN(k19_d19)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k19_d16)(buf + (size_t)i * 65536); PASS3L(buf, 524288, 65536, 5); SWEEP(buf, 524288, 5); }
/* float 2^20: P = 5; base block 2^12 */
BLOCK FN(k20_d12)(ELT *buf) { FIRST8(buf, 4096); PASS3(buf, 4096, 64); PASS3(buf, 4096, 512); }
BLOCK FN(k20_d15)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k20_d12)(buf + (size_t)i * 4096); PASS3(buf, 32768, 4096); }
BLOCK FN(k20_d18)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k20_d15)(buf + (size_t)i * 32768); PASS3L(buf, 262144, 32768, 5); }
TOP FN(k20_d20)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k20_d18)(buf + (size_t)i * 262144); PASS2(buf, 1048576, 262144); SWEEP(buf, 1048576, 5); }
/* float 2^21: P = 6; base block 2^9 */
BLOCK FN(k21_d9)(ELT *buf) { FIRST8(buf, 512); PASS3(buf, 512, 64); }
BLOCK FN(k21_d12)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k21_d9)(buf + (size_t)i * 512); PASS3(buf, 4096, 512); }
BLOCK FN(k21_d15)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k21_d12)(buf + (size_t)i * 4096); PASS3(buf, 32768, 4096); }
BLOCK FN(k21_d18)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k21_d15)(buf + (size_t)i * 32768); PASS3(buf, 262144, 32768); }
TOP FN(k21_d21)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k21_d18)(buf + (size_t)i * 262144); PASS3L(buf, 2097152, 262144, 6); SWEEP(buf, 2097152, 6); }
/* float 2^22: P = 5; base block 2^11 */
BLOCK FN(k22_d11)(ELT *buf) { FIRST8(buf, 2048); PASS3(buf, 2048, 64); PASS2(buf, 2048, 512); }
BLOCK FN(k22_d14)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k22_d11)(buf + (size_t)i * 2048); PASS3(buf, 16384, 2048); }
BLOCK FN(k22_d17)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k22_d14)(buf + (size_t)i * 16384); PASS3(buf, 131072, 16384); }
BLOCK FN(k22_d20)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k22_d17)(buf + (size_t)i * 131072); PASS3L(buf, 1048576, 131072, 5); }
TOP FN(k22_d22)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k22_d20)(buf + (size_t)i * 1048576); PASS2(buf, 4194304, 1048576); SWEEP(buf, 4194304, 5); }
/* float 2^23: P = 6; base block 2^9 */
BLOCK FN(k23_d9)(ELT *buf) { FIRST8(buf, 512); PASS3(buf, 512, 64); }
BLOCK FN(k23_d12)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k23_d9)(buf + (size_t)i * 512); PASS3(buf, 4096, 512); }
BLOCK FN(k23_d15)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k23_d12)(buf + (size_t)i * 4096); PASS3(buf, 32768, 4096); }
BLOCK FN(k23_d18)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k23_d15)(buf + (size_t)i * 32768); PASS3(buf, 262144, 32768); }
BLOCK FN(k23_d21)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k23_d18)(buf + (size_t)i * 262144); PASS3L(buf, 2097152, 262144, 6); }
TOP FN(k23_d23)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k23_d21)(buf + (size_t)i * 2097152); PASS2(buf, 8388608, 2097152); SWEEP(buf, 8388608, 6); }
/* float 2^24: P = 7; base block 2^12 */
BLOCK FN(k24_d12)(ELT *buf) { FIRST8(buf, 4096); PASS3(buf, 4096, 64); PASS3(buf, 4096, 512); }
BLOCK FN(k24_d15)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k24_d12)(buf + (size_t)i * 4096); PASS3(buf, 32768, 4096); }
BLOCK FN(k24_d18)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k24_d15)(buf + (size_t)i * 32768); PASS3(buf, 262144, 32768); }
BLOCK FN(k24_d21)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k24_d18)(buf + (size_t)i * 262144); PASS3(buf, 2097152, 262144); }
TOP FN(k24_d24)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k24_d21)(buf + (size_t)i * 2097152); PASS3L(buf, 16777216, 2097152, 7); SWEEP(buf, 16777216, 7); }
/* float 2^25: P = 7; base block 2^7 */
BLOCK FN(k25_d7)(ELT *buf) { FIRST8(buf, 128); PASS1(buf, 128, 64); }
BLOCK FN(k25_d10)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k25_d7)(buf + (size_t)i * 128); PASS3(buf, 1024, 128); }
BLOCK FN(k25_d13)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k25_d10)(buf + (size_t)i * 1024); PASS3(buf, 8192, 1024); }
BLOCK FN(k25_d16)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k25_d13)(buf + (size_t)i * 8192); PASS3(buf, 65536, 8192); }
BLOCK FN(k25_d19)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k25_d16)(buf + (size_t)i * 65536); PASS3(buf, 524288, 65536); }
BLOCK FN(k25_d22)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k25_d19)(buf + (size_t)i * 524288); PASS3(buf, 4194304, 524288); }
TOP FN(k25_d25)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k25_d22)(buf + (size_t)i * 4194304); PASS3L(buf, 33554432, 4194304, 7); SWEEP(buf, 33554432, 7); }
/* float 2^26: P = 7; base block 2^12 */
BLOCK FN(k26_d12)(ELT *buf) { FIRST8(buf, 4096); PASS3(buf, 4096, 64); PASS3(buf, 4096, 512); }
BLOCK FN(k26_d15)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k26_d12)(buf + (size_t)i * 4096); PASS3(buf, 32768, 4096); }
BLOCK FN(k26_d18)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k26_d15)(buf + (size_t)i * 32768); PASS3(buf, 262144, 32768); }
BLOCK FN(k26_d21)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k26_d18)(buf + (size_t)i * 262144); PASS3(buf, 2097152, 262144); }
BLOCK FN(k26_d24)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k26_d21)(buf + (size_t)i * 2097152); PASS3L(buf, 16777216, 2097152, 7); }
TOP FN(k26_d26)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k26_d24)(buf + (size_t)i * 16777216); PASS2(buf, 67108864, 16777216); SWEEP(buf, 67108864, 7); }
/* float 2^27: P = 8; base block 2^12 */
BLOCK FN(k27_d12)(ELT *buf) { FIRST8(buf, 4096); PASS3(buf, 4096, 64); PASS3(buf, 4096, 512); }
BLOCK FN(k27_d15)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k27_d12)(buf + (size_t)i * 4096); PASS3(buf, 32768, 4096); }
BLOCK FN(k27_d18)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k27_d15)(buf + (size_t)i * 32768); PASS3(buf, 262144, 32768); }
BLOCK FN(k27_d21)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k27_d18)(buf + (size_t)i * 262144); PASS3(buf, 2097152, 262144); }
BLOCK FN(k27_d24)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k27_d21)(buf + (size_t)i * 2097152); PASS3(buf, 16777216, 2097152); }
TOP FN(k27_d27)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k27_d24)(buf + (size_t)i * 16777216); PASS3L(buf, 134217728, 16777216, 8); SWEEP(buf, 134217728, 8); }
/* float 2^28: P = 8; base block 2^7 */
BLOCK FN(k28_d7)(ELT *buf) { FIRST8(buf, 128); PASS1(buf, 128, 64); }
BLOCK FN(k28_d10)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k28_d7)(buf + (size_t)i * 128); PASS3(buf, 1024, 128); }
BLOCK FN(k28_d13)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k28_d10)(buf + (size_t)i * 1024); PASS3(buf, 8192, 1024); }
BLOCK FN(k28_d16)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k28_d13)(buf + (size_t)i * 8192); PASS3(buf, 65536, 8192); }
BLOCK FN(k28_d19)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k28_d16)(buf + (size_t)i * 65536); PASS3(buf, 524288, 65536); }
BLOCK FN(k28_d22)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k28_d19)(buf + (size_t)i * 524288); PASS3(buf, 4194304, 524288); }
BLOCK FN(k28_d25)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k28_d22)(buf + (size_t)i * 4194304); PASS3(buf, 33554432, 4194304); }
TOP FN(k28_d28)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k28_d25)(buf + (size_t)i * 33554432); PASS3L(buf, 268435456, 33554432, 8); SWEEP(buf, 268435456, 8); }
/* float 2^29: P = 8; base block 2^12 */
BLOCK FN(k29_d12)(ELT *buf) { FIRST8(buf, 4096); PASS3(buf, 4096, 64); PASS3(buf, 4096, 512); }
BLOCK FN(k29_d15)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k29_d12)(buf + (size_t)i * 4096); PASS3(buf, 32768, 4096); }
BLOCK FN(k29_d18)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k29_d15)(buf + (size_t)i * 32768); PASS3(buf, 262144, 32768); }
BLOCK FN(k29_d21)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k29_d18)(buf + (size_t)i * 262144); PASS3(buf, 2097152, 262144); }
BLOCK FN(k29_d24)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k29_d21)(buf + (size_t)i * 2097152); PASS3(buf, 16777216, 2097152); }
BLOCK FN(k29_d27)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k29_d24)(buf + (size_t)i * 16777216); PASS3L(buf, 134217728, 16777216, 8); }
TOP FN(k29_d29)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k29_d27)(buf + (size_t)i * 134217728); PASS2(buf, 536870912, 134217728); SWEEP(buf, 536870912, 8); }
/* float 2^30: P = 9; base block 2^6 */
BLOCK FN(k30_d6)(ELT *buf) { FIRST8(buf, 64); }
BLOCK FN(k30_d9)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k30_d6)(buf + (size_t)i * 64); PASS3(buf, 512, 64); }
BLOCK FN(k30_d12)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k30_d9)(buf + (size_t)i * 512); PASS3(buf, 4096, 512); }
BLOCK FN(k30_d15)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k30_d12)(buf + (size_t)i * 4096); PASS3(buf, 32768, 4096); }
BLOCK FN(k30_d18)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k30_d15)(buf + (size_t)i * 32768); PASS3(buf, 262144, 32768); }
BLOCK FN(k30_d21)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k30_d18)(buf + (size_t)i * 262144); PASS3(buf, 2097152, 262144); }
BLOCK FN(k30_d24)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k30_d21)(buf + (size_t)i * 2097152); PASS3(buf, 16777216, 2097152); }
BLOCK FN(k30_d27)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k30_d24)(buf + (size_t)i * 16777216); PASS3(buf, 134217728, 16777216); }
TOP FN(k30_d30)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k30_d27)(buf + (size_t)i * 134217728); PASS3L(buf, 1073741824, 134217728, 9); SWEEP(buf, 1073741824, 9); }
void NAME(ELT *buf, int k)
{
    switch (k) {
    case 3: FN(k3_d3)(buf); break;
    case 4: FN(k4_d4)(buf); break;
    case 5: FN(k5_d5)(buf); break;
    case 6: FN(k6_d6)(buf); break;
    case 7: FN(k7_d7)(buf); break;
    case 8: FN(k8_d8)(buf); break;
    case 9: FN(k9_d9)(buf); break;
    case 10: FN(k10_d10)(buf); break;
    case 11: FN(k11_d11)(buf); break;
    case 12: FN(k12_d12)(buf); break;
    case 13: FN(k13_d13)(buf); break;
    case 14: FN(k14_d14)(buf); break;
    case 15: FN(k15_d15)(buf); break;
    case 16: FN(k16_d16)(buf); break;
    case 17: FN(k17_d17)(buf); break;
    case 18: FN(k18_d18)(buf); break;
    case 19: FN(k19_d19)(buf); break;
    case 20: FN(k20_d20)(buf); break;
    case 21: FN(k21_d21)(buf); break;
    case 22: FN(k22_d22)(buf); break;
    case 23: FN(k23_d23)(buf); break;
    case 24: FN(k24_d24)(buf); break;
    case 25: FN(k25_d25)(buf); break;
    case 26: FN(k26_d26)(buf); break;
    case 27: FN(k27_d27)(buf); break;
    case 28: FN(k28_d28)(buf); break;
    case 29: FN(k29_d29)(buf); break;
    case 30: FN(k30_d30)(buf); break;
    default: break;
    }
}
#endif
#ifdef PLAN_P_FLOAT
/* P for 2^0 .. 2^30 floats: the number of 8-register passes */
static const signed char plan_P_float[31] = {-1, -1, -1, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 2, 3, 3, 4, 4, 5, 5, 5, 6, 5, 6, 7, 7, 7, 8, 8, 8, 9};
#endif
#ifdef PLAN_DOUBLE
/* double 2^3: P = 0; base block 2^3 */
TOP FN(k3_d3)(ELT *buf) { FIRST2(buf, 8); }
/* double 2^4: P = 0; base block 2^4 */
TOP FN(k4_d4)(ELT *buf) { FIRST4(buf, 16); }
/* double 2^5: P = 1; base block 2^5 */
TOP FN(k5_d5)(ELT *buf) { FIRST8L(buf, 32, 1); SWEEP(buf, 32, 1); }
/* double 2^6: P = 1; base block 2^6 */
TOP FN(k6_d6)(ELT *buf) { FIRST8L(buf, 64, 1); PASS1(buf, 64, 32); SWEEP(buf, 64, 1); }
/* double 2^7: P = 1; base block 2^7 */
TOP FN(k7_d7)(ELT *buf) { FIRST8L(buf, 128, 1); PASS2(buf, 128, 32); SWEEP(buf, 128, 1); }
/* double 2^8: P = 2; base block 2^8 */
TOP FN(k8_d8)(ELT *buf) { FIRST8(buf, 256); PASS3L(buf, 256, 32, 2); SWEEP(buf, 256, 2); }
/* double 2^9: P = 2; base block 2^9 */
TOP FN(k9_d9)(ELT *buf) { FIRST8(buf, 512); PASS3L(buf, 512, 32, 2); PASS1(buf, 512, 256); SWEEP(buf, 512, 2); }
/* double 2^10: P = 2; base block 2^10 */
TOP FN(k10_d10)(ELT *buf) { FIRST8(buf, 1024); PASS3L(buf, 1024, 32, 2); PASS2(buf, 1024, 256); SWEEP(buf, 1024, 2); }
/* double 2^11: P = 3; base block 2^11 */
TOP FN(k11_d11)(ELT *buf) { FIRST8(buf, 2048); PASS3(buf, 2048, 32); PASS3L(buf, 2048, 256, 3); SWEEP(buf, 2048, 3); }
/* double 2^12: P = 3; base block 2^11 */
BLOCK FN(k12_d11)(ELT *buf) { FIRST8(buf, 2048); PASS3(buf, 2048, 32); PASS3L(buf, 2048, 256, 3); }
TOP FN(k12_d12)(ELT *buf) { for (int i = 0; i < 2; i++) FN(k12_d11)(buf + (size_t)i * 2048); PASS1(buf, 4096, 2048); SWEEP(buf, 4096, 3); }
/* double 2^13: P = 3; base block 2^11 */
BLOCK FN(k13_d11)(ELT *buf) { FIRST8(buf, 2048); PASS3(buf, 2048, 32); PASS3L(buf, 2048, 256, 3); }
TOP FN(k13_d13)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k13_d11)(buf + (size_t)i * 2048); PASS2(buf, 8192, 2048); SWEEP(buf, 8192, 3); }
/* double 2^14: P = 3; base block 2^12 */
BLOCK FN(k14_d12)(ELT *buf) { FIRST8(buf, 4096); PASS3(buf, 4096, 32); PASS3L(buf, 4096, 256, 3); PASS1(buf, 4096, 2048); }
TOP FN(k14_d14)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k14_d12)(buf + (size_t)i * 4096); PASS2(buf, 16384, 4096); SWEEP(buf, 16384, 3); }
/* double 2^15: P = 4; base block 2^12 */
BLOCK FN(k15_d12)(ELT *buf) { FIRST8(buf, 4096); PASS3(buf, 4096, 32); PASS3(buf, 4096, 256); PASS1(buf, 4096, 2048); }
TOP FN(k15_d15)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k15_d12)(buf + (size_t)i * 4096); PASS3L(buf, 32768, 4096, 4); SWEEP(buf, 32768, 4); }
/* double 2^16: P = 4; base block 2^11 */
BLOCK FN(k16_d11)(ELT *buf) { FIRST8(buf, 2048); PASS3(buf, 2048, 32); PASS3(buf, 2048, 256); }
BLOCK FN(k16_d14)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k16_d11)(buf + (size_t)i * 2048); PASS3L(buf, 16384, 2048, 4); }
TOP FN(k16_d16)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k16_d14)(buf + (size_t)i * 16384); PASS2(buf, 65536, 16384); SWEEP(buf, 65536, 4); }
/* double 2^17: P = 5; base block 2^11 */
BLOCK FN(k17_d11)(ELT *buf) { FIRST8(buf, 2048); PASS3(buf, 2048, 32); PASS3(buf, 2048, 256); }
BLOCK FN(k17_d14)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k17_d11)(buf + (size_t)i * 2048); PASS3(buf, 16384, 2048); }
TOP FN(k17_d17)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k17_d14)(buf + (size_t)i * 16384); PASS3L(buf, 131072, 16384, 5); SWEEP(buf, 131072, 5); }
/* double 2^18: P = 5; base block 2^12 */
BLOCK FN(k18_d12)(ELT *buf) { FIRST8(buf, 4096); PASS3(buf, 4096, 32); PASS3(buf, 4096, 256); PASS1(buf, 4096, 2048); }
BLOCK FN(k18_d15)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k18_d12)(buf + (size_t)i * 4096); PASS3(buf, 32768, 4096); }
TOP FN(k18_d18)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k18_d15)(buf + (size_t)i * 32768); PASS3L(buf, 262144, 32768, 5); SWEEP(buf, 262144, 5); }
/* double 2^19: P = 5; base block 2^11 */
BLOCK FN(k19_d11)(ELT *buf) { FIRST8(buf, 2048); PASS3(buf, 2048, 32); PASS3(buf, 2048, 256); }
BLOCK FN(k19_d14)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k19_d11)(buf + (size_t)i * 2048); PASS3(buf, 16384, 2048); }
BLOCK FN(k19_d17)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k19_d14)(buf + (size_t)i * 16384); PASS3L(buf, 131072, 16384, 5); }
TOP FN(k19_d19)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k19_d17)(buf + (size_t)i * 131072); PASS2(buf, 524288, 131072); SWEEP(buf, 524288, 5); }
/* double 2^20: P = 5; base block 2^9 */
BLOCK FN(k20_d9)(ELT *buf) { FIRST8(buf, 512); PASS3(buf, 512, 32); PASS1(buf, 512, 256); }
BLOCK FN(k20_d12)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k20_d9)(buf + (size_t)i * 512); PASS3(buf, 4096, 512); }
BLOCK FN(k20_d15)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k20_d12)(buf + (size_t)i * 4096); PASS3(buf, 32768, 4096); }
BLOCK FN(k20_d18)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k20_d15)(buf + (size_t)i * 32768); PASS3L(buf, 262144, 32768, 5); }
TOP FN(k20_d20)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k20_d18)(buf + (size_t)i * 262144); PASS2(buf, 1048576, 262144); SWEEP(buf, 1048576, 5); }
/* double 2^21: P = 5; base block 2^7 */
BLOCK FN(k21_d7)(ELT *buf) { FIRST8(buf, 128); PASS2(buf, 128, 32); }
BLOCK FN(k21_d10)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k21_d7)(buf + (size_t)i * 128); PASS3(buf, 1024, 128); }
BLOCK FN(k21_d13)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k21_d10)(buf + (size_t)i * 1024); PASS3(buf, 8192, 1024); }
BLOCK FN(k21_d16)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k21_d13)(buf + (size_t)i * 8192); PASS3(buf, 65536, 8192); }
BLOCK FN(k21_d19)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k21_d16)(buf + (size_t)i * 65536); PASS3L(buf, 524288, 65536, 5); }
TOP FN(k21_d21)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k21_d19)(buf + (size_t)i * 524288); PASS2(buf, 2097152, 524288); SWEEP(buf, 2097152, 5); }
/* double 2^22: P = 6; base block 2^11 */
BLOCK FN(k22_d11)(ELT *buf) { FIRST8(buf, 2048); PASS3(buf, 2048, 32); PASS3(buf, 2048, 256); }
BLOCK FN(k22_d14)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k22_d11)(buf + (size_t)i * 2048); PASS3(buf, 16384, 2048); }
BLOCK FN(k22_d17)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k22_d14)(buf + (size_t)i * 16384); PASS3(buf, 131072, 16384); }
BLOCK FN(k22_d20)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k22_d17)(buf + (size_t)i * 131072); PASS3L(buf, 1048576, 131072, 6); }
TOP FN(k22_d22)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k22_d20)(buf + (size_t)i * 1048576); PASS2(buf, 4194304, 1048576); SWEEP(buf, 4194304, 6); }
/* double 2^23: P = 7; base block 2^11 */
BLOCK FN(k23_d11)(ELT *buf) { FIRST8(buf, 2048); PASS3(buf, 2048, 32); PASS3(buf, 2048, 256); }
BLOCK FN(k23_d14)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k23_d11)(buf + (size_t)i * 2048); PASS3(buf, 16384, 2048); }
BLOCK FN(k23_d17)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k23_d14)(buf + (size_t)i * 16384); PASS3(buf, 131072, 16384); }
BLOCK FN(k23_d20)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k23_d17)(buf + (size_t)i * 131072); PASS3(buf, 1048576, 131072); }
TOP FN(k23_d23)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k23_d20)(buf + (size_t)i * 1048576); PASS3L(buf, 8388608, 1048576, 7); SWEEP(buf, 8388608, 7); }
/* double 2^24: P = 6; base block 2^10 */
BLOCK FN(k24_d10)(ELT *buf) { FIRST8(buf, 1024); PASS3(buf, 1024, 32); PASS2(buf, 1024, 256); }
BLOCK FN(k24_d13)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k24_d10)(buf + (size_t)i * 1024); PASS3(buf, 8192, 1024); }
BLOCK FN(k24_d16)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k24_d13)(buf + (size_t)i * 8192); PASS3(buf, 65536, 8192); }
BLOCK FN(k24_d19)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k24_d16)(buf + (size_t)i * 65536); PASS3(buf, 524288, 65536); }
BLOCK FN(k24_d22)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k24_d19)(buf + (size_t)i * 524288); PASS3L(buf, 4194304, 524288, 6); }
TOP FN(k24_d24)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k24_d22)(buf + (size_t)i * 4194304); PASS2(buf, 16777216, 4194304); SWEEP(buf, 16777216, 6); }
/* double 2^25: P = 7; base block 2^8 */
BLOCK FN(k25_d8)(ELT *buf) { FIRST8(buf, 256); PASS3(buf, 256, 32); }
BLOCK FN(k25_d11)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k25_d8)(buf + (size_t)i * 256); PASS3(buf, 2048, 256); }
BLOCK FN(k25_d14)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k25_d11)(buf + (size_t)i * 2048); PASS3(buf, 16384, 2048); }
BLOCK FN(k25_d17)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k25_d14)(buf + (size_t)i * 16384); PASS3(buf, 131072, 16384); }
BLOCK FN(k25_d20)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k25_d17)(buf + (size_t)i * 131072); PASS3(buf, 1048576, 131072); }
BLOCK FN(k25_d23)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k25_d20)(buf + (size_t)i * 1048576); PASS3L(buf, 8388608, 1048576, 7); }
TOP FN(k25_d25)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k25_d23)(buf + (size_t)i * 8388608); PASS2(buf, 33554432, 8388608); SWEEP(buf, 33554432, 7); }
/* double 2^26: P = 8; base block 2^11 */
BLOCK FN(k26_d11)(ELT *buf) { FIRST8(buf, 2048); PASS3(buf, 2048, 32); PASS3(buf, 2048, 256); }
BLOCK FN(k26_d14)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k26_d11)(buf + (size_t)i * 2048); PASS3(buf, 16384, 2048); }
BLOCK FN(k26_d17)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k26_d14)(buf + (size_t)i * 16384); PASS3(buf, 131072, 16384); }
BLOCK FN(k26_d20)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k26_d17)(buf + (size_t)i * 131072); PASS3(buf, 1048576, 131072); }
BLOCK FN(k26_d23)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k26_d20)(buf + (size_t)i * 1048576); PASS3(buf, 8388608, 1048576); }
TOP FN(k26_d26)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k26_d23)(buf + (size_t)i * 8388608); PASS3L(buf, 67108864, 8388608, 8); SWEEP(buf, 67108864, 8); }
/* double 2^27: P = 8; base block 2^9 */
BLOCK FN(k27_d9)(ELT *buf) { FIRST8(buf, 512); PASS3(buf, 512, 32); PASS1(buf, 512, 256); }
BLOCK FN(k27_d12)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k27_d9)(buf + (size_t)i * 512); PASS3(buf, 4096, 512); }
BLOCK FN(k27_d15)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k27_d12)(buf + (size_t)i * 4096); PASS3(buf, 32768, 4096); }
BLOCK FN(k27_d18)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k27_d15)(buf + (size_t)i * 32768); PASS3(buf, 262144, 32768); }
BLOCK FN(k27_d21)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k27_d18)(buf + (size_t)i * 262144); PASS3(buf, 2097152, 262144); }
BLOCK FN(k27_d24)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k27_d21)(buf + (size_t)i * 2097152); PASS3(buf, 16777216, 2097152); }
TOP FN(k27_d27)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k27_d24)(buf + (size_t)i * 16777216); PASS3L(buf, 134217728, 16777216, 8); SWEEP(buf, 134217728, 8); }
/* double 2^28: P = 8; base block 2^11 */
BLOCK FN(k28_d11)(ELT *buf) { FIRST8(buf, 2048); PASS3(buf, 2048, 32); PASS3(buf, 2048, 256); }
BLOCK FN(k28_d14)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k28_d11)(buf + (size_t)i * 2048); PASS3(buf, 16384, 2048); }
BLOCK FN(k28_d17)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k28_d14)(buf + (size_t)i * 16384); PASS3(buf, 131072, 16384); }
BLOCK FN(k28_d20)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k28_d17)(buf + (size_t)i * 131072); PASS3(buf, 1048576, 131072); }
BLOCK FN(k28_d23)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k28_d20)(buf + (size_t)i * 1048576); PASS3(buf, 8388608, 1048576); }
BLOCK FN(k28_d26)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k28_d23)(buf + (size_t)i * 8388608); PASS3L(buf, 67108864, 8388608, 8); }
TOP FN(k28_d28)(ELT *buf) { for (int i = 0; i < 4; i++) FN(k28_d26)(buf + (size_t)i * 67108864); PASS2(buf, 268435456, 67108864); SWEEP(buf, 268435456, 8); }
/* double 2^29: P = 9; base block 2^11 */
BLOCK FN(k29_d11)(ELT *buf) { FIRST8(buf, 2048); PASS3(buf, 2048, 32); PASS3(buf, 2048, 256); }
BLOCK FN(k29_d14)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k29_d11)(buf + (size_t)i * 2048); PASS3(buf, 16384, 2048); }
BLOCK FN(k29_d17)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k29_d14)(buf + (size_t)i * 16384); PASS3(buf, 131072, 16384); }
BLOCK FN(k29_d20)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k29_d17)(buf + (size_t)i * 131072); PASS3(buf, 1048576, 131072); }
BLOCK FN(k29_d23)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k29_d20)(buf + (size_t)i * 1048576); PASS3(buf, 8388608, 1048576); }
BLOCK FN(k29_d26)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k29_d23)(buf + (size_t)i * 8388608); PASS3(buf, 67108864, 8388608); }
TOP FN(k29_d29)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k29_d26)(buf + (size_t)i * 67108864); PASS3L(buf, 536870912, 67108864, 9); SWEEP(buf, 536870912, 9); }
/* double 2^30: P = 9; base block 2^9 */
BLOCK FN(k30_d9)(ELT *buf) { FIRST8(buf, 512); PASS3(buf, 512, 32); PASS1(buf, 512, 256); }
BLOCK FN(k30_d12)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k30_d9)(buf + (size_t)i * 512); PASS3(buf, 4096, 512); }
BLOCK FN(k30_d15)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k30_d12)(buf + (size_t)i * 4096); PASS3(buf, 32768, 4096); }
BLOCK FN(k30_d18)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k30_d15)(buf + (size_t)i * 32768); PASS3(buf, 262144, 32768); }
BLOCK FN(k30_d21)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k30_d18)(buf + (size_t)i * 262144); PASS3(buf, 2097152, 262144); }
BLOCK FN(k30_d24)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k30_d21)(buf + (size_t)i * 2097152); PASS3(buf, 16777216, 2097152); }
BLOCK FN(k30_d27)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k30_d24)(buf + (size_t)i * 16777216); PASS3(buf, 134217728, 16777216); }
TOP FN(k30_d30)(ELT *buf) { for (int i = 0; i < 8; i++) FN(k30_d27)(buf + (size_t)i * 134217728); PASS3L(buf, 1073741824, 134217728, 9); SWEEP(buf, 1073741824, 9); }
void NAME(ELT *buf, int k)
{
    switch (k) {
    case 3: FN(k3_d3)(buf); break;
    case 4: FN(k4_d4)(buf); break;
    case 5: FN(k5_d5)(buf); break;
    case 6: FN(k6_d6)(buf); break;
    case 7: FN(k7_d7)(buf); break;
    case 8: FN(k8_d8)(buf); break;
    case 9: FN(k9_d9)(buf); break;
    case 10: FN(k10_d10)(buf); break;
    case 11: FN(k11_d11)(buf); break;
    case 12: FN(k12_d12)(buf); break;
    case 13: FN(k13_d13)(buf); break;
    case 14: FN(k14_d14)(buf); break;
    case 15: FN(k15_d15)(buf); break;
    case 16: FN(k16_d16)(buf); break;
    case 17: FN(k17_d17)(buf); break;
    case 18: FN(k18_d18)(buf); break;
    case 19: FN(k19_d19)(buf); break;
    case 20: FN(k20_d20)(buf); break;
    case 21: FN(k21_d21)(buf); break;
    case 22: FN(k22_d22)(buf); break;
    case 23: FN(k23_d23)(buf); break;
    case 24: FN(k24_d24)(buf); break;
    case 25: FN(k25_d25)(buf); break;
    case 26: FN(k26_d26)(buf); break;
    case 27: FN(k27_d27)(buf); break;
    case 28: FN(k28_d28)(buf); break;
    case 29: FN(k29_d29)(buf); break;
    case 30: FN(k30_d30)(buf); break;
    default: break;
    }
}
#endif
#ifdef PLAN_P_DOUBLE
/* P for 2^0 .. 2^30 doubles: the number of 8-register passes */
static const signed char plan_P_double[31] = {-1, -1, -1, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5, 5, 5, 6, 7, 6, 7, 8, 8, 8, 9, 9};
#endif
