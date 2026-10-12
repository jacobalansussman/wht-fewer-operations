// Written by gen_rtl.py.  Do not edit by hand.
// 8-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/fpga/rtl/circuits/8_ar2023.txt
// Alman and Rao (2023), Algorithm 5 at 8 points: 22 adders; the halving and the doublings are wiring.
// Their sums of three and four terms are bracketed in pairs.
// Inputs: 8 signed values of 16 bits.  Outputs: 8 signed values of 19 bits.
// Adders 22, depth 6 adder levels, adder bits 402 (chain bits 392).
// Variant c: combinational.  Latency 0.  clk is not used.
`default_nettype none
module wht_8_ar2023_c_w16 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [127:0] in_data,
    output wire                 out_valid,
    output wire [151:0] out_data
);
    wire signed [15:0] x0 = in_data[15:0];
    wire signed [15:0] x1 = in_data[31:16];
    wire signed [15:0] x2 = in_data[47:32];
    wire signed [15:0] x3 = in_data[63:48];
    wire signed [15:0] x4 = in_data[79:64];
    wire signed [15:0] x5 = in_data[95:80];
    wire signed [15:0] x6 = in_data[111:96];
    wire signed [15:0] x7 = in_data[127:112];
    wire signed [16:0] n_B1 = x1 + x2;   // level 1
    wire signed [16:0] n_B2 = x3 + x7;   // level 1
    wire signed [16:0] n_B3 = x5 + x6;   // level 1
    wire signed [17:0] n_t1 = n_B1 + n_B2;   // level 2
    wire signed [17:0] n_t2 = n_B3 + x4;   // level 2
    wire signed [18:0] n_totsum = n_t1 + n_t2;   // level 3
    wire signed [18:0] n_diff = x0 - n_totsum;   // level 4
    wire signed [18:0] n_D = n_diff + (x3 <<< 1);   // level 5
    wire signed [18:0] n_E = n_diff + (x4 <<< 1);   // level 5
    wire signed [18:0] n_H = n_diff + (x7 <<< 1);   // level 5
    wire signed [18:0] n_y0 = x0 + n_totsum;   // level 4
    wire signed [16:0] n_u1 = x2 + x6;   // level 1
    wire signed [18:0] n_y1 = n_E + (n_u1 <<< 1);   // level 6
    wire signed [16:0] n_u2 = x1 + x5;   // level 1
    wire signed [18:0] n_y2 = n_E + (n_u2 <<< 1);   // level 6
    wire signed [18:0] n_y3 = n_E + (n_B2 <<< 1);   // level 6
    wire signed [18:0] n_y4 = n_D + (n_B1 <<< 1);   // level 6
    wire signed [16:0] n_u3 = x2 + x5;   // level 1
    wire signed [18:0] n_y5 = n_H + (n_u3 <<< 1);   // level 6
    wire signed [16:0] n_u4 = x1 + x6;   // level 1
    wire signed [18:0] n_y6 = n_H + (n_u4 <<< 1);   // level 6
    wire signed [18:0] n_y7 = n_D + (n_B3 <<< 1);   // level 6
    wire signed [18:0] o0 = n_y0;
    wire signed [18:0] o1 = n_y1;
    wire signed [18:0] o2 = n_y2;
    wire signed [18:0] o3 = n_y3;
    wire signed [18:0] o4 = n_y4;
    wire signed [18:0] o5 = n_y5;
    wire signed [18:0] o6 = n_y6;
    wire signed [18:0] o7 = n_y7;
    assign out_data = {
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    assign out_valid = in_valid;
    wire _unused_clk = clk;
endmodule
`default_nettype wire
