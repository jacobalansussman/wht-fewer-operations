#!/bin/bash
# run.sh -- x86-hybrid (built 22 Oct 2026 from x86-wht, which is unchanged).
#
# Question: does an FFHT-structured whole Walsh-Hadamard transform, with this repository's fewer-addition circuits as its
#   in-register kernels, beat FFHT itself on AMD Zen 2 / Zen 4 / Zen 5 (AVX2 first, AVX-512 if present)?
#   Tonight on Zen 2 the circuits won single passes (0.78-0.82 of the best textbook) but whole transforms came out
#   0.96-1.03 of FFHT / textbook, probably because x86-wht's whole transform is not FFHT's structure. Here the structure
#   is FFHT's (same blocks, recursion, loop order, in-lane sequences: check_plan.py proves the step sequence equals the
#   pinned fht_avx.c) and only the kernel on the 8 (or 16) vectors held in registers changes. See bench_hyb.c.
# Twin review (22 Oct 2026, a reviewing agent's report): new rival hyb8-tb8balS (the balanced textbook
#   with each butterfly emitted SUB before FMA: clang's FMA-first tb8bal carries 12 register copies per 8-point step,
#   tb8balS 0); clang_avx2_f64 is built and timed; the hfirst_/hstep_ disassembly of every binary is kept in out/asm/,
#   and asm_counts.txt counts register-to-register vector moves (regmov).
#
# Run on an x86-64 Linux machine:   bash run.sh   (see README.md in this folder for what it needs)
#   results:             out/ (out/SUMMARY.md last); the runs of 22 Oct 2026 are in ../runs/
# Env: MODE=quick|full (full: every binary, same array 2^10..2^20 and separate 2^12..2^20 even: about 28 min without
#      AVX-512, about 48 min with it [derived: 64 or 112 program-sizes (4 or 7 binaries x 16 sizes) x 11 programs x
#      2.3 s + about 1 min; 2.3 s = the Zen 5 full run 82494: 2206 s of timing for 96 x 10 program-sizes]);
#      CORE=<cpu to pin> (default: the last CPU); FORCE=1 times even if busy; TBUDGET=<s> (default 1620: a run that would
#      end after this many seconds from the start is skipped and listed in SUMMARY.md; MODE=full: default 4000).
# Runtime (quick): about 15-17 min without AVX-512, about 24 min with it (27 if apt must install compilers), on 8 vCPU
#   [derived: 2.3 s per program and size measured in the Zen 5 quick runs 74788 / 79401 (1197-1199 s in all for 51
#   sizes x 10 programs; timing began at 23-24 s); now 11 programs and 4 more sizes (clang_avx2_f64):
#   33 sizes x 11 x 2.3 s = 835 s without AVX-512 (Intel run 75640: 2.6 s per program and size, 944 s), 55 x 11 x
#   2.3 s = 1392 s with it; plus about 0.5 min of builds and gates (up to 4 min with apt installs)]. The budget guard
#   (estimate 2.6 s per program and size) skips the last, least important runs if it runs slow: on a host at 2.6 s with
#   AVX-512 that is the final whole_sep_gcc_avx512_f32 [derived: 50 + 52 x 11 x 2.6 + 91 = 1628 s > 1620 s].
# RAM: < 1 GB (same array), about 0.75 GB in the separate-array runs (11 programs x 64 MiB). No GPU.
# Binaries, objects and the FFHT clone live in $AZ_BUILD = /content/build/x86-hybrid, not in this folder.
set -u
cd "$(dirname "$0")"
W=$PWD; O=$W/out; mkdir -p $O
exec > >(tee -a $O/run.log) 2>&1
. "$W/az_pre.sh" x86-hybrid
T0=$(date +%s)
MODE=${MODE:-quick}; if [ "$MODE" = full ]; then TBUDGET=${TBUDGET:-4000}; else TBUDGET=${TBUDGET:-1620}; fi
echo "== x86-hybrid job, MODE=$MODE, time budget $TBUDGET s, start $(date -u)"
az_machine
FLAGS=$(grep -m1 '^flags' /proc/cpuinfo)
for f in avx2 fma avx512f avx512vl avx512dq; do echo "$FLAGS" | grep -qw $f && echo "CPU has $f" || echo "CPU lacks $f"; done
VENDOR=$(grep -m1 vendor_id /proc/cpuinfo | awk '{print $3}'); FAM=$(grep -m1 'cpu family' /proc/cpuinfo | awk '{print $4}')
MOD=$(grep -m1 '^model[[:space:]]*:' /proc/cpuinfo | awk '{print $3}'); STEP=$(grep -m1 stepping /proc/cpuinfo | awk '{print $3}')
case "$VENDOR/$FAM/$MOD" in
  GenuineIntel/6/79) UARCH="Intel Broadwell (adds and FMAs share 2 pipes; FADD 3, FMA 5 cycles)";;
  GenuineIntel/6/85) [ "${STEP:-0}" -ge 5 ] && UARCH="Intel Cascade Lake (shared pipes; FADD = FMA = 4 cycles)" || UARCH="Intel Skylake-SP (shared pipes; FADD = FMA = 4 cycles)";;
  GenuineIntel/6/106|GenuineIntel/6/108) UARCH="Intel Ice Lake-SP";;
  GenuineIntel/6/143|GenuineIntel/6/207) UARCH="Intel Sapphire/Emerald Rapids (Golden Cove: extra fast-add ports)";;
  AuthenticAMD/23/49) UARCH="AMD Zen 2 Rome (2 FADD + 2 FMA pipes)";;
  AuthenticAMD/25/1) UARCH="AMD Zen 3 Milan (2 FADD + 2 FMA pipes)";;
  AuthenticAMD/25/17) UARCH="AMD Zen 4 Genoa (2 FADD + 2 FMA pipes; AVX-512 on 256-bit units)";;
  AuthenticAMD/26/*) UARCH="AMD Zen 5";;
  *) UARCH="unknown ($VENDOR family $FAM model $MOD)";;
esac
echo "MICROARCHITECTURE (from family/model, recalled table): $UARCH"
echo "== tools"
pk=""; command -v gcc >/dev/null && command -v make >/dev/null || pk="$pk build-essential"; command -v clang >/dev/null || pk="$pk clang"
command -v git >/dev/null || pk="$pk git"; command -v python3 >/dev/null || pk="$pk python3"
if [ -n "$pk" ]; then echo "apt-get install$pk"; apt-get update -qq >/dev/null 2>&1; apt-get install -y -qq $pk >/dev/null 2>&1; fi
command -v taskset >/dev/null || apt-get install -y -qq util-linux >/dev/null 2>&1
gcc --version | head -1; if command -v clang >/dev/null; then clang --version | head -1; else echo "no clang (gcc only)"; fi
az_versions > $O/tools.txt 2>&1
FF=$AZ_BUILD/FFHT
if [ ! -d "$FF" ]; then git clone -q https://github.com/FALCONN-LIB/FFHT.git "$FF"; fi
(cd "$FF" && git checkout -q fba727a3ff72c862260460631ae1cc8e3e44e861 && git log -1 --format='FFHT %H %cd') || az_stop "FFHT checkout failed"
HAVE512=0; echo "$FLAGS" | grep -qw avx512f && echo "$FLAGS" | grep -qw avx512vl && HAVE512=1

BIN=$AZ_BUILD/bin
echo "== build (binaries in $BIN, outside the job folder; FFHT built from $FF with each binary's own flags)"
mkdir -p "$BIN" "$O/buildlogs"
# name : XT : flags : compilers.  XT 0 = 256-bit f32, 1 = 512-bit f32, 2 = 256-bit f64, 3 = 512-bit f64.
# avx2r32 = 256-bit vectors with 32 registers (the AVX-512 register file): where hyb16 (16 vectors) stops spilling.
CFGS=("avx2_f32:0:-mavx2 -mfma:gcc clang" "avx2_f64:2:-mavx2 -mfma:gcc clang")
[ $HAVE512 = 1 ] && CFGS+=("avx512_f32:1:-mavx2 -mfma -mavx512f -mavx512vl:gcc" "avx512_f64:3:-mavx2 -mfma -mavx512f -mavx512vl:gcc" \
                           "avx2r32_f32:0:-mavx2 -mfma -mavx512f -mavx512vl:gcc")
BINS=""
for cfg in "${CFGS[@]}"; do
  IFS=: read -r nm xt fl ccs <<< "$cfg"
  for cc in $ccs; do
    command -v $cc >/dev/null || { echo "no $cc: ${cc}_$nm not built"; continue; }
    if $cc -O3 $fl -DXT=$xt -DWITH_FFHT -I"$FF" bench_hyb.c "$FF/fht.c" "$FF/fast_copy.c" -o $BIN/${cc}_$nm -lm 2> $O/buildlogs/${cc}_$nm.buildlog; then
      BINS="$BINS ${cc}_$nm"; echo "built ${cc}_$nm ($cc -O3 $fl -DXT=$xt)"
      objdump -d --no-show-raw-insn $BIN/${cc}_$nm > $BIN/${cc}_$nm.asm 2>/dev/null
    else echo "BUILD FAILED ${cc}_$nm (see $O/buildlogs/${cc}_$nm.buildlog)"; fi
  done
done
[ -n "$BINS" ] || az_stop "no binary built"
python3 -I asmcount_hyb.py $BIN/*.asm > $O/asm_counts.txt 2>&1
grep -E "^==|hstep_(g52|tb16|g20|tb8)_|hfirst_(g52|tb16|g20|tb8)_" $O/asm_counts.txt | head -100
# keep the timed step functions' disassembly (hfirst_*, hstep_*: every kernel's code as timed); drop the rest
mkdir -p $O/asm
for a in $BIN/*.asm; do awk '/^[0-9a-f]+ <_?h(first|step)_[^>]*>:$/{p=1} p{print} /^$/{p=0}' "$a" > "$O/asm/$(basename "$a")"; done
rm -f "${BIN:?}"/*.asm

echo "== structure: the hybrid's step sequence must equal FFHT's (pinned fht_avx.c), float and double"
for t in float:gcc_avx2_f32 double:gcc_avx2_f64; do
  ty=${t%%:*}; b=${t#*:}
  case " $BINS " in *" $b "*) ;; *) az_stop "no $b for the $ty plan check";; esac
  python3 -I check_plan.py "$FF/fht_avx.c" $ty $BIN/$b 1 20 > $O/plan_check_$ty.txt 2>&1; rc=$?
  tail -2 $O/plan_check_$ty.txt
  [ $rc = 0 ] || az_stop "PLAN MISMATCH ($ty): the hybrid is not FFHT's structure"
done
for b in $BINS; do $BIN/$b plan 10 11 12 13 14 15 16 17 18 19 20 > $O/plan_$b.txt 2>&1; done

echo "== exactness gate: every binary, every variant (FFHT included) exact on random integers 2^1..2^20, broken copy caught"
for b in $BINS; do
  $BIN/$b check 20 > $O/check_$b.txt 2>&1; echo "$b: $(grep 'broken copy' $O/check_$b.txt | sed 's/.*: //') / $(tail -1 $O/check_$b.txt)"
  grep -q "^ALL PASS" $O/check_$b.txt || az_stop "CHECK FAILED $b (out/check_$b.txt)"
done

NCPU=$(nproc); CORE=${CORE:-$((NCPU - 1))}
SIBS=$(cat /sys/devices/system/cpu/cpu$CORE/topology/thread_siblings_list 2>/dev/null || echo $CORE)
echo "== pinning every timing to CPU $CORE; its SMT sibling(s): $SIBS"
T() { taskset -c $CORE "$@"; }
NPROG=11; SEC_PER=${SEC_PER:-2.6}   # seconds per program and size (estimate for the time budget)
run() { # name binary mode sizes...  -> out/<name>.txt; skipped if it would end after TBUDGET
  local nm=$1 b=$2 mode=$3; shift 3
  case " $BINS " in *" $b "*) ;; *) echo "-- $nm: no binary $b (not built here)"; return 0;; esac
  local est now; est=$(awk -v n=$# -v p=$NPROG -v s=$SEC_PER 'BEGIN{printf "%d", n*p*s + 5}'); now=$(( $(date +%s) - T0 ))
  if [ $((now + est)) -gt $TBUDGET ]; then echo "SKIPPED $nm (time budget: at $now s, needs about $est s, budget $TBUDGET s)"; return 0; fi
  az_quiet "$nm" "$SIBS"
  echo "-- $nm: $b whole $mode $* ($(date -u +%H:%M:%S), at $now s, about $est s)"
  T $BIN/$b whole $mode "$@" > $O/$nm.txt 2>&1
  grep "^RATIO" $O/$nm.txt | grep -E "hyb8-g|hyb8-h20|hyb16-g52" | awk '{printf "   %s %-13s / %s median %s best %s\n", $5, $7, $11, $13, $15}'
}

echo "== timing ($MODE)"
uptime
ALL="10 11 12 13 14 15 16 17 18 19 20"
if [ "$MODE" = full ]; then
  for b in $BINS; do run whole_same_$b $b same $ALL; done
  for b in $BINS; do run whole_sep_$b $b separate 12 14 16 18 20; done
else  # priority order: the deciding AVX2 binary first, then AVX-512, then the rest
  run whole_same_gcc_avx2_f32 gcc_avx2_f32 same $ALL
  run whole_same_gcc_avx512_f32 gcc_avx512_f32 same $ALL
  run whole_same_clang_avx2_f32 clang_avx2_f32 same $ALL
  run whole_sep_gcc_avx2_f32 gcc_avx2_f32 separate 12 16 20
  run whole_same_gcc_avx2_f64 gcc_avx2_f64 same 10 12 14 16
  run whole_same_clang_avx2_f64 clang_avx2_f64 same 10 12 14 16
  run whole_same_gcc_avx512_f64 gcc_avx512_f64 same 10 12 14 16
  run whole_same_gcc_avx2r32_f32 gcc_avx2r32_f32 same 10 12 14 16
  run whole_sep_gcc_avx512_f32 gcc_avx512_f32 separate 12 16 20
fi
echo "== load after timing"; uptime
python3 -I summarize_hyb.py $O > $O/SUMMARY.md 2>&1; cat $O/SUMMARY.md
echo "DONE $(date -u) after $(( $(date +%s) - T0 )) s"
