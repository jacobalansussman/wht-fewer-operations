# Makefile -- kloop: one pass of 8 registers and 3 levels, alone, for every kernel.
#   make            (in style-generator/kloop; needs ../gen.py and ../k8kernel.py)
# kloop_passes.c is compiled with FFHT's own flags.
FFHT_DIR ?= ../../FFHT
FFHT_FLAGS := $(shell sed -n 's/^CFLAGS = //p' $(FFHT_DIR)/Makefile)
all: kloop lat
lat: lat.c
	gcc -O2 -mavx2 -mfma -Wall -Wextra $< -o $@
kloop_passes.c kloop_list.inc: ../kloop_gen.py ../gen.py ../k8kernel.py
	cd .. && python3 -B kloop_gen.py > kloop/kloop_passes.c
kloop_passes.o: kloop_passes.c
	gcc $(FFHT_FLAGS) -c $< -o $@
kloop: kloop_main.c kloop_nothing.c kloop_passes.o kloop_list.inc
	gcc -O2 -std=gnu11 -Wall -Wextra -c kloop_main.c -o kloop_main.o
	gcc -O2 -std=gnu11 -Wall -Wextra -c kloop_nothing.c -o kloop_nothing.o
	gcc -o $@ kloop_main.o kloop_nothing.o kloop_passes.o
clean:
	rm -f kloop *.o kloop_passes.c kloop_list.inc
