# lit-constants: what is published about the constant in front of N log N for the Walsh-Hadamard transform

> Editor's note (11 October 2026): this search was made in under half an hour and missed the paper of Coppersmith, Feig and Linzer (1994), to which the 4-point circuit in 7 operations and the rate 7/8 are due. So for "public in 2004" read 1994, and for "at least 24 years old" read 32. The 2019 paper that it gives to A. Antonevich is listed by two indexes under M. Parfieniuk. Its remark that two groups of authors show no sign of knowing each other, and its remark on what the "recent progress" of a seminar became, are guesses; the seminar text it quotes is a public announcement of a talk, not a paper. Among the journals it lists as not searched was the one with the 1994 paper. That paper and one of 2000 were read afterwards. See [Earlier papers](../README.md#earlier-papers).

## Five-line summary

1. **Count (G), the 3/4 family: apparently new.** The best published rate I found is 7/8, and it is older than we thought: a Comsys patent filed in August 2002 has the 4-point transform in 7 additions with free doublings and 16 points in 56; Alman and Rao (2022) have the same 7/8 as their Theorem 6.1. Nothing published has 20 or 19 at 8 points (published: 22), 52 at 16 points (published: 56), or a rate below 7/8.
2. **Count (O), exact H x: apparently new.** The published record is Alman and Rao's (23/24) N log2 N + (13/12) N, which counts what OpenAI counts (additions, subtractions, multiplications by constants; they differ only on a bare negation) and is for H x itself, not a scaled H. Both of our rates (7/8, and 5/6 from the 19-gate circuit) are below it. Their algorithm first beats the textbook near 2^24 points; ours at 4,096 and at 512.
3. **The "Sergeev note with 7/8" does not exist as such.** Sergeev's arXiv list has no note on the Walsh-Hadamard transform. The memory mixes three real things: his December 2022 note on Kronecker powers (disjointness matrix, depth 2), his 2017 constant for the complex DFT, and Alman and Rao's own 7/8.
4. **WAVE2-NOTE line 14 is right but should be reworded.** 7/8 is below 23/24 in the same count. But 7/8 is also Alman and Rao's own published number for additions alone, so the sentence invites confusion; and 5/6 now supersedes 7/8 in count (O). In the limit the "best constant" is already zero (OpenAI 2026, and this project), so these are records for explicit circuits at usable sizes only.
5. **How sure.** A short search (under half an hour): arXiv searched systematically (14 queries by API), two citation indexes (both visibly incomplete), about a dozen web searches, one patent family. No lower bound in either count separates our constants from optimal: with free coefficients nothing above linear is known. Not checked: Google Scholar's citing list, the signal-processing journals behind paywalls, and whether the layered "wire count" circuits of Alman (2021) convert to fewer gates.

---

11 October 2026, 00:09 to 00:23 EDT (times from `date`). Private. Nothing published, no git. One file written: this one.

**Marks.** [read] = I read it today in the source named. Most web pages were read through a fetching tool that summarises; where I read the raw text myself I say "raw text". [derived] = my own arithmetic or program today. [recalled, not checked] = from memory. [guess].

**Counts.** N = 2^k points; H is the matrix of +1 and -1; "exact" means every output is a row of H times x with factor 1.
- **(G)**: a gate is any a·u + b·v. Scalings are free.
- **(O)**: every addition, every subtraction and every multiplication by a constant costs one. (Alman and Rao let a multiplication by −1 go free. OpenAI's model has u − v as one gate but would charge a bare −u. The difference is at most a few operations in the circuits discussed here, but it is a difference.)
- **(W)**: a third count used in the circuit papers: the number of wires in a layered circuit whose gates may have any number of inputs. It is not (G) and not (O). See section 3.
- The textbook costs N log2 N in (G) and in (O), and 2 N log2 N in (W) (about 1.88 N log2 N with the depth chosen best).

## 1. Verdicts

| Claim | Verdict | Best published number found | Ours |
|---|---|---|---|
| (a) count (G): (3/4) N log2 N + N/4 for every N | **Apparently new** | (7/8) N log2 N (patent 2002; Alman and Rao 2022, Thm 6.1) | 3/4 |
| 8 points in 20 gates (G) | **Apparently new** | 22 (Alman and Rao Thm 6.2; also what the patent's layout gives) | 20 |
| 8 points in 19 gates (G) | **Apparently new** | 22 | 19 |
| 16 points in 52 gates (G) | **Apparently new** | 56 (patent, stated; Alman and Rao Thm 6.1) | 52 |
| 4 points in 7 gates (G) | **Known** | 7 (Reshef and Alrod, filed 2002; Alman and Rao 2022, Algorithm 9) | 7 |
| (b) count (O): H x/√N in (7/8) N log2 N + N/4, N a power of 4 | **Apparently new** | N log2 N: Alman and Rao's Algorithm 9 (7 additions and 1 halving per 4 points) ties the textbook; their 8-point kernel needs N extra multiplications to reach 1/√N, so it helps only beyond 2^24 points [derived] | 7/8 |
| (b) count (O): exact H x below the textbook from 4,096 points | **Apparently new, but superseded tonight** by the next line | Alman and Rao: from about 2^24 points | 4,096 |
| count (O): exact H x, (5/6) N log2 N + N, below the textbook from 512 points | **Apparently new** | (23/24) N log2 N + (13/12) N (Alman and Rao Thm 1.1) | 5/6 |
| (c) "7/8 is below the 23/24 of Alman and Rao; no paper found" | **True as a comparison of leading constants in one count.** Reword: see section 6 | | |

"Apparently new" means: not found in the search described in section 7. It does not mean proved new.

None of this is improved on by anything I found. The only published results that go below every constant are the asymptotic ones (OpenAI's two preprints of 25 September 2026 and this project's own result). They say nothing about sizes anyone can write down.

## 2. Alman and Rao, read closely

Source: Josh Alman and Kevin Rao, "Faster Walsh-Hadamard and Discrete Fourier Transforms From Matrix Non-Rigidity", arXiv:2211.06459, version 1 of 11 November 2022, version 2 of 14 June 2023, STOC 2023 (doi 10.1145/3564246.3585188). HTML of version 2, https://arxiv.org/html/2211.06459v2 , read 11 October 2026 through the summarising tool, in three passes that together cover the whole text.

- **What is charged.** [read] Section 3.1: "we simply count the number of field additions and field scalar multiplications". A subtraction is an addition. Multiplying by 1, -1 and 0 is free (said in the part on real operations). This is count (O). OpenAI's model is the same up to how a bare negation is charged: gates u+v, u-v, λu, one each [read, raw text, `(not in this repository) upstream/openai-math/preprints/Finite-tensor-savings-and-exact-Fourier-circuits-September-25-2026/build/sections/01-introduction.tex`, lines 36 to 43].
- **Theorem 1.1.** [read] "For any field F, given x in F^N for N a power of 2, we can compute H_N x using at most 23/24 N log N + 13/12 N field operations." It is for H x itself. No scaled H.
- **The breakdown.** [read] 22/24 N log N + N/12 additions and subtractions, 1/24 N log N "divide by 2" operations, and N - 1 "multiply by a power of 2" operations. Section 2.2 gives the count as 23/24 N log N + N/24 (log N mod 3) + N - 1.
- **Their 8-point kernel.** [read] 23 operations on vectors of length N/8: 22 additions and one halving. It returns the transform up to a power of two that is carried down the recursion; the N - 1 final multiplications repair it. So their kernel gives H_8 x / 2 in 23 operations where g-1's gives it in 20. [derived from their description; the top-level call was not visible in the text I was shown]
- **Their second algorithm (Theorem 6.1, Algorithm 9, from the 4-point matrix).** [read] 7/8 N log N additions, 1/8 N log N halvings, N - 1 multiplications by a power of two. Per 4 points: 7 additions and 1 halving. They say it "does not use fewer total operations" than the textbook, but does "when 'divide by 2' operations are ignored". **So Alman and Rao's own published rate with free scalings is 7/8.**
- **Theorem 6.2 (from the 8-point matrix).** [read] 22 N log N / 24 + (N/24)(log N mod 3) additions, N log N / 24 halvings, N - 1 multiplications by a power of two. At 8 points: 22 additions.
- **Where it first beats the textbook.** [derived] From the Section 2.2 expression, at log N = 24 it is one operation below N log N; so from N = 2^24 = 16,777,216. From the bound as stated in Theorem 1.1, from 2^27. They give no crossover size themselves [read].
- **16 points.** [read] "despite some effort, we have not been able to design an improved algorithm with a decomposition of H_16".
- **Open problem.** [read] They call the Ω(N log N) conjecture open, and say theirs is "to our knowledge" the first improvement on the textbook count.
- **Sergeev.** [read] Cited only for the DFT: [Ser17], "On the real complexity of a complex DFT", constant 3.76875. The acknowledgments thank him for answers about that algorithm.

## 3. Everything else found, by count

### Count (G): additions, scalings free

- **Reshef and Alrod, Comsys Communications and Signal Processing, "Reduced complexity fast Hadamard transform", US patent 7,003,536 B2.** Priority and filing 15 August 2002, granted 21 February 2006. Also WO2004017154A2, published 26 February 2004. https://patents.google.com/patent/US7003536 and https://patents.google.com/patent/WO2004017154A2/en , read 11 October 2026 (summarising tool; first 100,000 characters of each, plus the cited-by list). [read]
  - The 4-point transform: w̃ = w0 + w1 + w2 − w3, then each output is ±w̃ ± 2·(one input). "utilizes only seven additions". "Assuming that multiplication by 2 is 'free'".
  - 16 points "is reduced to 7×8=56 operations". A 12.5 % reduction. Outputs are the exact rows of H.
  - For odd k it adds one textbook stage. So 8 points cost 2×7 + 8 = 22 [derived; the patent states no 8-point count].
  - No 8-point brick. No sharing between stages. No formula for general N.
  - One patent cites it: US 8,842,665 (Li and Yu, LSI, 2012, "Mixed radix fast Hadamard transform"). It counts 8 for 4 points and has no reduced brick [read].
- So the rate 7/8 with free doublings was public in 2004. Alman and Rao reach it independently in 2022 by the low-rank-plus-sparse route. I saw no sign that either knows the other [guess; I did not read Alman and Rao's reference list entry by entry].
- Other signal-processing traces [read, search summaries only, not opened]: US patent RE42186 (lossless 4-point Hadamard by ladder steps, eight add/subtract operations reduced to seven); A. Antonevich, "Lifting-based Algorithms for Computing the 4-Point Walsh-Hadamard Transform", Signal Processing Symposium, Kraków, September 2019 (title page only); Suzuki and Ikehara, ICIP 2014, lifting Hadamard blocks for JPEG XR (raw text scanned: adders and shifters, no count that matters here). All are about 4 points.
- Johnson and Püschel, "In Search of the Optimal Walsh-Hadamard Transform" (ICASSP 2000): a search over ways to split the textbook algorithm for speed on real machines; every variant uses N log N additions [recalled, not checked; the search engine returned the title only].
- **Nothing found** for 8 points below 22, for 16 points below 56, or for any rate below 7/8. Searches for "19/20/21 additions", "radix-8", "52/54 additions", "straight-line program", "additive complexity" with Hadamard returned nothing relevant.
- **Exact minima for small sizes.** I found no published exact minimum, in any count, for 4, 8 or 16 points. The hardware literature on "constant matrix times vector with the fewest adders" (shifts free) exists and uses integer programs, but I found no paper applying it to a Hadamard matrix [read, search summaries only].

### Count (O): everything charged

- Alman and Rao's Theorem 1.1 is the only published explicit count below the textbook that I found. Section 2.
- The seminar abstract of 19 November 2024 (J. Alman, University of Chicago theory seminar; raw text read 11 October 2026 from https://mailman.cs.uchicago.edu/mailman/public/theory/2024q4/003571.html ) still says: "(23/24) N log N + O(N) arithmetic operations. This is, to my knowledge, the first improvement on the leading constant." The "very recent progress with Jingxun Liang and Baitian Li" it mentions became papers on rigidity and on depth-2 circuits, not on this constant [read: arXiv:2502.19580, title only; arXiv:2509.14489, abstract and first part of the text].
- **OpenAI, "Finite tensor savings and exact Fourier circuits" and "An explicit power saving for the exact discrete Fourier transform", both 25 September 2026** (local copies under `(not in this repository) upstream/openai-math/preprints/`; introductions read today, raw text). [read]
  - Main theorem: liminf L(n) / (n log2 n) = 0 for the DFT, "an existence theorem in the stated nonuniform model", along lengths that are products of distinct primes. The second paper: O(n (log n)^(1 − 10^-13)) for all lengths.
  - On constants: "Alman and Rao obtain new leading constants for power-of-two transforms ... A fixed leading-constant improvement does not settle the quantified question addressed here."
  - It gives no count at any small size and no crossover size. Its statement cannot see a constant.
  - The task brief calls the paper "Exact Fourier transforms below n log n". I found no preprint with that title; I take it to mean these two.
- Alman, "Faster Walsh-Hadamard Transform and Matrix Multiplication over Finite Fields using Lookup Tables", arXiv:2211.04643, 9 November 2022: O(N log N / log log N) **bit** operations over small finite fields, with tables. A different model. Not comparable. [read, abstract through search results]

### Count (W): wires in layered circuits (not comparable, and the main thing left unchecked)

- Alman, "Kronecker Products, Low-Depth Circuits, and Matrix Rigidity", arXiv:2102.11992, 24 February 2021 (STOC 2021). [read, abstract and ar5iv text, first 100,000 characters] The transform "has a linear circuit of size ≤ (1.81 + o(1)) N log2 N", against "≈ 1.88 N log2 N" for the textbook with the depth chosen best. Size is the number of wires; gates have any number of inputs. Coefficients grow like a power of N.
- Alman, Guan and Padaki, "Smaller Low-Depth Circuits for Kronecker Powers", arXiv:2211.05217, 9 November 2022 (SODA 2023). [read, raw text of the PDF] Depth 2: N^1.443 for the transform. It states no constant for N log N. Their Lemma 1.1 turns depth-2 size N^(1+c/2) into depth-d size O(d·N^(1+c/d)). With c = 0.886 that is about 1.67 N log2 N wires if the hidden constant is 1 [derived; 1.884 × 0.886; the same sum with c = 0.96 gives Alman's 1.81, which is how I know the sum is the right one].
- Sergeev, arXiv:2212.01776 (below): disjointness matrix only.
- Alman and Li, "Kronecker Powers, Orthogonal Vectors, and the Asymptotic Spectrum", arXiv:2509.14489, 17 September 2025. [read, first 100,000 characters] Depth 2 for the transform stays at N^1.443. It says better depth-2 circuits improve "the leading constants of algorithms like Yates' algorithm and the fast Walsh-Hadamard transform" but gives no number. Under SETH there is no depth-2 circuit of size N^(1+o(1)) for the transform.
- **Why (W) is not (G).** A gate with f inputs is f − 1 gates of (G), so gates = wires − nodes. In (W) a wire that just carries a value to the next layer costs one; in (G) it is free. The 4-point brick shows the gap: 16 wires as a layered circuit (no better than the textbook's 16), but 7 gates against 8. So a good (W) number does not give a good (G) number, or the reverse. [derived]
- **Not checked.** I did not convert the 1.81 or the 1.67 circuits into (G). A crude bound from "gates = wires − nodes" puts them anywhere between about 0.55 and 1.5 N log2 N, which decides nothing [derived]. My guess is that they are above the textbook in (G), because they are tuned to save carried wires, which (G) does not charge [guess]. This is the one place where a published construction could, in principle, already be below 3/4 in (G) without saying so.
- In the other direction: our 3/4 family is a circuit with at most 1.5 N log2 N + N/2 wires if layers are not required (two wires per gate) [derived]. That is below 1.81 and below 1.67, but the comparison is unfair to those papers, which keep layers. I would not claim it.

## 4. The Sergeev question

- Igor Sergeev's arXiv author page (https://arxiv.org/a/sergeev_i_1 , read 11 October 2026) lists nothing on the Walsh-Hadamard transform between 2017 and 2026. [read]
- What exists:
  - I. S. Sergeev, "Notes on the complexity of coverings for Kronecker powers of symmetric matrices", arXiv:2212.01776, 4 December 2022. [read: abstract page, and the raw text of the PDF searched for "Hadamard", "Sylvester", "log N": no hit] It reworks the method of Alman, Guan and Padaki for symmetric matrices and gets depth-2 size O(N^1.251) for the Boolean disjointness matrix. No Hadamard matrix, no N log N constant.
  - I. S. Sergeev, "On the real complexity of a complex DFT", 2017: constant 3.76875 for the FFT, cited by Alman and Rao. [read, via Alman and Rao]
  - The number 7/8 for the Walsh-Hadamard transform: that is Alman and Rao's Theorem 6.1, additions only.
- Two searches in English and one in Russian for a Sergeev note on this transform found nothing. I did not search mathnet.ru or the Russian journals directly.

## 5. Lower bounds, by count

- **Free coefficients, counts (G) and (O).** No lower bound above linear is known for any explicit matrix, and none for H. [read on 9 October by an earlier reader of this project, `(not in this repository) wht33/research-2026-10-09/readers/lit-lower-bounds.md`, section 3, quoting Kumar and Volk, arXiv:1904.01182; I re-read today only that Alman and Rao and OpenAI both call the question open.] So nothing published says 3/4 or 5/6 is close to best, or far from it.
- **Bounded coefficients (Morgenstern 1973, J. ACM 20).** [read, as quoted by Alman and Rao, Section 1.4: "a 1/2 N log N lower bound" for coefficients "of magnitude at most 1"; original not read] The argument is by the determinant, and det H = N^(N/2).
  - Our (G) circuits use coefficients 1 and 2 only. The same argument with |a| + |b| ≤ 3 gives 0.3155 N log2 N [derived by critic b-0; I did not check the general form in Morgenstern's paper]. So this family lives between 0.3155 and 0.75.
  - It says nothing about H x/√N, whose determinant is 1. This is why the scaled and the exact transform must be kept apart in count (O). OpenAI's introduction makes the same point: "the normalization must be retained when comparing the restricted models" [read].
- **Layered circuits with bounded coefficients (Pudlák 2000).** [read, as quoted in Alman 2021] Depth d: at least d·N^(1+1/d)/c² wires. Any depth: at least (e·ln 2/c²) N log2 N ≈ 1.884 N log2 N / c² wires. Count (W) only.
- **Chazelle's spectral bound; Ailon's bounds (2013 to 2016) for circuits of 2×2 rotations and for well-conditioned circuits.** [read on 9 October by the earlier reader; Alman and Rao's one-line account read today] Order n log n under those hypotheses, with constant 1/2 for unitary gates. Our circuits are not of that kind.
- **Depth 2.** Ω(N log N) wires for H (Alon, Karchmer, Wigderson 1990) [read, as quoted by Alman and Li 2025].
- **Exact small cases.** None published that I found. The project's own "4 points cost exactly 8 in count (O)" and "at least 2N − 1 gates in (G)" have no counterpart in the literature that I could find.

## 6. What to change in WAVE2-NOTE.md

- Line 13, "The best rate before tonight was 7/8": true of the project and, as it happens, of the literature. Say whose: Reshef and Alrod (filed 2002) and Alman and Rao (2022, Theorem 6.1).
- Line 14, "The leading constant 7/8 is below the 23/24 of Alman and Rao (2022)": true, same count, and both are for exact H x once the +N terms are included. Add three things. (i) Their count and OpenAI's are the same (up to a bare negation). (ii) Their own additions-only number is also 7/8, so name the count each time. (iii) The later 5/6 is the better number in count (O).
- Line 17, "so the 7-gate brick is not special to the transform": the brick itself is at least 24 years old.
- Anywhere "record" is written: it is a record for an explicit circuit at a given size. As a statement about the limit it is not one, since the published results give fewer than c·N log N for every c > 0.

## 7. How thorough, and what remains unchecked

Done, all on 11 October 2026 between 00:09 and 00:23 EDT:
- Alman and Rao: whole HTML text in three passes (summarising tool).
- arXiv API, 14 queries, sorted by date [raw results read]: "Walsh-Hadamard" with each of "leading constant", "operation count", "arithmetic operations", "number of additions", "fewer additions", "fewer operations", "linear circuit(s)", "arithmetic circuit", "non-rigidity"; "Hadamard" with "straight-line program", "additive complexity"; every 2026 paper mentioning Walsh-Hadamard in cs.CC, cs.DS, cs.SC, cs.IT, eess.SP, math.CO (14 papers, none on operation counts); all of J. Alman's papers since 2023 (27); K. Rao (4). Result: no paper after November 2022 on this constant.
- Citing lists. Semantic Scholar: 7 papers cite Alman and Rao, 13 cite Alman 2021, 5 cite Alman, Guan and Padaki. OpenAlex: 3 cite Alman and Rao. None improves the constant. **These lists are incomplete**: OpenAI's preprint cites Alman and Rao and is not in them.
- Web searches: about twelve, in English, one in Russian.
- Patents: one family found and read; its single citing patent read.
- I replayed the 19-gate listing of `g-1.md` myself in exact integers: 19 gates, outputs are rows 0 to 7 of H_8 with factor 1 [derived; script in the session scratchpad, not kept].

Not done:
- Google Scholar's citing list for Alman and Rao (I could not open it). This is the most likely place for a follow-up I missed.
- The full text of Alman 2021 beyond the first 100,000 characters, and any conversion of its circuits to (G). See section 3.
- The STOC proceedings version of Alman and Rao against the arXiv version; a possible journal version.
- Signal-processing journals and conference papers behind paywalls (IEEE, Elsevier). The patent suggests engineers knew the 4-point brick; an 8-point or interleaved version could sit in a 2000s conference paper that no search engine summarises. I found none.
- Russian-language journals; theses; lecture notes; MathOverflow and cstheory threads (one search, nothing).
- The repositories that grew around OpenAI's release in the last three weeks. They chase the exponent, not constants [read on 9 October by the earlier reader, `web-frontier.md`], but I did not look for small circuits there.
- Morgenstern's and Pudlák's original papers.

## 8. Sources, with the date read (all 11 October 2026 unless said)

- J. Alman, K. Rao, 2022/2023, arXiv:2211.06459v2, https://arxiv.org/html/2211.06459v2 .
- E. Reshef, I. Alrod (Comsys), filed 2002, US 7,003,536 B2, https://patents.google.com/patent/US7003536 ; WO2004017154A2, https://patents.google.com/patent/WO2004017154A2/en .
- C. Li, M.-L. Yu (LSI), 2012, US 8,842,665 B2, https://patents.google.com/patent/US8842665 .
- J. Alman, 2021, arXiv:2102.11992, https://arxiv.org/abs/2102.11992 and https://ar5iv.labs.arxiv.org/html/2102.11992 .
- J. Alman, Y. Guan, A. Padaki, 2022, arXiv:2211.05217 (abstract page and PDF text).
- I. S. Sergeev, 2022, arXiv:2212.01776 (abstract page and PDF text); author page https://arxiv.org/a/sergeev_i_1 .
- J. Alman, B. Li, 2025, arXiv:2509.14489, https://arxiv.org/html/2509.14489v1 .
- J. Alman, 2026, "Superlogarithmic-Rank Matrix Rigidity for the Walsh-Hadamard Transform", arXiv:2608.06592, 6 August 2026 (abstract): rigidity over F_3, no circuit count.
- B. Kivva, 2021, "Improved upper bounds for the rigidity of Kronecker products", arXiv:2103.05631 (abstract): rigidity only, no operation count.
- J. Alman, 2022, arXiv:2211.04643 (abstract via search results).
- J. Alman, H. Yu, 2024, "Improving the Leading Constant of Matrix Multiplication", arXiv:2410.20538 (title only): matrix multiplication, not this transform.
- J. Alman, seminar abstract, 19 November 2024, https://mailman.cs.uchicago.edu/mailman/public/theory/2024q4/003571.html (raw text).
- OpenAI, 25 September 2026, two preprints, local copies named in section 3 (raw text of the introductions).
- T. Suzuki, M. Ikehara, ICIP 2014, https://www.cs.tsukuba.ac.jp/~taizo/pdf/conference/201410_IEEE_ICIP.pdf (PDF text scanned).
- A. Antonevich, 2019, https://matematyka.uwb.edu.pl/en/scientific-research/conference-participation/lifting-based-algorithms-for-computing-the-4-point-walsh-hadamard-transform-1160.html (title page only).
- Semantic Scholar API (citing lists) and OpenAlex API, https://export.arxiv.org/api/query (arXiv API).
- Project files read: `WAVE2-NOTE.md`, `e2-0.md`, `g-1.md`, `b-0.md`, `h-3.md`, `c-0.md`, `c-1.md` (first lines and their literature sections), and the 9 October reader notes `lit-lower-bounds.md` and `web-frontier.md`.
