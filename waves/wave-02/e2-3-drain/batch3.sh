#!/bin/sh
for s in $(seq 2 17); do ./drain2 16 $s 3000 2 140 40 r16seed/bentchain_s$s.jsonl H 400000 0 pre16_bent_chain.txt 0; done
