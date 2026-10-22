#!/bin/bash
# ay-h0 wave 16 (critic of ax-h0), Colab GPU job: the non-power-of-two part of Dao's fast-hadamard-transform
# (12/20/28/40N; LLaMA-3 / Mistral 14,336 = 28 x 512) against THREE rivals, same matrices, exact:
#   orig : Dao's dense signed sums (commit e7706faf)
#   cse  : ax-h0's greedy common-subexpression circuit (drop-in header)
#   grp  : the published structured form, groups of 4 (arXiv 2601.22347 App. A.1 style) (drop-in header)
#   mm   : QuaRot style: Dao's power-of-two transform, then the K x K matmul (tensor cores in fp16/bf16)
# Extends ax-h0's earlier job gpu-hk (same bench, CUDA events, 20 warm-up + 200 calls, median of 7 rounds).
# Needs: any NVIDIA GPU runtime (A100 or L4 preferred; T4 fine for a first pass), ~35 min (three CUDA builds).
# Starts from a clean Colab/Ubuntu runtime; writes everything to out/.  Nothing else may run while it times.
# Shared preamble (22 Oct 2026; ay-k0 fix 17 for gpu-hk, which this job extends): machine and compilers first (az_pre.sh);
#   the clones and the three CUDA builds live in $AZ_BUILD/src (= /content/build/gpu-hk3/src, through the symlink
#   src), not in this folder; a CORRECTNESS GATE before any timing: every variant runs bench.py with
#   BENCH_CHECK_ONLY=1 and compare3.py must print PASS for every case of cse, grp and mm; the GPU must be idle and the
#   host quiet (az_quiet) before each timed run. bench.py: BENCH_CHECK_ONLY added (bench.py.orig). Original: run.sh.orig.
set -u; cd "$(dirname "$0")"; W=$PWD; mkdir -p out; exec > >(tee out/log.txt) 2>&1
. ./az_pre.sh gpu-hk3
az_machine
date; lscpu | head -20; nproc; free -g; nvidia-smi || { echo "NO GPU: this job needs a GPU runtime"; exit 1; }
gpu_idle() { local k a u; for k in 1 2 3 4 5 6 7 8 9; do a=$(nvidia-smi --query-compute-apps=pid --format=csv,noheader | wc -l)
  u=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits | head -1); [ "$a" = 0 ] && [ "${u:-100}" -lt 5 ] && return 0
  echo "GPU busy (apps $a, util $u %); waiting 20 s"; sleep 20; done
  [ "${FORCE:-0}" = 1 ] && { echo "GPU BUSY, FORCE=1: timing anyway"; return 0; }; echo "GPU BUSY: refusing to time"; exit 6; }
nvcc --version || true; python3 -c "import torch;print('torch',torch.__version__,'cuda',torch.version.cuda,torch.cuda.get_device_name())"
COMMIT=e7706faf8d1c3b9f241e36860640ad1dac644ede     # Dao-AILab/fast-hadamard-transform, read on 21 Oct 2026
rm -rf "${AZ_BUILD:?}/src" src && mkdir -p "$AZ_BUILD/src" && ln -sfn "$AZ_BUILD/src" src && git clone -q https://github.com/Dao-AILab/fast-hadamard-transform.git src/orig && (cd src/orig && git checkout -q $COMMIT && git log -1 --format='%H %cd')
cp -r src/orig src/cse; cp -r src/orig src/grp
python3 gen_special_cse.py src/orig/csrc/code_gen.py src/cse/csrc/fast_hadamard_transform_special.h | tee out/cse_counts.txt || exit 1
python3 gen_special_grp.py src/orig/csrc/code_gen.py src/grp/csrc/fast_hadamard_transform_special.h | tee out/grp_counts.txt || exit 1
CC_ARCH=$(python3 -c "import torch;m,n=torch.cuda.get_device_capability();print(f'{m}.{n}')")
export TORCH_CUDA_ARCH_LIST="$CC_ARCH" MAX_JOBS=$(nproc) FAST_HADAMARD_TRANSFORM_FORCE_BUILD=TRUE
pip install -q ninja packaging || pip install -q --break-system-packages ninja packaging || true   # review fix: externally managed pip
for v in orig cse grp; do  # build in place; if setup.py refuses, build a wheel and unpack it into src/$v/site
  if ! (cd src/$v && python3 setup.py build_ext --inplace > $W/out/build_$v.txt 2>&1); then
    echo "build_ext $v failed, trying a wheel"; tail -5 out/build_$v.txt
    (cd src/$v && pip wheel --no-build-isolation --no-deps -w ../wheel_$v . >> $W/out/build_$v.txt 2>&1) || { echo "build $v FAILED"; tail -40 out/build_$v.txt; exit 1; }
    mkdir -p src/$v/site && (cd src/$v/site && python3 -m zipfile -e ../../wheel_$v/*.whl .)
  fi
done
path() { if [ -d src/$1/site ]; then echo src/$1/site; else echo src/$1; fi; }
export HAD_CODEGEN=src/orig/csrc/code_gen.py
echo "== correctness gate (fixed fp32 input, outputs only; nothing timed yet)"
for v in orig cse grp mm; do P=$(path $v); [ $v = mm ] && P=$(path orig)
  BENCH_CHECK_ONLY=1 PYTHONPATH=$P python3 bench.py $v out/chk_${v}.json > out/chk_${v}.txt 2>&1 || { tail -5 out/chk_${v}.txt; az_stop "bench.py $v check-only run failed"; }
done
python3 compare3.py out/chk_orig.json out/chk_cse.json out/chk_grp.json out/chk_mm.json > out/check.md 2>&1; rc=$?; grep '^check' out/check.md
{ [ $rc = 0 ] && grep -q '^check' out/check.md && ! grep -q -E 'FAIL|MISSING' out/check.md; } || az_stop "a variant does not equal Dao's original (out/check.md)"
for round in 1 2; do                        # two rounds, variants alternating; mm uses the orig build
  for v in orig cse grp mm; do
    P=$(path $v); [ $v = mm ] && P=$(path orig)
    gpu_idle; az_quiet "bench $v round $round"
    PYTHONPATH=$P python3 bench.py $v out/res_${v}.json | tee -a out/bench_${v}.txt
  done
done
python3 compare3.py out/res_orig.json out/res_cse.json out/res_grp.json out/res_mm.json | tee out/compare.md
date
