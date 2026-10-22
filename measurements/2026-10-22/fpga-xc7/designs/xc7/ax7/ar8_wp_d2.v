// Written by gen_ax7.py (wave 16, ax-7).  Do not edit by hand.
// 8-point WHT, word-parallel, registers placed by an integer program (min register bits).
// Source: tools/circuits/fpga/rtl/circuits/8_ar2023.txt
// adders 22, depth 6; at most 2 adder level(s) per clock; latency 3; register bits 304 (after adders 146, delay 158).
`default_nettype none
module wht_ar8_wp_d2 (
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
    reg signed [8:0] r_B1_b1;
    reg signed [8:0] r_B1_b2;
    reg signed [8:0] r_B2_b1;
    reg signed [8:0] r_B2_b2;
    reg signed [8:0] r_B3_b1;
    reg signed [8:0] r_B3_b2;
    reg signed [9:0] r_t1_b1;
    reg signed [9:0] r_t2_b1;
    reg signed [10:0] r_diff_b2;
    reg signed [10:0] r_y0_b2;
    reg signed [10:0] r_y0_b3;
    reg signed [10:0] r_y1_b3;
    reg signed [10:0] r_y2_b3;
    reg signed [10:0] r_y3_b3;
    reg signed [10:0] r_y4_b3;
    reg signed [10:0] r_y5_b3;
    reg signed [10:0] r_y6_b3;
    reg signed [10:0] r_y7_b3;
    reg signed [7:0] r_x0_b1;
    reg signed [7:0] r_x1_b1;
    reg signed [7:0] r_x1_b2;
    reg signed [7:0] r_x2_b1;
    reg signed [7:0] r_x2_b2;
    reg signed [7:0] r_x3_b1;
    reg signed [7:0] r_x3_b2;
    reg signed [7:0] r_x4_b1;
    reg signed [7:0] r_x4_b2;
    reg signed [7:0] r_x5_b1;
    reg signed [7:0] r_x5_b2;
    reg signed [7:0] r_x6_b1;
    reg signed [7:0] r_x6_b2;
    reg signed [7:0] r_x7_b1;
    reg signed [7:0] r_x7_b2;
    wire signed [8:0] n_B1 = x1 + x2;   // stage 1 place 1
    wire signed [8:0] n_B2 = x3 + x7;   // stage 1 place 1
    wire signed [8:0] n_B3 = x5 + x6;   // stage 1 place 1
    wire signed [9:0] n_t1 = n_B1 + n_B2;   // stage 1 place 2
    wire signed [9:0] n_t2 = n_B3 + x4;   // stage 1 place 2
    wire signed [10:0] n_totsum = r_t1_b1 + r_t2_b1;   // stage 2 place 1
    wire signed [10:0] n_diff = r_x0_b1 - n_totsum;   // stage 2 place 2
    wire signed [10:0] n_D = r_diff_b2 + (r_x3_b2 <<< 1);   // stage 3 place 1
    wire signed [10:0] n_E = r_diff_b2 + (r_x4_b2 <<< 1);   // stage 3 place 1
    wire signed [10:0] n_H = r_diff_b2 + (r_x7_b2 <<< 1);   // stage 3 place 1
    wire signed [10:0] n_y0 = r_x0_b1 + n_totsum;   // stage 2 place 2
    wire signed [8:0] n_u1 = r_x2_b2 + r_x6_b2;   // stage 3 place 1
    wire signed [10:0] n_y1 = n_E + (n_u1 <<< 1);   // stage 3 place 2
    wire signed [8:0] n_u2 = r_x1_b2 + r_x5_b2;   // stage 3 place 1
    wire signed [10:0] n_y2 = n_E + (n_u2 <<< 1);   // stage 3 place 2
    wire signed [10:0] n_y3 = n_E + (r_B2_b2 <<< 1);   // stage 3 place 2
    wire signed [10:0] n_y4 = n_D + (r_B1_b2 <<< 1);   // stage 3 place 2
    wire signed [8:0] n_u3 = r_x2_b2 + r_x5_b2;   // stage 3 place 1
    wire signed [10:0] n_y5 = n_H + (n_u3 <<< 1);   // stage 3 place 2
    wire signed [8:0] n_u4 = r_x1_b2 + r_x6_b2;   // stage 3 place 1
    wire signed [10:0] n_y6 = n_H + (n_u4 <<< 1);   // stage 3 place 2
    wire signed [10:0] n_y7 = n_D + (r_B3_b2 <<< 1);   // stage 3 place 2
    always @(posedge clk) begin
        r_B1_b1 <= n_B1;
        r_B1_b2 <= r_B1_b1;
        r_B2_b1 <= n_B2;
        r_B2_b2 <= r_B2_b1;
        r_B3_b1 <= n_B3;
        r_B3_b2 <= r_B3_b1;
        r_t1_b1 <= n_t1;
        r_t2_b1 <= n_t2;
        r_diff_b2 <= n_diff;
        r_y0_b2 <= n_y0;
        r_y0_b3 <= r_y0_b2;
        r_y1_b3 <= n_y1;
        r_y2_b3 <= n_y2;
        r_y3_b3 <= n_y3;
        r_y4_b3 <= n_y4;
        r_y5_b3 <= n_y5;
        r_y6_b3 <= n_y6;
        r_y7_b3 <= n_y7;
        r_x0_b1 <= x0;
        r_x1_b1 <= x1;
        r_x1_b2 <= r_x1_b1;
        r_x2_b1 <= x2;
        r_x2_b2 <= r_x2_b1;
        r_x3_b1 <= x3;
        r_x3_b2 <= r_x3_b1;
        r_x4_b1 <= x4;
        r_x4_b2 <= r_x4_b1;
        r_x5_b1 <= x5;
        r_x5_b2 <= r_x5_b1;
        r_x6_b1 <= x6;
        r_x6_b2 <= r_x6_b1;
        r_x7_b1 <= x7;
        r_x7_b2 <= r_x7_b1;
    end
    wire signed [10:0] o0 = r_y0_b3;
    wire signed [10:0] o1 = r_y1_b3;
    wire signed [10:0] o2 = r_y2_b3;
    wire signed [10:0] o3 = r_y3_b3;
    wire signed [10:0] o4 = r_y4_b3;
    wire signed [10:0] o5 = r_y5_b3;
    wire signed [10:0] o6 = r_y6_b3;
    wire signed [10:0] o7 = r_y7_b3;
    assign out_data = {o7, o6, o5, o4, o3, o2, o1, o0};
    reg [2:0] vld = 0;
    always @(posedge clk) vld <= {vld[1:0], in_valid};
    assign out_valid = vld[2];
endmodule
