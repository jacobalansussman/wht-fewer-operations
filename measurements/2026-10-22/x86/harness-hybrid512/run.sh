#!/bin/bash
# run.sh -- x86-hybrid512 (built 22 Oct 2026 from x86-hybrid, which is unchanged).
#
# Question: does the circuit beat the BEST 512-bit (AVX-512F) whole Walsh-Hadamard transform on Zen 4 / Zen 5,
#   not just FFHT?  Tonight on Zen 5 (EPYC 9B45) a plain 512-bit textbook was 1.30-1.45x faster than any 256-bit code;
#   inside the old, untuned 512-bit build the circuit was mixed (0.88-1.07 of the best rival).  Here: an FFHT-style
#   512-bit transform re-made and TUNED on the textbook (in-lane form, thresholds; bench_h512.c), then the same structure
#   with the circuits as the in-register step, against x86-wht's 512-bit codes and FFHT (256-bit, reference).
#
# Run on an x86-64 Linux machine:   bash run.sh   (see README.md in this folder for what it needs)
#   results:             out/ (out/SUMMARY.md last); the runs of 22 Oct 2026 are in ../runs/
# Needs AVX-512F + VL (Zen 4, Zen 5, Intel Xeon since Skylake-SP); stops without it.
# Env: CORE=<cpu to pin> (default: the last CPU); FORCE=1 times even if busy; TBUDGET=<s> (default 1950: a run that
#      would end after this many seconds from the start is skipped and listed in SUMMARY.md); H512_TUNE_MS (default 15).
# Runtime: about 31-33 min on 8 vCPU [derived: 15 programs x 2.3-2.5 s per program and size (x86-hybrid's Zen 5 runs:
#   2.3 s) = 35-38 s per size; same array: gcc f64 + gcc f32 at 13 sizes, clang f64 + clang f32 at the 7 even sizes =
#   40 sizes = 1380-1500 s; separate arrays gcc f64 + f32 at 3 sizes = 210-225 s; setup, parallel builds and gates, tune
#   about 4-5 min].  The budget guard (TBUDGET 1950 s, pace re-estimated after every run) drops the separate-array runs
#   first, so the job ends inside 35 min.
# RAM: < 1 GB (separate arrays: 15 programs x 64 MiB = 0.96 GB).  No GPU.
# Binaries, objects, disassembly and the FFHT clone live in $AZ_BUILD = /content/build/x86-hybrid512, not in this folder
# (only the hybrid step functions' disassembly is copied to out/asm/).
set -u
cd "$(dirname "$0")"
W=$PWD; O=$W/out; mkdir -p $O
exec > >(tee -a $O/run.log) 2>&1
. "$W/az_pre.sh" x86-hybrid512
T0=$(date +%s)
TBUDGET=${TBUDGET:-1950}
echo "== x86-hybrid512 job, time budget $TBUDGET s, start $(date -u)"
az_machine
FLAGS=$(grep -m1 '^flags' /proc/cpuinfo)
for f in avx2 fma avx512f avx512vl avx512dq; do echo "$FLAGS" | grep -qw $f && echo "CPU has $f" || echo "CPU lacks $f"; done
VENDOR=$(grep -m1 vendor_id /proc/cpuinfo | awk '{print $3}'); FAM=$(grep -m1 'cpu family' /proc/cpuinfo | awk '{print $4}')
MOD=$(grep -m1 '^model[[:space:]]*:' /proc/cpuinfo | awk '{print $3}'); STEP=$(grep -m1 stepping /proc/cpuinfo | awk '{print $3}')
case "$VENDOR/$FAM/$MOD" in
  GenuineIntel/6/85) [ "${STEP:-0}" -ge 5 ] && UARCH="Intel Cascade Lake (AVX-512: 1 or 2 FMA units)" || UARCH="Intel Skylake-SP (AVX-512: 1 or 2 FMA units)";;
  GenuineIntel/6/106|GenuineIntel/6/108) UARCH="Intel Ice Lake-SP";;
  GenuineIntel/6/143|GenuineIntel/6/207) UARCH="Intel Sapphire/Emerald Rapids";;
  AuthenticAMD/25/17) UARCH="AMD Zen 4 Genoa (AVX-512 on 256-bit units: a 512-bit op takes a pipe for 2 cycles)";;
  AuthenticAMD/26/*) UARCH="AMD Zen 5 (full-width 512-bit units on the server parts)";;
  *) UARCH="unknown ($VENDOR family $FAM model $MOD)";;
esac
echo "MICROARCHITECTURE (from family/model, recalled table): $UARCH"
echo "$FLAGS" | grep -qw avx512f && echo "$FLAGS" | grep -qw avx512vl || az_stop "no AVX-512F/VL on this CPU: this job is 512-bit only"
echo "== tools"
pk=""; command -v gcc >/dev/null && command -v make >/dev/null || pk="$pk build-essential"; command -v clang >/dev/null || pk="$pk clang"
command -v git >/dev/null || pk="$pk git"; command -v python3 >/dev/null || pk="$pk python3"; command -v objdump >/dev/null || pk="$pk binutils"
if [ -n "$pk" ]; then echo "apt-get install$pk"; apt-get update -qq >/dev/null 2>&1; apt-get install -y -qq $pk >/dev/null 2>&1; fi
command -v taskset >/dev/null || apt-get install -y -qq util-linux >/dev/null 2>&1
gcc --version | head -1; if command -v clang >/dev/null; then clang --version | head -1; else echo "no clang (gcc only)"; fi
az_versions > $O/tools.txt 2>&1
FF=$AZ_BUILD/FFHT
if [ ! -d "$FF" ]; then git clone -q https://github.com/FALCONN-LIB/FFHT.git "$FF"; fi
(cd "$FF" && git checkout -q fba727a3ff72c862260460631ae1cc8e3e44e861 && git log -1 --format='FFHT %H %cd') || az_stop "FFHT checkout failed"

BIN=$AZ_BUILD/bin
echo "== build (binaries in $BIN, outside the job folder; FFHT built from $FF with each binary's own flags)"
mkdir -p "$BIN" "$O/buildlogs" "$O/asm"; rm -f "${BIN:?}"/*   # no stale binary from an earlier run on this Colab
# name : XT : flags : compilers.  XT 1 = 512-bit f32, 3 = 512-bit f64 (timed); 0 / 2 = 256-bit (plan check only).
F512="-mavx2 -mfma -mavx512f -mavx512vl"
CFGS=("avx512_f64:3:$F512:gcc clang" "avx512_f32:1:$F512:gcc clang")
BINS=""; CAND=""
for cfg in "${CFGS[@]}"; do  # the builds run in parallel (nothing is timed yet)
  IFS=: read -r nm xt fl ccs <<< "$cfg"
  for cc in $ccs; do
    command -v $cc >/dev/null || { echo "no $cc: ${cc}_$nm not built"; continue; }
    CAND="$CAND ${cc}_$nm"
    ( $cc -O3 $fl -DXT=$xt -DWITH_FFHT -I"$FF" bench_h512.c "$FF/fht.c" "$FF/fast_copy.c" -o $BIN/${cc}_$nm -lm \
        2> $O/buildlogs/${cc}_$nm.buildlog && echo "built ${cc}_$nm ($cc -O3 $fl -DXT=$xt)" > $O/buildlogs/${cc}_$nm.ok ) &
  done
done
for p in "plan_avx2_f32:0" "plan_avx2_f64:2"; do  # the same plan code at 256 bits, without FFHT: for check_plan.py
  nm=${p%%:*}; xt=${p#*:}
  gcc -O2 -mavx2 -mfma -DXT=$xt bench_h512.c -o $BIN/$nm -lm 2> $O/buildlogs/$nm.buildlog &
done
wait $(jobs -p)   # fix 22 Oct 2026: a bare "wait" also waits for the >(tee) process substitution on bash >= 5.1 and hung the job
for b in $CAND; do
  if [ -f $O/buildlogs/$b.ok ]; then
    BINS="$BINS $b"; cat $O/buildlogs/$b.ok; rm -f $O/buildlogs/$b.ok
    objdump -d --no-show-raw-insn $BIN/$b > $BIN/$b.asm 2>/dev/null
    # keep the timed step functions' disassembly (hf<form>_<kernel>, hs_<kernel>, and x86-wht's textbook passes
    # pass_<tb16|tb8>_<nat|bal|balS>_1): the twin review asked for it
    awk '/^[0-9a-f]+ <_?((hf[012]|hs)_[A-Za-z0-9_.]+|pass_(tb16|tb8)_(nat|bal|balS)_1[A-Za-z0-9_.]*)>:/{p=1} p&&/^$/{p=0; print ""} p' \
        $BIN/$b.asm > $O/asm/$b.steps.asm
  else echo "BUILD FAILED $b (see $O/buildlogs/$b.buildlog)"; fi
done
for nm in plan_avx2_f32 plan_avx2_f64; do [ -x $BIN/$nm ] || az_stop "plan build $nm failed ($O/buildlogs/$nm.buildlog)"; done
[ -n "$BINS" ] || az_stop "no binary built"
python3 -I asmcount_h512.py $BIN/*_avx512_*.asm > $O/asm_counts.txt 2>&1
grep -E "^==|hf0_(tb8_nat|tb8_balS|g20_nat|tb16_nat|g52_nat) |hs_(tb8_nat|tb8_bal|tb8_balS|g20_nat|g19_nat|tb16_balS|g52_nat) " $O/asm_counts.txt | head -60
rm -f "${BIN:?}"/*.asm

echo "== structure: at 256 bits the plan code must give FFHT's step sequence (pinned fht_avx.c), float and double"
for t in float:plan_avx2_f32 double:plan_avx2_f64; do
  ty=${t%%:*}; b=${t#*:}
  python3 -I check_plan.py "$FF/fht_avx.c" $ty $BIN/$b 1 20 > $O/plan_check_$ty.txt 2>&1; rc=$?
  tail -2 $O/plan_check_$ty.txt
  [ $rc = 0 ] || az_stop "PLAN MISMATCH ($ty): the plan code is not FFHT's algorithm"
done

echo "== exactness gate: every binary, every program (FFHT included), every hybrid in every in-lane form at every"
echo "   threshold candidate, 2^1..2^20 on random integers; broken copies caught"
for b in $BINS; do $BIN/$b check 20 > $O/check_$b.txt 2>&1 & done; wait $(jobs -p)   # in parallel; fix 22 Oct: bare wait hung on >(tee) (nothing is timed yet)
for b in $BINS; do
  echo "$b: $(grep -m1 'sweep total' $O/check_$b.txt | sed 's/CHECK //') / $(grep -m1 'deliberately broken' $O/check_$b.txt | sed 's/.*: //') / $(tail -1 $O/check_$b.txt)"
  grep -q "^ALL PASS" $O/check_$b.txt || az_stop "CHECK FAILED $b (out/check_$b.txt)"
done

NCPU=$(nproc); CORE=${CORE:-$((NCPU - 1))}
SIBS=$(cat /sys/devices/system/cpu/cpu$CORE/topology/thread_siblings_list 2>/dev/null || echo $CORE)
echo "== pinning every timing to CPU $CORE; its SMT sibling(s): $SIBS"
T() { taskset -c $CORE "$@"; }

echo "== tune (textbook only): in-lane form, then the threshold per n for each structure; the circuits inherit them"
export H512_TUNE_MS=${H512_TUNE_MS:-15}
for b in $BINS; do
  az_quiet "tune_$b" "$SIBS"
  T $BIN/$b tune > $O/tune_$b.txt 2>&1 || az_stop "tune failed for $b (out/tune_$b.txt)"
  grep -E "^TUNEFORM score" $O/tune_$b.txt | sed "s/^/$b: /"
  echo "$b: thresholds 8-vector: $(awk '$1=="THR" && $2==0 {printf "%s:%s ", $3, $4}' $O/tune_$b.txt)"
  echo "$b: thresholds 16-vector: $(awk '$1=="THR" && $2==1 {printf "%s:%s ", $3, $4}' $O/tune_$b.txt)"
  # the tuned configuration must pass the gate as the timed programs run it (it is one of the gated candidates)
  H512_TUNE=$O/tune_$b.txt $BIN/$b check 20 > $O/check_tuned_$b.txt 2>&1
  grep -q "^ALL PASS" $O/check_tuned_$b.txt || az_stop "CHECK FAILED with the tuned configuration: $b (out/check_tuned_$b.txt)"
  H512_TUNE=$O/tune_$b.txt $BIN/$b plan 8 9 10 11 12 13 14 15 16 17 18 19 20 > $O/plan_$b.txt 2>&1
done

NPROG=15; SEC_PER=${SEC_PER:-2.5}   # seconds per program and size (estimate for the time budget; raised to the observed
                                    # pace after every run, so a slow host drops the last runs instead of overrunning)
run() { # name binary mode sizes...  -> out/<name>.txt; skipped if it would end after TBUDGET
  local nm=$1 b=$2 mode=$3; shift 3
  case " $BINS " in *" $b "*) ;; *) echo "-- $nm: no binary $b (not built here)"; return 0;; esac
  local est now; est=$(awk -v n=$# -v p=$NPROG -v s=$SEC_PER 'BEGIN{printf "%d", n*p*s + 5}'); now=$(( $(date +%s) - T0 ))
  if [ $((now + est)) -gt $TBUDGET ]; then echo "SKIPPED $nm (time budget: at $now s, needs about $est s, budget $TBUDGET s)"; return 0; fi
  az_quiet "$nm" "$SIBS"
  echo "-- $nm: $b whole $mode $* ($(date -u +%H:%M:%S), at $now s, about $est s)"
  local t1=$(date +%s)
  H512_TUNE=$O/tune_$b.txt T $BIN/$b whole $mode "$@" > $O/$nm.txt 2>&1
  SEC_PER=$(awk -v s=$SEC_PER -v d=$(( $(date +%s) - t1 )) -v n=$# -v p=$NPROG 'BEGIN{o=d/(n*p); printf "%.2f", (o>s?o:s)}')
  echo "   (took $(( $(date +%s) - t1 )) s; pace estimate now $SEC_PER s per program and size)"
  grep "^RATIO" $O/$nm.txt | grep -E " h8-g|h8-h20|h16-g52" | awk '{printf "   %s %-12s / %s median %s best %s\n", $5, $7, $11, $13, $15}'
}

echo "== timing (priority order: gcc f64, gcc f32 at every size; clang at the even sizes; then separate arrays)"
uptime
ALL="8 9 10 11 12 13 14 15 16 17 18 19 20"; EVEN="8 10 12 14 16 18 20"
run whole_same_gcc_avx512_f64 gcc_avx512_f64 same $ALL
run whole_same_gcc_avx512_f32 gcc_avx512_f32 same $ALL
run whole_same_clang_avx512_f64 clang_avx512_f64 same $EVEN
run whole_same_clang_avx512_f32 clang_avx512_f32 same $EVEN
run whole_sep_gcc_avx512_f64 gcc_avx512_f64 separate 12 16 20
run whole_sep_gcc_avx512_f32 gcc_avx512_f32 separate 12 16 20
echo "== load after timing"; uptime
python3 -I summarize_h512.py $O > $O/SUMMARY.md 2>&1; cat $O/SUMMARY.md
echo "DONE $(date -u) after $(( $(date +%s) - T0 )) s"
