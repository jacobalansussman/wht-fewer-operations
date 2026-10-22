// Written by gen_ax7.py (wave 16, ax-7).  Do not edit by hand.
// 8-point WHT, word-parallel, registers placed by an integer program (min register bits).
// Source: tools/circuits/programs/h8_19gates.txt
// adders 19, depth 6; at most 1 adder level(s) per clock; latency 6; register bits 601 (after adders 199, delay 402).
`default_nettype none
module wht_o19_wp_d1 (
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
    reg signed [8:0] r_g1_b1;
    reg signed [8:0] r_g1_b2;
    reg signed [8:0] r_g1_b3;
    reg signed [8:0] r_g1_b4;
    reg signed [8:0] r_g1_b5;
    reg signed [8:0] r_g2_b1;
    reg signed [8:0] r_g2_b2;
    reg signed [8:0] r_g2_b3;
    reg signed [8:0] r_g2_b4;
    reg signed [8:0] r_g2_b5;
    reg signed [8:0] r_g3_b1;
    reg signed [8:0] r_g3_b2;
    reg signed [8:0] r_g3_b3;
    reg signed [8:0] r_g3_b4;
    reg signed [8:0] r_g3_b5;
    reg signed [8:0] r_g4_b1;
    reg signed [8:0] r_g4_b2;
    reg signed [8:0] r_g4_b3;
    reg signed [8:0] r_g4_b4;
    reg signed [8:0] r_g4_b5;
    reg signed [9:0] r_g5_b2;
    reg signed [9:0] r_g5_b3;
    reg signed [9:0] r_g5_b4;
    reg signed [9:0] r_g5_b5;
    reg signed [9:0] r_g6_b2;
    reg signed [9:0] r_g6_b3;
    reg signed [9:0] r_g6_b4;
    reg signed [9:0] r_g6_b5;
    reg signed [10:0] r_g7_b3;
    reg signed [10:0] r_g8_b4;
    reg signed [10:0] r_g9_b4;
    reg signed [10:0] r_g10_b5;
    reg signed [10:0] r_g11_b5;
    reg signed [10:0] r_y7_b6;
    reg signed [10:0] r_y3_b5;
    reg signed [10:0] r_y3_b6;
    reg signed [10:0] r_y5_b6;
    reg signed [10:0] r_y1_b6;
    reg signed [10:0] r_y6_b6;
    reg signed [10:0] r_y2_b5;
    reg signed [10:0] r_y2_b6;
    reg signed [10:0] r_y4_b6;
    reg signed [10:0] r_y0_b6;
    reg signed [7:0] r_x1_b1;
    reg signed [7:0] r_x1_b2;
    reg signed [7:0] r_x1_b3;
    reg signed [7:0] r_x1_b4;
    reg signed [7:0] r_x3_b1;
    reg signed [7:0] r_x3_b2;
    reg signed [7:0] r_x3_b3;
    reg signed [7:0] r_x3_b4;
    reg signed [7:0] r_x4_b1;
    reg signed [7:0] r_x4_b2;
    reg signed [7:0] r_x4_b3;
    reg signed [7:0] r_x4_b4;
    reg signed [7:0] r_x5_b1;
    reg signed [7:0] r_x5_b2;
    reg signed [7:0] r_x5_b3;
    reg signed [7:0] r_x6_b1;
    reg signed [7:0] r_x6_b2;
    reg signed [7:0] r_x6_b3;
    reg signed [7:0] r_x6_b4;
    reg signed [7:0] r_x7_b1;
    reg signed [7:0] r_x7_b2;
    reg signed [7:0] r_x7_b3;
    wire signed [8:0] n_g1 = x0 + x7;   // stage 1 place 1
    wire signed [8:0] n_g2 = x1 + x6;   // stage 1 place 1
    wire signed [8:0] n_g3 = x2 - x5;   // stage 1 place 1
    wire signed [8:0] n_g4 = x3 - x4;   // stage 1 place 1
    wire signed [9:0] n_g5 = r_g1_b1 - r_g2_b1;   // stage 2 place 1
    wire signed [9:0] n_g6 = r_g3_b1 + r_g4_b1;   // stage 2 place 1
    wire signed [10:0] n_g7 = r_g5_b2 - r_g6_b2;   // stage 3 place 1
    wire signed [10:0] n_g8 = r_g7_b3 - (r_x7_b3 <<< 1);   // stage 4 place 1
    wire signed [10:0] n_g9 = r_g7_b3 - (r_x5_b3 <<< 1);   // stage 4 place 1
    wire signed [10:0] n_g10 = r_g8_b4 + (r_x6_b4 <<< 1);   // stage 5 place 1
    wire signed [10:0] n_g11 = r_g9_b4 - (r_x4_b4 <<< 1);   // stage 5 place 1
    wire signed [10:0] n_y7 = r_g10_b5 + (r_g4_b5 <<< 1);   // stage 6 place 1
    wire signed [10:0] n_y3 = r_g9_b4 + (r_x3_b4 <<< 1);   // stage 5 place 1
    wire signed [10:0] n_y5 = (r_g5_b5 <<< 1) - r_y3_b5;   // stage 6 place 1
    wire signed [10:0] n_y1 = r_g10_b5 + (r_g3_b5 <<< 1);   // stage 6 place 1
    wire signed [10:0] n_y6 = r_g11_b5 + (r_g2_b5 <<< 1);   // stage 6 place 1
    wire signed [10:0] n_y2 = r_g8_b4 + (r_x1_b4 <<< 1);   // stage 5 place 1
    wire signed [10:0] n_y4 = r_y2_b5 + (r_g6_b5 <<< 1);   // stage 6 place 1
    wire signed [10:0] n_y0 = (r_g1_b5 <<< 1) - r_g11_b5;   // stage 6 place 1
    always @(posedge clk) begin
        r_g1_b1 <= n_g1;
        r_g1_b2 <= r_g1_b1;
        r_g1_b3 <= r_g1_b2;
        r_g1_b4 <= r_g1_b3;
        r_g1_b5 <= r_g1_b4;
        r_g2_b1 <= n_g2;
        r_g2_b2 <= r_g2_b1;
        r_g2_b3 <= r_g2_b2;
        r_g2_b4 <= r_g2_b3;
        r_g2_b5 <= r_g2_b4;
        r_g3_b1 <= n_g3;
        r_g3_b2 <= r_g3_b1;
        r_g3_b3 <= r_g3_b2;
        r_g3_b4 <= r_g3_b3;
        r_g3_b5 <= r_g3_b4;
        r_g4_b1 <= n_g4;
        r_g4_b2 <= r_g4_b1;
        r_g4_b3 <= r_g4_b2;
        r_g4_b4 <= r_g4_b3;
        r_g4_b5 <= r_g4_b4;
        r_g5_b2 <= n_g5;
        r_g5_b3 <= r_g5_b2;
        r_g5_b4 <= r_g5_b3;
        r_g5_b5 <= r_g5_b4;
        r_g6_b2 <= n_g6;
        r_g6_b3 <= r_g6_b2;
        r_g6_b4 <= r_g6_b3;
        r_g6_b5 <= r_g6_b4;
        r_g7_b3 <= n_g7;
        r_g8_b4 <= n_g8;
        r_g9_b4 <= n_g9;
        r_g10_b5 <= n_g10;
        r_g11_b5 <= n_g11;
        r_y7_b6 <= n_y7;
        r_y3_b5 <= n_y3;
        r_y3_b6 <= r_y3_b5;
        r_y5_b6 <= n_y5;
        r_y1_b6 <= n_y1;
        r_y6_b6 <= n_y6;
        r_y2_b5 <= n_y2;
        r_y2_b6 <= r_y2_b5;
        r_y4_b6 <= n_y4;
        r_y0_b6 <= n_y0;
        r_x1_b1 <= x1;
        r_x1_b2 <= r_x1_b1;
        r_x1_b3 <= r_x1_b2;
        r_x1_b4 <= r_x1_b3;
        r_x3_b1 <= x3;
        r_x3_b2 <= r_x3_b1;
        r_x3_b3 <= r_x3_b2;
        r_x3_b4 <= r_x3_b3;
        r_x4_b1 <= x4;
        r_x4_b2 <= r_x4_b1;
        r_x4_b3 <= r_x4_b2;
        r_x4_b4 <= r_x4_b3;
        r_x5_b1 <= x5;
        r_x5_b2 <= r_x5_b1;
        r_x5_b3 <= r_x5_b2;
        r_x6_b1 <= x6;
        r_x6_b2 <= r_x6_b1;
        r_x6_b3 <= r_x6_b2;
        r_x6_b4 <= r_x6_b3;
        r_x7_b1 <= x7;
        r_x7_b2 <= r_x7_b1;
        r_x7_b3 <= r_x7_b2;
    end
    wire signed [10:0] o0 = r_y0_b6;
    wire signed [10:0] o1 = r_y1_b6;
    wire signed [10:0] o2 = r_y2_b6;
    wire signed [10:0] o3 = r_y3_b6;
    wire signed [10:0] o4 = r_y4_b6;
    wire signed [10:0] o5 = r_y5_b6;
    wire signed [10:0] o6 = r_y6_b6;
    wire signed [10:0] o7 = r_y7_b6;
    assign out_data = {o7, o6, o5, o4, o3, o2, o1, o0};
    reg [5:0] vld = 0;
    always @(posedge clk) vld <= {vld[4:0], in_valid};
    assign out_valid = vld[5];
endmodule
