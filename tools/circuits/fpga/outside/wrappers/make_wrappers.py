#!/usr/bin/env python3
"""Write thin wrappers around two outside cores, so that they have the same ports
as the designs in ../../rtl/v (written by gen_rtl.py):

    module wht_<N>_<core>_<variant>_w<W> (clk, in_valid, in_data, out_valid, out_data)
    x_i is in_data[W*i +: W]  (signed);  y_J is out_data[(W+log2 N)*J +: (W+log2 N)]  (signed)
    y_J = sum over i of (-1)^popcount(J & i) * x_i
    variant c: combinational, latency 0.
    variant r: one register stage at the inputs, one at the outputs, nothing between, latency 2.

The cores themselves are NOT copied and NOT changed.  A wrapper only instantiates a
module of the core and connects wires.  The core file is given to the tool beside the
wrapper (see ../build_examples.sh).

  xk265 : module hadamard_trans_1d in cores/openasic-org_xk265/rtl/fme/fme_satd_8x8.v
          8 points, 24 adders, width is a parameter (DATA_WIDTH).
  xk264 : module intra_hadamard4x4 in cores/openasic-org_xk264/rtl/intra/intra_hadamard4x4.v
          4 x 4 = 16 points, 64 adders, the input width is fixed at 9 bits in the core.

Usage:  python3 -B make_wrappers.py      (writes the .v files beside this script)
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def ports(name, n, w, wo):
    return (
        f"module {name} (\n"
        f"    input  wire                 clk,\n"
        f"    input  wire                 in_valid,\n"
        f"    input  wire [{n*w-1}:0] in_data,\n"
        f"    output wire                 out_valid,\n"
        f"    output wire [{n*wo-1}:0] out_data\n"
        f");\n"
    )


def shell(variant, n, w, wo, inst):
    """inst(xin, yout) returns the text of the core instance, wired to the nets xin and yout."""
    s = ""
    if variant == "c":
        s += f"    wire [{n*w-1}:0] x_bus = in_data;\n"
        s += f"    wire [{n*wo-1}:0] y_bus;\n"
        s += inst("x_bus", "y_bus")
        s += "    assign out_data = y_bus;\n"
        s += "    assign out_valid = in_valid;\n"
    else:
        s += f"    reg  [{n*w-1}:0] x_bus;\n"
        s += f"    wire [{n*wo-1}:0] y_bus;\n"
        s += f"    reg  [{n*wo-1}:0] out_q1;\n"
        s += "    reg  [1:0] vld = 2'd0;\n"
        s += "    always @(posedge clk) begin\n"
        s += "        x_bus <= in_data;\n"
        s += "        out_q1 <= y_bus;\n"
        s += "        vld <= {vld[0:0], in_valid};\n"
        s += "    end\n"
        s += inst("x_bus", "y_bus")
        s += "    assign out_data = out_q1;\n"
        s += "    assign out_valid = vld[1];\n"
    return s + "endmodule\n"


def xk265_8(variant, w):
    n, wo = 8, w + 3
    name = f"wht_8_xk265_{variant}_w{w}"

    def inst(xin, yout):
        t = f"    hadamard_trans_1d #(.DATA_WIDTH({w})) core (\n"
        t += "".join(f"        .idata_{i}({xin}[{w*i+w-1}:{w*i}]),\n" for i in range(n))
        t += ",\n".join(f"        .odata_{j}({yout}[{wo*j+wo-1}:{wo*j}])" for j in range(n))
        return t + "\n    );\n"

    head = (
        "// Thin wrapper written for the FPGA check.  Written by make_wrappers.py.\n"
        "// It instantiates, unchanged, the module hadamard_trans_1d of the open HEVC encoder xk265\n"
        "// (file rtl/fme/fme_satd_8x8.v, commit 832e564a8e59dd90a18fb7ee8e2ed87d96aa03bc).\n"
        "// That module is the textbook network: 3 layers of 8 additions or subtractions, 24 adders.\n"
        f"// Inputs: 8 signed values of {w} bits.  Outputs: 8 signed values of {wo} bits.\n"
        + ("// Variant c: combinational.  Latency 0.  clk is not used.\n" if variant == "c" else
           "// Variant r: one register stage at the inputs, 1 at the outputs, nothing between.  Latency 2.\n")
    )
    return name, head + ports(name, n, w, wo) + shell(variant, n, w, wo, inst)


def xk264_16(variant):
    n, w, wo = 16, 9, 13
    name = f"wht_16_xk264_{variant}_w{w}"

    def inst(xin, yout):
        t = "    intra_hadamard4x4 core (\n"
        # x_{4r+c} is the core's input ht_s<r><c>_i ; y_{4r+c} is its output ht_d<r><c>_o
        for r in range(4):
            for c in range(4):
                i = 4 * r + c
                t += f"        .ht_s{r}{c}_i({xin}[{w*i+w-1}:{w*i}]),\n"
        lines = []
        for r in range(4):
            for c in range(4):
                j = 4 * r + c
                lines.append(f"        .ht_d{r}{c}_o({yout}[{wo*j+wo-1}:{wo*j}])")
        return t + ",\n".join(lines) + "\n    );\n"

    head = (
        "// Thin wrapper written for the FPGA check.  Written by make_wrappers.py.\n"
        "// It instantiates, unchanged, the module intra_hadamard4x4 of the open H.264 encoder xk264\n"
        "// (file rtl/intra/intra_hadamard4x4.v, commit b59222e67fb77917a3afe97941c9a25b2b3a41f9).\n"
        "// That module is the textbook 4 x 4 transform: 8 four-point butterflies of 8 adders, 64 adders.\n"
        "// A 4 x 4 two-dimensional Hadamard transform is the 16-point transform: x_{4r+c} is row r, column c.\n"
        "// The core writes a - b as a + (~b + 1); whether a tool folds that into one subtractor is the tool's affair.\n"
        f"// Inputs: 16 signed values of {w} bits (the width is fixed in the core).  Outputs: 16 signed values of {wo} bits.\n"
        + ("// Variant c: combinational.  Latency 0.  clk is not used.\n" if variant == "c" else
           "// Variant r: one register stage at the inputs, 1 at the outputs, nothing between.  Latency 2.\n")
    )
    return name, head + ports(name, n, w, wo) + shell(variant, n, w, wo, inst)


def main():
    written = []
    for variant in ("c", "r"):
        for w in (8, 9, 12, 16):
            name, text = xk265_8(variant, w)
            written.append((name, text))
        name, text = xk264_16(variant)
        written.append((name, text))
    for name, text in written:
        path = os.path.join(HERE, name[len("wht_"):] + ".v")
        with open(path, "w") as f:
            f.write(text)
        print("wrote", os.path.basename(path))


if __name__ == "__main__":
    main()
