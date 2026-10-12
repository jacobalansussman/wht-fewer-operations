// Test bench for selftest_top: a 12 MHz clock, and a serial receiver that samples the transmit pin
// at 115,200 baud by its own clock (nanoseconds, not the design's divider), so the baud rate of the
// design is checked too.  Received bytes go to the file given by +out=<file>; LED states and
// framing errors go to the log.
//   +clocks=<n>   stop after n clocks
//   +out=<file>   file for the received bytes
`timescale 1ns/1ps
`default_nettype none
module tb_top;
    parameter integer PPS = 375;
    parameter real HALF = 41.6665;            // 12 MHz: period 83.333 ns
    parameter real BIT  = 8680.5556;          // 115,200 baud

    reg clk = 1'b0;
    always #(HALF) clk = ~clk;

    wire [7:0] led;
    wire       tx;
`ifdef CHIP
    // the netlist that icebox_vlog decodes from the packed image (module "chip", one port per pin)
    chip dut (.clk(clk), .\led[0] (led[0]), .\led[1] (led[1]), .\led[2] (led[2]), .\led[3] (led[3]),
              .\led[4] (led[4]), .\led[5] (led[5]), .\led[6] (led[6]), .\led[7] (led[7]), .uart_tx(tx));
`elsif GATE
    // the netlist yosys wrote after synthesis (parameters are fixed in it)
    selftest_top dut (.clk(clk), .led(led), .uart_tx(tx));
`else
    selftest_top #(.PPS(PPS)) dut (.clk(clk), .led(led), .uart_tx(tx));
`endif

    integer nclk = 2000000;
    integer fd;
    reg [1023:0] outname;
    integer cyc = 0;
    integer nbytes = 0, nlines = 0, frame_err = 0, x_seen = 0;
    reg [7:0] rxb;
    integer i;

    initial begin
        if (!$value$plusargs("clocks=%d", nclk)) nclk = 2000000;
        if (!$value$plusargs("out=%s", outname)) outname = "uart.bin";
        fd = $fopen(outname, "wb");
        if (fd == 0) begin $display("cannot open output file"); $finish; end
    end

    always @(posedge clk) begin
        cyc <= cyc + 1;
        if (cyc > 200 && (tx === 1'bx || tx === 1'bz || ^led === 1'bx)) x_seen <= x_seen + 1;
        if (cyc == nclk) begin
            $display("END clocks=%0d bytes=%0d lines=%0d framing_errors=%0d undefined_pin_samples=%0d led=%b",
                     cyc, nbytes, nlines, frame_err, x_seen, led);
            $fclose(fd);
            $finish;
        end
    end

    // serial receiver
    initial begin
        #1000;
        forever begin
            @(negedge tx);
            #(BIT * 0.5);
            if (tx !== 1'b0) begin frame_err = frame_err + 1; $display("FRAMING start bit at %0t", $time); end
            for (i = 0; i < 8; i = i + 1) begin
                #(BIT);
                rxb[i] = tx;
            end
            #(BIT);
            if (tx !== 1'b1) begin frame_err = frame_err + 1; $display("FRAMING stop bit at %0t", $time); end
            $fwrite(fd, "%c", rxb);
            nbytes = nbytes + 1;
            if (rxb == 8'h0A) begin
                nlines = nlines + 1;
                $display("LINE %0d complete at clock %0d, led=%b", nlines, cyc, led);
            end
        end
    end
endmodule
`default_nettype wire
