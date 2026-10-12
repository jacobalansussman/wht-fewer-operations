# af-0: criticism of ad-6's "N + o(N) for degree 2"

11 October 2026, 07:34 to 07:50 EDT, 30-minute box. Private. One agent; nothing in Lean, nothing published.
Marks: [ran] = my own run this morning, whole numbers, files in `af-0/`; [derived] = by hand this morning, checked by
nobody else; [read] = from ad-6, ae-cross or a source on the web; [guess].
Gate counts: **(G)** a gate is any a*u + b*v, scalings free; **(O)** OpenAI's count, where an addition, a subtraction
and a multiplication by a constant each cost one (`OAI/Computability/FourierCircuit/Core.lean`, gates add, sub, scale).

## Verdict

**The claim holds, I did not find it in print, and it changes nothing for the transform.** It is a statement about a
much smaller problem (about (log2 N)^2 / 2 inputs instead of N), it lowers a leading constant from 2 to 1, and that
constant cannot go lower: any circuit needs at least N - 1 gates [derived, section 5]. So this object is finished in
its leading term, and it carries no saving exponent.

One thing built on it elsewhere is wrong by N: ae-cross hybrid 1's "the transform modulo 8 in 2N + o(N)" (section 6).

## 1. The claim, stated exactly

A polynomial of degree at most 2 in k bits is q(x) = c + sum_p l_p x_p + sum_{p<r} Q_pr x_p x_r. Its D = 1 + k +
k(k-1)/2 numbers c, l_p, Q_pr are the *coefficients*. N = 2^k.

- (a) **Circuit.** For every k there is a program whose inputs are the D coefficients and nothing else, whose gates are
  all u + v or u - v, and whose outputs are q(x) at all N points, with E2(k) = N (1 + O(log k / k)) gates.
- (b) **Two helpers.** There are two ways P1, P2 of cutting the N points into classes, with about 2 N log2(k)/k classes
  in all, such that every q is (a number per P1 class) + (a number per P2 class).
- (c) **Least classes** V(4) = 14 at 16 points and V(5) = 24 at 32 points.
- It claims nothing for the transform. ad-6 says so in its third line.

## 2. What I checked, with my own code

**Their circuit, replayed from the coefficients** [ran, `trace.py`, `trace.out`, `trace-17-20.out`]. I did not use
their checker. I handed their builder (`circuit2.eval2`, untouched) D objects, one per coefficient, each carrying its
exact linear form; the objects can only be combined through my own "add" (which counts a gate) or a change of sign;
adding a plain number raises an error. So every wire is provably made from the coefficients alone, the count is mine,
and "output x has the form [1, x, products of pairs of x]" is a proof for all inputs, not a test on samples.

| k | 3 | 4 | 5 | 6 | 7 | **8** | 9 | 12 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gates (G), my count | 13 | 29 | 63 | 130 | 265 | **528** | 1055 | 6729 | 97078 | 191050 | 375794 | 744372 | 1473899 |
| gates / N | 1.63 | 1.81 | 1.97 | 2.03 | 2.07 | **2.06** | 2.06 | 1.64 | 1.48 | 1.46 | 1.43 | 1.42 | 1.41 |

All 18 sizes k = 3 to 20: every output form exact, my count equals theirs. ad-6 had exact replay to k = 9 and random
numbers to k = 16; k = 10 to 20 exact is new. The only output that is not a gate is the point 0 (it is the input c).
Inputs: exactly the D coefficients; nothing already summed.

**My own builder, written from the identity alone** [ran, `own.py`, `own.out`]. It imports nothing of ad-6 and writes
an explicit list of gates (wire i +- wire j). Exact on every unit input for k = 3 to 13; on random whole numbers to
k = 20. Gates: 12, 28, 62, 125, 246, 478 at k = 3 to 8; 96,744 at k = 16 (1.476 N); 1,472,990 at k = 20 (1.405 N).
Every gate is one addition or one subtraction and no output needs a sign flip, so **the count is the same in (G) and
in (O)**. The last layer reads 8, 14, 24 helper classes at k = 3, 4, 5, as claimed.

**V(4) = 14 without the recalled theorem** [ran, `v4.py`, `v4.out`, 90 seconds]. The fact needed is about graphs: no
graph with every degree at least 2, no cycle shorter than 8, and three more edges than vertices, on 16 edges or fewer.
I listed all 8,257 "kernels" (the graph with its vertices of degree 2 erased: at most 6 vertices and 9 edges, repeated
edges and loops allowed, no use of symmetry, two-sidedness not assumed) and for each searched every way of
lengthening its edges. **The least is 18 edges**, and the graph that attains it is the 3 x 3 two-sided graph with
every edge cut in two, exactly the example ad-6 named. So 13 classes are impossible at 16 points, and 14 are attained
(my builder at k = 4, replayed exactly). V(4) = 14 stands on a search now.
The step "a good pair has no cycle shorter than 8" [derived]: around a cycle the alternating sum of any (P1 number +
P2 number) is 0; a cycle of 2, 4 or 6 points would then be a linear relation between at most 6 evaluation points, and
any 7 points are independent for degree 2 (the dual of the second-order Reed-Muller code has least weight 8).

**V(5) = 24.** Upper bound: verified (24 classes at k = 5, exact replay). Lower bound: still rests on the theorem of
Alon, Hoory and Linial (2002). I confirmed its statement from a paper that restates it (sources) and evaluated it in
fractions [ran, `ahl.py`]: classes >= 8, 14, 24, 40, 68, 116 at 8 to 256 points, ad-6's numbers. At 16 points the
theorem and my exhaustive search agree at 16, 17 and 18 edges (impossible, impossible, possible). I did not search
32 points exhaustively (kernels of up to 18 vertices: too many for this box).

## 3. Does it scale: the growth law

[ran, `own.py`, count-only formula; it equals every built program k = 3 to 20; `own.out`, `law-65536.out`]
ad-6 counted to k = 400. I counted to k = 65,536.

| k | 8 | 16 | 32 | 64 | 128 | 256 | 400 | 1024 | 4096 | 16384 | 65536 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| (gates - N)/N | 0.867 | 0.476 | 0.245 | 0.149 | 0.0719 | 0.0369 | 0.0305 | 0.0120 | 0.00394 | 0.00099 | 0.00026 |
| that, times k / log2 k | 2.31 | 1.90 | 1.57 | 1.59 | 1.32 | 1.18 | 1.41 | 1.23 | 1.34 | 1.16 | 1.06 |

**Law observed: gates = N (1 + c log2(k)/k) with c between 1.06 and 1.5 at the 18 sizes sampled from k = 100 to
65,536**, wobbling because the number t of selector bits is a whole number. In terms of n = N points: n + about 1.1 to
1.5 times n log2(log2 n)/log2 n. This matches the hand count [derived]: excess/N is about 2^-t + 2^-s, t selector
bits, s bits per atom, s about (k - t)/2^t. ad-6's "1.5 log2(k)/k" is right for its range; its "about 2N log2(k)/k
classes" is on the safe side (its own table gives 1.1 to 1.6 in place of 2).

Fair warning about size: the convergence is slow. 1.41 N at a million points, 1.15 N at 2^64, below 1.1 N only beyond
about 2^80 points [read: ad-6's `law.out`, 1.109 at k = 80, 1.088 at k = 96]. At 128 to 512 points their circuit is
above 2N (2.06 to 2.07); mine is 1.80 to 1.92 there.

## 4. Is it known?

Six searches, about ten minutes; not a proof of absence.
- Known, degree d in general: d operations per point. Bouillaguet, Chen, Cheng, Chou, Niederhagen, Shamir, Yang,
  "Fast exhaustive search for polynomial systems in F2", CHES 2010 (the Gray-code walk); Bouillaguet, "Evaluating a
  Boolean polynomial on all possible inputs", ePrint 2022/1412, both methods O(d 2^n). That is 2N for degree 2: the
  "plain way" ad-6 improves.
- Known, degree 1, exact: Li, Lin, Han, "On the exact lower bounds of encoding circuit sizes of Hamming codes and
  Hadamard codes", arXiv:1804.09903 (2018): exactly 2^k - k - 1 additions. Their abstract does not treat degree 2.
- The same problem under another name is "the size of an encoder for the second-order Reed-Muller code". I found no
  statement of N + o(N) for it, and none of "one addition per point" for a quadratic form on the cube.
- [guess] It may be folklore among people who count XOR gates of encoders; the proof is five lines. I would call it
  "new as far as I can find" and not more.

What the known theory then says about "linear or not": this problem was always linear (2N); the question was only the
constant. Nothing in that literature connects it to the order of the transform.

## 5. Two bounds that pin the object [derived, this morning, unchecked by anyone]

- **At least N - 1 gates, for any circuit, in count (G).** The N outputs are N linear forms no two of which are
  proportional, and only one of them (the point 0) is an input. So N + o(N) is the right leading term and the only
  thing left open is the size of the o(N).
- **The o(N) is at least of order N^(2/3).** Call a wire a *helper* if it is not an output. An output cannot be made
  from two other outputs (three points are independent). A helper can pair with an output to make another output for
  at most one pair of points (four points are independent). Outputs made from two helpers form a graph on the helpers
  in which no set of at most 7 edges touches fewer vertices than it has edges (seven points are independent); such a
  graph on h vertices has at most a constant times h^(3/2) edges. So N <= h + C h^(3/2).
  Truth is therefore between N + c N^(2/3) and N + 1.5 N log2(k)/k. This is a question about a constant's correction
  term and is below the user's bar.

## 6. In the user's terms

- **For the transform: nothing.** No circuit size for the transform on n points, no saving exponent.
- For the smaller problem (degree at most 2 on n = 2^k cube points, from its coefficients): n (1 + about
  1.1 to 1.5 times log2(log2 n)/log2 n) gates, the same in (G) and (O), against 2n by the textbook and at least n - 1.
- **Error found in what was built on it** [derived]. ae-cross hybrid 1 prices "the superset sums of levels 0, 1, 2
  (the transpose of ad-6's matrix)" at N + o(N). Turning a linear circuit round (reverse every wire; a fan-out becomes
  an addition) changes the count by exactly (outputs - inputs) of the original, here N - D. So the turned-round map
  costs **2N + o(N), and at least 2N - D - 1** by the bound above, not N + o(N). Check on the smallest case: 1 number
  copied to N places costs 0 gates; N numbers summed to 1 costs N - 1. Hence "the transform modulo 8 in 2N + o(N)"
  should read **3N + o(N)** by that route, unless the two halves share gates, which nobody has shown.
- Not checked by me: ad-6's "degree d in (d - 1) N + o(N)" (derived there, not built) and its failure at degree 3.
  ad-6's own ceiling stands as far as I can see: two helpers cannot serve degree beyond about log2 k with o(N) classes,
  so this device alone gives no slope in the degree, and the slope is what the order of the transform is made of.

## 7. If one wants a nearest stronger true statement

None fails, so only sharpenings: (i) the count is the same in OpenAI's model; (ii) exact for all inputs to a million
points; (iii) V(4) = 14 by search, with "18 edges is the least for three more edges than vertices"; (iv) first-order
optimal by N - 1.

## Sources

- Alon, Hoory, Linial, "The Moore bound for irregular graphs", Graphs and Combinatorics 18 (2002) 53-57. Statement
  read in Babu and Radhakrishnan, "An entropy based proof of the Moore bound for irregular graphs", arXiv:1011.1058
  (their Theorem 3.3: girth 2r, least degree 2, average degree d, then n >= 2 (1 + (d-1) + ... + (d-1)^(r-1))).
  I did not open the original PDF.
- Bouillaguet et al., CHES 2010; Bouillaguet, IACR ePrint 2022/1412 (read as search summaries, not the papers).
- Li, Lin, Han, arXiv:1804.09903 (abstract read).

## Files

`waves/wave-09/af-0/`:
trace.py, trace.out, trace-17-20.out (their circuit, my tracer, exact, k = 3 to 20);
own.py, own.out, law-65536.out (my builder, exact replay, count law to k = 65,536);
v4.py, v4.out (exhaustive search behind V(4) = 14); ahl.py, ahl.out (the recalled theorem in fractions).
