// Written by gen_rtl.py.  Do not edit by hand.
// 8-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/programs/h8_19gates.txt
// This work: the 19-adder circuit.
// Inputs: 8 signed values of 12 bits.  Outputs: 8 signed values of 15 bits.
// Adders 19, depth 6 adder levels, adder bits 275 (chain bits 265).
// Variant p: a register after every adder level.  Latency 6.
// Register bits: 275 after adders, 586 in delay registers, 6 valid bits.
`default_nettype none
module wht_8_ours_p_w12 (
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
    reg  signed [11:0] x1_r1;
    reg  signed [11:0] x1_r2;
    reg  signed [11:0] x1_r3;
    reg  signed [11:0] x1_r4;
    reg  signed [11:0] x3_r1;
    reg  signed [11:0] x3_r2;
    reg  signed [11:0] x3_r3;
    reg  signed [11:0] x3_r4;
    reg  signed [11:0] x4_r1;
    reg  signed [11:0] x4_r2;
    reg  signed [11:0] x4_r3;
    reg  signed [11:0] x4_r4;
    reg  signed [11:0] x5_r1;
    reg  signed [11:0] x5_r2;
    reg  signed [11:0] x5_r3;
    reg  signed [11:0] x6_r1;
    reg  signed [11:0] x6_r2;
    reg  signed [11:0] x6_r3;
    reg  signed [11:0] x6_r4;
    reg  signed [11:0] x7_r1;
    reg  signed [11:0] x7_r2;
    reg  signed [11:0] x7_r3;
    wire signed [12:0] n_g1 = x0 + x7;   // level 1, stage 1
    reg  signed [12:0] n_g1_r1;
    reg  signed [12:0] n_g1_r2;
    reg  signed [12:0] n_g1_r3;
    reg  signed [12:0] n_g1_r4;
    reg  signed [12:0] n_g1_r5;
    wire signed [12:0] n_g2 = x1 + x6;   // level 1, stage 1
    reg  signed [12:0] n_g2_r1;
    reg  signed [12:0] n_g2_r2;
    reg  signed [12:0] n_g2_r3;
    reg  signed [12:0] n_g2_r4;
    reg  signed [12:0] n_g2_r5;
    wire signed [12:0] n_g3 = x2 - x5;   // level 1, stage 1
    reg  signed [12:0] n_g3_r1;
    reg  signed [12:0] n_g3_r2;
    reg  signed [12:0] n_g3_r3;
    reg  signed [12:0] n_g3_r4;
    reg  signed [12:0] n_g3_r5;
    wire signed [12:0] n_g4 = x3 - x4;   // level 1, stage 1
    reg  signed [12:0] n_g4_r1;
    reg  signed [12:0] n_g4_r2;
    reg  signed [12:0] n_g4_r3;
    reg  signed [12:0] n_g4_r4;
    reg  signed [12:0] n_g4_r5;
    wire signed [13:0] n_g5 = n_g1_r1 - n_g2_r1;   // level 2, stage 2
    reg  signed [13:0] n_g5_r2;
    reg  signed [13:0] n_g5_r3;
    reg  signed [13:0] n_g5_r4;
    reg  signed [13:0] n_g5_r5;
    wire signed [13:0] n_g6 = n_g3_r1 + n_g4_r1;   // level 2, stage 2
    reg  signed [13:0] n_g6_r2;
    reg  signed [13:0] n_g6_r3;
    reg  signed [13:0] n_g6_r4;
    reg  signed [13:0] n_g6_r5;
    wire signed [14:0] n_g7 = n_g5_r2 - n_g6_r2;   // level 3, stage 3
    reg  signed [14:0] n_g7_r3;
    wire signed [14:0] n_g8 = n_g7_r3 - (x7_r3 <<< 1);   // level 4, stage 4
    reg  signed [14:0] n_g8_r4;
    wire signed [14:0] n_g9 = n_g7_r3 - (x5_r3 <<< 1);   // level 4, stage 4
    reg  signed [14:0] n_g9_r4;
    wire signed [14:0] n_g10 = n_g8_r4 + (x6_r4 <<< 1);   // level 5, stage 5
    reg  signed [14:0] n_g10_r5;
    wire signed [14:0] n_g11 = n_g9_r4 - (x4_r4 <<< 1);   // level 5, stage 5
    reg  signed [14:0] n_g11_r5;
    wire signed [14:0] n_y7 = n_g10_r5 + (n_g4_r5 <<< 1);   // level 6, stage 6
    reg  signed [14:0] n_y7_r6;
    wire signed [14:0] n_y3 = n_g9_r4 + (x3_r4 <<< 1);   // level 5, stage 5
    reg  signed [14:0] n_y3_r5;
    reg  signed [14:0] n_y3_r6;
    wire signed [14:0] n_y5 = (n_g5_r5 <<< 1) - n_y3_r5;   // level 6, stage 6
    reg  signed [14:0] n_y5_r6;
    wire signed [14:0] n_y1 = n_g10_r5 + (n_g3_r5 <<< 1);   // level 6, stage 6
    reg  signed [14:0] n_y1_r6;
    wire signed [14:0] n_y6 = n_g11_r5 + (n_g2_r5 <<< 1);   // level 6, stage 6
    reg  signed [14:0] n_y6_r6;
    wire signed [14:0] n_y2 = n_g8_r4 + (x1_r4 <<< 1);   // level 5, stage 5
    reg  signed [14:0] n_y2_r5;
    reg  signed [14:0] n_y2_r6;
    wire signed [14:0] n_y4 = n_y2_r5 + (n_g6_r5 <<< 1);   // level 6, stage 6
    reg  signed [14:0] n_y4_r6;
    wire signed [14:0] n_y0 = (n_g1_r5 <<< 1) - n_g11_r5;   // level 6, stage 6
    reg  signed [14:0] n_y0_r6;
    wire signed [14:0] o0 = n_y0_r6;
    wire signed [14:0] o1 = n_y1_r6;
    wire signed [14:0] o2 = n_y2_r6;
    wire signed [14:0] o3 = n_y3_r6;
    wire signed [14:0] o4 = n_y4_r6;
    wire signed [14:0] o5 = n_y5_r6;
    wire signed [14:0] o6 = n_y6_r6;
    wire signed [14:0] o7 = n_y7_r6;
    assign out_data = {
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    reg  [5:0] vld = 6'd0;
    always @(posedge clk) begin
        x1_r1 <= x1;
        x1_r2 <= x1_r1;
        x1_r3 <= x1_r2;
        x1_r4 <= x1_r3;
        x3_r1 <= x3;
        x3_r2 <= x3_r1;
        x3_r3 <= x3_r2;
        x3_r4 <= x3_r3;
        x4_r1 <= x4;
        x4_r2 <= x4_r1;
        x4_r3 <= x4_r2;
        x4_r4 <= x4_r3;
        x5_r1 <= x5;
        x5_r2 <= x5_r1;
        x5_r3 <= x5_r2;
        x6_r1 <= x6;
        x6_r2 <= x6_r1;
        x6_r3 <= x6_r2;
        x6_r4 <= x6_r3;
        x7_r1 <= x7;
        x7_r2 <= x7_r1;
        x7_r3 <= x7_r2;
        n_g1_r1 <= n_g1;
        n_g1_r2 <= n_g1_r1;
        n_g1_r3 <= n_g1_r2;
        n_g1_r4 <= n_g1_r3;
        n_g1_r5 <= n_g1_r4;
        n_g2_r1 <= n_g2;
        n_g2_r2 <= n_g2_r1;
        n_g2_r3 <= n_g2_r2;
        n_g2_r4 <= n_g2_r3;
        n_g2_r5 <= n_g2_r4;
        n_g3_r1 <= n_g3;
        n_g3_r2 <= n_g3_r1;
        n_g3_r3 <= n_g3_r2;
        n_g3_r4 <= n_g3_r3;
        n_g3_r5 <= n_g3_r4;
        n_g4_r1 <= n_g4;
        n_g4_r2 <= n_g4_r1;
        n_g4_r3 <= n_g4_r2;
        n_g4_r4 <= n_g4_r3;
        n_g4_r5 <= n_g4_r4;
        n_g5_r2 <= n_g5;
        n_g5_r3 <= n_g5_r2;
        n_g5_r4 <= n_g5_r3;
        n_g5_r5 <= n_g5_r4;
        n_g6_r2 <= n_g6;
        n_g6_r3 <= n_g6_r2;
        n_g6_r4 <= n_g6_r3;
        n_g6_r5 <= n_g6_r4;
        n_g7_r3 <= n_g7;
        n_g8_r4 <= n_g8;
        n_g9_r4 <= n_g9;
        n_g10_r5 <= n_g10;
        n_g11_r5 <= n_g11;
        n_y7_r6 <= n_y7;
        n_y3_r5 <= n_y3;
        n_y3_r6 <= n_y3_r5;
        n_y5_r6 <= n_y5;
        n_y1_r6 <= n_y1;
        n_y6_r6 <= n_y6;
        n_y2_r5 <= n_y2;
        n_y2_r6 <= n_y2_r5;
        n_y4_r6 <= n_y4;
        n_y0_r6 <= n_y0;
        vld <= {vld[4:0], in_valid};
    end
    assign out_valid = vld[5];
endmodule
`default_nettype wire
