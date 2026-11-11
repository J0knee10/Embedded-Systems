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

## Systems

**FIR vs IIR.** Both names describe h[n], the response to a single kick δ.
- **FIR** has no feedback. For example, y = ½x[n] + ½x[n−1] gives h = [½, ½] and then stops. The coefficients are h, every pole is at 0, and it's always stable.
- **IIR** has feedback (y[n−k] on the right-hand side). For example, y = 0.5y[n−1] + x[n] gives h = 0.5ⁿ, which never ends. H = z/(z−0.5), and it's stable only if the pole is inside |z| = 1. Changing 0.5 to 2 makes it blow up.

**Analysing a signal or a system?** Both, with the same maths.
- Transform a signal and you get X: what frequencies it contains.
- Transform an impulse response h and you get H: what the system does to each frequency.
- They connect through Y = H·X.
- The same ROC rules answer different questions. For a signal: which way it runs, and whether the DTFT exists. For a system: whether it's causal and whether it's stable.

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
