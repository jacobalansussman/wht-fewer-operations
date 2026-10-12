// Verilator harness: runs the design for a number of clocks and decodes the serial transmit pin
// with its own 115,200-baud timing (12,000,000 / 115,200 = 104.1667 clocks per bit, kept as a
// fraction), so the design's baud rate is checked as well.  Received bytes go to a file.
//   <binary> <clocks> <output file>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include "verilated.h"
#include VTOP_H

int main(int argc, char **argv) {
    Verilated::commandArgs(argc, argv);
    if (argc < 3) { fprintf(stderr, "usage: %s clocks outfile\n", argv[0]); return 2; }
    uint64_t nclk = strtoull(argv[1], nullptr, 10);
    FILE *f = fopen(argv[2], "wb");
    if (!f) { perror("open"); return 2; }
    VTOP *top = new VTOP;
    const double BIT = 12000000.0 / 115200.0;
    uint64_t nbytes = 0, nlines = 0, ferr = 0;
    int state = 0;            // 0 idle, 1 receiving
    double tstart = 0;        // clock at which the start bit began
    int bit = 0; unsigned sh = 0;
    int prev = 1;
    top->clk = 0; top->eval();
    for (uint64_t c = 0; c < nclk; c++) {
        top->clk = 1; top->eval();
        top->clk = 0; top->eval();
        int tx = top->uart_tx & 1;
        if (state == 0) {
            if (prev == 1 && tx == 0) { state = 1; tstart = (double)c; bit = 0; sh = 0; }
        } else {
            // sample points: middle of start bit (bit -1), data bits 0..7, stop bit (8)
            double due = tstart + BIT * (0.5 + bit);
            if ((double)c >= due) {
                if (bit == 0) { if (tx != 0) ferr++; }
                else if (bit <= 8) { sh |= (unsigned)tx << (bit - 1); }
                else {
                    if (tx != 1) ferr++;
                    fputc((int)sh, f); nbytes++;
                    if (sh == 0x0A) {
                        nlines++;
                        printf("LINE %llu complete at clock %llu, led=%d%d%d%d%d%d%d%d\n",
                               (unsigned long long)nlines, (unsigned long long)c,
                               (top->led >> 7) & 1, (top->led >> 6) & 1, (top->led >> 5) & 1, (top->led >> 4) & 1,
                               (top->led >> 3) & 1, (top->led >> 2) & 1, (top->led >> 1) & 1, top->led & 1);
                        fflush(stdout); fflush(f);
                    }
                    state = 0;
                }
                bit++;
            }
        }
        prev = tx;
    }
    printf("END clocks=%llu bytes=%llu lines=%llu framing_errors=%llu led=0x%02x\n",
           (unsigned long long)nclk, (unsigned long long)nbytes, (unsigned long long)nlines,
           (unsigned long long)ferr, (unsigned)top->led);
    fclose(f);
    delete top;
    return ferr ? 1 : 0;
}
