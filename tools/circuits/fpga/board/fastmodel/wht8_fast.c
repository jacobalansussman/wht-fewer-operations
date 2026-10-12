/* Fast model of the serial lines of the self-test image (board/selftest/selftest_top.v).
 *
 * It computes the same lines as board/expected.py, about 300 times faster, so that lines read from
 * the board hours after the load can be compared.  It is a transliteration of expected.py's run():
 * the same 521-bit shift register, the same extreme-value vectors, the same transform from its
 * definition as three butterfly levels, the same checksum.  check_fast.sh compares its first 121
 * lines with board/expected-first-120s.txt, byte for byte.
 *
 *   wht8_fast SECONDS [FROM]      prints the lines k = FROM .. SECONDS (FROM defaults to 0)
 *
 * The line:  WHT8 k=KKKK n=NNNNNNNN bad=00000000 ctl=CCCCCCCC sum=SSSSSSSS ref=SSSSSSSS
 * k is 16 bits, n, ctl and sum are 32 bits in the design, so they wrap: n wraps after 5,726 s,
 * k after 65,536 s.  The true number of vectors after k seconds is 750,000 * k; this program
 * prints it on standard error at the end.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;

#define PERIOD_VECTORS 2000   /* BURST   */
#define CORNER 256
#define PPS 375

/* SEED of expected.py: the low 521 bits of sha512(text/0) || sha512(text/1); the same constant as
 * in board/selftest/selftest_params.vh (130 hexadecimal digits). */
static const char SEED_HEX[] =
    "2CB7212EF6007CD093A1C251E653D580AA19C1B2FF3081522481449F4ACA63F326CC8D0E7E1E6101ADB0E23D5A014A04"
    "D1DC88CA5ADF1E12D31655F1646D83BB48";

static const u128 ML = (((u128)1) << 96) - 1;

static int seed_bit(int i)            /* bit i of SEED, i = 0 is the least significant */
{
    int nd = (int)strlen(SEED_HEX);
    int d = i / 4;
    if (d >= nd) return 0;
    char c = SEED_HEX[nd - 1 - d];
    int v = (c >= '0' && c <= '9') ? c - '0' : c - 'A' + 10;
    return (v >> (i % 4)) & 1;
}

/* One vector: d is the 96-bit input bus (input i in bits 12i+11..12i, two's complement).
 * Returns the fold of the 120-bit output bus; *diff = 1 if x3 != x4 (the broken copy differs). */
static inline uint32_t vec(u128 d, uint32_t *diff)
{
    uint64_t lo = (uint64_t)d, hi = (uint64_t)(d >> 64);
    /* x_i + 2048, each 0..4095 */
    int32_t a0 = (int32_t)((lo ^ 0x800) & 4095);
    int32_t a1 = (int32_t)(((lo >> 12) ^ 0x800) & 4095);
    int32_t a2 = (int32_t)(((lo >> 24) ^ 0x800) & 4095);
    int32_t a3 = (int32_t)(((lo >> 36) ^ 0x800) & 4095);
    int32_t a4 = (int32_t)(((lo >> 48) ^ 0x800) & 4095);
    int32_t a5 = (int32_t)((((lo >> 60) | (hi << 4)) ^ 0x800) & 4095);
    int32_t a6 = (int32_t)(((hi >> 8) ^ 0x800) & 4095);
    int32_t a7 = (int32_t)(((hi >> 20) ^ 0x800) & 4095);
    int32_t b0 = a0 + a1, b1 = a0 - a1, b2 = a2 + a3, b3 = a2 - a3;
    int32_t b4 = a4 + a5, b5 = a4 - a5, b6 = a6 + a7, b7 = a6 - a7;
    int32_t c0 = b0 + b2, c2 = b0 - b2, c1 = b1 + b3, c3 = b1 - b3;
    int32_t c4 = b4 + b6, c6 = b4 - b6, c5 = b5 + b7, c7 = b5 - b7;
    u128 o = (u128)((uint32_t)(c0 + c4 - 16384) & 32767u)
           | ((u128)((uint32_t)(c1 + c5) & 32767u) << 15)
           | ((u128)((uint32_t)(c2 + c6) & 32767u) << 30)
           | ((u128)((uint32_t)(c3 + c7) & 32767u) << 45)
           | ((u128)((uint32_t)(c0 - c4) & 32767u) << 60)
           | ((u128)((uint32_t)(c1 - c5) & 32767u) << 75)
           | ((u128)((uint32_t)(c2 - c6) & 32767u) << 90)
           | ((u128)((uint32_t)(c3 - c7) & 32767u) << 105);
    *diff = (a3 != a4);
    return (uint32_t)(o ^ (o >> 32) ^ (o >> 64) ^ (o >> 96));
}

int main(int argc, char **argv)
{
    if (argc < 2) {
        fprintf(stderr, "usage: wht8_fast SECONDS [FROM]\n");
        return 2;
    }
    long seconds = atol(argv[1]);
    long from = argc > 2 ? atol(argv[2]) : 0;
    if (seconds < 0 || seconds > 65535 || from < 0) {
        fprintf(stderr, "SECONDS must be 0..65535 (k is 16 bits in the design)\n");
        return 2;
    }

    /* the register as six 96-bit pieces: h[j] = bits 96j+95 .. 96j of the 521-bit state */
    u128 h[6];
    for (int j = 0; j < 6; j++) {
        u128 v = 0;
        for (int b = 0; b < 96; b++) {
            int i = 96 * j + b;
            if (i < 521 && seed_bit(i)) v |= ((u128)1) << b;
        }
        h[j] = v;
    }

    /* the 256 extreme-value vectors: input i is -2048 (0x800) if bit i of the position is 1, else +2047 */
    uint32_t cfold[CORNER], cdiff[CORNER];
    for (int ph = 0; ph < CORNER; ph++) {
        u128 d = 0;
        for (int i = 0; i < 8; i++)
            d |= ((u128)(((ph >> i) & 1) ? 0x800 : 0x7FF)) << (12 * i);
        cfold[ph] = vec(d, &cdiff[ph]);
    }

    uint32_t n = 0, ctl = 0, csum = 0;
    uint64_t total = 0;
    long periods = seconds * (long)PPS;
    if (periods == 0) periods = 1;                 /* SECONDS = 0: the k = 0 line only */
    for (long p = 0; p < periods; p++) {
        for (int ph = 0; ph < PERIOD_VECTORS; ph++) {
            uint32_t f, df;
            if (ph < CORNER) { f = cfold[ph]; df = cdiff[ph]; }
            else             { f = vec(h[0], &df); }
            csum += f ^ n;
            ctl += df;
            n++;
            /* advance the register by 96 bits: new = (state >> 425) ^ (state >> 257), 96 bits */
            u128 nw = (((h[4] >> 41) | (h[5] << 55)) ^ ((h[2] >> 65) | (h[3] << 31))) & ML;
            h[5] = h[4]; h[4] = h[3]; h[3] = h[2]; h[2] = h[1]; h[1] = h[0]; h[0] = nw;
        }
        total += PERIOD_VECTORS;
        if (p == 0 && from == 0)
            printf("WHT8 k=%04X n=%08X bad=%08X ctl=%08X sum=%08X ref=%08X\n", 0u, n, 0u, ctl, csum, csum);
        if ((p + 1) % PPS == 0 && seconds > 0) {
            long k = (p + 1) / PPS;
            if (k >= from)
                printf("WHT8 k=%04X n=%08X bad=%08X ctl=%08X sum=%08X ref=%08X\n",
                       (unsigned)(k & 0xFFFF), n, 0u, ctl, csum, csum);
        }
    }
    fprintf(stderr, "wht8_fast: %ld seconds of board time, %llu vectors in all (750000 per second)\n",
            seconds, (unsigned long long)total);
    return 0;
}
