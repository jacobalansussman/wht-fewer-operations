// Written by gen_rtl.py.  Do not edit by hand.
// 8-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/programs/h8_19gates.txt
// Inputs: 8 signed values of 9 bits.  Outputs: 8 signed values of 12 bits.
// Adders 19, depth 6 adder levels, adder bits 218 (chain bits 208).
// Variant c: combinational.  Latency 0.  clk is not used.
`default_nettype none
module wht_8_ours_c_w9 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [71:0] in_data,
    output wire                 out_valid,
    output wire [95:0] out_data
);
    wire signed [8:0] x0 = in_data[8:0];
    wire signed [8:0] x1 = in_data[17:9];
    wire signed [8:0] x2 = in_data[26:18];
    wire signed [8:0] x3 = in_data[35:27];
    wire signed [8:0] x4 = in_data[44:36];
    wire signed [8:0] x5 = in_data[53:45];
    wire signed [8:0] x6 = in_data[62:54];
    wire signed [8:0] x7 = in_data[71:63];
    wire signed [9:0] n_g1 = x0 + x7;   // level 1
    wire signed [9:0] n_g2 = x1 + x6;   // level 1
    wire signed [9:0] n_g3 = x2 - x5;   // level 1
    wire signed [9:0] n_g4 = x3 - x4;   // level 1
    wire signed [10:0] n_g5 = n_g1 - n_g2;   // level 2
    wire signed [10:0] n_g6 = n_g3 + n_g4;   // level 2
    wire signed [11:0] n_g7 = n_g5 - n_g6;   // level 3
    wire signed [11:0] n_g8 = n_g7 - (x7 <<< 1);   // level 4
    wire signed [11:0] n_g9 = n_g7 - (x5 <<< 1);   // level 4
    wire signed [11:0] n_g10 = n_g8 + (x6 <<< 1);   // level 5
    wire signed [11:0] n_g11 = n_g9 - (x4 <<< 1);   // level 5
    wire signed [11:0] n_y7 = n_g10 + (n_g4 <<< 1);   // level 6
    wire signed [11:0] n_y3 = n_g9 + (x3 <<< 1);   // level 5
    wire signed [11:0] n_y5 = (n_g5 <<< 1) - n_y3;   // level 6
    wire signed [11:0] n_y1 = n_g10 + (n_g3 <<< 1);   // level 6
    wire signed [11:0] n_y6 = n_g11 + (n_g2 <<< 1);   // level 6
    wire signed [11:0] n_y2 = n_g8 + (x1 <<< 1);   // level 5
    wire signed [11:0] n_y4 = n_y2 + (n_g6 <<< 1);   // level 6
    wire signed [11:0] n_y0 = (n_g1 <<< 1) - n_g11;   // level 6
    wire signed [11:0] o0 = n_y0;
    wire signed [11:0] o1 = n_y1;
    wire signed [11:0] o2 = n_y2;
    wire signed [11:0] o3 = n_y3;
    wire signed [11:0] o4 = n_y4;
    wire signed [11:0] o5 = n_y5;
    wire signed [11:0] o6 = n_y6;
    wire signed [11:0] o7 = n_y7;
    assign out_data = {
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    assign out_valid = in_valid;
    wire _unused_clk = clk;
endmodule
`default_nettype wire
