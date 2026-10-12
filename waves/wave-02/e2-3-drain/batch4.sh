#!/bin/sh
# 16 points, EVERY candidate gets the full evaluation (K = 100000), 3 seeds unseeded and 2 seeded with the bent centre's chain tree
./drain2 16 1 100000 2 140 100 r16all/bentchain_s1.jsonl H 400000 0 pre16_bent_chain.txt 0
./drain2 16 1 100000 2 140 130 r16all/free_s1.jsonl H 400000 0
./drain2 16 2 100000 2 140 130 r16all/free_s2.jsonl H 400000 0
