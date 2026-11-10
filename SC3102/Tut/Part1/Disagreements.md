# SC3102 Tutorials 1–4: Course Method vs Practice

This file goes with `Tutorial1_Solutions.md` … `Tutorial4_Solutions.md`. Those files follow the official course method step by step.
This file has two parts:
1. **Errors / ⚠ Check:** genuine mistakes in the official solutions, or in the answer keys printed on the question sheets.
2. **Course method vs practice:** for each question where it helps, how the course wants it done, and how an engineer would actually do it or check it.

Every numerical claim here was checked in Python (numpy/scipy).

---

## Errors / ⚠ Check

All four official solution PDFs are **typed and fully legible**. No page was unreadable.

### Errors that change a result

| # | Where | What the official material says | What it should be | Why |
|---|---|---|---|---|
| 1 | **T3 Ex 3(f)**: official worked solution *and* the answer key on the question sheet | The output is non-zero on $3\le t<8$, with cases at $t=3,5,6,8$ and terms like $-\frac45(e^{-5t}-e^{-15})$ | The output is non-zero on **$5\le t<10$**. The cases are $[5,7)$, $[7,8)$, $[8,10)$, and every expression has $t$ replaced by $t-2$ (see `Tutorial3_Solutions.md`) | The input $\Pi\!\left(\frac{t-3}{2}\right)$ lives on $[2,4]$, but the official limits place the flipped box on $[t-2,t]$, which is correct only for an input on $[0,2]$. The official sketch of $x(t)$ even shows it on $[2,4]$. A numerical convolution matches the corrected version for the stated input. The official formulas match an input of $\Pi\!\left(\frac{t-1}{2}\right)$ instead |
| 2 | **T3 Ex 2(a)**: answer key on the question sheet | "Linear, time-invariant, not causal" | **Time-variant** | The equation contains $-t\,y(t)$, a coefficient that depends on time. The official *worked* solution correctly says time-variant, so only the answer key is wrong |
| 3 | **T3 Ex 3(d)**: answer key on the question sheet | $y(t)=\frac12t^3u(t)$ | $y(t)=\frac13t^3u(t)$ | $\int_0^t\tau^2d\tau=t^3/3$. The official *worked* solution gets $\frac13$, so only the answer key is wrong |

### Errors in an intermediate step (the final answer is still right)

| # | Where | Official | Correct | Why it doesn't change the answer |
|---|---|---|---|---|
| 4 | **T1 Q5(b)** | The triangle's Fourier transform is $2\,\mathrm{sinc}^2(2f)$ | $\mathrm{sinc}^2(f)$ | The given pair $\mathrm{tri}(t/T)\leftrightarrow T\mathrm{sinc}^2(fT)$ with $T=1$ gives $\mathrm{sinc}^2(f)$. At $f=0$ the transform must equal the area, which is 1, not 2. Both expressions are $\ge0$, so the conclusion ("valid autocorrelation") stands |

### Document and conceptual issues

| # | Where | Issue |
|---|---|---|
| 5 | **T3 Ex 3(f)**, official PDF | The restated question shows a different part (f), "$h(t)=u(t-3)$, $x(t)=e^{2t}u(-t)$", but the PDF then solves the $4e^{-5t}$ version from the question sheet. I added a solution for the other version: $y=\frac12e^{2(t-3)}$ for $t<3$, and $\frac12$ for $t\ge3$ |
| 6 | **T2 Q5(c)**, official PDF | It adds a part (c), "new transmitted signal", but the signal is identical to the original and no answer is given. It looks like an unfinished edit |
| 7 | **T3 Ex 2(b)**, official and answer key | It gives "impulse response $h(t)=\delta(t)+\delta(t-4)+3$" for a system it has just called **non-linear**. That is the response to $\delta(t)$, but convolving with it does not reproduce the system's output: $x*3=3\int x$, not $3$. An impulse response only fully describes **LTI** systems |

### Minor notation and labelling (results unaffected)

- **T4 Q5:** the PSD is written $|Y(f)|^2=A^2\delta(f)+\dots$. You can't square a delta. The correct statement for a periodic signal is $S_y(f)=\sum_k|C_k|^2\delta(f-kf_0)$, which gives the same expression, and the total power $A^2+B^2/2$ is right.
- **T3 Q5(b):** it writes $y[n]\le B_x$; strictly this should be $|y[n]|\le B_x$.
- **T4 Q4 (question sheet figure):** the right pulse is labelled $T$ and the left one $-T_0$. Both the official solution and mine take the spacing to be $T_0$ on both sides.

---

## Course method vs practice

The course wants the **derivation shown**, for example proving periodicity from the definition, or doing every convolution by flip and slide. That's because exams mark the reasoning.
In practice you'd use **known results**: transform tables, the properties below, and rules of thumb. You'd also **check numerically** before trusting anything.
Both approaches give the same answers; the practical one is mostly faster and easier to check.

### A small Python toolkit for checking answers

```python
import numpy as np
from scipy.integrate import quad

# 1) Numerical convolution, to check any piecewise y(t) = x*h (T3 Q4c, Ex 3f)
dt = 1e-3
t = np.arange(-2, 15, dt)
x = ((t >= 2) & (t <= 4)).astype(float)                  # Pi((t-3)/2)
h = 4*np.exp(-5*t) * ((t >= 3) & (t <= 6))
y = np.convolve(x, h) * dt                               # multiply by dt: a Riemann sum
ty = 2*t[0] + dt*np.arange(len(y))                       # time axis of the full convolution
# compare y against your piecewise formula at a few points

# 2) Numerical CT Fourier transform at one frequency (T1 Q5, T4 Q3/Q4)
def ft(xfun, f, a, b):
    re = quad(lambda s: xfun(s)*np.cos(2*np.pi*f*s), a, b)[0]
    im = quad(lambda s: -xfun(s)*np.sin(2*np.pi*f*s), a, b)[0]
    return re + 1j*im
ft(lambda s: 1 - abs(s), 0.0, -1, 1)                     # -> 1.0, so the triangle's FT is sinc^2(f), not 2 sinc^2(2f)

# 3) Fourier-series coefficients from one sampled period (T4 Q1b)
N, T0 = 4096, 3.0
tt = np.arange(N) * T0/N
Ck = np.fft.fft(np.exp(-tt)) / N                         # Ck[k] ~ C_k for small k (C_{-k} = Ck[N-k])

# 4) Spectra of a sampled sinusoid sum: single-sided amplitude = 2|X[k]|/N (T2 Q1)
```

`sympy` handles the delta integrals in T2 Q4 exactly:
`integrate(cos(pi*t)*DiracDelta(2*t-2), (t, -oo, oo))` returns $-1/2$.

### Tutorial 1

| Question | Course method | In practice | Why they differ |
|---|---|---|---|
| Q1 (a)(b) periodicity of $e^{st}$ | Assume a period $T$ and show $e^{3.1T}=1$ forces $T=0$, or that $e^{j3.1T}=1$ gives $T=2\pi n/3.1$ | Rule: $e^{st}$ is periodic **only if $s$ is purely imaginary** ($s=j\omega\ne0$), and then $T_0=2\pi/\lvert\omega\rvert$ | The course trains proof from the definition; the rule is that proof done once |
| Q1(c) $\sum g(t-3n)$ | Re-index the sum and show $T=3m$ works | "Periodic extension with spacing 3": the period is 3 by construction | Caveat: 3 is the period you can *guarantee*. A special $g$ (for example a constant) can make the true fundamental period smaller |
| Q2 sums of sinusoids | Ratio of the periods; irrational means not periodic | Quick test: if one frequency has a $\pi$ in it and another doesn't (like $20$ vs $30\pi$), the sum can't be periodic. $\cos^2$ and $\sin^2$ double the frequency | Same idea, but read off at a glance |
| Q3 energy or power | Evaluate $E$ and the $P$ limit | Classify by shape: bounded and finite length means energy signal; periodic or constant magnitude means power signal; grows without bound means neither. Numerically, `np.mean(abs(x)**2)` over longer and longer windows shows whether it settles | Shape rules are what you use to sanity-check the integrals |
| Q4 orthogonal energies | Expand $\int(x\pm y)^2$; the cross term is 0 | It's Pythagoras: $\lVert x\pm y\rVert^2=\lVert x\rVert^2+\lVert y\rVert^2$ when $\langle x,y\rangle=0$. Check with `np.dot(x, y)*dt ≈ 0` | Same maths in vector language |
| Q5 / Ex 3 valid autocorrelation | Check symmetry, a peak at 0, and a non-negative transform from the given pair | **Wiener–Khinchin**: a valid $R(\tau)$ is always some signal convolved with its own mirror image, so its transform is $\lvert X\rvert^2\ge0$. A triangle is rect $*$ rect, so it's valid; a lone rectangle has a sinc spectrum that goes negative, so it's not. Numerically: FFT the symmetric samples and look for negative values | The "convolved with its mirror" view tells you the answer without computing a transform |

### Tutorial 2

| Question | Course method | In practice | Why they differ |
|---|---|---|---|
| Q1 / Ex 1 spectra | Trig identities to turn everything into $+A\cos(\cdot+\phi)$, then Euler for the double-sided spectrum | Think in **phasors**: each term is a complex amplitude $A\angle\phi$. A sine is $\angle-90°$; a minus sign is $\angle\pm180°$. The double-sided spectrum is $\frac A2\angle\pm\phi$. Verify with `np.fft.rfft`: amplitude $=2\lvert X[k]\rvert/N$ and phase $=\angle X[k]$, provided the record holds whole cycles | Phasors are faster. The FFT check catches sign and phase slips |
| Q2 sketches | Case-by-case evaluation | Plot it: `np.maximum(t,0)-np.maximum(t-1,0)` | It only takes seconds to confirm a sketch |
| Q3 / Ex 3 singularity functions | Split into pieces, then expand $t\,u(t-a)$ algebraically into ramps and steps | **Jump-and-kink bookkeeping**: each jump of size $J$ at $a$ becomes $J\,u(t-a)$; each change of slope $\Delta m$ at $a$ becomes $\Delta m\,r(t-a)$. For Ex 3: jumps of $-1$ at 1 and $+4$ at 2; slope changes of $-1$ at 1 and $+1$ at 4. That gives $-u(t-1)+4u(t-2)-r(t-1)+r(t-4)$ in one line | The bookkeeping gives the same answer with almost no algebra |
| Q4 delta integrals | Sifting property, plus $\delta(at)=\delta(t)/\lvert a\rvert$ | Same rule; or let `sympy` do it. The general form is $\int f(t)\delta(g(t))\,dt=\sum f(t_i)/\lvert g'(t_i)\rvert$ over the roots $t_i$ of $g$ | The general form covers any argument inside the delta, not just $at-b$ |
| Q5 sampling | $F_s=2f_m=8000$ Hz, so $T_s=1/8000$ s and 480 000 samples per minute | The theorem strictly needs **$F_s>2f_m$**: a cosine at exactly $F_s/2$ can be sampled at its zero crossings and vanish. Real systems also leave a margin for the anti-aliasing filter (for example 44.1 kHz audio for a 20 kHz band). So 8 kHz is the theoretical limit; in practice you'd pick something like 10 kHz | The course asks for the boundary value; engineering adds a margin |

### Tutorial 3

| Question | Course method | In practice | Why they differ |
|---|---|---|---|
| Q1, Q2, Ex 1, Ex 2 system properties | Formal tests with $x_1$, $x_2$ and shifts | Rules of thumb: a time-dependent coefficient (like $t\,y$ or $\sin(2t)x$) means time-**variant**. An added constant or a non-linear function of $x$ or $y$ ($\lvert x\rvert$, $x^2$, $+3$) means non-linear. Any $x(t+a)$ with $a>0$ means non-causal. For an LTI system, read everything off $h$: causal if $h=0$ for $t<0$, stable if $\int\lvert h\rvert<\infty$ | Exams want the formal test; the rules tell you the expected answer before you start |
| Q2 sampling | Shows $y_o\ne y(t-t_0)$ | Sampling is **periodically** time-varying: shifting by a multiple of $T_s$ *does* commute with it. That's why it can be treated as LTI on the sample grid | Extra context that is useful for Part 2 |
| Q3 step response | Write $\Pi(t)$ as two steps, then use linearity and time invariance | Differentiate the step response: $h=g'=\delta(t)-\delta(t-2)$, so $y=x(t)-x(t-2)=\Pi(t)-\Pi(t-2)$. It's the same answer and shows causality immediately | Both are valid; $h=g'$ is the standard move |
| Q4(c), Ex 3(f) convolution | Graphical flip and slide, case by case | Check numerically with `np.convolve(x, h)*dt` (toolkit above). This is exactly how error #1 above was found. After Laplace (Step 15 in your notes): $Y(s)=X(s)H(s)$ | Graphical is good for intuition but error-prone with shifted signals. Numerical checking catches limit mistakes |
| Q5 BIBO | Find a bad bounded input (a), or bound the output directly (b) | Test $h$: the accumulator has $h=u[n]$, so $\sum\lvert h\rvert=\infty$ and it's unstable. The moving average is FIR, so $\sum\lvert h\rvert=1$ and it's stable. **Every FIR filter is stable** | The $\sum\lvert h\rvert$ test is one line |
| Q6 sinusoid through $H(\omega)$ | Expand into four complex exponentials and scale each by $H$ | **Sinusoid in, sinusoid out**: $\cos(\omega t)\to\lvert H(\omega)\rvert\cos(\omega t+\angle H(\omega))$. Here $y=\frac1{\sqrt2}\cos(t-45°)+\frac1{\sqrt{10}}\sin(3t-71.6°)$. `scipy.signal.freqs([1],[1,1],[1,3])` gives $H$ | Real form in two terms, compared with four complex terms |
| Ex 3(a)–(d) | Convolution integral with $h=u$ | $h=u$ is an **integrator**, so $y(t)=\int_{-\infty}^t x$. Each part is then a one-line integral | Recognising the system type saves setting up the integral |
| Ex 4 discrete $h[n]$ | Sum two geometric series to get $\frac47+\frac{44}{21}=\frac83<\infty$ | **Pole and ROC view** (Part 2, Step 12): the two pieces are poles at $z=\frac14$ (right-sided) and $z=2$ (left-sided). The ROC is the ring $\frac14<\lvert z\rvert<2$. It **contains the unit circle**, so the system is stable; it is **not outside the outermost pole**, so it is non-causal | The Z-transform answers both parts without summing anything |

### Tutorial 4

| Question | Course method | In practice | Why they differ |
|---|---|---|---|
| Q1(a), Ex 1 Fourier series of trig sums | Find $\omega_0$, expand with Euler, read off $C_k$ | Same. Euler *is* the fast way. Watch the indexing: $C_k$ multiplies $e^{jk\omega_0t}$, so $e^{j6t}$ with $\omega_0=2$ is $k=3$ | — |
| Q1(b) Fourier series of a piecewise signal | Integrate $\frac1{T_0}\int x\,e^{-jk\omega_0t}$ | Check with an FFT of one sampled period: `np.fft.fft(x)/N` gives $C_k$ (toolkit above) | A numerical check of the closed form |
| Q2 power via Parseval | List $C_k$ and sum $\lvert C_k\rvert^2$ | Shortcut: a complex exponential of amplitude $A$ has power $\lvert A\rvert^2$; a real sinusoid of amplitude $A$ has power $A^2/2$. So $1+\frac12+\frac12=2$, in your head | The same result as Parseval, without listing coefficients |
| Q3(b) $t e^{-\alpha t}u(t)$ | Integration by parts | Standard table entry: $t^ne^{-\alpha t}u(t)\leftrightarrow\frac{n!}{(\alpha+j2\pi f)^{n+1}}$. Or use the "multiply by $t$ ↔ differentiate in frequency" property | The course shows the derivation; practice uses the table |
| Q4 three pulses | Shift property on each pulse, plus the rect integral | Structure view: one pulse convolved with three deltas, so the transform is $\text{sinc}\times(1+2\cos2\pi fT_0)$, the familiar "array factor" | Same maths, recognised as a pattern |
| Q5 filtering | Full convolution theorem with sketches | Check which input frequencies (0, 100 Hz) fall below the cutoff (1000 Hz). All of them do, so the output equals the input. PSD: each sinusoid of amplitude $B$ puts $B^2/4$ at $\pm f_0$ | The answer follows from inspecting the frequencies; the course wants the machinery shown |
| Ex 2 sinc convolution | Duality twice, multiply the boxes, invert | Rule: two ideal low-pass filters in series act like the **narrower** one. $\frac{\sin t}{t}$ has the narrower band, so the result is $\pi\cdot\frac{\sin t}{t}$. Check with `quad` (it matches to $10^{-7}$) | The rule gives the answer immediately |
| Ex 3 staircase inverse transform | Integrate three pieces of $\frac1{2\pi}\int X e^{j\omega t}$ | Split the staircase into **two stacked boxes** (height 1 on $\lvert\omega\rvert<2$ plus height 1 on $\lvert\omega\rvert<1$). Each uses the table pair box$(\lvert\omega\rvert<W)\leftrightarrow\frac{\sin Wt}{\pi t}$, giving $\frac{\sin2t+\sin t}{\pi t}$ in one line | Linearity plus one table entry, instead of three integrals |
