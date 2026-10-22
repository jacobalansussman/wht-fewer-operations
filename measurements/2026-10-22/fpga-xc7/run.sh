#!/bin/bash
# run.sh (ax-k1, wave 16): the FPGA Colab kit.  One command per job; every job starts from a clean Ubuntu x86-64
# runtime, installs the SAME tool builds as the Mac (setup_tools.sh), runs the self-test, then its work.
#
#   bash run.sh selftest            reproduce wave-14 figures (UP5K, ECP5-25k, CrossLink-NX; 5 seeds each)   ~10 min
#   bash run.sh xc7                 openXC7 place and route of the Xilinx designs in designs/xc7 (aj-5, ax-7, as-4)
#   bash run.sh fme                 xk265 FME: whole FME on the ECP5-85F + interpolator / FME on Xilinx 7 (designs/fme)
#   bash run.sh farm DIR [opts]     any design folder in our format (DIR/runs.txt; see tools/farm.py)
#   bash run.sh all                 selftest, xc7, fme in that order
# Environment: SEEDS (default 5), SLOTS (tool runs at once; default min(cores, RAM/MEM_PER_RUN)), MEM_PER_RUN (GB,
#              default 2; the fme job uses 8), ONLY=tag1,tag2 (a subset of runs.txt lines), TOOLS (/content/fpga-tools).
# Run on a fresh Ubuntu x86-64 machine:  bash run.sh xc7     (the job of 22 Oct 2026; see README.md)
#   (the jobs selftest, fme and all need files that are not in this repository)
# Output: out/ (run.log, selftest.jsonl, <job>/farm.jsonl, <job>/farm_table.md, logs).  Nothing else runs on the
# machine while a job runs (the job checks the load first and waits up to 10 minutes for other heavy processes).
# Shared preamble (22 Oct 2026): this is ay-k1's corrected copy (MUST fixes 1-4, SHOULD fixes 5-6;
#   the first run.sh is not published), plus ay-k1's fix 9b: the FIRST job on a runtime runs the FULL self-test (--xc7,
#   every chip) instead of the quick one and leaves a marker in the tools folder; later jobs on the same runtime run
#   the quick gate. Machine first: also writes out/machine.txt (az_pre.sh). No quiet gate: place-and-route figures do
#   not depend on load (same seed, same result); the job records what else runs and refuses only on low memory.
set -u
cd "$(dirname "$0")"
KIT=$PWD
JOB=${1:-selftest}; shift || true
mkdir -p out
exec > >(tee -a out/run_$JOB.log) 2>&1

. "$KIT/az_pre.sh" "fpga-$JOB"; az_machine > /dev/null
echo "== ax-k1 FPGA kit: job $JOB   $(date -u)"
echo "== machine"; lscpu | head -20; echo "nproc $(nproc)"; free -g; (nvidia-smi 2>/dev/null || echo "no GPU"); (gcc --version 2>/dev/null | head -1); (python3 --version); head -3 /etc/os-release
# ay-k1: place-and-route figures do not depend on the machine's load (same seed, same result), so another job only costs
# time and memory.  Record what else runs (top, not ps pcpu, which is a lifetime average) and refuse only when memory is short.
echo "== other processes using CPU now (recorded; FPGA figures do not depend on load)"
top -b -n 1 | sed -n '7,14p'
avail=$(free -g | awk '/Mem/{print $7}')
need=${MIN_FREE_GB:-6}
[ "${avail:-0}" -lt "$need" ] && { echo "REFUSED: only ${avail} GB available (need ${need}; set MIN_FREE_GB to override)"; exit 9; }

bash "$KIT/setup_tools.sh" || { echo "tool setup failed"; exit 2; }
. "${TOOLS:-/content/fpga-tools}/env.sh"
export FARM_DIRECT=1
export FARM_WORK=${FARM_WORK:-/content/fpga-work}   # netlists and per-seed logs stay on the Colab (not fetched back)
SEEDS=${SEEDS:-5}
NP=$(nproc)

selftest() {
  echo "== self-test $(date -u)"
  python3 -B tools/selftest.py ${1:-} --jobs $NP --work $FARM_WORK/selftest --out out/selftest.jsonl
  local rc=$?
  echo "self-test exit $rc"
  return $rc
}

gate() {  # ay-k1: run the self-test; 0 = go, 1 = stop.  (ay-k1 9b): full self-test once per runtime
  local M=${TOOLS:-/content/fpga-tools}/SELFTEST_FULL_DONE args="$*"
  if [ ! -f "$M" ]; then echo "first job on this runtime: FULL self-test (--xc7) instead of '$args'"; args="--xc7"; fi
  selftest "$args"; local rc=$?
  if [ ! -f "$M" ] && { [ $rc = 0 ] || [ $rc = 3 ]; }; then echo "full self-test exit $rc on $(hostname) $(date -u)" > "$M"; cp "$M" out/; fi
  [ $rc = 0 ] && return 0
  [ $rc = 3 ] && { echo "SELF-TEST: synthesis differs from the Mac's; running anyway. Do NOT mix this machine's rows with the Mac's."; return 0; }
  return 1
}

farm() {  # farm DIR MEM_PER_RUN [extra]
  local dir=$1 mem=$2; shift 2
  echo "== farm $dir $(date -u)"
  python3 -B tools/farm.py "$dir" --seeds $SEEDS --mem-per-run ${MEM_PER_RUN:-$mem} ${SLOTS:+--slots $SLOTS} \
      ${ONLY:+--only $ONLY} --out out/$(basename $dir) "$@"
}

case $JOB in
  selftest) selftest ;;
  # ay-k1: gate() stops only on FAIL (exit 1); a synthesis difference from the Mac (exit 3) lets the job run, stamped.
  # published copy: the self-test needs reference designs that are not in this repository, so it runs only with
  # SELFTEST=1 (the run of 22 Oct 2026 ran it; its rows are in results/selftest_ax7_*.jsonl)
  xc7)      if [ "${SELFTEST:-0}" = 1 ]; then gate "--quick --xc7" || exit 3; fi; farm designs/xc7 3 ;;
  fme)      gate "--quick --xc7" || exit 3; farm designs/fme 8 --timeout 14400 ;;   # 6 of its lines are openXC7
  farm)     [ $# -ge 1 ] || { echo "usage: run.sh farm DIR [opts]"; exit 1; }
            gate "--quick --xc7" || exit 3; d=$1; shift; farm "$d" 2 "$@" ;;
  all)      gate --xc7 || exit 3; farm designs/xc7 3; farm designs/fme 8 --timeout 14400 ;;
  *) echo "unknown job $JOB"; exit 1 ;;
esac
echo "== END $(date -u)"
