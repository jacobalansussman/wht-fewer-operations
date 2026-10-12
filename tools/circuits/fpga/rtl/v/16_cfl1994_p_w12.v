// Written by gen_rtl.py.  Do not edit by hand.
// 16-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/fpga/rtl/circuits/16_cfl1994.txt
// Coppersmith, Feig, Linzer (1994): eight 4-point circuits of 7 in two layers.  56 adders.
// Inputs: 16 signed values of 12 bits.  Outputs: 16 signed values of 16 bits.
// Adders 56, depth 8 adder levels, adder bits 832 (chain bits 808).
// Variant p: a register after every adder level.  Latency 8.
// Register bits: 832 after adders, 1272 in delay registers, 8 valid bits.
`default_nettype none
module wht_16_cfl1994_p_w12 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [191:0] in_data,
    output wire                 out_valid,
    output wire [255:0] out_data
);
    wire signed [11:0] x0 = in_data[11:0];
    wire signed [11:0] x1 = in_data[23:12];
    wire signed [11:0] x2 = in_data[35:24];
    wire signed [11:0] x3 = in_data[47:36];
    wire signed [11:0] x4 = in_data[59:48];
    wire signed [11:0] x5 = in_data[71:60];
    wire signed [11:0] x6 = in_data[83:72];
    wire signed [11:0] x7 = in_data[95:84];
    wire signed [11:0] x8 = in_data[107:96];
    wire signed [11:0] x9 = in_data[119:108];
    wire signed [11:0] x10 = in_data[131:120];
    wire signed [11:0] x11 = in_data[143:132];
    wire signed [11:0] x12 = in_data[155:144];
    wire signed [11:0] x13 = in_data[167:156];
    wire signed [11:0] x14 = in_data[179:168];
    wire signed [11:0] x15 = in_data[191:180];
    reg  signed [11:0] x0_r1;
    reg  signed [11:0] x0_r2;
    reg  signed [11:0] x1_r1;
    reg  signed [11:0] x1_r2;
    reg  signed [11:0] x1_r3;
    reg  signed [11:0] x2_r1;
    reg  signed [11:0] x2_r2;
    reg  signed [11:0] x2_r3;
    reg  signed [11:0] x3_r1;
    reg  signed [11:0] x3_r2;
    reg  signed [11:0] x3_r3;
    reg  signed [11:0] x4_r1;
    reg  signed [11:0] x4_r2;
    reg  signed [11:0] x5_r1;
    reg  signed [11:0] x5_r2;
    reg  signed [11:0] x5_r3;
    reg  signed [11:0] x6_r1;
    reg  signed [11:0] x6_r2;
    reg  signed [11:0] x6_r3;
    reg  signed [11:0] x7_r1;
    reg  signed [11:0] x7_r2;
    reg  signed [11:0] x7_r3;
    reg  signed [11:0] x8_r1;
    reg  signed [11:0] x8_r2;
    reg  signed [11:0] x9_r1;
    reg  signed [11:0] x9_r2;
    reg  signed [11:0] x9_r3;
    reg  signed [11:0] x10_r1;
    reg  signed [11:0] x10_r2;
    reg  signed [11:0] x10_r3;
    reg  signed [11:0] x11_r1;
    reg  signed [11:0] x11_r2;
    reg  signed [11:0] x11_r3;
    reg  signed [11:0] x12_r1;
    reg  signed [11:0] x12_r2;
    reg  signed [11:0] x13_r1;
    reg  signed [11:0] x13_r2;
    reg  signed [11:0] x13_r3;
    reg  signed [11:0] x14_r1;
    reg  signed [11:0] x14_r2;
    reg  signed [11:0] x14_r3;
    reg  signed [11:0] x15_r1;
    reg  signed [11:0] x15_r2;
    reg  signed [11:0] x15_r3;
    wire signed [12:0] n_t1 = x1 + x2;   // level 1, stage 1
    reg  signed [12:0] n_t1_r1;
    wire signed [13:0] n_t2 = n_t1_r1 + x3_r1;   // level 2, stage 2
    reg  signed [13:0] n_t2_r2;
    wire signed [13:0] n_t3 = x0_r2 - n_t2_r2;   // level 3, stage 3
    reg  signed [13:0] n_t3_r3;
    wire signed [13:0] n_t4 = x0_r2 + n_t2_r2;   // level 3, stage 3
    reg  signed [13:0] n_t4_r3;
    reg  signed [13:0] n_t4_r4;
    reg  signed [13:0] n_t4_r5;
    wire signed [13:0] n_t5 = n_t3_r3 + (x2_r3 <<< 1);   // level 4, stage 4
    reg  signed [13:0] n_t5_r4;
    reg  signed [13:0] n_t5_r5;
    reg  signed [13:0] n_t5_r6;
    wire signed [13:0] n_t6 = n_t3_r3 + (x1_r3 <<< 1);   // level 4, stage 4
    reg  signed [13:0] n_t6_r4;
    reg  signed [13:0] n_t6_r5;
    reg  signed [13:0] n_t6_r6;
    wire signed [13:0] n_t7 = n_t3_r3 + (x3_r3 <<< 1);   // level 4, stage 4
    reg  signed [13:0] n_t7_r4;
    reg  signed [13:0] n_t7_r5;
    reg  signed [13:0] n_t7_r6;
    wire signed [12:0] n_t8 = x5 + x6;   // level 1, stage 1
    reg  signed [12:0] n_t8_r1;
    wire signed [13:0] n_t9 = n_t8_r1 + x7_r1;   // level 2, stage 2
    reg  signed [13:0] n_t9_r2;
    wire signed [13:0] n_t10 = x4_r2 - n_t9_r2;   // level 3, stage 3
    reg  signed [13:0] n_t10_r3;
    wire signed [13:0] n_t11 = x4_r2 + n_t9_r2;   // level 3, stage 3
    reg  signed [13:0] n_t11_r3;
    reg  signed [13:0] n_t11_r4;
    reg  signed [13:0] n_t11_r5;
    reg  signed [13:0] n_t11_r6;
    wire signed [13:0] n_t12 = n_t10_r3 + (x6_r3 <<< 1);   // level 4, stage 4
    reg  signed [13:0] n_t12_r4;
    reg  signed [13:0] n_t12_r5;
    reg  signed [13:0] n_t12_r6;
    reg  signed [13:0] n_t12_r7;
    wire signed [13:0] n_t13 = n_t10_r3 + (x5_r3 <<< 1);   // level 4, stage 4
    reg  signed [13:0] n_t13_r4;
    reg  signed [13:0] n_t13_r5;
    reg  signed [13:0] n_t13_r6;
    reg  signed [13:0] n_t13_r7;
    wire signed [13:0] n_t14 = n_t10_r3 + (x7_r3 <<< 1);   // level 4, stage 4
    reg  signed [13:0] n_t14_r4;
    reg  signed [13:0] n_t14_r5;
    reg  signed [13:0] n_t14_r6;
    reg  signed [13:0] n_t14_r7;
    wire signed [12:0] n_t15 = x9 + x10;   // level 1, stage 1
    reg  signed [12:0] n_t15_r1;
    wire signed [13:0] n_t16 = n_t15_r1 + x11_r1;   // level 2, stage 2
    reg  signed [13:0] n_t16_r2;
    wire signed [13:0] n_t17 = x8_r2 - n_t16_r2;   // level 3, stage 3
    reg  signed [13:0] n_t17_r3;
    wire signed [13:0] n_t18 = x8_r2 + n_t16_r2;   // level 3, stage 3
    reg  signed [13:0] n_t18_r3;
    reg  signed [13:0] n_t18_r4;
    reg  signed [13:0] n_t18_r5;
    reg  signed [13:0] n_t18_r6;
    wire signed [13:0] n_t19 = n_t17_r3 + (x10_r3 <<< 1);   // level 4, stage 4
    reg  signed [13:0] n_t19_r4;
    reg  signed [13:0] n_t19_r5;
    reg  signed [13:0] n_t19_r6;
    reg  signed [13:0] n_t19_r7;
    wire signed [13:0] n_t20 = n_t17_r3 + (x9_r3 <<< 1);   // level 4, stage 4
    reg  signed [13:0] n_t20_r4;
    reg  signed [13:0] n_t20_r5;
    reg  signed [13:0] n_t20_r6;
    reg  signed [13:0] n_t20_r7;
    wire signed [13:0] n_t21 = n_t17_r3 + (x11_r3 <<< 1);   // level 4, stage 4
    reg  signed [13:0] n_t21_r4;
    reg  signed [13:0] n_t21_r5;
    reg  signed [13:0] n_t21_r6;
    reg  signed [13:0] n_t21_r7;
    wire signed [12:0] n_t22 = x13 + x14;   // level 1, stage 1
    reg  signed [12:0] n_t22_r1;
    wire signed [13:0] n_t23 = n_t22_r1 + x15_r1;   // level 2, stage 2
    reg  signed [13:0] n_t23_r2;
    wire signed [13:0] n_t24 = x12_r2 - n_t23_r2;   // level 3, stage 3
    reg  signed [13:0] n_t24_r3;
    wire signed [13:0] n_t25 = x12_r2 + n_t23_r2;   // level 3, stage 3
    reg  signed [13:0] n_t25_r3;
    reg  signed [13:0] n_t25_r4;
    reg  signed [13:0] n_t25_r5;
    reg  signed [13:0] n_t25_r6;
    wire signed [13:0] n_t26 = n_t24_r3 + (x14_r3 <<< 1);   // level 4, stage 4
    reg  signed [13:0] n_t26_r4;
    reg  signed [13:0] n_t26_r5;
    reg  signed [13:0] n_t26_r6;
    reg  signed [13:0] n_t26_r7;
    wire signed [13:0] n_t27 = n_t24_r3 + (x13_r3 <<< 1);   // level 4, stage 4
    reg  signed [13:0] n_t27_r4;
    reg  signed [13:0] n_t27_r5;
    reg  signed [13:0] n_t27_r6;
    reg  signed [13:0] n_t27_r7;
    wire signed [13:0] n_t28 = n_t24_r3 + (x15_r3 <<< 1);   // level 4, stage 4
    reg  signed [13:0] n_t28_r4;
    reg  signed [13:0] n_t28_r5;
    reg  signed [13:0] n_t28_r6;
    reg  signed [13:0] n_t28_r7;
    wire signed [14:0] n_t29 = n_t11_r3 + n_t18_r3;   // level 4, stage 4
    reg  signed [14:0] n_t29_r4;
    wire signed [15:0] n_t30 = n_t29_r4 + n_t25_r4;   // level 5, stage 5
    reg  signed [15:0] n_t30_r5;
    wire signed [15:0] n_t31 = n_t4_r5 - n_t30_r5;   // level 6, stage 6
    reg  signed [15:0] n_t31_r6;
    wire signed [15:0] n_t32 = n_t4_r5 + n_t30_r5;   // level 6, stage 6
    reg  signed [15:0] n_t32_r6;
    reg  signed [15:0] n_t32_r7;
    reg  signed [15:0] n_t32_r8;
    wire signed [15:0] n_t33 = n_t31_r6 + (n_t18_r6 <<< 1);   // level 7, stage 7
    reg  signed [15:0] n_t33_r7;
    reg  signed [15:0] n_t33_r8;
    wire signed [15:0] n_t34 = n_t31_r6 + (n_t11_r6 <<< 1);   // level 7, stage 7
    reg  signed [15:0] n_t34_r7;
    reg  signed [15:0] n_t34_r8;
    wire signed [15:0] n_t35 = n_t31_r6 + (n_t25_r6 <<< 1);   // level 7, stage 7
    reg  signed [15:0] n_t35_r7;
    reg  signed [15:0] n_t35_r8;
    wire signed [14:0] n_t36 = n_t12_r4 + n_t19_r4;   // level 5, stage 5
    reg  signed [14:0] n_t36_r5;
    wire signed [15:0] n_t37 = n_t36_r5 + n_t26_r5;   // level 6, stage 6
    reg  signed [15:0] n_t37_r6;
    wire signed [15:0] n_t38 = n_t5_r6 - n_t37_r6;   // level 7, stage 7
    reg  signed [15:0] n_t38_r7;
    wire signed [15:0] n_t39 = n_t5_r6 + n_t37_r6;   // level 7, stage 7
    reg  signed [15:0] n_t39_r7;
    reg  signed [15:0] n_t39_r8;
    wire signed [15:0] n_t40 = n_t38_r7 + (n_t19_r7 <<< 1);   // level 8, stage 8
    reg  signed [15:0] n_t40_r8;
    wire signed [15:0] n_t41 = n_t38_r7 + (n_t12_r7 <<< 1);   // level 8, stage 8
    reg  signed [15:0] n_t41_r8;
    wire signed [15:0] n_t42 = n_t38_r7 + (n_t26_r7 <<< 1);   // level 8, stage 8
    reg  signed [15:0] n_t42_r8;
    wire signed [14:0] n_t43 = n_t13_r4 + n_t20_r4;   // level 5, stage 5
    reg  signed [14:0] n_t43_r5;
    wire signed [15:0] n_t44 = n_t43_r5 + n_t27_r5;   // level 6, stage 6
    reg  signed [15:0] n_t44_r6;
    wire signed [15:0] n_t45 = n_t6_r6 - n_t44_r6;   // level 7, stage 7
    reg  signed [15:0] n_t45_r7;
    wire signed [15:0] n_t46 = n_t6_r6 + n_t44_r6;   // level 7, stage 7
    reg  signed [15:0] n_t46_r7;
    reg  signed [15:0] n_t46_r8;
    wire signed [15:0] n_t47 = n_t45_r7 + (n_t20_r7 <<< 1);   // level 8, stage 8
    reg  signed [15:0] n_t47_r8;
    wire signed [15:0] n_t48 = n_t45_r7 + (n_t13_r7 <<< 1);   // level 8, stage 8
    reg  signed [15:0] n_t48_r8;
    wire signed [15:0] n_t49 = n_t45_r7 + (n_t27_r7 <<< 1);   // level 8, stage 8
    reg  signed [15:0] n_t49_r8;
    wire signed [14:0] n_t50 = n_t14_r4 + n_t21_r4;   // level 5, stage 5
    reg  signed [14:0] n_t50_r5;
    wire signed [15:0] n_t51 = n_t50_r5 + n_t28_r5;   // level 6, stage 6
    reg  signed [15:0] n_t51_r6;
    wire signed [15:0] n_t52 = n_t7_r6 - n_t51_r6;   // level 7, stage 7
    reg  signed [15:0] n_t52_r7;
    wire signed [15:0] n_t53 = n_t7_r6 + n_t51_r6;   // level 7, stage 7
    reg  signed [15:0] n_t53_r7;
    reg  signed [15:0] n_t53_r8;
    wire signed [15:0] n_t54 = n_t52_r7 + (n_t21_r7 <<< 1);   // level 8, stage 8
    reg  signed [15:0] n_t54_r8;
    wire signed [15:0] n_t55 = n_t52_r7 + (n_t14_r7 <<< 1);   // level 8, stage 8
    reg  signed [15:0] n_t55_r8;
    wire signed [15:0] n_t56 = n_t52_r7 + (n_t28_r7 <<< 1);   // level 8, stage 8
    reg  signed [15:0] n_t56_r8;
    wire signed [15:0] o0 = n_t32_r8;
    wire signed [15:0] o1 = n_t39_r8;
    wire signed [15:0] o2 = n_t46_r8;
    wire signed [15:0] o3 = n_t53_r8;
    wire signed [15:0] o4 = n_t33_r8;
    wire signed [15:0] o5 = n_t40_r8;
    wire signed [15:0] o6 = n_t47_r8;
    wire signed [15:0] o7 = n_t54_r8;
    wire signed [15:0] o8 = n_t34_r8;
    wire signed [15:0] o9 = n_t41_r8;
    wire signed [15:0] o10 = n_t48_r8;
    wire signed [15:0] o11 = n_t55_r8;
    wire signed [15:0] o12 = n_t35_r8;
    wire signed [15:0] o13 = n_t42_r8;
    wire signed [15:0] o14 = n_t49_r8;
    wire signed [15:0] o15 = n_t56_r8;
    assign out_data = {
        o15, o14, o13, o12, o11, o10, o9, o8,
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    reg  [7:0] vld = 8'd0;
    always @(posedge clk) begin
        x0_r1 <= x0;
        x0_r2 <= x0_r1;
        x1_r1 <= x1;
        x1_r2 <= x1_r1;
        x1_r3 <= x1_r2;
        x2_r1 <= x2;
        x2_r2 <= x2_r1;
        x2_r3 <= x2_r2;
        x3_r1 <= x3;
        x3_r2 <= x3_r1;
        x3_r3 <= x3_r2;
        x4_r1 <= x4;
        x4_r2 <= x4_r1;
        x5_r1 <= x5;
        x5_r2 <= x5_r1;
        x5_r3 <= x5_r2;
        x6_r1 <= x6;
        x6_r2 <= x6_r1;
        x6_r3 <= x6_r2;
        x7_r1 <= x7;
        x7_r2 <= x7_r1;
        x7_r3 <= x7_r2;
        x8_r1 <= x8;
        x8_r2 <= x8_r1;
        x9_r1 <= x9;
        x9_r2 <= x9_r1;
        x9_r3 <= x9_r2;
        x10_r1 <= x10;
        x10_r2 <= x10_r1;
        x10_r3 <= x10_r2;
        x11_r1 <= x11;
        x11_r2 <= x11_r1;
        x11_r3 <= x11_r2;
        x12_r1 <= x12;
        x12_r2 <= x12_r1;
        x13_r1 <= x13;
        x13_r2 <= x13_r1;
        x13_r3 <= x13_r2;
        x14_r1 <= x14;
        x14_r2 <= x14_r1;
        x14_r3 <= x14_r2;
        x15_r1 <= x15;
        x15_r2 <= x15_r1;
        x15_r3 <= x15_r2;
        n_t1_r1 <= n_t1;
        n_t2_r2 <= n_t2;
        n_t3_r3 <= n_t3;
        n_t4_r3 <= n_t4;
        n_t4_r4 <= n_t4_r3;
        n_t4_r5 <= n_t4_r4;
        n_t5_r4 <= n_t5;
        n_t5_r5 <= n_t5_r4;
        n_t5_r6 <= n_t5_r5;
        n_t6_r4 <= n_t6;
        n_t6_r5 <= n_t6_r4;
        n_t6_r6 <= n_t6_r5;
        n_t7_r4 <= n_t7;
        n_t7_r5 <= n_t7_r4;
        n_t7_r6 <= n_t7_r5;
        n_t8_r1 <= n_t8;
        n_t9_r2 <= n_t9;
        n_t10_r3 <= n_t10;
        n_t11_r3 <= n_t11;
        n_t11_r4 <= n_t11_r3;
        n_t11_r5 <= n_t11_r4;
        n_t11_r6 <= n_t11_r5;
        n_t12_r4 <= n_t12;
        n_t12_r5 <= n_t12_r4;
        n_t12_r6 <= n_t12_r5;
        n_t12_r7 <= n_t12_r6;
        n_t13_r4 <= n_t13;
        n_t13_r5 <= n_t13_r4;
        n_t13_r6 <= n_t13_r5;
        n_t13_r7 <= n_t13_r6;
        n_t14_r4 <= n_t14;
        n_t14_r5 <= n_t14_r4;
        n_t14_r6 <= n_t14_r5;
        n_t14_r7 <= n_t14_r6;
        n_t15_r1 <= n_t15;
        n_t16_r2 <= n_t16;
        n_t17_r3 <= n_t17;
        n_t18_r3 <= n_t18;
        n_t18_r4 <= n_t18_r3;
        n_t18_r5 <= n_t18_r4;
        n_t18_r6 <= n_t18_r5;
        n_t19_r4 <= n_t19;
        n_t19_r5 <= n_t19_r4;
        n_t19_r6 <= n_t19_r5;
        n_t19_r7 <= n_t19_r6;
        n_t20_r4 <= n_t20;
        n_t20_r5 <= n_t20_r4;
        n_t20_r6 <= n_t20_r5;
        n_t20_r7 <= n_t20_r6;
        n_t21_r4 <= n_t21;
        n_t21_r5 <= n_t21_r4;
        n_t21_r6 <= n_t21_r5;
        n_t21_r7 <= n_t21_r6;
        n_t22_r1 <= n_t22;
        n_t23_r2 <= n_t23;
        n_t24_r3 <= n_t24;
        n_t25_r3 <= n_t25;
        n_t25_r4 <= n_t25_r3;
        n_t25_r5 <= n_t25_r4;
        n_t25_r6 <= n_t25_r5;
        n_t26_r4 <= n_t26;
        n_t26_r5 <= n_t26_r4;
        n_t26_r6 <= n_t26_r5;
        n_t26_r7 <= n_t26_r6;
        n_t27_r4 <= n_t27;
        n_t27_r5 <= n_t27_r4;
        n_t27_r6 <= n_t27_r5;
        n_t27_r7 <= n_t27_r6;
        n_t28_r4 <= n_t28;
        n_t28_r5 <= n_t28_r4;
        n_t28_r6 <= n_t28_r5;
        n_t28_r7 <= n_t28_r6;
        n_t29_r4 <= n_t29;
        n_t30_r5 <= n_t30;
        n_t31_r6 <= n_t31;
        n_t32_r6 <= n_t32;
        n_t32_r7 <= n_t32_r6;
        n_t32_r8 <= n_t32_r7;
        n_t33_r7 <= n_t33;
        n_t33_r8 <= n_t33_r7;
        n_t34_r7 <= n_t34;
        n_t34_r8 <= n_t34_r7;
        n_t35_r7 <= n_t35;
        n_t35_r8 <= n_t35_r7;
        n_t36_r5 <= n_t36;
        n_t37_r6 <= n_t37;
        n_t38_r7 <= n_t38;
        n_t39_r7 <= n_t39;
        n_t39_r8 <= n_t39_r7;
        n_t40_r8 <= n_t40;
        n_t41_r8 <= n_t41;
        n_t42_r8 <= n_t42;
        n_t43_r5 <= n_t43;
        n_t44_r6 <= n_t44;
        n_t45_r7 <= n_t45;
        n_t46_r7 <= n_t46;
        n_t46_r8 <= n_t46_r7;
        n_t47_r8 <= n_t47;
        n_t48_r8 <= n_t48;
        n_t49_r8 <= n_t49;
        n_t50_r5 <= n_t50;
        n_t51_r6 <= n_t51;
        n_t52_r7 <= n_t52;
        n_t53_r7 <= n_t53;
        n_t53_r8 <= n_t53_r7;
        n_t54_r8 <= n_t54;
        n_t55_r8 <= n_t55;
        n_t56_r8 <= n_t56;
        vld <= {vld[6:0], in_valid};
    end
    assign out_valid = vld[7];
endmodule
`default_nettype wire
