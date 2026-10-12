// Test bench.  Compares a wrapped core with the definition
//   y_J = sum over i of (-1)^popcount(J & i) * x_i
// on 4*N corner vectors (for every output J: the inputs that make y_J largest and smallest,
// and the same with one step inside the range) and on `NRAND random vectors.
// Give on the command line: -DDUT=<module> -DDUTNAME='"<module>"' -DN=<points> -DW=<input bits> -DLAT=<latency in clocks>
`timescale 1ns/1ps
`ifndef NRAND
`define NRAND 20000
`endif
module tb;
    localparam N  = `N;
    localparam W  = `W;
    localparam LG = $clog2(N);
    localparam WO = W + LG;
    reg clk = 0;
    reg in_valid = 1;
    reg  [N*W-1:0]  in_data = 0;
    wire            out_valid;
    wire [N*WO-1:0] out_data;
    `DUT dut (.clk(clk), .in_valid(in_valid), .in_data(in_data), .out_valid(out_valid), .out_data(out_data));
    always #5 clk = ~clk;

    integer errors = 0, vectors = 0, seed = 20261011;
    integer i, j, k, t;
    reg signed [31:0] acc;
    reg signed [W-1:0]  xi;
    reg signed [WO-1:0] yj;
    reg signed [W-1:0]  vmax, vmin;

    function parity(input integer v);
        integer b; begin parity = 0; for (b = 0; b < 16; b = b + 1) parity = parity ^ v[b]; end
    endfunction

    task settle_and_check;
        begin
            if (`LAT == 0) #1; else begin repeat (`LAT) @(posedge clk); #1; end
            for (j = 0; j < N; j = j + 1) begin
                acc = 0;
                for (i = 0; i < N; i = i + 1) begin
                    xi = in_data[W*i +: W];
                    if (parity(j & i)) acc = acc - xi; else acc = acc + xi;
                end
                yj = out_data[WO*j +: WO];
                if (yj !== acc) begin
                    errors = errors + 1;
                    if (errors <= 5) $display("MISMATCH vector %0d output %0d: got %0d, want %0d", vectors, j, yj, acc);
                end
            end
            vectors = vectors + 1;
            @(negedge clk);
        end
    endtask

    initial begin
        vmax = {1'b0, {(W-1){1'b1}}};
        vmin = {1'b1, {(W-1){1'b0}}};
        @(negedge clk);
        for (k = 0; k < N; k = k + 1) begin
            for (t = 0; t < 4; t = t + 1) begin
                for (i = 0; i < N; i = i + 1) begin
                    // t=0: y_k largest; t=1: y_k smallest; t=2,3: the same, one step inside the range
                    if (parity(k & i) ^ t[0]) in_data[W*i +: W] = (t[1] ? vmin + 1 : vmin);
                    else                      in_data[W*i +: W] = (t[1] ? vmax - 1 : vmax);
                end
                settle_and_check;
            end
        end
        for (k = 0; k < `NRAND; k = k + 1) begin
            for (i = 0; i < N; i = i + 1) in_data[W*i +: W] = $random(seed);
            settle_and_check;
        end
        if (errors == 0) $display("PASS dut=%0s N=%0d W=%0d latency=%0d vectors=%0d", `DUTNAME, N, W, `LAT, vectors);
        else             $display("FAIL dut=%0s errors=%0d of %0d vectors", `DUTNAME, errors, vectors);
        $finish;
    end
endmodule
