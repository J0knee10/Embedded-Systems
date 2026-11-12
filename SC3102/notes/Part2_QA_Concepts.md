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
