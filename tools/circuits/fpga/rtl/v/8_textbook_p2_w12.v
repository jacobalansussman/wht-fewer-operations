// Written by gen_rtl.py.  Do not edit by hand.
// 8-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/programs/generated/O_textbook_8.txt
// The textbook: 3 layers of 4 butterflies (a+b, a-b).  24 adders.
// Inputs: 8 signed values of 12 bits.  Outputs: 8 signed values of 15 bits.
// Adders 24, depth 3 adder levels, adder bits 336 (chain bits 336).
// Variant p2: a register after every second adder level.  Latency 2.
// Register bits: 232 after adders, 0 in delay registers, 2 valid bits.
`default_nettype none
module wht_8_textbook_p2_w12 (
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
    wire signed [12:0] n_t1 = x0 + x1;   // level 1, stage 1
    wire signed [12:0] n_t2 = x0 - x1;   // level 1, stage 1
    wire signed [12:0] n_t3 = x2 + x3;   // level 1, stage 1
    wire signed [12:0] n_t4 = x2 - x3;   // level 1, stage 1
    wire signed [12:0] n_t5 = x4 + x5;   // level 1, stage 1
    wire signed [12:0] n_t6 = x4 - x5;   // level 1, stage 1
    wire signed [12:0] n_t7 = x6 + x7;   // level 1, stage 1
    wire signed [12:0] n_t8 = x6 - x7;   // level 1, stage 1
    wire signed [13:0] n_t9 = n_t1 + n_t3;   // level 2, stage 1
    reg  signed [13:0] n_t9_r1;
    wire signed [13:0] n_t10 = n_t1 - n_t3;   // level 2, stage 1
    reg  signed [13:0] n_t10_r1;
    wire signed [13:0] n_t11 = n_t2 + n_t4;   // level 2, stage 1
    reg  signed [13:0] n_t11_r1;
    wire signed [13:0] n_t12 = n_t2 - n_t4;   // level 2, stage 1
    reg  signed [13:0] n_t12_r1;
    wire signed [13:0] n_t13 = n_t5 + n_t7;   // level 2, stage 1
    reg  signed [13:0] n_t13_r1;
    wire signed [13:0] n_t14 = n_t5 - n_t7;   // level 2, stage 1
    reg  signed [13:0] n_t14_r1;
    wire signed [13:0] n_t15 = n_t6 + n_t8;   // level 2, stage 1
    reg  signed [13:0] n_t15_r1;
    wire signed [13:0] n_t16 = n_t6 - n_t8;   // level 2, stage 1
    reg  signed [13:0] n_t16_r1;
    wire signed [14:0] n_t17 = n_t9_r1 + n_t13_r1;   // level 3, stage 2
    reg  signed [14:0] n_t17_r2;
    wire signed [14:0] n_t18 = n_t9_r1 - n_t13_r1;   // level 3, stage 2
    reg  signed [14:0] n_t18_r2;
    wire signed [14:0] n_t19 = n_t11_r1 + n_t15_r1;   // level 3, stage 2
    reg  signed [14:0] n_t19_r2;
    wire signed [14:0] n_t20 = n_t11_r1 - n_t15_r1;   // level 3, stage 2
    reg  signed [14:0] n_t20_r2;
    wire signed [14:0] n_t21 = n_t10_r1 + n_t14_r1;   // level 3, stage 2
    reg  signed [14:0] n_t21_r2;
    wire signed [14:0] n_t22 = n_t10_r1 - n_t14_r1;   // level 3, stage 2
    reg  signed [14:0] n_t22_r2;
    wire signed [14:0] n_t23 = n_t12_r1 + n_t16_r1;   // level 3, stage 2
    reg  signed [14:0] n_t23_r2;
    wire signed [14:0] n_t24 = n_t12_r1 - n_t16_r1;   // level 3, stage 2
    reg  signed [14:0] n_t24_r2;
    wire signed [14:0] o0 = n_t17_r2;
    wire signed [14:0] o1 = n_t19_r2;
    wire signed [14:0] o2 = n_t21_r2;
    wire signed [14:0] o3 = n_t23_r2;
    wire signed [14:0] o4 = n_t18_r2;
    wire signed [14:0] o5 = n_t20_r2;
    wire signed [14:0] o6 = n_t22_r2;
    wire signed [14:0] o7 = n_t24_r2;
    assign out_data = {
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    reg  [1:0] vld = 2'd0;
    always @(posedge clk) begin
        n_t9_r1 <= n_t9;
        n_t10_r1 <= n_t10;
        n_t11_r1 <= n_t11;
        n_t12_r1 <= n_t12;
        n_t13_r1 <= n_t13;
        n_t14_r1 <= n_t14;
        n_t15_r1 <= n_t15;
        n_t16_r1 <= n_t16;
        n_t17_r2 <= n_t17;
        n_t18_r2 <= n_t18;
        n_t19_r2 <= n_t19;
        n_t20_r2 <= n_t20;
        n_t21_r2 <= n_t21;
        n_t22_r2 <= n_t22;
        n_t23_r2 <= n_t23;
        n_t24_r2 <= n_t24;
        vld <= {vld[0:0], in_valid};
    end
    assign out_valid = vld[1];
endmodule
`default_nettype wire
