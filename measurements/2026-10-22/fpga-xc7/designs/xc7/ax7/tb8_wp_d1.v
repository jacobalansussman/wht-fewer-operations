// Written by gen_ax7.py (wave 16, ax-7).  Do not edit by hand.
// 8-point WHT, word-parallel, registers placed by an integer program (min register bits).
// Source: tools/circuits/programs/generated/O_textbook_8.txt
// adders 24, depth 3; at most 1 adder level(s) per clock; latency 3; register bits 240 (after adders 240, delay 0).
`default_nettype none
module wht_tb8_wp_d1 (
    input  wire clk,
    input  wire in_valid,
    input  wire [63:0] in_data,
    output wire out_valid,
    output wire [87:0] out_data
);
    wire signed [7:0] x0 = in_data[7:0];
    wire signed [7:0] x1 = in_data[15:8];
    wire signed [7:0] x2 = in_data[23:16];
    wire signed [7:0] x3 = in_data[31:24];
    wire signed [7:0] x4 = in_data[39:32];
    wire signed [7:0] x5 = in_data[47:40];
    wire signed [7:0] x6 = in_data[55:48];
    wire signed [7:0] x7 = in_data[63:56];
    reg signed [8:0] r_t1_b1;
    reg signed [8:0] r_t2_b1;
    reg signed [8:0] r_t3_b1;
    reg signed [8:0] r_t4_b1;
    reg signed [8:0] r_t5_b1;
    reg signed [8:0] r_t6_b1;
    reg signed [8:0] r_t7_b1;
    reg signed [8:0] r_t8_b1;
    reg signed [9:0] r_t9_b2;
    reg signed [9:0] r_t10_b2;
    reg signed [9:0] r_t11_b2;
    reg signed [9:0] r_t12_b2;
    reg signed [9:0] r_t13_b2;
    reg signed [9:0] r_t14_b2;
    reg signed [9:0] r_t15_b2;
    reg signed [9:0] r_t16_b2;
    reg signed [10:0] r_t17_b3;
    reg signed [10:0] r_t18_b3;
    reg signed [10:0] r_t19_b3;
    reg signed [10:0] r_t20_b3;
    reg signed [10:0] r_t21_b3;
    reg signed [10:0] r_t22_b3;
    reg signed [10:0] r_t23_b3;
    reg signed [10:0] r_t24_b3;
    wire signed [8:0] n_t1 = x0 + x1;   // stage 1 place 1
    wire signed [8:0] n_t2 = x0 - x1;   // stage 1 place 1
    wire signed [8:0] n_t3 = x2 + x3;   // stage 1 place 1
    wire signed [8:0] n_t4 = x2 - x3;   // stage 1 place 1
    wire signed [8:0] n_t5 = x4 + x5;   // stage 1 place 1
    wire signed [8:0] n_t6 = x4 - x5;   // stage 1 place 1
    wire signed [8:0] n_t7 = x6 + x7;   // stage 1 place 1
    wire signed [8:0] n_t8 = x6 - x7;   // stage 1 place 1
    wire signed [9:0] n_t9 = r_t1_b1 + r_t3_b1;   // stage 2 place 1
    wire signed [9:0] n_t10 = r_t1_b1 - r_t3_b1;   // stage 2 place 1
    wire signed [9:0] n_t11 = r_t2_b1 + r_t4_b1;   // stage 2 place 1
    wire signed [9:0] n_t12 = r_t2_b1 - r_t4_b1;   // stage 2 place 1
    wire signed [9:0] n_t13 = r_t5_b1 + r_t7_b1;   // stage 2 place 1
    wire signed [9:0] n_t14 = r_t5_b1 - r_t7_b1;   // stage 2 place 1
    wire signed [9:0] n_t15 = r_t6_b1 + r_t8_b1;   // stage 2 place 1
    wire signed [9:0] n_t16 = r_t6_b1 - r_t8_b1;   // stage 2 place 1
    wire signed [10:0] n_t17 = r_t9_b2 + r_t13_b2;   // stage 3 place 1
    wire signed [10:0] n_t18 = r_t9_b2 - r_t13_b2;   // stage 3 place 1
    wire signed [10:0] n_t19 = r_t11_b2 + r_t15_b2;   // stage 3 place 1
    wire signed [10:0] n_t20 = r_t11_b2 - r_t15_b2;   // stage 3 place 1
    wire signed [10:0] n_t21 = r_t10_b2 + r_t14_b2;   // stage 3 place 1
    wire signed [10:0] n_t22 = r_t10_b2 - r_t14_b2;   // stage 3 place 1
    wire signed [10:0] n_t23 = r_t12_b2 + r_t16_b2;   // stage 3 place 1
    wire signed [10:0] n_t24 = r_t12_b2 - r_t16_b2;   // stage 3 place 1
    always @(posedge clk) begin
        r_t1_b1 <= n_t1;
        r_t2_b1 <= n_t2;
        r_t3_b1 <= n_t3;
        r_t4_b1 <= n_t4;
        r_t5_b1 <= n_t5;
        r_t6_b1 <= n_t6;
        r_t7_b1 <= n_t7;
        r_t8_b1 <= n_t8;
        r_t9_b2 <= n_t9;
        r_t10_b2 <= n_t10;
        r_t11_b2 <= n_t11;
        r_t12_b2 <= n_t12;
        r_t13_b2 <= n_t13;
        r_t14_b2 <= n_t14;
        r_t15_b2 <= n_t15;
        r_t16_b2 <= n_t16;
        r_t17_b3 <= n_t17;
        r_t18_b3 <= n_t18;
        r_t19_b3 <= n_t19;
        r_t20_b3 <= n_t20;
        r_t21_b3 <= n_t21;
        r_t22_b3 <= n_t22;
        r_t23_b3 <= n_t23;
        r_t24_b3 <= n_t24;
    end
    wire signed [10:0] o0 = r_t17_b3;
    wire signed [10:0] o1 = r_t19_b3;
    wire signed [10:0] o2 = r_t21_b3;
    wire signed [10:0] o3 = r_t23_b3;
    wire signed [10:0] o4 = r_t18_b3;
    wire signed [10:0] o5 = r_t20_b3;
    wire signed [10:0] o6 = r_t22_b3;
    wire signed [10:0] o7 = r_t24_b3;
    assign out_data = {o7, o6, o5, o4, o3, o2, o1, o0};
    reg [2:0] vld = 0;
    always @(posedge clk) vld <= {vld[1:0], in_valid};
    assign out_valid = vld[2];
endmodule
