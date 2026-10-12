# Makefile -- style-fused: the harness of ../harness with int32 added, FFHT's own fht.o, and whtf.c / whts.c.
#
#   make            build/harness, build/uarch, build/fpdiff and the assembly listings build/*.s
#   make check      every variant against the reference, 2^3 .. 2^26
#
# FFHT is used where it is (FFHT_DIR, built by its own Makefile).  Nothing of FFHT is copied here.

FFHT_DIR     ?= ../FFHT
CC           := gcc
# J32: the assembler keeps every jump inside one 32-byte block (see NOTES.md, the jump erratum)
J32          ?= -Wa,-mbranches-within-32B-boundaries
CFLAGS       ?= -O3 -march=native $(J32)
KFLAGS       ?= -O3 -march=native -fno-tree-reassoc $(J32)
SCALAR_FLAGS ?= -O3 -march=native -fno-tree-vectorize -fno-tree-slp-vectorize -fwrapv $(J32)
WARN         := -Wall -Wextra
B            := build

FFHT_COMMIT := $(shell git -C $(FFHT_DIR) rev-parse HEAD 2>/dev/null)
FFHT_FLAGS  := $(shell sed -n 's/^CFLAGS = //p' $(FFHT_DIR)/Makefile)
FFHT_OBJ    := $(FFHT_DIR)/fht.o $(FFHT_DIR)/fast_copy.o

DEFS := -DHARNESS_FLAGS='"$(CC) $(CFLAGS); whtf.c: $(CC) $(KFLAGS)"' -DNAIVE_FLAGS='"$(CC) $(SCALAR_FLAGS)"' \
        -DFFHT_COMMIT='"$(FFHT_COMMIT)"' -DFFHT_FLAGS='"gcc $(FFHT_FLAGS)"'

OBJ := $(B)/harness.o $(B)/variants.o $(B)/naive_i.o $(B)/whtf.o $(B)/whts.o $(B)/fhtB.o

all: $(B)/harness $(B)/uarch $(B)/fpdiff $(B)/whtf.s $(B)/whts.s

$(B):
	mkdir -p $(B)

$(B)/harness.o: harness.c engine.inc variants.h | $(B)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) $(DEFS) -c $< -o $@
$(B)/variants.o: variants.c variants.h whtf.h | $(B)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) -I$(FFHT_DIR) -c $< -o $@
$(B)/naive_i.o: naive_i.c whtf.h | $(B)
	$(CC) -std=gnu11 $(WARN) $(SCALAR_FLAGS) -c $< -o $@
$(B)/whtf.o: whtf.c whtf.h kern.h impl.inc three.inc | $(B)
	$(CC) -std=gnu11 $(WARN) $(KFLAGS) -c $< -o $@
$(B)/whts.o: whts.c whtf.h kern.h impl.inc | $(B)
	$(CC) -std=gnu11 $(WARN) $(SCALAR_FLAGS) -c $< -o $@
$(B)/whtf.s: whtf.c whtf.h kern.h impl.inc three.inc | $(B)
	$(CC) -std=gnu11 $(KFLAGS) -S $< -o $@
$(B)/whts.s: whts.c whtf.h kern.h impl.inc | $(B)
	$(CC) -std=gnu11 $(SCALAR_FLAGS) -S $< -o $@

# FFHT's fht.c compiled a second time, into this folder, with FFHT's own flags plus J32; its four
# public names get the prefix B and all its other names are made local, so that both objects can be linked.  FFHT's folder is not touched.
$(B)/fhtB.o: $(FFHT_DIR)/fht.c | $(B)
	$(CC) $(FFHT_FLAGS) $(J32) -c $< -o $(B)/fhtB.tmp.o
	objcopy --redefine-sym fht_float=Bfht_float --redefine-sym fht_double=Bfht_double \
	        --redefine-sym fht_float_oop=Bfht_float_oop --redefine-sym fht_double_oop=Bfht_double_oop $(B)/fhtB.tmp.o $(B)/fhtB.tmp2.o
	objcopy -G Bfht_float -G Bfht_double $(B)/fhtB.tmp2.o $@

$(B)/harness: $(OBJ) $(FFHT_OBJ)
	$(CC) $(CFLAGS) -o $@ $(OBJ) $(FFHT_OBJ) -lm

$(B)/uarch: uarch.c | $(B)
	$(CC) -O2 -mavx2 -mfma $(J32) $(WARN) $< -o $@

$(B)/fpdiff: fpdiff.c $(B)/whtf.o $(B)/whts.o $(B)/naive_i.o
	$(CC) -std=gnu11 $(WARN) -O2 -march=native fpdiff.c $(B)/whtf.o $(B)/whts.o $(B)/naive_i.o -o $@ -lm -lquadmath

check: $(B)/harness
	$(B)/harness check -t all -k 3 26

clean:
	rm -rf $(B)

.PHONY: all check clean
