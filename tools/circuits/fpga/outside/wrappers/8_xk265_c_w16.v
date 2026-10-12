// Thin wrapper written for the FPGA check.  Written by make_wrappers.py.
// It instantiates, unchanged, the module hadamard_trans_1d of the open HEVC encoder xk265
// (file rtl/fme/fme_satd_8x8.v, commit 832e564a8e59dd90a18fb7ee8e2ed87d96aa03bc).
// That module is the textbook network: 3 layers of 8 additions or subtractions, 24 adders.
// Inputs: 8 signed values of 16 bits.  Outputs: 8 signed values of 19 bits.
// Variant c: combinational.  Latency 0.  clk is not used.
module wht_8_xk265_c_w16 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [127:0] in_data,
    output wire                 out_valid,
    output wire [151:0] out_data
);
    wire [127:0] x_bus = in_data;
    wire [151:0] y_bus;
    hadamard_trans_1d #(.DATA_WIDTH(16)) core (
        .idata_0(x_bus[15:0]),
        .idata_1(x_bus[31:16]),
        .idata_2(x_bus[47:32]),
        .idata_3(x_bus[63:48]),
        .idata_4(x_bus[79:64]),
        .idata_5(x_bus[95:80]),
        .idata_6(x_bus[111:96]),
        .idata_7(x_bus[127:112]),
        .odata_0(y_bus[18:0]),
        .odata_1(y_bus[37:19]),
        .odata_2(y_bus[56:38]),
        .odata_3(y_bus[75:57]),
        .odata_4(y_bus[94:76]),
        .odata_5(y_bus[113:95]),
        .odata_6(y_bus[132:114]),
        .odata_7(y_bus[151:133])
    );
    assign out_data = y_bus;
    assign out_valid = in_valid;
endmodule
