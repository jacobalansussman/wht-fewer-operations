# fpga-xc7: the circuits placed on a Xilinx Artix-7 with open tools

On 22 October 2026 I had the 19-adder 8-point circuit and the 52-adder 16-point circuit placed and routed on a
Xilinx Artix-7 (xc7a100tcsg324-1) with open tools only, against the textbook (24 and 64 adders) and against Alman
and Rao's 22-adder 8-point step, 5 placement seeds each. The result is a loss: the circuits use fewer carry blocks
but use more slices once placed. Results: [../README.md](../README.md), section "Xilinx Artix-7".

The tools: openXC7 release 2026-10-19 (nextpnr-xilinx `e7a6fb0e`, prjxray-db `6a6debcd`) and the YosysHQ
oss-cad-suite release 2026-10-11 (Yosys 0.69+274). `setup_tools.sh` downloads both and checks their SHA-256
digests. There is no vendor tool (Vivado) here and no bitstream: openXC7's timing uses placeholder delays, so the
clock figures are estimates, and its packer adds a pass-through LUT at carry inputs, so its LUT count is not a LUT
count that Vivado would report. The carry-block count (CARRY4) is exact and the same on every seed.

## Files

| file | what it is |
|---|---|
| `run.sh`, `setup_tools.sh`, `az_pre.sh` | the job: tools, then the place-and-route farm |
| `tools/farm.py`, `tools/fpga_farm.py` | the farm and the measurement tool (synthesis once per design, one nextpnr run per seed, counting) |
| `designs/xc7/ax7/*.v` | the designs: textbook (`tb8`, `tb16`), the circuits (`o19`, `o52`) and Alman and Rao's step (`ar8`), registered every 1 to 4 adder levels (`_d1` to `_d4`); written by a generator from the circuit files of this repository (line 3 of each file names its source; the generator itself is not included) |
| `designs/xc7/runs.txt` | the list of designs and options |
| `results/` | the run: `xc7/farm.jsonl.gz` (every seed and a summary per design), `xc7/farm_table.md`, the logs of the designs above, the self-test rows of two of them, `run_xc7.log`, `machine.txt` |

The run placed other designs too, from studies that are not part of this repository (`aj5_*`: ternary-adder
Hadamard designs; `as4_*`: a filter bank). Their rows are kept in `farm.jsonl.gz` and `farm_table.md`, which are
unchanged, but their design files and logs are not included. One of them, the hand-built ternary-adder 8-point
textbook, is quoted on the results page.

## Run it again

On a fresh Ubuntu 24.04 x86-64 machine with about 6 GB of free memory and the internet, from this folder:

    bash run.sh xc7

Off Colab, give the two working folders, since the defaults are under `/content`, Colab's working folder:
`TOOLS=$HOME/fpga-tools FARM_WORK=$HOME/fpga-work bash run.sh xc7`.

About 35 minutes on 8 cores. The run of 22 October first ran a self-test that compared this machine's tools with
earlier runs of designs not in this repository; the published `run.sh` skips it unless `SELFTEST=1`, since those
designs are missing here. `results/selftest_ax7_*.jsonl` are the self-test rows of the two Artix-7 designs.
