/* kern.h -- the 8-point steps on 8 vector registers, written once for floats and doubles.
 *
 * A step takes 8 registers x0..x7 (row i of the 8-point transform is x_i) and leaves in the same
 * 8 names y_J = c * sum over i of (-1)^popcount(i & J) x_i, natural order.  c is 1 (the
 * transform itself) or 1/2 or a power of two, as said at each step.
 *
 * The includer sets: V (the register type), ADD, SUB, MUL, and for the steps that use them
 *   FMADD(a, b, c)  = a*b + c      (vfmadd)
 *   FMSUB(a, b, c)  = a*b - c      (vfmsub)
 *   FNMADD(a, b, c) = c - a*b      (vfnmadd)
 * and the names of the registers that hold the constants (K_HALF = 0.5, K_C, K_CH, K_TWO).
 *
 * KERNEL_T     textbook: three levels of 4 butterflies.  24 add/sub.                 c = 1
 * KERNEL_N     circuits/h8_half_20ops.txt, line for line, in the order of that file:
 *              19 add/sub and one multiplication by 0.5.                              c = 1/2
 * KERNEL_NF    the same with the halving fused into its two uses (m8 - x7 and m8 - x5 become
 *              g7*0.5 - x7 and g7*0.5 - x5): 17 add/sub and 2 fused multiply-subtracts.
 *              19 instructions.                                                       c = 1/2
 * KERNEL_NM    the 20 lines of KERNEL_N and 8 multiplications of the outputs by K_C.  c = K_C / 2
 * KERNEL_NC    the 20-line circuit with every later line "w +- p" written "w +- K_C * p" as one
 *              fused multiply-add, and the halving replaced by a multiplication by K_CH = K_C / 2:
 *              7 add/sub, 1 multiplication, 12 fused multiply-adds.  20 instructions. c = K_C / 2
 * KERNEL_G     KERNEL_NC with K_C = 2 (K_TWO): the multiplication is by 1 and is left out.  This
 *              is circuits/h8_19gates.txt: 7 add/sub and 12 fused multiply-adds.       c = 1
 *
 * KERNEL_N in other orders of its 20 lines (same values, same result):
 * KERNEL_N2    outputs as early as possible: every output is computed as soon as its operands exist.
 * KERNEL_N3    the two halves of the tree after m8 one after the other (g9 side, then g10 side).
 */
#ifndef STYLE_INTRINSICS_KERN_H
#define STYLE_INTRINSICS_KERN_H

#define KERNEL_T(x0, x1, x2, x3, x4, x5, x6, x7) do { \
    const V a0 = ADD(x0, x1), a1 = SUB(x0, x1), a2 = ADD(x2, x3), a3 = SUB(x2, x3); \
    const V a4 = ADD(x4, x5), a5 = SUB(x4, x5), a6 = ADD(x6, x7), a7 = SUB(x6, x7); \
    const V b0 = ADD(a0, a2), b2 = SUB(a0, a2), b1 = ADD(a1, a3), b3 = SUB(a1, a3); \
    const V b4 = ADD(a4, a6), b6 = SUB(a4, a6), b5 = ADD(a5, a7), b7 = SUB(a5, a7); \
    x0 = ADD(b0, b4); x4 = SUB(b0, b4); x1 = ADD(b1, b5); x5 = SUB(b1, b5); \
    x2 = ADD(b2, b6); x6 = SUB(b2, b6); x3 = ADD(b3, b7); x7 = SUB(b3, b7); \
} while (0)

#define KERNEL_N_HEAD(x0, x1, x2, x3, x4, x5, x6, x7) \
    const V g1 = ADD(x0, x7); \
    const V g2 = ADD(x1, x6); \
    const V g3 = SUB(x2, x5); \
    const V g4 = SUB(x3, x4); \
    const V g5 = SUB(g1, g2); \
    const V g6 = ADD(g3, g4); \
    const V g7 = SUB(g5, g6);

#define KERNEL_N_TAIL(x0, x1, x2, x3, x4, x5, x6, x7) \
    const V g11 = ADD(g9, x6); \
    const V g12 = SUB(g10, x4); \
    const V g13 = ADD(g11, g4); \
    const V g14 = ADD(g10, x3); \
    const V g15 = SUB(g5, g14); \
    const V g16 = ADD(g11, g3); \
    const V g17 = ADD(g12, g2); \
    const V g18 = ADD(g9, x1); \
    const V g19 = ADD(g18, g6); \
    const V g20 = SUB(g1, g12);

#define KERNEL_N(x0, x1, x2, x3, x4, x5, x6, x7) do { \
    KERNEL_N_HEAD(x0, x1, x2, x3, x4, x5, x6, x7) \
    const V m8 = MUL(g7, K_HALF); \
    const V g9 = SUB(m8, x7); \
    const V g10 = SUB(m8, x5); \
    KERNEL_N_TAIL(x0, x1, x2, x3, x4, x5, x6, x7) \
    x0 = g20; x1 = g16; x2 = g18; x3 = g14; x4 = g19; x5 = g15; x6 = g17; x7 = g13; \
} while (0)

#define KERNEL_NF(x0, x1, x2, x3, x4, x5, x6, x7) do { \
    KERNEL_N_HEAD(x0, x1, x2, x3, x4, x5, x6, x7) \
    const V g9 = FMSUB(g7, K_HALF, x7); \
    const V g10 = FMSUB(g7, K_HALF, x5); \
    KERNEL_N_TAIL(x0, x1, x2, x3, x4, x5, x6, x7) \
    x0 = g20; x1 = g16; x2 = g18; x3 = g14; x4 = g19; x5 = g15; x6 = g17; x7 = g13; \
} while (0)

#define KERNEL_NM(x0, x1, x2, x3, x4, x5, x6, x7) do { \
    KERNEL_N_HEAD(x0, x1, x2, x3, x4, x5, x6, x7) \
    const V m8 = MUL(g7, K_HALF); \
    const V g9 = SUB(m8, x7); \
    const V g10 = SUB(m8, x5); \
    KERNEL_N_TAIL(x0, x1, x2, x3, x4, x5, x6, x7) \
    x0 = MUL(g20, K_C); x1 = MUL(g16, K_C); x2 = MUL(g18, K_C); x3 = MUL(g14, K_C); \
    x4 = MUL(g19, K_C); x5 = MUL(g15, K_C); x6 = MUL(g17, K_C); x7 = MUL(g13, K_C); \
} while (0)

/* every g below is K_C times the g of the same name in KERNEL_N */
#define KERNEL_C_TAIL(x0, x1, x2, x3, x4, x5, x6, x7, KC) \
    const V g9 = FNMADD(KC, x7, m8);       /* m8 - C x7  */ \
    const V g10 = FNMADD(KC, x5, m8);      /* m8 - C x5  */ \
    const V g11 = FMADD(KC, x6, g9);       /* g9 + C x6  */ \
    const V g12 = FNMADD(KC, x4, g10);     /* g10 - C x4 */ \
    const V g13 = FMADD(KC, g4, g11);      /* g11 + C g4 */ \
    const V g14 = FMADD(KC, x3, g10);      /* g10 + C x3 */ \
    const V g15 = FMSUB(KC, g5, g14);      /* C g5 - g14 */ \
    const V g16 = FMADD(KC, g3, g11);      /* g11 + C g3 */ \
    const V g17 = FMADD(KC, g2, g12);      /* g12 + C g2 */ \
    const V g18 = FMADD(KC, x1, g9);       /* g9 + C x1  */ \
    const V g19 = FMADD(KC, g6, g18);      /* g18 + C g6 */ \
    const V g20 = FMSUB(KC, g1, g12);      /* C g1 - g12 */ \
    x0 = g20; x1 = g16; x2 = g18; x3 = g14; x4 = g19; x5 = g15; x6 = g17; x7 = g13;

#define KERNEL_NC(x0, x1, x2, x3, x4, x5, x6, x7) do { \
    KERNEL_N_HEAD(x0, x1, x2, x3, x4, x5, x6, x7) \
    const V m8 = MUL(g7, K_CH); \
    KERNEL_C_TAIL(x0, x1, x2, x3, x4, x5, x6, x7, K_C) \
} while (0)

#define KERNEL_G(x0, x1, x2, x3, x4, x5, x6, x7) do { \
    KERNEL_N_HEAD(x0, x1, x2, x3, x4, x5, x6, x7) \
    const V m8 = g7; \
    KERNEL_C_TAIL(x0, x1, x2, x3, x4, x5, x6, x7, K_TWO) \
} while (0)

/* the 20 lines of KERNEL_N, every output as early as its operands allow */
#define KERNEL_N2(x0, x1, x2, x3, x4, x5, x6, x7) do { \
    KERNEL_N_HEAD(x0, x1, x2, x3, x4, x5, x6, x7) \
    const V m8 = MUL(g7, K_HALF); \
    const V g10 = SUB(m8, x5); \
    const V g14 = ADD(g10, x3); \
    const V g15 = SUB(g5, g14); \
    const V g12 = SUB(g10, x4); \
    const V g17 = ADD(g12, g2); \
    const V g20 = SUB(g1, g12); \
    const V g9 = SUB(m8, x7); \
    const V g18 = ADD(g9, x1); \
    const V g19 = ADD(g18, g6); \
    const V g11 = ADD(g9, x6); \
    const V g16 = ADD(g11, g3); \
    const V g13 = ADD(g11, g4); \
    x0 = g20; x1 = g16; x2 = g18; x3 = g14; x4 = g19; x5 = g15; x6 = g17; x7 = g13; \
} while (0)

/* the 20 lines of KERNEL_N, the g9 side first, then the g10 side */
#define KERNEL_N3(x0, x1, x2, x3, x4, x5, x6, x7) do { \
    KERNEL_N_HEAD(x0, x1, x2, x3, x4, x5, x6, x7) \
    const V m8 = MUL(g7, K_HALF); \
    const V g9 = SUB(m8, x7); \
    const V g10 = SUB(m8, x5); \
    const V g11 = ADD(g9, x6); \
    const V g18 = ADD(g9, x1); \
    const V g13 = ADD(g11, g4); \
    const V g16 = ADD(g11, g3); \
    const V g19 = ADD(g18, g6); \
    const V g12 = SUB(g10, x4); \
    const V g14 = ADD(g10, x3); \
    const V g17 = ADD(g12, g2); \
    const V g20 = SUB(g1, g12); \
    const V g15 = SUB(g5, g14); \
    x0 = g20; x1 = g16; x2 = g18; x3 = g14; x4 = g19; x5 = g15; x6 = g17; x7 = g13; \
} while (0)

/* ---- The steps in two halves, for the passes that are staggered by hand (impl.inc, STAGGER). ----
 *
 * FRONT takes the 8 inputs and leaves in the "carried" registers (KT_CARRY, KN_CARRY, ...) what
 * BACK needs; BACK computes the 8 outputs into y0..y7.  A staggered loop does, in one turn, BACK
 * for the registers of the turn before and then FRONT for the registers of this turn.  The
 * operations and their number are those of the whole step; only the order in the program differs.
 *
 * Textbook: FRONT = levels a and b (16 add/sub), 8 values carried; BACK = level c (8 add/sub).
 * N: FRONT = g1..g7 and the halving (7 add/sub + 1 mul), 7 values carried (g1..g6 and m8);
 *    BACK = the 12 lines after the halving.  BACK needs x1, x3, x4, x5, x6, x7 again: it gets
 *    them as arguments (the loop reads them from memory a second time; they are not yet overwritten).
 * NF: FRONT = g1..g7 (7 add/sub), carried g1..g7; BACK = 2 fused multiply-subtracts + 10 add/sub.
 * NC, G: FRONT as N with K_CH for the halving (G: no multiplication); BACK = the 12 fused lines.
 */
#define KT_CARRY V c0, c1, c2, c3, c4, c5, c6, c7;
#define KT_FRONT(x0, x1, x2, x3, x4, x5, x6, x7) do { \
    const V a0 = ADD(x0, x1), a1 = SUB(x0, x1), a2 = ADD(x2, x3), a3 = SUB(x2, x3); \
    const V a4 = ADD(x4, x5), a5 = SUB(x4, x5), a6 = ADD(x6, x7), a7 = SUB(x6, x7); \
    c0 = ADD(a0, a2); c2 = SUB(a0, a2); c1 = ADD(a1, a3); c3 = SUB(a1, a3); \
    c4 = ADD(a4, a6); c6 = SUB(a4, a6); c5 = ADD(a5, a7); c7 = SUB(a5, a7); \
} while (0)
#define KT_BACK(x1, x3, x4, x5, x6, x7, y0, y1, y2, y3, y4, y5, y6, y7) \
    const V y0 = ADD(c0, c4), y4 = SUB(c0, c4), y1 = ADD(c1, c5), y5 = SUB(c1, c5); \
    const V y2 = ADD(c2, c6), y6 = SUB(c2, c6), y3 = ADD(c3, c7), y7 = SUB(c3, c7);
#define KT_BACK_READS 0

#define KN_CARRY V c1, c2, c3, c4, c5, c6, c8;
#define KN_FRONT_(x0, x1, x2, x3, x4, x5, x6, x7, LAST) do { \
    c1 = ADD(x0, x7); c2 = ADD(x1, x6); c3 = SUB(x2, x5); c4 = SUB(x3, x4); \
    c5 = SUB(c1, c2); c6 = ADD(c3, c4); \
    c8 = LAST(SUB(c5, c6)); \
} while (0)
#define KN_HALVE(v) MUL(v, K_HALF)
#define KN_SCALE(v) MUL(v, K_CH)
#define KN_KEEP(v) (v)
#define KN_FRONT(x0, x1, x2, x3, x4, x5, x6, x7) KN_FRONT_(x0, x1, x2, x3, x4, x5, x6, x7, KN_HALVE)
#define KNF_FRONT(x0, x1, x2, x3, x4, x5, x6, x7) KN_FRONT_(x0, x1, x2, x3, x4, x5, x6, x7, KN_KEEP)
#define KNC_FRONT(x0, x1, x2, x3, x4, x5, x6, x7) KN_FRONT_(x0, x1, x2, x3, x4, x5, x6, x7, KN_SCALE)
#define KN_BACK_TAIL(x1, x3, x4, x5, x6, x7, y0, y1, y2, y3, y4, y5, y6, y7) \
    const V g11 = ADD(g9, x6); \
    const V g12 = SUB(g10, x4); \
    const V y7 = ADD(g11, c4); \
    const V y3 = ADD(g10, x3); \
    const V y5 = SUB(c5, y3); \
    const V y1 = ADD(g11, c3); \
    const V y6 = ADD(g12, c2); \
    const V y2 = ADD(g9, x1); \
    const V y4 = ADD(y2, c6); \
    const V y0 = SUB(c1, g12);
#define KN_BACK(x1, x3, x4, x5, x6, x7, y0, y1, y2, y3, y4, y5, y6, y7) \
    const V g9 = SUB(c8, x7); \
    const V g10 = SUB(c8, x5); \
    KN_BACK_TAIL(x1, x3, x4, x5, x6, x7, y0, y1, y2, y3, y4, y5, y6, y7)
#define KNF_BACK(x1, x3, x4, x5, x6, x7, y0, y1, y2, y3, y4, y5, y6, y7) \
    const V g9 = FMSUB(c8, K_HALF, x7); \
    const V g10 = FMSUB(c8, K_HALF, x5); \
    KN_BACK_TAIL(x1, x3, x4, x5, x6, x7, y0, y1, y2, y3, y4, y5, y6, y7)
#define KC_BACK_(x1, x3, x4, x5, x6, x7, y0, y1, y2, y3, y4, y5, y6, y7, KC) \
    const V g9 = FNMADD(KC, x7, c8); \
    const V g10 = FNMADD(KC, x5, c8); \
    const V g11 = FMADD(KC, x6, g9); \
    const V g12 = FNMADD(KC, x4, g10); \
    const V y7 = FMADD(KC, c4, g11); \
    const V y3 = FMADD(KC, x3, g10); \
    const V y5 = FMSUB(KC, c5, y3); \
    const V y1 = FMADD(KC, c3, g11); \
    const V y6 = FMADD(KC, c2, g12); \
    const V y2 = FMADD(KC, x1, g9); \
    const V y4 = FMADD(KC, c6, y2); \
    const V y0 = FMSUB(KC, c1, g12);
#define KNC_BACK(x1, x3, x4, x5, x6, x7, y0, y1, y2, y3, y4, y5, y6, y7) \
    KC_BACK_(x1, x3, x4, x5, x6, x7, y0, y1, y2, y3, y4, y5, y6, y7, K_C)
#define KG_BACK(x1, x3, x4, x5, x6, x7, y0, y1, y2, y3, y4, y5, y6, y7) \
    KC_BACK_(x1, x3, x4, x5, x6, x7, y0, y1, y2, y3, y4, y5, y6, y7, K_TWO)
#define KN_BACK_READS 1

#endif
