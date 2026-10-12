/* kern.h -- the two 8-point steps, written once for every number type.
 *
 * A step replaces 8 registers x0..x7 (row i of the 8-point transform is x_i) by y0..y7, where
 * y_J = sum over i of (-1)^popcount(i & J) x_i: the 8-point Walsh-Hadamard transform, natural
 * order, no scaling.
 *
 * KERNEL_T  the textbook: 24 additions and subtractions, three levels of 8.
 * KERNEL_G  the 19-line circuit of h8_19gates.txt (form G): 7 additions and subtractions that
 *           merge the inputs into the centre g7, then 12 lines of the form a + 2b, a - 2b or
 *           2b - a.  How such a line is computed is left to three macros, set by the includer:
 *               PL2(a, b) = a + 2b      MI2(a, b) = a - 2b      RS2(a, b) = 2b - a
 *           fused multiply-add (one instruction), or two additions, or shift and add.
 *
 * ADD, SUB and the register type V are set by the includer too.
 *
 * Values alive in KERNEL_G: right after g7 there are 13 (g7, the six pieces g1..g6 and the six
 * inputs x1, x3, x4, x5, x6, x7); every one of the 12 later lines needs g7 and the 12 other
 * operands are 12 different values, so no order of the lines can have fewer than 13 alive at
 * that point.  With the register holding 2.0 that is 14 of the 16 registers.  From there on
 * every line has an operand that is used for the last time, so the result can take its place.
 */
#ifndef STYLE_FUSED_KERN_H
#define STYLE_FUSED_KERN_H

#define KERNEL_T(x0, x1, x2, x3, x4, x5, x6, x7) do { \
    const V a0 = ADD(x0, x1), a1 = SUB(x0, x1), a2 = ADD(x2, x3), a3 = SUB(x2, x3); \
    const V a4 = ADD(x4, x5), a5 = SUB(x4, x5), a6 = ADD(x6, x7), a7 = SUB(x6, x7); \
    const V b0 = ADD(a0, a2), b2 = SUB(a0, a2), b1 = ADD(a1, a3), b3 = SUB(a1, a3); \
    const V b4 = ADD(a4, a6), b6 = SUB(a4, a6), b5 = ADD(a5, a7), b7 = SUB(a5, a7); \
    x0 = ADD(b0, b4); x4 = SUB(b0, b4); x1 = ADD(b1, b5); x5 = SUB(b1, b5); \
    x2 = ADD(b2, b6); x6 = SUB(b2, b6); x3 = ADD(b3, b7); x7 = SUB(b3, b7); \
} while (0)

#define KERNEL_G(x0, x1, x2, x3, x4, x5, x6, x7) do { \
    const V g1 = ADD(x0, x7), g2 = ADD(x1, x6), g3 = SUB(x2, x5), g4 = SUB(x3, x4); \
    const V g5 = SUB(g1, g2), g6 = ADD(g3, g4); \
    const V g7 = SUB(g5, g6); \
    const V g8 = MI2(g7, x7), g9 = MI2(g7, x5); \
    const V g10 = PL2(g8, x6), g11 = MI2(g9, x4); \
    const V y7 = PL2(g10, g4), y3 = PL2(g9, x3); \
    const V y5 = RS2(y3, g5), y1 = PL2(g10, g3), y6 = PL2(g11, g2), y2 = PL2(g8, x1); \
    const V y4 = PL2(y2, g6), y0 = RS2(g11, g1); \
    x0 = y0; x1 = y1; x2 = y2; x3 = y3; x4 = y4; x5 = y5; x6 = y6; x7 = y7; \
} while (0)

/* KERNEL_TF: the textbook step with every addition written as a fused multiply-add by 1.0
 * (FA(a, b) = a + 1.0 * b, FS(a, b) = a - 1.0 * b).  Same 24 lines, same depth 3, same results bit
 * for bit; only the kind of instruction changes.  A control: on a core where additions have one
 * unit and multiply-adds two, this is the known way to double the additions per cycle. */
#define KERNEL_TF(x0, x1, x2, x3, x4, x5, x6, x7) do { \
    const V a0 = FA(x0, x1), a1 = FS(x0, x1), a2 = FA(x2, x3), a3 = FS(x2, x3); \
    const V a4 = FA(x4, x5), a5 = FS(x4, x5), a6 = FA(x6, x7), a7 = FS(x6, x7); \
    const V b0 = FA(a0, a2), b2 = FS(a0, a2), b1 = FA(a1, a3), b3 = FS(a1, a3); \
    const V b4 = FA(a4, a6), b6 = FS(a4, a6), b5 = FA(a5, a7), b7 = FS(a5, a7); \
    x0 = FA(b0, b4); x4 = FS(b0, b4); x1 = FA(b1, b5); x5 = FS(b1, b5); \
    x2 = FA(b2, b6); x6 = FS(b2, b6); x3 = FA(b3, b7); x7 = FS(b3, b7); \
} while (0)

#endif
