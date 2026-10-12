// Written by gen_rtl.py.  Do not edit by hand.
// 8-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/programs/generated/O_textbook_8.txt
// The textbook: 3 layers of 4 butterflies (a+b, a-b).  24 adders.
// Inputs: 8 signed values of 16 bits.  Outputs: 8 signed values of 19 bits.
// Adders 24, depth 3 adder levels, adder bits 432 (chain bits 432).
// Variant c: combinational.  Latency 0.  clk is not used.
`default_nettype none
module wht_8_textbook_c_w16 (
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
    wire signed [16:0] n_t1 = x0 + x1;   // level 1
    wire signed [16:0] n_t2 = x0 - x1;   // level 1
    wire signed [16:0] n_t3 = x2 + x3;   // level 1
    wire signed [16:0] n_t4 = x2 - x3;   // level 1
    wire signed [16:0] n_t5 = x4 + x5;   // level 1
    wire signed [16:0] n_t6 = x4 - x5;   // level 1
    wire signed [16:0] n_t7 = x6 + x7;   // level 1
    wire signed [16:0] n_t8 = x6 - x7;   // level 1
    wire signed [17:0] n_t9 = n_t1 + n_t3;   // level 2
    wire signed [17:0] n_t10 = n_t1 - n_t3;   // level 2
    wire signed [17:0] n_t11 = n_t2 + n_t4;   // level 2
    wire signed [17:0] n_t12 = n_t2 - n_t4;   // level 2
    wire signed [17:0] n_t13 = n_t5 + n_t7;   // level 2
    wire signed [17:0] n_t14 = n_t5 - n_t7;   // level 2
    wire signed [17:0] n_t15 = n_t6 + n_t8;   // level 2
    wire signed [17:0] n_t16 = n_t6 - n_t8;   // level 2
    wire signed [18:0] n_t17 = n_t9 + n_t13;   // level 3
    wire signed [18:0] n_t18 = n_t9 - n_t13;   // level 3
    wire signed [18:0] n_t19 = n_t11 + n_t15;   // level 3
    wire signed [18:0] n_t20 = n_t11 - n_t15;   // level 3
    wire signed [18:0] n_t21 = n_t10 + n_t14;   // level 3
    wire signed [18:0] n_t22 = n_t10 - n_t14;   // level 3
    wire signed [18:0] n_t23 = n_t12 + n_t16;   // level 3
    wire signed [18:0] n_t24 = n_t12 - n_t16;   // level 3
    wire signed [18:0] o0 = n_t17;
    wire signed [18:0] o1 = n_t19;
    wire signed [18:0] o2 = n_t21;
    wire signed [18:0] o3 = n_t23;
    wire signed [18:0] o4 = n_t18;
    wire signed [18:0] o5 = n_t20;
    wire signed [18:0] o6 = n_t22;
    wire signed [18:0] o7 = n_t24;
    assign out_data = {
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    assign out_valid = in_valid;
    wire _unused_clk = clk;
endmodule
`default_nettype wire
