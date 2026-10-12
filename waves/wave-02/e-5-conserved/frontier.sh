#!/bin/sh
# Frontier curve at 16 points (floating point): the most entropy found with at most B operations, gates on 2,4,5,6,7,8 points.
for B in 12 24 36 48 52 56 60; do python3 -I -B anneal16b.py $B 22 2,4,5,6,7,8 1 $((700+B)); python3 -I -B anneal16b.py $B 12 2,4 1 $((800+B)); done
