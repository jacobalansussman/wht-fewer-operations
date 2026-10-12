#!/bin/sh
cd waves/wave-08/ab-0-neighboursums || exit 1
timeout 1100 nice -n 19 ./flat3 flats6.txt > flat3_k7.out 2>&1
echo "exit $?" >> flat3_k7.out
echo done > job5.done
