# SC3102 Handoff

Where I am in this course, so I (or Claude) can pick up on another device. Last updated 2026-11-12.

## Where I am

- **Part 2 term test:** 12 Nov 2026, 16:00–17:00. Closed-book and on paper, with one double-sided A4 sheet of notes allowed. **Confirmed scope (2026-11-12): discrete time only.** That's the five discrete decks (`lecture-00` to `lecture(3)`: discrete signals, DFT, DTFT, Z, and LCCDEs with Z), which means T01–T03 plus T04 Q1–2. **Laplace and differential equations are NOT tested** (`lecture(4)`, `lecture(5)`, T04 Q3–4, T05). `Cheatsheet.docx` is the Part 1 sheet only.
- **Part 1 (continuous time):** done and understood. Tutorials 1–4 have worked solutions in `Tut/Part1/`.
- **Part 2 (discrete time):** working through `notes/Part2_Discrete_Time_Guide.md` one step at a time. Covered in the Q&A so far: Steps 1–9, which are sampling through the DTFS, leakage, circular convolution and the DTFT. I understand these conceptually but am still shaky. **The Z-transform and the ROC (Steps 11–13) don't make sense to me yet; that's next.** On 2026-11-11, Steps 5–13 were rewritten at a beginner level: Steps 5–10 from this Q&A, and Steps 11–13 from scratch using T03 as the worked examples.
- **Resume here (test-day plan, 2026-11-12):** the Z concept and FIR/IIR are now understood. Do the tutorial questions in this order, attempting each before checking it against the guide section or with Claude:
  **The question list, in tutorial order T01 → T02 → T03 → T04 Q1–2, is in `Tut/Part2/Question_Tracker.md`.** It has tick boxes, what each question tests, where to check it, and hidden final answers. Within T03 it goes easiest first, finishing with Q4. ⭐ marks the questions for when time is short. **Current position: T01 is finished, and the user is now on T02**, starting with Q1 (the DFT matrix: G, G^H and why it uses −j are already explained). Next in the tracker: T02 Q1(a)(d) → Q2(a)(b) → Q4 → Q3(a)(b), then T03.
  Cheat sheet (handwritten, double-sided A4): the content is in the Claude Doc "SC3102 Part 2 Cheat Sheet" (https://claude.ai/artifact/DhJn8mg5wuztEbXWaBpQTi). There's also a print-ready 2-page A4 copy at `notes/Part2_Cheat_Sheet.pdf` (built from `notes/Part2_Cheat_Sheet.html`; to rebuild, open the HTML in a browser and print to A4). Skip T02 Q3(c), T03 Q1(a)(c), T03 Q2(b), T03 Q3(d) and all of Laplace.
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

**Standing rule (2026-11-12):** log every new concept question in `notes/Part2_QA_Concepts.md` and add a compact version to section 9 of the cheat sheet. Update both the HTML/PDF (keep it at exactly 2 pages) and the Claude Doc. **Both sides are now full:** the Side 2 block "9. Q&A notes (continued)" used up the last free space at the bottom of column 2, so any new item has to replace or shorten an existing line. Rebuild the PDF with headless Edge: `msedge --headless --no-pdf-header-footer --print-to-pdf=<out> file:///…/Part2_Cheat_Sheet.html`, then check that it has 2 pages.

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
- **What X(z) is (guide 11.1–11.2):** it's the transform of x, just like X(Ω). The letter in the brackets tells you which transform it is. X(z) is the DTFT of x[n]·r⁻ⁿ, with z=re^{jΩ}: |z| is how hard you fade and the angle of z is the frequency. Each circle |z|=r is one DTFT, and the circle |z|=1 is the plain DTFT. X(Ω)'s axis from −π to π wraps round to form that unit circle: Ω=0→z=1, π/2→j, ±π→−1. It's one dial (Ω) against two (r and Ω), not a line against a plane. The building blocks are spirals zⁿ, not steady walkers, which is why 2ⁿu[n] works (with r=4 the faded signal is 0.5ⁿ). On the quiz, X(z) is a fraction/tag/algebra tool, not a frequency plot.
- **T01 Q1, N and m in the official solution:** N is the period (a whole number of samples) and m is the number of full 2π laps in those N samples. Ω₀N = 2πm, so look for the smallest m that makes N a whole number. Continuous time always uses m=1; discrete time may need more laps (cos(3.5πn): m=7, N=4). Shortcut: Ω₀/2π = m/N in lowest terms. Ω₀/2π = f/fₛ (cycles per sample), so a sampled sinusoid is periodic ⇔ f/fₛ is rational. Reduce to lowest terms first: the bottom number is N₀ and the top number is the number of cycles. The rule gives when the *walker* returns. For a single sinusoid, the true N₀ is only smaller when every sample is 0 (sin(πn), sin(3πn), …; the rule says 2 but the zero signal has period 1). So simplify first (sin(πn)=0, aliases), then apply the rule.
- **Poles and zeros (guide 12.7, Lab 4 1B):** they belong to a fraction, X(z) or H(z), so signals and systems both have them. Make one fraction in +powers of z, factor, cancel; zeros = top roots, poles = bottom roots. The lab's z/(z−0.6) + z/(z−1.2) = 2z(z−0.9)/(…): the zero at 0.9 is hidden until you combine (H(0.9) = 3 − 3 = 0). 1/(1 − 0.5z⁻¹) = z/(z−0.5) has a zero at 0. In an LCCDE, the x-terms give the zeros and the y-terms give the poles. A zero blocks the input zⁿ (the averager kills (−1)ⁿ); only poles set the ROC and stability.
- **What pⁿ, zeros and the ROC mean physically:** pⁿ = ×p every step (0.5ⁿ dies, 1ⁿ stays, 2ⁿ grows, (−0.5)ⁿ flips). **Poles are the ROC edges *because* pole p ⇔ pⁿ in the signal:** 0.5ⁿu[n] gives X = 1 + (0.5/z) + (0.5/z)² + …, which adds up only for |z| > 0.5 (z = 1 → 2, z = 0.5 → ∞, z = 0.25 → blows up). The "feedback number" is just the coefficient of y[n−1]: y = 0.5y[n−1] + x → H = z/(z−0.5), pole 0.5.
- **ROC ≠ stable:** the ROC is where Σh[n]z⁻ⁿ converges *with help from the weight*. Stable = Σ|h| converges with no help = the weight at |z| = 1. Lab 4 Region 0's h blows up going left (−165.6 at n = −10), but at z = 0.3 the weighted terms shrink (sum −1.33 = H(0.3)), so it has an ROC (|z| < 0.6). At z = 1 there's no help, so it's not stable. All three regions have an ROC; only Region 1 contains |z| = 1. Formula + ROC = exactly one signal. "Stable" describes the signal, not the transform; the transform only exists or doesn't (2ⁿu[n] has one). The DTFT exists only when the system is stable.
- **The Z-transform doesn't make an unstable signal stable for the DTFT:** a circle r in the ROC gives the DTFT of the faded copy r⁻ⁿx (2ⁿ with r = 4 → 0.5ⁿ). Putting z = e^(jΩ) into the formula outside the ROC gives the *other* signal's DTFT (z/(z−2) at Ω = 0 = −1 = Σ of −2ⁿu[−n−1]). Unstable means no DTFT, and no frequency response physically. For unstable systems, the Z-transform is for algebra.
- **What the Z-transform is for ("analyse"):** all systems, not just unstable ones. The LCCDE comes first, and Z *solves* it into formulas for h[n], y[n], causal/stable and (if stable) the frequency response. y = 0.5y[n−1] + x, x = u → (2 − 0.5ⁿ)u[n] (by hand 1, 1.5, 1.75, …). y = 2y[n−1] + x → (2ⁿ⁺¹ − 1)u[n] (1, 3, 7, 15), which the DTFT can't do.
- **Two meanings of "analyse":** Fourier = the frequencies in a signal / H(Ω) = DTFT of h for a system (stable only). Z = poles/zeros/ROC → h, y, causal, stable (any system). They meet at z = e^(jΩ). For y = 0.5y[n−1] + x: H(0) = 2, H(π) = 0.67, so it's low-pass. A zero = an input it blocks: differencer kills a constant, averager kills (−1)ⁿ, x[n] + x[n−2] kills 50 Hz hum at fₛ = 200 Hz. For a signal, zeros are just bookkeeping. The ROC picks which system one formula is: z/(z−2) with |z| > 2 is 2ⁿu[n] (causal, unstable), with |z| < 2 it's −2ⁿu[−n−1] (stable, not causal). ROC outside → real time; |z| = 1 inside → stable.
- **FIR vs IIR (guide 14.5):** both names describe h[n], the response to a single kick δ[n]. FIR has no feedback: y=½x[n]+½x[n−1] gives h=[½,½] and then stops, the coefficients are h, every pole is at 0, and it's always stable. IIR has feedback: y=0.5y[n−1]+x[n] gives h=0.5ⁿ (1, 0.5, 0.25, …, never 0), H=z/(z−0.5), and it's stable only if the pole is inside the unit circle. Changing 0.5 to 2 makes it blow up. Quick test: is y[n−k] on the right-hand side, or is there a nonzero pole?

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
- **(2026-11-12) Don't pile up analogies.** A bell, an echo, interest and cooling all in one answer confused me badly. Build from what I already understand (e.g. "poles bound the ROC") and add one fact at a time, with numbers.
- On NTULearn, the Part 1 solution PDFs can't be downloaded from the viewer. The question sheets have "Download Original File".
- Offered, not started: a Part 2 double-sided A4 cheat sheet for the term test.
- **My level (2026-11-11):** still weak. Don't skip steps, and work every idea with real numbers. Steps 11–13 now cover all of T03: series expansion (13.5), the x[−n] and aⁿx[n] properties (13.1), the damped-cosine Z pair (13.2), and T03 Q1/Q2/Q4 worked through.
- **Guide gaps compared with the tutorials** (the guide doesn't cover these yet):
  - T04 Q1: partial fractions in z² with a cosine input, and setting initial conditions to cancel the transient
  - T04 Q2: H(z) with a delay x[n−k], for k=2 and k=−1
  - Laplace damped cosine/sine pairs and partial fractions with a quadratic factor (T04 Q3b–c)
  - Laplace ROCs and whether the CTFT exists (T04 Q4); Step 15 is only a comparison table
