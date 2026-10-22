#!/bin/bash
# run.sh -- job 3 of 21-22 Oct 2026: WHT and FFT on an NVIDIA GPU.   UNTESTED ON A GPU WHEN WRITTEN.
# CORRECTED COPY by ay-k0: (1) a missing nvcc now stops the job; (2) VkFFT's hard-coded sm_60..86 list is replaced by
# this GPU's architecture (vkfft_arch_patch.py, copy it next to this file); (3) samples 1000/1001 (every length
# 2..4,096, a fresh VkFFT plan per length and run) run only with FULL=1, VkFFT and cuFFT as SEPARATE processes, so a
# timeout cannot cut the cuFFT half away.
#
# Questions:
#   A. In a WHT row kernel (one block per row, rows from memory), does the 19-line / 52-line / ax-s0 56-line register
#      step beat the textbook? And in the register stage alone (compute-bound ceiling)?           (wht_cuda.cu)
#   B. Patched INTO the strongest public CUDA WHT (Dao-AILab fast-hadamard-transform, per-thread stage), does the
#      step change its time? Where does HadaCore (tensor cores) sit?                               (bench_dao.py)
#   C. cuFFT vs VkFFT at real sizes (fp32/fp64 C2C, R2C, non-power-of-two, 3-D): which is the GPU baseline to beat?
# Every program checks itself first and this script stops on any FAIL (nothing is timed after a failure).
# Run (25-50 min, most of it building Dao twice and VkFFT):
#   bash run.sh
# Runtime: a GPU runtime. T4 (sm_75) runs A, B (no HadaCore) and C. L4 (sm_89) or A100 (sm_80) run everything,
#   and A100 is the one that matters for LLM serving. RAM >= 12 GB. Disk ~3 GB under /content (builds stay outside
#   this folder, so only out/ needs to be copied back).
# Env: SKIP_DAO=1, SKIP_VKFFT=1, FORCE=1 (time even if the GPU is busy).
# Shared preamble (22 Oct 2026): this is ay-k0's corrected copy, installed over the first run.sh
#   (the first run.sh is not published), plus az_pre.sh: the machine and compilers printed first (out/machine.txt) and the
#   host CPU checked quiet (az_quiet) inside gpu_quiet before every timing. Builds stay in /content/k0src, /content/k0build.
set -u
cd "$(dirname "$0")"
W=$PWD; O=$W/out; mkdir -p $O
SRC=${K0SRC:-/content/k0src}; KB=${KBUILD:-/content/k0build}; mkdir -p $SRC $KB; export K0SRC=$SRC KBUILD=$KB
exec > >(tee -a $O/run.log) 2>&1
export PATH=/usr/local/cuda/bin:$PATH
. "$W/az_pre.sh" gpu-wht
echo "== gpu-wht job start $(date -u)"
az_machine
echo "== machine"; nvidia-smi || { echo "NO GPU: this job needs a GPU runtime"; exit 2; }
lscpu | head -20; nproc; free -g
export PATH=/usr/local/cuda/bin:$PATH
command -v nvcc >/dev/null || { echo "no nvcc"; exit 2; }; nvcc --version | tail -2
CAP=$(nvidia-smi --query-gpu=compute_cap --format=csv,noheader | head -1 | tr -d ' .'); echo "compute capability sm_$CAP"
python3 -c "import torch; print('torch', torch.__version__, torch.version.cuda, torch.cuda.is_available())" || echo "no torch (part B skipped)"

gpu_quiet() { # the GPU must be idle (no other compute process, utilisation < 5 %) before any timing
  for k in 1 2 3 4 5 6 7 8 9; do
    apps=$(nvidia-smi --query-compute-apps=pid --format=csv,noheader | wc -l); u=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits | head -1)
    [ "$apps" = 0 ] && [ "${u:-100}" -lt 5 ] && return 0
    echo "GPU busy (apps $apps, util $u %); waiting 20 s"; sleep 20
  done
  [ "${FORCE:-0}" = 1 ] && { echo "GPU BUSY, FORCE=1: timing anyway"; return 0; }
  echo "GPU BUSY: refusing to time"; exit 6
}
_gpu_quiet_only=$(declare -f gpu_quiet | sed '1s/gpu_quiet/_gpu_idle/'); eval "$_gpu_quiet_only"
gpu_quiet() { _gpu_idle "$@"; az_quiet "${1:-gpu timing}"; }   # GPU idle AND host CPU quiet (exit 6 otherwise)

echo "== A. wht_cuda (own row kernel: textbook vs circuits, like for like)"
nvcc -O3 -std=c++17 -lineinfo -arch=sm_$CAP wht_cuda.cu -o $KB/wht_cuda > $O/wht_cuda_build.txt 2>&1; tail -5 $O/wht_cuda_build.txt
if [ ! -x $KB/wht_cuda ]; then echo "BUILD FAILED wht_cuda (part A skipped; B and C still run)"; else
# SASS evidence: FADD / FFMA / FMUL per kernel instance (one instruction per circuit line expected)
cuobjdump -sass $KB/wht_cuda > $KB/wht_cuda.sass 2>/dev/null && awk '/Function :/{f=$3} /FADD/{a[f]++} /FFMA/{m[f]++} /FMUL/{u[f]++} /LDS/{l[f]++} /STS/{s[f]++} /LDL|STL/{sp[f]++}
  END{for (k in a) printf "%-60s FADD %4d FFMA %4d FMUL %3d LDS %4d STS %4d local(spill) %d\n", k, a[k], m[k], u[k], l[k], s[k], sp[k]}' $KB/wht_cuda.sass | sort > $O/sass_counts.txt
head -30 $O/sass_counts.txt
$KB/wht_cuda check > $O/wht_cuda_check.txt 2>&1; tail -3 $O/wht_cuda_check.txt
if grep -q "^ALL PASS" $O/wht_cuda_check.txt; then
  gpu_quiet; $KB/wht_cuda all > $O/wht_cuda_all.txt 2>&1; grep "^RESULT\|^COPY" $O/wht_cuda_all.txt
else echo "wht_cuda CHECK FAILED: part A not timed"; fi
fi

if [ "${SKIP_DAO:-0}" != 1 ] && python3 -c "import torch; assert torch.cuda.is_available()" 2>/dev/null; then
  echo "== B. Dao fast-hadamard-transform (pinned e7706fa), patched copy, HadaCore"
  # Review fix (22 Oct 2026): bench_dao.py builds with torch.utils.cpp_extension.load, which needs ninja; a pip that refuses
  # system installs (an externally managed Python over ssh) used to fail here in silence and part B then died later
  pip -q install ninja >/dev/null 2>&1 || pip -q install --break-system-packages ninja >/dev/null 2>&1
  python3 -c "import torch.utils.cpp_extension as e; e.verify_ninja_availability()" 2>/dev/null && echo "ninja OK" || echo "WARNING: no ninja: part B (Dao JIT build) will fail"
  [ -d $SRC/fast-hadamard-transform ] || git clone -q https://github.com/Dao-AILab/fast-hadamard-transform.git $SRC/fast-hadamard-transform
  (cd $SRC/fast-hadamard-transform && git checkout -q e7706faf8d1c3b9f241e36860640ad1dac644ede && git log -1 --format='Dao FHT %H %cd')
  python3 patch_dao.py $SRC/fast-hadamard-transform $SRC/fast-hadamard-transform-g || { echo "PATCH FAILED"; exit 4; }
  [ -d $SRC/applied-ai ] || git clone -q --depth 1 https://github.com/pytorch-labs/applied-ai.git $SRC/applied-ai
  (cd $SRC/applied-ai && git log -1 --format='HadaCore (applied-ai) %H %cd')
  gpu_quiet; python3 bench_dao.py > $O/bench_dao.txt 2>&1; rc=$?
  grep "^CHECK\|^ALL\|^RESULT\|^NOTE\|built\|HadaCore" $O/bench_dao.txt | head -150
  [ $rc = 3 ] && { echo "Dao/HadaCore CHECK FAILED: their timings were not taken"; }
fi

if [ "${SKIP_VKFFT:-0}" != 1 ]; then
  echo "== C. cuFFT vs VkFFT (VkFFT's own test suite, CUDA backend, with its cuFFT benchmark; pinned 066a17c)"
  command -v cmake >/dev/null || pip -q install cmake
  [ -d $SRC/VkFFT ] || git clone -q https://github.com/DTolm/VkFFT.git $SRC/VkFFT
  (cd $SRC/VkFFT && git checkout -q 066a17c17068c0f11c9298d848c2976c71fad1c1 2>/dev/null; git log -1 --format='VkFFT %H %cd')
  python3 $W/vkfft_arch_patch.py $SRC/VkFFT/CMakeLists.txt $CAP || { echo "VkFFT arch patch FAILED"; }
  # fix 22 Oct 2026: CUDA 13 headers make cuCtxCreate_v4 take a CUctxCreateParams* second argument
  grep -q "CUDA_VERSION >= 13000" $SRC/VkFFT/VkFFT_TestSuite.cpp 2>/dev/null || sed -i 's|cuCtxCreate_v4(&vkGPU->context, 0, (int)vkGPU->device)|cuCtxCreate_v4(\&vkGPU->context, NULL, 0, (int)vkGPU->device) /* CUDA_VERSION >= 13000 */|' $SRC/VkFFT/VkFFT_TestSuite.cpp
  cmake -S $SRC/VkFFT -B $KB/vkfft -DVKFFT_BACKEND=1 -Dbuild_VkFFT_cuFFT_benchmark=ON -DCMAKE_CUDA_ARCHITECTURES=$CAP \
        -DCMAKE_BUILD_TYPE=Release > $O/vkfft_cmake.txt 2>&1 && make -C $KB/vkfft -j$(nproc) > $O/vkfft_make.txt 2>&1
  if [ -x $KB/vkfft/VkFFT_TestSuite ]; then
    # 0 fp32 C2C 1-D batched, 1 fp64 C2C, 3 fp32 3-D, 6 fp32 R2C, 7 fp32 Bluestein (non-power-of-two), 8 fp64 Bluestein,
    # 1000 / 1001 every length 2..4096 (fp32 / fp64). VkFFT checks nothing here: its precision tests need FFTW
    # (-test); correctness of both libraries is VkFFT's own published test record, so mark these TIMING ONLY.
    for s in 0 1 3 6 7 8; do
      gpu_quiet; echo "-- sample $s ($(date -u +%H:%M:%S))"
      timeout 900 $KB/vkfft/VkFFT_TestSuite -d 0 -o $O/vkfft_s$s.txt -vkfft $s -cufft $s > $O/vkfft_s${s}_stdout.txt 2>&1
      echo "   exit $?"; tail -4 $O/vkfft_s${s}_stdout.txt
    done
    if [ "${FULL:-0}" = 1 ]; then   # every length 2..4096: compare on the lengths BOTH halves reached
      for s in 1000 1001; do for lib in vkfft cufft; do
        gpu_quiet; echo "-- sample $s $lib ($(date -u +%H:%M:%S))"
        timeout 1800 $KB/vkfft/VkFFT_TestSuite -d 0 -o $O/${lib}_s$s.txt -$lib $s > $O/${lib}_s${s}_stdout.txt 2>&1
        echo "   exit $? (124 = timed out; partial file kept)"; tail -2 $O/${lib}_s${s}_stdout.txt
      done; done
    fi
  else echo "VkFFT BUILD FAILED (see out/vkfft_make.txt)"; tail -20 $O/vkfft_make.txt; fi
fi
echo "DONE $(date -u)"
