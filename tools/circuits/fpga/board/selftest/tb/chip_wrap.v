// Wrapper that gives the netlist decoded from the image (module "chip") the port list of selftest_top.
`default_nettype none
module chip_wrap (input wire clk, output wire [7:0] led, output wire uart_tx);
    chip u (.clk(clk), .\led[0] (led[0]), .\led[1] (led[1]), .\led[2] (led[2]), .\led[3] (led[3]),
            .\led[4] (led[4]), .\led[5] (led[5]), .\led[6] (led[6]), .\led[7] (led[7]), .uart_tx(uart_tx));
endmodule
`default_nettype wire
