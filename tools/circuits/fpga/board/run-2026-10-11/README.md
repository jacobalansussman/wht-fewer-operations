# The run on the board, 11 October 2026

On an iCE40-HX8K breakout board, with the chip's own 12 MHz oscillator as the clock, the self-test of this
folder (`../selftest/`) ran for 797 seconds. It feeds the same test inputs to three pipelined 8-point circuits:
the textbook circuit, the 19-adder circuit, and a copy of the 19-adder circuit that is broken on purpose. Inside
the chip a comparator counts the inputs, the mismatches of the real pair and the mismatches of the broken copy,
and once a second the chip sends one line of text with those three counts and a running checksum of the outputs.

**The result.** 597,750,000 test inputs (750,000 a second); mismatches between the textbook circuit and the 19-adder
circuit: 0; mismatches of the broken copy: 559,367,052, which shows that the test can fail. The checksum the
board sent equals the checksum of the software model in every line that was read.

**What it shows, and what it does not.** It shows that the 19-adder circuit computes the same values as the
textbook circuit on a real chip. It says nothing about size or speed: in this pipelined build the 19-adder
circuit is the larger of the two designs (the unpipelined comparison is in [../../README.md](../../README.md)).
It is one board, one chip, one build of the image and one run.

## The lines

[lines-read.txt](lines-read.txt) holds the 534 lines that were read, for the seconds k = 70 to 797 after the
load (some seconds were not read: only one program at a time was allowed on the board). A line looks like this:

    WHT8 k=031D n=23A0F0F0 bad=00000000 ctl=2157438C sum=C8FC6286 ref=C8FC6286

- `k`: seconds since the load, in hexadecimal.
- `n`: test inputs so far. `bad`: mismatches of the real pair. `ctl`: mismatches of the broken copy.
- `sum`: the running checksum of the 19-adder circuit's outputs. `ref`: the same for the textbook circuit.

Each line carries the totals since the start, so the last line covers all the inputs. A model computes the
same lines on a computer: `../expected.py` (slow, about one second per second of board time) and
`../fastmodel/wht8_fast.c` (the same computation in C). Every line in the file equals the model's line for
its `k`. To check it, from this folder:

    cc -O2 -o /tmp/wht8_fast ../fastmodel/wht8_fast.c
    /tmp/wht8_fast 797 70 | tr -d '\r' | grep -F -x -c -f lines-read.txt        # prints 534

## The inputs

Eight signed 12-bit numbers per test input. In every burst of 2,000 inputs, 256 are the sign patterns of the
extreme values and 1,744 are pseudo-random.

## How it was loaded, and one thing learned

The image (`../selftest/`, built by `build.sh`) was loaded into the chip's volatile memory over the board's USB
chip; nothing was written to the board's flash. The lines were read back over the same USB chip's second
channel at 115,200 baud, in two ways (directly over USB, and through the computer's serial driver), with the
same result. During the run the chip's "configuration done" signal was read high 793,108 times and never low.

A first attempt the same afternoon lost the image at once: the chip accepted it and then held nothing. The
loading program's last command, which lets go of the pins, set the value of the reset line to 0 in the same
command that turned the pin into an input, and this chip erases its configuration on a low pulse of 200
nanoseconds on that line. With the last command changed so that the reset line's value stays 1, the image
stayed. That the old last command was the cause fits both runs and is not proved: it is one load each way.

This run was made by the AI agents I work with, at my direction; I have not repeated it.
