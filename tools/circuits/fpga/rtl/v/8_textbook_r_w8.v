// Written by gen_rtl.py.  Do not edit by hand.
// 8-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/programs/generated/O_textbook_8.txt
// The textbook: 3 layers of 4 butterflies (a+b, a-b).  24 adders.
// Inputs: 8 signed values of 8 bits.  Outputs: 8 signed values of 11 bits.
// Adders 24, depth 3 adder levels, adder bits 240 (chain bits 240).
// Variant r: one register stage at the inputs, 1 at the outputs, nothing between.  Latency 2.
// Register bits: 64 at the inputs, 88 at the outputs, 2 valid bits.
`default_nettype none
module wht_8_textbook_r_w8 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [63:0] in_data,
    output wire                 out_valid,
    output wire [87:0] out_data
);
    reg  signed [7:0] x0;
    reg  signed [7:0] x1;
    reg  signed [7:0] x2;
    reg  signed [7:0] x3;
    reg  signed [7:0] x4;
    reg  signed [7:0] x5;
    reg  signed [7:0] x6;
    reg  signed [7:0] x7;
    always @(posedge clk) begin
        x0 <= in_data[7:0];
        x1 <= in_data[15:8];
        x2 <= in_data[23:16];
        x3 <= in_data[31:24];
        x4 <= in_data[39:32];
        x5 <= in_data[47:40];
        x6 <= in_data[55:48];
        x7 <= in_data[63:56];
    end
    wire signed [8:0] n_t1 = x0 + x1;   // level 1
    wire signed [8:0] n_t2 = x0 - x1;   // level 1
    wire signed [8:0] n_t3 = x2 + x3;   // level 1
    wire signed [8:0] n_t4 = x2 - x3;   // level 1
    wire signed [8:0] n_t5 = x4 + x5;   // level 1
    wire signed [8:0] n_t6 = x4 - x5;   // level 1
    wire signed [8:0] n_t7 = x6 + x7;   // level 1
    wire signed [8:0] n_t8 = x6 - x7;   // level 1
    wire signed [9:0] n_t9 = n_t1 + n_t3;   // level 2
    wire signed [9:0] n_t10 = n_t1 - n_t3;   // level 2
    wire signed [9:0] n_t11 = n_t2 + n_t4;   // level 2
    wire signed [9:0] n_t12 = n_t2 - n_t4;   // level 2
    wire signed [9:0] n_t13 = n_t5 + n_t7;   // level 2
    wire signed [9:0] n_t14 = n_t5 - n_t7;   // level 2
    wire signed [9:0] n_t15 = n_t6 + n_t8;   // level 2
    wire signed [9:0] n_t16 = n_t6 - n_t8;   // level 2
    wire signed [10:0] n_t17 = n_t9 + n_t13;   // level 3
    wire signed [10:0] n_t18 = n_t9 - n_t13;   // level 3
    wire signed [10:0] n_t19 = n_t11 + n_t15;   // level 3
    wire signed [10:0] n_t20 = n_t11 - n_t15;   // level 3
    wire signed [10:0] n_t21 = n_t10 + n_t14;   // level 3
    wire signed [10:0] n_t22 = n_t10 - n_t14;   // level 3
    wire signed [10:0] n_t23 = n_t12 + n_t16;   // level 3
    wire signed [10:0] n_t24 = n_t12 - n_t16;   // level 3
    wire signed [10:0] o0 = n_t17;
    wire signed [10:0] o1 = n_t19;
    wire signed [10:0] o2 = n_t21;
    wire signed [10:0] o3 = n_t23;
    wire signed [10:0] o4 = n_t18;
    wire signed [10:0] o5 = n_t20;
    wire signed [10:0] o6 = n_t22;
    wire signed [10:0] o7 = n_t24;
    wire [87:0] out_comb = {
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    reg  [87:0] out_q1;
    reg  [1:0] vld = 2'd0;
    always @(posedge clk) begin
        out_q1 <= out_comb;
        vld <= {vld[0:0], in_valid};
    end
    assign out_data = out_q1;
    assign out_valid = vld[1];
endmodule
`default_nettype wire
