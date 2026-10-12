// Written by gen_rtl.py.  Do not edit by hand.
// 8-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/fpga/rtl/circuits/8_cfl1994.txt
// Coppersmith, Feig, Linzer (1994): two 4-point circuits of 7, then one plain layer of 8.  22 adders.
// Inputs: 8 signed values of 16 bits.  Outputs: 8 signed values of 19 bits.
// Adders 22, depth 5 adder levels, adder bits 402 (chain bits 396).
// Variant p: a register after every adder level.  Latency 5.
// Register bits: 402 after adders, 390 in delay registers, 5 valid bits.
`default_nettype none
module wht_8_cfl1994_p_w16 (
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
    reg  signed [15:0] x0_r1;
    reg  signed [15:0] x0_r2;
    reg  signed [15:0] x1_r1;
    reg  signed [15:0] x1_r2;
    reg  signed [15:0] x1_r3;
    reg  signed [15:0] x2_r1;
    reg  signed [15:0] x2_r2;
    reg  signed [15:0] x2_r3;
    reg  signed [15:0] x3_r1;
    reg  signed [15:0] x3_r2;
    reg  signed [15:0] x3_r3;
    reg  signed [15:0] x4_r1;
    reg  signed [15:0] x4_r2;
    reg  signed [15:0] x5_r1;
    reg  signed [15:0] x5_r2;
    reg  signed [15:0] x5_r3;
    reg  signed [15:0] x6_r1;
    reg  signed [15:0] x6_r2;
    reg  signed [15:0] x6_r3;
    reg  signed [15:0] x7_r1;
    reg  signed [15:0] x7_r2;
    reg  signed [15:0] x7_r3;
    wire signed [16:0] n_t1 = x1 + x2;   // level 1, stage 1
    reg  signed [16:0] n_t1_r1;
    wire signed [17:0] n_t2 = n_t1_r1 + x3_r1;   // level 2, stage 2
    reg  signed [17:0] n_t2_r2;
    wire signed [17:0] n_t3 = x0_r2 - n_t2_r2;   // level 3, stage 3
    reg  signed [17:0] n_t3_r3;
    wire signed [17:0] n_t4 = x0_r2 + n_t2_r2;   // level 3, stage 3
    reg  signed [17:0] n_t4_r3;
    wire signed [17:0] n_t5 = n_t3_r3 + (x2_r3 <<< 1);   // level 4, stage 4
    reg  signed [17:0] n_t5_r4;
    wire signed [17:0] n_t6 = n_t3_r3 + (x1_r3 <<< 1);   // level 4, stage 4
    reg  signed [17:0] n_t6_r4;
    wire signed [17:0] n_t7 = n_t3_r3 + (x3_r3 <<< 1);   // level 4, stage 4
    reg  signed [17:0] n_t7_r4;
    wire signed [16:0] n_t8 = x5 + x6;   // level 1, stage 1
    reg  signed [16:0] n_t8_r1;
    wire signed [17:0] n_t9 = n_t8_r1 + x7_r1;   // level 2, stage 2
    reg  signed [17:0] n_t9_r2;
    wire signed [17:0] n_t10 = x4_r2 - n_t9_r2;   // level 3, stage 3
    reg  signed [17:0] n_t10_r3;
    wire signed [17:0] n_t11 = x4_r2 + n_t9_r2;   // level 3, stage 3
    reg  signed [17:0] n_t11_r3;
    wire signed [17:0] n_t12 = n_t10_r3 + (x6_r3 <<< 1);   // level 4, stage 4
    reg  signed [17:0] n_t12_r4;
    wire signed [17:0] n_t13 = n_t10_r3 + (x5_r3 <<< 1);   // level 4, stage 4
    reg  signed [17:0] n_t13_r4;
    wire signed [17:0] n_t14 = n_t10_r3 + (x7_r3 <<< 1);   // level 4, stage 4
    reg  signed [17:0] n_t14_r4;
    wire signed [18:0] n_t15 = n_t4_r3 + n_t11_r3;   // level 4, stage 4
    reg  signed [18:0] n_t15_r4;
    reg  signed [18:0] n_t15_r5;
    wire signed [18:0] n_t16 = n_t4_r3 - n_t11_r3;   // level 4, stage 4
    reg  signed [18:0] n_t16_r4;
    reg  signed [18:0] n_t16_r5;
    wire signed [18:0] n_t17 = n_t5_r4 + n_t12_r4;   // level 5, stage 5
    reg  signed [18:0] n_t17_r5;
    wire signed [18:0] n_t18 = n_t5_r4 - n_t12_r4;   // level 5, stage 5
    reg  signed [18:0] n_t18_r5;
    wire signed [18:0] n_t19 = n_t6_r4 + n_t13_r4;   // level 5, stage 5
    reg  signed [18:0] n_t19_r5;
    wire signed [18:0] n_t20 = n_t6_r4 - n_t13_r4;   // level 5, stage 5
    reg  signed [18:0] n_t20_r5;
    wire signed [18:0] n_t21 = n_t7_r4 + n_t14_r4;   // level 5, stage 5
    reg  signed [18:0] n_t21_r5;
    wire signed [18:0] n_t22 = n_t7_r4 - n_t14_r4;   // level 5, stage 5
    reg  signed [18:0] n_t22_r5;
    wire signed [18:0] o0 = n_t15_r5;
    wire signed [18:0] o1 = n_t17_r5;
    wire signed [18:0] o2 = n_t19_r5;
    wire signed [18:0] o3 = n_t21_r5;
    wire signed [18:0] o4 = n_t16_r5;
    wire signed [18:0] o5 = n_t18_r5;
    wire signed [18:0] o6 = n_t20_r5;
    wire signed [18:0] o7 = n_t22_r5;
    assign out_data = {
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    reg  [4:0] vld = 5'd0;
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
        x3_r3 <= x3_r2;
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
        x7_r3 <= x7_r2;
        n_t1_r1 <= n_t1;
        n_t2_r2 <= n_t2;
        n_t3_r3 <= n_t3;
        n_t4_r3 <= n_t4;
        n_t5_r4 <= n_t5;
        n_t6_r4 <= n_t6;
        n_t7_r4 <= n_t7;
        n_t8_r1 <= n_t8;
        n_t9_r2 <= n_t9;
        n_t10_r3 <= n_t10;
        n_t11_r3 <= n_t11;
        n_t12_r4 <= n_t12;
        n_t13_r4 <= n_t13;
        n_t14_r4 <= n_t14;
        n_t15_r4 <= n_t15;
        n_t15_r5 <= n_t15_r4;
        n_t16_r4 <= n_t16;
        n_t16_r5 <= n_t16_r4;
        n_t17_r5 <= n_t17;
        n_t18_r5 <= n_t18;
        n_t19_r5 <= n_t19;
        n_t20_r5 <= n_t20;
        n_t21_r5 <= n_t21;
        n_t22_r5 <= n_t22;
        vld <= {vld[3:0], in_valid};
    end
    assign out_valid = vld[4];
endmodule
`default_nettype wire
