/* wht56.c -- the Walsh-Hadamard transform on doubles, in place, four ways.
 *
 *   wht56_textbook_r2   the textbook, one layer (one address bit) per pass
 *   wht56_textbook_r8   the textbook, three layers per pass: 24 additions and subtractions for
 *                       each 8 points of a pass
 *   wht56_k8_raw        the 20-operation circuit, three address bits per pass: 19 additions and
 *                       subtractions and one halving for each 8 points; the result is
 *                       H x / 2^m, m = floor(log2(n) / 3)
 *   wht56_k8            the same, and the result is H x exactly: in the last pass every output
 *                       is multiplied by 2^m as it is stored (n multiplications)
 *
 * n must be a power of two; for any other n the functions return at once and leave x
 * untouched (wht56_valid_length(n) tests a length).  Output j is the sum over i of (-1)^(number of 1-bits common to j
 * and i) * x[i].  The 8-point passes are in kernels.h, which codegen.py writes from the circuit
 * files; nothing of the circuits is typed here.  When log2(n) is not a multiple of 3, the one
 * or two bits left over are done first, by textbook passes.
 *
 * The three programs that work on 8 points at a time are organised the same way, so that a
 * difference in time between them is a difference of the kernels (the radix-2 textbook is
 * organised differently in one respect, which is the point of it: one address bit per pass):
 * the passes with a small stride are done block by block (blocks of 2^12 numbers,
 * 32 kilobytes, or a little less), and the passes with a larger stride go over the whole array.
 */
#include "wht56.h"
#include "kernels.h"

#define WHT56_BLOCK_BITS 12

int wht56_valid_length(size_t n)
{
    return n != 0 && (n & (n - 1)) == 0;
}

/* called only with a power of two */
static int log2_of(size_t n)
{
    int k = 0;
    while (((size_t)1 << k) < n) k++;
    return k;
}

/* one textbook pass: pairs at distance s.  The two smallest strides are written out, so that
 * the compiler sees loops of a known length. */
static void r2_pass(double *x, size_t n, size_t s)
{
    if (s == 1) {
        for (size_t b = 0; b < n; b += 2) {
            const double u = x[b], v = x[b + 1];
            x[b] = u + v;
            x[b + 1] = u - v;
        }
    } else if (s == 2) {
        for (size_t b = 0; b < n; b += 4) {
            const double u0 = x[b], u1 = x[b + 1], v0 = x[b + 2], v1 = x[b + 3];
            x[b] = u0 + v0;
            x[b + 1] = u1 + v1;
            x[b + 2] = u0 - v0;
            x[b + 3] = u1 - v1;
        }
    } else {
        for (size_t b = 0; b < n; b += 2 * s) {
            double *restrict p = x + b;
            double *restrict q = x + b + s;
            for (size_t i = 0; i < s; i++) {
                const double u = p[i], v = q[i];
                p[i] = u + v;
                q[i] = u - v;
            }
        }
    }
}

void wht56_textbook_r2(double *x, size_t n)
{
    if (!wht56_valid_length(n)) return;
    const size_t blk = n < ((size_t)1 << WHT56_BLOCK_BITS) ? n : ((size_t)1 << WHT56_BLOCK_BITS);
    for (size_t off = 0; off < n; off += blk)
        for (size_t s = 1; s < blk; s *= 2)
            r2_pass(x + off, blk, s);
    for (size_t s = blk; s < n; s *= 2)
        r2_pass(x, n, s);
}

/* 8-point passes with strides s0, 8 s0, 64 s0, ... below s1.  kind: 0 = textbook,
 * 1 = the 20-operation circuit.  The pass whose stride is last_s multiplies its outputs by c
 * (pass last_s = 0 for none).  Stride 1 is called with a constant, so that the compiler
 * writes that pass as straight-line code; this is done for every kernel alike. */
#define ROWS(p, s) (p), (p) + (s), (p) + 2 * (s), (p) + 3 * (s), (p) + 4 * (s), (p) + 5 * (s), (p) + 6 * (s), (p) + 7 * (s)

static void passes8(double *x, size_t n, size_t s0, size_t s1, int kind, size_t last_s, double c)
{
    for (size_t s = s0; s < s1; s *= 8) {
        if (kind == 0) {
            if (s == 1)
                for (size_t b = 0; b < n; b += 8) wht56_pass_t8(ROWS(x + b, 1), 1);
            else
                for (size_t b = 0; b < n; b += 8 * s) wht56_pass_t8(ROWS(x + b, s), s);
        } else if (s == last_s) {
            if (s == 1)
                for (size_t b = 0; b < n; b += 8) wht56_pass_o8_scaled(ROWS(x + b, 1), 1, c);
            else
                for (size_t b = 0; b < n; b += 8 * s) wht56_pass_o8_scaled(ROWS(x + b, s), s, c);
        } else {
            if (s == 1)
                for (size_t b = 0; b < n; b += 8) wht56_pass_o8(ROWS(x + b, 1), 1);
            else
                for (size_t b = 0; b < n; b += 8 * s) wht56_pass_o8(ROWS(x + b, s), s);
        }
    }
}

static void run8(double *x, size_t n, int kind, int exact)
{
    if (!wht56_valid_length(n)) return;
    const int k = log2_of(n);
    const int r = k % 3;                       /* bits left over: textbook passes */
    const int m = k / 3;                       /* 8-point passes */
    int bb = r + 3 * ((WHT56_BLOCK_BITS - r) / 3);
    if (bb > k) bb = k;
    const size_t blk = (size_t)1 << bb;
    const size_t lo = (size_t)1 << r;
    const size_t last_s = (kind == 1 && exact && m > 0) ? n / 8 : 0;
    const double c = (double)((size_t)1 << m);
    for (size_t off = 0; off < n; off += blk) {
        for (size_t s = 1; s < lo; s *= 2)
            r2_pass(x + off, blk, s);
        passes8(x + off, blk, lo, blk, kind, last_s, c);
    }
    passes8(x, n, blk, n, kind, last_s, c);
}

void wht56_textbook_r8(double *x, size_t n) { run8(x, n, 0, 0); }
void wht56_k8_raw(double *x, size_t n)      { run8(x, n, 1, 0); }
void wht56_k8(double *x, size_t n)          { run8(x, n, 1, 1); }

double wht56_k8_raw_factor(size_t n)
{
    if (!wht56_valid_length(n)) return 0.0;
    return 1.0 / (double)((size_t)1 << (log2_of(n) / 3));
}
