# az_pre.sh -- shared preamble of the timing jobs of 22 Oct 2026, run on rented Colab machines.
# Copied into every job folder that uses it (a job folder is copied to the Colab on its own). Source it from run.sh,
# in the main shell (not in a subshell or a pipe, or its exits only leave the subshell):
#     . "$(dirname "$0")/az_pre.sh" <job-name>
# It sets and provides:
#   AZ_DIR    the job folder;   AZ_OUT  = $AZ_DIR/out (created)
#   AZ_BUILD  = /content/build/<job-name> (created): builds, clones, venvs and downloads go HERE, outside the job folder,
#             so that only out/ needs to be copied back from the machine. Override with BUILD=/path.
#   az_machine          prints date, uname, lscpu, nproc, free -g, nvidia-smi (if present), compiler versions, load;
#                       also writes them to out/machine.txt. Call it FIRST.
#   az_versions         compiler / tool versions again (call it after the job installed its tools).
#   az_quiet LABEL [CPUS]  refuses to time on a busy machine: az_quiet.py over 3 s (rule: no other process above
#                       QUIET_PCT=5 % of a core, the CPUs used not above 5 % busy, the machine not above max(0.3, 5 % of
#                       nproc) cores busy); waits up to QUIET_WAIT=180 s, then exits the job with code 6 unless FORCE=1.
#                       Every check is recorded in out/quiet.log. CPUS = the CPUs the timing pins to (default: all).
#   az_stop MSG         prints "STOP: MSG: nothing (more) is timed" and exits 3 (use when a correctness check fails).
AZ_JOB=${1:-job}
AZ_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
AZ_OUT=$AZ_DIR/out; mkdir -p "$AZ_OUT"
if [ -n "${BUILD:-}" ]; then AZ_BUILD=$BUILD
elif [ -d /content ]; then AZ_BUILD=/content/build/$AZ_JOB
else AZ_BUILD=${TMPDIR:-/tmp}/az-build/$AZ_JOB; fi
mkdir -p "$AZ_BUILD"
az_versions() {
  local c
  for c in gcc g++ clang clang++ nvcc cmake python3; do
    if command -v $c >/dev/null 2>&1; then echo "-- $c: $($c --version 2>&1 | grep -m1 -E '[0-9]+\.[0-9]+' )"; else echo "-- $c: not installed"; fi
  done
  if command -v nvcc >/dev/null 2>&1; then nvcc --version 2>&1 | tail -2; fi
}
az_machine() {
  {
    echo "== machine ($AZ_JOB) $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    uname -a; echo; lscpu 2>/dev/null || cat /proc/cpuinfo | head -30; echo
    echo "nproc: $(nproc 2>/dev/null)"; free -g 2>/dev/null
    if command -v nvidia-smi >/dev/null 2>&1; then nvidia-smi 2>&1 | head -25
      nvidia-smi --query-gpu=name,driver_version,memory.total,clocks.max.sm --format=csv 2>&1
    else echo "nvidia-smi: not present (no GPU)"; fi
    echo "== compilers and tools"; az_versions
    echo "== load: $(cat /proc/loadavg 2>/dev/null)"; echo "== job folder $AZ_DIR, build folder $AZ_BUILD"
  } 2>&1 | tee -a "$AZ_OUT/machine.txt"
}
az_quiet() {
  local label=${1:-timing} cpus=${2:-} rc
  if [ -n "$cpus" ]; then python3 -I "$AZ_DIR/az_quiet.py" --label "$label" --cpus "$cpus" --log "$AZ_OUT/quiet.log"; rc=$?
  else python3 -I "$AZ_DIR/az_quiet.py" --label "$label" --log "$AZ_OUT/quiet.log"; rc=$?; fi
  [ $rc = 0 ] && return 0
  if [ "${FORCE:-0}" = 1 ]; then echo "az_quiet: BUSY but FORCE=1: timing anyway ($label); mark these numbers" | tee -a "$AZ_OUT/quiet.log"; return 0; fi
  echo "az_quiet: MACHINE BUSY for ${QUIET_WAIT:-180} s before '$label': refusing to time (exit 6; FORCE=1 overrides)" | tee -a "$AZ_OUT/quiet.log"
  exit 6
}
az_stop() { echo "STOP: $*: nothing (more) is timed" | tee -a "$AZ_OUT/STOP.txt"; exit 3; }
