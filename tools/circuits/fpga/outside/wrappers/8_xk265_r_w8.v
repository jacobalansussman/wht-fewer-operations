// Thin wrapper written for the FPGA check.  Written by make_wrappers.py.
// It instantiates, unchanged, the module hadamard_trans_1d of the open HEVC encoder xk265
// (file rtl/fme/fme_satd_8x8.v, commit 832e564a8e59dd90a18fb7ee8e2ed87d96aa03bc).
// That module is the textbook network: 3 layers of 8 additions or subtractions, 24 adders.
// Inputs: 8 signed values of 8 bits.  Outputs: 8 signed values of 11 bits.
// Variant r: one register stage at the inputs, 1 at the outputs, nothing between.  Latency 2.
module wht_8_xk265_r_w8 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [63:0] in_data,
    output wire                 out_valid,
    output wire [87:0] out_data
);
    reg  [63:0] x_bus;
    wire [87:0] y_bus;
    reg  [87:0] out_q1;
    reg  [1:0] vld = 2'd0;
    always @(posedge clk) begin
        x_bus <= in_data;
        out_q1 <= y_bus;
        vld <= {vld[0:0], in_valid};
    end
    hadamard_trans_1d #(.DATA_WIDTH(8)) core (
        .idata_0(x_bus[7:0]),
        .idata_1(x_bus[15:8]),
        .idata_2(x_bus[23:16]),
        .idata_3(x_bus[31:24]),
        .idata_4(x_bus[39:32]),
        .idata_5(x_bus[47:40]),
        .idata_6(x_bus[55:48]),
        .idata_7(x_bus[63:56]),
        .odata_0(y_bus[10:0]),
        .odata_1(y_bus[21:11]),
        .odata_2(y_bus[32:22]),
        .odata_3(y_bus[43:33]),
        .odata_4(y_bus[54:44]),
        .odata_5(y_bus[65:55]),
        .odata_6(y_bus[76:66]),
        .odata_7(y_bus[87:77])
    );
    assign out_data = out_q1;
    assign out_valid = vld[1];
endmodule
