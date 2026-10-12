// Written by gen_rtl.py.  Do not edit by hand.
// 8-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/programs/h8_19gates.txt
// This work: the 19-adder circuit.
// Inputs: 8 signed values of 12 bits.  Outputs: 8 signed values of 15 bits.
// Adders 19, depth 6 adder levels, adder bits 275 (chain bits 265).
// Variant c: combinational.  Latency 0.  clk is not used.
`default_nettype none
module wht_8_ours_c_w12 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [95:0] in_data,
    output wire                 out_valid,
    output wire [119:0] out_data
);
    wire signed [11:0] x0 = in_data[11:0];
    wire signed [11:0] x1 = in_data[23:12];
    wire signed [11:0] x2 = in_data[35:24];
    wire signed [11:0] x3 = in_data[47:36];
    wire signed [11:0] x4 = in_data[59:48];
    wire signed [11:0] x5 = in_data[71:60];
    wire signed [11:0] x6 = in_data[83:72];
    wire signed [11:0] x7 = in_data[95:84];
    wire signed [12:0] n_g1 = x0 + x7;   // level 1
    wire signed [12:0] n_g2 = x1 + x6;   // level 1
    wire signed [12:0] n_g3 = x2 - x5;   // level 1
    wire signed [12:0] n_g4 = x3 - x4;   // level 1
    wire signed [13:0] n_g5 = n_g1 - n_g2;   // level 2
    wire signed [13:0] n_g6 = n_g3 + n_g4;   // level 2
    wire signed [14:0] n_g7 = n_g5 - n_g6;   // level 3
    wire signed [14:0] n_g8 = n_g7 - (x7 <<< 1);   // level 4
    wire signed [14:0] n_g9 = n_g7 - (x5 <<< 1);   // level 4
    wire signed [14:0] n_g10 = n_g8 + (x6 <<< 1);   // level 5
    wire signed [14:0] n_g11 = n_g9 - (x4 <<< 1);   // level 5
    wire signed [14:0] n_y7 = n_g10 + (n_g4 <<< 1);   // level 6
    wire signed [14:0] n_y3 = n_g9 + (x3 <<< 1);   // level 5
    wire signed [14:0] n_y5 = (n_g5 <<< 1) - n_y3;   // level 6
    wire signed [14:0] n_y1 = n_g10 + (n_g3 <<< 1);   // level 6
    wire signed [14:0] n_y6 = n_g11 + (n_g2 <<< 1);   // level 6
    wire signed [14:0] n_y2 = n_g8 + (x1 <<< 1);   // level 5
    wire signed [14:0] n_y4 = n_y2 + (n_g6 <<< 1);   // level 6
    wire signed [14:0] n_y0 = (n_g1 <<< 1) - n_g11;   // level 6
    wire signed [14:0] o0 = n_y0;
    wire signed [14:0] o1 = n_y1;
    wire signed [14:0] o2 = n_y2;
    wire signed [14:0] o3 = n_y3;
    wire signed [14:0] o4 = n_y4;
    wire signed [14:0] o5 = n_y5;
    wire signed [14:0] o6 = n_y6;
    wire signed [14:0] o7 = n_y7;
    assign out_data = {
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    assign out_valid = in_valid;
    wire _unused_clk = clk;
endmodule
`default_nettype wire
