#!/bin/sh
# Build the self-test image: synthesis (yosys), place and route (nextpnr-ice40), timing (icetime),
# bitstream (icepack).  Nothing here touches the board.
#   sh build.sh            writes build/selftest.bin and the logs
set -eu
SUITE=${OSS_CAD_SUITE:-/opt/oss-cad-suite}      # the unpacked oss-cad-suite
export PATH="$SUITE/bin:$PATH"
cd "$(dirname "$0")"
mkdir -p build
python3 gen_params.py > build/gen_params.log
SRC="selftest_top.v rtl/8_textbook_p_w12.v rtl/8_ours_p_w12.v rtl/8_broken_p_w12.v"
MODS="wht_8_textbook_p_w12 wht_8_ours_p_w12 wht_8_broken_p_w12"

# The three transforms are synthesised as separate modules (keep_hierarchy), so that yosys cannot
# merge the broken copy into the real one or share logic between them.  They are flattened only
# after synthesis, with no optimisation afterwards.
yosys -q -l build/yosys.log -p "
  read_verilog -I. $SRC;
  hierarchy -check -top selftest_top;
  setattr -mod -set keep_hierarchy 1 $MODS;
  synth_ice40 -top selftest_top;
  tee -q -o build/stat_hier.txt stat;
  setattr -mod -unset keep_hierarchy $MODS;
  flatten; clean;
  tee -q -o build/stat_flat.txt stat;
  write_json build/selftest.json;
  write_verilog -noattr build/selftest_synth.v"

nextpnr-ice40 --hx8k --package ct256 --json build/selftest.json --pcf hx8k.pcf \
    --asc build/selftest.asc --freq 12 --seed 1 --report build/nextpnr_report.json \
    -l build/nextpnr.log -q

icetime -d hx8k -P ct256 -p hx8k.pcf -c 12 -t -m -r build/icetime.rpt build/selftest.asc > build/icetime.log 2>&1

# Lattice FPGA-TN-02001-3.5 p. 30: an image for SPI peripheral ("slave") loading must not use the
# warm boot option.  icepack takes that from a line in its input.
(cat build/selftest.asc; echo ".warmboot disabled") > build/selftest_nowarm.asc
icepack build/selftest_nowarm.asc build/selftest.bin
iceunpack build/selftest.bin build/selftest_unpacked.asc

ls -l build/selftest.bin
shasum -a 256 build/selftest.bin
