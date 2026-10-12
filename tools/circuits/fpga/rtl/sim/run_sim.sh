#!/bin/sh
# run_sim.sh -- simulate every design against the golden vectors, with two simulators.
# Run from fpga/rtl after "python3 -B gen_rtl.py --all" and "python3 -B sim/golden.py".
# One process at a time.  Results: work/log/verilator_<bench>.log, work/log/iverilog_<bench>.log,
# and the summary sim/RESULTS.txt (one RESULT line per design and simulator).
#   Verilator: every bench, every vector.
#   Icarus Verilog: every vector at 8 and 16 points; the first IV64 vectors at 64 points
#   (all corner cases and the first random vectors), because it is slow there.
set -u
export PATH="${OSS_CAD_SUITE:-/opt/oss-cad-suite}/bin:$PATH"
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT" || exit 1
IV64=${IV64:-12000}
mkdir -p work/vl work/iv work/log
for b in 8_w8 8_w12 8_w16 16_w8 16_w12 16_w16 64_w8 64_w12 64_w16; do
  files=$(cat work/tb/tb_$b.files)
  verilator --binary --timing -j 1 -Wno-fatal -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDSIGNAL \
      -Wno-DECLFILENAME -CFLAGS -O1 --top-module tb --Mdir work/vl/tb_$b -o sim \
      work/tb/tb_$b.v $files > work/log/verilator_build_$b.log 2>&1
  ( cd work/vec && ../vl/tb_$b/sim ) > work/log/verilator_$b.log 2>&1
  grep -c '^RESULT' work/log/verilator_$b.log | sed "s/^/verilator $b RESULT lines: /"
  grep '^BENCH' work/log/verilator_$b.log
done
for b in 8_w8 8_w12 8_w16 16_w8 16_w12 16_w16 64_w8 64_w12 64_w16; do
  files=$(cat work/tb/tb_$b.files)
  case $b in
    64_*) P="-Ptb.NRUN=$IV64" ;;
    *)    P="" ;;
  esac
  iverilog -g2005 $P -o work/iv/tb_$b.vvp -s tb work/tb/tb_$b.v $files > work/log/iverilog_build_$b.log 2>&1
  ( cd work/vec && vvp -n ../iv/tb_$b.vvp ) > work/log/iverilog_$b.log 2>&1
  grep '^BENCH' work/log/iverilog_$b.log
done
{
  echo "# simulator bench-line or result-line (written by sim/run_sim.sh on $(date))"
  for s in verilator iverilog; do
    for b in 8_w8 8_w12 8_w16 16_w8 16_w12 16_w16 64_w8 64_w12 64_w16; do
      grep -E '^(RESULT|BENCH|MISMATCH)' work/log/${s}_$b.log | sed "s/^/$s /"
    done
  done
} > sim/RESULTS.txt
echo done
