// Self-test image for the Lattice iCE40-HX8K breakout board (iCE40HX8K, package CT256).
//
// One pseudo-random source feeds the same 8-point input vectors (12-bit signed) to
//   u_ref  the textbook transform, 24 adders, pipelined, latency 3   (rtl/8_textbook_p_w12.v)
//   u_dut  the 19-adder transform, pipelined, latency 6              (rtl/8_ours_p_w12.v)
//   u_ctl  a deliberately broken copy of the 19-adder transform      (rtl/8_broken_p_w12.v)
// The textbook outputs are delayed by three clocks so that all three arrive together.  A comparator
// counts vectors and mismatches and keeps two checksums.  One text line a second goes out on the
// serial port.  The Python model of all of it is ../expected.py; read its header for the details.
//
// Pins: clk (input), led[7:0] (outputs), uart_tx (output).  Nothing else.
//   led[0]  heartbeat: lit during the first half of every second
//   led[1]  pass: at the last report there was no mismatch, both checksums agreed, and the broken
//           copy had been caught
//   led[2]  fail: a mismatch or a checksum disagreement has occurred (stays lit)
//   led[3]  the broken copy has been caught at least once (expected: lit)
//   led[7:4] always off
//
// No reset pin: every register that matters starts at 0 after configuration, and a counter holds
// the design in reset for the first 128 clocks.
`default_nettype none
module selftest_top #(
    parameter integer PERIOD   = 32000,  // clocks per period
    parameter integer BURST    = 2000,   // input vectors at the start of every period
    parameter integer CORNER   = 256,    // of these, the first CORNER are extreme-value vectors
    parameter integer PPS      = 375,    // periods per report: 375 * 32000 = 12,000,000 clocks = 1 s
    parameter integer BAUD_DIV = 104     // clocks per serial bit: 12 MHz / 104 = 115,384.6 baud
) (
    input  wire       clk,
    output wire [7:0] led,
    output wire       uart_tx
);
    localparam integer N   = 8;
    localparam integer W   = 12;
    localparam integer OW  = 15;
    localparam integer IW  = N * W;      // 96
    localparam integer BW  = N * OW;     // 120
    localparam integer DLY = 3;          // latency of the 19-adder transform minus that of the textbook
`include "selftest_params.vh"

    // ---------------------------------------------------------------- start-up reset
    reg [7:0] porc = 8'd0;
    wire rst = ~porc[7];
    always @(posedge clk) if (rst) porc <= porc + 8'd1;

    // ---------------------------------------------------------------- time base
    reg [14:0] ph   = 15'd0;             // clock within the period
    reg [8:0]  per  = 9'd0;              // period within the second
    reg [15:0] secs = 16'd0;             // seconds finished
    wire ph_last  = (ph == PERIOD - 1);
    wire per_last = (per == PPS - 1);
    always @(posedge clk) begin
        if (rst) begin
            ph <= 15'd0; per <= 9'd0; secs <= 16'd0;
        end else begin
            ph <= ph_last ? 15'd0 : ph + 15'd1;
            if (ph_last) begin
                per <= per_last ? 9'd0 : per + 9'd1;
                if (per_last) secs <= secs + 16'd1;
            end
        end
    end
    wire in_valid = ~rst && (ph < BURST);
    wire corner   = (ph < CORNER);

    // ---------------------------------------------------------------- stimulus
    // 521-bit shift register, b[t] = b[t-521] ^ b[t-353], advanced 96 bits per vector.
    // Bit i of lfsr is b[T-1-i].  The 96 new bits are each the xor of two old bits.
    reg  [520:0] lfsr = 521'd0;
    wire [IW-1:0] lfsr_new = lfsr[520 -: IW] ^ lfsr[LFSR_Q - 1 -: IW];
    always @(posedge clk) begin
        if (rst)           lfsr <= SEED;
        else if (in_valid) lfsr <= {lfsr[520-IW:0], lfsr_new};
    end
    wire [IW-1:0] cor;
    genvar gi;
    generate
        for (gi = 0; gi < N; gi = gi + 1) begin : g_cor
            assign cor[W*gi +: W] = ph[gi] ? 12'h800 : 12'h7FF;   // -2048 or +2047
        end
    endgenerate
    wire [IW-1:0] in_data = corner ? cor : lfsr[IW-1:0];

    // ---------------------------------------------------------------- the three circuits
    wire          v_ref, v_dut, v_ctl;
    wire [BW-1:0] o_ref, o_dut, o_ctl;
    wht_8_textbook_p_w12 u_ref (.clk(clk), .in_valid(in_valid), .in_data(in_data),
                                .out_valid(v_ref), .out_data(o_ref));
    wht_8_ours_p_w12     u_dut (.clk(clk), .in_valid(in_valid), .in_data(in_data),
                                .out_valid(v_dut), .out_data(o_dut));
    wht_8_broken_p_w12   u_ctl (.clk(clk), .in_valid(in_valid), .in_data(in_data),
                                .out_valid(v_ctl), .out_data(o_ctl));

    // the textbook is three clocks faster: delay it
    reg [BW-1:0] rd1, rd2, rd3;
    reg          rv1 = 1'b0, rv2 = 1'b0, rv3 = 1'b0;
    always @(posedge clk) begin
        rd1 <= o_ref; rd2 <= rd1; rd3 <= rd2;
        rv1 <= v_ref; rv2 <= rv1; rv3 <= rv2;
    end
    wire          rv = rv3;
    wire [BW-1:0] rd = rd3;

    // ---------------------------------------------------------------- comparator
    function [31:0] fold;
        input [BW-1:0] o;
        fold = o[31:0] ^ o[63:32] ^ o[95:64] ^ {8'd0, o[119:96]};
    endfunction
    reg [31:0] n = 32'd0, bad = 32'd0, ctl = 32'd0, sum = 32'd0, rn = 32'd0, rsum = 32'd0;
    wire dut_mis = (v_dut != rv) || (v_dut && (o_dut != rd));
    wire ctl_mis = (v_ctl != rv) || (v_ctl && (o_ctl != rd));
    always @(posedge clk) begin
        if (rst) begin
            n <= 32'd0; bad <= 32'd0; ctl <= 32'd0; sum <= 32'd0; rn <= 32'd0; rsum <= 32'd0;
        end else begin
            if (v_dut) begin n  <= n  + 32'd1; sum  <= sum  + (fold(o_dut) ^ n);  end
            if (rv)    begin rn <= rn + 32'd1; rsum <= rsum + (fold(rd)    ^ rn); end
            if (dut_mis) bad <= bad + 32'd1;
            if (ctl_mis) ctl <= ctl + 32'd1;
        end
    end

    // ---------------------------------------------------------------- report: one line per second
    // A line with k = 0 after the very first period, then one line at the end of every second.
    wire        rep  = ~rst && ph_last && (per_last || (per == 9'd0 && secs == 16'd0));
    wire [15:0] kval = per_last ? secs + 16'd1 : 16'd0;

    reg         line_busy = 1'b0;
    reg [6:0]   idx  = 7'd0;
    reg [175:0] snap = 176'd0;           // k, n, bad, ctl, sum, ref: 44 hex digits, first digit on top
    wire [7:0]  tch    = TMPL[8*(LEN-1-idx) +: 8];
    wire        is_hex = (tch == 8'h23);
    wire [3:0]  nib    = snap[175:172];
    wire [7:0]  hexch  = (nib < 4'd10) ? (8'h30 + {4'd0, nib}) : (8'h37 + {4'd0, nib});
    wire [7:0]  ch     = is_hex ? hexch : tch;

    // serial sender, 8 data bits, no parity, 1 stop bit.  The shift register is kept inverted so
    // that its start value 0 is the idle (high) level of the line.
    reg       ch_busy = 1'b0;
    reg [8:0] shn  = 9'd0;
    reg [3:0] bitn = 4'd0;
    reg [6:0] bcnt = 7'd0;
    assign uart_tx = ~shn[0];
    always @(posedge clk) begin
        if (rst) begin
            line_busy <= 1'b0; idx <= 7'd0; ch_busy <= 1'b0; shn <= 9'd0; bitn <= 4'd0; bcnt <= 7'd0;
        end else begin
            if (rep && !line_busy) begin
                line_busy <= 1'b1;
                idx  <= 7'd0;
                snap <= {kval, n, bad, ctl, sum, rsum};
            end
            if (ch_busy) begin
                if (bcnt == 7'd0) begin
                    bcnt <= BAUD_DIV - 1;
                    shn  <= {1'b0, shn[8:1]};
                    bitn <= bitn - 4'd1;
                    if (bitn == 4'd1) ch_busy <= 1'b0;
                end else begin
                    bcnt <= bcnt - 7'd1;
                end
            end else if (line_busy) begin
                shn  <= {~ch, 1'b1};      // start bit, then the character, least significant bit first
                bitn <= 4'd10;
                bcnt <= BAUD_DIV - 1;
                ch_busy <= 1'b1;
                if (is_hex) snap <= {snap[171:0], 4'd0};
                if (idx == LEN - 1) line_busy <= 1'b0;
                idx <= idx + 7'd1;
            end
        end
    end

    // ---------------------------------------------------------------- LEDs (registered)
    reg hb = 1'b0, pass = 1'b0, fail = 1'b0, caught = 1'b0;
    wire agree = (sum == rsum) && (n == rn);
    always @(posedge clk) begin
        if (rst) begin
            hb <= 1'b0; pass <= 1'b0; fail <= 1'b0; caught <= 1'b0;
        end else begin
            hb <= (per < PPS / 2);
            caught <= (ctl != 32'd0);
            if (bad != 32'd0 || (rep && !agree)) fail <= 1'b1;
            if (rep) pass <= (bad == 32'd0) && agree && (n != 32'd0) && (ctl != 32'd0) && !fail;
        end
    end
    assign led = {4'b0000, caught, fail, pass, hb};
endmodule
`default_nettype wire
