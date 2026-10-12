// Written by gen_rtl.py.  Do not edit by hand.
// 16-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/fpga/rtl/circuits/16_cfl1994.txt
// Coppersmith, Feig, Linzer (1994): eight 4-point circuits of 7 in two layers.  56 adders.
// Inputs: 16 signed values of 16 bits.  Outputs: 16 signed values of 20 bits.
// Adders 56, depth 8 adder levels, adder bits 1056 (chain bits 1032).
// Variant p2: a register after every second adder level.  Latency 4.
// Register bits: 779 after adders, 546 in delay registers, 4 valid bits.
`default_nettype none
module wht_16_cfl1994_p2_w16 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [255:0] in_data,
    output wire                 out_valid,
    output wire [319:0] out_data
);
    wire signed [15:0] x0 = in_data[15:0];
    wire signed [15:0] x1 = in_data[31:16];
    wire signed [15:0] x2 = in_data[47:32];
    wire signed [15:0] x3 = in_data[63:48];
    wire signed [15:0] x4 = in_data[79:64];
    wire signed [15:0] x5 = in_data[95:80];
    wire signed [15:0] x6 = in_data[111:96];
    wire signed [15:0] x7 = in_data[127:112];
    wire signed [15:0] x8 = in_data[143:128];
    wire signed [15:0] x9 = in_data[159:144];
    wire signed [15:0] x10 = in_data[175:160];
    wire signed [15:0] x11 = in_data[191:176];
    wire signed [15:0] x12 = in_data[207:192];
    wire signed [15:0] x13 = in_data[223:208];
    wire signed [15:0] x14 = in_data[239:224];
    wire signed [15:0] x15 = in_data[255:240];
    reg  signed [15:0] x0_r1;
    reg  signed [15:0] x1_r1;
    reg  signed [15:0] x2_r1;
    reg  signed [15:0] x3_r1;
    reg  signed [15:0] x4_r1;
    reg  signed [15:0] x5_r1;
    reg  signed [15:0] x6_r1;
    reg  signed [15:0] x7_r1;
    reg  signed [15:0] x8_r1;
    reg  signed [15:0] x9_r1;
    reg  signed [15:0] x10_r1;
    reg  signed [15:0] x11_r1;
    reg  signed [15:0] x12_r1;
    reg  signed [15:0] x13_r1;
    reg  signed [15:0] x14_r1;
    reg  signed [15:0] x15_r1;
    wire signed [16:0] n_t1 = x1 + x2;   // level 1, stage 1
    wire signed [17:0] n_t2 = n_t1 + x3;   // level 2, stage 1
    reg  signed [17:0] n_t2_r1;
    wire signed [17:0] n_t3 = x0_r1 - n_t2_r1;   // level 3, stage 2
    wire signed [17:0] n_t4 = x0_r1 + n_t2_r1;   // level 3, stage 2
    reg  signed [17:0] n_t4_r2;
    wire signed [17:0] n_t5 = n_t3 + (x2_r1 <<< 1);   // level 4, stage 2
    reg  signed [17:0] n_t5_r2;
    reg  signed [17:0] n_t5_r3;
    wire signed [17:0] n_t6 = n_t3 + (x1_r1 <<< 1);   // level 4, stage 2
    reg  signed [17:0] n_t6_r2;
    reg  signed [17:0] n_t6_r3;
    wire signed [17:0] n_t7 = n_t3 + (x3_r1 <<< 1);   // level 4, stage 2
    reg  signed [17:0] n_t7_r2;
    reg  signed [17:0] n_t7_r3;
    wire signed [16:0] n_t8 = x5 + x6;   // level 1, stage 1
    wire signed [17:0] n_t9 = n_t8 + x7;   // level 2, stage 1
    reg  signed [17:0] n_t9_r1;
    wire signed [17:0] n_t10 = x4_r1 - n_t9_r1;   // level 3, stage 2
    wire signed [17:0] n_t11 = x4_r1 + n_t9_r1;   // level 3, stage 2
    reg  signed [17:0] n_t11_r2;
    reg  signed [17:0] n_t11_r3;
    wire signed [17:0] n_t12 = n_t10 + (x6_r1 <<< 1);   // level 4, stage 2
    reg  signed [17:0] n_t12_r2;
    reg  signed [17:0] n_t12_r3;
    wire signed [17:0] n_t13 = n_t10 + (x5_r1 <<< 1);   // level 4, stage 2
    reg  signed [17:0] n_t13_r2;
    reg  signed [17:0] n_t13_r3;
    wire signed [17:0] n_t14 = n_t10 + (x7_r1 <<< 1);   // level 4, stage 2
    reg  signed [17:0] n_t14_r2;
    reg  signed [17:0] n_t14_r3;
    wire signed [16:0] n_t15 = x9 + x10;   // level 1, stage 1
    wire signed [17:0] n_t16 = n_t15 + x11;   // level 2, stage 1
    reg  signed [17:0] n_t16_r1;
    wire signed [17:0] n_t17 = x8_r1 - n_t16_r1;   // level 3, stage 2
    wire signed [17:0] n_t18 = x8_r1 + n_t16_r1;   // level 3, stage 2
    reg  signed [17:0] n_t18_r2;
    reg  signed [17:0] n_t18_r3;
    wire signed [17:0] n_t19 = n_t17 + (x10_r1 <<< 1);   // level 4, stage 2
    reg  signed [17:0] n_t19_r2;
    reg  signed [17:0] n_t19_r3;
    wire signed [17:0] n_t20 = n_t17 + (x9_r1 <<< 1);   // level 4, stage 2
    reg  signed [17:0] n_t20_r2;
    reg  signed [17:0] n_t20_r3;
    wire signed [17:0] n_t21 = n_t17 + (x11_r1 <<< 1);   // level 4, stage 2
    reg  signed [17:0] n_t21_r2;
    reg  signed [17:0] n_t21_r3;
    wire signed [16:0] n_t22 = x13 + x14;   // level 1, stage 1
    wire signed [17:0] n_t23 = n_t22 + x15;   // level 2, stage 1
    reg  signed [17:0] n_t23_r1;
    wire signed [17:0] n_t24 = x12_r1 - n_t23_r1;   // level 3, stage 2
    wire signed [17:0] n_t25 = x12_r1 + n_t23_r1;   // level 3, stage 2
    reg  signed [17:0] n_t25_r2;
    reg  signed [17:0] n_t25_r3;
    wire signed [17:0] n_t26 = n_t24 + (x14_r1 <<< 1);   // level 4, stage 2
    reg  signed [17:0] n_t26_r2;
    reg  signed [17:0] n_t26_r3;
    wire signed [17:0] n_t27 = n_t24 + (x13_r1 <<< 1);   // level 4, stage 2
    reg  signed [17:0] n_t27_r2;
    reg  signed [17:0] n_t27_r3;
    wire signed [17:0] n_t28 = n_t24 + (x15_r1 <<< 1);   // level 4, stage 2
    reg  signed [17:0] n_t28_r2;
    reg  signed [17:0] n_t28_r3;
    wire signed [18:0] n_t29 = n_t11 + n_t18;   // level 4, stage 2
    reg  signed [18:0] n_t29_r2;
    wire signed [19:0] n_t30 = n_t29_r2 + n_t25_r2;   // level 5, stage 3
    wire signed [19:0] n_t31 = n_t4_r2 - n_t30;   // level 6, stage 3
    reg  signed [19:0] n_t31_r3;
    wire signed [19:0] n_t32 = n_t4_r2 + n_t30;   // level 6, stage 3
    reg  signed [19:0] n_t32_r3;
    reg  signed [19:0] n_t32_r4;
    wire signed [19:0] n_t33 = n_t31_r3 + (n_t18_r3 <<< 1);   // level 7, stage 4
    reg  signed [19:0] n_t33_r4;
    wire signed [19:0] n_t34 = n_t31_r3 + (n_t11_r3 <<< 1);   // level 7, stage 4
    reg  signed [19:0] n_t34_r4;
    wire signed [19:0] n_t35 = n_t31_r3 + (n_t25_r3 <<< 1);   // level 7, stage 4
    reg  signed [19:0] n_t35_r4;
    wire signed [18:0] n_t36 = n_t12_r2 + n_t19_r2;   // level 5, stage 3
    wire signed [19:0] n_t37 = n_t36 + n_t26_r2;   // level 6, stage 3
    reg  signed [19:0] n_t37_r3;
    wire signed [19:0] n_t38 = n_t5_r3 - n_t37_r3;   // level 7, stage 4
    wire signed [19:0] n_t39 = n_t5_r3 + n_t37_r3;   // level 7, stage 4
    reg  signed [19:0] n_t39_r4;
    wire signed [19:0] n_t40 = n_t38 + (n_t19_r3 <<< 1);   // level 8, stage 4
    reg  signed [19:0] n_t40_r4;
    wire signed [19:0] n_t41 = n_t38 + (n_t12_r3 <<< 1);   // level 8, stage 4
    reg  signed [19:0] n_t41_r4;
    wire signed [19:0] n_t42 = n_t38 + (n_t26_r3 <<< 1);   // level 8, stage 4
    reg  signed [19:0] n_t42_r4;
    wire signed [18:0] n_t43 = n_t13_r2 + n_t20_r2;   // level 5, stage 3
    wire signed [19:0] n_t44 = n_t43 + n_t27_r2;   // level 6, stage 3
    reg  signed [19:0] n_t44_r3;
    wire signed [19:0] n_t45 = n_t6_r3 - n_t44_r3;   // level 7, stage 4
    wire signed [19:0] n_t46 = n_t6_r3 + n_t44_r3;   // level 7, stage 4
    reg  signed [19:0] n_t46_r4;
    wire signed [19:0] n_t47 = n_t45 + (n_t20_r3 <<< 1);   // level 8, stage 4
    reg  signed [19:0] n_t47_r4;
    wire signed [19:0] n_t48 = n_t45 + (n_t13_r3 <<< 1);   // level 8, stage 4
    reg  signed [19:0] n_t48_r4;
    wire signed [19:0] n_t49 = n_t45 + (n_t27_r3 <<< 1);   // level 8, stage 4
    reg  signed [19:0] n_t49_r4;
    wire signed [18:0] n_t50 = n_t14_r2 + n_t21_r2;   // level 5, stage 3
    wire signed [19:0] n_t51 = n_t50 + n_t28_r2;   // level 6, stage 3
    reg  signed [19:0] n_t51_r3;
    wire signed [19:0] n_t52 = n_t7_r3 - n_t51_r3;   // level 7, stage 4
    wire signed [19:0] n_t53 = n_t7_r3 + n_t51_r3;   // level 7, stage 4
    reg  signed [19:0] n_t53_r4;
    wire signed [19:0] n_t54 = n_t52 + (n_t21_r3 <<< 1);   // level 8, stage 4
    reg  signed [19:0] n_t54_r4;
    wire signed [19:0] n_t55 = n_t52 + (n_t14_r3 <<< 1);   // level 8, stage 4
    reg  signed [19:0] n_t55_r4;
    wire signed [19:0] n_t56 = n_t52 + (n_t28_r3 <<< 1);   // level 8, stage 4
    reg  signed [19:0] n_t56_r4;
    wire signed [19:0] o0 = n_t32_r4;
    wire signed [19:0] o1 = n_t39_r4;
    wire signed [19:0] o2 = n_t46_r4;
    wire signed [19:0] o3 = n_t53_r4;
    wire signed [19:0] o4 = n_t33_r4;
    wire signed [19:0] o5 = n_t40_r4;
    wire signed [19:0] o6 = n_t47_r4;
    wire signed [19:0] o7 = n_t54_r4;
    wire signed [19:0] o8 = n_t34_r4;
    wire signed [19:0] o9 = n_t41_r4;
    wire signed [19:0] o10 = n_t48_r4;
    wire signed [19:0] o11 = n_t55_r4;
    wire signed [19:0] o12 = n_t35_r4;
    wire signed [19:0] o13 = n_t42_r4;
    wire signed [19:0] o14 = n_t49_r4;
    wire signed [19:0] o15 = n_t56_r4;
    assign out_data = {
        o15, o14, o13, o12, o11, o10, o9, o8,
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    reg  [3:0] vld = 4'd0;
    always @(posedge clk) begin
        x0_r1 <= x0;
        x1_r1 <= x1;
        x2_r1 <= x2;
        x3_r1 <= x3;
        x4_r1 <= x4;
        x5_r1 <= x5;
        x6_r1 <= x6;
        x7_r1 <= x7;
        x8_r1 <= x8;
        x9_r1 <= x9;
        x10_r1 <= x10;
        x11_r1 <= x11;
        x12_r1 <= x12;
        x13_r1 <= x13;
        x14_r1 <= x14;
        x15_r1 <= x15;
        n_t2_r1 <= n_t2;
        n_t4_r2 <= n_t4;
        n_t5_r2 <= n_t5;
        n_t5_r3 <= n_t5_r2;
        n_t6_r2 <= n_t6;
        n_t6_r3 <= n_t6_r2;
        n_t7_r2 <= n_t7;
        n_t7_r3 <= n_t7_r2;
        n_t9_r1 <= n_t9;
        n_t11_r2 <= n_t11;
        n_t11_r3 <= n_t11_r2;
        n_t12_r2 <= n_t12;
        n_t12_r3 <= n_t12_r2;
        n_t13_r2 <= n_t13;
        n_t13_r3 <= n_t13_r2;
        n_t14_r2 <= n_t14;
        n_t14_r3 <= n_t14_r2;
        n_t16_r1 <= n_t16;
        n_t18_r2 <= n_t18;
        n_t18_r3 <= n_t18_r2;
        n_t19_r2 <= n_t19;
        n_t19_r3 <= n_t19_r2;
        n_t20_r2 <= n_t20;
        n_t20_r3 <= n_t20_r2;
        n_t21_r2 <= n_t21;
        n_t21_r3 <= n_t21_r2;
        n_t23_r1 <= n_t23;
        n_t25_r2 <= n_t25;
        n_t25_r3 <= n_t25_r2;
        n_t26_r2 <= n_t26;
        n_t26_r3 <= n_t26_r2;
        n_t27_r2 <= n_t27;
        n_t27_r3 <= n_t27_r2;
        n_t28_r2 <= n_t28;
        n_t28_r3 <= n_t28_r2;
        n_t29_r2 <= n_t29;
        n_t31_r3 <= n_t31;
        n_t32_r3 <= n_t32;
        n_t32_r4 <= n_t32_r3;
        n_t33_r4 <= n_t33;
        n_t34_r4 <= n_t34;
        n_t35_r4 <= n_t35;
        n_t37_r3 <= n_t37;
        n_t39_r4 <= n_t39;
        n_t40_r4 <= n_t40;
        n_t41_r4 <= n_t41;
        n_t42_r4 <= n_t42;
        n_t44_r3 <= n_t44;
        n_t46_r4 <= n_t46;
        n_t47_r4 <= n_t47;
        n_t48_r4 <= n_t48;
        n_t49_r4 <= n_t49;
        n_t51_r3 <= n_t51;
        n_t53_r4 <= n_t53;
        n_t54_r4 <= n_t54;
        n_t55_r4 <= n_t55;
        n_t56_r4 <= n_t56;
        vld <= {vld[2:0], in_valid};
    end
    assign out_valid = vld[3];
endmodule
`default_nettype wire
