#!/bin/bash
# run.sh -- x86-hybrid-small (built 22 Oct 2026 from x86-hybrid, which is unchanged).
#
# Question: do the circuits help at the sizes libraries use (RaBitQ-Library, FAISS, ik_llama.cpp: 64-512 points, mostly
#   single precision, many vectors at a time)?  x86-hybrid timed one 2^10..2^20 transform at a time.  Here each timed call
#   transforms a BATCH of B vectors of n points (n = 2^6..2^9, plus 2^10 and 2^12 to overlap x86-hybrid), the batch sized
#   to fit in L2, against FFHT itself, x86-wht's whole transform, FFHT's structure with textbook kernels, and the
#   straight-line in-register transform (one 8- or 16-vector step does all of n) with textbook and circuit kernels.
#   f32 first, then f64; 256-bit AVX2 and, when the CPU has avx512f + avx512vl, 512-bit; gcc and clang.  See bench_small.c.
#
# Run on an x86-64 Linux machine:   bash run.sh   (see README.md in this folder for what it needs)
#   results:             out/ (out/SUMMARY.md last); the runs of 22 Oct 2026 are in ../runs/
# Env: CORE=<cpu to pin> (default: the last CPU); FORCE=1 times even if busy; TBUDGET=<s> (default 1680: a run that would
#      end after this many seconds from the start is skipped and listed in SUMMARY.md); BATCH_KB=<KB> (default: half the
#      L2 of the pinned core, at most 512); SIZES (default "6 7 8 9 10 12"); SEC_PER (default 2.5 s per program and size).
# Runtime: about 14 min without AVX-512, about 26-27 min with it [derived: x86-hybrid tonight took 2.28 s per program
#   and size on Zen 5 (251 s for 11 sizes x 10 programs); here 68-81 timed (program, size) pairs per binary (bench_small
#   count + FFHT: 77 avx2_f32, 79 avx2_f64, 68 avx512_f32, 81 avx512_f64), 4 binaries without AVX-512 and 8 with it:
#   312 x 2.35 s = 733 s or 610 x 2.35 s = 1434 s, plus about 1.5-3 min of install, builds and gates].  The budget guard
#   (TBUDGET 1680 s) drops the last, least important runs if the host is slower.
# Twin (22 Oct): hyb8-tb8balS, the SUB-first balanced rival of x86-hybrid (the reviewing agent's twin report, verdict READY),
#   is ported here, with its straight-line form sl8-tb8balS and the same order for the 16-vector textbook (tb16balS).
# RAM: < 100 MB.  No GPU.  Binaries, objects and the FFHT clone live in $AZ_BUILD = /content/build/x86-hybrid-small.
set -u
cd "$(dirname "$0")"
W=$PWD; O=$W/out; mkdir -p $O
exec > >(tee -a $O/run.log) 2>&1
. "$W/az_pre.sh" x86-hybrid-small
T0=$(date +%s)
TBUDGET=${TBUDGET:-1680}; SIZES=${SIZES:-"6 7 8 9 10 12"}
echo "== x86-hybrid-small job, sizes 2^($SIZES), time budget $TBUDGET s, start $(date -u)"
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

NCPU=$(nproc); CORE=${CORE:-$((NCPU - 1))}
SIBS=$(cat /sys/devices/system/cpu/cpu$CORE/topology/thread_siblings_list 2>/dev/null || echo $CORE)
# batch footprint: half the L2 of the pinned core, at most 512 KB (Zen 4/5: 1 MB L2 -> 512 KB; Zen 2/3: 512 KB -> 256 KB)
L2S=""; for d in /sys/devices/system/cpu/cpu$CORE/cache/index*; do
  [ "$(cat $d/level 2>/dev/null)" = 2 ] && [ "$(cat $d/type 2>/dev/null)" != Instruction ] && L2S=$(cat $d/size 2>/dev/null)
done
case "$L2S" in *K) L2KB=${L2S%K};; *M) L2KB=$(( ${L2S%M} * 1024 ));; *) L2KB="";; esac
if [ -z "$L2KB" ]; then L2KB=1024; L2NOTE="(L2 size not readable from sysfs: assumed 1024 KB)"; else L2NOTE="(sysfs, cpu$CORE)"; fi
if [ -z "${BATCH_KB:-}" ]; then BATCH_KB=$(( L2KB / 2 )); [ $BATCH_KB -gt 512 ] && BATCH_KB=512; fi
export BATCH_KB
echo "BATCH: L2 per core $L2KB KB $L2NOTE; batch footprint BATCH_KB = $BATCH_KB KB (B = BATCH_KB / (n x element size))"

BIN=$AZ_BUILD/bin
echo "== build (binaries in $BIN, outside the job folder; FFHT built from $FF with each binary's own flags)"
mkdir -p "$BIN" "$O/buildlogs" "$O/asm"
# name : XT : flags : compilers.  XT 0 = 256-bit f32, 1 = 512-bit f32, 2 = 256-bit f64, 3 = 512-bit f64.
CFGS=("avx2_f32:0:-mavx2 -mfma:gcc clang" "avx2_f64:2:-mavx2 -mfma:gcc clang")
[ $HAVE512 = 1 ] && CFGS+=("avx512_f32:1:-mavx2 -mfma -mavx512f -mavx512vl:gcc clang" "avx512_f64:3:-mavx2 -mfma -mavx512f -mavx512vl:gcc clang")
BINS=""
for cfg in "${CFGS[@]}"; do
  IFS=: read -r nm xt fl ccs <<< "$cfg"
  for cc in $ccs; do
    command -v $cc >/dev/null || { echo "no $cc: ${cc}_$nm not built"; continue; }
    if $cc -O3 $fl -DXT=$xt -DWITH_FFHT -I"$FF" bench_small.c "$FF/fht.c" "$FF/fast_copy.c" -o $BIN/${cc}_$nm -lm 2> $O/buildlogs/${cc}_$nm.buildlog; then
      BINS="$BINS ${cc}_$nm"; echo "built ${cc}_$nm ($cc -O3 $fl -DXT=$xt)"
      objdump -d --no-show-raw-insn $BIN/${cc}_$nm > $BIN/${cc}_$nm.asm 2>/dev/null
      # keep the disassembly of every hyb / straight-line step function (hfirst_* = the straight-line step), not FFHT's
      awk '/^[0-9a-f]+ <_?(hfirst|hstep|sl)_/{p=1} p{print} p && /^$/{p=0}' $BIN/${cc}_$nm.asm | gzip -9 > $O/asm/${cc}_$nm.steps.asm.gz
    else echo "BUILD FAILED ${cc}_$nm (see $O/buildlogs/${cc}_$nm.buildlog)"; fi
  done
done
[ -n "$BINS" ] || az_stop "no binary built"
python3 -I asmcount_hyb.py $BIN/*.asm > $O/asm_counts.txt 2>&1
grep -E "^==| (sl|hstep)_(g20_nat|tb8_nat|tb8_bal|tb8_balS|g52_nat|tb16_nat|tb16_bal|tb16_balS|g20_x2) " $O/asm_counts.txt | head -110
rm -f "${BIN:?}"/*.asm

echo "== structure: the hyb plans must equal FFHT's (pinned fht_avx.c), float and double"
for t in float:gcc_avx2_f32 double:gcc_avx2_f64; do
  ty=${t%%:*}; b=${t#*:}
  case " $BINS " in *" $b "*) ;; *) b=clang_${b#gcc_}; case " $BINS " in *" $b "*) ;; *) az_stop "no binary for the $ty plan check";; esac;; esac
  python3 -I check_plan.py "$FF/fht_avx.c" $ty $BIN/$b 1 20 > $O/plan_check_$ty.txt 2>&1; rc=$?
  tail -2 $O/plan_check_$ty.txt
  [ $rc = 0 ] || az_stop "PLAN MISMATCH ($ty): the hybrid is not FFHT's structure"
done
for b in $BINS; do $BIN/$b list $SIZES > $O/list_$b.txt 2>&1; done
grep -h "^SIZE" $O/list_gcc_avx2_f32.txt 2>/dev/null | cut -c1-160

echo "== exactness gate: every binary, every program (FFHT included), every size 2^1..2^12 (batch of 3) and every timed size"
echo "   with its timing batch: exact on random integers, guard zones intact, real-input error, the timing loop finite and"
echo "   back at its start after the exact rescale; every deliberately broken copy must fail wherever it runs"
for b in $BINS; do
  $BIN/$b check 12 $SIZES > $O/check_$b.txt 2>&1
  echo "$b: $(grep -c 'FAIL (caught, good)' $O/check_$b.txt) broken-copy runs caught / $(grep '^CHECK [0-9]* (program' $O/check_$b.txt | sed 's/^CHECK //' | cut -c1-60) / $(tail -1 $O/check_$b.txt)"
  grep -q "^ALL PASS" $O/check_$b.txt || az_stop "CHECK FAILED $b (out/check_$b.txt)"
done

echo "== pinning every timing to CPU $CORE; its SMT sibling(s): $SIBS"
T() { taskset -c $CORE "$@"; }
SEC_PER=${SEC_PER:-2.5}   # seconds per program and size (estimate for the time budget)
run() { # binary -> out/batch_<binary>.txt; skipped if it would end after TBUDGET
  local b=$1
  case " $BINS " in *" $b "*) ;; *) echo "-- $b: not built here"; return 0;; esac
  local cnt est now
  cnt=$($BIN/$b count $SIZES | awk '/^COUNT/{print $2}'); cnt=${cnt:-70}
  est=$(awk -v n=$cnt -v s=$SEC_PER 'BEGIN{printf "%d", n*s + 5}'); now=$(( $(date +%s) - T0 ))
  if [ $((now + est)) -gt $TBUDGET ]; then echo "SKIPPED batch_$b (time budget: at $now s, needs about $est s for $cnt program-sizes, budget $TBUDGET s)"; return 0; fi
  az_quiet "batch_$b" "$SIBS"
  echo "-- batch_$b: $b batch $SIZES ($(date -u +%H:%M:%S), at $now s, $cnt program-sizes, about $est s)"
  T $BIN/$b batch $SIZES > $O/batch_$b.txt 2>&1
  grep "^RATIO" $O/batch_$b.txt | grep -E " (sl8-g20|hyb8-g20|sl16-g52|sl16-g20x2|hyb16-g52) " | awk '{printf "   %s %-12s / %s median %s\n", $4, $6, $10, $12}'
}

echo "== timing (priority order: f32 before f64, gcc AVX2 first)"
uptime
for b in gcc_avx2_f32 clang_avx2_f32 gcc_avx512_f32 gcc_avx2_f64 clang_avx2_f64 gcc_avx512_f64 clang_avx512_f32 clang_avx512_f64; do run $b; done
echo "== load after timing"; uptime
python3 -I summarize_small.py $O > $O/SUMMARY.md 2>&1; cat $O/SUMMARY.md
echo "DONE $(date -u) after $(( $(date +%s) - T0 )) s"
