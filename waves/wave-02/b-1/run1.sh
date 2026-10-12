set -e
cd waves/wave-02/b-1 || exit 1
gcc -O2 -o cover cover.c
python3 dual.py 4 > dual4.txt 2> dual4.err; python3 dual.py 5 > dual5.txt 2> dual5.err; cat dual4.err dual5.err
echo "== the seven lines of clique.out, recomputed =="
./cover 4 4 0 design 0001:4 0010:4 0100:4 1000:4
./cover 4 4 0 design 0001:1 0010:1 0011:1 0100:1 0101:1 0110:1 0111:1 1000:1 1001:1 1010:1 1011:1 1100:1 1101:1 1110:1 1111:1
./cover 4 5 0 design 0001:2 0010:2 0011:1 0100:2 0101:1 0110:1 0111:1 1000:2 1001:1 1010:1 1011:1 1100:1 1101:1 1110:1 1111:1
./cover 4 6 0 design 0001:3 0010:3 0011:1 0100:3 0101:1 0110:1 0111:1 1000:3 1001:1 1010:1 1011:1 1100:1 1101:1 1110:1 1111:1
./cover 4 7 0 design 0001:2 0010:2 0011:1 0100:2 0101:1 0110:1 0111:3 1000:2 1001:1 1010:1 1011:3 1100:1 1101:3 1110:3 1111:1
./cover 4 8 0 design 0001:2 0010:2 0011:2 0100:2 0101:2 0110:2 0111:2 1000:2 1001:2 1010:2 1011:2 1100:2 1101:2 1110:2 1111:2
./cover 5 4 0 design 00001:1 00010:1 00100:1 00111:1 01000:1 01011:1 01101:1 01110:1 10000:1 10011:1 10101:1 10110:1 11001:1 11010:1 11100:1 11111:1
echo "== exhaustive, block size 4 =="
for a in "1 3" "2 7" "3 11" "4 15" "5 19" "6 23" "7 27" "8 31"; do set -- $a; timeout 60 ./cover 4 $1 $2 dual4.txt || echo "TIMEOUT 4 $1 $2"; done
echo "== exhaustive, block size 5 =="
for a in "1 4" "2 9" "3 14" "4 16" "4 17"; do set -- $a; timeout 120 ./cover 5 $1 $2 dual5.txt || echo "TIMEOUT 5 $1 $2"; done
