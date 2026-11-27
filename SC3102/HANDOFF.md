# SC3102 Handoff

Where I am in this course, so I (or Claude) can pick up on another device. Last updated 2026-11-28.

## Where I am

- **Final exam: Mon 30 Nov 2026, 09:00–11:00.** It has 4 compulsory questions of 25 marks each, and one double-sided A4 sheet is allowed. **It covers the whole course, including Laplace and differential equations.** The "NOT tested" note below applied only to the Part 2 term test; every past final has a Laplace question.
- **Resume here (2026-11-28): doing the past papers. Next: 24S2, from Q1(a)**, then 25S2, then the rest as revision.
  - **Progress:**
    - **25S1: done** (2026-11-26/27, all of Q1–Q4).
    - **24S1: done** (2026-11-27/28). Q1(a)–(b) were done on the other device. I did Q2 to Q3(b)(i) and Q4(b) myself; Claude explained Q1(c), Q3(b)(ii), Q4(a) and Q4(c).
    - **24S2: not started.** It's the next paper.
    - **25S2: not started.** On 2026-11-28 Claude showed its Q1(a) by mistake; start it again from Q1(a).
    - **23S1 and 23S2:** revision only.
  - **2026-11-28: the histories were merged.** On 2026-11-27 the two devices split. One worked on branch `sc3102-25s1-walkthrough` (the 25S1 walkthrough and the exam-style rewrite); the other worked on `main` (24S1 Q1(a)–(b)). Both are now merged into `main`. **Work on `main`, and `git pull` before starting.**
  - **Solutions:** worked solutions for all **six** papers, plus a whole-course topic map, are in `PYP/Solutions/` (start with `00_Exam_Guide.md`). Each file has a collapsed answer key for self-marking.
  - **Rewritten 2026-11-27:** all five original files now have an **Exam answer** block in every part (question quoted, given/asked, named steps, every line shown, boxed answer, a check), followed by an **Explanation** block. No final answers changed. The new figures are in `figs/` (`*_split`, `*_slide`, `*_map`, `*_rows`, `25S2_Q4a_s_to_z`).
  - **24S2 (new 2026-11-28):**
    - **The paper:** `PYP/SC3102-24S2.pdf`, the original 4 pages. It's on NTULearn under "Past Year Exam Papers" → "SC3102: SEMESTER 2 EXAMINATION 2024-2025", attachment `CE3102-24S2.pdf`. The download button is disabled, but the professor emailed to say students may copy it. A Claude-in-Chrome agent fetched the file the viewer loads. Chrome saves to `D:\Download`, which also holds a spare copy.
    - **Solutions:** an agent wrote `PYP/Solutions/SC3102-24S2_Solutions.md` in the same format as the others. Its figures are `figs/24S2_*`, drawn by `PYP/Solutions/make_figures_24S2.py`, which also re-checks the answers. The paper is now in `00_Exam_Guide.md` too. The least certain part is **Q3(a)(ii)**, the DTFT sketch of a periodic signal. The slides never draw one, so the main answer gives impulse areas 2π·a_k and lists the other labels a marker might expect.
  - **Final cheat sheet: BUILT 2026-11-28** (see the What's-where table). It's 2 pages, A4 landscape, in the same panel style as the Part 2 sheet. It has 21 numbered panels plus a recipes panel. The text is 6pt Calibri, every fraction is stacked, and the highlight is #ffd84d, which prints as light grey in black and white. **To do: a test print to check the 6pt is readable.** If it isn't, trim panels and enlarge the font.
  - **Optional leftovers:** three figures drawn by `make_figures.py` need small fixes. The solution text is already correct in all three.
    - `23S1_Q2c_X.png`: the title says the main lobe reaches |f| = 0.5; it's actually 0.25.
    - `25S2_Q4b_y.png`: the "final value −23/24" label sits on a dashed line.
    - `25S2_Q4a.png`: the e^(jΩ) label is half-hidden by the ROC box.
  - Every concept question is logged in `notes/Part2_QA_Concepts.md`. 2026-11-24 covered:
    - discrete LCCDE → Laplace → differential equations (now Steps 14–16 of the guide);
    - LCCDE vs LTI;
    - when a Σ p(t − nT) sum is periodic.
  - 2026-11-26 covered:
    - s ↔ z (z = e^(sT));
    - sums of periodic signals and LCM;
    - power and power signals; calculus refresher;
    - autocorrelation vs convolution; PSD/ESD/Parseval;
    - CTFT by hand and |a + jb|²;
    - FS vs FT vs Laplace;
    - FS methods (Euler vs integral vs table shortcut) and harmonics;
    - time-shift property; the properties tested in past papers;
    - the flip in convolution;
    - the 25S1 Q1(b) hint slips;
    - a flipped phase at ±1 Hz in the "modulated waveform" answer.
  - 2026-11-27 covered (25S1 Q2(b) to Q4(b)):
    - **Convolution and pairs:** convolution with overlapping δ copies; the new transform-pairs table (`notes/Transform_Pairs.pdf`).
    - **Laplace concepts:**
      - σ in the Laplace ROC; why Laplace and Z have both a fade and a spin;
      - |X(s)| as a surface (the σ = 0 slice is the CTFT); finding poles;
      - what each transform is for; what a pole means physically.
    - **Rules and links:** the unilateral derivative rule on a timeline; how s and z connect (z = e^(sT)).
    - **Q3(c) concepts:**
      - the characteristic polynomial, and why s = 0 is a pole of Y but belongs to the input;
      - initial conditions; why h is defined from rest; zero-input = (initial-condition terms)/A(s);
      - zero-input vs zero-state, natural vs forced, transient vs steady state, with the integrator exception.
    - **Where an ROC comes from:** signal → transform uses the table and the overlap; transform → signal uses the poles and the description. Q3(c) never asks for one.
    - **Working methods:**
      - doing Q3(c)(ii) by reusing (i); the Z time-shift rules;
      - which initial conditions each part uses (a checklist).
    - **Q4 concepts:**
      - 4(a)(iv) steady state via H(e^(jΩ₀));
      - inverse Z: the 3 methods vs the fixes for equal powers on top and bottom;
      - long division; Laplace with equal powers (K + cover-up); Z with top power > bottom means non-causal;
      - the recursion check; an N-point inverse DFT gives exactly N values.
  - 2026-11-27, on the other device (24S1 Q1(a)), logged under "Complex-number tricks":
    - why 1/j = −j;
    - why sin(6πt) has spectral lines at ∓90° even though its bracket has no offset (phase is measured against a cosine).
  - 2026-11-28, logged under "24S1 walkthrough":
    - **Angle of a sum (Q3(b)(ii)):** you can keep H as 2/(s+1) + 4/(s+3), but you can't add the terms' angles; only products and quotients work that way. Add the terms as a + jb first, then take one angle.
    - **"General frequency behaviour" (Q4(a)):** what the filter type means; evaluating H on the jω-axis / unit circle at the low and high ends; the geometric distance method and a band-pass example.
      - The geometric method is **not in the slides**. The course's way is L2 p.103–106 (the two-sample mean). Give the numbers first and use geometry as the reason.
    - **Degrees:** Laplace answers have top < bottom, Z answers have top = bottom. The reasons: 1/(s−p) vs z/(z−p); X(∞) = x[0]; the initial value theorem.
    - **The DFT:** what kn means (the number of quarter-turns for N = 4), and why analysis uses −j while synthesis uses +j.
  - **Final cheat sheet: built** (see above). New "put this on my cheat sheet" items go on `notes/Final_Cheat_Sheet.html`, and must be tagged **[FINAL SHEET: must include]** in the Q&A file. The Part 2 sheet and its Claude Doc are frozen.
- **Part 2 term test (done):** 12 Nov 2026, 16:00–17:00. Closed-book and on paper, with one double-sided A4 sheet of notes allowed. **Confirmed scope (2026-11-12): discrete time only.** That's the five discrete decks (`lecture-00` to `lecture(3)`: discrete signals, DFT, DTFT, Z, and LCCDEs with Z), which means T01–T03 plus T04 Q1–2. **Laplace and differential equations are NOT tested** (`lecture(4)`, `lecture(5)`, T04 Q3–4, T05). `Cheatsheet.docx` is the Part 1 sheet only. **The answer script provides a Z-transform table** (pairs pⁿu[n], −pⁿu[−n−1], ρⁿcos/sin(Ω₀n)u[n]; properties linear/delay/x[−n]/aⁿx/x∗h; unilateral and bilateral shift rules), so the cheat sheet leaves these out and keeps only the extra pairs.
- **Part 1 (continuous time):** done and understood. Tutorials 1–4 have worked solutions in `Tut/Part1/`.
- **Part 2 (discrete time):** working through `notes/Part2_Discrete_Time_Guide.md` one step at a time. Covered in the Q&A so far: Steps 1–9, which are sampling through the DTFS, leakage, circular convolution and the DTFT. I understand these conceptually but am still shaky. **The Z-transform and the ROC (Steps 11–13) don't make sense to me yet; that's next.** On 2026-11-11, Steps 5–13 were rewritten at a beginner level: Steps 5–10 from this Q&A, and Steps 11–13 from scratch using T03 as the worked examples.
- **Test-day plan (2026-11-12, now past):** the Z concept and FIR/IIR are now understood. Do the tutorial questions in this order, attempting each before checking it against the guide section or with Claude:
  **The question list, in tutorial order T01 → T02 → T03 → T04 Q1–2, is in `Tut/Part2/Question_Tracker.md`.** It has tick boxes, what each question tests, where to check it, and hidden final answers. Within T03 it goes easiest first, finishing with Q4. ⭐ marks the questions for when time is short. **Current position (2026-11-12 afternoon):** T01 is done. In T02, Q2(b)(c) and Q3(a)(b) have been explained, but **Q1(a)(d) and Q4 are still to do**. In T03, Q1(b) and Q2(a) (x₂ = n·u[n], including the left-sided −n·u[−n−1] variant) have been explained. **Next: T03 Q2 x₃, x₄**, then the rest of T03 in tracker order, then T04 Q1–2. I now give full worked answers, not hints.
  Cheat sheet (handwritten, double-sided A4): the content is in the Claude Doc "SC3102 Part 2 Cheat Sheet" (https://claude.ai/artifact/DhJn8mg5wuztEbXWaBpQTi). The print-ready sheet is `notes/Part2_Cheat_Sheet.pdf`: **A4 landscape**, 2 sides × 3 columns of panels, built from `notes/Part2_Cheat_Sheet.html`. It includes question-type recipe panels (R) and a partial-fractions panel (7b). There's also a blue handwriting-font copy, `notes/Part2_Cheat_Sheet_Handwritten.pdf`; rebuild it with `python notes/make_handwritten.py` after any edit to the main HTML (the fonts are in `notes/fonts/`). Print both landscape, double-sided, flipping on the long edge. Skip T02 Q3(c), T03 Q1(a)(c), T03 Q2(b), T03 Q3(d) and all of Laplace.
- **Labs 1–4:** done (`Lab1/` … `Lab4/`, each with a `_Answers.md`).

## What's where

| Path | Contents |
|---|---|
| `notes/Part2_Discrete_Time_Guide.md` | The 16-step study guide. Steps 1–14 are discrete time; Step 15 is Laplace and Step 16 is differential equations. It refers to `../Slides/`, which is local only: it's in `.gitignore`, so other devices won't have it |
| `notes/Transform_Pairs.pdf` | One table of CTFT, Laplace, Z and DTFT pairs with their ROCs (2 A4 pages). The `.html` source needs internet for KaTeX, so use the PDF |
| `notes/figs/` | Figures for the 2026-11-27 Q&A entries: overlapping convolution, the s-plane surface, the derivative rule, one rule with two h's, initial conditions, the three ways to split an output |
| `PYP/*.pdf`, `PYP/Solutions/` | The six past finals (23S1, 23S2, 24S1, 24S2, 25S1, 25S2), with worked solutions (every part: Exam answer + Explanation), figures (`figs/`, redrawn by `make_figures.py`; the 24S2 figures by `make_figures_24S2.py`) and `00_Exam_Guide.md` (question patterns, recipes, the paper hints that are wrong) |
| `notes/Final_Cheat_Sheet.pdf`, `notes/Final_Cheat_Sheet_Handwritten.pdf` | **The final-exam sheet** (whole course, 2 pages, print landscape, double-sided, flip on the long edge), built from `notes/Final_Cheat_Sheet.html` (plain HTML, works offline). Rebuild the PDF with headless Edge (see the standing rule below). Rebuild the handwritten copy from inside `notes/` with `python make_handwritten.py --src=Final_Cheat_Sheet.html --ink-digits "" 6.3 1.0`; it prints column bottoms, which must be ≤ about 570pt. Run with no arguments, the script still builds the Part 2 sheet |
| `Cheat Sheet - Signals and Systems Concepts.pdf` | Someone else's midterm sheet from Studocu, not mine. My Part 1 sheet is `Cheatsheet.docx` |
| `Slides/` (local, gitignored) | Part 2 lecture slides, numbered from 0. `sc3102-transform-lecture-00-…`=L0 discrete signals and systems, `lecture.pdf`=L1 DFT, `lecture(1)`=L2 DTFS/circular convolution/DTFT, `lecture(2)`=L3 Z-transform, `lecture(3)`=L4 LCCDEs with Z (its title says "Lecture 4"), `lecture(4)`=L5 Laplace, `lecture(5)`=L6 differential equations. `Introduction`, `Signals(1)`, `Systems`, `Transforms(1)` are Part 1 |
| `Tut/Part1/Tutorial{1..4}(…).pdf` | Part 1 question sheets, with short answer keys |
| `Tut/Part1/Tutorial{1..4}_Solutions.md` | Worked solutions that follow the official NTULearn method step by step, written in our own words |
| `Tut/Part1/Disagreements.md` | Errors in the official answers, plus the course method compared with how it's done in practice |
| `Tut/Part2/student*.pdf` | Part 2 questions. `student.pdf`=T01 discrete signals and systems, `(1)`=T02 DFT and DTFS, `(2)`=T03 Z-transform, `(3)`=T04 difference equations and Laplace, `(4)`=T05 differential equations |
| `Tut/Part2/teacher*.pdf` | Part 2 solution slides. `teacher.pdf`=T01, `(1)`=T02, `(2)`=T03, `(3)`=T04. **There are no T05 solutions yet** |

## Already explained in the Q&A (no need to repeat)

**Standing rule (2026-11-12; since 2026-11-28 the Part 2 sheet is frozen, so the cheat-sheet steps below apply to `notes/Final_Cheat_Sheet.html`, and only for items the user asks to put on it):** log every new concept question in `notes/Part2_QA_Concepts.md` and add a compact version to section 9 of the cheat sheet. Update both the HTML/PDF (keep it at exactly 2 pages) and the Claude Doc. Space is tight. Each side clips silently at about 575pt (`overflow:hidden`), so after any edit, re-render and check that every column's bottom is ≤ about 570pt (`make_handwritten.py` prints these for the handwritten copy). Only add maths that's a concept. The user doesn't want pure working on the sheet, and the given Z table must stay off it. Rebuild the PDF with headless Edge: `msedge --headless --no-pdf-header-footer --print-to-pdf=<out> file:///…/Part2_Cheat_Sheet.html`, then check that it has 2 pages. **Give `--print-to-pdf` an absolute path and a fresh `--user-data-dir`.** A relative path, or a profile still held by an earlier Edge process, silently writes nothing, so you end up checking the old PDF (this happened on 2026-11-24). Delete the old PDF first, or check that the new text is in it.

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
- **(2026-11-12) Give full worked answers to tutorial questions in one go,** all the steps through to the final answer. Don't stop with "your turn" and make me prompt for each step.
- **(2026-11-12) Don't pile up analogies.** A bell, an echo, interest and cooling all in one answer confused me badly. Build from what I already understand (e.g. "poles bound the ROC") and add one fact at a time, with numbers.
- **(2026-11-26/27) My maths is rusty, so never jump algebra or reasoning steps.**
  - **No bare claims:** show where each statement comes from, with a small worked example and real numbers.
  - **Write terms out in full** ("initial conditions", "region of convergence", …), and define any abbreviation on first use.
- **Don't mention the exam date or count down to it.**
- **Commit or push only when asked.** Leave `Tut/Part2/teacher(4).pdf` untracked.
- On NTULearn, the Part 1 solution PDFs can't be downloaded from the viewer. The question sheets have "Download Original File". When the button is disabled, the original file can still be fetched: the viewer loads a `/bbcswebdav/...` address, which redirects to a page whose address holds a signed link to the PDF. That's how 24S2 was copied, with permission.
- **This repo is public on GitHub.** Ask before pushing anything that shouldn't be public.
- **My level (2026-11-11):** still weak. Don't skip steps, and work every idea with real numbers. Steps 11–13 now cover all of T03: series expansion (13.5), the x[−n] and aⁿx[n] properties (13.1), the damped-cosine Z pair (13.2), and T03 Q1/Q2/Q4 worked through.
- **Guide gaps compared with the tutorials** (the guide doesn't cover these yet):
  - T04 Q1: partial fractions in z² with a cosine input, and setting initial conditions to cancel the transient
  - T04 Q2: H(z) with a delay x[n−k], for k=2 and k=−1
  - Laplace partial fractions with a quadratic factor (T04 Q3c). The damped cos/sin pairs are now in Step 15.3; Laplace ROCs and whether the CTFT exists (T04 Q4) are in Step 15.2 (added 2026-11-24)
