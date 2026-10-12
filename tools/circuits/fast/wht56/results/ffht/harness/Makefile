# Makefile -- build the harness.
#
#   make                 build/harness
#   make check           every variant against FFHT, 2^1 .. 2^27 points, float and double
#   make list            the variants
#   make cpufreq         build/cpufreq, which measures the real frequency of a core
#   make ports           build/ports, which measures how many vector additions a core starts per cycle
#
# FFHT is used where it is: FFHT_DIR is its own clone, already built by its own Makefile
# ("make" there gives fht.o and fast_copy.o).  Nothing of FFHT is copied or rebuilt here.
#
# ours/ holds copies of three files of wht56/c/ (wht56.c, wht56.h, kernels.h): our plain C for
# doubles.  The float version is the same text with "float" for "double", written by sed below.

FFHT_DIR     ?= ../FFHT
CC           := gcc
CFLAGS       ?= -O3 -march=native
NAIVE_CFLAGS ?= -O3 -mavx2
WARN         := -Wall -Wextra
B            := build

FFHT_COMMIT := $(shell git -C $(FFHT_DIR) rev-parse HEAD 2>/dev/null)
FFHT_FLAGS  := $(shell sed -n 's/^CFLAGS = //p' $(FFHT_DIR)/Makefile)
FFHT_OBJ    := $(FFHT_DIR)/fht.o $(FFHT_DIR)/fast_copy.o

DEFS := -DHARNESS_FLAGS='"$(CC) $(CFLAGS)"' -DNAIVE_FLAGS='"$(CC) $(NAIVE_CFLAGS)"' \
        -DFFHT_COMMIT='"$(FFHT_COMMIT)"' -DFFHT_FLAGS='"gcc $(FFHT_FLAGS)"'

OBJ := $(B)/harness.o $(B)/variants.o $(B)/empty.o $(B)/naive.o $(B)/wht56.o $(B)/wht56f.o

all: $(B)/harness

$(B):
	mkdir -p $(B)

$(FFHT_OBJ):
	@echo "FFHT is not built: run 'make' in $(FFHT_DIR) first" >&2; exit 1

# the float copy of our plain C
$(B)/wht56f.c: ours/wht56.c | $(B)
	sed -e 's/\bdouble\b/float/g' -e 's/wht56_/wht56f_/g' -e 's/"wht56\.h"/"wht56f.h"/' -e 's/"kernels\.h"/"kernelsf.h"/' $< > $@
$(B)/wht56f.h: ours/wht56.h | $(B)
	sed -e 's/\bdouble\b/float/g' -e 's/wht56_/wht56f_/g' -e 's/WHT56_H/WHT56F_H/g' $< > $@
$(B)/kernelsf.h: ours/kernels.h | $(B)
	sed -e 's/\bdouble\b/float/g' -e 's/wht56_/wht56f_/g' -e 's/WHT56_KERNELS_H/WHT56F_KERNELS_H/g' -e 's/0\.5\*/0.5f*/g' $< > $@

$(B)/harness.o: harness.c engine.inc variants.h | $(B)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) $(DEFS) -c $< -o $@
$(B)/variants.o: variants.c variants.h ours/wht56.h $(B)/wht56f.h | $(B)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) -I$(FFHT_DIR) -Iours -I$(B) -c $< -o $@
$(B)/empty.o: empty.c | $(B)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) -c $< -o $@
$(B)/naive.o: naive.c | $(B)
	$(CC) -std=gnu11 $(WARN) $(NAIVE_CFLAGS) -c $< -o $@
$(B)/wht56.o: ours/wht56.c ours/wht56.h ours/kernels.h | $(B)
	$(CC) -std=c11 $(CFLAGS) -Iours -c $< -o $@
$(B)/wht56f.o: $(B)/wht56f.c $(B)/wht56f.h $(B)/kernelsf.h
	$(CC) -std=c11 $(CFLAGS) -I$(B) -c $< -o $@

$(B)/harness: $(OBJ) $(FFHT_OBJ)
	$(CC) $(CFLAGS) -o $@ $(OBJ) $(FFHT_OBJ) -lm

# the real frequency of a processor core (see cpufreq.c); run it pinned, like the harness
cpufreq: $(B)/cpufreq
$(B)/cpufreq: cpufreq.c | $(B)
	$(CC) -O2 $(WARN) $< -o $@

# how many vector additions per cycle a core can start (see ports.c); run it pinned
ports: $(B)/ports
$(B)/ports: ports.c | $(B)
	$(CC) -O2 -mavx2 -mfma $(WARN) $< -o $@

check: $(B)/harness
	$(B)/harness check -k 1 27

list: $(B)/harness
	$(B)/harness list

clean:
	rm -rf $(B)

.PHONY: all check list clean cpufreq ports
