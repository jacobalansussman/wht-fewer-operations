#!/bin/sh
# build_variants.sh -- write fht_avx.c with the patched generator for every kernel, and build each
# one exactly as FFHT builds itself.
#
#   sh build_variants.sh
#
# For every variant V:
#   gen/V/fht_avx.c      what the patched gen.py writes with FFHT's own shipped plan
#                        (FFHT_PLAN = hall_of_fame_avx.txt of the untouched clone; nothing is measured)
#   gen/V/k8_scale.inc   by which power of two the output is divided, for every size
#   build/V/             a copy of the untouched FFHT clone (without .git and without its built
#                        files) in which fht_avx.c is replaced by gen/V/fht_avx.c, built by FFHT's
#                        own Makefile: fht.o, fast_copy.o, test_float, test_double
#   build/V/fht_V.o, fast_copy_V.o   the same two objects with the global symbols they define
#                        renamed from NAME to V_NAME, so that several variants can be linked into
#                        one program (objcopy; the code is not touched)
#
#   sh build_variants.sh where
#
# builds p20s, p19f, c20s, d20s, d20x, d19f: the new kernel only in the larger passes (see below).
#
# The variant gT is the textbook kernel.  Its fht_avx.c must be the same file, byte for byte, as
# FFHT's own: the script stops if it is not.
#
#   sh build_variants.sh alt
#
# builds the variants aT, a20x, a20s, a19f instead: the same kernels with the plan gen/alt_plan.txt
# (alt_plan.py), which differs from FFHT's shipped plan at 7 sizes where the shipped plan has one
# pass of 8 registers fewer than the size allows.
set -e
here=$(cd "$(dirname "$0")" && pwd)
FFHT=${FFHT_DIR:-$here/../FFHT}        # the clone of FFHT at the commit named in ../README.md
cd "$here"

if [ "$1" = alt ]; then
    mkdir -p gen
    python3 -B alt_plan.py "$FFHT/hall_of_fame_avx.txt" > gen/alt_plan.txt
    plan=gen/alt_plan.txt
    variants="aT:textbook:exact:mem:0 a20x:half20:exact:mem:0 a20s:half20:raw:mem:0 a19f:fma19:exact:mem:0"
elif [ "$1" = where ]; then
    plan=$FFHT/hall_of_fame_avx.txt
    # the last field: the new kernel only in passes whose block is at least that many bytes
    #   p: every pass but the first (block of 512 bytes or more)
    #   c: passes whose block does not fit in the first-level cache (64 KiB or more)
    #   d: passes whose block does not fit in the second-level cache (512 KiB or more)
    variants="p20s:half20:raw:mem:512 p19f:fma19:exact:mem:512 c20s:half20:raw:mem:65536 d20s:half20:raw:mem:524288 d20x:half20:exact:mem:524288 d19f:fma19:exact:mem:524288"
else
    plan=$FFHT/hall_of_fame_avx.txt
    variants="gT:textbook:exact:mem:0 g20x:half20:exact:mem:0 g20s:half20:raw:mem:0 g19f:fma19:exact:mem:0 g19r:fma19:exact:reg:0"
fi

for spec in $variants; do
    v=$(echo "$spec" | cut -d: -f1)
    kernel=$(echo "$spec" | cut -d: -f2)
    scale=$(echo "$spec" | cut -d: -f3)
    fmac=$(echo "$spec" | cut -d: -f4)
    minb=$(echo "$spec" | cut -d: -f5)
    mkdir -p "gen/$v"
    FFHT_K8_KERNEL=$kernel FFHT_K8_SCALE=$scale FFHT_K8_FMACONST=$fmac FFHT_K8_MIN_BLOCK_BYTES=$minb \
        FFHT_PLAN="$plan" FFHT_OUT="gen/$v" python3 -B gen.py
    echo "$v: kernel=$kernel scale=$scale fma-constant=$fmac min-block-bytes=$minb: $(wc -l < "gen/$v/fht_avx.c") lines, sha256 $(sha256sum "gen/$v/fht_avx.c" | cut -c1-16)"
done

if [ "$1" = where ]; then
    :
elif [ "$1" = alt ]; then
    echo "aT/fht_avx.c differs from FFHT's own in $(diff gen/aT/fht_avx.c "$FFHT/fht_avx.c" | grep -c '^[<>]') lines (the helpers of the 7 sizes)"
elif cmp -s gen/gT/fht_avx.c "$FFHT/fht_avx.c"; then
    echo "gT/fht_avx.c is FFHT's own fht_avx.c, byte for byte (sha256 $(sha256sum "$FFHT/fht_avx.c" | cut -c1-16))"
else
    echo "STOP: the textbook output of the patched generator differs from FFHT's fht_avx.c" >&2
    cmp gen/gT/fht_avx.c "$FFHT/fht_avx.c" >&2 || true
    exit 1
fi

for spec in $variants; do
    v=$(echo "$spec" | cut -d: -f1)
    rm -rf "build/$v"
    mkdir -p "build/$v"
    # the untouched clone as git has it (no .git, no built files)
    git -C "$FFHT" archive --format=tar HEAD | tar -x -C "build/$v"
    cp "gen/$v/fht_avx.c" "build/$v/fht_avx.c"
    ( cd "build/$v" && make > make.log 2>&1 ) || { echo "STOP: make failed for $v" >&2; tail -20 "build/$v/make.log" >&2; exit 1; }
    w=$(grep -ci warning "build/$v/make.log" || true)
    # rename the global symbols that the two objects define (fht_float -> V_fht_float, ...)
    nm --defined-only -g "build/$v/fht.o" "build/$v/fast_copy.o" | awk -v v="$v" 'NF == 3 {print $3, v "_" $3}' > "build/$v/rename.map"
    objcopy --redefine-syms="build/$v/rename.map" "build/$v/fht.o" "build/$v/fht_$v.o"
    objcopy --redefine-syms="build/$v/rename.map" "build/$v/fast_copy.o" "build/$v/fast_copy_$v.o"
    echo "$v: built by FFHT's Makefile ($w warnings); fht.o text $(size -A "build/$v/fht.o" | awk '$1 == ".text" {print $2}') bytes"
done
