// Written by gen_rtl.py.  Do not edit by hand.
// 16-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/programs/generated/O_textbook_16.txt
// The textbook: 4 layers of 8 butterflies.  64 adders.
// Inputs: 16 signed values of 16 bits.  Outputs: 16 signed values of 20 bits.
// Adders 64, depth 4 adder levels, adder bits 1184 (chain bits 1184).
// Variant p2: a register after every second adder level.  Latency 2.
// Register bits: 608 after adders, 0 in delay registers, 2 valid bits.
`default_nettype none
module wht_16_textbook_p2_w16 (
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
    wire signed [16:0] n_t1 = x0 + x1;   // level 1, stage 1
    wire signed [16:0] n_t2 = x0 - x1;   // level 1, stage 1
    wire signed [16:0] n_t3 = x2 + x3;   // level 1, stage 1
    wire signed [16:0] n_t4 = x2 - x3;   // level 1, stage 1
    wire signed [16:0] n_t5 = x4 + x5;   // level 1, stage 1
    wire signed [16:0] n_t6 = x4 - x5;   // level 1, stage 1
    wire signed [16:0] n_t7 = x6 + x7;   // level 1, stage 1
    wire signed [16:0] n_t8 = x6 - x7;   // level 1, stage 1
    wire signed [16:0] n_t9 = x8 + x9;   // level 1, stage 1
    wire signed [16:0] n_t10 = x8 - x9;   // level 1, stage 1
    wire signed [16:0] n_t11 = x10 + x11;   // level 1, stage 1
    wire signed [16:0] n_t12 = x10 - x11;   // level 1, stage 1
    wire signed [16:0] n_t13 = x12 + x13;   // level 1, stage 1
    wire signed [16:0] n_t14 = x12 - x13;   // level 1, stage 1
    wire signed [16:0] n_t15 = x14 + x15;   // level 1, stage 1
    wire signed [16:0] n_t16 = x14 - x15;   // level 1, stage 1
    wire signed [17:0] n_t17 = n_t1 + n_t3;   // level 2, stage 1
    reg  signed [17:0] n_t17_r1;
    wire signed [17:0] n_t18 = n_t1 - n_t3;   // level 2, stage 1
    reg  signed [17:0] n_t18_r1;
    wire signed [17:0] n_t19 = n_t2 + n_t4;   // level 2, stage 1
    reg  signed [17:0] n_t19_r1;
    wire signed [17:0] n_t20 = n_t2 - n_t4;   // level 2, stage 1
    reg  signed [17:0] n_t20_r1;
    wire signed [17:0] n_t21 = n_t5 + n_t7;   // level 2, stage 1
    reg  signed [17:0] n_t21_r1;
    wire signed [17:0] n_t22 = n_t5 - n_t7;   // level 2, stage 1
    reg  signed [17:0] n_t22_r1;
    wire signed [17:0] n_t23 = n_t6 + n_t8;   // level 2, stage 1
    reg  signed [17:0] n_t23_r1;
    wire signed [17:0] n_t24 = n_t6 - n_t8;   // level 2, stage 1
    reg  signed [17:0] n_t24_r1;
    wire signed [17:0] n_t25 = n_t9 + n_t11;   // level 2, stage 1
    reg  signed [17:0] n_t25_r1;
    wire signed [17:0] n_t26 = n_t9 - n_t11;   // level 2, stage 1
    reg  signed [17:0] n_t26_r1;
    wire signed [17:0] n_t27 = n_t10 + n_t12;   // level 2, stage 1
    reg  signed [17:0] n_t27_r1;
    wire signed [17:0] n_t28 = n_t10 - n_t12;   // level 2, stage 1
    reg  signed [17:0] n_t28_r1;
    wire signed [17:0] n_t29 = n_t13 + n_t15;   // level 2, stage 1
    reg  signed [17:0] n_t29_r1;
    wire signed [17:0] n_t30 = n_t13 - n_t15;   // level 2, stage 1
    reg  signed [17:0] n_t30_r1;
    wire signed [17:0] n_t31 = n_t14 + n_t16;   // level 2, stage 1
    reg  signed [17:0] n_t31_r1;
    wire signed [17:0] n_t32 = n_t14 - n_t16;   // level 2, stage 1
    reg  signed [17:0] n_t32_r1;
    wire signed [18:0] n_t33 = n_t17_r1 + n_t21_r1;   // level 3, stage 2
    wire signed [18:0] n_t34 = n_t17_r1 - n_t21_r1;   // level 3, stage 2
    wire signed [18:0] n_t35 = n_t19_r1 + n_t23_r1;   // level 3, stage 2
    wire signed [18:0] n_t36 = n_t19_r1 - n_t23_r1;   // level 3, stage 2
    wire signed [18:0] n_t37 = n_t18_r1 + n_t22_r1;   // level 3, stage 2
    wire signed [18:0] n_t38 = n_t18_r1 - n_t22_r1;   // level 3, stage 2
    wire signed [18:0] n_t39 = n_t20_r1 + n_t24_r1;   // level 3, stage 2
    wire signed [18:0] n_t40 = n_t20_r1 - n_t24_r1;   // level 3, stage 2
    wire signed [18:0] n_t41 = n_t25_r1 + n_t29_r1;   // level 3, stage 2
    wire signed [18:0] n_t42 = n_t25_r1 - n_t29_r1;   // level 3, stage 2
    wire signed [18:0] n_t43 = n_t27_r1 + n_t31_r1;   // level 3, stage 2
    wire signed [18:0] n_t44 = n_t27_r1 - n_t31_r1;   // level 3, stage 2
    wire signed [18:0] n_t45 = n_t26_r1 + n_t30_r1;   // level 3, stage 2
    wire signed [18:0] n_t46 = n_t26_r1 - n_t30_r1;   // level 3, stage 2
    wire signed [18:0] n_t47 = n_t28_r1 + n_t32_r1;   // level 3, stage 2
    wire signed [18:0] n_t48 = n_t28_r1 - n_t32_r1;   // level 3, stage 2
    wire signed [19:0] n_t49 = n_t33 + n_t41;   // level 4, stage 2
    reg  signed [19:0] n_t49_r2;
    wire signed [19:0] n_t50 = n_t33 - n_t41;   // level 4, stage 2
    reg  signed [19:0] n_t50_r2;
    wire signed [19:0] n_t51 = n_t35 + n_t43;   // level 4, stage 2
    reg  signed [19:0] n_t51_r2;
    wire signed [19:0] n_t52 = n_t35 - n_t43;   // level 4, stage 2
    reg  signed [19:0] n_t52_r2;
    wire signed [19:0] n_t53 = n_t37 + n_t45;   // level 4, stage 2
    reg  signed [19:0] n_t53_r2;
    wire signed [19:0] n_t54 = n_t37 - n_t45;   // level 4, stage 2
    reg  signed [19:0] n_t54_r2;
    wire signed [19:0] n_t55 = n_t39 + n_t47;   // level 4, stage 2
    reg  signed [19:0] n_t55_r2;
    wire signed [19:0] n_t56 = n_t39 - n_t47;   // level 4, stage 2
    reg  signed [19:0] n_t56_r2;
    wire signed [19:0] n_t57 = n_t34 + n_t42;   // level 4, stage 2
    reg  signed [19:0] n_t57_r2;
    wire signed [19:0] n_t58 = n_t34 - n_t42;   // level 4, stage 2
    reg  signed [19:0] n_t58_r2;
    wire signed [19:0] n_t59 = n_t36 + n_t44;   // level 4, stage 2
    reg  signed [19:0] n_t59_r2;
    wire signed [19:0] n_t60 = n_t36 - n_t44;   // level 4, stage 2
    reg  signed [19:0] n_t60_r2;
    wire signed [19:0] n_t61 = n_t38 + n_t46;   // level 4, stage 2
    reg  signed [19:0] n_t61_r2;
    wire signed [19:0] n_t62 = n_t38 - n_t46;   // level 4, stage 2
    reg  signed [19:0] n_t62_r2;
    wire signed [19:0] n_t63 = n_t40 + n_t48;   // level 4, stage 2
    reg  signed [19:0] n_t63_r2;
    wire signed [19:0] n_t64 = n_t40 - n_t48;   // level 4, stage 2
    reg  signed [19:0] n_t64_r2;
    wire signed [19:0] o0 = n_t49_r2;
    wire signed [19:0] o1 = n_t51_r2;
    wire signed [19:0] o2 = n_t53_r2;
    wire signed [19:0] o3 = n_t55_r2;
    wire signed [19:0] o4 = n_t57_r2;
    wire signed [19:0] o5 = n_t59_r2;
    wire signed [19:0] o6 = n_t61_r2;
    wire signed [19:0] o7 = n_t63_r2;
    wire signed [19:0] o8 = n_t50_r2;
    wire signed [19:0] o9 = n_t52_r2;
    wire signed [19:0] o10 = n_t54_r2;
    wire signed [19:0] o11 = n_t56_r2;
    wire signed [19:0] o12 = n_t58_r2;
    wire signed [19:0] o13 = n_t60_r2;
    wire signed [19:0] o14 = n_t62_r2;
    wire signed [19:0] o15 = n_t64_r2;
    assign out_data = {
        o15, o14, o13, o12, o11, o10, o9, o8,
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    reg  [1:0] vld = 2'd0;
    always @(posedge clk) begin
        n_t17_r1 <= n_t17;
        n_t18_r1 <= n_t18;
        n_t19_r1 <= n_t19;
        n_t20_r1 <= n_t20;
        n_t21_r1 <= n_t21;
        n_t22_r1 <= n_t22;
        n_t23_r1 <= n_t23;
        n_t24_r1 <= n_t24;
        n_t25_r1 <= n_t25;
        n_t26_r1 <= n_t26;
        n_t27_r1 <= n_t27;
        n_t28_r1 <= n_t28;
        n_t29_r1 <= n_t29;
        n_t30_r1 <= n_t30;
        n_t31_r1 <= n_t31;
        n_t32_r1 <= n_t32;
        n_t49_r2 <= n_t49;
        n_t50_r2 <= n_t50;
        n_t51_r2 <= n_t51;
        n_t52_r2 <= n_t52;
        n_t53_r2 <= n_t53;
        n_t54_r2 <= n_t54;
        n_t55_r2 <= n_t55;
        n_t56_r2 <= n_t56;
        n_t57_r2 <= n_t57;
        n_t58_r2 <= n_t58;
        n_t59_r2 <= n_t59;
        n_t60_r2 <= n_t60;
        n_t61_r2 <= n_t61;
        n_t62_r2 <= n_t62;
        n_t63_r2 <= n_t63;
        n_t64_r2 <= n_t64;
        vld <= {vld[0:0], in_valid};
    end
    assign out_valid = vld[1];
endmodule
`default_nettype wire
