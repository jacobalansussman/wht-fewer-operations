# gpu/kpart: a separate test, the non-power-of-two rotation of language models

This folder is **not about the circuits of this repository**. Some language models are quantised with a Hadamard
rotation of a length that is not a power of two, for example 14,336 = 28 x 512 (LLaMA-3.1-8B, Mistral-7B) or
28,672 = 28 x 1,024 (LLaMA-3.3-70B). Dao-AILab's fast-hadamard-transform library does such a rotation as a
power-of-two transform plus a fixed 12-, 20-, 28- or 40-point Hadamard matrix (the "K-part"), each output written as
a full signed sum: 27 additions per output at 28 points, 756 in all.

The idea of computing the K-part with shared partial sums, and its count of additions, are from Sanjeet, Colbert
et al. (arXiv:2601.22347, Appendix A.1 and Table 4): sums over groups of four, 252 additions at 28 points. My part
is small: a shared-subexpression circuit for the same matrices, found by a randomized greedy search (Paar's method),
235 additions at 28 points, and one measurement on one GPU of both forms against Dao's original.

| folder | what it is |
|---|---|
| `generator/` | `emit.py` and `cse_lib.py` write the drop-in header from the circuit files in `search/circ/`, checking each circuit exactly first; `search/mats/` holds the matrices as Dao's and executorch's code generators define them. `check_dropin.txt` is the record of the exactness check of the drop-in headers on the Mac |
| `dao-cse/` | the job that timed Dao's original against the same build with the 235-addition header (`dao_fast_hadamard_transform_special.h`, which `generator/emit.py` writes byte for byte) |
| `three-forms/` | the job that timed Dao's original against three other forms: a greedy circuit generated on the machine (`cse`), the groups of four of Sanjeet, Colbert et al. (`grp`), and a QuaRot-style power-of-two transform followed by a matrix product (`mm`) |
| `runs/` | the raw results of both jobs. The `res_*.json` files have their `outputs` arrays (16 MB of output tensors each) removed; the `ptxas_*.txt` files keep only the compiler's lines about the 12N, 20N, 28N and 40N kernels of the build logs |

Both jobs fetch Dao's library at commit `e7706faf` and build it with PyTorch's extension builder; neither includes
any file of Dao's. Each checks that every variant gives Dao's outputs on a fixed input (`check.md`) before anything
is timed. Results: [../../README.md](../../README.md), section "A separate test".

## Run it again

On a machine with an NVIDIA GPU, CUDA 13, PyTorch with CUDA, git and pip, idle, from `dao-cse/` or `three-forms/`:

    bash run.sh

About 10 minutes for `dao-cse` (two CUDA builds) and 15 for `three-forms` (three). To make the header again:

    cd generator && python3 -B emit.py

It writes `generator/out/` (the Dao and executorch drop-ins and a table of counts); its
`dao_fast_hadamard_transform_special.h` equals `dao-cse/dao_fast_hadamard_transform_special.h` byte for byte
(checked on 22 October 2026).
