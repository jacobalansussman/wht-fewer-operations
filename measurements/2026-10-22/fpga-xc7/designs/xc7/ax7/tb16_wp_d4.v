// Written by gen_ax7.py (wave 16, ax-7).  Do not edit by hand.
// 16-point WHT, word-parallel, registers placed by an integer program (min register bits).
// Source: tools/circuits/programs/generated/O_textbook_16.txt
// adders 64, depth 4; at most 4 adder level(s) per clock; latency 1; register bits 192 (after adders 192, delay 0).
`default_nettype none
module wht_tb16_wp_d4 (
    input  wire clk,
    input  wire in_valid,
    input  wire [127:0] in_data,
    output wire out_valid,
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
    reg signed [11:0] r_t49_b1;
    reg signed [11:0] r_t50_b1;
    reg signed [11:0] r_t51_b1;
    reg signed [11:0] r_t52_b1;
    reg signed [11:0] r_t53_b1;
    reg signed [11:0] r_t54_b1;
    reg signed [11:0] r_t55_b1;
    reg signed [11:0] r_t56_b1;
    reg signed [11:0] r_t57_b1;
    reg signed [11:0] r_t58_b1;
    reg signed [11:0] r_t59_b1;
    reg signed [11:0] r_t60_b1;
    reg signed [11:0] r_t61_b1;
    reg signed [11:0] r_t62_b1;
    reg signed [11:0] r_t63_b1;
    reg signed [11:0] r_t64_b1;
    wire signed [8:0] n_t1 = x0 + x1;   // stage 1 place 1
    wire signed [8:0] n_t2 = x0 - x1;   // stage 1 place 1
    wire signed [8:0] n_t3 = x2 + x3;   // stage 1 place 1
    wire signed [8:0] n_t4 = x2 - x3;   // stage 1 place 1
    wire signed [8:0] n_t5 = x4 + x5;   // stage 1 place 1
    wire signed [8:0] n_t6 = x4 - x5;   // stage 1 place 1
    wire signed [8:0] n_t7 = x6 + x7;   // stage 1 place 1
    wire signed [8:0] n_t8 = x6 - x7;   // stage 1 place 1
    wire signed [8:0] n_t9 = x8 + x9;   // stage 1 place 1
    wire signed [8:0] n_t10 = x8 - x9;   // stage 1 place 1
    wire signed [8:0] n_t11 = x10 + x11;   // stage 1 place 1
    wire signed [8:0] n_t12 = x10 - x11;   // stage 1 place 1
    wire signed [8:0] n_t13 = x12 + x13;   // stage 1 place 1
    wire signed [8:0] n_t14 = x12 - x13;   // stage 1 place 1
    wire signed [8:0] n_t15 = x14 + x15;   // stage 1 place 1
    wire signed [8:0] n_t16 = x14 - x15;   // stage 1 place 1
    wire signed [9:0] n_t17 = n_t1 + n_t3;   // stage 1 place 2
    wire signed [9:0] n_t18 = n_t1 - n_t3;   // stage 1 place 2
    wire signed [9:0] n_t19 = n_t2 + n_t4;   // stage 1 place 2
    wire signed [9:0] n_t20 = n_t2 - n_t4;   // stage 1 place 2
    wire signed [9:0] n_t21 = n_t5 + n_t7;   // stage 1 place 2
    wire signed [9:0] n_t22 = n_t5 - n_t7;   // stage 1 place 2
    wire signed [9:0] n_t23 = n_t6 + n_t8;   // stage 1 place 2
    wire signed [9:0] n_t24 = n_t6 - n_t8;   // stage 1 place 2
    wire signed [9:0] n_t25 = n_t9 + n_t11;   // stage 1 place 2
    wire signed [9:0] n_t26 = n_t9 - n_t11;   // stage 1 place 2
    wire signed [9:0] n_t27 = n_t10 + n_t12;   // stage 1 place 2
    wire signed [9:0] n_t28 = n_t10 - n_t12;   // stage 1 place 2
    wire signed [9:0] n_t29 = n_t13 + n_t15;   // stage 1 place 2
    wire signed [9:0] n_t30 = n_t13 - n_t15;   // stage 1 place 2
    wire signed [9:0] n_t31 = n_t14 + n_t16;   // stage 1 place 2
    wire signed [9:0] n_t32 = n_t14 - n_t16;   // stage 1 place 2
    wire signed [10:0] n_t33 = n_t17 + n_t21;   // stage 1 place 3
    wire signed [10:0] n_t34 = n_t17 - n_t21;   // stage 1 place 3
    wire signed [10:0] n_t35 = n_t19 + n_t23;   // stage 1 place 3
    wire signed [10:0] n_t36 = n_t19 - n_t23;   // stage 1 place 3
    wire signed [10:0] n_t37 = n_t18 + n_t22;   // stage 1 place 3
    wire signed [10:0] n_t38 = n_t18 - n_t22;   // stage 1 place 3
    wire signed [10:0] n_t39 = n_t20 + n_t24;   // stage 1 place 3
    wire signed [10:0] n_t40 = n_t20 - n_t24;   // stage 1 place 3
    wire signed [10:0] n_t41 = n_t25 + n_t29;   // stage 1 place 3
    wire signed [10:0] n_t42 = n_t25 - n_t29;   // stage 1 place 3
    wire signed [10:0] n_t43 = n_t27 + n_t31;   // stage 1 place 3
    wire signed [10:0] n_t44 = n_t27 - n_t31;   // stage 1 place 3
    wire signed [10:0] n_t45 = n_t26 + n_t30;   // stage 1 place 3
    wire signed [10:0] n_t46 = n_t26 - n_t30;   // stage 1 place 3
    wire signed [10:0] n_t47 = n_t28 + n_t32;   // stage 1 place 3
    wire signed [10:0] n_t48 = n_t28 - n_t32;   // stage 1 place 3
    wire signed [11:0] n_t49 = n_t33 + n_t41;   // stage 1 place 4
    wire signed [11:0] n_t50 = n_t33 - n_t41;   // stage 1 place 4
    wire signed [11:0] n_t51 = n_t35 + n_t43;   // stage 1 place 4
    wire signed [11:0] n_t52 = n_t35 - n_t43;   // stage 1 place 4
    wire signed [11:0] n_t53 = n_t37 + n_t45;   // stage 1 place 4
    wire signed [11:0] n_t54 = n_t37 - n_t45;   // stage 1 place 4
    wire signed [11:0] n_t55 = n_t39 + n_t47;   // stage 1 place 4
    wire signed [11:0] n_t56 = n_t39 - n_t47;   // stage 1 place 4
    wire signed [11:0] n_t57 = n_t34 + n_t42;   // stage 1 place 4
    wire signed [11:0] n_t58 = n_t34 - n_t42;   // stage 1 place 4
    wire signed [11:0] n_t59 = n_t36 + n_t44;   // stage 1 place 4
    wire signed [11:0] n_t60 = n_t36 - n_t44;   // stage 1 place 4
    wire signed [11:0] n_t61 = n_t38 + n_t46;   // stage 1 place 4
    wire signed [11:0] n_t62 = n_t38 - n_t46;   // stage 1 place 4
    wire signed [11:0] n_t63 = n_t40 + n_t48;   // stage 1 place 4
    wire signed [11:0] n_t64 = n_t40 - n_t48;   // stage 1 place 4
    always @(posedge clk) begin
        r_t49_b1 <= n_t49;
        r_t50_b1 <= n_t50;
        r_t51_b1 <= n_t51;
        r_t52_b1 <= n_t52;
        r_t53_b1 <= n_t53;
        r_t54_b1 <= n_t54;
        r_t55_b1 <= n_t55;
        r_t56_b1 <= n_t56;
        r_t57_b1 <= n_t57;
        r_t58_b1 <= n_t58;
        r_t59_b1 <= n_t59;
        r_t60_b1 <= n_t60;
        r_t61_b1 <= n_t61;
        r_t62_b1 <= n_t62;
        r_t63_b1 <= n_t63;
        r_t64_b1 <= n_t64;
    end
    wire signed [11:0] o0 = r_t49_b1;
    wire signed [11:0] o1 = r_t51_b1;
    wire signed [11:0] o2 = r_t53_b1;
    wire signed [11:0] o3 = r_t55_b1;
    wire signed [11:0] o4 = r_t57_b1;
    wire signed [11:0] o5 = r_t59_b1;
    wire signed [11:0] o6 = r_t61_b1;
    wire signed [11:0] o7 = r_t63_b1;
    wire signed [11:0] o8 = r_t50_b1;
    wire signed [11:0] o9 = r_t52_b1;
    wire signed [11:0] o10 = r_t54_b1;
    wire signed [11:0] o11 = r_t56_b1;
    wire signed [11:0] o12 = r_t58_b1;
    wire signed [11:0] o13 = r_t60_b1;
    wire signed [11:0] o14 = r_t62_b1;
    wire signed [11:0] o15 = r_t64_b1;
    assign out_data = {o15, o14, o13, o12, o11, o10, o9, o8, o7, o6, o5, o4, o3, o2, o1, o0};
    reg [0:0] vld = 0;
    always @(posedge clk) vld <= in_valid;
    assign out_valid = vld[0];
endmodule
