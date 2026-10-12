// Thin wrapper written for the FPGA check.  Written by make_wrappers.py.
// It instantiates, unchanged, the module hadamard_trans_1d of the open HEVC encoder xk265
// (file rtl/fme/fme_satd_8x8.v, commit 832e564a8e59dd90a18fb7ee8e2ed87d96aa03bc).
// That module is the textbook network: 3 layers of 8 additions or subtractions, 24 adders.
// Inputs: 8 signed values of 9 bits.  Outputs: 8 signed values of 12 bits.
// Variant c: combinational.  Latency 0.  clk is not used.
module wht_8_xk265_c_w9 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [71:0] in_data,
    output wire                 out_valid,
    output wire [95:0] out_data
);
    wire [71:0] x_bus = in_data;
    wire [95:0] y_bus;
    hadamard_trans_1d #(.DATA_WIDTH(9)) core (
        .idata_0(x_bus[8:0]),
        .idata_1(x_bus[17:9]),
        .idata_2(x_bus[26:18]),
        .idata_3(x_bus[35:27]),
        .idata_4(x_bus[44:36]),
        .idata_5(x_bus[53:45]),
        .idata_6(x_bus[62:54]),
        .idata_7(x_bus[71:63]),
        .odata_0(y_bus[11:0]),
        .odata_1(y_bus[23:12]),
        .odata_2(y_bus[35:24]),
        .odata_3(y_bus[47:36]),
        .odata_4(y_bus[59:48]),
        .odata_5(y_bus[71:60]),
        .odata_6(y_bus[83:72]),
        .odata_7(y_bus[95:84])
    );
    assign out_data = y_bus;
    assign out_valid = in_valid;
endmodule
