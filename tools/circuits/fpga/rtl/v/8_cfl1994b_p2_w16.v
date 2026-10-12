// Written by gen_rtl.py.  Do not edit by hand.
// 8-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/fpga/rtl/circuits/8_cfl1994b.txt
// Coppersmith, Feig, Linzer (1994), the other order: one plain layer of 8, then two 4-point circuits of 7.
// Inputs: 8 signed values of 16 bits.  Outputs: 8 signed values of 19 bits.
// Adders 22, depth 5 adder levels, adder bits 400 (chain bits 394).
// Variant p2: a register after every second adder level.  Latency 3.
// Register bits: 362 after adders, 140 in delay registers, 3 valid bits.
`default_nettype none
module wht_8_cfl1994b_p2_w16 (
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
    wire signed [16:0] n_t1 = x0 + x1;   // level 1, stage 1
    reg  signed [16:0] n_t1_r1;
    wire signed [16:0] n_t2 = x0 - x1;   // level 1, stage 1
    reg  signed [16:0] n_t2_r1;
    wire signed [16:0] n_t3 = x2 + x3;   // level 1, stage 1
    reg  signed [16:0] n_t3_r1;
    reg  signed [16:0] n_t3_r2;
    wire signed [16:0] n_t4 = x2 - x3;   // level 1, stage 1
    reg  signed [16:0] n_t4_r1;
    reg  signed [16:0] n_t4_r2;
    wire signed [16:0] n_t5 = x4 + x5;   // level 1, stage 1
    reg  signed [16:0] n_t5_r1;
    reg  signed [16:0] n_t5_r2;
    wire signed [16:0] n_t6 = x4 - x5;   // level 1, stage 1
    reg  signed [16:0] n_t6_r1;
    reg  signed [16:0] n_t6_r2;
    wire signed [16:0] n_t7 = x6 + x7;   // level 1, stage 1
    reg  signed [16:0] n_t7_r1;
    reg  signed [16:0] n_t7_r2;
    wire signed [16:0] n_t8 = x6 - x7;   // level 1, stage 1
    reg  signed [16:0] n_t8_r1;
    reg  signed [16:0] n_t8_r2;
    wire signed [17:0] n_t9 = n_t3 + n_t5;   // level 2, stage 1
    reg  signed [17:0] n_t9_r1;
    wire signed [18:0] n_t10 = n_t9_r1 + n_t7_r1;   // level 3, stage 2
    wire signed [18:0] n_t11 = n_t1_r1 - n_t10;   // level 4, stage 2
    reg  signed [18:0] n_t11_r2;
    wire signed [18:0] n_t12 = n_t1_r1 + n_t10;   // level 4, stage 2
    reg  signed [18:0] n_t12_r2;
    reg  signed [18:0] n_t12_r3;
    wire signed [18:0] n_t13 = n_t11_r2 + (n_t5_r2 <<< 1);   // level 5, stage 3
    reg  signed [18:0] n_t13_r3;
    wire signed [18:0] n_t14 = n_t11_r2 + (n_t3_r2 <<< 1);   // level 5, stage 3
    reg  signed [18:0] n_t14_r3;
    wire signed [18:0] n_t15 = n_t11_r2 + (n_t7_r2 <<< 1);   // level 5, stage 3
    reg  signed [18:0] n_t15_r3;
    wire signed [17:0] n_t16 = n_t4 + n_t6;   // level 2, stage 1
    reg  signed [17:0] n_t16_r1;
    wire signed [18:0] n_t17 = n_t16_r1 + n_t8_r1;   // level 3, stage 2
    wire signed [18:0] n_t18 = n_t2_r1 - n_t17;   // level 4, stage 2
    reg  signed [18:0] n_t18_r2;
    wire signed [18:0] n_t19 = n_t2_r1 + n_t17;   // level 4, stage 2
    reg  signed [18:0] n_t19_r2;
    reg  signed [18:0] n_t19_r3;
    wire signed [18:0] n_t20 = n_t18_r2 + (n_t6_r2 <<< 1);   // level 5, stage 3
    reg  signed [18:0] n_t20_r3;
    wire signed [18:0] n_t21 = n_t18_r2 + (n_t4_r2 <<< 1);   // level 5, stage 3
    reg  signed [18:0] n_t21_r3;
    wire signed [18:0] n_t22 = n_t18_r2 + (n_t8_r2 <<< 1);   // level 5, stage 3
    reg  signed [18:0] n_t22_r3;
    wire signed [18:0] o0 = n_t12_r3;
    wire signed [18:0] o1 = n_t19_r3;
    wire signed [18:0] o2 = n_t13_r3;
    wire signed [18:0] o3 = n_t20_r3;
    wire signed [18:0] o4 = n_t14_r3;
    wire signed [18:0] o5 = n_t21_r3;
    wire signed [18:0] o6 = n_t15_r3;
    wire signed [18:0] o7 = n_t22_r3;
    assign out_data = {
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    reg  [2:0] vld = 3'd0;
    always @(posedge clk) begin
        n_t1_r1 <= n_t1;
        n_t2_r1 <= n_t2;
        n_t3_r1 <= n_t3;
        n_t3_r2 <= n_t3_r1;
        n_t4_r1 <= n_t4;
        n_t4_r2 <= n_t4_r1;
        n_t5_r1 <= n_t5;
        n_t5_r2 <= n_t5_r1;
        n_t6_r1 <= n_t6;
        n_t6_r2 <= n_t6_r1;
        n_t7_r1 <= n_t7;
        n_t7_r2 <= n_t7_r1;
        n_t8_r1 <= n_t8;
        n_t8_r2 <= n_t8_r1;
        n_t9_r1 <= n_t9;
        n_t11_r2 <= n_t11;
        n_t12_r2 <= n_t12;
        n_t12_r3 <= n_t12_r2;
        n_t13_r3 <= n_t13;
        n_t14_r3 <= n_t14;
        n_t15_r3 <= n_t15;
        n_t16_r1 <= n_t16;
        n_t18_r2 <= n_t18;
        n_t19_r2 <= n_t19;
        n_t19_r3 <= n_t19_r2;
        n_t20_r3 <= n_t20;
        n_t21_r3 <= n_t21;
        n_t22_r3 <= n_t22;
        vld <= {vld[1:0], in_valid};
    end
    assign out_valid = vld[2];
endmodule
`default_nettype wire
