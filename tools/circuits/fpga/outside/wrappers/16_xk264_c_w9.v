// Thin wrapper written for the FPGA check.  Written by make_wrappers.py.
// It instantiates, unchanged, the module intra_hadamard4x4 of the open H.264 encoder xk264
// (file rtl/intra/intra_hadamard4x4.v, commit b59222e67fb77917a3afe97941c9a25b2b3a41f9).
// That module is the textbook 4 x 4 transform: 8 four-point butterflies of 8 adders, 64 adders.
// A 4 x 4 two-dimensional Hadamard transform is the 16-point transform: x_{4r+c} is row r, column c.
// The core writes a - b as a + (~b + 1); whether a tool folds that into one subtractor is the tool's affair.
// Inputs: 16 signed values of 9 bits (the width is fixed in the core).  Outputs: 16 signed values of 13 bits.
// Variant c: combinational.  Latency 0.  clk is not used.
module wht_16_xk264_c_w9 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [143:0] in_data,
    output wire                 out_valid,
    output wire [207:0] out_data
);
    wire [143:0] x_bus = in_data;
    wire [207:0] y_bus;
    intra_hadamard4x4 core (
        .ht_s00_i(x_bus[8:0]),
        .ht_s01_i(x_bus[17:9]),
        .ht_s02_i(x_bus[26:18]),
        .ht_s03_i(x_bus[35:27]),
        .ht_s10_i(x_bus[44:36]),
        .ht_s11_i(x_bus[53:45]),
        .ht_s12_i(x_bus[62:54]),
        .ht_s13_i(x_bus[71:63]),
        .ht_s20_i(x_bus[80:72]),
        .ht_s21_i(x_bus[89:81]),
        .ht_s22_i(x_bus[98:90]),
        .ht_s23_i(x_bus[107:99]),
        .ht_s30_i(x_bus[116:108]),
        .ht_s31_i(x_bus[125:117]),
        .ht_s32_i(x_bus[134:126]),
        .ht_s33_i(x_bus[143:135]),
        .ht_d00_o(y_bus[12:0]),
        .ht_d01_o(y_bus[25:13]),
        .ht_d02_o(y_bus[38:26]),
        .ht_d03_o(y_bus[51:39]),
        .ht_d10_o(y_bus[64:52]),
        .ht_d11_o(y_bus[77:65]),
        .ht_d12_o(y_bus[90:78]),
        .ht_d13_o(y_bus[103:91]),
        .ht_d20_o(y_bus[116:104]),
        .ht_d21_o(y_bus[129:117]),
        .ht_d22_o(y_bus[142:130]),
        .ht_d23_o(y_bus[155:143]),
        .ht_d30_o(y_bus[168:156]),
        .ht_d31_o(y_bus[181:169]),
        .ht_d32_o(y_bus[194:182]),
        .ht_d33_o(y_bus[207:195])
    );
    assign out_data = y_bus;
    assign out_valid = in_valid;
endmodule
