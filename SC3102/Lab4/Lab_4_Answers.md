# SC3102 Lab 4: Z-transforms and Difference Equations — Complete Answers & Notes

**Environment:** the repo-wide venv at `D:\Jon\Uni\SYproject\embeddedSys\.venv`
(Python 3.11.9 · numpy 2.4.6 · scipy 1.17.1 · matplotlib 3.11.2). For this lab I added `plotly`
7.1.0, which the interactive 3D plot in 1B needs (the lab pins 6.3.0), and `nbformat`/`nbclient`/`nbconvert`
to run the notebook. `lab_tools.py` ran **unchanged**, with no errors or warnings.

The answers are also written directly into [Lab-04-Z-transform.ipynb](Lab-04-Z-transform.ipynb) as
markdown cells under each question. The notebook has been executed, so every plot, the 3D plot and
every audio player are saved in it. All numbers below come from that run, or from extra runs of the
same `lab_tools` functions with other parameter values.

---

## 0. The one idea this lab is built around

You know the **CTFT** from Part 1: $X(\omega)=\int x(t)e^{-j\omega t}dt$. It only exists if
$\int|x(t)|\,dt<\infty$. The **DTFT** is the same thing with a sum,
$X(\Omega)=\sum_n x[n]e^{-j\Omega n}$, and it only exists if $\sum_n|x[n]|<\infty$.
Many signals we care about fail that test: $u[n]$, $1.2^n u[n]$ (Q1), the ramp you get in Q2 when $a=1$.

**The Z-transform fixes this by squashing the signal first, then taking the DTFT** (lecture 2):

$$x[n]\;\longrightarrow\;x[n]\,r^{-n}\quad\text{(pick $r$ so this is summable), then DTFT:}\quad
\sum_n x[n]\,r^{-n}e^{-j\Omega n}=\sum_n x[n]\,(re^{j\Omega})^{-n}=\sum_n x[n]\,z^{-n}=X(z).$$

So a point $z=re^{j\Omega}$ in the complex plane carries two instructions:
**$|z|=r$ is how hard to squash, and $\angle z=\Omega$ is which frequency to read off.**

- **ROC** = the squash factors $r$ for which $x[n]r^{-n}$ is summable. It depends only on $|z|$, so
  ROCs are always circles and rings.
- **The unit circle $|z|=1$ means no squashing.** There $X(z)$ *is* the DTFT. If $h[n]$ is an
  impulse response, this is the frequency response, and "unit circle in the ROC" is exactly
  "$\sum|h[n]|<\infty$", i.e. **BIBO stable**.
- Every ROC in this lab is a **geometric series** question: $\sum q^n=\frac{1}{1-q}$ iff $|q|<1$.
  For example, $\sum_{n\ge0}0.6^n z^{-n}=\sum(0.6/z)^n$ converges iff $|z|>0.6$, giving
  $\frac{z}{z-0.6}$.
- **The formula alone is not enough.** $\frac{z}{z-0.6}$ is the transform of $0.6^n u[n]$ when
  $|z|>0.6$, and of $-0.6^n u[-n-1]$ when $|z|<0.6$. So **a Z-transform = expression + ROC** (Q1C, Q1D).

**ROC rules (lectures 2–3), with the Q1 example $H(z)=\frac{z}{z-0.6}+\frac{z}{z-1.2}$:**

| Signal is… | ROC is… | Q1 example |
|---|---|---|
| finite length | everything except maybe $z=0$ / $\infty$ | Q3's FIR filters: $\lvert z\rvert>0$ |
| right-sided | **outside** the outermost pole | Region 2: $\lvert z\rvert>1.2$ |
| left-sided | **inside** the innermost pole | Region 0: $\lvert z\rvert<0.6$ |
| two-sided | a **ring** between poles | Region 1: $0.6<\lvert z\rvert<1.2$ |

| System property | ROC test |
|---|---|
| BIBO stable | unit circle $\lvert z\rvert=1$ is in the ROC |
| causal | ROC is the outside of the outermost pole, including $z=\infty$ |
| causal **and** stable | **all poles inside the unit circle** |

**Mapping from what you already know (CT) to this lab (DT).** The Laplace column is lecture 4, which
comes next. It is the mirror image of the Z-transform, so you don't need it yet.

| Continuous time (Part 1) | Discrete time (this lab) | Laplace (lecture 4, coming next) |
|---|---|---|
| CTFT $\int x(t)e^{-j\omega t}dt$, needs $\int\lvert x\rvert<\infty$ | DTFT $\sum x[n]e^{-j\Omega n}$, needs $\sum\lvert x\rvert<\infty$ | |
| — | **Z:** $\sum x[n]z^{-n}$, $z=re^{j\Omega}$ = DTFT of $x[n]r^{-n}$ | $\int x(t)e^{-st}dt$, $s=\sigma+j\omega$ = CTFT of $x(t)e^{-\sigma t}$ |
| frequency response $H(\omega)$ | $H(z)$ on the **unit circle** | $H(s)$ on the **$j\omega$ axis** |
| mode $e^{\lambda t}$ decays iff $\mathrm{Re}\,\lambda<0$ | mode $a^n$ decays iff $\lvert a\rvert<1$; $a<0$ flips sign every sample | with $z=e^{s}$: left half-plane ↔ inside the unit circle |
| convolution $y=x*h \leftrightarrow Y=HX$ | $y[n]=\sum_k h[k]x[n-k]\leftrightarrow Y(z)=H(z)X(z)$ (Q3) | same |
| $\frac{d}{dt}$ is the basic operation | $z^{-1}$ = **one-sample delay** | $s$ = differentiate |
| ODE $y'=-\alpha y+x$ | difference equation $y[n]=a\,y[n-1]+x[n]$ (Q2) | |
| $y=y_0e^{-\alpha t}+\frac{c}{\alpha}(1-e^{-\alpha t})$ (zero-input + zero-state) | $y=y_{-1}a^{n+1}+c\frac{1-a^{n+1}}{1-a}$ (zero-input + zero-state) | |

The last row is the main thing to see in Q2. A first-order system with a constant input looks the same in
both worlds: an initial condition that dies away geometrically, plus a rise to a steady state. In DT,
$a$ plays the role of $e^{-\alpha T}$. Sampling $e^{-\alpha t}$ every $T$ seconds gives
$(e^{-\alpha T})^n=a^n$, and that is the $z=e^{sT}$ link.

---

## 1. Q1 — The Z-transform and the ROC

### 1A. The weighted sum
`weight(np.arange(3), 2.0)` = $[1,\ 0.5,\ 0.25]$, i.e. $z^{-n}$ for $z=2$. For $h[n]=0.6^nu[n]$ the
weighted terms are $(0.6/z)^n$, a geometric series. It converges iff $|z|>0.6$ and sums to $\frac{z}{z-0.6}$.

### 1B. Poles and zeros
$H(z)=\frac{2z^2-1.8z}{z^2-1.8z+0.72}=\frac{2z(z-0.9)}{(z-0.6)(z-1.2)}$: zeros at $0,\ 0.9$, poles at
$0.6,\ 1.2$ (confirmed by `rational_parts`: residues 1 and 1, no direct term). Two poles give three
candidate ROCs.

### 1C. Which inverse belongs to which ROC

| Region | ROC | $h[n]$ | Values | Side | Causal | Stable |
|---|---|---|---|---|---|---|
| 0 | $\lvert z\rvert<0.6$ | $-(0.6^n+1.2^n)u[-n-1]$ | $h[-1]=-2.5$, $h[-35]\approx-5.8\times10^7$ | left | no (anti-causal) | no |
| 1 | $0.6<\lvert z\rvert<1.2$ | $0.6^nu[n]-1.2^nu[-n-1]$ | $h[0]=1$, $h[-1]=-0.833$; $\sum\lvert h\rvert=2.5+5=7.5$ | two-sided | no | **yes** |
| 2 | $\lvert z\rvert>1.2$ | $(0.6^n+1.2^n)u[n]$ | $h[0]=2$, $h[35]\approx591$ | right | **yes** | no |

- Only Region 1 contains the unit circle ($0.6<1<1.2$), so only it is stable.
- Only Region 2 is the outside of the outermost pole, so only it is causal.
- Causal **and** stable would need both poles inside $|z|=1$. The pole at 1.2 rules that out, so here
  you have to choose one or the other.

### 1D. Outside the ROC (Region 1, $z=0.9$ vs $z=1.5$)

Each term is geometric: right tail $|h[n]z^{-n}|=(0.6/|z|)^n$, left tail $(|z|/1.2)^{|n|}$.

| | right-tail ratio | left-tail ratio | partial-sum error at $M=0,\,10,\,20,\,35$ |
|---|---|---|---|
| $z=0.9$ (inside) | $2/3$ (decays) | $3/4$ (decays) | $1,\ 0.134,\ 0.0089,\ 1.3\times10^{-4}$, i.e. ×0.75 per step → **converges** |
| $z=1.5$ (outside) | $0.4$ (decays) | $1.25$ (**grows**) | $5.67,\ 46.6,\ 434,\ 1.2\times10^{4}$, i.e. ×1.25 per step → **diverges** |

- At $z=0.9$ the sum converges to the rational value, which happens to be $H(0.9)=0$ because
  $0.9$ is the zero of $H$ (right tail $=+3$, left tail $=-3$).
- At $z=1.5$ the formula still gives $H(1.5)=6.67$, but the series of *this* signal runs off to
  $-\infty$ ($S_{35}\approx-1.2\times10^4$). $6.67$ is the value of the **Region 2** signal's transform.
- **The expression is defined everywhere except at the poles, but it equals the sum only inside the ROC.**

---

## 2. Q2 — LCCDEs: $y[n]=a\,y[n-1]+x[n]$, $x[n]=c$ for $n\ge0$, $y[-1]=y_{-1}$

### 2A. Initial conditions and steady state ($a=0.9,\ c=1$)

Measure from the steady state: $y[n]-10=0.9^{n+1}(y_{-1}-10)$. The gap shrinks by 10% per sample.

| $y_{-1}$ | $y[0],y[1],y[2]$ | trend | $y[50]$ |
|---|---|---|---|
| 11 (default) | 10.9, 10.81, 10.73 | decreasing | 10.005 |
| 10 | 10, 10, 10 | constant | 10 |
| 4 | 4.6, 5.14, 5.63 | increasing | 9.97 |

- **The initial value only sets the start and the direction:** above 10 the output falls, below 10 it rises.
- **Steady state $=c/(1-a)$** (set $y[n]=y[n-1]$). It doesn't depend on $y_{-1}$ but does depend on `decay`:
  $a=0,\ 0.5,\ 0.9,\ 0.99\to1,\ 2,\ 10,\ 100$. A bigger $a$ also means a slower approach. The number
  of samples to close 99% of the gap, $\ln0.01/\ln a$, is $7,\ 44,\ 458$, so for $a=0.99$ the output
  is still only at 46.7 when $n=50$. The steady state scales with $c$.
- **Outside $0<a<1$:** $a=-0.5$ alternates in sign while converging to $0.667$. $a=1$ gives a ramp
  ($y[n]=y_{-1}+c(n+1)$, 62 at $n=50$). $a=-1$ bounces between $-10$ and $11$ forever. $a=1.1$ blows
  up (2702 at $n=50$). **The output settles iff $|a|<1$**, i.e. iff the pole $z=a$ is inside the
  unit circle. This agrees with the lecture's final value theorem,
  $\lim_{z\to1}(1-z^{-1})Y_+(z)=c/(1-a)$.

### 2B. Omitting $y_{-1}$ from the shift rule

$$\sum_{n=0}^{\infty}y[n-1]z^{-n}=\underbrace{y[-1]}_{n=0\text{ term}}+z^{-1}\sum_{m=0}^{\infty}y[m]z^{-m}=y_{-1}+z^{-1}Y_+.$$

Dropping $y_{-1}$ **assumes $y[-1]=0$** (the system starts at rest). Then
$Y_+=az^{-1}Y_++X_+\Rightarrow Y_+=\frac{X_+}{1-az^{-1}}$, so **only the zero-state response survives**
and the zero-input term $y_{-1}a^{n+1}$ is lost. What remains is $Y_+=H(z)X_+$ with
$H(z)=\frac{z}{z-a}$: the LCCDE is LTI only under zero initial conditions (lecture 3). With the
defaults, the true $y[0]=0.9\cdot11+1=10.9$, but dropping $y_{-1}$ gives $1$.

### 2C. Formula vs simulation

The largest gap between `response_formula` and `initial_condition_demo` is pure round-off:
$1.8\times10^{-15}$ ($a=0.9,\,y_{-1}=4$, $n\le20$), $3.6\times10^{-15}$ ($y_{-1}=11$), $0$ ($a=\pm0.5$),
$2.3\times10^{-13}$ ($a=1.1$, values up to 1800), $8.5\times10^{-14}$ ($a=0.99,\,c=2$, $n\le200$). They
agree. Zero-input + zero-state = complete response to $1.8\times10^{-15}$. The one exception is
$a=1$: the formula is $0/0$ (numpy returns `nan`), and you need the limit $c(n+1)$.

$a=0.5,\ y_{-1}=1,\ c=1$ is the **lecture 3 example** $y[n]-\tfrac12y[n-1]=u[n]$: zero-input
$(\tfrac12)^{n+1}$, zero-state $2-(\tfrac12)^n$, total $2-(\tfrac12)^{n+1}=1.5,\,1.75,\,1.875,\dots$ ✓.

### 2D. Zero-input response $y_{zi}[n]=4a^{n+1}$

| $a$ | first values | $n=50$ | |
|---|---|---|---|
| 0.5 | 2, 1, 0.5, 0.25 | $2\times10^{-15}$ | gone in ~10 samples |
| 0.9 | 3.6, 3.24, 2.92 | 0.019 | slow decay |
| 0 | 0, 0, 0 | 0 | no memory at all |
| −0.5 | −2, 1, −0.5 | ≈0 | flips sign, decays |
| 1 / −1 | 4, 4, 4 / −4, 4, −4 | 4 / −4 | never dies |
| 1.1 / 1.5 | 4.4, 4.84 / 6, 9, 13.5 | 517 / $3.8\times10^9$ | grows |

**$|a|$ sets whether the initial condition is forgotten** ($<1$ forgotten, $=1$ kept, $>1$ amplified).
The closer $|a|$ is to 1, the longer the memory. **The sign of $a$ sets whether it alternates.** In
CT, $e^{\lambda t}$ behaves the same way with $\mathrm{Re}\,\lambda<0$. The zero-state response
(next cell, $a=0.5$) rises $1,\,1.5,\,1.75,\dots\to2$.

---

## 3. Q3 — FIR filters as difference equations

### 3A. What the filter is

- **Impulse response:** set $x=\delta$, and $y[n]=h[n]$ for $0\le n\le M-1$, zero otherwise.
  **The taps are the impulse response.** It has finite length, so this is an **FIR** filter, and
  $y[n]=\sum_k h[k]x[n-k]$ is just convolution.
- **Transfer function:** $H(z)=\sum_{k=0}^{M-1}h[k]z^{-k}=\frac{h[0]z^{M-1}+\dots+h[M-1]}{z^{M-1}}$.
  **All poles are at $z=0$**, so the ROC is $|z|>0$, which always includes the unit circle. FIR is
  **always stable**, and **causal**. The zeros shape the response (for $M=33$: 32 zeros,
  $0.77\le|z|\le1.30$).
- It uses no past outputs, so it is the LCCDE with no feedback. With feedback (IIR, like Q2) you get
  sharper edges per coefficient, but you also get real poles and have to check stability.
- **How `lab_tools` makes $h$:** `firwin(M, [100, 1000], window="hamming")` takes the ideal band-pass
  impulse response (two sincs), keeps the middle $M$ samples, tapers them with a Hamming window, and
  shifts them to start at 0. The taps are symmetric, so the filter is a **pure delay of $(M-1)/2$
  samples**. `firwin` also scales the gain to exactly 1 at the band centre (550 Hz), which matters in 3C.

**Frequency response vs $M$** ($f_s=16$ kHz):

| $M$ | 0 Hz | 100 | 220 | 440 | 1000 | 3600 | 4100 | gain ≥ 0.5 over | transition ≈ $3.3f_s/M$ |
|---|---|---|---|---|---|---|---|---|---|
| 9 | 1.06 | 1.06 | 1.05 | 1.02 | 0.88 | 0.073 | 0.028 | 0–1963 Hz | 5900 Hz |
| 33 | 0.96 | 0.97 | 0.99 | 1.02 | 0.61 | 0.001 | 0.001 | 0–1082 Hz | 1600 Hz |
| 513 | 0.002 | 0.50 | 1.00 | 1.00 | 0.50 | ≈0 | ≈0 | 100–1000 Hz | 103 Hz |

**As $M$ grows, the response approaches the ideal box.** The edges sharpen roughly like $1/M$, the
passband flattens (±0.3% at 513), and the stopband deepens (−10, −55 and −74 dB worst case above
2.5 kHz). **$M=9$ and $33$ are really low-pass filters:** a transition more than 1 kHz wide cannot
make an edge at 100 Hz, so DC passes with gain ≈1. This is the same resolution limit as the
$N$-point DFT in Lab 3: $M$ samples can't resolve detail finer than about $f_s/M$ Hz.

### 3C. RMS error vs the clean signal

| $M$ | 9 | 17 | **33** | 65 | 129 | 257 | **513** | 1025 | 2049 | FFT mask |
|---|---|---|---|---|---|---|---|---|---|---|
| RMS error | **0.0329** | 0.0682 | **0.0078** | 0.1218 | 0.0477 | 0.00077 | **0.00033** | 0.00077 | 0.000047 | $1.3\times10^{-13}$ |

(Bold = the lab's defaults. The clean signal's RMS is 0.568, so 0.0329 is 5.8% and 0.00033 is 0.06%.)

- **With the defaults, the error falls about 100× from $M=9$ to $513$** and approaches the ideal
  mask, though it never reaches it.
- **It is not monotonic.** $M=65$ is the worst of all.
  - The short filters are low-pass filters with gain ≈1 at 220/440 Hz, and this test signal has
    nothing below 100 Hz, so not rejecting it costs nothing.
  - At $M=65$–$129$ the 100 Hz edge exists but is 400–800 Hz wide, so it lands on the 220 Hz tone
    (gain 0.78 at $M=65$).
  - Once the transition fits in the 120 Hz gap between 100 and 220 Hz ($M\gtrsim220$), the error
    stays small: every $M\ge201$ in a sweep up to 593 was under 1%.
- The whistle leakage is ≤ $3.3\times10^{-4}$ for all $M\ge17$. The error is almost all distortion
  of the tones.
- **The metric depends on the test signal.** Add a 50 Hz hum (amplitude 0.3) and the short filters
  fail properly: 0.23 ($M=9$), 0.20 ($33$), 0.085 ($129$), 0.028 ($257$), 0.0007 ($513$).

### 3D. Listening

Component amplitudes after filtering:

| | 220 Hz | 440 Hz | 3600 Hz | 4100 Hz | whistles relative to the tone |
|---|---|---|---|---|---|
| input | 0.769 | 0.231 | 0.35 | 0.25 | −5 dB |
| $M=9$ | 0.807 | 0.236 | 0.025 | 0.007 | −30 dB |
| $M=33$ | 0.759 | 0.234 | 0.0004 | 0.0003 | −64 dB |
| $M=513$ | 0.770 | 0.231 | ≈0 | ≈0 | −83 dB |

- **$M=513$ is the best** by error.
- **$M=33$ should already sound identical to the original.**
- **$M=9$ leaves a faint whistle** (only 30 dB under the tone).
- Going up from 33 buys nothing audible here. It only costs latency of $(M-1)/2$ samples
  (16 ms at 513) and $M$ multiply-adds per sample.

### 3E. Radio with FIR filters ($f_s=60$ kHz, carriers 12/24 kHz, $B=4$ kHz)

| $M$ | delay ($M-1$ samples) | Music error | Dialogue error | crosstalk into Music |
|---|---|---|---|---|
| 9 | 0.13 ms | 3.8% | 11.3% | 3.2% |
| 33 | 0.53 ms | 2.3% | 8.6% | ≈0 |
| 65 | 1.1 ms | 0.9% | 3.8% | ≈0 |
| 129 | 2.1 ms | 0.5% | 2.3% | ≈0 |
| 513 | 8.5 ms | 0.1% | 1.1% | ≈0 |

(Errors are RMS error relative to each message's own RMS.)

- **Quality degrades for $M\lesssim33$.**
  - **$M=9$** adds junk at 8–16 kHz, which should be audible as a high hiss/garble: 86% of the
    dialogue's error energy is out of band.
    - For the dialogue, the junk is its own $2f_c=48$ kHz copy. At $f_s=60$ kHz that copy aliases to
      12 kHz, and the 9-tap low-pass passes 13% of it.
    - For the music, it is the dialogue leaking through the very wide band-pass, which passes 42% at
      20 kHz.
  - **$M=33$** has no junk, but **muffles the dialogue**: its low-pass is down to 0.76 at 3 kHz.
- **Why the dialogue suffers more:** it has 6% of its energy above 2 kHz, against 0.4% for the music
  (26% of the music is below 300 Hz).
- **Why radio needs fewer taps than denoising:** what matters is the transition width relative to
  $f_s$, and $3.3f_s/M$ must fit the gaps.
  - Radio: a 4 kHz guard gap at 60 kHz, so crosstalk is gone for $M\gtrsim25$.
  - Denoiser: a 120 Hz gap at 16 kHz, so $M\gtrsim220$.
- **The trade-off for a large $M$:**
  - **latency:** $M-1$ samples through the two filters, 8.5 ms at 513
  - **memory:** $M-1$ stored inputs
  - **computation:** $M$ multiply-adds per sample per filter, about 31 M/s at 513 taps and 60 kHz

---

## 4. Problems in the lab text

- **Typos:** "maagnitudes", "for for" (1D terms), "comptue" (1D sums), "out side" (1D intro).
- **2D question** says "values of the input response". It means the **zero-input** response.
- **2C** says to "try our previously used values and verify that the outputs match", but its cell
  hard-codes `initial = 4` while the 2A simulation defaults to `initial = 11`. The plots only match if
  you change one of them. It also silently reuses `decay`/`input_level` from whichever cell ran last
  (after the 2D cell, `decay` is 0.5).
- **Q3 intro** says the filters use "previous values of the output signal". The FIR equation
  $y[n]=\sum h[k]x[n-k]$ uses none. It also lists the inputs as $x[n-M],\dots,x[n]$, which is $M+1$
  samples, while the sum uses $M$ samples ($x[n-M+1],\dots,x[n]$).
- **1B** calls `b = [2, -1.8]` "coefficients in decreasing powers of $z$". It is really
  $B(z^{-1})=2-1.8z^{-1}$. The "decreasing powers of $z$" reading only works after padding to the
  same length as `a`, giving $2z^2-1.8z+0$, which is what `rational_parts` does. The function's
  docstring states it correctly.
- **3C** refers to "the boundary effects seen in the last exercise", but no cell shows them:
  `fir_demo(view="time")`, which plots the start-up transient and delay, is never called.

---

## 5. Key takeaways

1. **Z-transform = DTFT of the squashed signal $x[n]r^{-n}$**, with $z=re^{j\Omega}$. The unit circle
   ($r=1$) is the DTFT, or frequency response.
2. **A Z-transform is an expression *plus* an ROC.** The same $\frac{z}{z-a}$ is $a^nu[n]$ or
   $-a^nu[-n-1]$.
3. **ROCs are rings bounded by poles:** right-sided means outside, left-sided means inside, two-sided
   means a ring between poles.
4. **Stable ⇔ unit circle in the ROC. Causal ⇔ outside the outermost pole. Both ⇔ all poles inside
   $|z|=1$.**
5. **Outside the ROC the formula still gives numbers, but the series diverges** (Q1D: errors grow
   ×1.25 per term at $z=1.5$).
6. **$y[n]=ay[n-1]+x[n]$:** the mode is $a^n$. $|a|<1$ decays and $a<0$ alternates. The steady state
   is $c/(1-a)$ (final value theorem).
7. **Response = zero-input ($y_{-1}a^{n+1}$) + zero-state ($c\frac{1-a^{n+1}}{1-a}$)**, the same split
   as for CT ODEs. Dropping $y_{-1}$ from the unilateral shift rule leaves only the zero-state
   response, i.e. the transfer function $H(z)=\frac{z}{z-a}$.
8. **FIR filter = convolution with $M$ taps.** $H(z)=\sum h[k]z^{-k}$ has all its poles at 0, so it
   is always stable and causal, with a delay of $(M-1)/2$ for symmetric taps.
9. **Sharper frequency edges need more taps:** transition ≈ $3.3f_s/M$ (Hamming). The price is
   latency, memory and computation.
10. **"Better" depends on the signal and the metric.** RMS error was not monotonic in $M$, and the
    ear ranks the filters differently from RMS.

---

## 6. How to run

```powershell
D:\Jon\Uni\SYproject\embeddedSys\.venv\Scripts\Activate.ps1
cd D:\Jon\Uni\SYproject\embeddedSys\SC3102\Lab4
python -m pip install notebook        # plotly is already installed; Jupyter itself isn't
python -m notebook Lab-04-Z-transform.ipynb
```

Or open `Lab-04-Z-transform.ipynb` in VS Code and pick the `.venv` kernel. The notebook is saved
with all outputs (about 17 MB: ~7 MB is the 3D plot, which bundles plotly.js so it works offline, and
~6 MB is the radio audio), so you can read it without running anything.

Every code cell is at its **default** setting. To redo the experiments, change:

| Question | What to change |
|---|---|
| Q1 | `region` in 1B/1D |
| 2A–2D | `decay`, `initial`, `input_level` |
| Q3 | `tap_counts`, `low`, `high` |
| 3E | `radio_carriers`, `radio_paths` |

The 1C sequence plot uses whichever `region` the 1B cell last ran with (0 by default).
