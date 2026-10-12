# Makefile -- style-intrinsics: the harness of ../harness (harness.c, engine.inc, empty.c, variants.h:
# byte-for-byte copies, see SHA256SUMS.harness), FFHT's own fht.o, and whti.c.
#
#   make            build/harness and the listing build/whti.dis
#   make check      every variant against FFHT, 2^3 .. 2^24 (the task) and on to 2^26
#   make counts     the instruction counts of every step, from the compiled code (asmcount.py)
#
# FFHT is used where it is (FFHT_DIR, built by its own Makefile).  Nothing of FFHT is copied here.
# B and KFLAGS can be set on the command line to build a second copy with other flags:
#   make B=build-j32 KFLAGS="-O3 -march=native -ffp-contract=off -Wa,-mbranches-within-32B-boundaries"

FFHT_DIR ?= ../FFHT
CC       := gcc
CFLAGS   ?= -O3 -march=native
KFLAGS   ?= -O3 -march=native -ffp-contract=off
WARN     := -Wall -Wextra
B        ?= build

FFHT_COMMIT := $(shell git -C $(FFHT_DIR) rev-parse HEAD 2>/dev/null)
FFHT_FLAGS  := $(shell sed -n 's/^CFLAGS = //p' $(FFHT_DIR)/Makefile)
FFHT_OBJ    := $(FFHT_DIR)/fht.o $(FFHT_DIR)/fast_copy.o

DEFS := -DHARNESS_FLAGS='"$(CC) $(CFLAGS); whti.c: $(CC) $(KFLAGS)"' -DNAIVE_FLAGS='"(not in this build)"' \
        -DFFHT_COMMIT='"$(FFHT_COMMIT)"' -DFFHT_FLAGS='"gcc $(FFHT_FLAGS)"'

# J32: the assembler keeps every jump inside one 32-byte block (the control for the jump erratum of
# Skylake-type cores; see jcc32.py).  whti.c is compiled a second time with it; every name of that
# object gets the prefix j32_, so that both copies are in one program and take turns in one run.
J32      ?= -Wa,-mbranches-within-32B-boundaries
OBJ := $(B)/harness.o $(B)/variants.o $(B)/empty.o $(B)/whti.o $(B)/whti_j32.o

all: $(B)/harness $(B)/whti.dis

$(B):
	mkdir -p $(B)

plans.inc: plans.json gen.py
	python3 -I gen.py > plans.txt

$(B)/harness.o: harness.c engine.inc variants.h | $(B)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) $(DEFS) -c $< -o $@
$(B)/variants.o: variants.c variants.h whti.h | $(B)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) -I$(FFHT_DIR) -c $< -o $@
$(B)/empty.o: empty.c | $(B)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) -c $< -o $@
$(B)/whti.o: whti.c whti.h kern.h impl.inc kernels.inc kernels_w.inc plans.inc | $(B)
	$(CC) -std=gnu11 $(WARN) $(KFLAGS) -c $< -o $@
$(B)/whti_j32.o: whti.c whti.h kern.h impl.inc kernels.inc kernels_w.inc plans.inc | $(B)
	$(CC) -std=gnu11 $(WARN) $(KFLAGS) $(J32) -c $< -o $(B)/whti_j32.tmp.o
	objcopy --prefix-symbols=j32_ $(B)/whti_j32.tmp.o $@
	rm -f $(B)/whti_j32.tmp.o
$(B)/whti.dis: $(B)/whti.o
	objdump -d --no-show-raw-insn $< > $@

$(B)/harness: $(OBJ) $(FFHT_OBJ)
	$(CC) $(CFLAGS) -o $@ $(OBJ) $(FFHT_OBJ) -lm

# harness_k: the same harness with a list of single passes instead of transforms (variants_k.c;
# whti.c compiled with -DSTEP_ONLY gives, per step and style, one function for the 3-level pass
# alone and one for the first pass alone).  For timing only: "check" means nothing there.
$(B)/kstep.o: whti.c kern.h impl.inc kernels.inc kernels_w.inc | $(B)
	$(CC) -std=gnu11 $(WARN) $(KFLAGS) -DSTEP_ONLY -c $< -o $@
$(B)/variants_k.o: variants_k.c variants.h | $(B)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) -I$(FFHT_DIR) -c $< -o $@
$(B)/harness_k: $(B)/harness.o $(B)/empty.o $(B)/variants_k.o $(B)/kstep.o $(FFHT_OBJ)
	$(CC) $(CFLAGS) -o $@ $(B)/harness.o $(B)/empty.o $(B)/variants_k.o $(B)/kstep.o $(FFHT_OBJ) -lm
	objdump -d --no-show-raw-insn $(B)/kstep.o > $(B)/kstep.dis

check: $(B)/harness
	$(B)/harness check -k 3 26

counts: $(B)/whti.dis
	python3 -I asmcount.py $(B)/whti.dis

uports: $(B)/uports
$(B)/uports: uports.c | $(B)
	$(CC) -O2 -mavx2 -mfma $(WARN) $< -o $@

clean:
	rm -rf $(B)

.PHONY: all check counts clean uports
