# SC3102 Lab 4: Z-transforms and Difference Equations — Quick Guide

A short overview of what this lab covers and what it's trying to teach.
For the full worked answers, see [Lab_4_Answers.md](Lab_4_Answers.md). The answers are also
written into [Lab-04-Z-transform.ipynb](Lab-04-Z-transform.ipynb) under each question, and the
notebook has been run so every plot and audio player is saved in it. Every number below comes from
running the experiments, not from theory alone.

---

## What the lab is about

You've done the CTFT, and the DTFT is the same idea with a sum. Both break on signals that don't die
out, like a step or a growing exponential. The Z-transform fixes that: it shrinks the signal by $r^{-n}$
first, then takes the DTFT. A point $z=re^{j\Omega}$ means "squash by $r$, look at frequency $\Omega$".
The unit circle ($r=1$) is the ordinary DTFT.

### 1. Why the ROC matters (Q1)

- $H(z)=\frac{z}{z-0.6}+\frac{z}{z-1.2}$ has poles at 0.6 and 1.2, so there are three possible ROCs,
  and each one is a **different signal**:
  - $|z|<0.6$: left-sided. Not causal, not stable.
  - $0.6<|z|<1.2$: two-sided. Not causal, but **stable** ($\sum|h|=7.5$).
  - $|z|>1.2$: right-sided. **Causal**, but not stable ($h[35]\approx591$).
- Stable means the unit circle is in the ROC. Causal means the ROC is the outside of the biggest
  pole. You can't have both here, because the pole at 1.2 sits outside the unit circle.
- Outside the ROC the formula still gives a number, but the actual sum blows up. At $z=1.5$ the
  partial-sum error grows ×1.25 per term (to 12 000 after 35 terms), while at $z=0.9$ it shrinks
  ×0.75 per term.

### 2. Difference equations (Q2)

- $y[n]=a\,y[n-1]+x[n]$ is the DT version of a first-order ODE. With $a=0.9$ and input 1, the output
  always heads to $c/(1-a)=10$. Starting from 11 it falls, and starting from 4 it rises.
- The output only settles if $|a|<1$. With $a=1$ it ramps, $a=-1$ bounces forever, and $a=1.1$ blows
  up. If $a<0$, the output flips sign every sample.
- **Response = zero-input + zero-state**, exactly like CT: $y_{-1}a^{n+1}$ from the initial condition,
  plus $c\frac{1-a^{n+1}}{1-a}$ from the input. The formula matches the simulation to about $10^{-15}$.
- Leaving $y_{-1}$ out of the unilateral shift rule means assuming $y[-1]=0$. Only the zero-state
  part survives, and that is the transfer function $H(z)=z/(z-a)$.

### 3. FIR filters (Q3)

- $y[n]=\sum_{k=0}^{M-1}h[k]x[n-k]$ is a filter whose impulse response is just the $M$ taps. Its
  $H(z)=\sum h[k]z^{-k}$ has all its poles at 0, so it is always stable and causal, and it can run
  live, one sample at a time.
- A bigger $M$ gets closer to the ideal Lab 3 filter. The edge width is about $3.3f_s/M$: 5.9 kHz at
  $M=9$, 103 Hz at $M=513$. With 9 or 33 taps the "band-pass" is really a low-pass.
- Denoising error: 0.033 ($M=9$), 0.0078 ($M=33$), 0.00033 ($M=513$). But it isn't monotonic:
  $M=65$ is worse (0.12) because its 100 Hz edge is wide enough to land on the 220 Hz tone. By ear,
  $M=33$ already removes the whistle, while $M=9$ leaves a faint one.
- Radio: quality drops for $M\lesssim33$. At $M=9$ there is high-frequency junk, and at $M=33$ the
  dialogue is muffled. By $M=513$ the errors are 0.1% (music) and 1.1% (dialogue).
- The cost of a large $M$ is delay ($(M-1)/2$ samples, which is 16 ms at 513 taps and 16 kHz), memory
  and computation.

---

## What you're supposed to learn

- **A Z-transform is an expression and an ROC.** The poles fix where the ROC boundaries can be.
- **You can read stability and causality off the pole-zero plot:** check the unit circle and the
  outermost pole.
- **A difference equation is solved like an ODE.** The geometric mode $a^n$ replaces $e^{\lambda t}$,
  and "inside the unit circle" replaces "left half-plane".
- **Practical filters are finite.** More taps give sharper edges, and they cost latency.

The first section of [Lab_4_Answers.md](Lab_4_Answers.md) has a table matching each CT idea you know
(CTFT, convolution, ODEs, zero-input and zero-state) to its DT version. It also has a column for
Laplace, which comes next in lecture 4.

---

## Things to know

- **Python version:** everything was run on the repo's `.venv` (Python 3.11, numpy 2.x), not the
  Python 3.8 the README pins. `lab_tools.py` worked without any changes. I added `plotly` (7.1.0,
  needed for the 3D plot in 1B) and `nbformat`/`nbclient`/`nbconvert` to that venv. To open the
  notebook in a browser you still need `pip install notebook`.
- **File size:** the notebook is about 17 MB. The 3D plot bundles plotly.js (~7 MB) so it works
  offline, and the radio audio players are ~6 MB.
- **Code cells:** no code was changed, and every cell is at its default setting. Saved plots show
  Region 0 in 1B/1C, $a=0.9$ in 2A, and $M=9, 33, 513$ in Q3.
- **Audio:** the "what you should hear" answers in 3D/3E are predicted from the measured levels
  (for example, a whistle 30 dB under the tone). Listen and check them yourself.
- **Typos in the handout:** "maagnitudes", "comptue", "input response" (should be zero-input), plus
  a 2C cell whose `initial` (4) doesn't match 2A's (11). The full list is in section 4 of the answers.

**Before the lab:** work through the "Key takeaways" list at the end of
[Lab_4_Answers.md](Lab_4_Answers.md) yourself. If you're asked about this in person, you'll need to
explain these ideas, not just have the answers.
