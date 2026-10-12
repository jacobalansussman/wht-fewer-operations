// Written by gen_rtl.py.  Do not edit by hand.
// 8-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/fpga/rtl/circuits/8_cfl1994.txt
// Coppersmith, Feig, Linzer (1994): two 4-point circuits of 7, then one plain layer of 8.  22 adders.
// Inputs: 8 signed values of 12 bits.  Outputs: 8 signed values of 15 bits.
// Adders 22, depth 5 adder levels, adder bits 314 (chain bits 308).
// Variant r: one register stage at the inputs, 1 at the outputs, nothing between.  Latency 2.
// Register bits: 96 at the inputs, 120 at the outputs, 2 valid bits.
`default_nettype none
module wht_8_cfl1994_r_w12 (
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
    wire signed [12:0] n_t1 = x1 + x2;   // level 1
    wire signed [13:0] n_t2 = n_t1 + x3;   // level 2
    wire signed [13:0] n_t3 = x0 - n_t2;   // level 3
    wire signed [13:0] n_t4 = x0 + n_t2;   // level 3
    wire signed [13:0] n_t5 = n_t3 + (x2 <<< 1);   // level 4
    wire signed [13:0] n_t6 = n_t3 + (x1 <<< 1);   // level 4
    wire signed [13:0] n_t7 = n_t3 + (x3 <<< 1);   // level 4
    wire signed [12:0] n_t8 = x5 + x6;   // level 1
    wire signed [13:0] n_t9 = n_t8 + x7;   // level 2
    wire signed [13:0] n_t10 = x4 - n_t9;   // level 3
    wire signed [13:0] n_t11 = x4 + n_t9;   // level 3
    wire signed [13:0] n_t12 = n_t10 + (x6 <<< 1);   // level 4
    wire signed [13:0] n_t13 = n_t10 + (x5 <<< 1);   // level 4
    wire signed [13:0] n_t14 = n_t10 + (x7 <<< 1);   // level 4
    wire signed [14:0] n_t15 = n_t4 + n_t11;   // level 4
    wire signed [14:0] n_t16 = n_t4 - n_t11;   // level 4
    wire signed [14:0] n_t17 = n_t5 + n_t12;   // level 5
    wire signed [14:0] n_t18 = n_t5 - n_t12;   // level 5
    wire signed [14:0] n_t19 = n_t6 + n_t13;   // level 5
    wire signed [14:0] n_t20 = n_t6 - n_t13;   // level 5
    wire signed [14:0] n_t21 = n_t7 + n_t14;   // level 5
    wire signed [14:0] n_t22 = n_t7 - n_t14;   // level 5
    wire signed [14:0] o0 = n_t15;
    wire signed [14:0] o1 = n_t17;
    wire signed [14:0] o2 = n_t19;
    wire signed [14:0] o3 = n_t21;
    wire signed [14:0] o4 = n_t16;
    wire signed [14:0] o5 = n_t18;
    wire signed [14:0] o6 = n_t20;
    wire signed [14:0] o7 = n_t22;
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
