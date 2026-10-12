// Written by gen_rtl.py.  Do not edit by hand.
// 8-point Walsh-Hadamard transform written from the definition:
// y_J = sum over i of (-1)^popcount(J & i) * x_i, one expression per output, 11 bits.
// A reference for the equivalence proofs; not a design to be measured.
`default_nettype none
module wht_8_def_c_w8 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [63:0] in_data,
    output wire                 out_valid,
    output wire [87:0] out_data
);
    wire signed [10:0] x0 = $signed(in_data[7:0]);
    wire signed [10:0] x1 = $signed(in_data[15:8]);
    wire signed [10:0] x2 = $signed(in_data[23:16]);
    wire signed [10:0] x3 = $signed(in_data[31:24]);
    wire signed [10:0] x4 = $signed(in_data[39:32]);
    wire signed [10:0] x5 = $signed(in_data[47:40]);
    wire signed [10:0] x6 = $signed(in_data[55:48]);
    wire signed [10:0] x7 = $signed(in_data[63:56]);
    wire signed [10:0] o0 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7;
    wire signed [10:0] o1 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7;
    wire signed [10:0] o2 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7;
    wire signed [10:0] o3 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7;
    wire signed [10:0] o4 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7;
    wire signed [10:0] o5 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7;
    wire signed [10:0] o6 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7;
    wire signed [10:0] o7 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7;
    assign out_data = {
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    assign out_valid = in_valid;
    wire _unused_clk = clk;
endmodule
`default_nettype wire
