# SC3102 Part 2: Concepts from my Q&A

These are things I asked about while studying, each written as a short answer. Section 9 of the
cheat sheet (`Part2_Cheat_Sheet.pdf`) has a compressed version.

## Z-transform

**What X(z) is.** X(z) is the transform of the signal x, just like X(Ω). The letter in the brackets
tells you which transform it is. X(z) = Σ x[n]z⁻ⁿ with z = re^(jΩ), and it's the **DTFT of the faded
signal r⁻ⁿx[n]**. |z| = r is how hard you fade, and the angle of z is the frequency.
- Worked example: 2ⁿu[n] has no DTFT. Fade it with r = 4 and you get 0.5ⁿ, which does have one. Any r > 2 works, and that range is the ROC.
- The building blocks are spirals zⁿ = rⁿe^(jΩn), not steady walkers. A pole at p means the signal contains pⁿ.

**Where the DTFT sits inside X(z).** The DTFT is X(z) on the unit circle |z| = 1. The Ω axis from −π
to π wraps round to form that circle: Ω = 0 → z = 1, π/2 → j, ±π → −1. The real difference is that
the DTFT has **one dial** (Ω) and the Z-transform has **two dials** (r and Ω). It's not "a line
against a plane".

**Poles and zeros: how to find them, and signal or system?** They belong to a Z-transform
*fraction*, so a signal has them (through X(z)) and so does a system (through H(z) = Z{h} = Y/X).
It's the same recipe for both, but quizzes mostly ask about H(z).
- **Recipe:** (1) make it **one fraction** (common denominator); (2) clear z⁻¹ by multiplying top and bottom by zᵏ; (3) factor and **cancel** common factors; (4) zeros = roots of the top (H = 0), poles = roots of the bottom (H → ∞).
- **Lab 4 example:** z/(z−0.6) + z/(z−1.2) = [z(z−1.2) + z(z−0.6)]/(…) = 2z(z−0.9)/((z−0.6)(z−1.2)), so the zeros are 0 and 0.9 and the poles are 0.6 and 1.2. Check: H(0.9) = 0.9/0.3 + 0.9/(−0.3) = 3 − 3 = 0, while H(0.61) ≈ 60 and H(0.601) ≈ 600.
- **Why the zeros get forgotten:** each piece z/(z−p) shows its pole, and partial fractions only use the poles. The zero at 0.9 is hidden until you combine the pieces; it's where they cancel.
- **Traps:** 1/(1 − 0.5z⁻¹) = z/(z−0.5) has a zero at 0. (z−0.5)/((z−0.5)(z−0.8)) = 1/(z−0.8) has no pole at 0.5. 0.6ⁿu[n] + 1.2ⁿu[n] has zeros at 0 and 0.9, while 0.6ⁿu[n] − 1.2ⁿu[n] gives −0.6z/(…), whose only zero is at 0. So the poles say which pⁿ ingredients are present, and the zeros depend on how much of each.
- **From an LCCDE:** y[n] = 0.5y[n−1] + x[n] − 0.9x[n−1] gives H = (1 − 0.9z⁻¹)/(1 − 0.5z⁻¹) = (z−0.9)/(z−0.5). The x-terms make the zeros and the y-terms (feedback) make the poles, which is why every FIR pole is at 0.
- **Meaning:** a pole p means the signal or h contains pⁿ, and poles set the ROC, causality and stability. A zero means an input zⁿ at that z gives an output of 0, and zeros never affect the ROC or stability. The averager y = ½x[n] + ½x[n−1] has H = (z+1)/(2z), with a zero at −1 (Ω = π). Input (−1)ⁿ gives ½ − ½ = 0, while input 1, 1, 1 gives 1, so it's low-pass. A zero on the unit circle kills that frequency, a zero near it makes a dip, and a pole near it makes a peak. In the Lab 4 3D plot, the poles are spikes and the zeros touch the floor.

**What pⁿ, zeros and the ROC mean physically.**
- **pⁿ = start at 1 and multiply by p every step.** 0.5ⁿ = 1, 0.5, 0.25, 0.125 dies out. 1ⁿ = 1, 1, 1 stays (u[n]). 2ⁿ = 1, 2, 4, 8 blows up. (−0.5)ⁿ = 1, −0.5, 0.25 flips sign and dies. So |p| says dies/stays/grows, and the angle of p says how fast it wiggles (±0.9j → 0.9ⁿcos(πn/2) = 1, 0, −0.81, 0, 0.656). Everyday examples: 5% interest → 1.05ⁿ, and a cooling gap shrinking 10% a minute → 0.9ⁿ. The continuous-time twin is e^(−at): sampling e^(−t) every 0.693 s gives 0.5ⁿ.
- **Poles are the ROC edges *because* pole p ⇔ the signal contains pⁿ (one idea, not two).** For 0.5ⁿu[n], X(z) = 1 + (0.5/z) + (0.5/z)² + …. At z = 1 the ratio is 0.5 and the sum is 2. At z = 0.6 the sum is 6. At z = 0.5 the ratio is 1 and the sum is 1 + 1 + 1 + … → ∞ (the edge). At z = 0.25 the ratio is 2 and the sum blows up, even though the formula z/(z−0.5) still gives −1 (that's "outside the ROC", Lab 4 1D). So the edge is |z| = 0.5, the number the signal multiplies by each step.
- **"Feedback number" = the number in front of y[n−1].** y[n] = 0.5y[n−1] + x[n] → Y(1 − 0.5z⁻¹) = X → H = z/(z−0.5), so the pole is 0.5 (and kicking it with δ gives h = 1, 0.5, 0.25 = 0.5ⁿ). "Feedback" only means the old output is fed back in. This is where poles come from when a question gives an equation instead of a signal. (The bell/echo/interest/cooling analogies were just pictures of "h dies out or grows"; ignore them.)
- **A zero is an input the system blocks.** Feed in zⁿ at the zero and the output is 0. On |z| = 1 at Ω₀, the blocked pattern is a pure tone, which is how filters remove frequencies:
  - y = x[n] − x[n−1], zero at 1 (Ω = 0): 5, 5, 5 → 0, so it removes a constant offset.
  - y = ½x[n] + ½x[n−1], zero at −1 (Ω = π): 1, −1, 1 → 0, so it smooths (low-pass).
  - y = x[n] + x[n−2], zeros at ±j (Ω = π/2): cos(πn/2) = 1, 0, −1, 0, 1 → y[2..4] = 0. With fₛ = 200 Hz, that's 50 Hz mains hum removed (the same idea as removing the whistles in Lab 4 Q3).
  - For a *signal*, zeros have little physical meaning; they're just where the pieces cancel.
  - Poles + zeros + one gain number = all of H(z), so the pole-zero plot is the system's fingerprint. It's used to analyse a system (what it does by itself, what it blocks) and to design one (zeros on frequencies to kill, poles near frequencies to boost).
- **The ROC picks which physical system one formula describes.** z/(z−2) with |z| > 2 is 2ⁿu[n] = 1, 2, 4, 8 (starts at the kick, blows up: causal, unstable). With |z| < 2 it's −2ⁿu[−n−1]: h[−1], h[−2], h[−3] = −0.5, −0.25, −0.125 (all before the kick: stable, not causal). The ROC answers (1) **which way in time**: outside the outermost pole → causal → can run in real time; inside → needs the future → offline only (e.g. a recorded file), and (2) **does it blow up**: |z| = 1 in the ROC → stable, with a frequency response. The edge is the signal's growth rate: 2ⁿ faded by r = 4 gives 0.5ⁿ (fine), by r = 1.5 gives 1.33ⁿ (blows up). With a pole at 2, a system can't be causal and stable at once. T03 Q4 (poles 2, −4): only |z| < 2 contains the unit circle → the only stable ROC, and it's left-sided.

**"Converges" (ROC) is not the same as "stable".** The ROC is where Σ h[n]z⁻ⁿ adds up *with help from the
weight z⁻ⁿ*. Stable means Σ|h[n]| adds up *with no help*, which is the weight at |z| = 1 (where |z⁻ⁿ| = 1).
- **Lab 4 Region 0:** h[n] = −(0.6ⁿ + 1.2ⁿ)u[−n−1] = −2.5, −3.47, −5.21, …, −165.6 at n = −10 (−5.8×10⁷ at n = −35). It blows up going left.
- **At z = 0.3** the weight 0.3^|n| tames it: −0.75, −0.31, −0.14, …, −0.001. The sum is −1.33 = H(0.3) ✓, so 0.3 is in the ROC.
- **At z = 1** the weighted terms are just h[n], which goes to −∞. So 1 is not in the ROC, and the system is not stable.
- The growth only limits *where* the ROC is (small |z| < 0.6 beats the 1.67^|n| growth); it doesn't remove it. All three Lab 4 regions have an ROC, but only Region 1 (the one containing |z| = 1) is stable. This is the fading idea again: the ROC lists the fading amounts that work, and stable means no fading is needed.
- **Formula + ROC = exactly one signal.** "Stable" describes that signal or system, never the transform: a Z-transform only *exists* (has an ROC) or doesn't. An unstable signal can have a perfectly good Z-transform (2ⁿu[n] ↔ z/(z−2), |z| > 2); that's the Z-transform's advantage over the DTFT. The ROC still shows the instability (|z| = 1 is not in it). The DTFT is the transform that exists only for stable signals: it's X(z) on |z| = 1.

**"Does the Z-transform make an unstable signal stable, so I can then take its DTFT?" No.**
- On a circle r inside the ROC you get the DTFT of a *faded copy* r⁻ⁿx[n], which is a different signal. For 2ⁿu[n], r = 4 gives the DTFT of 0.5ⁿu[n].
- Plugging z = e^(jΩ) into the formula when |z| = 1 is *outside* the ROC still gives a number, but it's the DTFT of the *other* signal with that formula (z/(z−2) at Ω = 0 gives −1 = Σ of −2ⁿu[−n−1] = −0.5 − 0.25 − …), not of 2ⁿu[n]. It's the same trap as Lab 4 1D at z = 1.5.
- An unstable signal has no DTFT at all (1 + 2 + 4 + … = ∞). Physically, a sine fed into an unstable system makes the output blow up, so there is no frequency response. The fading is only on paper.
- **Correct version:** the Z-transform analyses any signal, even one that blows up. You get its frequencies only when it's stable, and then they're X(e^(jΩ)) (0.5ⁿu[n]: 1/(1 − 0.5e^(−jΩ)); at Ω = 0 that's 2 = 1 + 0.5 + 0.25 + …). For unstable systems the Z-transform is for algebra (poles, ROC, causal/stable, inversion, LCCDEs), not frequencies.

**What the Z-transform is for, and what "analyse" means.** It works on *all* systems; unstable ones are just
where it's the only tool. It doesn't make difference equations: the LCCDE comes first (the rule applied each
step), and the Z-transform **solves** it. "Analyse" means getting h[n], y[n] for an input, causal/stable, and
(if stable) the frequency response, as formulas for every n at once.
- **Stable:** y = 0.5y[n−1] + x with x = u[n]. By hand you get 1, 1.5, 1.75, 1.875, … (does it reach 2?). With Z: Y = z/(z−0.5) · z/(z−1) = −z/(z−0.5) + 2z/(z−1), so y = (2 − 0.5ⁿ)u[n], which goes to exactly 2.
- **Unstable:** y = 2y[n−1] + x with x = u[n]. By hand: 1, 3, 7, 15, … With Z: Y = 2z/(z−2) − z/(z−1), so y = (2ⁿ⁺¹ − 1)u[n], which shows exactly how it blows up. The DTFT can't do this (h = 2ⁿu[n] has no DTFT).
- The DTFT handles h/y formulas and the frequency response for stable systems only. The Z-transform also handles unstable systems, causal/stable checks, and initial conditions (unilateral).

## Systems

**FIR vs IIR.** Both names describe h[n], the response to a single kick δ.
- **FIR** has no feedback. For example, y = ½x[n] + ½x[n−1] gives h = [½, ½] and then stops. The coefficients are h, every pole is at 0, and it's always stable.
- **IIR** has feedback (y[n−k] on the right-hand side). For example, y = 0.5y[n−1] + x[n] gives h = 0.5ⁿ, which never ends. H = z/(z−0.5), and it's stable only if the pole is inside |z| = 1. Changing 0.5 to 2 makes it blow up.

**Analysing a signal or a system?** Both, with the same maths.
- Transform a signal and you get X: what frequencies it contains.
- Transform an impulse response h and you get H: what the system does to each frequency.
- They connect through Y = H·X.
- The same ROC rules answer different questions. For a signal: which way it runs, and whether the DTFT exists. For a system: whether it's causal and whether it's stable.
- **Two meanings of "analyse".** In the Fourier sense (DFT/DTFT), analysing a signal = which frequencies it contains, and analysing a system = its frequency response H(Ω) = DTFT of h. In the Z sense, it's the poles/zeros/ROC → h[n], causal?, stable?, y for any input; this works for every system. They meet on the unit circle: H(Ω) = H(z) at z = e^(jΩ), if |z| = 1 is in the ROC. Example: y = 0.5y[n−1] + x has H = z/(z−0.5), pole 0.5, causal and stable. H(Ω) = 1/(1 − 0.5e^(−jΩ)) gives H(0) = 2 (1, 1, 1 → 2, 2, 2; check 2 = 0.5·2 + 1) and H(π) = 0.67 ((−1)ⁿ → 0.67(−1)ⁿ), so it's low-pass. y = 2y[n−1] + x has no frequency response, but Z still gives pole 2, h = 2ⁿu[n], unstable. Quiz: "frequency response" → H(e^(jΩ)) (stable only); causal/stable/h/y → poles + ROC.

**Causality (T01 Q3b definition).** If two inputs are identical up to time N, a causal system gives
identical outputs up to N. In practice, check that **every x[·] index is ≤ n for every n**.
- Shifts are by whole numbers.
- The traps are x[2n] (at n = 1 it needs x[2]) and x[−n] (at n = −1 it needs x[1]).
- n·x[n] is still causal.

**Linearity (T01 Q3c).** The test is T(a·x₁ + b·x₂) = a·Tx₁ + b·Tx₂, where a and b scale the
**values**, not the time index (x[an] would be time scaling).
- **To disprove it,** one counterexample is enough. Choose an input that switches on the term you suspect. For x[n]·x[n−1], use v = δ[n] + δ[n−1]: (Tv)[1] = 3 but (T(2v))[1] = 8 ≠ 6.
- **To prove it,** you need the general algebra. With p, q, r, s = x₁[n], x₁[n−1], x₂[n], x₂[n−1], the result is T(w) = aTx₁ + bTx₂ + (a²−a)pq + (b²−b)rs + ab(ps + rq). The step that makes it work is adding and subtracting: a²pq = a·pq + (a²−a)pq.
- **Quick checks:** zero in should give zero out. Products, squares, |x| and adding a constant all break linearity. n·x[n] and cos(n)·x[n] are linear but time-varying.

**Convolution.** Write the input as kicks, x = Σ x[m]δ[n−m]. Each kick sends out its own copy
x[m]·h[n−m], and you add up the copies. This only works for LTI systems.
- Worked example: x = [2, 1] and h = [1, 2, 3] give y = [2, 5, 8, 3].
- Every transform turns convolution into multiplication: Y = H·X.
- It's also just an operation on two signals, e.g. y = x ∗ x in T02 Q3.

**Running sum (T01 Q4b).** With h = u, y[n] = Σ x[m] for m ≤ n, because u[n−m] switches off every
m > n.
- Feed in u and you get (n+1)u[n]: count the ones from 0 to n.
- A bounded input giving an unbounded output means it's not stable. This agrees with Σ|h| = ∞ and with the pole at z = 1, which is on the unit circle.

## Periods and sampling (T01 Q1)

**N and m in the official solution.** N is the period (a whole number of samples) and m is the number
of full 2π laps in those N samples. **Ω₀N = 2πm**, so look for the smallest m that makes N a whole
number.
- Continuous time always uses m = 1. Discrete time may need more laps: cos(3.5πn) has m = 7 and N = 4.

**f/fₛ rule.** Ω₀/2π = f/fₛ, which is cycles per sample. A sampled sinusoid is **periodic ⇔ f/fₛ is
rational**. Reduce the fraction to lowest terms: the bottom number is N₀ and the top number is the
number of cycles.

**Tₛ vs T₀ vs N₀ vs N.**
- Tₛ = 1/fₛ is a property of the sampler, in seconds.
- T₀ = 1/f is a property of the continuous wave, in seconds.
- N₀ is a property of the samples, as a whole number of samples.
- N is either a test period (in T01 Q1) or the DFT size (in DFT questions).
- They connect through N₀·Tₛ = m·T₀.

**Why x₃ + x₄ cancels.** sin(πn) = 0 for every whole number n, because each step turns half a lap and
the walker only ever lands at ±1, where the height is 0. That makes x₄ = −cos n, and x₃ + x₄ = 0. The
zero signal has period 1 (not "none": in discrete time the smallest positive whole number is 1). This
only happens because n is a whole number. In continuous time, sin(πt) isn't 0 at t = 0.5.

**When the period rule "fails".** The rule gives when the **walker** returns, but cos and sin each read
only one coordinate of it.
- For a single sinusoid, the true N₀ is only smaller when **every sample is 0** (sin(πn), sin(3πn), …): the rule says 2, but the actual period is 1.
- So **simplify first**: remove terms that are 0 at every whole n, and reduce aliases. Then apply the rule (and the LCM for sums).

**Negative Ω.** Drop the sign: the period is always positive. Adding or subtracting 2π (aliasing)
doesn't change N₀ either, because 3.5π, 1.5π, −0.5π and 0.5π all give a denominator of 4. For the
signal itself, cos(−θ) = cos θ, so the sign disappears, while sin(−θ) = −sin θ, so the sign moves to
the front.

**25S1 Q1: how to read x(t) = Σ f(t − 4n)·e^(−α|t−4n|), and why it's periodic although it "decays".**
- **n is only a counter** (n = …, −1, 0, 1, 2, …); t is time. The question never says what n means. Write the terms out (α = 1):
  - n = 0: f(t)·e^(−|t|). The gate f = u(t+1) − u(t−1) is on for −1 ≤ t < 1, so this is a pulse on [−1, 1) peaking at 0.
  - n = 1: f(t−4)·e^(−|t−4|), on for −1 ≤ t−4 < 1, i.e. [3, 5), peaking at 4.
  - n = −1: on [−5, −3), peaking at −4. So term n is the same pulse centred at 4n ("pulse number" is a nickname for the counter).
- **Shift rule:** g(t − c) is g moved right by c, because at t = c it gives g(0).
- **Evaluating at a time:** substitute that t into every term. x(4.5): only n = 1 has its gate on (f(0.5) = 1), giving e^(−0.5) = 0.607. x(2) = 0, because every gate is off (a gap). t = 4.5 was my test point, not part of the formula.
- **Why it's periodic:** the exponent is the distance from *each pulse's own centre*, |t − 4n|, not from t = 0, so the decay restarts at every pulse: x(0.5) = x(4.5) = x(8.5) = 0.607. "Decaying" means *within* each pulse (1 at the centre → e^(−1) = 0.368 at the edges). The misread version e^(−α|t|)·Σf(t − 4n) would shrink (peaks 1, 0.018, 0.0003) and wouldn't be periodic.
- **Template:** Σ p(t − nT) = copies of one shape p every T → periodic with period T (re-index m = n − 1). Then rule out a smaller period: x = 1 only at t = 4n, so T₀ = 4. 23S1 Q1 is the same with Σ g(t − 3n).
- **"So is the exponential periodic?" No.** e^(−|t|) is one bump, and one term f(t−4)e^(−|t−4|) is that bump once, at 4. Only the **whole sum** is periodic: a copy every 4 s, forever both ways. At any t at most one gate is on, so x(t) = e^(−distance to the nearest centre) within 1 of a centre, else 0, and that distance repeats every 4 s.
- **"Does any |t − xn| make it periodic?" No.** The shift test decides: put t + T in for t and check that term n just becomes another term of the same sum. Here f(t+4−4n)e^(−α|t+4−4n|) = term n−1 ✓. It fails when:
  - the shifts don't match: Σ f(t−4n)e^(−|t−2n|) (term n → gate n−1 but exponential n−2); values at t = 0, 4, 8 are 1, 0.135, 0.018;
  - the exponential isn't shifted: Σ f(t−4n)e^(−|t|); values 1, 0.018, 0.0003;
  - n doesn't run over all integers: Σ_{n≥0} has 1, 1, 1 at t = 0, 4, 8 but x(−4) = 0 ≠ x(0) = 1. A periodic signal has no start.
- **The rule:** Σ_{n=−∞}^{∞} p(t − nT) is periodic with period T when every t in the term appears as t − nT (the same nT everywhere) and the sum is finite at each t. Overlap is fine: without the gate, Σ e^(−α|t−4n|) has overlapping tails but is still periodic. Then check whether a smaller period exists.

**Follow-up: what if it were f(t − 4n) + e^(−α|t−4n|) (plus instead of times)? Still periodic, T₀ = 4.**
- **Shift test is unchanged.** Term n is still one shape q(t) = f(t) + e^(−α|t|) moved to 4n, so x(t + 4) = Σ q(t − 4(n−1)) = x(t). The test only relabels which term is which; it never asks whether the terms overlap.
- **What the plus changes:** the gate no longer cuts the exponential off, so every e^(−α|t−4n|) has tails out to ±∞ and every t gets a bit of every term. Split it: x(t) = (rectangular train, 1 on [4n−1, 4n+1)) + g(t), with g(t) = Σ e^(−α|t−4n|).
- **The sum must be finite.** For 0 ≤ t < 4, the centres at or left of t give one geometric series and those to the right give another: g(t) = [e^(−αt) + e^(−α(4−t))]/(1 − e^(−4α)) = cosh(α(t−2))/sinh(2α). That needs α > 0: with α = 0 every point gets 1 + 1 + 1 + … = ∞. The original product never needed this, because at most one gate is on at any t.
- **Numbers for α = 1** (checked by brute-force summing 401 terms):

  | t | 0 | 0.5 | 1⁻ → 1 | 2 | 3⁻ → 3 | 4 | 4.5 |
  |---|---|---|---|---|---|---|---|
  | g(t) | 1.037 | 0.649 | 0.426 | 0.276 | 0.426 | 1.037 | 0.649 |
  | x(t) | 2.037 | 1.649 | 1.426 → 0.426 | 0.276 | 0.426 → 1.426 | 2.037 | 1.649 |

  At t = 0: own pulse 1 + neighbours 2e^(−4) + 2e^(−8) + … = 1.037. At t = 2: the two nearest give 2e^(−2) = 0.271 and the rest add 0.005. No zero gaps any more; the curve between pulses is a sagging cosh with the ±1 gate steps on top.
- **Smallest period has to be re-argued.** The official step "x = 1 only at t = 4n" relied on no overlap. Use the peak instead: g is biggest at the centres (cosh(α(t−2)) is largest farthest from t = 2) and the gate is on there, so the maximum 1 + coth(2α) = 2.037 occurs only at t = 4n. A period T < 4 would need x(T) = x(0), so T₀ = 4.
- **Knock-on for 1(a)(iii):** power must be (1/4)∫ x² over one whole period of the full sum. The shortcut "one term's energy ÷ 4" only worked because no two terms were ever on at once.
- (If "plus" meant t + 4n instead: n runs over all integers, so n → −n gives back the same sum, i.e. the identical signal.)

**Sum of two sinusoids, e.g. x(t) = sin(πt) + cos(2πt): periodic? Yes, T₀ = 2 s.**
- **Each part's period:** T = 2π/ω. sin(πt) has T₁ = 2π/π = 2 and cos(2πt) has T₂ = 2π/2π = 1.
- **The sum repeats when both parts are back at their start at the same time.** That's the smallest time that is a whole number of each period: T₀ = LCM(2, 1) = 2. In frequency terms, ω₀ = GCD(π, 2π) = π, and the two parts are harmonics 1 and 2 of it.
- **Check:** x(t + 2) = sin(πt + 2π) + cos(2πt + 4π) = x(t) ✓. T = 1 is too small: x(0.5) = 1 + (−1) = 0 but x(1.5) = −1 + (−1) = −2, because sin flips sign after half its period.
- **When it fails:** the period ratio must be rational. sin(πt) + cos(2t) has T₁ = 2 and T₂ = π, ratio 2/π, which is irrational. No whole number of 2s ever equals a whole number of πs, so the two parts never line up again: **not periodic**, although each part is.
- **Link to the 25S1 "plus" case:** that's also a sum, but every term already shares period 4, so the LCM is just 4.
- **Discrete time adds one step:** each part must be periodic on its own first (Ω/2π rational), then N₀ = LCM(N₁, N₂).

**25S1 Q1(a)(iii) power, step by step, and "why is |e^(−t)|² = e^(−2|t|)?"**
- **It isn't |e^(−t)|.** There are two different sets of bars:
  - |t| was in the signal from the start: x(t) = Σ f(t−4n)·e^(−α|t−4n|), and the n = 0 term with α = 1 is e^(−|t|).
  - |x(t)|² is the power formula's bar, there for complex signals. x = e^(−|t|) is real and positive, so that bar does nothing: |x|² = x² = (e^(−|t|))² = e^(−2|t|), using (eᵃ)² = e^(2a). The intuition is right: |eᵃ| = eᵃ for any real a.
  - The |t| matters. e^(−t) at t = −1 is e¹ = 2.718, but the pulse there is e^(−|−1|) = e^(−1) = 0.368. The pulse is symmetric and peaks at 1.
- **The method is right:** P = (1/T₀)∫ |x|² over any one period. T₀ = 4, so pick [−2, 2). Only the n = 0 pulse is on there, and only on [−1, 1), so the integral is ∫ from −1 to 1 of e^(−2|t|) dt.
- **Getting rid of |t|** by splitting at 0: for t ≥ 0, |t| = t; for t < 0, |t| = −t.
  - ∫ from 0 to 1 of e^(−2t) dt = [−e^(−2t)/2] from 0 to 1 = (1 − e^(−2))/2 = 0.432.
  - ∫ from −1 to 0 of e^(2t) dt = [e^(2t)/2] from −1 to 0 = (1 − e^(−2))/2 = 0.432.
  - The halves are equal because e^(−2|t|) is even, which is why the solution writes 2∫ from 0 to 1. Total 1 − e^(−2) = 0.865.
- **P = 0.865/4 = (1 − e^(−2))/4 = 0.216.**
- **Are all power signals periodic? No.** A power signal has 0 < P < ∞, where P = lim over T → ∞ of (1/2T)∫ from −T to T of |x|² dt. A nonzero periodic signal is always one (each period adds the same energy, so the average settles), but the reverse fails:
  - u(t): (1/2T)·T → **P = ½**, never repeats.
  - sin(πt) + cos(2t) (irrational period ratio, not periodic): the cross term averages to 0, so **P = ½ + ½ = 1**.
  - Random noise is a power signal too.
  - For a signal that isn't periodic, use the limit; the "one period" shortcut only exists for periodic signals.
- **The three classes:** energy signal (E finite, so P = 0, e.g. one pulse e^(−|t|)), power signal (P finite and nonzero, E = ∞), or neither (e^t, t·u(t): P = ∞).

**Calculus refresher: differentiating and integrating exponentials (all numbers checked numerically).**
- **Derivative:** d/dt e^(at) = a·e^(at) (chain rule: the number in front of t comes down). d/dt e^(−2t) = −2e^(−2t).
- **Integral = the reverse, so divide by a:** ∫ e^(at) dt = e^(at)/a + C. ∫ e^(−2t) dt = e^(−2t)/(−2) = −½e^(−2t). Why: let u = −2t, so dt = −du/2. Always check by differentiating back: d/dt(−½e^(−2t)) = e^(−2t) ✓. The common slip is multiplying by −2 instead of dividing.
- **Definite: [F]ₐᵇ = F(b) − F(a), and e⁰ = 1.** ∫₀¹ e^(−2t) dt = (−½e^(−2)) − (−½) = ½(1 − e^(−2)) = 0.432.
- **To ∞:** e^(−2t) → 0, so ∫₀^∞ e^(−2t) dt = 0 − (−½) = ½. It only converges when the exponent's real part is negative, which is exactly where the Laplace ROC comes from: ∫₀^∞ e^(−2t)e^(−st) dt = 1/(s+2) needs Re s > −2.
- **Complex a works the same way.** ∫₀^∞ e^(−2t)e^(−jωt) dt = ∫ e^(−(2+jω)t) dt = 1/(2+jω), the CTFT of e^(−2t)u(t) (at ω = 1: 0.4 − 0.2j). Gate: ∫₋₁¹ e^(−jωt) dt = (e^(−jω) − e^(jω))/(−jω) = 2 sin ω/ω, using e^(jθ) − e^(−jθ) = 2j sin θ (at ω = π/2: 4/π = 1.273).
- **|t| in the exponent:** split at 0 (|t| = t for t ≥ 0, −t for t < 0); if the integrand is even, take 2∫ from 0.
- **t times an exponential → by parts**, ∫u dv = uv − ∫v du with u = t, dv = e^(−2t)dt: ∫ t e^(−2t) dt = −½t e^(−2t) − ¼e^(−2t) + C, and ∫₀^∞ t e^(−2t) dt = ¼ (matches L{t·u(t)} = 1/s² at s = 2).
- **Sinusoids:** d/dt sin(ωt) = ω cos(ωt), d/dt cos(ωt) = −ω sin(ωt); ∫ cos(ωt) dt = sin(ωt)/ω, ∫ sin(ωt) dt = −cos(ωt)/ω. Over a whole period, ∫ cos = ∫ sin = 0, and the average of sin² or cos² is ½ (so A cos(ω₀t) has P = A²/2).
- **Steps and impulses:** d/dt u(t) = δ(t), ∫ δ = u, sifting ∫ f(t)δ(t − t₀) dt = f(t₀). Product rule: d/dt[e^(−2t)u(t)] = −2e^(−2t)u(t) + δ(t) (e^(−2t)δ(t) = e⁰δ(t)); Laplace agrees: s/(s+2) = 1 − 2/(s+2).

**Is autocorrelation a signal convolved with itself? No: correlation slides without flipping.**
- **Convolution** (yes, flip and slide): y(t) = ∫ x(τ)h(t−τ) dτ. Flip h, slide it by t, multiply by x, take the area.
- **Autocorrelation** (slide, no flip): R_x(τ) = ∫ x(t)x(t−τ) dt for a real signal. Multiply x by a copy shifted by τ and take the area, i.e. how alike x is to itself shifted. As a convolution: R_x(τ) = x(τ) ∗ x(−τ), the convolution with the *pre-flipped* copy, so the two flips cancel.
- **x ∗ x (self-convolution) is a different thing.** The two agree only when x is even, which is why the gate gives the triangle 1 − |τ| either way (T01 Q5(b)).
- **Discrete x = [1, 2, 3]:** x ∗ x = [1, 4, 10, 12, 9] (lopsided); R = [3, 8, 14, 8, 3] (symmetric, peak 14 = energy 1 + 4 + 9).
- **Continuous x = e^(−t)u(t):** R(τ) = ½e^(−|τ|) (even, peak ½ = energy at τ = 0); x ∗ x = t·e^(−t)u(t) (0 at t = 0, peak 0.368 at t = 1).
  - **The integral, step by step (τ ≥ 0, using the x(t+τ) form; x(t−τ) gives the same because R is even):**
    1. Limits: x(t)x(t+τ) needs u(t) = 1 and u(t+τ) = 1, i.e. t ≥ 0 and t ≥ −τ; for τ ≥ 0 the binding one is t ≥ 0, so ∫₀^∞.
    2. Merge exponents (eᵃeᵇ = e^(a+b)): e^(−t)·e^(−(t+τ)) = e^(−2t−τ) = e^(−τ)·e^(−2t).
    3. τ is fixed while t is integrated, so e^(−τ) comes out: R = e^(−τ)∫₀^∞ e^(−2t) dt = e^(−τ)·½.
    4. τ < 0: the limit becomes t ≥ −τ, and e^(−τ)∫ from −τ to ∞ of e^(−2t) dt = e^(−τ)·½e^(2τ) = ½e^(τ). Together, R = ½e^(−|τ|); at τ = ±1, 0.184.
  - Why it's so clean: on t ≥ 0 the shifted copy is the original times e^(−τ), so the area is e^(−τ) × the energy ½.
- **Frequency side:** x ∗ x ↔ X², but R ↔ |X|² ≥ 0, because flipping a real signal conjugates its spectrum (x(−t) ↔ X*). That's why the Fourier transform of an autocorrelation (the ESD/PSD) can never be negative, which is the decisive test in 25S1 Q1(b). For e^(−t)u(t): |1/(1+jω)|² = 1/(1+ω²), the transform of ½e^(−|τ|) ✓.
- **Power signals:** R(τ) = (1/T₀)∫ over one period of x(t)x(t−τ) dt (or the limit for non-periodic), and R(0) = P. A cos(ω₀t) → (A²/2)cos(ω₀τ).
- **[FINAL SHEET: must include, user asked] The 4 properties of an autocorrelation R(τ)** (as in the 25S1 Q1(b) solution):
  1. **Even:** R(−τ) = R(τ) (conjugate symmetric, R(−τ) = R*(τ), for a complex signal).
  2. **Peak at the origin:** |R(τ)| ≤ R(0), and R(0) = the power (or the energy) ≥ 0.
  3. **Non-negative spectrum (Wiener–Khinchin):** S(f) = F{R(τ)} ≥ 0 for all f. The decisive test, because 1 and 2 follow from it.
  4. **Periodic part:** if x has a periodic part, R has a periodic part with the same period.
  - Put next to them: R(τ) = x(τ) ∗ x(−τ) ↔ |X|², i.e. slide without flipping, which is why property 3 holds.

**What is the PSD?** Power spectral density: how a power signal's average power is spread over frequency, in power per Hz.
- **[FINAL SHEET: must include, user asked] The PSD formulas in this entry:** Wiener–Khinchin S = F{R}; P = ∫S df = R(0); band power (both ±f sides, 2∫ from f₁ to f₂ for real x); S ≥ 0; ESD = |X|² with E = ∫|X|² df; periodic → spikes at harmonics (cos of amplitude A → A²/4 at ±f₀); S_y = |H|²S_x; white noise N₀/2 ↔ (N₀/2)δ(τ).
- **Formula (Wiener–Khinchin):** S_x(f) = F{R_x(τ)}, so R_x(τ) = F⁻¹{S_x(f)}.
- **Area = power:** P = ∫ S_x(f) df over all f = R_x(0). Power in a band: ∫ over that band, counting both +f and −f (for a real signal, 2∫ from f₁ to f₂).
- **Always ≥ 0** (it's power per Hz; also R ↔ |X|²). So "is this a valid autocorrelation?" = take its transform and check ≥ 0.
- **Energy-signal twin: ESD = |X(f)|²,** with E = ∫|X(f)|² df (Parseval). PSD is for power signals (E = ∞).
- **Periodic signal → spikes at the harmonics.** x = √3 + 2cos(2πf₀t + θ) (23S2): R = 3 + 2cos(2πf₀τ), S = 3δ(f) + δ(f − f₀) + δ(f + f₀). Area 3 + 1 + 1 = 5 = DC power 3 + cosine power 2²/2 ✓. The phase θ disappears.
- **Smooth example:** R = e^(−|τ|) → S = 2/(1 + (2πf)²). Total area 1 = R(0) ✓. Power in |f| < 1/2π (|ω| < 1): (1/π)∫₋₁¹ dω/(1+ω²) = (1/π)(π/2) = ½, so half the power sits below 0.159 Hz.
- **Through an LTI filter:** S_y(f) = |H(f)|²·S_x(f). The phase of H doesn't matter.
- **White noise:** flat S = N₀/2 at every f ↔ R = (N₀/2)δ(τ), uncorrelated with any shifted copy of itself.

**Why P = ∫S df = R(0), power in a band, and S_y = |H|²S_x.**
- **R(0) = P by definition:** R(τ) is the time-average of x(t)·x(t−τ). At τ = 0 there's no shift, so it's the time-average of x², which is the power formula.
- **∫S df = R(0) from the inverse transform:** R(τ) = ∫S(f)e^(j2πfτ) df. At τ = 0, e⁰ = 1, so R(0) = ∫S(f) df. A general Fourier fact: the value at 0 in one domain = the area in the other.
- **Checks:** e^(−|τ|): R(0) = 1 = area of 2/(1+(2πf)²). 23S2: R(0) = 3 + 2 = 5 = spikes 3 + 1 + 1 = DC 3 + cosine 2²/2.
- **Band power = density × width, i.e. the area over the band.** A real signal's spectrum is mirrored at −f, so the band "f₁ to f₂ Hz" means [f₁, f₂] **and** [−f₂, −f₁]: 2∫ from f₁ to f₂ of S df. Forgetting the mirror gives half. Example: 2cos(2πf₀t) has spikes of 1 at ±f₀; a band around f₀ holds 1 + 1 = 2 = all its power.
  - For e^(−|τ|), power with |ω| < W is (2/π)·arctan W: W = 1 → 0.5, W = 2 → 0.705, so the band 1 ≤ |ω| ≤ 2 holds 0.205.
- **Through an LTI filter, S_y = |H(f)|²·S_x(f):** each frequency's amplitude is scaled by |H(f)| and its phase shifted by ∠H. Power goes with amplitude², and a phase shift doesn't change power. (Proof: R_y = h(τ) ∗ h(−τ) ∗ R_x ↔ H·H*·S_x.)
  - Example: x = √3 + 2cos(2πf₀t) through H(0) = 1, |H(f₀)| = 0.5 → S_y = 3δ(f) + 0.25[δ(f − f₀) + δ(f + f₀)] → P_y = 3.5. Directly: y = √3 + 1·cos(…), P = 3 + ½ = 3.5 ✓.
  - An ideal band-pass filter has |H|² = 1 in the band and 0 outside, so its output power **is** the band power. That's what "power in a band" means physically.

**Is energy/power the same formula in time and frequency? Yes, in shape (Parseval): square the magnitude, add it all up.**

| | Time side | Frequency side |
|---|---|---|
| Energy signal | E = ∫\|x(t)\|² dt | E = ∫\|X(f)\|² df (ESD = \|X\|²) |
| Periodic power signal | P = (1/T₀)∫ over one period of \|x\|² dt | P = Σ\|c_k\|² (PSD = spikes \|c_k\|² at kf₀) |
| Any power signal | P = lim (1/2T)∫ from −T to T of \|x\|² dt | P = ∫S(f) df, S = F{R} |

- **Three catches:**
  1. With ω instead of f: E = (1/2π)∫|X(ω)|² dω.
  2. The power rows have no 1/T on the frequency side; the averaging is already inside c_k and S.
  3. For a power signal, don't square X(f): it is made of deltas (or doesn't exist), and |δ|² means nothing. Use Σ|c_k|² or S = F{R}.
- **Why they agree:** the Fourier transform writes x as a sum of orthogonal sinusoids, and the energy of orthogonal pieces just adds (T01 Q4: E_{x+y} = E_x + E_y when ∫xy = 0). Like Pythagoras.
- **Energy check, x = e^(−t)u(t):** time ∫₀^∞ e^(−2t) dt = ½. Frequency: X = 1/(1 + j2πf), |X|² = 1/(1 + (2πf)²), ∫ df = (1/2π)∫ dω/(1+ω²) = π/2π = ½ ✓. Also |X|² = F{R} = F{½e^(−|τ|)} ✓.
- **Power check, x = √3 + 2cos(2πf₀t):** time (1/T₀)∫(√3 + 2cos)² = 3 + 4·½ + 0 (cross term) = 5. Frequency: c₀ = √3, c_±1 = 1 (2cos = e^(j…) + e^(−j…)), Σ|c_k|² = 3 + 1 + 1 = 5 ✓.
- **25S1 pulse train:** c_k = ½∫₀¹ e^(−t)cos(πkt/2) dt (c₀ = 0.316, c₁ = 0.228), and Σ|c_k|² = 0.2162, the same as the time-side (1 − e^(−2))/4. **Method: pick whichever side is easier**; here time is one line, frequency is an infinite sum.

**How to Fourier-transform a continuous signal (worked: x = e^(−t)u(t)).**
- **Definition:** X(f) = ∫ from −∞ to ∞ of x(t)·e^(−j2πft) dt (ω form: X(ω) = ∫x(t)e^(−jωt) dt, with ω = 2πf). Multiply by a probe spinning at −f and take the area. Inverse: x(t) = ∫X(f)e^(j2πft) df.
- **Steps:**
  1. u(t) sets the limits to 0…∞: ∫₀^∞ e^(−t)e^(−j2πft) dt.
  2. Merge the exponents: e^(−(1 + j2πf)t), so a = −(1 + j2πf).
  3. Divide by a: [e^(−(1+j2πf)t) / (−(1 + j2πf))] from 0 to ∞.
  4. At ∞: |e^(−(1+j2πf)t)| = e^(−t)·|e^(−j2πft)| = e^(−t)·1 → 0 (the spinning part has size 1, and e^(−t) kills it). At 0: e⁰ = 1.
  5. 0 − 1/(−(1 + j2πf)) = **1/(1 + j2πf)**.
- **Reading it:** one complex number per f. f = 0 → X = 1 = ∫x dt (the area). f = 1/2π = 0.159 Hz (ω = 1) → 1/(1 + j) = 0.5 − 0.5j, |X| = 0.707, phase −45°. Large f → X → 0.
- **|X|²:** |a + jb|² = a² + b², so |1 + j2πf|² = 1 + (2πf)² and |X|² = 1/(1 + (2πf)²).
- **∫|X|² df:** substitute ω = 2πf, df = dω/2π, and use ∫dω/(1+ω²) = arctan ω: (1/2π)[arctan ω] from −∞ to ∞ = (1/2π)(π/2 + π/2) = ½ ✓ (= the time-side energy).
- **In the exam, use the table:** e^(−at)u(t) ↔ 1/(a + j2πf) = 1/(a + jω), for a > 0. It's also Laplace with s = jω: 1/(s + 1) → 1/(jω + 1).
- **[FINAL SHEET: must include, user asked] The CTFT table pairs** (f form; for ω put 2πf → ω). Cross-check against the course formula sheet and the Part 1 sheet when building; sinc(x) = sin(πx)/(πx).

  | x(t) | X(f) |
  |---|---|
  | δ(t) | 1 |
  | 1 | δ(f) |
  | e^(j2πf₀t) | δ(f − f₀) |
  | cos(2πf₀t) | ½[δ(f − f₀) + δ(f + f₀)] |
  | sin(2πf₀t) | (1/2j)[δ(f − f₀) − δ(f + f₀)] |
  | e^(−at)u(t), a > 0 | 1/(a + j2πf) |
  | t·e^(−at)u(t), a > 0 | 1/(a + j2πf)² |
  | e^(−a\|t\|), a > 0 | 2a/(a² + (2πf)²) |
  | u(t) | 1/(j2πf) + ½δ(f) |
  | Π(t/T) (1 on \|t\| < T/2) | T·sinc(fT) |
  | sinc(Wt) | (1/W)·Π(f/W) |
  | Λ(t/T) (triangle, base 2T) | T·sinc²(fT) |

  With the key properties: shift x(t − t₀) ↔ e^(−j2πft₀)X(f); modulation e^(j2πf₀t)x(t) ↔ X(f − f₀); scaling x(at) ↔ (1/|a|)X(f/a); duality X(t) ↔ x(−f); convolution ↔ product; Parseval ∫|x|² dt = ∫|X|² df.

**Why |a + jb|² = a² + b² (complex magnitude, no steps skipped).**
- **Picture:** a + jb is the point a across, b up. |a + jb| is the arrow's length from 0. The arrow, the a-side and the b-side form a right triangle, so Pythagoras gives |a + jb|² = a² + b². E.g. |3 + 4j|² = 9 + 16 = 25, so |3 + 4j| = 5.
- **Algebra:** |z|² = z·z*, where the conjugate z* = a − jb flips the sign of the j part. Expand term by term: (a + jb)(a − jb) = a·a + a·(−jb) + (jb)·a + (jb)(−jb) = a² − jab + jab − j²b². The middle two cancel, giving a² − j²b². Since j² = −1, that's a² − (−1)b² = a² + b².
- **Trap:** |z|² ≠ z². (3 + 4j)² = 9 + 24j + 16j² = 9 + 24j − 16 = −7 + 24j, a complex number and not a length.
- **Our case:** 1 + j2πf has a = 1, b = 2πf, so |1 + j2πf|² = 1² + (2πf)². At f = 1/2π: |1 + j|² = 1 + 1 = 2.
- **For a fraction:** sizes divide, |p/q| = |p|/|q|, so |1/(1 + j2πf)|² = 1²/|1 + j2πf|² = 1/(1 + (2πf)²). Check at f = 1/2π: 1/(1 + j) = (1 − j)/((1 + j)(1 − j)) = (1 − j)/2 = 0.5 − 0.5j (multiply top and bottom by the conjugate), and |0.5 − 0.5j|² = 0.25 + 0.25 = 0.5 = 1/2 ✓.
- **Angle:** the arrow's direction, tan θ = b/a. 1 + j has a = b, so 45°. Dividing by it turns the other way, so 1/(1 + j) is at −45°.

**Fourier transform vs ESD vs PSD: what each one tells you.**

| | X(f), the Fourier transform | ESD = \|X(f)\|² | PSD = S(f) |
|---|---|---|---|
| For | energy signals (periodic ones only via deltas) | energy signals | power signals (periodic, noise) |
| Values | complex: magnitude **and phase** | real, ≥ 0 | real, ≥ 0 |
| Answers | which frequencies, how big, and how they line up in time | how much energy per Hz | how much average power per Hz |
| Area | (not a size) | total energy E | total power P |
| Rebuild x(t) from it? | yes, exactly (inverse FT) | no, the phase is gone | no |
| Link to R | | F{R} (energy version) | F{R} (power version) |

- **Squaring throws away the phase,** because |e^(−jθ)| = 1. So different signals can share one ESD/PSD:
  - **Delay:** e^(−t)u(t) and e^(−(t−3))u(t−3) have X₂ = X₁·e^(−j2πf·3) but the same |X|² = 1/(1 + (2πf)²).
  - **Reversal:** e^(t)u(−t) has X = 1/(1 − j2πf), again with the same |X|².
  - **Phase shift:** cos(2πf₀t) ↔ ½[δ(f − f₀) + δ(f + f₀)] and sin(2πf₀t) ↔ (1/2j)[δ(f − f₀) − δ(f + f₀)] have different transforms, but both have PSD ¼[δ(f − f₀) + δ(f + f₀)] (|1/2j|² = ¼) and power ½.
- **Why PSD exists at all:** a power signal never dies out, so ∫|x|² = ∞ and its FT is deltas or doesn't exist. For random noise, every recording has a different random X(f), but its power per Hz is stable. The PSD is what a spectrum analyser shows.
- **Which to use in a question:**
  - The actual output signal y(t), a sketch of a spectrum, modulation → the FT (Y = H·X needs the phase).
  - Energy or power in a band, filter output power (S_y = |H|²S_x), bandwidth, a valid autocorrelation, noise → ESD/PSD.

**"FS for periodic, FT for finite energy, Laplace for everything else"? Close, but the three overlap rather than nest.**
- **FS:** periodic signals → coefficients c_k at the harmonics kf₀.
- **FT:** in the ordinary sense, signals with ∫|x| dt < ∞ (or finite energy). **With deltas allowed it also covers periodic signals and u(t), 1, cos**: a periodic x ↔ Σ c_k δ(f − kf₀), so the FS is a special case of the FT.
- **Laplace:** multiplies by e^(−σt) first, so it also handles signals that **grow** (e^(2t)u(t) ↔ 1/(s − 2), ROC Re s > 2), as long as **one** σ tames both sides. It fails when no σ works:
  - eternal cos(ω₀t) or 1 (the right side needs σ > 0, the left needs σ < 0 → empty ROC), although the FT with deltas works;
  - e^(|t|) (needs σ > 1 and σ < −1);
  - e^(t²) (grows faster than any exponential).
  The course mostly uses the unilateral version (t ≥ 0), where cos(ω₀t)u(t) ↔ s/(s² + ω₀²) is fine.
- **Link:** FT = Laplace on the jω-axis (s = j2πf).
  - ROC contains the axis → the FT is the plain substitution: e^(−2t)u(t): 1/(s + 2) → 1/(2 + j2πf).
  - Pole on the axis → the FT needs deltas: u(t): 1/s, FT = 1/(j2πf) + ½δ(f).
  - Axis outside the ROC → no FT: e^(2t)u(t).
- **Each tool's real job:** FS/FT describe what frequencies a signal contains; Laplace is mainly for systems: ODEs with initial conditions, transients and stability.
- **Discrete twin:** DTFS (periodic) / DTFT (Σ|x| < ∞, or deltas) / Z (growing, via r⁻ⁿ); the DFT is the finite-length computing version.

| Signal | FS | FT | Laplace (bilateral) |
|---|---|---|---|
| cos(ω₀t), all t | ✓ c_±1 = ½ | ✓ ½[δ(f − f₀) + δ(f + f₀)] | ✗ empty ROC |
| e^(−2t)u(t) | ✗ not periodic | ✓ 1/(2 + j2πf) | ✓ 1/(s + 2), Re s > −2 |
| u(t) | ✗ | ✓ only with δ | ✓ 1/s, Re s > 0 |
| e^(2t)u(t) | ✗ | ✗ | ✓ 1/(s − 2), Re s > 2 |
| e^(\|t\|) | ✗ | ✗ | ✗ |

**FS vs FT vs Laplace: formulas (forward + inverse) and differences.** (Exam "CTFT vs Laplace" discuss template: `PYP/Solutions/00_Exam_Guide.md` §4.)
- **[FINAL SHEET: must include, user asked] This whole entry:** the comparison table (forward, inverse, ω forms), the FS ↔ FT and FT ↔ Laplace links, the cosine form 2|c_k|, the properties side by side, and the partial-fraction inverse method.

| | Fourier series | Fourier transform | Laplace transform |
|---|---|---|---|
| Forward | c_k = (1/T₀)∫ over one period of x(t)e^(−j2πkf₀t) dt | X(f) = ∫ from −∞ to ∞ of x(t)e^(−j2πft) dt | X(s) = ∫ from −∞ to ∞ of x(t)e^(−st) dt (unilateral: from 0⁻) |
| Inverse | x(t) = Σ over all k of c_k e^(j2πkf₀t) | x(t) = ∫ from −∞ to ∞ of X(f)e^(j2πft) df | x(t) = (1/2πj)∫ along Re s = σ in the ROC of X(s)e^(st) ds; in practice partial fractions + table |
| ω form | f₀ → ω₀ = 2π/T₀, same 1/T₀ | X(ω) = ∫x e^(−jωt) dt; inverse has 1/2π | s = σ + jω already |
| Input | periodic x | ∫\|x\| < ∞ (or deltas for periodic, u, cos) | anything one e^(−σt) can tame |
| Output | a list of numbers c_k (discrete freqs kf₀) | a function of real f (continuous) | a function of complex s (a plane) + ROC |
| Probe | e^(−j2πkf₀t), harmonics only | e^(−j2πft), every f | e^(−st) = e^(−σt)e^(−jωt): spin and fade |
| Parseval | P = Σ\|c_k\|² | E = ∫\|X\|² df | not used |

- **Pattern:** forward = multiply by the probe with a **minus** sign, then integrate. Inverse = rebuild from **plus**-sign exponentials. The FS averages over one period (1/T₀) and rebuilds with a sum; the others integrate over all time.
- **Real x, cosine form:** x(t) = c₀ + Σ over k ≥ 1 of 2|c_k|cos(2πkf₀t + ∠c_k): the k-th cosine has amplitude 2|c_k|.
- **FS ↔ FT:** c_k = (1/T₀)·P(kf₀), where P is the FT of one period. 25S1: P(f) = ∫₋₁¹ e^(−|t|)e^(−j2πft) dt, T₀ = 4 → c₀ = 0.316, c₁ = 0.228. A periodic x ↔ X(f) = Σ c_k δ(f − kf₀).
- **FT ↔ Laplace:** X(σ + jω) = the FT of x(t)e^(−σt); the FT is X(s) at s = j2πf when the jω-axis is in the ROC.
- **Same signals through all three:**
  - cos(2πf₀t): FS c_±1 = ½ (others 0); FT ½[δ(f − f₀) + δ(f + f₀)]; Laplace (unilateral, cos·u) s/(s² + ω₀²), Re s > 0.
  - e^(−t)u(t): FS none (not periodic); FT 1/(1 + j2πf); Laplace 1/(s + 1), Re s > −1, and s = j2πf gives the FT.
- **Properties side by side:**
  - Derivative: c_k → j2πkf₀·c_k; X → j2πf·X; X → sX (unilateral: sX − x(0⁻)).
  - Delay t₀: c_k·e^(−j2πkf₀t₀); X·e^(−j2πft₀); X·e^(−st₀).
  - LTI output: d_k = H(kf₀)·c_k (each harmonic scaled); Y = H·X; Y = H·X (ROC ⊇ the overlap).
- **Inverting in practice:** FS just sum the terms; FT use the table and properties; Laplace use partial fractions, then the table, choosing each term's side by the ROC. E.g. 1/((s+1)(s+2)): A = 1/(s+2) at s = −1 → 1; B = 1/(s+1) at s = −2 → −1; so 1/(s+1) − 1/(s+2) → (e^(−t) − e^(−2t))u(t) for ROC Re s > −1.

**Why the Euler method and the FS integral give the same c_k (proof), and when to use which.**
- **Key fact (orthogonality):** (1/T₀)∫ over one period of e^(j2πnf₀t) dt = 1 if n = 0, else 0.
  - n = 0: e⁰ = 1, so (1/T₀)·T₀ = 1.
  - n ≠ 0 (a whole number): [e^(j2πnf₀t)/(j2πnf₀)] from 0 to T₀ = (e^(j2πn) − 1)/(j2πnf₀), using f₀T₀ = 1. Then e^(j2πn) = cos 2πn + j sin 2πn = 1 + 0, so the result is (1 − 1)/(…) = 0. A whole number of turns of the spinning arrow averages to 0.
- **Proof:** suppose algebra (Euler) gives x(t) = Σ_m a_m e^(j2πmf₀t). Put that into the integral: c_k = (1/T₀)∫ Σ_m a_m e^(j2πmf₀t)e^(−j2πkf₀t) dt = Σ_m a_m·(1/T₀)∫ e^(j2π(m−k)f₀t) dt. The key fact with n = m − k makes every term 0 except m = k, which gives 1. So c_k = a_k. The integral picks out exactly the weight Euler reads off, which is also why the c_k are unique.
- **Worked check, −4sin(2πt), T₀ = 1, k = 1:**
  - Euler: −4·(e^(j2πt) − e^(−j2πt))/(2j) → the weight on e^(j2πt) is −4/(2j) = −2/j = −2·(−j) = 2j (1/j = −j because j·(−j) = −j² = 1).
  - Integral: (−2/j)∫₀¹(e^(j2πt) − e^(−j2πt))e^(−j2πt) dt = (−2/j)∫₀¹(1 − e^(−j4πt)) dt = (−2/j)(1 − 0) = 2j ✓ (numerically 2j). Note 2j = 2∠+π/2, the phase the shown answer flipped.
- **When to use which:**
  - **Euler / identities:** x is a finite sum or product of sin, cos, e^(j…) (the "spectra" questions). Always faster.
  - **Integral (or the shortcut c_k = (1/T₀)·P(kf₀), with P the FT of one period from the table):** x is defined by its shape over one period (pulse trains, square or triangle waves, sawtooth, |sin|, the 25S1 e^(−|t|) train). It has infinitely many harmonics, so there's nothing to read off.
  - Example: a rectangular pulse train of height 1, width 1, T₀ = 4. P(f) = sinc(f) → c_k = ¼·sinc(k/4): c₀ = 0.25 (the average), c₁ = 0.225, c₂ = 0.159, c₄ = 0 (checked against the integral).

**FS coefficients: one worked example per signal type (all checked numerically).**
- **A. Finite sum, x = 2 + 6cos(4πt + π/3) − 4sin(6πt):**
  1. Frequencies 0, 2, 3 Hz → f₀ = 1 Hz, T₀ = 1 s, k = 0, 2, 3.
  2. sin → cos and absorb the minus: −4sin(6πt) = −4cos(6πt − π/2) = 4cos(6πt + π/2) (check t = 1/12: −4 both ways).
  3. A cos(2πkf₀t + φ) → c_k = (A/2)e^(jφ), c₋ₖ = (A/2)e^(−jφ); a constant → c₀.
  4. c₀ = 2; c_±2 = 3∠±π/3 = 1.5 ± 2.598j; c_±3 = 2∠±π/2 = ±2j.
  5. Parseval check: 4 + 2(9) + 2(4) = 30 = 2² + 6²/2 + 4²/2.
- **B. Product, x = 4cos(2πt)cos(6πt):** turn it into a sum first, then do A.
  - Identity cos A cos B = ½[cos(A−B) + cos(A+B)] → 2cos(4πt) + 2cos(8πt).
  - Or multiply the Euler forms: 4·½(e^(jA) + e^(−jA))·½(e^(jB) + e^(−jB)) = e^(j(A+B)) + e^(j(A−B)) + e^(−j(A−B)) + e^(−j(A+B)). This needs no identity.
  - 2 and 4 Hz → f₀ = 2 Hz, T₀ = 0.5 s: c_±1 = 1, c_±2 = 1.
  - Also: sin²(2πt) = ½ − ½cos(4πt) → c₀ = ½, c_±1 = −¼ (size ¼, phase π).
  - Identities: sin A cos B = ½[sin(A+B) + sin(A−B)]; cos A cos B = ½[cos(A−B) + cos(A+B)]; sin A sin B = ½[cos(A−B) − cos(A+B)]; cos²A = ½(1 + cos 2A); sin²A = ½(1 − cos 2A).
- **C. Shape over one period:** x = 2 for |t| < ½, 0 for ½ < |t| < 1, T₀ = 2 (f₀ = ½).
  - Integral: c_k = (1/2)∫ from −½ to ½ of 2e^(−jπkt) dt.
    - k = 0 separately: ∫ from −½ to ½ of 1 dt = 1 (= the average).
    - k ≠ 0: [e^(−jπkt)/(−jπk)] from −½ to ½ = (e^(−jπk/2) − e^(jπk/2))/(−jπk) = (−2j sin(πk/2))/(−jπk) = 2sin(πk/2)/(πk).
  - Table shortcut: one period = 2Π(t) ↔ 2sinc(f), so c_k = (1/T₀)P(kf₀) = ½·2sinc(k/2) = sinc(k/2), the same.
  - Values: c₁ = 0.637, c₂ = 0, c₃ = −0.212 (phase π), c₄ = 0, c₅ = 0.127. So x = 1 + 1.273cos(πt) − 0.424cos(3πt) + 0.255cos(5πt) − …, which sums to 2 at t = 0.
  - Tips: pick a symmetric window for even shapes; do k = 0 separately (the formula gives 0/0); integrate piece by piece where the shape changes. If one period isn't in the table (25S1 e^(−|t|) on [−1, 1)), integrate.

**Does the FT have infinitely many k too? It has no k at all: X(f) is defined at every real f from −∞ to ∞, a continuum rather than a list.**
- **FT = the FS with the period stretched to ∞.** Pulse of width 1:
  - T₀ = 4: lines every f₀ = ¼, c_k = ¼·sinc(k/4).
  - T₀ = 8: lines every ⅛, c_k = ⅛·sinc(k/8).
  - The line at f = 0.25 is c₁ = 0.225 (T₀ = 4) or c₂ = 0.1125 (T₀ = 8); times T₀, both give 0.900 = sinc(0.25).
  - So T₀·c_k = P(kf₀) always sits on the curve sinc(f). As T₀ → ∞ the lines get infinitely dense and merge into X(f) = sinc(f).
- **So X(f) is a density (per Hz):** the sum Σ c_k e^(j2πkf₀t) becomes the integral ∫X(f)e^(j2πft) df, and "amount at one harmonic" becomes "amount in a thin band", X(f)df. This is why ESD/PSD are "per Hz".
- **Does it reach f = ±∞?** For signals with jumps, yes (sinc decays slowly, like 1/f). **Band-limited** signals have X(f) = 0 beyond some f (sinc(Wt) ↔ (1/W)Π(f/W), zero for |f| > W/2), the FT version of "finitely many nonzero c_k".
- **Frequency variable in each transform:**
  - FS: k, every integer, discrete and unbounded.
  - FT: f, every real number, continuous and unbounded.
  - DTFS and DFT: k = 0…N−1, discrete and finite.
  - DTFT: Ω continuous but only over 2π (periodic).
  - Laplace and Z: s and z, the whole complex plane (with an ROC).

**25S1 Q2(a) method: known step response → new input, using L + TI only.**
- **Read the boxes:** AΠ((t − c)/w) has height A, centre c, width w, so it's on from c − w/2 to c + w/2. 3Π((t−6)/4) → 3 on [4, 8]; Π((t−3)/2) → 1 on [2, 4].
- **Box = difference of two steps:** A on [a, b] = A·u(t − a) − A·u(t − b) (check: before a 0 − 0, inside A − 0, after A − A). So x = 3u(t−4) − 3u(t−8).
- **Name each property as you use it:** TI: u(t − 4) → y_u(t − 4); homogeneity: ×3 → ×3; additivity: the difference → the difference. So y = 3y_u(t−4) − 3y_u(t−8).
- **Shift = replace every t by (t − t₀), inside the brackets:** y_u(t − 4) = 2δ(t − 5) + Π(((t−4) − 3)/2) = 2δ(t − 5) + Π((t − 7)/2), the box on [6, 8]. Not Π((t−3)/2 − 4).
- **Answer:** 6δ(t − 5) + 3Π((t−7)/2) − 6δ(t − 9) − 3Π((t−11)/2): an arrow of area 6 at 5, +3 on [6, 8], an arrow of area −6 at 9, −3 on [10, 12].

**Which transform properties the five past papers tested** (from the solution files).
- **[FINAL SHEET: must include, user asked] This whole list:** each property's formula with the paper references, the time-shift traps, and the system-property tests.
- **CT Fourier:**
  - Linearity: everywhere (split terms, add the PSDs).
  - Time shift: 25S1 2(c)(i), named in the question; δ(t − t₀) ↔ e^(−j2πft₀).
  - Convolution ↔ product: 24S1 2(b)(i) (state the steps and why it's easier), 24S1 2(b)(ii), 25S2 2(b)(ii) (state + verify), 25S1 2(c).
  - Product ↔ convolution: 23S1 2(c)(i).
  - Modulation / frequency shift: 23S2 2(c) RF pulse; 23S1 1(b) product spectra.
  - Duality (sinc ↔ rect): 24S1 2(b)(ii).
  - ∗δ = shift (sifting): 23S2 2(b)(i), 24S1 1(c), 25S1 2(b).
  - Parseval / power from lines: 23S1 1(b). Wiener–Khinchin: 23S2 1(c), 25S1 1(b).
  - Conjugate symmetry: 24S1 1(a)(ii) trap (a complex signal has no mirror line).
  - Frequency response (sinusoid scaled by |H|, shifted by ∠H): 23S1 2(b), 23S1 3(b), 24S1 3(b).
- **Laplace:**
  - Linearity + ROC intersection: 25S1 3(a).
  - s-shift e^(−at)f(t) ↔ F(s + a) (the damped cos/sin pairs): 25S1 3(a).
  - Derivative with ICs (sY − y(0⁻), s²Y − sy(0⁻) − y′(0⁻)): 23S1 3(a), 25S1 3(c), 25S2 4(b).
  - IVT: 23S1 3(b). FVT + pole check: 25S2 4(b)(ii).
  - CTFT link: 23S2 3(c), 24S1 3(a).
  - **Time-shift traps:** cos(3t + π/4)u(t) (24S1 3(c)) and e^(j(t+3))u(t) (25S1 3(b)) are not delays, because u(t) isn't shifted; expand instead.
- **Z / DFT:**
  - Delay z^(−n₀): 23S1 4(b), and every LCCDE → H(z).
  - Steady state via H(e^(jΩ)): 25S1 4(a), 25S2 3(c).
  - Circular vs linear convolution + zero padding: 23S2 4(a).
  - DFT conjugate symmetry X[N − k] = X[k]* (IDFT shortcut / check): 24S1 4(c), 25S1 4(b).
- **System properties** (linearity, time invariance, causality tests): 23S1 1(c), 23S2 2(a), 24S1 2(a), 25S2 2(a); using L + TI to get an output: 25S1 2(a).

**Time-shifting property: x(t − t₀) ↔ X(f)·e^(−j2πft₀).**
- **Proof (substitution):** F{x(t − t₀)} = ∫x(t − t₀)e^(−j2πft) dt. Let u = t − t₀, so t = u + t₀ and dt = du (limits unchanged). Then ∫x(u)e^(−j2πf(u + t₀)) du = ∫x(u)e^(−j2πfu)·e^(−j2πft₀) du (eᵃ⁺ᵇ = eᵃeᵇ) = e^(−j2πft₀)·∫x(u)e^(−j2πfu) du = e^(−j2πft₀)X(f).
- **Magnitude unchanged** (|e^(−jθ)| = 1): a delay doesn't change how much of each frequency there is, so the same |X| and the same ESD.
- **Phase gets −2πft₀ added,** a straight line in f. A delay of t₀ is f·t₀ cycles of a wave at f: cos(2πf(t − t₀)) = cos(2πft − 2πft₀). With t₀ = 2: f = 0.125 Hz (period 8) → ¼ cycle → −π/2; f = 0.25 (period 4) → ½ cycle → −π; f = 0.5 (period 2) → 1 cycle → −2π ≡ 0.
- **25S1 Q2(c):** e^(−t)u(t) ↔ 1/(1 + j2πf), so x(t − 2) ↔ e^(−j2πf·2)/(1 + j2πf) = e^(−j4πf)/(1 + j2πf). At f = 0.25: |X| = 0.537 both ways; phase −57.5° → −57.5° − 180° = −237.5° ≡ 122.5° (checked numerically).
- **Signs:** delay (t − t₀, moves right) → minus; advance x(t + 3) → e^(+j2πf·3). δ(t − t₀) ↔ e^(−j2πft₀) is the same rule with X = 1.
- **Same rule everywhere:** Laplace e^(−st₀)X(s); Z z^(−n₀)X(z) (the "z⁻¹ = one step later" tag); DTFT e^(−jΩn₀)X(e^(jΩ)).

**25S1 Q2(b): where is the flip? It is a real convolution, but impulses make the flip invisible.**
- **Not multiplication:** x(t)·δ(t − t₀) = x(t₀)δ(t − t₀), one impulse (sampling). x(t) ∗ δ(t − t₀) = x(t − t₀), the whole signal moved (shifting). E.g. triangle·δ(t − 1) = 1·δ(t − 1), but triangle ∗ δ(t − 1) = the triangle on [1, 3].
- **Why ∗δ is a shift:** ∫x(τ)δ(t − τ − t₀) dτ. The δ is nonzero only where t − τ − t₀ = 0, i.e. τ = t − t₀, so sifting picks x(t − t₀).
- **Either one can be flipped.**
  - Flip h: h(t − τ) has impulses at τ = t − 2, t − 5, t − 9 (reversed order).
  - Flip x: y = ∫h(τ)x(t − τ) dτ; the flipped triangle sits on (t − 2, t] and slides right, and each impulse inside adds weight × value. t = 2.5 → x(0.5) = 0.5; t = 3 → 1; t = 4.5 → 0; t = 6 → −1; t = 10 → 1.
- **Why the output isn't flipped:** the flip in τ is undone by the sliding. The right end of the flipped x (its start, x(0)) reaches each impulse first, so the copy comes out in the original order. Check with a ramp x = t on [0, 2): ramp ∗ δ(t − 2) = a rising ramp on [2, 4). The triangle is also symmetric, so a flip would look the same anyway.
- **Exam:** the question says "illustrate each step", so write the integral, split h (distributive), sift each impulse, then give the piecewise y and the sketch. Optionally draw the window at 2–3 values of t.

**What "flipping" means in convolution: a mirror about the vertical axis (time reversal), x(τ) → x(−τ).**
- Positions mirror and values stay: what was at τ = +a is now at τ = −a. Ramp x = τ on [0, 2): x(−τ) lives on (−2, 0] with x(−0.5) = x(0.5) = 0.5 and x(−1.5) = 1.5, rising to the left.
- **Not** a mirror about the horizontal axis: that's −x(t), an upside-down copy (like the −δ(t − 5) echo in 25S1 Q2(b)).
- **x(t − τ) = flip first, then slide right by t:** x(t − τ) = x(−(τ − t)). With t = 3 the ramp sits on (1, 3]: τ = 3 → x(0) = 0, τ = 2 → x(1) = 1, τ = 1.5 → x(1.5) = 1.5. The other order (shift, then flip) gives x(−τ − t), which is wrong.
- **Flipping the impulses (25S1 Q2(b), flip h):** yes, they really go to the left. h(−τ) has spikes at −2 (+), −5 (−), −9 (+), mirrored order. Then h(t − τ) has them at t − 2, t − 5, t − 9, a spike train marching right over the fixed triangle on [0, 2).
  - t = 0: −9, −5, −2 → none on the triangle, y = 0.
  - t = 3: −6, −2, 1 → the + at 1, y = x(1) = 1.
  - t = 6: −3, 1, 4 → the − at 1, y = −1.
  - t = 10: 1, 5, 8 → the + at 1, y = 1.
  - **Variant h = δ(t−2) + δ(t−5) − δ(t−9)** (the − spike last, to see the order): flipped, the − spike is at −9, the back of the train, so it arrives last. t = 0: spikes at −9(−), −5(+), −2(+); t = 3: the + from 2 is on the triangle → 1; t = 6: the + from 5 → 1; t = 10: the − from 9 → −1. So y = x(t−2) + x(t−5) − x(t−9): +, +, − copies at 2, 5, 9, the same order as h.
  - **Why the answer isn't mirrored:** the flip puts h's *earliest* spike (from 2) at the front (rightmost) of the marching train, so it reaches the triangle first (at t = 2), then the one from 5 (t = 5), then 9. Each spike scans x left to right, reading x(0), x(0.5), x(1), … in order. Flip + slide right = original order. "Looks the same" was about the final output, not the intermediate picture.
- **Why convolution flips:** y(t) = ∫x(τ)h(t − τ) dτ, and t − τ is how long ago input τ went in. h(t − τ) weights each past input by its age. E.g. h = e^(−t)u(t) at t = 5: input at τ = 5 → h(0) = 1, τ = 4 → h(1) = 0.368, τ = 3 → h(2) = 0.135. Later inputs get the start of h, so h is read backwards along τ, which is the flip. Discrete: y[n] = Σ x[k]h[n − k].

**Across the five past papers: definition integral/sum, or table/Euler?** (Checked against all five solution files.)
- **CT Fourier transform: table + properties almost always.**
  - Convolution theorem: 23S1 2(c)(i), 24S1 2(b)(ii), 25S2 2(b)(ii). Modulation: 23S2 2(c). Y = H·X: 25S1 2(c), 23S1 2(b). PSD checks: 23S2 1(c), 25S1 1(b).
  - The definition integral was asked **once**: 23S1 2(c)(ii), "verify with X(f) = ∫x e^(−j2πft) dt" (5 marks). After Euler it's just ∫ from −2 to 2 of e^(−j2πνt) dt = 4sinc(4ν).
  - "Discuss" questions (23S2 3(c), 24S1 3(a)) ask you to *write* the FT/Laplace definitions, not evaluate them.
- **CT Fourier series: Euler every time** (23S1 1(b), 24S1 1(a)(ii), 25S2 1(b)). No paper asked for the c_k integral. Keep the shape method as a backup.
- **Laplace: table + properties + partial fractions every time** (23S1 Q3, 23S2 Q3, 24S1 Q3, 25S1 Q3, 25S2 Q4(b)).
- **Integration you still need is not a transform:** convolution integrals (23S1 2(a), 23S2 2(b)(ii), 25S2 2(b)(i)) and energy/power integrals (23S2 1(b)(ii), 24S1 1(b), 25S1 1(a)(iii), 25S2 1(a)(ii)). These are ∫ of exponentials and polynomials.
- **Discrete:**
  - **DFT/IDFT: the definition sum, in every paper** (23S2 4(b), 24S1 4(c), 25S1 4(b), 25S2 3(a)). There's no table, but N = 4 makes it easy: e^(±j2πkn/4) = (±j)^(kn). 23S1 4(a): the DTFS analysis matrix for N = 5 (the definition in matrix form).
  - DTFS: Euler/inspection (25S2 3(b)).
  - DTFT: only as H(e^(jΩ)) = H(z) at z = e^(jΩ) for steady state, never the definition sum.
  - Z: table + partial fractions + LCCDE in every Q4 (23S1 4(b), 23S2 4(c), 24S1 4(b), 25S1 4(a), 25S2 4(a)).
- **The exam gives no formula sheet** (only occasional hints, like the 3 pairs in 25S1 Q1(b)), so "use the table" means the table on your own cheat sheet.
- **For a "from first principles" part, two derivations cover almost everything:** the gate ∫ from −T/2 to T/2 of e^(−j2πft) dt = T·sinc(fT), and ∫₀^∞ e^(−(a+j2πf)t) dt = 1/(a + j2πf).
- **[FINAL SHEET: must include, user asked] 4-point DFT by hand:**
  - X[k] = Σ from n=0 to 3 of x[n]·(−j)^(kn); x[n] = ¼Σ from k=0 to 3 of X[k]·j^(kn).
  - Powers: j⁰ = 1, j¹ = j, j² = −1, j³ = −j, repeating every 4 (use kn mod 4).
  - Checks: X[0] = Σx[n]; x[0] = ¼ΣX[k]; X[2] = x[0] − x[1] + x[2] − x[3].
  - Real x shortcut (X[3] = X[1]*): x[n] = ¼[X[0] + X[2](−1)ⁿ + 2Re{X[1]·jⁿ}]. 24S1 4(c): X = [12, 8+4j, 0, 8−4j] → n = 1: (8+4j)j = −4 + 8j, Re = −4 → ¼(12 − 8) = 1; all of x = [7, 1, −1, 5].
- **[FINAL SHEET: must include, user asked] The two first-principles CTFT derivations:**
  1. **Gate:** ∫ from −T/2 to T/2 of e^(−j2πft) dt = [e^(−j2πft)/(−j2πf)] from −T/2 to T/2 = (e^(−jπfT) − e^(jπfT))/(−j2πf) = (−2j·sin(πfT))/(−j2πf) = sin(πfT)/(πf) = T·sinc(fT).
  2. **One-sided exponential:** ∫₀^∞ e^(−at)e^(−j2πft) dt = ∫₀^∞ e^(−(a+j2πf)t) dt = [e^(−(a+j2πf)t)/(−(a+j2πf))] from 0 to ∞ = 0 − 1/(−(a + j2πf)) = 1/(a + j2πf) (a > 0, so the ∞ end → 0).
  - Combine with Euler (cos → two exponentials, giving shifted versions) and splitting at 0 (e^(−a|t|) → 1/(a + j2πf) + 1/(a − j2πf) = 2a/(a² + (2πf)²)).

**"Discrete time always has c_k because of sampling"? Half right: sampling makes the frequency *range* finite (it repeats), but *having* c_k (lines) comes from the signal being periodic.**
- **Two independent switches** (each one does something to the other domain):
  - sampled in time ↔ periodic in frequency (repeats every 2π in Ω, i.e. every fₛ in Hz);
  - periodic in time ↔ discrete in frequency (lines, c_k).

  | | Not periodic | Periodic |
  |---|---|---|
  | Continuous time | FT: continuous f, unbounded | FS: lines c_k, unbounded k |
  | Discrete time | DTFT: continuous Ω, repeats every 2π (**no c_k**) | DTFS: lines, repeating → only N distinct |

- **Non-periodic DT has no c_k:** (½)ⁿu[n] → DTFT 1/(1 − ½e^(−jΩ)), a continuous curve. Ω = 0 → 2, Ω = π → 1/(1 + ½) = 0.667, Ω = 2π → 2 again (repeat).
- **Periodic DT has a finite list:** cos(πn/2), N = 4 = ½e^(jπn/2) + ½e^(−jπn/2), and −1 ≡ 3 (mod 4), so a = [0, ½, 0, ½] (course X[k] = N·a_k = [0, 2, 0, 2]).
- **The DFT always has X[k] because it *treats* the N samples as one period** (periodic extension: the source of circular convolution). X[k] = the DTFT of those N samples, sampled at Ω = 2πk/N.
- **What fₛ sets:** the map Ω = 2πf/fₛ, so only −fₛ/2 ≤ f < fₛ/2 is distinct. fₛ = 100 Hz: 70 Hz → Ω = 1.4π ≡ −0.6π → looks like 30 Hz (aliasing).
- **One-line rule:** sampling in one domain ↔ periodic repetition in the other.

**What c₀ means, and what the other c_k are.**
- **c₀ = the DC component = the average over one period.** Put k = 0 in the formula: e⁰ = 1, so c₀ = (1/T₀)∫ over one period of x dt. It's the "0th harmonic", at f = 0.
  - Examples: pulse train of height 1, width 1, T₀ = 4 → c₀ = 0.25 (height × duty cycle); the 25S1 train → 0.316; 2 + 6cos(…) − 4sin(…) → 2; sin²(2πt) → ½ (which is exactly why a sinusoid's power is A²/2); a pure sinusoid or a ±1 square wave → 0 (zero mean).
- **Power splits as DC + AC:** P = c₀² + Σ over k ≠ 0 of |c_k|² (e.g. 30 = 4 + 26).
- A DC-blocking capacitor (H(0) = 0) removes exactly c₀ and leaves a zero-mean signal.
- **Same idea in every transform:** c₀ = average, X(0) = area (FT), X[0] = sum of the samples (DFT, = N × mean), DTFS a₀ = mean.
- **c_k for k ≠ 0:** the pair c_k and c₋ₖ together is the k-th harmonic at k·f₀ (a multiple of the fundamental *frequency* f₀ = 1/T₀). For a real x they combine into one real cosine 2|c_k|cos(2πkf₀t + ∠c_k). The negative k aren't extra physical frequencies; they're the mirror partners, since c₋ₖ = c_k*.

**Non-periodic signals like e^(−|t|) and (½)^t u(t): no Fourier series. Use the FT (and Laplace).** ("Finite sum" in the FS examples meant *a finite number of sin/cos terms added*, not finite energy.)
- **First classify:**
  - periodic → FS;
  - not periodic with ∫|x| < ∞ → FT, by table or definition integral, plus Laplace with the jω-axis in the ROC;
  - grows → Laplace only.
  Both signals here have finite area, so the FT exists and the spectrum is continuous (every f, no lines).
- **x = e^(−|t|) (two-sided, even):**
  - Table: e^(−a|t|) ↔ 2a/(a² + (2πf)²), a = 1 → X(f) = 2/(1 + (2πf)²). Integral: split at 0 → 1/(1 + j2πf) + 1/(1 − j2πf) = 2/(1 + (2πf)²).
  - Real and even, so the phase is 0 everywhere. Values: X(0) = 2 (= area), X at ω = 1 is 1, at ω = 2 it's 0.4.
  - Bilateral Laplace: right half 1/(s + 1) (Re s > −1); left half e^t u(−t) ↔ ∫ from −∞ to 0 of e^((1−s)t) dt = 1/(1 − s) (Re s < 1). Sum = 2/(1 − s²), ROC −1 < Re s < 1, a **strip** because the signal is two-sided. It contains the jω-axis, so s = jω gives 2/(1 + ω²) ✓.
- **x = (½)^t u(t) (one-sided):**
  - Key step, rewrite as e^(−at): b^t = e^(t·ln b) (because e^(ln b) = b), so (½)^t = e^(t·ln ½) = e^(−t·ln 2), a = ln 2 = 0.693. Check t = 1: e^(−0.693) = 0.5 ✓.
  - Table: e^(−at)u(t) ↔ 1/(a + j2πf) → X(f) = 1/(0.693 + j2πf). Integral: ∫₀^∞ e^(−(ln 2 + j2πf)t) dt gives the same.
  - Complex (one-sided, not even), so there's a phase. |X| = 1/√(0.693² + (2πf)²), ∠X = −arctan(2πf/0.693). X(0) = 1/ln 2 = 1.443 (= area). At f = 0.110 Hz (2πf = 0.693): |X| = 1.020, phase −45°.
  - Laplace: 1/(s + ln 2), ROC Re s > −0.693 (contains the axis).
- **Repeated every T₀ → back to an FS:** c_k = (1/T₀)·P(kf₀), with P the FT of the repeated pulse.
- **Discrete twin (½)ⁿu[n] (Part 2):** Z = 1/(1 − ½z⁻¹) = z/(z − ½), |z| > ½; DTFT 1/(1 − ½e^(−jΩ)); at Ω = 0 that's 2 = Σ(½)ⁿ.

**Where does k stop in a continuous-time FS? It doesn't: k runs over all integers, −∞ to ∞.**
- **Discrete time stops at N − 1 because of aliasing:** n is a whole number, so e^(j2π(k+N)n/N) = e^(j2πkn/N)·e^(j2πn) = e^(j2πkn/N). Harmonic k + N is the same sequence as k, so only N are distinct.
- **Continuous time has no aliasing:** t takes every value in between, so every k is a different function. E.g. f₀ = ¼: k = 1 and k = 5 agree at t = 1 (both j) but not at t = 0.5 (e^(jπ/4) vs e^(j5π/4), opposite directions).
- **Finite sums of sinusoids** (types A/B) have only finitely many nonzero c_k; the rest are 0. **Shapes with jumps or corners** (type C) have infinitely many nonzero c_k, shrinking like 1/k (jumps) or 1/k² (corners, e.g. a triangle wave).
- **Example, a pulse train of width 1, T₀ = 4:** c_k = ¼·sinc(k/4).
  - c₀…c₁₂ = 0.25, 0.225, 0.159, 0.075, 0, −0.045, −0.053, −0.032, 0, 0.025, 0.032, 0.021, 0. Every 4th is 0 (sinc of a whole number) because the duty cycle is 1/4.
  - (My earlier list skipped c₃ = 0.075.)
  - The power captured by |k| ≤ K, out of P = 0.25: K = 1 → 65.5%, 2 → 85.8%, 3 → 90.3%, 8 → 95.0%, 20 → 98.0%, 100 → 99.6%. It never reaches 100% with a finite K.
- **In the exam:** the answer is the general formula for all k ("k = 0, ±1, ±2, …"). For a sketch, draw the envelope P(f)/T₀ = ¼sinc(f) dashed, then lines at f = k/4 up to the first zero or two, then "…". The spectrum is even in k for a real even signal (c₋ₖ = c_k).

**What are harmonics?** Whole-number multiples of the fundamental frequency, k·f₀, where f₀ = 1/T₀.
- k = 1 is the fundamental (1st harmonic), k = 2 the 2nd harmonic, …; k = 0 is DC (the average).
- **Why a periodic signal can only contain harmonics:** a sinusoid at k·f₀ does exactly k cycles in T₀, so it's back at its start after T₀. A component at 1.5f₀ would do 1.5 cycles and wouldn't line up, so the sum couldn't repeat every T₀. That's why the FS has only c_k at kf₀ (a line spectrum) while the FT of a non-periodic signal is continuous.
- **Finding f₀:** the GCD of the frequencies present (equivalently T₀ = LCM of the periods). The image example (1, 2, 4 Hz) has f₀ = 1 Hz: 1st, 2nd and 4th harmonics, and the 3rd is absent (c₃ = 0). sin(πt) + cos(2πt) (0.5 and 1 Hz): f₀ = 0.5 Hz, 1st and 2nd.
- **f₀ need not be present:** cos(4πt) + cos(6πt) (2 and 3 Hz) has f₀ = 1 Hz, T₀ = 1 s, and contains only the 2nd and 3rd harmonics.
- **Square wave ±1:** (4/π)[sin(2πf₀t) + ⅓sin(2π·3f₀t) + ⅕sin(2π·5f₀t) + …], odd harmonics only, amplitudes 1.273, 0.424, 0.255.
- **Discrete time:** harmonics are Ω_k = 2πk/N, and only N of them are distinct (k = 0…N−1), because k and k + N alias.

**"Double-sided amplitude and phase spectra" questions: is that a transform? Yes, it's the Fourier series (exponential c_k), found by Euler instead of the integral.**
- Example (a past-paper style Q2, 10 marks): x(t) = 10cos(4πt + π/8) + 8sin(3πt)cos(5πt), i.e. Tutorial 2 Q1(a) + Q1(b) combined.
- Frequencies 2, 4 and 1 Hz → f₀ = GCD = 1 Hz, T₀ = 1 s, harmonics k = 1, 2, 4. The double-sided spectrum plots |c_k| and ∠c_k at f = kf₀ for ±k; it's also the weights of the FT's spikes, X(f) = Σ c_k δ(f − kf₀). Single-sided = cosine amplitude 2|c_k| at f ≥ 0.
- **Why Euler is allowed:** the c_k are unique, so writing x as a sum of e^(j2πkf₀t) terms reads them off. The analysis integral gives the same (checked numerically).
- **Recipe:**
  1. Products → sums: sin A cos B = ½[sin(A+B) + sin(A−B)].
  2. sin → cos: sin θ = cos(θ − π/2).
  3. Make every amplitude positive: −cos θ = cos(θ + π).
  4. Each A cos(2πft + φ) → (A/2)∠φ at +f and (A/2)∠−φ at −f.
  5. Amplitude is even, phase is odd.
- **Answer:** |c| = 5 at ±2, 2 at ±1, 2 at ±4; phase +π/8 at 2, −π/2 at 4, **+π/2 at 1**, and the negatives at −f.
- **⚠ The shown answer plots −π/2 at +1 Hz and +π/2 at −1 Hz (flipped).** It wrote −2e^(j(2πt − π/2)) and dropped the minus sign: −2e^(−jπ/2) = 2e^(jπ)e^(−jπ/2) = 2e^(+jπ/2). Check at t = 0.25: −4sin(2π·0.25) = −4, and 4cos(2πt + π/2) = −4 ✓, but the plotted 4cos(2πt − π/2) = +4 ✗. My Tutorial 2 Q1(b) solution has the correct +π/2 at 1 Hz.
- **Modulation view:** sin(3πt) is 1.5 Hz; × cos(5πt) (2.5 Hz carrier) shifts it to 2.5 ± 1.5 = 4 and 1 Hz, i.e. x(t)cos(2πf_c t) ↔ ½[X(f − f_c) + X(f + f_c)].

**25S1 Q1(b): is x(τ) = Ae^(−α|τ|) + B·sin(πf₀τ)/(πf₀τ) + C·cos(2πf₁τ) a valid autocorrelation? And is the paper's hint really wrong?**
- **Method:** check the 4 properties term by term, then combine (sum of even = even; triangle inequality for the peak; sum of PSDs ≥ 0). Property 3 (PSD ≥ 0) is decisive.
  - Example where 1 and 2 hold but 3 fails: Π(τ) is even with peak 1 at 0, but F = sinc(f), and sinc(1.5) = −0.212 < 0. So it's not valid.
- **Term by term:**
  - Ae^(−α|τ|): even because |−τ| = |τ|; peak at τ = 0 (e⁰ = 1, otherwise < 1); F = 2Aα/(α² + (2πf)²) ≥ 0 (A ≥ 0, α > 0, bottom is a sum of squares).
  - B·sinc(f₀τ): even because sin(−θ)/(−θ) = sin θ/θ; |sinc| ≤ 1 = sinc(0) (sin θ/θ → 1 as θ → 0; e.g. sin 0.1/0.1 = 0.998); F = (B/f₀)Π(f/f₀) ≥ 0 (Π is only 0 or 1).
  - C·cos(2πf₁τ): even because cos(−θ) = cos θ; |cos| ≤ 1 = cos 0; F = (C/2)[δ(f − f₁) + δ(f + f₁)] ≥ 0.
- **Combine:** |x(τ)| ≤ A·|e^…| + B·|sinc| + C·|cos| ≤ A + B + C = x(0). S(f) is a sum of three non-negative pieces. The cosine is a periodic part, which is allowed. **Valid** for A, B, C ≥ 0 (not all 0); R(0) = A + B + C = total power.
- **The hint table has two slips (checked by derivation, a sanity check and numerical integration).** Typos in printed hint tables do get through.
  - e^(−α|τ|): derivation ∫₀^∞ e^(−(α+j2πf)τ)dτ + ∫ from −∞ to 0 of e^((α−j2πf)τ)dτ = 1/(α + j2πf) + 1/(α − j2πf) = 2α/(α² + (2πf)²). Sanity check X(0) = area = 2/α; the hint gives 2/α². Numerically, at α = 2, f = 0.3: 0.530 vs the hint's 0.265.
  - sinc(f₀τ): correct is (1/f₀)Π(f/f₀), from Π(t/T) ↔ T·sinc(fT) plus duality. Sanity checks: X(0) = ∫sinc(f₀τ)dτ = 1/f₀ (not 1), and sin(πf₀τ) oscillates at f₀/2, so the spectrum must stop at ±f₀/2, not ±f₀. Numerically, f₀ = 2: X(0.5) = 0.5, X(1.5) = 0. The hint's RHS is the transform of sin(2πf₀τ)/(πτ).
  - **Exam method:** the slips only change sizes, not signs, so the conclusion is unchanged. Use the hint as given, and add at most a one-line note.

## DFT

**The matrix notation on the T02 "Recall" slide.** It's the ordinary DFT sums written as matrix
multiplication.
- ω = e^(+j2π/N) is the primitive root of unity (for N = 4, ω = j).
- G is the N×N matrix with G[n,k] = ω^(nk).
- G^H is the conjugate transpose: flip the rows and columns, and swap j ↔ −j. G is symmetric, so for the DFT this just swaps j ↔ −j.
- **X = G^H·x** is the analysis sum: row k of G^H dotted with x gives X[k] = Σ x[n]ω^(−kn).
- **x = (1/N)·G·X** is the synthesis.
- This works because G·G^H = N·I. The roots of unity are orthogonal: each row dotted with its own conjugate gives N, and with any other row gives 0.
- Worked example for N = 4 and x = [1, 2, 3, 4]: X = [10, −2+2j, −2, −2−2j]. Check: x[0] = (10 − 2 + 2j − 2 − 2 − 2j)/4 = 1 ✓.

**Why swap j ↔ −j, and where the row/column swap went.**
- **Conjugate (j ↔ −j):** analysis multiplies by the walker spinning the *opposite* way. For x[n] = jⁿ (frequency k = 1), dotting with row 1 of G^H gives [1, −j, −1, j]·[1, j, −1, −j] = 1 + 1 + 1 + 1 = 4 = N. Each product jⁿ·(−j)ⁿ = 1, so the spin is stopped. Dotting with row 1 of G instead (no swap) gives 1 − 1 + 1 − 1 = 0, which is wrong. Any other frequency still spins and cancels to 0. That's why the DFT analysis has the minus sign.
- **Transpose (swapping rows and columns):** it's there, but you can't see it. G[n,k] = ω^(nk) = ω^(kn) = G[k,n], so row 1 = column 1 = [1, j, −1, −j], and flipping changes nothing. The "H" includes the transpose because it matters for general matrices: [[1, 2j], [3, 4]]^H = [[1, 3], [−2j, 4]].

**DTFS by Euler (T02 Q2(b)): why e^(−j2πn/8) becomes e^(j2π(7)n/8).** Three steps, no Σ needed.
- **Split:** cos(2πn/8) = ½e^(j2πn/8) + ½e^(−j2πn/8). One arrow turns +1/8 lap per sample, the other −1/8.
- **Rename:** the DTFS only uses k = 0…N−1, so k = −1 has to move. Back 1/8 lap = forward 7/8 lap (they differ by a whole lap), so the angles at n = 1, 2, 3 (−π/4 vs 7π/4, …) differ by 2π, 4π, 6π, which is the same spot. In general, **−k ≡ N − k** (aliasing again).
- **Match:** synthesis is a[n] = (1/N)ΣA[k]e^(j2πkn/N), so each weight = A[k]/N, i.e. A[k] = N × weight. Weight ½ gives A[1] = A[7] = 4, and everything else is 0. Check: n = 0 gives (4 + 4)/8 = 1 = cos 0 ✓.

**sin → cos first: same DTFS? Yes.** The coefficients of a signal are unique, so either route gives the same answer.
- sin θ = cos(θ − π/2). T02 Q2(b): b[n] = sin(2πn/6 + π/3) = cos(2πn/6 − π/6) = ½e^(−jπ/6)·e^(j2πn/6) + ½e^(jπ/6)·e^(−j2πn/6).
- Why the sin route agrees: 1/j = −j = e^(−jπ/2), so dividing by 2j means "halve it and turn back a quarter lap", the same −π/2 shift. e^(jπ/3)/(2j) = ½e^(−jπ/6) ✓ and −e^(−jπ/3)/(2j) = ½e^(jπ/6) ✓ (−1/j = e^(jπ/2)).
- The cos route avoids dividing by j, so it's harder to slip on.

**The geometric series, which is used everywhere (asked to make it prominent on the sheet).** Sum = **first term / (1 − ratio)**, and it only works if |ratio| < 1.
- Any range: Σ from n = a to b of qⁿ = (qᵃ − q^(b+1))/(1 − q). Finite block from 0 to N−1: (1 − q^N)/(1 − q).
- Right-sided Z: Σ_{n≥0} (az⁻¹)ⁿ = z/(z−a). It needs |az⁻¹| < 1, i.e. |z| > |a|, which is *where the ROC comes from*.
- Left-sided Z: Σ_{n≥1} (z/a)ⁿ = (z/a)/(1 − z/a). It needs |z| < |a|.
- DTFT: the same sum with z = e^(jΩ). For example Σ(ae^(−jΩ))ⁿ = 1/(1 − ae^(−jΩ)) when |a| < 1.

**Why |q| < 1 for q = a⁻¹e^(−jΩ) (T02 Q3(b)).** Two facts: |A·B| = |A|·|B|, and |e^(−jΩ)| = √(cos²Ω + sin²Ω) = 1 (it only sets the direction). So |q| = (1/|a|)·1 = 1/|a|, which is < 1 exactly when |a| > 1.
- a = 2: q = ½e^(−jΩ) = 0.5, −0.5j, −0.5, 0.5j at Ω = 0, π/2, π, 3π/2, always size 0.5 (a circle of radius 0.5).
- a = 0.5: |q| = 2, so the sum blows up and there's no DTFT (Q3(a)).
- **Why the official solution may "assume |a| > 1":** the question only says a ≠ 0, but Q3(a) showed Σ|x| = Σ(1/|a|)ⁿ < ∞ ⇔ |a| > 1 (and Σ|y| ≤ (Σ|x|)²). For any other a there is no DTFT to compute, so Q3(b) works in the only case that exists. Chain: Q3(a) → |a| > 1 → |q| < 1 → 1/(1 − q) allowed. With a = 0.5 the formula 1/(1 − 2e^(−jΩ)) can still be written (−1 at Ω = 0), but it isn't x's DTFT (the outside-the-ROC trap). On the test, write "valid since |q| < 1".
- Then X(Ω) = Σ qⁿ = 1/(1 − a⁻¹e^(−jΩ)) and Y = X² (y = x ∗ x). Check with a = 2, Ω = 0: 1 + 0.5 + 0.25 + … = 2 = 1/(1 − 0.5) ✓.

**T03 Q1(b): recovering x from X on the circle r = 3.** Given X(3e^(jΩ)) = 1/(1 − (j/2)e^(−jΩ)).
- (1) With z = 3e^(jΩ), z⁻ⁿ = 3⁻ⁿe^(−jΩn), so X(3e^(jΩ)) = Σ(3⁻ⁿx[n])e^(−jΩn) is the DTFT of **w[n] = 3⁻ⁿx[n]**.
- (2) Match aⁿu[n] ↔ 1/(1 − ae^(−jΩ)) (|a| < 1): a = j/2, |a| = ½ ✓, so w = (j/2)ⁿu[n].
- (3) Undo the fading: x = 3ⁿw = (3j/2)ⁿu[n] = 1, 1.5j, −2.25, −3.375j, 5.06 (w shrinks, x grows).
- Why r = 3: |3j/2| = 1.5 > 1, so x has no DTFT. The ROC is |z| > 1.5, and 3 is inside it. Check: 1/(1 − (3j/2)z⁻¹) at z = 3e^(jΩ) gives the given expression ✓.
- **Reading the question's sentence** "z = 3e^(jΩ) in its ROC and X(3e^(jΩ)) = …" gives two facts. (1) The whole circle |z| = 3 (z = 3, 3j, −3, −3j at Ω = 0, π/2, π, 3π/2) is inside the ROC, so Σx[n]z⁻ⁿ converges there, w = 3⁻ⁿx has a DTFT, and inverting is legal (it also pins down which signal the formula belongs to). (2) The formula is X *evaluated at* those points, not multiplied: at Ω = 0, X(3) = 1/(1 − j/2), and the answer X(z) = 1/(1 − (3j/2)z⁻¹) gives the same ✓. Knowing X on one circle in the ROC is enough: that's the inverse-Z synthesis formula with r = 3.

**Nonempty vs empty ROC.** The ROC is the *set* of z where Σx[n]z⁻ⁿ is finite. Nonempty means at least one z works, so the Z-transform exists. Empty means no z works, so there is no Z-transform.
- Only two-sided signals can have an empty ROC: the right part needs |z| big (> a), the left part needs |z| small (< b), and they overlap only if a < b.
- 0.5^|n|: |z| > 0.5 and |z| < 2 → ring 0.5 < |z| < 2 (at z = 1 the sum is 1 + 2(0.5 + 0.25 + …) = 3 ✓).
- 2^|n|: |z| > 2 and |z| < 0.5 → empty. 2ⁿ for all n: |z| > 2 and |z| < 2 → empty (T03 Q1d).
- The lecture's four nonempty shapes (L3 slide 37): finite → all z (except maybe 0/∞); right-sided → |z| > a; left-sided → |z| < b; two-sided → ring a < |z| < b.

**T03 Q2(a): why Z{(n+1)u[n]} = U(z)².** (1) (u ∗ u)[n] = Σ u[m]u[n−m], where each term is 1 only for 0 ≤ m ≤ n, so it counts n+1 values: 1, 2, 3, … = (n+1)u[n] (the running sum again, T01 Q4b). (2) Convolution ↔ product, so Z{u ∗ u} = U·U = z²/(z−1)². Series check: (1 + z⁻¹ + z⁻² + …)² has coefficient of z⁻ⁿ = the number of ways a + b = n = n+1 ✓. Then n·u[n] = (n+1)u[n] − u[n], so X₂ = z²/(z−1)² − z/(z−1) = [z² − z(z−1)]/(z−1)² = z/(z−1)², |z| > 1, no DTFT (pole on |z| = 1). Shortcut: n·pⁿu[n] ↔ pz/(z−p)² with p = 1.

**Right- or left-sided ROC (T03 Q2a), and making the pole at 1 left-sided.** Going from a signal to X(z), the *signal* picks the side, not the formula: u[n] (nonzero for n ≥ 0) → right-sided → |z| > |p|; u[−n−1] (n ≤ −1) → left-sided → |z| < |p|; mixed pieces → the overlap ring. x₂ = n·u[n] is right-sided, so |z| > 1.
- Left-sided version: x = −n·u[−n−1] = …, 3, 2, 1 at n = −3, −2, −1, and 0 for n ≥ 0. X = Σ_{k≥1} k·z^k = z/(z−1)², which needs |z| < 1. It's the same formula with the opposite ROC (the extra pair −n·pⁿu[−n−1] ↔ pz/(z−p)², p = 1). Series check: z/(1−z)² = z + 2z² + 3z³ + … ✓. Still no DTFT (pole on |z| = 1).
- Given only X = z/(z−1)², the question must state the ROC: |z| > 1 → n·u[n]; |z| < 1 → −n·u[−n−1]. One pole gives only 2 ROCs, so there's no two-sided option.

**Range of the DTFT synthesis integral "∫_{2π}".** Any window of length 2π; the lecture writes 0 → 2π, and −π → π is identical. Reason: X(Ω) repeats every 2π, and e^(jΩn) does too (e^(j2πn) = 1 for whole n), so any full period gives the same area. Check with δ[n] (X = 1): x[0] = (1/2π)·2π = 1, and x[1] = (1/2π)∫e^(jΩ)dΩ = 0 (a full lap averages to 0). The CT twin integrates over all ω; DT needs only one lap because frequencies 2π apart are the same (aliasing).

## LCCDEs, Laplace and differential equations (final-exam prep)

The full version with rendered maths is Steps 14–16 of `Part2_Discrete_Time_Guide.md`.

**The ladder: each transform fixes what the one before couldn't handle.**
- Continuous time: Fourier series (periodic only) → CTFT (needs ∫|x| < ∞) → Laplace (fade by e^(−σt) first, so u(t), e^(2t)u(t) and unstable h work) → used to solve differential equations.
- Discrete time: DFT → DTFS → DTFT (needs Σ|x| < ∞) → Z (fade by r⁻ⁿ first) → used to solve difference equations.

**Difference equations (lecture 4).** The system is given as a rule, y[n] − ½y[n−1] = x[n]. Running it gives numbers one at a time; Z gives formulas because a delay is ×z⁻¹.
- The rule alone has infinitely many answers: for x = u, every y = 2 + C(½)ⁿ fits. You need P initial conditions; y[−1] = 1 gives C = −½. The ½ is the pole (try w = pⁿ).
- Output = zero-input (initial conditions only) + zero-state (input only). Unilateral shift: y[n−1] → z⁻¹Y₊ + y[−1]. Example: (½)ⁿ⁺¹ + [2 − (½)ⁿ] = 2 − (½)ⁿ⁺¹ = 1.5, 1.75, 1.875 ✓ (same as the loop).
- Zero initial conditions → LTI → H(z) = Y/X; y-terms → poles, x-terms → zeros. One H, several h: y − 2.5y[n−1] + y[n−2] = x has poles ½ and 2, so |z| > 2 is causal (unstable) and ½ < |z| < 2 is stable (two-sided). That's running the rule forward vs backward.
- Stable + sinusoid in → y_ss = |H(e^(jΩ₀))|·cos(Ω₀n + ∠H). Input (−1)ⁿ: H(−1) = 1/(1 + ½) = 2/3, so y_ss = (2/3)(−1)ⁿ. The poles make the transient; the input's frequency makes the steady state.

**Laplace (lecture 5) is Z's twin.** X(s) = ∫x(t)e^(−st)dt with s = σ + jω: σ is how hard you fade, ω is the frequency.
- The ROC depends only on σ, so it's a vertical strip (Z: a ring). Right-sided → right of the rightmost pole. The CTFT is X on the jω-axis, so it exists iff the axis is in the ROC.
- Main pair: e^(at)u(t) ↔ 1/(s−a), Re s > a. −e^(at)u(−t) gives the same formula with Re s < a. Partial fractions work directly on X(s) (no ÷z step). A pole left of the ROC runs forward (×u(t)); right of it, backward (×−u(−t)).
- **d/dt ↔ ×s** because d/dt e^(st) = s·e^(st) (Z: delaying zⁿ multiplies it by z⁻¹). That's why differential equations become algebra.
- z = e^(sT): the left half-plane → inside the unit circle, the jω-axis → the unit circle. So causal + stable means poles in Re s < 0.

**Differential equations (lecture 6) = lecture 4 with z⁻¹ → s.** y' + y = 2u(t), y(0⁻) = 1.
- Unilateral: y' → sY − y(0⁻) (integration by parts); y'' → s²Y − s·y(0⁻) − y'(0⁻).
- sY − 1 + Y = 2/s → Y = 1/(s+1) [zero-input] + 2/(s(s+1)) [zero-state] → y = e^(−t) + (2 − 2e^(−t)) = 2 − e^(−t). Discrete twin: 2 − (½)ⁿ⁺¹.
- Zero initial conditions → H(s); y'' − y = x has poles ±1: Re s > 1 is causal (unstable), −1 < Re s < 1 is stable.
- Steady state for cos ω₀t: H(jω₀). y' + y = cos t: H(j) = 1/(1+j) = 0.707∠−45°, so y_ss = ½(cos t + sin t).
- IVT: y(0⁺) = lim_{s→∞} sY. FVT: lim_{s→0} sY, but only if every pole of Y is in Re s < 0 apart from at most one simple pole at 0. Trap: 1/(s(s−1)) gives −1, but y = e^t − 1 → ∞.

**"Is an LCCDE another kind of system, besides LTI and non-LTI?" No: it's a way of *describing* a system, not a category.** LTI is a *property* (yes/no), like causal or stable. An LCCDE is a *description*, like a formula, an h[n], an H(z) or a circuit.
- The name says it's built to be LTI: **linear** (no y², no x·y) → L; **constant coefficients** (no n or t in them) → TI. The only thing that can break it is a non-zero starting state: y[−1] = 1 makes input 0 give output (½)ⁿ⁺¹ ≠ 0.
- **The nesting:** LCCDE at rest ⊂ LTI ⊂ all systems.
  - LTI but not an LCCDE: the pure delay y(t) = x(t − 2) (H = e^(−2s), not a fraction of polynomials) and the ideal low-pass filter (sinc h).
  - Not LTI at all: y = x², y[n] = n·x[n], y = x[2n], 2sin(x) (23S1 Q1).
- **Transforms belong to signals, not systems.** You can take the FT/Z/Laplace of any signal that has one, including the output of a non-LTI system. What needs LTI is the *system* shortcut y = h ∗ x ⇔ Y = H·X, and "sinusoid in → same sinusoid out, scaled".
  - y = x² with input cos t gives ½ + ½cos 2t. New frequencies 0 and 2 appear, but H can only scale and shift the frequencies already there, so no H exists. Its output's FT is still fine: impulses at 0 and ±2.
  - y[n] = n·x[n]: kicking at n = 0 gives 0, kicking at n = 1 gives δ[n−1]. The response depends on *when* you kick, so there's no single h.
- **LCCDE with initial conditions → yes, Z/Laplace still work.** The unilateral transform gives Y₊ = (initial-condition terms)/A + H·X₊ = zero-input + zero-state. The zero-state part is pure LTI; the "non-LTI" part is just an added term from the stored memory, not real nonlinearity.
- In all five past papers, non-LTI systems appear only in "test linear / time-invariant / causal" questions. Every convolution or transform question is about an LTI system (or an LCCDE with initial conditions).

**Bilateral vs unilateral transform.** The only difference is where the sum (or integral) starts.
- Bilateral (two-sided): X(z) = Σ_{n=−∞}^{∞} x[n]z⁻ⁿ, X(s) = ∫_{−∞}^{∞} x(t)e^(−st)dt. It sees the whole timeline.
- Unilateral (one-sided): Y₊(z) = Σ_{n=0}^{∞} y[n]z⁻ⁿ, Y₊(s) = ∫_{0⁻}^{∞} y(t)e^(−st)dt. It ignores everything before 0.
- **For a signal that is 0 before n = 0 they're identical** (0.5ⁿu[n] → z/(z−0.5) either way), so the pairs table is the same. Only the **shift and derivative rules** differ.
- **Why the unilateral shift rule has an extra term**, using y[n] − ½y[n−1] = u[n], y[−1] = 1, so y = 1 | 1.5, 1.75, 1.875, … (the bar is n = 0):
  - Y₊ = 1.5 + 1.75z⁻¹ + 1.875z⁻² + … (y[−1] is outside the window).
  - w[n] = y[n−1] slides everything right one step, so w[0] = y[−1] = 1, w[1] = 1.5, w[2] = 1.75, …
  - W₊ = 1 + 1.5z⁻¹ + 1.75z⁻² + … = **y[−1] + z⁻¹Y₊**. Delaying drags the stored value y[−1] into the window. Two steps: y[n−2] → z⁻²Y₊ + z⁻¹y[−1] + y[−2].
  - Continuous twin: y′ → sY₊ − y(0⁻), and y″ → s²Y₊ − s·y(0⁻) − y′(0⁻). Here y(0⁻) is the stored state, e.g. a capacitor's voltage.
  - Bilateral: y[n−1] → z⁻¹Y and y′ → sY, with no extra term, because nothing is outside its window.
- **Which one to use:**

| Situation | Transform | Why |
|---|---|---|
| y[−1], y[−2] or y(0⁻), y′(0⁻) are given | unilateral | the initial conditions enter through the shift/derivative rule → zero-input + zero-state |
| "initially at rest"/"relaxed", or find H, h, poles, the ROC, causal/stable | bilateral | no stored state; you choose the ROC |
| IVT / FVT | unilateral | both theorems are stated for Y₊ |
| a signal that's non-zero before 0 (left- or two-sided) | bilateral | the unilateral transform would throw away n < 0 |

- A unilateral transform always describes a right-sided signal, so there's no ROC choice: invert with the right-sided pairs, and the answer holds for n ≥ 0 (t ≥ 0).
- In 25S1: Q3(c), y″ − 2y′ + y = u(t) with y(0) = 2, y′(0) = 0, is unilateral: s²Y − 2s − 2(sY − 2) + Y = 1/s → y = 1 + (1 − t)eᵗ. Q4(a) (find H(z), the ROC, stability and h[n]) is bilateral.

**z⁻ⁿ is a position tag, and ×z⁻¹ is "one step later".** Every Z-transform has negative powers, not just the transform of y[n−1].
- Σ y[n]z⁻ⁿ tags each sample with its position: y[0]·z⁰ + y[1]·z⁻¹ + y[2]·z⁻². So in Y₊ = 1.5 + 1.75z⁻¹ + 1.875z⁻², the z⁻¹ is "this sample sits at n = 1".
- Multiplying the whole transform by z⁻¹ adds 1 to every tag, which moves every sample one step later. z⁻¹Y₊ = 1.5z⁻¹ + 1.75z⁻² + … is the list 0, 1.5, 1.75, … at n = 0, 1, 2: the in-window part of y delayed by one step, with the n = 0 slot left empty.
- The true delayed signal w[n] = y[n−1] has y[−1] = 1 in that slot, so W₊ = y[−1] + z⁻¹Y₊. Bilateral: nothing is outside the window, so the slot is never empty and the rule is just z⁻¹Y.

**y′ and z⁻¹ are not the same operation; they're the same *role*.** Each is what its equation is built from, and each turns into multiplication.

| | Discrete | Continuous |
|---|---|---|
| delay | y[n−1] → z⁻¹Y | y(t−T) → e^(−sT)Y |
| rate of change | y[n] − y[n−1] → (1 − z⁻¹)Y | y′ → sY |

- A difference equation is built from delays, so Z turns it into algebra in z⁻¹. A differential equation is built from derivatives, so Laplace turns it into algebra in s. The link is z = e^(sT).

**H vs Y vs X: what a transform "means".**
- Transform of a **system** = transform of its impulse response h → **H(z) or H(s), the system (transfer) function**. It's the system's recipe for every input, not a response to any one input.
- Transform of a **signal** x → X: the signal rewritten as a sum of building blocks pⁿ (or e^(pt)). Its poles say which pⁿ it's made of (|p| = grow/stay/die, angle = how fast it wiggles). The ROC says which way in time each runs. If |z| = 1 is in the ROC, X on the circle is its frequency content (DTFT).
- **The response** to a particular input is y: Y = H·X, and then invert. Output poles = system poles (the transient, e.g. (½)ⁿ) + input poles (the steady state, e.g. the constant from u[n]). For y[n] − ½y[n−1] = u[n]: Y = z/(z−½) · z/(z−1) → (½)ⁿ part + constant 2.
- **Paper workflow:** pattern-match with the pairs table in both directions. Forward: split into pieces that match the pairs and properties. Then do the algebra for Y or H. Inverse: partial fractions until each piece matches a pair. What the table doesn't give you (and the marks reward) is the reasoning: which ROC, stable/causal, which steady state, whether the FVT applies, and the "discuss" parts.

**The point of the course.** Rewrite signals as sums of building blocks that an LTI system only *scales*: e^(jωt) (Fourier), zⁿ (Z), e^(st) (Laplace). Feed in e^(st) and an LTI system gives H(s)·e^(st) out. Then the hard operations become easy: convolution → multiplication, difference/differential equations → algebra.
- **Fourier family** (FS, CTFT, DFT, DTFS, DTFT): what frequencies a signal contains, and what a system does to each frequency (the frequency response: filters, spectra, power, sampling/aliasing).
- **Z / Laplace:** going beyond frequencies to signals and systems that blow up, initial conditions, and stability/causality from the poles and the ROC.

**Closing the circle: analog design (Laplace) → z → a difference equation on an MCU.** (I'd called it a "differential equation" from an earlier course; the MCU runs a *difference* equation, because it has no derivatives, only stored samples.) Every step is a piece of this course:

| Step | Course topic |
|---|---|
| 1. Model or design in continuous time: ODE → H(s) | Laplace + ODEs (guide Step 16, L6 RLC) |
| 2. Sample the sensor: x[n] = x(nT), with fₛ > 2 × the highest frequency | sampling, Nyquist, aliasing (Steps 1–2) |
| 3. Move each pole: z = e^(sT) (left half-plane → inside the unit circle) | the Laplace–Z link (Step 15.6, L5 p.54–57; 24S1/25S2 Q4(a)) |
| 4. H(z) → difference equation: cross-multiply, z⁻ᵏ → a k-step delay | LCCDE, run backwards (Step 14) |
| 5. Check: poles inside |z| = 1, H(e^(jΩ)) with Ω = ωT | poles/ROC, frequency response (Steps 10, 12, 14.5) |
| 6. Run it every sample; the stored y_prev starts at the initial condition | LCCDE as a loop; zero-input = the starting value (14.1, 14.3) |

- **Worked (RC low-pass, τ = 0.1 s, fₛ = 100 Hz, T = 0.01 s):**
  - 0.1y′ + y = x → H(s) = 10/(s + 10), so the pole is −10.
  - Its z-plane pole is e^(−10·0.01) = e^(−0.1) = 0.9048, inside the circle, so it's stable.
  - Choose the gain so H(1) = 1: H(z) = 0.0952/(1 − 0.9048z⁻¹).
  - Cross-multiplying gives y[n] = 0.9048·y[n−1] + 0.0952·x[n]. That's the exponential moving average: one multiply-add per sample, and it settles at 1 for a step input.
- **Why the pole moves by z = e^(sT):** e^(−10t) sampled every 0.01 s is 1, 0.9048, 0.8187, …, 0.3679 at n = 0, 1, 2, …, 10, which is exactly 0.9048ⁿ. A continuous pole p and a discrete pole e^(pT) describe the same decay per sample.
- **Not covered in the course:** practical discretization methods (Tustin/bilinear, zero-order hold, MATLAB `c2d`) choose the numerator differently. ZOH puts the pole exactly at e^(pT); Tustin gives 0.95/1.05 = 0.9048 too. The course only examines the s-plane ↔ z-plane mapping and comparison.

**Where z = e^(sT) comes from (why the pole −10 became e^(−10×0.01)).**
- An s-pole p means the signal contains **e^(pt)**: H(s) = 10/(s+10) ↔ h(t) = 10e^(−10t). A z-pole q means it contains **qⁿ** (qⁿu[n] ↔ z/(z−q)).
- The MCU only sees t = nT = 0, 0.01, 0.02, …, so e^(−10t) becomes e^(−10·nT) = **(e^(−10T))ⁿ** = (e^(−0.1))ⁿ = 0.9048ⁿ (exponent rule e^(an) = (eᵃ)ⁿ). So the samples are qⁿ with **q = e^(pT)**.
- Meaning: e^(pT) is what the continuous exponential gets multiplied by during one sample gap. e^(−10t) at t = 0, 0.01, 0.02, 0.03 is 1, 0.9048, 0.8187, 0.7408: each is 0.9048 × the one before. Continuous exponents *add* (e^(p(t+T)) = e^(pT)·e^(pt)); discrete steps *multiply*.
- Reverse: **s = ln(z)/T**. ln(0.9048)/0.01 = −0.1/0.01 = −10.
- A complex pole s = σ + jω gives z = e^(σT)·e^(jωT): |z| = e^(σT) is the decay per sample, and the angle ωT = **Ω** (rad/sample) is where Ω = ω/fₛ comes from. So σ < 0 → |z| < 1 (inside), the jω-axis → |z| = 1, σ > 0 → outside.
- Table with T = 0.01 (fₛ = 100 Hz): s = −10 → 0.9048 (dies); 0 → 1 (constant); +10 → e^(0.1) = 1.105 (grows ×1.105 per sample, so unstable); j2π·50 (50 Hz) → e^(jπ) = −1, which is cos(πn) = (−1)ⁿ at the Nyquist rate.
- ω and ω + 2π/T land on the same z (e^(j2π) = 1). That's **aliasing**, seen as poles.
- You **move poles**; you don't substitute. Putting s = ln(z)/T into H(s) gives 10/(100 ln z + 10), which isn't a fraction of polynomials, so you can't run it on an MCU. Then set the gain separately (here H(1) = 1 gives b = 0.0952).
