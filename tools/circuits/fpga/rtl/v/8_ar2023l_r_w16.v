// Written by gen_rtl.py.  Do not edit by hand.
// 8-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/fpga/rtl/circuits/8_ar2023l.txt
// Alman and Rao (2023), Algorithm 5 at 8 points, sums taken from left to right as written.  22 adders.
// Inputs: 8 signed values of 16 bits.  Outputs: 8 signed values of 19 bits.
// Adders 22, depth 8 adder levels, adder bits 411 (chain bits 397).
// Variant r: one register stage at the inputs, 1 at the outputs, nothing between.  Latency 2.
// Register bits: 128 at the inputs, 152 at the outputs, 2 valid bits.
`default_nettype none
module wht_8_ar2023l_r_w16 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [127:0] in_data,
    output wire                 out_valid,
    output wire [151:0] out_data
);
    reg  signed [15:0] x0;
    reg  signed [15:0] x1;
    reg  signed [15:0] x2;
    reg  signed [15:0] x3;
    reg  signed [15:0] x4;
    reg  signed [15:0] x5;
    reg  signed [15:0] x6;
    reg  signed [15:0] x7;
    always @(posedge clk) begin
        x0 <= in_data[15:0];
        x1 <= in_data[31:16];
        x2 <= in_data[47:32];
        x3 <= in_data[63:48];
        x4 <= in_data[79:64];
        x5 <= in_data[95:80];
        x6 <= in_data[111:96];
        x7 <= in_data[127:112];
    end
    wire signed [16:0] n_B1 = x1 + x2;   // level 1
    wire signed [16:0] n_B2 = x3 + x7;   // level 1
    wire signed [16:0] n_B3 = x5 + x6;   // level 1
    wire signed [17:0] n_t1 = n_B1 + n_B2;   // level 2
    wire signed [18:0] n_t2 = n_t1 + n_B3;   // level 3
    wire signed [18:0] n_totsum = n_t2 + x4;   // level 4
    wire signed [18:0] n_diff = x0 - n_totsum;   // level 5
    wire signed [18:0] n_D = n_diff + (x3 <<< 1);   // level 6
    wire signed [18:0] n_E = n_diff + (x4 <<< 1);   // level 6
    wire signed [18:0] n_H = n_diff + (x7 <<< 1);   // level 6
    wire signed [18:0] n_y0 = x0 + n_totsum;   // level 5
    wire signed [18:0] n_u1 = n_E + (x2 <<< 1);   // level 7
    wire signed [18:0] n_y1 = n_u1 + (x6 <<< 1);   // level 8
    wire signed [18:0] n_u2 = n_E + (x1 <<< 1);   // level 7
    wire signed [18:0] n_y2 = n_u2 + (x5 <<< 1);   // level 8
    wire signed [18:0] n_y3 = n_E + (n_B2 <<< 1);   // level 7
    wire signed [18:0] n_y4 = n_D + (n_B1 <<< 1);   // level 7
    wire signed [18:0] n_u3 = n_H + (x2 <<< 1);   // level 7
    wire signed [18:0] n_y5 = n_u3 + (x5 <<< 1);   // level 8
    wire signed [18:0] n_u4 = n_H + (x1 <<< 1);   // level 7
    wire signed [18:0] n_y6 = n_u4 + (x6 <<< 1);   // level 8
    wire signed [18:0] n_y7 = n_D + (n_B3 <<< 1);   // level 7
    wire signed [18:0] o0 = n_y0;
    wire signed [18:0] o1 = n_y1;
    wire signed [18:0] o2 = n_y2;
    wire signed [18:0] o3 = n_y3;
    wire signed [18:0] o4 = n_y4;
    wire signed [18:0] o5 = n_y5;
    wire signed [18:0] o6 = n_y6;
    wire signed [18:0] o7 = n_y7;
    wire [151:0] out_comb = {
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    reg  [151:0] out_q1;
    reg  [1:0] vld = 2'd0;
    always @(posedge clk) begin
        out_q1 <= out_comb;
        vld <= {vld[0:0], in_valid};
    end
    assign out_data = out_q1;
    assign out_valid = vld[1];
endmodule
`default_nettype wire
