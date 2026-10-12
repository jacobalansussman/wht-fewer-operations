/* whts.c -- the same plan as whtf.c for 32-bit integers, ONE number at a time, so that the compiler
 * can write a line a + 2b as one LEA instruction.
 *
 *   wht_s_T    textbook step, 24 additions and subtractions
 *   wht_s_G19  form G, the 12 lines written as a + 2*b, a - 2*b, 2*b - a in C
 *
 * Build: gcc -O3 -march=native -fno-tree-vectorize -fno-tree-slp-vectorize -fwrapv
 * (no vector code; -fwrapv: the sums wrap like the vector instructions do).
 */
#include <stddef.h>
#include <stdint.h>
#include "kern.h"
#include "whtf.h"

#ifndef BASEMAX_4
#define BASEMAX_4 12
#endif

#define ELT int32_t
#define V int32_t
#define W 1
#define LW 0
#define BASEMAX BASEMAX_4
#define LOAD(p) (*(p))
#define STORE(p, v) (*(p) = (v))
#define ADD(a, b) ((a) + (b))
#define SUB(a, b) ((a) - (b))
#define IDECL
#define INREG(v) (void)0
#define PIN(v)

#define NAME wht_s_T
#define KDECL
#define KERNEL KERNEL_T
#include "impl.inc"
#undef NAME
#undef KERNEL

#define NAME wht_s_G19
#define KERNEL KERNEL_G
#define PL2(a, b) ((a) + 2 * (b))
#define MI2(a, b) ((a) - 2 * (b))
#define RS2(a, b) (2 * (b) - (a))
#include "impl.inc"
