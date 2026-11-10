# SC3102 Handoff

Where I am in this course, so I (or Claude) can pick up on another device. Last updated 2026-11-11.

## Where I am

- **Part 2 term test:** 12 Nov 2026, 16:00–17:00. Closed-book and on paper, with one double-sided A4 sheet of notes allowed. The listed topics are "Discrete Signals, DFT, Z and Laplace Transforms", which is Lectures 0–5 (Tutorials T01–T04). Lecture 6 (differential equations, T05) is probably not included. `Cheatsheet.docx` is the Part 1 sheet only.
- **Part 1 (continuous time):** done and understood. Tutorials 1–4 have worked solutions in `Tut/Part1/`.
- **Part 2 (discrete time):** working through `notes/Part2_Discrete_Time_Guide.md` one step at a time. Covered in the Q&A so far: Steps 1–9, which are sampling through the DTFS, leakage, circular convolution and the DTFT. I understand these conceptually but am still shaky. **The Z-transform and the ROC (Steps 11–13) don't make sense to me yet; that's next.** On 2026-11-11, Steps 5–13 were rewritten at a beginner level: Steps 5–10 from this Q&A, and Steps 11–13 from scratch using T03 as the worked examples.
- **Resume here:** start at guide **Step 11.1**, the fading table. Read through 11.3 and ask about the first line that doesn't make sense. Then go on to Step 12 (ROC on the |z| ruler), Step 13 (partial fractions), and the self-check questions 11–13.
- **After Z:** Step 14 (difference equations, T04 Q1–2), then Step 15 (Laplace, T04 Q3–4). Both are still in their old, short form.
- **Laplace and LCCDEs** (Step 15, Part 2 Tutorials 04–05) are the last lecture topic and haven't been taught yet.
- **Labs 1–4:** done (`Lab1/` … `Lab4/`, each with a `_Answers.md`).

## What's where

| Path | Contents |
|---|---|
| `notes/Part2_Discrete_Time_Guide.md` | The 15-step discrete-time study guide. It refers to `../Slides/`, which is local only: it's in `.gitignore`, so other devices won't have it |
| `Slides/` (local, gitignored) | Part 2 lecture slides, numbered from 0. `sc3102-transform-lecture-00-…`=L0 discrete signals and systems, `lecture.pdf`=L1 DFT, `lecture(1)`=L2 DTFS/circular convolution/DTFT, `lecture(2)`=L3 Z-transform, `lecture(3)`=L4 LCCDEs with Z (its title says "Lecture 4"), `lecture(4)`=L5 Laplace, `lecture(5)`=L6 differential equations. `Introduction`, `Signals(1)`, `Systems`, `Transforms(1)` are Part 1 |
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
- **The DFT assumes the block repeats:** worked examples are in guide 7.1. cos(πn/2) with N=4 is clean; cos(πn/4) with N=4 jumps at the seam and every bin is nonzero; cos(πn/4) with N=8 is clean again. The inverse DFT is always exact inside the block, so leakage only affects how the spectrum reads.
- **N₀ vs N (guide 7.2):** N₀ is the signal's period, calculated from the formula. N is the DFT size, which you choose. No leakage ⇔ N is a whole multiple of N₀.
- **Finding the period from samples alone:** look for the smallest N₀ with x[n+N₀]=x[n]; no DFT is needed. This usually fails with real data, for three reasons: f₀/f_s must be a fraction, there's noise, and several tones give an LCM. In practice you reduce leakage instead of hunting for N.
- **Window length vs window shape (guide 7.3):** length trades timing against frequency resolution (bins f_s/N apart). Shape (tapering the ends) reduces leakage. Neither is in the lecture titles; only f_k = k·f_s/N is examinable.
- **Circular convolution (guide Step 8):** derived from the DFT product: pairs count when m+l ≡ n (mod N). Padding to N ≥ Lx+Lh−1 stops the wrap. Continuous time avoids it because the CTFT and DTFT cover the whole axis; the DFT is the DTFT sampled, which makes time repeat.
- **M and N on the DTFT slides (guide 9.1–9.3):** the block runs from −M to M, so N=2M+1. The gold dots are DTFS samples of the solid curve X_M(Ω), which approaches the true X(Ω). The slide's signal is (½)^|n|.
- **Ω has one meaning (guide 5.3 box):** radians per sample, = ω/f_s. θ = Ωn is "where you've got to". The slides write ω for Ω in Part 2.
- **Why u[n] has no DTFT (guide 9.6):** the partial sums never settle (X_M(0)=M+1).

## Conventions

- Ω is discrete-time frequency (rad/sample) and ω is continuous-time (rad/s). The slides use ω for both.
- N₀ is a signal's period and N is the DFT size. The slides use N for both.
- This course writes the DTFS exactly like the DFT: no 1/N in the analysis sum, and 1/N in synthesis.

## Known errors in the official Part 1 material

See `Tut/Part1/Disagreements.md`. The main ones are in the Tutorial 3 answer keys:
- Ex 3(f): the output should be non-zero on 5≤t<10, not 3≤t<8.
- Ex 2(a) is time-*variant*.
- Ex 3(d) is ⅓t³u(t).

## Notes for Claude

- Explain one step at a time, with worked numbers and tables, and connect each discrete-time idea to its continuous-time twin.
- On NTULearn, the Part 1 solution PDFs can't be downloaded from the viewer. The question sheets have "Download Original File".
- Offered, not started: a Part 2 double-sided A4 cheat sheet for the term test.
- **My level (2026-11-11):** still weak. Don't skip steps, and work every idea with real numbers. Steps 11–13 now cover all of T03: series expansion (13.5), the x[−n] and aⁿx[n] properties (13.1), the damped-cosine Z pair (13.2), and T03 Q1/Q2/Q4 worked through.
- **Guide gaps compared with the tutorials** (the guide doesn't cover these yet):
  - T04 Q1: partial fractions in z² with a cosine input, and setting initial conditions to cancel the transient
  - T04 Q2: H(z) with a delay x[n−k], for k=2 and k=−1
  - Laplace damped cosine/sine pairs and partial fractions with a quadratic factor (T04 Q3b–c)
  - Laplace ROCs and whether the CTFT exists (T04 Q4); Step 15 is only a comparison table
