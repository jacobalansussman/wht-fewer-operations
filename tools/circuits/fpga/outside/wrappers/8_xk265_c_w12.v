// Thin wrapper written for the FPGA check.  Written by make_wrappers.py.
// It instantiates, unchanged, the module hadamard_trans_1d of the open HEVC encoder xk265
// (file rtl/fme/fme_satd_8x8.v, commit 832e564a8e59dd90a18fb7ee8e2ed87d96aa03bc).
// That module is the textbook network: 3 layers of 8 additions or subtractions, 24 adders.
// Inputs: 8 signed values of 12 bits.  Outputs: 8 signed values of 15 bits.
// Variant c: combinational.  Latency 0.  clk is not used.
module wht_8_xk265_c_w12 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [95:0] in_data,
    output wire                 out_valid,
    output wire [119:0] out_data
);
    wire [95:0] x_bus = in_data;
    wire [119:0] y_bus;
    hadamard_trans_1d #(.DATA_WIDTH(12)) core (
        .idata_0(x_bus[11:0]),
        .idata_1(x_bus[23:12]),
        .idata_2(x_bus[35:24]),
        .idata_3(x_bus[47:36]),
        .idata_4(x_bus[59:48]),
        .idata_5(x_bus[71:60]),
        .idata_6(x_bus[83:72]),
        .idata_7(x_bus[95:84]),
        .odata_0(y_bus[14:0]),
        .odata_1(y_bus[29:15]),
        .odata_2(y_bus[44:30]),
        .odata_3(y_bus[59:45]),
        .odata_4(y_bus[74:60]),
        .odata_5(y_bus[89:75]),
        .odata_6(y_bus[104:90]),
        .odata_7(y_bus[119:105])
    );
    assign out_data = y_bus;
    assign out_valid = in_valid;
endmodule
