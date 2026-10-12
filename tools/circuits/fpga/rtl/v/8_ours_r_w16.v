// Written by gen_rtl.py.  Do not edit by hand.
// 8-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/programs/h8_19gates.txt
// This work: the 19-adder circuit.
// Inputs: 8 signed values of 16 bits.  Outputs: 8 signed values of 19 bits.
// Adders 19, depth 6 adder levels, adder bits 351 (chain bits 341).
// Variant r: one register stage at the inputs, 1 at the outputs, nothing between.  Latency 2.
// Register bits: 128 at the inputs, 152 at the outputs, 2 valid bits.
`default_nettype none
module wht_8_ours_r_w16 (
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
    wire signed [16:0] n_g1 = x0 + x7;   // level 1
    wire signed [16:0] n_g2 = x1 + x6;   // level 1
    wire signed [16:0] n_g3 = x2 - x5;   // level 1
    wire signed [16:0] n_g4 = x3 - x4;   // level 1
    wire signed [17:0] n_g5 = n_g1 - n_g2;   // level 2
    wire signed [17:0] n_g6 = n_g3 + n_g4;   // level 2
    wire signed [18:0] n_g7 = n_g5 - n_g6;   // level 3
    wire signed [18:0] n_g8 = n_g7 - (x7 <<< 1);   // level 4
    wire signed [18:0] n_g9 = n_g7 - (x5 <<< 1);   // level 4
    wire signed [18:0] n_g10 = n_g8 + (x6 <<< 1);   // level 5
    wire signed [18:0] n_g11 = n_g9 - (x4 <<< 1);   // level 5
    wire signed [18:0] n_y7 = n_g10 + (n_g4 <<< 1);   // level 6
    wire signed [18:0] n_y3 = n_g9 + (x3 <<< 1);   // level 5
    wire signed [18:0] n_y5 = (n_g5 <<< 1) - n_y3;   // level 6
    wire signed [18:0] n_y1 = n_g10 + (n_g3 <<< 1);   // level 6
    wire signed [18:0] n_y6 = n_g11 + (n_g2 <<< 1);   // level 6
    wire signed [18:0] n_y2 = n_g8 + (x1 <<< 1);   // level 5
    wire signed [18:0] n_y4 = n_y2 + (n_g6 <<< 1);   // level 6
    wire signed [18:0] n_y0 = (n_g1 <<< 1) - n_g11;   // level 6
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
