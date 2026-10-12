// Written by gen_rtl.py.  Do not edit by hand.
// 8-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/fpga/rtl/circuits/8_ar2023l.txt
// Alman and Rao (2023), Algorithm 5 at 8 points, sums taken from left to right as written.  22 adders.
// Inputs: 8 signed values of 8 bits.  Outputs: 8 signed values of 11 bits.
// Adders 22, depth 8 adder levels, adder bits 235 (chain bits 221).
// Variant p2: a register after every second adder level.  Latency 4.
// Register bits: 169 after adders, 225 in delay registers, 4 valid bits.
`default_nettype none
module wht_8_ar2023l_p2_w8 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [63:0] in_data,
    output wire                 out_valid,
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
    reg  signed [7:0] x0_r1;
    reg  signed [7:0] x0_r2;
    reg  signed [7:0] x1_r1;
    reg  signed [7:0] x1_r2;
    reg  signed [7:0] x1_r3;
    reg  signed [7:0] x2_r1;
    reg  signed [7:0] x2_r2;
    reg  signed [7:0] x2_r3;
    reg  signed [7:0] x3_r1;
    reg  signed [7:0] x3_r2;
    reg  signed [7:0] x4_r1;
    reg  signed [7:0] x4_r2;
    reg  signed [7:0] x5_r1;
    reg  signed [7:0] x5_r2;
    reg  signed [7:0] x5_r3;
    reg  signed [7:0] x6_r1;
    reg  signed [7:0] x6_r2;
    reg  signed [7:0] x6_r3;
    reg  signed [7:0] x7_r1;
    reg  signed [7:0] x7_r2;
    wire signed [8:0] n_B1 = x1 + x2;   // level 1, stage 1
    reg  signed [8:0] n_B1_r1;
    reg  signed [8:0] n_B1_r2;
    reg  signed [8:0] n_B1_r3;
    wire signed [8:0] n_B2 = x3 + x7;   // level 1, stage 1
    reg  signed [8:0] n_B2_r1;
    reg  signed [8:0] n_B2_r2;
    reg  signed [8:0] n_B2_r3;
    wire signed [8:0] n_B3 = x5 + x6;   // level 1, stage 1
    reg  signed [8:0] n_B3_r1;
    reg  signed [8:0] n_B3_r2;
    reg  signed [8:0] n_B3_r3;
    wire signed [9:0] n_t1 = n_B1 + n_B2;   // level 2, stage 1
    reg  signed [9:0] n_t1_r1;
    wire signed [10:0] n_t2 = n_t1_r1 + n_B3_r1;   // level 3, stage 2
    wire signed [10:0] n_totsum = n_t2 + x4_r1;   // level 4, stage 2
    reg  signed [10:0] n_totsum_r2;
    wire signed [10:0] n_diff = x0_r2 - n_totsum_r2;   // level 5, stage 3
    wire signed [10:0] n_D = n_diff + (x3_r2 <<< 1);   // level 6, stage 3
    reg  signed [10:0] n_D_r3;
    wire signed [10:0] n_E = n_diff + (x4_r2 <<< 1);   // level 6, stage 3
    reg  signed [10:0] n_E_r3;
    wire signed [10:0] n_H = n_diff + (x7_r2 <<< 1);   // level 6, stage 3
    reg  signed [10:0] n_H_r3;
    wire signed [10:0] n_y0 = x0_r2 + n_totsum_r2;   // level 5, stage 3
    reg  signed [10:0] n_y0_r3;
    reg  signed [10:0] n_y0_r4;
    wire signed [10:0] n_u1 = n_E_r3 + (x2_r3 <<< 1);   // level 7, stage 4
    wire signed [10:0] n_y1 = n_u1 + (x6_r3 <<< 1);   // level 8, stage 4
    reg  signed [10:0] n_y1_r4;
    wire signed [10:0] n_u2 = n_E_r3 + (x1_r3 <<< 1);   // level 7, stage 4
    wire signed [10:0] n_y2 = n_u2 + (x5_r3 <<< 1);   // level 8, stage 4
    reg  signed [10:0] n_y2_r4;
    wire signed [10:0] n_y3 = n_E_r3 + (n_B2_r3 <<< 1);   // level 7, stage 4
    reg  signed [10:0] n_y3_r4;
    wire signed [10:0] n_y4 = n_D_r3 + (n_B1_r3 <<< 1);   // level 7, stage 4
    reg  signed [10:0] n_y4_r4;
    wire signed [10:0] n_u3 = n_H_r3 + (x2_r3 <<< 1);   // level 7, stage 4
    wire signed [10:0] n_y5 = n_u3 + (x5_r3 <<< 1);   // level 8, stage 4
    reg  signed [10:0] n_y5_r4;
    wire signed [10:0] n_u4 = n_H_r3 + (x1_r3 <<< 1);   // level 7, stage 4
    wire signed [10:0] n_y6 = n_u4 + (x6_r3 <<< 1);   // level 8, stage 4
    reg  signed [10:0] n_y6_r4;
    wire signed [10:0] n_y7 = n_D_r3 + (n_B3_r3 <<< 1);   // level 7, stage 4
    reg  signed [10:0] n_y7_r4;
    wire signed [10:0] o0 = n_y0_r4;
    wire signed [10:0] o1 = n_y1_r4;
    wire signed [10:0] o2 = n_y2_r4;
    wire signed [10:0] o3 = n_y3_r4;
    wire signed [10:0] o4 = n_y4_r4;
    wire signed [10:0] o5 = n_y5_r4;
    wire signed [10:0] o6 = n_y6_r4;
    wire signed [10:0] o7 = n_y7_r4;
    assign out_data = {
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    reg  [3:0] vld = 4'd0;
    always @(posedge clk) begin
        x0_r1 <= x0;
        x0_r2 <= x0_r1;
        x1_r1 <= x1;
        x1_r2 <= x1_r1;
        x1_r3 <= x1_r2;
        x2_r1 <= x2;
        x2_r2 <= x2_r1;
        x2_r3 <= x2_r2;
        x3_r1 <= x3;
        x3_r2 <= x3_r1;
        x4_r1 <= x4;
        x4_r2 <= x4_r1;
        x5_r1 <= x5;
        x5_r2 <= x5_r1;
        x5_r3 <= x5_r2;
        x6_r1 <= x6;
        x6_r2 <= x6_r1;
        x6_r3 <= x6_r2;
        x7_r1 <= x7;
        x7_r2 <= x7_r1;
        n_B1_r1 <= n_B1;
        n_B1_r2 <= n_B1_r1;
        n_B1_r3 <= n_B1_r2;
        n_B2_r1 <= n_B2;
        n_B2_r2 <= n_B2_r1;
        n_B2_r3 <= n_B2_r2;
        n_B3_r1 <= n_B3;
        n_B3_r2 <= n_B3_r1;
        n_B3_r3 <= n_B3_r2;
        n_t1_r1 <= n_t1;
        n_totsum_r2 <= n_totsum;
        n_D_r3 <= n_D;
        n_E_r3 <= n_E;
        n_H_r3 <= n_H;
        n_y0_r3 <= n_y0;
        n_y0_r4 <= n_y0_r3;
        n_y1_r4 <= n_y1;
        n_y2_r4 <= n_y2;
        n_y3_r4 <= n_y3;
        n_y4_r4 <= n_y4;
        n_y5_r4 <= n_y5;
        n_y6_r4 <= n_y6;
        n_y7_r4 <= n_y7;
        vld <= {vld[2:0], in_valid};
    end
    assign out_valid = vld[3];
endmodule
`default_nettype wire
