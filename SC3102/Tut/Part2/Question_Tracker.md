# Part 2 Test: Question Tracker

Test: 12 Nov 2026, 16:00–17:00. **Scope: T01–T03 and T04 Q1–2 only.** Laplace (T04 Q3–4) and T05 are not tested.

**How to use this:** work from top to bottom. Try each question **without looking**, then check it,
then tick the box. Final answers are hidden at the bottom of this file. Open one only after you've
tried the question.

**Files:** questions are in `student.pdf` (T01), `student(1).pdf` (T02), `student(2).pdf` (T03) and
`student(3).pdf` (T04). Official solutions are in `teacher.pdf`, `teacher(1).pdf`, `teacher(2).pdf` and
`teacher(3).pdf`. The guide is `../../notes/Part2_Discrete_Time_Guide.md`.

**Short on time?** Do only the ⭐ questions.

---

## T01: Discrete signals and systems (about 40 min)

- [ ] ⭐ **Q1(a)(c)**: fundamental periods, aperiodic signals, period of a sum. *Check:* official slides 5–11.
- [ ] **Q1(b)**: cos(3.5πn) compared with cos(3.5πt), i.e. aliasing. *Check:* official slides 8–9.
- [ ] **Q1(d)**: 2-min concept check. Can a periodic signal be absolutely summable?
- [ ] **Q2(c)(d)(e)**: aliasing. Which frequencies f give the same samples? *Check:* official slides 19–21.
- [ ] ⭐ **Q3(b)(c)**: test causal, stable, time-invariant and linear, and give a counterexample. *Check:* official slides 28–32.
- [ ] **Q4(c)(d)**: step response to impulse response, using h[n] = s[n] − s[n−1], then causality and stability. *Check:* official slides 41–43.

Skip: Q2(a)(b), Q3(a), Q4(a)(b) (quick; just read the official answer).

## T02: DFT, DTFS and DTFT (about 55 min)

- [ ] ⭐ **Q1(a)**: write out the 4-point analysis and synthesis matrices.
- [ ] ⭐ **Q1(d)**: use conjugate symmetry and one synthesis row to find A, B and v. *Check:* official slides 12–14.
- [ ] **Q1(b)(c)**: 2-min concept check. Rows 1 and 3, and what that means for X[1] and X[3].
- [ ] **Q2(a)(b)**: periods, and the DTFS via Euler (no sum needed). *Check:* cheat sheet section 3.
- [ ] **Q2(c)**: 2-min concept check. Does N = 12 recover a and b? *Check:* guide 7.2.
- [ ] ⭐ **Q4(a)–(d)**: linear vs circular convolution, the wrap rule and padding. *Check:* guide 8.5.
- [ ] **Q3(a)(b)**: when the DTFT exists, and the DTFT via the geometric series.

Skip: Q3(c) (long error-bound calculation, worked in guide 9.7).

## T03: Z-transform (about 75 min), easiest first

- [ ] **Q1(b)**: undo the fading (the bridge from the DTFT to Z). *Check:* guide 13.3.
- [ ] ⭐ **Q2(a)(c)** for x₂, x₃, x₄: X(z), ROC, and whether the DTFT exists. *Check:* guide 12.10.
- [ ] **Q1(d)**: 2-min concept check. Do 2ⁿ (for all n) and 2^|n| have an ROC? *Check:* guide 12.5.
- [ ] **Q3(c)**: series expansion, to find y[1], y[2], y[3]. *Check:* guide 13.5.
- [ ] **Q3(a)**: spot the cosine pair. *Check:* guide 13.2.
- [ ] **Q3(b)**: partial fractions with no z in the numerator. *Check:* guide 13.4, example B.
- [ ] ⭐ **Q4(a)–(e)**: pole-zero plot, 3 ROCs, invert for each one, causal vs two-sided. *Check:* guide 12.7–12.8, 13.4 example A.

Skip: Q1(a) (definition), Q1(c) and Q2(b) (covered by Q2 and Q4), Q3(d) (reading off tags).

## T04: Difference equations, Q1–2 only (about 60 min). Ask Claude to guide you; the guide doesn't cover these yet.

- [ ] ⭐ **Q2 with k = 2, (a)–(e)**: H(z) from the equation, the ROCs, causal and stable, and h[n].
- [ ] **Q2 with k = −1, (a) and (c) only**: what changes when there's an x[n+1]?
- [ ] **Q1(a)**: unilateral Z with initial conditions, zero-input and zero-state, and partial fractions in z². Warm up first with guide 14.3 if you need to.
- [ ] **Q1(b)(c)**: transient vs steady-state, and choosing initial conditions so there's no transient.

Skip: Q3, Q4 (Laplace, not tested).

---

## Final answers (open only after trying)

<details><summary>T01</summary>

- **Q1(a):** x₁: N₀ = 24 (π/12 ÷ 2π = 1/24). x₂: N₀ = 4 (3.5π ÷ 2π = 7/4, so 7 laps in 4 samples). x₃ = cos n is aperiodic (1/2π is irrational). x₄ = sin(πn) − cos n = −cos n, also aperiodic.
- **Q1(b):** the continuous period is 4/7 s, but the discrete period is 4 samples. That's aliasing: cos(3.5πn) = cos(−0.5πn) = cos(0.5πn).
- **Q1(c):** x₁ + x₂ has period LCM(24, 4) = 24. x₃ + x₄ = 0, which is periodic with period 1.
- **Q1(d):** no. Σ|x| adds the same nonzero block forever, so it goes to ∞.
- **Q2(c):** no. The samples are x[n] = cos(πfn/1000), so f = 100 Hz, 1900 Hz, 2100 Hz, … all give cos(0.1πn).
- **Q2(d):** f = 100 Hz, so x_c(t) = cos(200πt).
- **Q2(e):** no. f = 1900 Hz gives cos(1.9πn) = cos(2πn − 0.1πn) = cos(0.1πn), which is the same.
- **Q3(b):** causal ✓ (it uses only x[n] and x[n−1]), stable ✓ (|y| ≤ 2M + M²), time-invariant ✓.
- **Q3(c):** not linear. Take v = δ[n] + δ[n−1]. Then (Tv)[1] = 1 + 1 + 1 = 3, but (T(2v))[1] = 2 + 2 + 4 = 8 ≠ 6.
- **Q4(c):** h[n] = s[n] − s[n−1] = 3(δ[n−2] − δ[n−3]) + 3(δ[n−k] − δ[n−k−1]).
- **Q4(d):** causal ⇔ k ≥ 0. Always stable, because h is finite.

</details>

<details><summary>T02</summary>

- **Q1(a):** ω = e^(j2π/4) = j. Analysis rows: [1 1 1 1], [1 −j −1 j], [1 −1 1 −1], [1 j −1 −j]. Synthesis = ¼ × the same matrix with j and −j swapped.
- **Q1(b)(c):** rows 1 and 3 are complex conjugates of each other, so a real x gives X[3] = X[1]*.
- **Q1(d):** B = 3 − 3j. Then v[2] = 0 forces A = 2, and v = [3, −1, 0, 2].
- **Q2(a):** a: N₀ = 8. b: N₀ = 6.
- **Q2(b):** A[1] = A[7] = 4, everything else 0. B[1] = 3e^(−jπ/6), B[5] = 3e^(jπ/6), everything else 0.
- **Q2(c):** a: no, because 12 isn't a multiple of 8 (a[12] = −1 ≠ a[0] = 1). b: yes, because 12 is a multiple of 6.
- **Q3(a):** both DTFTs exist for |a| > 1.
- **Q3(b):** X(Ω) = 1/(1 − a⁻¹e^(−jΩ)) and Y(Ω) = X(Ω)², because y = x ∗ x.
- **Q4(a):** linear convolution = [−2, 1, 3, −6, 2, 8].
- **Q4(b):** circular convolution (N = 4) = [0, 9, 3, −6].
- **Q4(c):** C[n] = L[n] + L[n+4].
- **Q4(d):** pad to length ≥ 4 + 3 − 1 = 6: two zeros on x and three zeros on y.

</details>

<details><summary>T03</summary>

- **Q1(b):** w[n] = (j/2)ⁿu[n], so x[n] = 3ⁿw[n] = (3j/2)ⁿu[n].
- **Q1(d):** neither has an ROC. 2ⁿ needs |z| > 2 and |z| < 2. 2^|n| needs |z| > 2 and |z| < ½.
- **Q2:**
  - x₂ = n·u[n]: X = z/(z−1)², |z| > 1, no DTFT (the edge is at 1).
  - x₃: X = −z/(z+2), |z| < 2, DTFT ✓.
  - x₄: X = z/(z−½) + z/(z−3), ½ < |z| < 3, DTFT ✓.
  - (x₁: X = (z−1)(z−2)/z², z ≠ 0, DTFT ✓.)
- **Q3(a):** x[n] = (½)ⁿcos(πn/2)u[n], which is 1, 0, −¼, 0, 1/16, …
- **Q3(b):** poles 2 and 3. C = 1, D = 2. a[n] = (2ⁿ⁻¹ + 2·3ⁿ⁻¹)u[n−1], which is 0, 3, 8, 22, …
- **Q3(c):** y[1] = 2, y[2] = 1, y[3] = ½ (and y[0] = 2).
- **Q4(a):** zeros at 0 and −1. Poles at 2 and −4. The ROCs are |z| < 2, 2 < |z| < 4 and |z| > 4. F = z/(z−2) + z/(z+4).
- **Q4(b):**
  - r = 1: f = −(2ⁿ + (−4)ⁿ)u[−n−1]
  - r = 3: f = 2ⁿu[n] − (−4)ⁿu[−n−1]
  - r = 5: f = (2ⁿ + (−4)ⁿ)u[n]
- **Q4(c):** |z| > 4.
- **Q4(d):** 2 < |z| < 4.
- **Q4(e):** no, because there's a pole on |z| = 4.

</details>

<details><summary>T04 Q1–2</summary>

- **Q2(a):** H_k(z) = z^(2−k) / ((z + ½)(z − 3/2)). So H₂ = 1/((z+½)(z−3/2)) and H₋₁ = z³/((z+½)(z−3/2)).
- **Q2(b):** poles at −½ and 3/2. The ROCs are |z| < ½, ½ < |z| < 3/2 and |z| > 3/2.
- **Q2(c):** stable only for ½ < |z| < 3/2. Causal only for k = 2 with |z| > 3/2. For k = −1, the z³ on top means it's never causal.
- **Q2(d):** no. Causal needs |z| > 3/2, but the unit circle isn't in that ROC.
- **Q2(e):** G = z²/((z+½)(z−3/2)) = ¼·z/(z+½) + ¾·z/(z−3/2), so g[n] = [¼(−½)ⁿ + ¾(3/2)ⁿ]u[n]. Then h₂[n] = g[n−2], which is causal but unstable. For k = −1 there's no causal h.
- **Q1(a):**
  - y_zi = −(½)ⁿcos(πn/2)
  - y_zs = [4 − (½)ⁿ]cos(πn/2)
  - y = [4 − 2(½)ⁿ]cos(πn/2), for n ≥ 0
- **Q1(b):** the transient is −2(½)ⁿcos(πn/2). The steady state is 4cos(πn/2).
- **Q1(c):** yes, with y[−1] = 0 and y[−2] = −4 (just put y_ss = 4cos(πn/2) at n = −1 and n = −2).

</details>
