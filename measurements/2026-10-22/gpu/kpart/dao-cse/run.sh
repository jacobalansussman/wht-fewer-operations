#!/bin/bash
# ax-13 wave 16, Colab GPU job: Dao-AILab/fast-hadamard-transform's 12/20/28/40N kernels as shipped (dense signed sums in
# hadamard_mult_thread_K) against the same build with ax-13's drop-in fast_hadamard_transform_special.h: shared-
# subexpression circuits for the SAME matrices (12: 48 adds vs 132; 20: 112 vs 380; 28: 235 vs 756; 40 = [[A,A],[A,-A]]:
# 276 vs 1,560), checked exact on the Mac (../generator/check_dropin.txt).  Based on ax-h0's gpu-hk kit.
# Needs: a GPU runtime (T4 is fine for a first pass; A100 / L4 / H100 better), ~25 min (two CUDA builds).
# Starts from a clean runtime; writes everything to out/.  Nothing else may run while it times.
# Shared preamble (22 Oct 2026): machine and compilers first (az_pre.sh, out/machine.txt); the clones and CUDA builds live in
#   $AZ_BUILD/src (= /content/build/gpu-dao/src, reached through the symlink src), not in this folder; a CORRECTNESS
#   GATE before any timing: both builds run bench.py with BENCH_CHECK_ONLY=1 (outputs on the fixed input only) and
#   compare.py must print PASS for every case; the GPU must be idle and the host quiet (az_quiet) before each timed
#   run. bench.py: BENCH_CHECK_ONLY added (bench.py.orig). Original: run.sh.orig.
set -u; cd "$(dirname "$0")"; W=$PWD; mkdir -p out; exec > >(tee out/log.txt) 2>&1
. ./az_pre.sh gpu-dao
az_machine
date; lscpu | head -20; nproc; free -g; nvidia-smi || { echo "NO GPU: this job needs a GPU runtime"; exit 1; }
gpu_idle() { local k a u; for k in 1 2 3 4 5 6 7 8 9; do a=$(nvidia-smi --query-compute-apps=pid --format=csv,noheader | wc -l)
  u=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits | head -1); [ "$a" = 0 ] && [ "${u:-100}" -lt 5 ] && return 0
  echo "GPU busy (apps $a, util $u %); waiting 20 s"; sleep 20; done
  [ "${FORCE:-0}" = 1 ] && { echo "GPU BUSY, FORCE=1: timing anyway"; return 0; }; echo "GPU BUSY: refusing to time"; exit 6; }
nvcc --version || true; python3 -c "import torch;print('torch',torch.__version__,'cuda',torch.version.cuda,torch.cuda.get_device_name())"
COMMIT=e7706faf8d1c3b9f241e36860640ad1dac644ede     # Dao-AILab/fast-hadamard-transform, read on 21 Oct 2026
rm -rf "${AZ_BUILD:?}/src" src && mkdir -p "$AZ_BUILD/src" && ln -sfn "$AZ_BUILD/src" src && git clone -q https://github.com/Dao-AILab/fast-hadamard-transform.git src/orig && (cd src/orig && git checkout -q $COMMIT && git log -1 --format='%H %cd')
cp -r src/orig src/cse
# the drop-in replaces the generated header; keep Dao's copyright banner on top
{ head -9 src/orig/csrc/fast_hadamard_transform_special.h; cat dao_fast_hadamard_transform_special.h; } > src/cse/csrc/fast_hadamard_transform_special.h
grep -c "__device__" src/orig/csrc/fast_hadamard_transform_special.h src/cse/csrc/fast_hadamard_transform_special.h
CC_ARCH=$(python3 -c "import torch;m,n=torch.cuda.get_device_capability();print(f'{m}.{n}')")
export TORCH_CUDA_ARCH_LIST="$CC_ARCH" MAX_JOBS=$(nproc) FAST_HADAMARD_TRANSFORM_FORCE_BUILD=TRUE
pip install -q ninja packaging || pip install -q --break-system-packages ninja packaging || true   # review fix: externally managed pip
for v in orig cse; do
  if ! (cd src/$v && python3 setup.py build_ext --inplace > $W/out/build_$v.txt 2>&1); then
    echo "build_ext $v failed, trying a wheel"; tail -5 out/build_$v.txt
    (cd src/$v && pip wheel --no-build-isolation --no-deps -w ../wheel_$v . >> $W/out/build_$v.txt 2>&1) || { echo "build $v FAILED"; tail -40 out/build_$v.txt; exit 1; }
    mkdir -p src/$v/site && (cd src/$v/site && python3 -m zipfile -e ../../wheel_$v/*.whl .)
  fi
done
P_orig=src/orig; [ -d src/orig/site ] && P_orig=src/orig/site
P_cse=src/cse;   [ -d src/cse/site ] && P_cse=src/cse/site
echo "== correctness gate (fixed fp32 input, outputs only; nothing timed yet)"
for v in orig cse; do P=$P_orig; [ $v = cse ] && P=$P_cse
  BENCH_CHECK_ONLY=1 PYTHONPATH=$P python3 bench.py $v out/chk_${v}.json > out/chk_${v}.txt 2>&1 || { tail -5 out/chk_${v}.txt; az_stop "bench.py $v check-only run failed"; }
done
python3 compare.py out/chk_orig.json out/chk_cse.json > out/check.md 2>&1; rc=$?; grep '^check' out/check.md
{ [ $rc = 0 ] && grep -q '^check' out/check.md && ! grep -q -E 'FAIL|MISSING' out/check.md; } || az_stop "the drop-in does not equal Dao's original (out/check.md)"
for v in orig cse orig cse; do
  P=$P_orig; [ $v = cse ] && P=$P_cse
  gpu_idle; az_quiet "bench $v"
  PYTHONPATH=$P python3 bench.py $v out/res_${v}.json | tee -a out/bench_${v}.txt
done
python3 compare.py out/res_orig.json out/res_cse.json | tee out/compare.md
date
