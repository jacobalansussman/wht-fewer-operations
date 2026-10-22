#!/bin/bash
# run.sh -- job 1 of 21-22 Oct 2026: the x86 redo of the 5/6 and 3/4 Walsh-Hadamard steps.
#
# Question: on an x86 core, does the 3/4 family's 16-point step (52 lines, one FMA or add each), ax-s0's depth-limited
#   56-line step, or the 5/6 step (19 lines; 20-op halved form) beat the textbook (64 / 24 adds) -- in one L1 pass,
#   with 1-4 independent blocks interleaved, on 16 and 32 registers, with gcc and clang -- and does a whole transform
#   2^6..2^24 beat FFHT (FALCONN-LIB, commit fba727a3) and our own intrinsics textbook?
#   NEW fair rival: "textbook-bal", the textbook with half its adds issued as FMA by an opaque 1. On cores whose adds
#   and FMAs use different pipes (AMD Zen 2-5; Intel Golden Cove and later) this is the textbook's best form.
#
# Run on an x86-64 Linux machine (it takes 30-45 min in the default MODE=quick):
#   bash run.sh
#   results land in out/ (the runs of 21-22 Oct 2026 are in ../runs/)
# Env: MODE=quick|full (full: every binary, every size 2^6..2^24, both array modes, interleave 2 inside whole
#      transforms: ~2 h); CORE=<cpu to pin> (default: the last CPU); FORCE=1 times even if the machine is busy.
# Runtime: any Colab CPU runtime works; the AVX-512 half runs only if the CPU has avx512f + avx512vl.
#   Most informative, in order: (1) an AMD EPYC (Zen 2/3/4: separate add and FMA pipes), (2) an Intel Xeon with
#   AVX-512 (Skylake / Cascade Lake: shared pipes, 32 registers), (3) the plain 2.2 GHz Xeon of 11 October (Broadwell,
#   16 registers, no AVX-512: a repeat of the old loss). RAM: < 2 GB (quick), < 4 GB (full). No GPU.
# Shared preamble (22 Oct 2026): az_pre.sh prints the machine first and keeps FFHT and the binaries OUTSIDE this folder
#   ($AZ_BUILD = /content/build/x86-wht); az_quiet (per-process rule on the pinned CPU and its SMT sibling) replaces
#   the old whole-machine gate; ay-k0 fix 13 (the "no clang" message). Original: run.sh.orig.
set -u
cd "$(dirname "$0")"
W=$PWD; O=$W/out; mkdir -p $O
exec > >(tee -a $O/run.log) 2>&1
. "$W/az_pre.sh" x86-wht
MODE=${MODE:-quick}
echo "== x86-wht job, MODE=$MODE, start $(date -u)"
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
# Review fix (22 Oct 2026): install only what is missing. The old line asked apt for python3 and git as well whenever clang was
# missing (always, on Colab), and "apt-get install python3" after an update can replace the runtime's own python3 [guess].
pk=""; command -v gcc >/dev/null && command -v make >/dev/null || pk="$pk build-essential"; command -v clang >/dev/null || pk="$pk clang"
command -v git >/dev/null || pk="$pk git"; command -v python3 >/dev/null || pk="$pk python3"
if [ -n "$pk" ]; then echo "apt-get install$pk"; apt-get update -qq >/dev/null 2>&1; apt-get install -y -qq $pk >/dev/null 2>&1; fi
command -v taskset >/dev/null || apt-get install -y -qq util-linux >/dev/null 2>&1
gcc --version | head -1; if command -v clang >/dev/null; then clang --version | head -1; else echo "no clang (gcc only)"; fi
az_versions > $O/tools.txt 2>&1
cd "$AZ_BUILD"
if [ ! -d FFHT ]; then git clone -q https://github.com/FALCONN-LIB/FFHT.git FFHT; fi
(cd FFHT && git checkout -q fba727a3ff72c862260460631ae1cc8e3e44e861 && git log -1 --format='FFHT %H %cd') || { echo "FFHT checkout failed"; exit 2; }
HAVE512=0; echo "$FLAGS" | grep -qw avx512f && echo "$FLAGS" | grep -qw avx512vl && HAVE512=1

cd "$W"; ln -sfn "$AZ_BUILD/FFHT" FFHT   # a symlink: the fetch copies the link, not the clone
BIN=$AZ_BUILD/bin
echo "== build (binaries in $BIN, outside the job folder)"
mkdir -p "$BIN" "$O/buildlogs"
CFGS=("avx2_f32:0:-mavx2 -mfma" "avx2_f64:2:-mavx2 -mfma")
[ $HAVE512 = 1 ] && CFGS+=("avx2r32_f32:0:-mavx2 -mfma -mavx512f -mavx512vl" "avx512_f32:1:-mavx2 -mfma -mavx512f -mavx512vl" "avx512_f64:3:-mavx2 -mfma -mavx512f -mavx512vl")
BINS=""
for cc in gcc clang; do
  command -v $cc >/dev/null || continue
  for cfg in "${CFGS[@]}"; do
    nm=${cfg%%:*}; rest=${cfg#*:}; xt=${rest%%:*}; fl=${rest#*:}
    if $cc -O3 $fl -DXT=$xt -DWITH_FFHT -IFFHT bench_k0.c FFHT/fht.c FFHT/fast_copy.c -o $BIN/${cc}_$nm -lm 2> $O/buildlogs/${cc}_$nm.buildlog; then
      BINS="$BINS ${cc}_$nm"; echo "built ${cc}_$nm ($cc -O3 $fl -DXT=$xt)"
      objdump -d --no-show-raw-insn $BIN/${cc}_$nm > $BIN/${cc}_$nm.asm 2>/dev/null
    else echo "BUILD FAILED ${cc}_$nm (see $O/buildlogs/${cc}_$nm.buildlog)"; fi
  done
done
[ -n "$BINS" ] || az_stop "no binary built"
python3 asmcount.py $BIN/*.asm > $O/asm_counts.txt 2>&1; head -80 $O/asm_counts.txt; rm -f "${BIN:?}"/*.asm

echo "== correctness: every binary must print ALL PASS (and catch the broken kernel) before any timing"
for b in $BINS; do
  $BIN/$b check 20 > $O/check_$b.txt 2>&1; echo "$b: $(tail -1 $O/check_$b.txt)"
  grep -q "^ALL PASS" $O/check_$b.txt || { echo "CHECK FAILED $b: stopping, nothing timed"; exit 3; }
done

# ---- quiet-machine gate: measure busy CPUs over 3 s from /proc/stat; wait up to 3 min; refuse to time if busy ----
busy_cpus() { local a b; a=($(head -1 /proc/stat)); sleep 3; b=($(head -1 /proc/stat))
  local it=0 tt=0 i; for i in 1 2 3 4 5 6 7 8; do tt=$((tt + ${b[$i]} - ${a[$i]})); done; it=$(( (${b[4]} - ${a[4]}) + (${b[5]} - ${a[5]}) ))
  awk -v t=$tt -v i=$it -v n=$(nproc) 'BEGIN{ if (t<=0) print 0; else printf "%.2f", (t-i)/t*n }'; }
quiet() {
  for k in 1 2 3 4 5 6 7 8 9; do
    bc=$(busy_cpus); echo "busy CPUs over 3 s: $bc (load $(cut -d' ' -f1-3 /proc/loadavg))"
    awk -v b=$bc 'BEGIN{exit !(b < 0.5)}' && return 0
    top -b -n 1 | head -15; sleep 20
  done
  [ "${FORCE:-0}" = 1 ] && { echo "BUSY but FORCE=1: timing anyway (mark these numbers)"; return 0; }
  echo "MACHINE BUSY for 3 minutes: refusing to time (set FORCE=1 to override)"; exit 6
}
NCPU=$(nproc); CORE=${CORE:-$((NCPU - 1))}
SIBS=$(cat /sys/devices/system/cpu/cpu$CORE/topology/thread_siblings_list 2>/dev/null || echo $CORE)
quiet() { az_quiet "${1:-timing}" "$SIBS"; }   # shared preamble: replaces the quiet() above; exit 6 if busy (FORCE=1 overrides)
echo "== pinning every timing to CPU $CORE; its SMT sibling(s): $(cat /sys/devices/system/cpu/cpu$CORE/topology/thread_siblings_list 2>/dev/null)"
T() { taskset -c $CORE "$@"; }
run() { # name, then the binary's arguments; output to out/<name>.txt
  local nm=$1; shift; quiet "$nm"; echo "-- $nm: $* ($(date -u +%H:%M:%S))"; T "$@" > $O/$nm.txt 2>&1; grep "^RATIO" $O/$nm.txt | sed 's/^/   /'
}

echo "== timing ($MODE)"
uptime
if [ "$MODE" = full ]; then PBINS="$BINS"; WBINS="$BINS"; WSIZES="6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24"; SSIZES="10 12 14 16 18 20 22 24"; IS="1 2 3 4"
else
  PBINS=""; for b in gcc_avx2_f32 clang_avx2_f32 gcc_avx2r32_f32 gcc_avx512_f32 clang_avx512_f32 gcc_avx2_f64 gcc_avx512_f64; do case " $BINS " in *" $b "*) PBINS="$PBINS $b";; esac; done
  WBINS=""; for b in gcc_avx2_f32 clang_avx2_f32 gcc_avx512_f32; do case " $BINS " in *" $b "*) WBINS="$WBINS $b";; esac; done
  WSIZES="6 8 10 12 14 16 18 20"; SSIZES="12 16 20 24"; IS="1 2 3 4"
fi
for b in $PBINS; do
  for I in $IS; do run pass16_I${I}_$b $BIN/$b pass 16 $I; run pass8_I${I}_$b $BIN/$b pass 8 $I; done
  for I in 1 2; do run regs16_I${I}_$b $BIN/$b regs 16 $I; done
  for I in $IS; do run regs8_I${I}_$b $BIN/$b regs 8 $I; done
done
for b in $WBINS; do
  run whole_same_$b $BIN/$b whole same $WSIZES
  run whole_sep_$b $BIN/$b whole separate $SSIZES
  if [ "$MODE" = full ]; then export WG_WHOLE_I=2; run whole_same_I2_$b $BIN/$b whole same $WSIZES; unset WG_WHOLE_I; fi
done
echo "== load after timing"; uptime
python3 summarize.py $O > $O/SUMMARY.md 2>&1; cat $O/SUMMARY.md
rm -f FFHT   # the symlink only; the clone stays in $AZ_BUILD on the Colab
echo "DONE $(date -u)"
