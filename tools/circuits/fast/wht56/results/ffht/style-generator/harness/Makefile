# Makefile -- the baseline harness (harness.c, engine.inc, variants.h, empty.c: unchanged copies
# of ../../harness) with the variants of the style-generator job (variants.c).
#
#   sh ../build_variants.sh      first: writes and builds every variant
#   make                         build/harness
#   make check                   every variant against FFHT, 2^1 .. 2^27 points, float and double
#   sh ../build_variants.sh alt  then  make alt:  build-alt/harness with the list variants_alt.c
#                                (the other plan at 7 sizes; see alt_plan.py)
#   sh ../build_variants.sh where  then  make where:  build-where/harness with variants_where.c
#                                (the new kernel only in the larger passes)
#
# FFHT itself is used where it is (FFHT_DIR, the untouched clone, built by its own Makefile).
FFHT_DIR ?= ../../FFHT
V_DIR    := ../build
CC       := gcc
CFLAGS   ?= -O3 -march=native
WARN     := -Wall -Wextra
B        := build
VARIANTS := gT g20x g20s g19f g19r

FFHT_COMMIT := $(shell git -C $(FFHT_DIR) rev-parse HEAD 2>/dev/null)
FFHT_FLAGS  := $(shell sed -n 's/^CFLAGS = //p' $(FFHT_DIR)/Makefile)
FFHT_OBJ    := $(FFHT_DIR)/fht.o $(FFHT_DIR)/fast_copy.o
V_OBJ       := $(foreach v,$(VARIANTS),$(V_DIR)/$(v)/fht_$(v).o $(V_DIR)/$(v)/fast_copy_$(v).o)

DEFS := -DHARNESS_FLAGS='"$(CC) $(CFLAGS)"' -DNAIVE_FLAGS='"not used here"' \
        -DFFHT_COMMIT='"$(FFHT_COMMIT)"' -DFFHT_FLAGS='"gcc $(FFHT_FLAGS)"'

OBJ := $(B)/harness.o $(B)/variants.o $(B)/empty.o

all: $(B)/harness

$(B):
	mkdir -p $(B)

$(B)/g20s_scale.inc: ../gen/g20s/k8_scale.inc | $(B)
	cp $< $@
$(B)/harness.o: harness.c engine.inc variants.h | $(B)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) $(DEFS) -c $< -o $@
$(B)/variants.o: variants.c variants.h $(B)/g20s_scale.inc | $(B)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) -I$(FFHT_DIR) -I$(B) -c $< -o $@
$(B)/empty.o: empty.c | $(B)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) -c $< -o $@

$(B)/harness: $(OBJ) $(FFHT_OBJ) $(V_OBJ)
	$(CC) $(CFLAGS) -o $@ $(OBJ) $(FFHT_OBJ) $(V_OBJ) -lm

# ---- the second harness: the other plan (variants_alt.c) ----
BA      := build-alt
A_NAMES := aT a20x a20s a19f g20s g19f
A_OBJ   := $(foreach v,$(A_NAMES),$(V_DIR)/$(v)/fht_$(v).o $(V_DIR)/$(v)/fast_copy_$(v).o)
alt: $(BA)/harness
$(BA):
	mkdir -p $(BA)
$(BA)/g20s_scale.inc: ../gen/g20s/k8_scale.inc | $(BA)
	cp $< $@
$(BA)/a20s_scale.inc: ../gen/a20s/k8_scale.inc | $(BA)
	sed 's/k8_\(scale\|passes\)_/alt_k8_\1_/g' $< > $@
$(BA)/harness.o: harness.c engine.inc variants.h | $(BA)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) $(DEFS) -c $< -o $@
$(BA)/variants_alt.o: variants_alt.c variants.h $(BA)/g20s_scale.inc $(BA)/a20s_scale.inc | $(BA)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) -I$(FFHT_DIR) -I$(BA) -c $< -o $@
$(BA)/empty.o: empty.c | $(BA)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) -c $< -o $@
$(BA)/harness: $(BA)/harness.o $(BA)/variants_alt.o $(BA)/empty.o $(FFHT_OBJ) $(A_OBJ)
	$(CC) $(CFLAGS) -o $@ $(BA)/harness.o $(BA)/variants_alt.o $(BA)/empty.o $(FFHT_OBJ) $(A_OBJ) -lm

# ---- the third harness: the new kernel only in the larger passes (variants_where.c) ----
BW      := build-where
W_NAMES := g20s p20s p19f c20s d20s d20x d19f
W_SCALE := g20s p20s c20s d20s
W_OBJ   := $(foreach v,$(W_NAMES),$(V_DIR)/$(v)/fht_$(v).o $(V_DIR)/$(v)/fast_copy_$(v).o)
where: $(BW)/harness
$(BW):
	mkdir -p $(BW)
$(BW)/%_scale.inc: ../gen/%/k8_scale.inc | $(BW)
	sed 's/k8_\(scale\|passes\)_/$*_k8_\1_/g' $< > $@
$(BW)/harness.o: harness.c engine.inc variants.h | $(BW)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) $(DEFS) -c $< -o $@
$(BW)/variants_where.o: variants_where.c variants.h $(foreach v,$(W_SCALE),$(BW)/$(v)_scale.inc) | $(BW)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) -I$(FFHT_DIR) -I$(BW) -c $< -o $@
$(BW)/empty.o: empty.c | $(BW)
	$(CC) -std=gnu11 $(WARN) $(CFLAGS) -c $< -o $@
$(BW)/harness: $(BW)/harness.o $(BW)/variants_where.o $(BW)/empty.o $(FFHT_OBJ) $(W_OBJ)
	$(CC) $(CFLAGS) -o $@ $(BW)/harness.o $(BW)/variants_where.o $(BW)/empty.o $(FFHT_OBJ) $(W_OBJ) -lm

check: $(B)/harness
	$(B)/harness check -k 1 27

list: $(B)/harness
	$(B)/harness list

clean:
	rm -rf $(B)

.PHONY: all alt where check list clean
