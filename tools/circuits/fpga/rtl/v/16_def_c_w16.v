// Written by gen_rtl.py.  Do not edit by hand.
// 16-point Walsh-Hadamard transform written from the definition:
// y_J = sum over i of (-1)^popcount(J & i) * x_i, one expression per output, 20 bits.
// A reference for the equivalence proofs; not a design to be measured.
`default_nettype none
module wht_16_def_c_w16 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [255:0] in_data,
    output wire                 out_valid,
    output wire [319:0] out_data
);
    wire signed [19:0] x0 = $signed(in_data[15:0]);
    wire signed [19:0] x1 = $signed(in_data[31:16]);
    wire signed [19:0] x2 = $signed(in_data[47:32]);
    wire signed [19:0] x3 = $signed(in_data[63:48]);
    wire signed [19:0] x4 = $signed(in_data[79:64]);
    wire signed [19:0] x5 = $signed(in_data[95:80]);
    wire signed [19:0] x6 = $signed(in_data[111:96]);
    wire signed [19:0] x7 = $signed(in_data[127:112]);
    wire signed [19:0] x8 = $signed(in_data[143:128]);
    wire signed [19:0] x9 = $signed(in_data[159:144]);
    wire signed [19:0] x10 = $signed(in_data[175:160]);
    wire signed [19:0] x11 = $signed(in_data[191:176]);
    wire signed [19:0] x12 = $signed(in_data[207:192]);
    wire signed [19:0] x13 = $signed(in_data[223:208]);
    wire signed [19:0] x14 = $signed(in_data[239:224]);
    wire signed [19:0] x15 = $signed(in_data[255:240]);
    wire signed [19:0] o0 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15;
    wire signed [19:0] o1 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 + x8 - x9 + x10 - x11 + x12 - x13 + x14 - x15;
    wire signed [19:0] o2 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 + x8 + x9 - x10 - x11 + x12 + x13 - x14 - x15;
    wire signed [19:0] o3 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 + x8 - x9 - x10 + x11 + x12 - x13 - x14 + x15;
    wire signed [19:0] o4 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 + x8 + x9 + x10 + x11 - x12 - x13 - x14 - x15;
    wire signed [19:0] o5 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 + x8 - x9 + x10 - x11 - x12 + x13 - x14 + x15;
    wire signed [19:0] o6 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 + x8 + x9 - x10 - x11 - x12 - x13 + x14 + x15;
    wire signed [19:0] o7 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 + x8 - x9 - x10 + x11 - x12 + x13 + x14 - x15;
    wire signed [19:0] o8 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 - x8 - x9 - x10 - x11 - x12 - x13 - x14 - x15;
    wire signed [19:0] o9 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 - x8 + x9 - x10 + x11 - x12 + x13 - x14 + x15;
    wire signed [19:0] o10 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 - x8 - x9 + x10 + x11 - x12 - x13 + x14 + x15;
    wire signed [19:0] o11 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 - x8 + x9 + x10 - x11 - x12 + x13 + x14 - x15;
    wire signed [19:0] o12 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 - x8 - x9 - x10 - x11 + x12 + x13 + x14 + x15;
    wire signed [19:0] o13 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 - x8 + x9 - x10 + x11 + x12 - x13 + x14 - x15;
    wire signed [19:0] o14 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 - x8 - x9 + x10 + x11 + x12 + x13 - x14 - x15;
    wire signed [19:0] o15 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 - x8 + x9 + x10 - x11 + x12 - x13 - x14 + x15;
    assign out_data = {
        o15, o14, o13, o12, o11, o10, o9, o8,
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    assign out_valid = in_valid;
    wire _unused_clk = clk;
endmodule
`default_nettype wire
