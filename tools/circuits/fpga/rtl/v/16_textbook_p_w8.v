// Written by gen_rtl.py.  Do not edit by hand.
// 16-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/programs/generated/O_textbook_16.txt
// The textbook: 4 layers of 8 butterflies.  64 adders.
// Inputs: 16 signed values of 8 bits.  Outputs: 16 signed values of 12 bits.
// Adders 64, depth 4 adder levels, adder bits 672 (chain bits 672).
// Variant p: a register after every adder level.  Latency 4.
// Register bits: 672 after adders, 0 in delay registers, 4 valid bits.
`default_nettype none
module wht_16_textbook_p_w8 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [127:0] in_data,
    output wire                 out_valid,
    output wire [191:0] out_data
);
    wire signed [7:0] x0 = in_data[7:0];
    wire signed [7:0] x1 = in_data[15:8];
    wire signed [7:0] x2 = in_data[23:16];
    wire signed [7:0] x3 = in_data[31:24];
    wire signed [7:0] x4 = in_data[39:32];
    wire signed [7:0] x5 = in_data[47:40];
    wire signed [7:0] x6 = in_data[55:48];
    wire signed [7:0] x7 = in_data[63:56];
    wire signed [7:0] x8 = in_data[71:64];
    wire signed [7:0] x9 = in_data[79:72];
    wire signed [7:0] x10 = in_data[87:80];
    wire signed [7:0] x11 = in_data[95:88];
    wire signed [7:0] x12 = in_data[103:96];
    wire signed [7:0] x13 = in_data[111:104];
    wire signed [7:0] x14 = in_data[119:112];
    wire signed [7:0] x15 = in_data[127:120];
    wire signed [8:0] n_t1 = x0 + x1;   // level 1, stage 1
    reg  signed [8:0] n_t1_r1;
    wire signed [8:0] n_t2 = x0 - x1;   // level 1, stage 1
    reg  signed [8:0] n_t2_r1;
    wire signed [8:0] n_t3 = x2 + x3;   // level 1, stage 1
    reg  signed [8:0] n_t3_r1;
    wire signed [8:0] n_t4 = x2 - x3;   // level 1, stage 1
    reg  signed [8:0] n_t4_r1;
    wire signed [8:0] n_t5 = x4 + x5;   // level 1, stage 1
    reg  signed [8:0] n_t5_r1;
    wire signed [8:0] n_t6 = x4 - x5;   // level 1, stage 1
    reg  signed [8:0] n_t6_r1;
    wire signed [8:0] n_t7 = x6 + x7;   // level 1, stage 1
    reg  signed [8:0] n_t7_r1;
    wire signed [8:0] n_t8 = x6 - x7;   // level 1, stage 1
    reg  signed [8:0] n_t8_r1;
    wire signed [8:0] n_t9 = x8 + x9;   // level 1, stage 1
    reg  signed [8:0] n_t9_r1;
    wire signed [8:0] n_t10 = x8 - x9;   // level 1, stage 1
    reg  signed [8:0] n_t10_r1;
    wire signed [8:0] n_t11 = x10 + x11;   // level 1, stage 1
    reg  signed [8:0] n_t11_r1;
    wire signed [8:0] n_t12 = x10 - x11;   // level 1, stage 1
    reg  signed [8:0] n_t12_r1;
    wire signed [8:0] n_t13 = x12 + x13;   // level 1, stage 1
    reg  signed [8:0] n_t13_r1;
    wire signed [8:0] n_t14 = x12 - x13;   // level 1, stage 1
    reg  signed [8:0] n_t14_r1;
    wire signed [8:0] n_t15 = x14 + x15;   // level 1, stage 1
    reg  signed [8:0] n_t15_r1;
    wire signed [8:0] n_t16 = x14 - x15;   // level 1, stage 1
    reg  signed [8:0] n_t16_r1;
    wire signed [9:0] n_t17 = n_t1_r1 + n_t3_r1;   // level 2, stage 2
    reg  signed [9:0] n_t17_r2;
    wire signed [9:0] n_t18 = n_t1_r1 - n_t3_r1;   // level 2, stage 2
    reg  signed [9:0] n_t18_r2;
    wire signed [9:0] n_t19 = n_t2_r1 + n_t4_r1;   // level 2, stage 2
    reg  signed [9:0] n_t19_r2;
    wire signed [9:0] n_t20 = n_t2_r1 - n_t4_r1;   // level 2, stage 2
    reg  signed [9:0] n_t20_r2;
    wire signed [9:0] n_t21 = n_t5_r1 + n_t7_r1;   // level 2, stage 2
    reg  signed [9:0] n_t21_r2;
    wire signed [9:0] n_t22 = n_t5_r1 - n_t7_r1;   // level 2, stage 2
    reg  signed [9:0] n_t22_r2;
    wire signed [9:0] n_t23 = n_t6_r1 + n_t8_r1;   // level 2, stage 2
    reg  signed [9:0] n_t23_r2;
    wire signed [9:0] n_t24 = n_t6_r1 - n_t8_r1;   // level 2, stage 2
    reg  signed [9:0] n_t24_r2;
    wire signed [9:0] n_t25 = n_t9_r1 + n_t11_r1;   // level 2, stage 2
    reg  signed [9:0] n_t25_r2;
    wire signed [9:0] n_t26 = n_t9_r1 - n_t11_r1;   // level 2, stage 2
    reg  signed [9:0] n_t26_r2;
    wire signed [9:0] n_t27 = n_t10_r1 + n_t12_r1;   // level 2, stage 2
    reg  signed [9:0] n_t27_r2;
    wire signed [9:0] n_t28 = n_t10_r1 - n_t12_r1;   // level 2, stage 2
    reg  signed [9:0] n_t28_r2;
    wire signed [9:0] n_t29 = n_t13_r1 + n_t15_r1;   // level 2, stage 2
    reg  signed [9:0] n_t29_r2;
    wire signed [9:0] n_t30 = n_t13_r1 - n_t15_r1;   // level 2, stage 2
    reg  signed [9:0] n_t30_r2;
    wire signed [9:0] n_t31 = n_t14_r1 + n_t16_r1;   // level 2, stage 2
    reg  signed [9:0] n_t31_r2;
    wire signed [9:0] n_t32 = n_t14_r1 - n_t16_r1;   // level 2, stage 2
    reg  signed [9:0] n_t32_r2;
    wire signed [10:0] n_t33 = n_t17_r2 + n_t21_r2;   // level 3, stage 3
    reg  signed [10:0] n_t33_r3;
    wire signed [10:0] n_t34 = n_t17_r2 - n_t21_r2;   // level 3, stage 3
    reg  signed [10:0] n_t34_r3;
    wire signed [10:0] n_t35 = n_t19_r2 + n_t23_r2;   // level 3, stage 3
    reg  signed [10:0] n_t35_r3;
    wire signed [10:0] n_t36 = n_t19_r2 - n_t23_r2;   // level 3, stage 3
    reg  signed [10:0] n_t36_r3;
    wire signed [10:0] n_t37 = n_t18_r2 + n_t22_r2;   // level 3, stage 3
    reg  signed [10:0] n_t37_r3;
    wire signed [10:0] n_t38 = n_t18_r2 - n_t22_r2;   // level 3, stage 3
    reg  signed [10:0] n_t38_r3;
    wire signed [10:0] n_t39 = n_t20_r2 + n_t24_r2;   // level 3, stage 3
    reg  signed [10:0] n_t39_r3;
    wire signed [10:0] n_t40 = n_t20_r2 - n_t24_r2;   // level 3, stage 3
    reg  signed [10:0] n_t40_r3;
    wire signed [10:0] n_t41 = n_t25_r2 + n_t29_r2;   // level 3, stage 3
    reg  signed [10:0] n_t41_r3;
    wire signed [10:0] n_t42 = n_t25_r2 - n_t29_r2;   // level 3, stage 3
    reg  signed [10:0] n_t42_r3;
    wire signed [10:0] n_t43 = n_t27_r2 + n_t31_r2;   // level 3, stage 3
    reg  signed [10:0] n_t43_r3;
    wire signed [10:0] n_t44 = n_t27_r2 - n_t31_r2;   // level 3, stage 3
    reg  signed [10:0] n_t44_r3;
    wire signed [10:0] n_t45 = n_t26_r2 + n_t30_r2;   // level 3, stage 3
    reg  signed [10:0] n_t45_r3;
    wire signed [10:0] n_t46 = n_t26_r2 - n_t30_r2;   // level 3, stage 3
    reg  signed [10:0] n_t46_r3;
    wire signed [10:0] n_t47 = n_t28_r2 + n_t32_r2;   // level 3, stage 3
    reg  signed [10:0] n_t47_r3;
    wire signed [10:0] n_t48 = n_t28_r2 - n_t32_r2;   // level 3, stage 3
    reg  signed [10:0] n_t48_r3;
    wire signed [11:0] n_t49 = n_t33_r3 + n_t41_r3;   // level 4, stage 4
    reg  signed [11:0] n_t49_r4;
    wire signed [11:0] n_t50 = n_t33_r3 - n_t41_r3;   // level 4, stage 4
    reg  signed [11:0] n_t50_r4;
    wire signed [11:0] n_t51 = n_t35_r3 + n_t43_r3;   // level 4, stage 4
    reg  signed [11:0] n_t51_r4;
    wire signed [11:0] n_t52 = n_t35_r3 - n_t43_r3;   // level 4, stage 4
    reg  signed [11:0] n_t52_r4;
    wire signed [11:0] n_t53 = n_t37_r3 + n_t45_r3;   // level 4, stage 4
    reg  signed [11:0] n_t53_r4;
    wire signed [11:0] n_t54 = n_t37_r3 - n_t45_r3;   // level 4, stage 4
    reg  signed [11:0] n_t54_r4;
    wire signed [11:0] n_t55 = n_t39_r3 + n_t47_r3;   // level 4, stage 4
    reg  signed [11:0] n_t55_r4;
    wire signed [11:0] n_t56 = n_t39_r3 - n_t47_r3;   // level 4, stage 4
    reg  signed [11:0] n_t56_r4;
    wire signed [11:0] n_t57 = n_t34_r3 + n_t42_r3;   // level 4, stage 4
    reg  signed [11:0] n_t57_r4;
    wire signed [11:0] n_t58 = n_t34_r3 - n_t42_r3;   // level 4, stage 4
    reg  signed [11:0] n_t58_r4;
    wire signed [11:0] n_t59 = n_t36_r3 + n_t44_r3;   // level 4, stage 4
    reg  signed [11:0] n_t59_r4;
    wire signed [11:0] n_t60 = n_t36_r3 - n_t44_r3;   // level 4, stage 4
    reg  signed [11:0] n_t60_r4;
    wire signed [11:0] n_t61 = n_t38_r3 + n_t46_r3;   // level 4, stage 4
    reg  signed [11:0] n_t61_r4;
    wire signed [11:0] n_t62 = n_t38_r3 - n_t46_r3;   // level 4, stage 4
    reg  signed [11:0] n_t62_r4;
    wire signed [11:0] n_t63 = n_t40_r3 + n_t48_r3;   // level 4, stage 4
    reg  signed [11:0] n_t63_r4;
    wire signed [11:0] n_t64 = n_t40_r3 - n_t48_r3;   // level 4, stage 4
    reg  signed [11:0] n_t64_r4;
    wire signed [11:0] o0 = n_t49_r4;
    wire signed [11:0] o1 = n_t51_r4;
    wire signed [11:0] o2 = n_t53_r4;
    wire signed [11:0] o3 = n_t55_r4;
    wire signed [11:0] o4 = n_t57_r4;
    wire signed [11:0] o5 = n_t59_r4;
    wire signed [11:0] o6 = n_t61_r4;
    wire signed [11:0] o7 = n_t63_r4;
    wire signed [11:0] o8 = n_t50_r4;
    wire signed [11:0] o9 = n_t52_r4;
    wire signed [11:0] o10 = n_t54_r4;
    wire signed [11:0] o11 = n_t56_r4;
    wire signed [11:0] o12 = n_t58_r4;
    wire signed [11:0] o13 = n_t60_r4;
    wire signed [11:0] o14 = n_t62_r4;
    wire signed [11:0] o15 = n_t64_r4;
    assign out_data = {
        o15, o14, o13, o12, o11, o10, o9, o8,
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    reg  [3:0] vld = 4'd0;
    always @(posedge clk) begin
        n_t1_r1 <= n_t1;
        n_t2_r1 <= n_t2;
        n_t3_r1 <= n_t3;
        n_t4_r1 <= n_t4;
        n_t5_r1 <= n_t5;
        n_t6_r1 <= n_t6;
        n_t7_r1 <= n_t7;
        n_t8_r1 <= n_t8;
        n_t9_r1 <= n_t9;
        n_t10_r1 <= n_t10;
        n_t11_r1 <= n_t11;
        n_t12_r1 <= n_t12;
        n_t13_r1 <= n_t13;
        n_t14_r1 <= n_t14;
        n_t15_r1 <= n_t15;
        n_t16_r1 <= n_t16;
        n_t17_r2 <= n_t17;
        n_t18_r2 <= n_t18;
        n_t19_r2 <= n_t19;
        n_t20_r2 <= n_t20;
        n_t21_r2 <= n_t21;
        n_t22_r2 <= n_t22;
        n_t23_r2 <= n_t23;
        n_t24_r2 <= n_t24;
        n_t25_r2 <= n_t25;
        n_t26_r2 <= n_t26;
        n_t27_r2 <= n_t27;
        n_t28_r2 <= n_t28;
        n_t29_r2 <= n_t29;
        n_t30_r2 <= n_t30;
        n_t31_r2 <= n_t31;
        n_t32_r2 <= n_t32;
        n_t33_r3 <= n_t33;
        n_t34_r3 <= n_t34;
        n_t35_r3 <= n_t35;
        n_t36_r3 <= n_t36;
        n_t37_r3 <= n_t37;
        n_t38_r3 <= n_t38;
        n_t39_r3 <= n_t39;
        n_t40_r3 <= n_t40;
        n_t41_r3 <= n_t41;
        n_t42_r3 <= n_t42;
        n_t43_r3 <= n_t43;
        n_t44_r3 <= n_t44;
        n_t45_r3 <= n_t45;
        n_t46_r3 <= n_t46;
        n_t47_r3 <= n_t47;
        n_t48_r3 <= n_t48;
        n_t49_r4 <= n_t49;
        n_t50_r4 <= n_t50;
        n_t51_r4 <= n_t51;
        n_t52_r4 <= n_t52;
        n_t53_r4 <= n_t53;
        n_t54_r4 <= n_t54;
        n_t55_r4 <= n_t55;
        n_t56_r4 <= n_t56;
        n_t57_r4 <= n_t57;
        n_t58_r4 <= n_t58;
        n_t59_r4 <= n_t59;
        n_t60_r4 <= n_t60;
        n_t61_r4 <= n_t61;
        n_t62_r4 <= n_t62;
        n_t63_r4 <= n_t63;
        n_t64_r4 <= n_t64;
        vld <= {vld[2:0], in_valid};
    end
    assign out_valid = vld[3];
endmodule
`default_nettype wire
