// Written by gen_rtl.py.  Do not edit by hand.
// 8-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/fpga/rtl/circuits/8_ar2023.txt
// Alman and Rao (2023), Algorithm 5 at 8 points: 22 adders; the halving and the doublings are wiring.
// Their sums of three and four terms are bracketed in pairs.
// Inputs: 8 signed values of 12 bits.  Outputs: 8 signed values of 15 bits.
// Adders 22, depth 6 adder levels, adder bits 314 (chain bits 304).
// Variant r: one register stage at the inputs, 1 at the outputs, nothing between.  Latency 2.
// Register bits: 96 at the inputs, 120 at the outputs, 2 valid bits.
`default_nettype none
module wht_8_ar2023_r_w12 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [95:0] in_data,
    output wire                 out_valid,
    output wire [119:0] out_data
);
    reg  signed [11:0] x0;
    reg  signed [11:0] x1;
    reg  signed [11:0] x2;
    reg  signed [11:0] x3;
    reg  signed [11:0] x4;
    reg  signed [11:0] x5;
    reg  signed [11:0] x6;
    reg  signed [11:0] x7;
    always @(posedge clk) begin
        x0 <= in_data[11:0];
        x1 <= in_data[23:12];
        x2 <= in_data[35:24];
        x3 <= in_data[47:36];
        x4 <= in_data[59:48];
        x5 <= in_data[71:60];
        x6 <= in_data[83:72];
        x7 <= in_data[95:84];
    end
    wire signed [12:0] n_B1 = x1 + x2;   // level 1
    wire signed [12:0] n_B2 = x3 + x7;   // level 1
    wire signed [12:0] n_B3 = x5 + x6;   // level 1
    wire signed [13:0] n_t1 = n_B1 + n_B2;   // level 2
    wire signed [13:0] n_t2 = n_B3 + x4;   // level 2
    wire signed [14:0] n_totsum = n_t1 + n_t2;   // level 3
    wire signed [14:0] n_diff = x0 - n_totsum;   // level 4
    wire signed [14:0] n_D = n_diff + (x3 <<< 1);   // level 5
    wire signed [14:0] n_E = n_diff + (x4 <<< 1);   // level 5
    wire signed [14:0] n_H = n_diff + (x7 <<< 1);   // level 5
    wire signed [14:0] n_y0 = x0 + n_totsum;   // level 4
    wire signed [12:0] n_u1 = x2 + x6;   // level 1
    wire signed [14:0] n_y1 = n_E + (n_u1 <<< 1);   // level 6
    wire signed [12:0] n_u2 = x1 + x5;   // level 1
    wire signed [14:0] n_y2 = n_E + (n_u2 <<< 1);   // level 6
    wire signed [14:0] n_y3 = n_E + (n_B2 <<< 1);   // level 6
    wire signed [14:0] n_y4 = n_D + (n_B1 <<< 1);   // level 6
    wire signed [12:0] n_u3 = x2 + x5;   // level 1
    wire signed [14:0] n_y5 = n_H + (n_u3 <<< 1);   // level 6
    wire signed [12:0] n_u4 = x1 + x6;   // level 1
    wire signed [14:0] n_y6 = n_H + (n_u4 <<< 1);   // level 6
    wire signed [14:0] n_y7 = n_D + (n_B3 <<< 1);   // level 6
    wire signed [14:0] o0 = n_y0;
    wire signed [14:0] o1 = n_y1;
    wire signed [14:0] o2 = n_y2;
    wire signed [14:0] o3 = n_y3;
    wire signed [14:0] o4 = n_y4;
    wire signed [14:0] o5 = n_y5;
    wire signed [14:0] o6 = n_y6;
    wire signed [14:0] o7 = n_y7;
    wire [119:0] out_comb = {
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    reg  [119:0] out_q1;
    reg  [1:0] vld = 2'd0;
    always @(posedge clk) begin
        out_q1 <= out_comb;
        vld <= {vld[0:0], in_valid};
    end
    assign out_data = out_q1;
    assign out_valid = vld[1];
endmodule
`default_nettype wire
