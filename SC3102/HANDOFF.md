# SC3102 Handoff

Where I am in this course, so I (or Claude) can pick up on another device. Last updated 2026-11-10.

## Where I am

- **Part 1 (continuous time):** done and understood. Tutorials 1–4 have worked solutions in `Tut/Part1/`.
- **Part 2 (discrete time):** working through `notes/Part2_Discrete_Time_Guide.md` one step at a time. I've covered Steps 1–7 (sampling through the DTFS). **Next is Step 8, circular vs linear convolution**, then Step 9, the DTFT.
- **Laplace and LCCDEs** (Step 15, Part 2 Tutorials 04–05) are the last lecture topic and haven't been taught yet.
- **Labs 1–4:** done (`Lab1/` … `Lab4/`, each with a `_Answers.md`).

## What's where

| Path | Contents |
|---|---|
| `notes/Part2_Discrete_Time_Guide.md` | The 15-step discrete-time study guide. It refers to `../Slides/`, which isn't in this repo |
| `Tut/Part1/Tutorial{1..4}(…).pdf` | Part 1 question sheets, with short answer keys |
| `Tut/Part1/Tutorial{1..4}_Solutions.md` | Worked solutions that follow the official NTULearn method step by step, written in our own words |
| `Tut/Part1/Disagreements.md` | Errors in the official answers, plus the course method compared with how it's done in practice |
| `Tut/Part2/student*.pdf` | Part 2 questions. `student.pdf`=T01 discrete signals and systems, `(1)`=T02 DFT and DTFS, `(2)`=T03 Z-transform, `(3)`=T04 difference equations and Laplace, `(4)`=T05 differential equations |
| `Tut/Part2/teacher*.pdf` | Part 2 solution slides. `teacher.pdf`=T01, `(1)`=T02, `(2)`=T03, `(3)`=T04. **There are no T05 solutions yet** |

## Already explained in the Q&A (no need to repeat)

- **FFT:** you don't need the algorithm for this course. Know three things: it gives exactly the same output as the DFT, it costs N log₂N instead of N², and it works by splitting into even and odd samples. What you do need is a fast hand-computed 4-point DFT, using the matrix of 1, −j, −1, j.
- **What "the DFT handles a finite list" means:** the sum stops at N−1, the frequencies are 2πk/N, and the inversion relies on q^N=1 (whole laps). This is not about energy signals. Finite length is not the same as finite energy. The synthesis formula repeats the block forever, which is what causes leakage.
- **Harmonics:** whole-number multiples kf₀ of the fundamental. The fundamental itself can be missing (T4 Q1(a)).
- **Why continuous time needs infinitely many harmonics but the DTFS needs only N:** harmonic k+N lands on exactly the same samples as harmonic k, which is the same thing as aliasing. A period has N values, so N coefficients are enough. A continuous square wave needs infinitely many harmonics; the discrete [1,1,−1,−1] is just √2·cos(πn/2−π/4). The infinite part of the continuous series is the Σ from k=−∞ to ∞ (T4 Q1(b) has C_k≠0 for every k, because of its jump).
- **DFT vs DTFS:** identical arithmetic. The DTFS adds the claim that the signal repeats every N samples, which is only true if N is a period. Part 2 T02 Q2(c) is the test case: a[12]=−1≠a[0].

## Conventions

- Ω is discrete-time frequency (rad/sample) and ω is continuous-time (rad/s). The slides use ω for both.
- This course writes the DTFS exactly like the DFT: no 1/N in the analysis sum, and 1/N in synthesis.

## Known errors in the official Part 1 material

See `Tut/Part1/Disagreements.md`. The main ones are in the Tutorial 3 answer keys:
- Ex 3(f): the output should be non-zero on 5≤t<10, not 3≤t<8.
- Ex 2(a) is time-*variant*.
- Ex 3(d) is ⅓t³u(t).

## Notes for Claude

- Explain one step at a time, with worked numbers and tables, and connect each discrete-time idea to its continuous-time twin.
- On NTULearn, the Part 1 solution PDFs can't be downloaded from the viewer. The question sheets have "Download Original File".
- Offered but not done yet: rewrite the "Problem" line in Step 7 of the notes, which was confusing.
