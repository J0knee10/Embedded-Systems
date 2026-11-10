# SC3102 Part 2: Discrete Time, Step by Step

Written for: "I'm fine with the continuous-time half, but the discrete half confuses me."

The steps follow the Part 2 lectures in `../Slides/` in order. Each step starts with the problem
the previous step couldn't solve. Every worked example was checked numerically.

**How each step is laid out:** **Problem** (what the last tool couldn't do), then **Idea** (the fix
in one sentence), then **Formula** (with every symbol explained), then **Example** (with real
numbers), then **Takeaway**.

**Notation:**
- The slides write discrete-time frequency as ω. This guide writes **Ω** (rad/sample) to keep it
  separate from continuous-time ω (rad/s). **Ω has only one meaning**: the angle turned per
  sample, which equals $\omega/f_s$. See the box in Step 5.3.
- The slides also use **N** for two different things. This guide keeps them apart:
  - **$N_0$** is the signal's **period**. It belongs to the signal, and you **calculate** it from
    the formula (Step 3).
  - **$N$** is the **DFT size**, the number of samples you feed into the DFT. You, or the
    question, **choose** it (Steps 6–7).

---

## The roadmap

```
STEP  TOPIC                                       SLIDES                 LAB
 1    Sampling: x[n] = x_c(nT_s)                  lecture-00, Part 1     Lab 3 Q1
 2    Aliasing and Nyquist                        lecture-00, Part 2     Lab 3 Q1
 3    Discrete-signal building blocks             lecture-00, Part 3
 4    LTI systems, convolution, causal, stable    lecture-00, Parts 4-5
        └─ problem: convolution is messy → describe signals by frequency instead
 5    Complex-number toolkit                      lecture.pdf, Parts 1-2
 6    DFT:  a finite list of N numbers            lecture.pdf, Parts 3-4 Lab 3 Q2-3
 7    DTFS: a periodic signal, forever            lecture(1), Part 1
 8    Circular vs linear convolution              lecture(1), Part 2
 9    DTFT: a non-periodic signal                 lecture(1), Part 3
10    Frequency response H(Ω)                     lecture(1), Part 4     Lab 3 Q4
        └─ problem: the DTFT needs Σ|x| < ∞, and u[n] and 2^n fail that
11    Z-transform                                 lecture(2), Part 1     Lab 4 Q1
12    ROC, poles and "sides"                      lecture(2), Parts 2-3  Lab 4 Q1
13    Inverting a Z-transform                     lecture(2), Parts 3-4  Lab 4 Q1
14    Difference equations                        lecture(3)             Lab 4 Q2-3
15    Laplace + differential equations            lecture(4), lecture(5)
        └─ Steps 11-14 again, for continuous time
```

**Lecture numbers.** The slides count from 0: `lecture-00` is Lecture 0, `lecture.pdf` is 1,
`lecture(1)` is 2, `lecture(2)` is 3, `lecture(3)` is 4 (its title slide says "Lecture 4"),
`lecture(4)` is 5 and `lecture(5)` is 6. The Part 2 term test lists "Discrete Signals, DFT, Z and
Laplace Transforms", which is Lectures 0–5. That's Steps 1–15, probably without the
differential-equations half of Step 15.

**The four transforms are one idea, extended four times:**

| | Works on | Frequencies it uses | Formula | Part 1 twin |
|---|---|---|---|---|
| **DFT** (Step 6) | a list of $N$ numbers | $N$ of them, $\Omega_k=2\pi k/N$ | $X[k]=\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N}$ | — |
| **DTFS** (Step 7) | a periodic signal, period $N_0$ | the same $N$, with $N=N_0$ | same formula, valid for every $n$ | Fourier series |
| **DTFT** (Step 9) | a non-periodic signal with $\sum\lvert x\rvert<\infty$ | every $\Omega$ in $[0,2\pi)$ | $X(\Omega)=\sum_{n=-\infty}^{\infty}x[n]e^{-j\Omega n}$ | CTFT |
| **Z** (Step 11) | almost anything | $z=re^{j\Omega}$ | $X(z)=\sum x[n]z^{-n}$, plus an ROC | Laplace |

**Why the maths isn't really harder than Part 1:** continuous time uses **integrals of
exponentials**, and discrete time uses **sums of powers**. Nearly every derivation below
(DFT orthogonality, the DTFT example, every ROC, solving difference equations) uses one formula,
the geometric series:
$$\sum_{n=0}^{\infty}q^n=\frac{1}{1-q}\ \ (\text{only if }\lvert q\rvert<1),\qquad \sum_{n=0}^{N-1}q^n=\frac{1-q^N}{1-q}\ \ (q\ne1).$$

---

## Step 1: Sampling, $x[n]=x_c(nT_s)$

**Problem.** A continuous signal $x_c(t)$ has a value at every instant, which means infinitely
many values. A computer can't store them all.

**Idea.** Take a reading every $T_s$ seconds.
- $T_s$ is the **sampling period**: the time between readings.
- $f_s=1/T_s$ is the **sampling frequency**: readings per second, in Hz.

**Formula.** Reading number $n$ is taken at time $t=nT_s$. So:
$$\underbrace{x[n]}_{\text{reading number }n}=\underbrace{x_c(nT_s)}_{\text{the curve's value at the time that reading was taken}}$$
You are not replacing $t$ with anything. You're looking at the curve only at the times
$0,\,T_s,\,2T_s,\,\dots$

**Example.** $x_c(t)=\cos(2\pi t)$ (a 1 Hz cosine), with $T_s=0.25$ s, so $f_s=4$ Hz:
```
time t:      0      0.25     0.5     0.75     1.0    ...
reading n:   0       1        2        3       4     ...
x[n]:        1       0       -1        0       1     ...
```
The same result by algebra: put $t=nT_s$ in, giving $x[n]=\cos(2\pi\cdot0.25\,n)=\cos(\tfrac{\pi}{2}n)$.
The lecture's version is 1000 Hz sampled at $f_s=8000$, which gives $\cos(\pi n/4)$.

**Takeaways.**
- **Square brackets mean integers only.** There is no $x[1.5]$.
- **The seconds disappear.** The list $1,0,-1,0,\dots$ doesn't record $T_s$, so frequency is
  now measured **per sample**: $\cos(\omega t)$ becomes $\cos(\omega T_s\,n)=\cos(\Omega n)$, where
  $$\boxed{\Omega=\omega T_s=2\pi f/f_s\ \text{rad/sample}}.$$
  In the example, $\Omega=2\pi\cdot1/4=\pi/2$.

---

## Step 2: Aliasing and Nyquist

**Problem.** You know nothing about the curve between readings.

**What aliasing is.** Different frequencies can give **identical samples**. A high frequency
then disguises itself as a low one. "Alias" means a false name.

**Example** ($f_s=4$ Hz):

| Cosine | Samples $x[n]$ |
|---|---|
| 1 Hz | 1, 0, −1, 0, 1, 0, −1, 0 |
| 3 Hz | 1, 0, −1, 0, 1, 0, −1, 0 |
| 5 Hz | 1, 0, −1, 0, 1, 0, −1, 0 |
| 7 Hz | 1, 0, −1, 0, 1, 0, −1, 0 |

Between two readings, the 5 Hz wave does 1.25 cycles. Whole cycles can't be seen, so the
sampler only sees the leftover 0.25 cycle, which is exactly what a 1 Hz wave does. Car wheels
that seem to spin backwards in videos are the same effect.

**Formula.**
$$\cos\!\left(2\pi\tfrac{f+kf_s}{f_s}n\right)=\cos\!\left(2\pi\tfrac{f}{f_s}n+2\pi kn\right)=\cos\!\left(2\pi\tfrac{f}{f_s}n\right),$$
because $2\pi kn$ is a whole number of turns. **Rule of thumb:** a frequency $f$ looks like its
distance to the nearest multiple of $f_s$. So everything above $f_s/2$ folds back into
$[0,f_s/2]$.

**Why it's worse than losing information:** the disguised high frequency lands on top of a real
low frequency. Once that happens, no processing can pull them apart.

**Nyquist–Shannon theorem.** Suppose $x_c$ is **bandlimited** to $B$ Hz, meaning it has no
content above $B$. If you sample at
$$\boxed{f_s>2B},$$
the samples determine the curve **exactly**, with no loss at all. Being bandlimited isn't enough
on its own: sample too slowly and it still aliases. For example, 3 Hz sampled at 4 Hz looks like
1 Hz. In practice, an **anti-aliasing lowpass filter** removes everything above $f_s/2$ *before*
sampling.

*Lecture check:* $B=3$ kHz and $f_s=8$ kHz is fine, since $8>6$. For $B\ge4$ kHz you would need a
higher $f_s$.

---

## Step 3: Discrete-signal building blocks

**Writing a signal down.** "$x[n]=(\tfrac12)^n$ for $n\ge0$, and 0 otherwise" is the same signal as the
list $\{\dots,0,\underline{1},\tfrac12,\tfrac14,\tfrac18,\dots\}$. The underline marks $n=0$.

**Operations.**
- $x[n-2]$ is a **delay**: everything moves 2 steps to the **right**. The value that was at
  $n=0$ now appears where $n-2=0$, which is $n=2$.
- $x[n+2]$ is an **advance**: everything moves 2 steps left.
- $x[-n]$ **flips** the signal about $n=0$. Read $y[n]=x[-n]$ as "to find $y$ at $n$, look up $x$
  at $-n$". So $y[5]=x[-5]$ and $y[-5]=x[5]$, while $n=0$ stays put because it is the mirror line.

  | $n$ | −2 | −1 | **0** | 1 | 2 |
  |---|---|---|---|---|---|
  | $x[n]$ | 0 | 0 | **3** | 2 | 1 |
  | $x[-n]$ | 1 | 2 | **3** | 0 | 0 |

  **Physically, it's the recording played backwards.** A piano note that hits hard and then fades
  becomes a swell that cuts off at $n=0$. This is a mirror at $n=0$, not just reading the list in
  reverse: the reversed list lands at $n=-2,-1,0$, so the future becomes the past. You'll use it
  in convolution (Step 4), where $h[n-k]$ as a function of $k$ is "$h$ flipped, then slid right by
  $n$".

**Periodic** means $x[n+N_0]=x[n]$ for every $n$, for some positive **integer** $N_0$. The
smallest such $N_0$ is the **fundamental period**.

**Test for $\cos(\Omega_0 n+\phi)$ or $e^{j\Omega_0 n}$:**
1. Find $\Omega_0$, the number multiplying $n$.
2. Compute $\Omega_0/2\pi$.
3. If it's a fraction, the signal is periodic. Reduce it to $k/N_0$ in lowest terms; the period is the denominator $N_0$.
4. If it isn't a fraction (a leftover $\pi$ or $\sqrt{\ }$), the signal is **never** periodic.

**Why:** you need $\Omega_0N_0=2\pi k$, a whole number of turns, with $N_0$ a whole number. In
continuous time $T=2\pi/\omega$ always works because $T$ can be any real number. In discrete time
$N_0$ has to be an integer, and that's the whole difference.

| Signal | $\Omega_0/2\pi$ | Period |
|---|---|---|
| $\cos(\pi n/2)$ | $1/4$ | 4 |
| $\cos(0.4\pi n)$ | $1/5$ | 5 |
| $\cos(3\pi n/8)$ | $3/16$ | **16** (not $16/3$: 3 cycles fit in 16 samples) |
| $\cos(n)$, $\cos(0.4n)$ | $\frac{1}{2\pi}$, $\frac{1}{5\pi}$ | never periodic |

- **Sums:** the period is the lowest common multiple of the parts' periods. For example,
  $\cos(\pi n/2)+\sin(\pi n/3)$ has periods 4 and 6, so $N_0=12$. If any part is never periodic,
  the sum isn't periodic either.
- **Other signals:** check the definition directly. $u[n]$, $a^nu[n]$, and any signal with only
  finitely many nonzero samples are never periodic.
- **Sampled cosines:** $\Omega_0/2\pi=f_0/f_s$, so the samples repeat only if $f_0/f_s$ is a
  fraction (Lab 3 Q1C).

**Impulse and step.**
$$\delta[n]=\begin{cases}1&n=0\\0&\text{otherwise}\end{cases}\qquad
u[n]=\begin{cases}1&n\ge0\\0&n<0\end{cases}\qquad
\delta[n]=u[n]-u[n-1]$$

**Impulse decomposition.** You'll need this in Step 4. Any signal is a sum of shifted, scaled
impulses:
$$x[n]=\sum_k x[k]\,\delta[n-k].$$
Example: $x[-1]=1,\ x[0]=2,\ x[2]=-1$ gives $x[n]=\delta[n+1]+2\delta[n]-\delta[n-2]$. All this
says is "a list is made of its entries, each sitting at its own position."

---

## Step 4: LTI systems, convolution, causality, stability

**System.** A rule $T$ that turns an input $x[n]$ into an output $y[n]$. Example: the two-sample
average $y[n]=\tfrac12(x[n]+x[n-1])$, which smooths noise.

- **Linear:** $T\{ax_1+bx_2\}=aT\{x_1\}+bT\{x_2\}$. Here $y=2x[n]-x[n-1]$ is linear;
  $y=x[n]^2$ is not.
- **Time-invariant:** delaying the input delays the output by the same amount. Here
  $y=x[n]+x[n-1]$ is time-invariant; $y=n\,x[n]$ is not, because the same sample gets a different
  weight depending on when it arrives.

**Impulse response:** $h[n]=T\{\delta[n]\}$, the output when you poke the system with a single 1
at $n=0$.

**Convolution, derived in three lines:**
1. Write the input as a sum of impulses: $x[n]=\sum_k x[k]\delta[n-k]$ (Step 3).
2. By time invariance, each $\delta[n-k]$ produces $h[n-k]$.
3. By linearity, each $x[k]\delta[n-k]$ produces $x[k]h[n-k]$. Add them all up:
$$\boxed{y[n]=(x*h)[n]=\sum_k x[k]\,h[n-k]}$$

In words: each input sample launches its own scaled, shifted copy of $h$, and the output is all
those copies added together. **$h$ tells you everything about an LTI system.**

**Example.** The two-sample average has $h=[\tfrac12,\tfrac12]$. Take the input
$x=\delta[n]+2\delta[n-1]$:
- the sample "1" at $n=0$ launches $[\tfrac12,\tfrac12]$, starting at $n=0$
- the sample "2" at $n=1$ launches $[1,1]$, starting at $n=1$
- adding them gives $y=[\tfrac12,\ \tfrac32,\ 1]$

**Causal** (the output never depends on the future) ⇔ $h[n]=0$ for every $n<0$.

**BIBO stable** (every bounded input gives a bounded output) ⇔ $\sum_n\lvert h[n]\rvert<\infty$.
- **Why:** if $\lvert x\rvert\le M$, then
  $\lvert y[n]\rvert\le\sum_k\lvert h[k]\rvert\,\lvert x[n-k]\rvert\le M\sum_k\lvert h[k]\rvert$.
- **Stable example:** $h=(\tfrac12)^n u[n]$ sums to 2.
- **Unstable example:** $h=u[n]$, a running total, sums to ∞. Feed it $x=u[n]$ and the output
  $y[n]=n+1$ grows forever.

**The problem that drives Steps 5–10:** convolution is messy, because every output sample needs
a whole sum. Lecture 0 ends by asking whether we can break signals into different pieces. If we
break $x$ into **frequencies** instead of impulses, convolution turns into plain
**multiplication**. Steps 5–10 build up to that.

---

## Step 5: Complex-number toolkit

**Note:** "walker" below is this guide's nickname. The slides call $e^{j\Omega n}$ a **complex
exponential**, so use that name in exams.

### 5.1 A complex number is a point on a flat plane

The real part goes **across** and the imaginary part goes **up**. $e^{j\theta}$ is the point on the
circle of radius 1 at angle $\theta$, like a clock hand:
```
                  Im (up)
                    j          angle 90°  (π/2)
                    •
                    |
   angle 180° (π)   |
        -1 •--------+--------• 1     angle 0°  → Re (across)
                    |
                    •
                   -j          angle 270° (3π/2)
```
**Euler's formula**, $e^{j\theta}=\cos\theta+j\sin\theta$, says the same thing in coordinates: the
point is $\cos\theta$ across and $\sin\theta$ up.

### 5.2 Multiplying means rotating

$e^{ja}e^{jb}=e^{j(a+b)}$: multiplying **adds the angles**. That's why $j\times j=-1$: two 90°
turns make 180°, which is the point $-1$.

### 5.3 The "walker" $e^{j\Omega n}$: turn by $\Omega$ every step

| $n$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $e^{j(\pi/2)n}$ | 1 | $j$ | −1 | $-j$ | 1 |
| across part ($\cos$) | **1** | **0** | **−1** | **0** | **1** |
| up part ($\sin$) | 0 | 1 | 0 | −1 | 0 |

The across part is the sampled cosine from Step 1. **$\Omega$ is the frequency, i.e. how fast the
point spins.**
- A small $\Omega$ changes slowly.
- $\Omega=\pi$ gives $1,-1,1,-1$, the fastest possible.
- $\Omega=\pi/2+2\pi$ adds a full lap you can't see, so it looks identical to $\pi/2$. That's
  aliasing.

> **Box: Ω has one meaning, seen from four places.**
>
> **Ω = how many radians the signal turns per sample** (rad/sample).
>
> **Why "$\omega/f_s$" and "angle per step" are the same thing.** A cosine at $f$ Hz turns
> $\omega=2\pi f$ radians **per second**. Samples are $T_s=1/f_s$ seconds apart. So between one
> sample and the next it turns
> $$\Omega=\omega\times T_s=\frac{\omega}{f_s}\qquad\left(\frac{\text{rad}}{\text{s}}\times\frac{\text{s}}{\text{sample}}=\frac{\text{rad}}{\text{sample}}\right).$$
> The frequency of anything that spins is how fast its angle changes. Per second, that's $\omega$.
> Per sample, it's $\Omega$.
>
> **One example everywhere:** the 1 Hz cosine sampled at $f_s=4$ Hz (Step 1).
>
> | Where you meet $\Omega$ | What it means there | Value |
> |---|---|---|
> | Sampling (Step 1) | $\Omega=\omega/f_s=2\pi f/f_s$ | $2\pi\cdot1/4=\pi/2$ |
> | Walker $e^{j\Omega n}$ (here) | the angle turned **each step**: at $n=0,1,2,3$ the angle is $0,\ \pi/2,\ \pi,\ 3\pi/2$ | $\pi/2$ (90° per step) |
> | DFT (Step 6) | the DFT only checks $\Omega_k=2\pi k/N$ | $N=4$, $k=1$: $2\pi/4=\pi/2$ |
> | DTFT (Step 9) | a **variable**: $X(\Omega)$ checks every $\Omega$ | the only frequencies present are $\Omega=\pm\pi/2$ (a never-ending cosine strictly uses the DTFS; see 9.6) |
>
> All four rows give $\pi/2$. Same quantity, same units.
>
> **Where θ fits.** $\theta$ is just a name for *any* angle, as in $e^{j\theta}=\cos\theta+j\sin\theta$.
> In $e^{j\Omega n}$ the angle at step $n$ is
> $$\theta=\Omega\cdot n\qquad(\text{angle at step }n)=(\text{angle per step})\times(\text{number of steps}).$$
> At $n=3$ with $\Omega=\pi/2$, $\theta=3\pi/2$. **$\Omega$ is the speed of turning; $\theta$ is
> where you've got to.** Continuous time is the same: in $e^{j\omega t}$, $\omega$ is the angle per
> second and $\omega t$ is the angle at time $t$.
>
> **Why the DTFT makes Ω look like "an angle".** Until Step 9, $\Omega$ is *the* frequency of one
> particular cosine. In the DTFT, $\Omega$ becomes a variable you sweep ("how much of frequency
> $\Omega$ is in the signal, for every $\Omega$"), just as Part 1's $\cos(\omega_0t)$ has one fixed
> $\omega_0$ but $X(\omega)$ runs over every $\omega$.
>
> **Why everything repeats every 2π.** Turning $\pi/2$ per step and turning $\pi/2+2\pi$ per step
> land on exactly the same point at every sample: the extra lap is invisible. So only
> $\Omega\in[-\pi,\pi]$ matters, and $\Omega=\pi$ (half a turn per step: $+1,-1,+1,\dots$) is the
> fastest wiggle there is.
>
> **Trap:** the Part 2 slides and tutorials reuse ω. In a discrete-time formula, $X(\omega)$ or
> $X(e^{j\omega})$ means rad/**sample**, so read it as $\Omega$.

### 5.4 A cosine is two walkers spinning opposite ways

| $n$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| anticlockwise $e^{+j(\pi/2)n}$ | 1 | $j$ | −1 | $-j$ |
| clockwise $e^{-j(\pi/2)n}$ | 1 | $-j$ | −1 | $j$ |
| **average** | **1** | **0** | **−1** | **0** |

The up parts cancel and the across parts agree, so
$\cos\theta=\tfrac12\left(e^{j\theta}+e^{-j\theta}\right)$. That's why a real signal's spectrum has
**two spikes, at $\pm$ the frequency**.

**This works at every angle, not just these four.** The two walkers are mirror images across the
real axis: $\cos\theta+j\sin\theta$ and $\cos\theta-j\sin\theta$. Adding them, the up parts
$\pm\sin\theta$ always cancel. Example at $\theta=30°$: $(0.866+0.5j)+(0.866-0.5j)=1.732$, and half
of that is $0.866=\cos30°$. Each walker has an imaginary part on its own; the sum never does.

> **Add the points, not the angles.** "Adding" here means adding arrows: across parts together,
> up parts together. Adding the *angles* is what multiplication does, and
> $e^{j\theta}\cdot e^{-j\theta}=e^{0}=1$, which is not a cosine.

### 5.5 Roots of unity: $N$ evenly spaced points (pizza slices)

"Unity" means 1. The $N$th roots of unity are the numbers that give 1 when raised to the power $N$.
On the circle they're $N$ equally spaced points. For $N=4$ they are $1,\ j,\ -1,\ -j$; for example,
$j^4=(j^2)^2=(-1)^2=1$. Raising to the $N$th power multiplies the angle by $N$, which brings you to
a full lap.

$w=e^{j2\pi/N}$ is the first slice after 1. Its powers step around the slices one at a time, and
$w^N=1$. So the roots of unity are **a walker with $\Omega=2\pi/N$, which does exactly one lap in
$N$ steps**.

### 5.6 Why the DFT needs them

The DFT's building blocks must return to the start after exactly $N$ steps, so they fit the block.
Those are the walkers that step $k$ slices at a time, $g_k[n]=w^{kn}$. For $N=4$:

| $k$ | $g_k[n]$ for $n=0..3$ | Meaning |
|---|---|---|
| 0 | 1, 1, 1, 1 | constant |
| 1 | 1, $j$, −1, $-j$ | one lap anticlockwise |
| 2 | 1, −1, 1, −1 | fastest wiggle |
| 3 | 1, $-j$, −1, $j$ | one lap **clockwise**, i.e. the $-1$ walker |

$k=4$ moves a full lap each step, which is the same as not moving ($k=0$). So **only $N$ building
blocks exist**.

**A way to remember it:** the roots of unity are the $N$ marks on the circle. The DFT patterns are
the $N$ walks that **hop the same number of marks, $k$, every step**. After $N$ steps each walk has
done exactly $k$ laps, so it ends where it started. For $N=10$ the marks are 36° apart:

| $k$ | Hop | Marks it lands on | As a wave |
|---|---|---|---|
| 0 | 0° | 1 | constant |
| 1 | 36° | all 10 | 1 cycle, the slowest |
| 2 | 72° | 5 | 2 cycles |
| 3 | 108° | all 10 | 3 cycles |
| 4 | 144° | 5 | 4 cycles |
| 5 | 180° | 2 | fastest, $+1,-1,\dots$ |
| 6–9 | 216°–324° | — | $k=4,3,2,1$ running **backwards** (negative frequencies) |

Not every walk lands on every mark. $k=10$ is the same as $k=0$, so there are only 10 walks. The
backward half is why a real cosine appears at both $k$ and $N-k$ in a DFT.

**Angles wrap around:** $e^{j(\theta+2\pi)}=e^{j\theta}$. This single fact is behind aliasing
(Step 2), the DTFS having only $N$ frequencies (Step 7), and the DTFT repeating every $2\pi$
(Step 9).

---

## Step 6: DFT, a list of $N$ numbers rewritten as $N$ frequencies

**Problem.** We want to describe a signal by "how much of each frequency" instead of "the value
at each time". Start with the simplest case: a finite list of $N$ numbers.

### 6.0 Plain-English version (read this first)

**Example signal:** $x_c(t)=1+\cos(2\pi t)$, a steady offset plus a 1 Hz wobble, measured 4 times
per second.

**Samples** are the numbers you measured, the only thing the DFT is given. $N$ is how many there
are.

| reading $n$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| time | 0 s | 0.25 s | 0.5 s | 0.75 s |
| **sample $x[n]$** | **2** | **1** | **0** | **1** |

**Patterns** are not measured. They're fixed reference lists written down in advance, each one a
single pure frequency, like answer keys:

| Pattern | List | Represents |
|---|---|---|
| A: constant | $[1,1,1,1]$ | 0 Hz |
| B: one cycle | $[1,0,-1,0]$ | 1 Hz |
| C: alternating | $[1,-1,1,-1]$ | 2 Hz, the fastest 4 readings can show |

**Scoring:** line the samples up with a pattern, multiply each column, and add the results. Then
divide by the pattern's score against itself to get how much of that frequency is present.

| Pattern | Column products | Score | Pattern vs itself | Amount |
|---|---|---|---|---|
| A | $2,1,0,1$ | 4 | 4 | **1**, the "1 +" part |
| B | $2,0,0,0$ | 2 | 2 | **1**, the "$\cos(2\pi t)$" part |
| C | $2,-1,0,-1$ | 0 | 4 | **0**, not present |

From $[2,1,0,1]$ alone, the DFT recovered $1+\cos(2\pi t)$. **That is the whole job of the DFT.**
The real DFT output for these samples is $[4,2,0,2]$: the same scores, plus a mirror copy of
pattern B (5.4).

**Why complex patterns:** a sine $[0,1,0,-1]$ scores **0** against the cosine pattern, so it is
missed even though it's the same frequency. A spinning point (Step 5) holds both a cosine part and
a sine part, so scoring against it catches either shape. The **size** of the score is the
amplitude (2 for both the cosine and the sine), and its **angle** is the shift, or phase (0° for
the cosine, −90° for the sine).

**Where roots of unity come in:** the patterns must complete whole laps in exactly $N$ steps. So
they hop between $N$ evenly spaced marks on the circle, like a clock face with $N$ marks. **Those
marks are the roots of unity.** For $N=4$ they are $1, j, -1, -j$. Pattern $k$ hops $k$ marks per
step, which gives exactly $N$ patterns.

The rest of this step is the same idea in formal language.

**Idea: change the building blocks.** Normally the list $x[0],\dots,x[N-1]$ means "$x[0]$ times
the impulse at 0, plus $x[1]$ times the impulse at 1, and so on" (Step 3). The DFT describes the
same list as "$X[0]$ of frequency 0, plus $X[1]$ of frequency 1, and so on."

The frequency building blocks are the walkers from Step 5, each sampled $N$ times:
$$g_k[n]=e^{j2\pi kn/N},\qquad k=0,1,\dots,N-1.$$
$g_k$ goes round the circle $k$ times in $N$ steps:
- $k=0$ is a constant.
- $k=1$ is one cycle.
- $k=N/2$ alternates $+1,-1$, the fastest possible.

**Why these building blocks work:** they don't overlap (they are *orthogonal*).
$\langle g_k,g_l\rangle=N$ when $k=l$, and 0 otherwise. The proof is the finite geometric sum
$\frac{1-q^N}{1-q}$ with $q^N=1$, which makes it 0.

**Formulas.**
$$\underbrace{X[k]=\sum_{n=0}^{N-1}x[n]\,e^{-j2\pi kn/N}}_{\textbf{analysis: how much of frequency }k\textbf{ is in }x}
\qquad\qquad
\underbrace{x[n]=\frac1N\sum_{k=0}^{N-1}X[k]\,e^{+j2\pi kn/N}}_{\textbf{synthesis: rebuild }x\textbf{ from its frequencies}}$$
- **Analysis** has a **minus** sign. It *measures* how well $x$ matches each walker.
- **Synthesis** has a **plus** sign and a $\frac1N$. It *rebuilds* $x$.

**What bin $k$ means in real units:** $\Omega_k=2\pi k/N$ rad/sample, which is $f_k=k\,f_s/N$ Hz.
Bins above $N/2$ are the negative frequencies: $k=N-1$ means $-1$.

**$N$ is your choice, not a property of the signal.** For a finite list, $N$ is normally its
length; you can make it bigger by padding with zeros (Step 8). The bins are $f_s/N$ Hz apart, so
that's the finest detail the DFT can show, its **frequency resolution**. With $f_s=8000$ Hz,
$N=64$ gives bins every 125 Hz, and $N=8000$ gives bins every 1 Hz.

**Example.** The sampled cosine from Step 1, $x=[1,0,-1,0]$, with $N=4$:
$$X[k]=1\cdot e^{0}+(-1)\cdot e^{-j2\pi k\cdot2/4}=1-(-1)^k\quad\Rightarrow\quad X=[0,\ 2,\ 0,\ 2].$$
- There are two spikes. $k=1$ is $f=1\cdot4/4=1$ Hz, the cosine's frequency ✓. $k=3$ is
  $-1$ Hz, the cosine's second walker (Step 5, fact 3).
- Each spike has height $NA/2=4\cdot1/2=2$.
- Synthesis gives back $\tfrac14\left(2e^{j\pi n/2}+2e^{-j\pi n/2}\right)=\cos(\pi n/2)$ ✓.

**FFT:** a fast way to compute exactly the same numbers. It takes about $N\log_2N$ operations
instead of $N^2$. At $N=64$ that's 384 instead of 4096.

---

## Step 7: DTFS, periodic signals that go on forever

**Problem.** The DFT takes exactly $N$ numbers: its sum runs from $n=0$ to $N-1$, and it gives
back $N$ frequencies. Many signals don't stop after $N$ samples. Periodic signals are the easiest
of these: they go on forever, but one period holds everything.

**Idea.** A signal with period $N_0$ is fully described by one period. So take the DFT of one
period ($N=N_0$), and use the same synthesis formula for **every** $n$.

**Why that works:**
- Which walkers $e^{j\Omega n}$ repeat every $N_0$ samples? We need $\Omega N_0=2\pi k$, so
  $\Omega=2\pi k/N_0$.
- $k$ and $k+N_0$ give the same walker, because angles wrap. So **only $N_0$ different
  frequencies exist** for period $N_0$, and they are exactly the DFT's.
- The synthesis formula is therefore periodic with period $N_0$. It matches $x$ on one period, and
  both repeat, so it matches $x$ everywhere.

**Formulas:** identical to the DFT, with $N=N_0$. Any whole multiple of $N_0$ also works (7.2).
$$X[k]=\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N},\qquad x[n]=\frac1N\sum_{k=0}^{N-1}X[k]e^{j2\pi kn/N}\quad\text{for every }n.$$

**DFT vs DTFS:** the same numbers, read differently. The DFT says "here are $N$ numbers"; the
DTFS says "here is an infinite periodic signal".

**Compared with Part 1:** the continuous-time Fourier series needs infinitely many harmonics. The
DTFS needs only $N_0$, because discrete harmonics wrap around.

### 7.1 The catch: the DFT always assumes the block repeats

Put any $n$ into the synthesis formula, even outside $0..N-1$, and it gives back **copies of your
block**. Each building block $e^{j2\pi kn/N}$ does exactly $k$ whole laps in $N$ steps, so it's
back at its start at $n=N$. Anything built only from them repeats every $N$. So the DFT never
describes "these $N$ numbers and nothing else". It describes **"these $N$ numbers, repeated
forever"**, which is the DTFS reading, whether you asked for it or not.

That's harmless when the copies join up. When they don't, you get **spectral leakage**.

**Example 1: a whole cycle in the block.** $\cos(\pi n/2)$, which has $N_0=4$, with $N=4$:

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| true signal | 1 | 0 | −1 | 0 | **1** | **0** | **−1** | **0** |
| block repeated (what the DFT assumes) | 1 | 0 | −1 | 0 | **1** | **0** | **−1** | **0** |

The rows match. DFT $=[0,2,0,2]$: one spike at $k=1$ and its mirror at $k=3$. ✅

**Example 2: half a cycle in the block.** $\cos(\pi n/4)$, which has $N_0=8$, with $N=4$:

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| true signal | 1 | 0.71 | 0 | −0.71 | **−1** | **−0.71** | **0** | **0.71** |
| block repeated (what the DFT assumes) | 1 | 0.71 | 0 | −0.71 | **1** | **0.71** | **0** | **−0.71** |

From $n=4$ the rows disagree: the repeated block **jumps** from −0.71 up to 1 at the seam. The DFT
by hand, using the 4-point rows $1,-j,-1,j$:

| $k$ | Calculation | $X[k]$ | $\lvert X[k]\rvert$ |
|---|---|---|---|
| 0 | $1+0.71+0-0.71$ | $1$ | **1** |
| 1 | $1+0.71(-j)+0(-1)+(-0.71)(j)$ | $1-1.41j$ | **1.73** |
| 2 | $1-0.71+0+0.71$ | $1$ | **1** |
| 3 | conjugate of $k=1$ | $1+1.41j$ | **1.73** |

One frequency went in, but **every bin is nonzero**. The energy has leaked into all of them. ❌

**Example 3: the same cosine, a longer block.** $\cos(\pi n/4)$ with $N=8$ holds one whole cycle,
so the copies join up. DFT $=[0,4,0,0,0,0,0,4]$, clean again. ✅ **So leakage isn't a property of
the signal. It comes from the block length not matching the period.**

**Two views of why it leaks (they're the same fact):**
- **Menu view:** with $N=4$, the only frequencies the DFT has do 0, 1, 2 or 3 whole cycles per
  block. Half a cycle per block isn't on the menu, so the DFT fakes it with a mix of everything it
  has.
- **Jump view:** the repeated block jumps at every seam, and a jump needs many frequencies to
  build. That's the Part 1 square wave, which needs infinitely many harmonics because of its jump.
  Here there are only $N$ frequencies, so it uses all $N$.

**Lab 3 Q2** is the same thing at $N=64$:
- $c=5$ whole cycles gives only $k=\pm5$.
- $c=5.5$ gives 0.33 at $k=6$ and 0.30 at $k=5$, with all 64 bins nonzero.
- In Q2C, $c=0.5$ showed the jump from $x[63]\approx-1$ to $x[64]=1$.

> **Exam sentence:** The DFT treats the $N$ samples as one period of a periodic signal. If $N$
> isn't a multiple of the true period $N_0$, the repeated block has a discontinuity, so energy
> spreads into other bins (spectral leakage).

**Synthesis is never affected.** The inverse DFT always rebuilds the block exactly, whatever $N$
is (Lab 3 Q2C: error about $10^{-16}$). Leakage only makes the spectrum harder to read.

### 7.2 $N_0$ is calculated, $N$ is chosen

> **No leakage ⇔ $N$ is a whole multiple of $N_0$** ($N=N_0,\,2N_0,\,3N_0,\dots$)

The signal $\cos(\pi n/4)$ has $N_0=8$ whatever you do. Only the block length changes:

| $N$ you choose | Cycles in the block ($N/N_0$) | Result |
|---|---|---|
| 4 | 0.5 | leaks |
| 8 | 1 | clean: spikes at $k=1,7$ |
| 12 | 1.5 | leaks |
| 16 | 2 | clean: spikes at $k=2,14$ |

**Which situation you're in:**
1. **You're given a formula and asked for the DTFS.** Calculate $N_0$ (Step 3) and use $N=N_0$.
   T02 Q2(b) says exactly this: "use the fundamental periods".
2. **You're given a finite list**, like T02 Q4's $[2,-1,1,4]$. $N$ is its length, or more if you
   pad with zeros (Step 8).
3. **Measured data** (Lab 3). You choose $N$ from how much you recorded, or a power of 2 for the
   FFT, and accept some leakage.

**T02 Q2(c) is the test case.** It sets $N=12$.
- $a[n]$ has $N_0=8$, and $12/8=1.5$, so synthesis fails outside the block. It repeats $a[0]=1$
  at $n=12$, but the true $a[12]=\cos(3\pi)=-1$.
- $b[n]$ has $N_0=6$, and $12/6=2$, so synthesis recovers $b$ for every $n$.

An **aperiodic** signal has no $N_0$, so no choice of $N$ makes the repeated block equal the real
signal. That's the problem Step 9 solves.

**If you only have the samples, not the formula:** you don't need DFTs to find $N_0$. Look for the
smallest $N_0$ with $x[n+N_0]=x[n]$ by comparing the list with shifted copies of itself. With real
recordings this usually fails anyway:
- A sampled periodic signal is periodic only if $f_0/f_s$ is a fraction, and the period can be
  huge: 3.3 Hz at $f_s=16$ Hz gives $N_0=160$ (Lab 3 Q1C).
- Noise means nothing ever repeats exactly.
- With several tones, $N_0$ is the LCM of their periods.

So in practice you don't hunt for the perfect $N$. You reduce the leakage instead (7.3).

### 7.3 Two meanings of "window" (background, not in the lecture titles)

| | Window **length** ($N$ per block) | Window **shape** (fading the block's ends) |
|---|---|---|
| What it does | trades timing against frequency detail | softens the seam jump, which reduces leakage |
| Example | spectrograms of audio | the same tapering idea as Lab 4's `firwin(..., window="hamming")`, applied to a filter |

**The length tradeoff.** The bins are $f_s/N$ Hz apart (Step 6). At $f_s=8000$ Hz:

| $N$ | Block | Bin spacing | 440 Hz vs 470 Hz? | Timing |
|---|---|---|---|---|
| 8000 | 1 s | 1 Hz | separated | only "somewhere in this second" |
| 80 | 10 ms | 100 Hz | merged into one blob | to within 10 ms |

- A long block doesn't miss or cut anything. Everything in it is in the spectrum; what you lose is
  **when** it happened.
- A short block's problem is poor **frequency resolution**, not leakage as such.
- The only examinable part is the bin formula $f_k=k\,f_s/N$.

---

## Step 8: The catch with multiplying DFTs (circular convolution)

This step is Step 7's "the DFT assumes the block repeats", applied to **convolution**.

**Problem.** Convolution (Step 4) needs a whole sum for every output sample, which is slow. In
continuous time there's a shortcut: **convolution in time = multiplication in frequency**. The DFT
can be computed fast with the FFT, so we'd like to do this:
```
DFT x → X,   DFT h → H,   multiply X[k]·H[k],   inverse DFT → x*h ?
```
For two signals of length 1000, direct convolution is about $1000\times1000=10^6$ multiplications.
Three FFTs of size 2048 plus the multiplication is about 70 000. So it's worth knowing whether the
shortcut gives the right answer.

### 8.1 The answer we want: linear convolution

The lecture example is $x=[1,2,1]$ and $h=[1,1,2]$, both starting at $n=0$. Each input sample
launches a scaled copy of $h$ (Step 4):
```
n:              0   1   2   3   4
1·h  from x[0]: 1   1   2
2·h  from x[1]:     2   2   4
1·h  from x[2]:         1   1   2
---------------------------------
x*h:            1   3   5   5   2      ← 5 values
```
The output is longer than either input: its length is $L_x+L_h-1=3+3-1=5$. This is called
**linear convolution**.

### 8.2 What multiplying 3-point DFTs gives instead: $[6,5,5]$

There are only 3 values, and two of them are wrong. To see why, work out what multiplying DFTs
really computes. Start from synthesis of the product, then substitute the DFT formulas for $X$
and $H$:
$$y[n]=\frac1N\sum_k X[k]H[k]e^{+j2\pi kn/N}
=\frac1N\sum_k\Big[\sum_m x[m]e^{-j2\pi km/N}\Big]\Big[\sum_l h[l]e^{-j2\pi kl/N}\Big]e^{+j2\pi kn/N}$$
Move the $k$-sum to the inside, since only the exponentials depend on $k$:
$$y[n]=\sum_m\sum_l x[m]\,h[l]\cdot\underbrace{\frac1N\sum_{k=0}^{N-1}e^{j2\pi k(n-m-l)/N}}_{S}$$
$S$ is the finite geometric series with $q=e^{j2\pi(n-m-l)/N}$. It's the same orthogonality fact
as in Step 6:
- If **$n-m-l$ is a multiple of $N$**, then $q=1$. Every term is 1, so $S=\frac1N\cdot N=$ **1**.
- Otherwise $q\ne1$ but $q^N=1$, so the sum is $\frac{1-q^N}{1-q}=0$ and $S=$ **0**.

So $S$ just switches each pair $(m,l)$ on or off:

| | Pairs $x[m]\,h[l]$ that count towards output $n$ |
|---|---|
| **Linear** convolution | those with $m+l=n$ exactly |
| **DFT product** | those with $m+l=n$, **or $n+N$, or $n+2N$, …** |

That is the whole difference. The DFT can't tell index $n$ apart from $n+N$, because
$e^{j2\pi k(n+N)/N}=e^{j2\pi kn/N}$. The indices live on a **clock with $N$ marks**: on a 3-hour
clock, positions 3 and 4 are the same as 0 and 1.

All 9 pairs for the example:

| $m$ | $l$ | $x[m]\,h[l]$ | $m+l$ (linear slot) | $(m+l)\bmod 3$ (circular slot) |
|---|---|---|---|---|
| 0 | 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 1 | 1 |
| 0 | 2 | 2 | 2 | 2 |
| 1 | 0 | 2 | 1 | 1 |
| 1 | 1 | 2 | 2 | 2 |
| 1 | 2 | **4** | 3 | **0** ← wrapped |
| 2 | 0 | 1 | 2 | 2 |
| 2 | 1 | **1** | 3 | **0** ← wrapped |
| 2 | 2 | **2** | 4 | **1** ← wrapped |

Add up by slot:
- **Linear:** $[1,\ 1+2,\ 2+2+1,\ 4+1,\ 2]=$ **$[1,3,5,5,2]$**
- **Circular:** $[1+4+1,\ 1+2+2,\ 2+2+1]=$ **$[6,5,5]$**. These are the same sums as on the
  lecture slide.

In the launch picture, the tail at $n=3,4$ has nowhere to go, so it folds back onto $n=0,1$:
$$\text{circular}[n]=\text{linear}[n]+\text{linear}[n+N]+\text{linear}[n+2N]+\dots\qquad
[6,5,5]=[1+5,\ 3+2,\ 5].$$
The slide's formal definition says the same thing:
$$y[n]=(x\circledast_N h)[n]=\sum_{m=0}^{N-1}x[m]\,h[(n-m)\bmod N],\qquad Y[k]=X[k]H[k].$$
It's called **circular** convolution because the indices wrap around a circle. In Step 7 words: the
DFT treats both signals as repeating every $N$, so the tail of one period's output lands on the
start of the next.

### 8.3 Padding: what it does and why the size is $L_x+L_h-1$

**Padding** means adding zeros to the end of each list before the DFT, which makes $N$ bigger.
- It doesn't change the signals: they were zero there anyway.
- It just makes the clock bigger, so the output has room.

The largest slot the output uses is $(L_x-1)+(L_h-1)=L_x+L_h-2$. For nothing to wrap, that slot
must be at most $N-1$:
$$L_x+L_h-2\le N-1\quad\Longleftrightarrow\quad\boxed{N\ge L_x+L_h-1}\ \ (\text{the length of the linear result}).$$

| $N$ (pad both to) | Result | What happened |
|---|---|---|
| 3 (no padding) | $[6,5,5]$ | slots 3 and 4 wrapped onto 0 and 1 |
| 4 (one zero each) | $[3,3,5,5]$ | only slot 4 wrapped onto 0: $1+2=3$ |
| **5** $=3+3-1$ | **$[1,3,5,5,2]$** ✅ | nothing wraps |
| 8 | $[1,3,5,5,2,0,0,0]$ ✅ | correct, plus spare zeros (handy, since the FFT likes powers of 2) |

The $N=4$ row shows why the bound is exact: one slot too few and the last value folds back.

**Pad both signals to the same $N$**, because $X[k]H[k]$ multiplies bin by bin, so both DFTs need
the same bins. That means $N-L_x$ zeros on $x$ and $N-L_h$ zeros on $h$.

### 8.4 Why continuous time doesn't have this problem

It isn't really about continuous vs discrete. It's about whether the transform covers the **whole
time axis** or **one period**:

| | Continuous time | Discrete time |
|---|---|---|
| Whole time axis; a spectrum at every frequency | **CTFT**: $X\cdot H\leftrightarrow$ **linear** convolution | **DTFT** (Step 9): $X\cdot H\leftrightarrow$ **linear** convolution |
| One period; a list of frequencies | **Fourier series**: multiplying coefficients $\leftrightarrow$ **periodic** convolution over one period | **DFT/DTFS**: $X[k]H[k]\leftrightarrow$ **circular** convolution |

- The CTFT in Part 1 integrates over all $t$, so there's no block and nothing to wrap. The DTFT
  has the same property, so discrete time is fine too when you use it.
- The catch: the DTFT gives a value at **every** $\Omega$, which is infinitely many numbers. A
  computer can only store $N$ of them. That's what the DFT is: **the DTFT sampled at
  $\Omega=2\pi k/N$** (you'll see this in Step 9).
- **Sampling the spectrum makes the time signal repeat.** This is the mirror of Step 2, where
  sampling in time made the spectrum repeat (aliasing). Circular convolution is **aliasing in
  time**: copies of the output, $N$ apart, overlap.
- Padding to $N\ge L_x+L_h-1$ spaces those copies far enough apart that they don't overlap. It's
  the time-domain version of sampling faster than Nyquist.
- The continuous-time Fourier series has the same issue. Part 1 just never multiplied two sets of
  series coefficients, so it didn't come up.

### 8.5 Test practice: T02 Q4, worked

$x=[2,-1,1,4]$ and $y=[-1,0,2]$, both starting at $n=0$. Try it yourself first.

**(a) Linear convolution.** The length is $4+3-1=6$:
```
n:                0    1    2    3    4    5
2·y  from x[0]:  −2    0    4
−1·y from x[1]:        1    0   −2
1·y  from x[2]:            −1    0    2
4·y  from x[3]:                 −4    0    8
-------------------------------------------
x*y:             −2    1    3   −6    2    8
```
**(b) Inverse DFT of $X\cdot Y$ with $N=4$, without computing DFTs.** It's circular convolution:
slots 4 and 5 wrap onto 0 and 1, giving $[-2+2,\ 1+8,\ 3,\ -6]=$ **$[0,9,3,-6]$**.

**(c) How they relate:** $\text{circular}[n]=\text{linear}[n]+\text{linear}[n+4]$.

**(d) How many zeros to pad:** pad both to length $4+3-1=6$, so **two zeros on $x$ and three on
$y$**. Then nothing wraps and you get $[-2,1,3,-6,2,8]$.

**Takeaway.** Multiplying DFTs gives **circular** convolution: the linear answer wrapped onto a
clock with $N$ marks. Pad both signals to $N\ge L_x+L_h-1$ and the wrap disappears.

---

## Step 9: DTFT, non-periodic signals

**Problem.** Most signals aren't periodic: a single clap, or $(\tfrac12)^n u[n]$. They have no
$N_0$, so no block length makes "the block repeated forever" equal the real signal (7.2).

**Idea: build up from the DTFS.** Keep a block of the signal, pretend it repeats (Step 7), and take
its DTFS. Then make the block bigger and bigger. In the limit the repeats are pushed out to
infinity, and the list of $N$ frequencies becomes a continuous curve. That curve is the DTFT.

**The DTFT recipe in one line:** for each frequency $\Omega$, multiply every sample by
$e^{-j\Omega n}$ and add the results. It's the DFT's "scoring" (6.0), but against **every**
frequency instead of $N$ of them, so the answer is a **curve** $X(\Omega)$, not a list.

### 9.1 What $M$ and $N$ are on the slides (`lecture(1)`, slides 34–40)

The slides cheat one step at a time:
1. Keep only a **block** of the signal, centred on $n=0$, from **$n=-M$ to $n=+M$**.
2. **$M$ is how far you reach on each side.** **$N=2M+1$ is how many samples that keeps**: $M$ on
   the left, $M$ on the right, plus $n=0$.
3. Pretend that block repeats forever (Step 7) and take its DTFS.
4. Make $M$ bigger and watch what happens.

The signal in the plots is $x[n]=(\tfrac12)^{\lvert n\rvert}$, which decays both ways. (The slides
don't name it, but every value on the plots matches it, as the tables below show.)
```
n:          −4    −3    −2    −1    0     1     2     3     4
x[n]:      .06   .13   .25    .5    1     .5   .25   .13   .06

M = 1:                       [.5    1    .5]                       N = 3
M = 2:                 [.25   .5    1     .5   .25]                N = 5
M = 4:     [.06  .13   .25    .5    1     .5   .25   .13   .06]    N = 9
```
- **Why centred:** this signal runs both ways. Slide 33 shows that a DTFS gives the same answer
  whichever sample the block starts on, so choosing $-M\dots M$ is allowed.
- **The purple $x_N[n]$ on slide 37** is this block glued end to end: Step 7's "the DFT assumes
  the block repeats". As $M$ grows, the joins move further from $n=0$. Inside the block, the copy
  matches $x[n]$ exactly.

### 9.2 What the slide plot shows

The y-axis ("Value") is **how much of frequency $\Omega$ is in the signal**. (This signal is
symmetric, so the values are real.)

| On the plot | Formula | Meaning |
|---|---|---|
| **Solid curve** $X_M(\Omega)$ | $\sum_{n=-M}^{M}x[n]e^{-j\Omega n}$ | the DTFT formula using only the kept samples, at **every** $\Omega$ |
| **Dashed curve** $X(\Omega)$ | $\sum_{n=-\infty}^{\infty}x[n]e^{-j\Omega n}$ | the true answer using **all** samples: the DTFT |
| **Gold dots** | the DTFS of the block | the solid curve **read off at $N$ evenly spaced points**, $\Omega_k=2\pi k/N$ |

**Key fact: the DTFS values are just samples of the solid curve.** The DTFS formula is the solid
curve's formula with $\Omega$ only allowed to be $2\pi k/N$. (This is also why the DFT is "the DTFT
sampled", 8.4.)

**Worked by hand: $M=1$.** The block is $x[-1],x[0],x[1]=0.5,\ 1,\ 0.5$:
$$X_1(\Omega)=0.5\,e^{+j\Omega}+1+0.5\,e^{-j\Omega}=1+\cos\Omega\qquad(\text{Euler: }e^{j\Omega}+e^{-j\Omega}=2\cos\Omega)$$
- The **solid curve** is $1+\cos\Omega$: 2 at $\Omega=0$ and 0 at $\Omega=\pi$, matching the slide 40
  plot.
- The **gold dots** are $N=3$ points, $2\pi/3$ apart:

| $k$ | $\Omega_k$ | $X_1(\Omega_k)=1+\cos\Omega_k$ |
|---|---|---|
| 0 | 0 | **2** |
| 1 | $2\pi/3$ (120°) | $1-0.5=$ **0.5** |
| 2 | $4\pi/3$ (240°) | **0.5** |

**As $M$ grows, two things happen** (slide 38):

| $M$ | $N=2M+1$ | Dot spacing $2\pi/N$ | $X_M(0)$ | $X_M(\pi)$ |
|---|---|---|---|---|
| 1 | 3 | 120° | 2 | 0 |
| 2 | 5 | 72° | 2.5 | 0.5 |
| 4 | 9 | 40° | 2.875 | 0.375 |
| 8 | 17 | 21° | 2.992 | 0.336 |
| 20 | 41 | 9° | 3.000 | 0.333 |
| **∞** | **∞** | **0: every $\Omega$** | **3** | **1/3** |

1. **The solid curve settles onto the dashed one**, because you're adding more terms of the full
   sum. At $\Omega=0$ you're just adding samples: $1$, then $1+2(0.5)=2$, then
   $1+2(0.5+0.25)=2.5$, … heading for 3.
2. **The dots crowd together** until they fill every $\Omega$. The list of $N$ numbers becomes a
   **continuous curve**: the DTFT.

**The dashed curve in closed form**, using the geometric series twice (once for $n\ge0$, once for
$n\le-1$):
$$X(\Omega)=\sum_{n\ge0}\left(\tfrac12e^{-j\Omega}\right)^n+\sum_{n\ge1}\left(\tfrac12e^{+j\Omega}\right)^n
=\frac{1}{1-\tfrac12e^{-j\Omega}}+\frac{\tfrac12e^{j\Omega}}{1-\tfrac12e^{j\Omega}}
=\frac{0.75}{1.25-\cos\Omega}.$$
Check: at $\Omega=0$, $0.75/0.25=3$ ✓. At $\Omega=\pi$, $0.75/2.25=\tfrac13$ ✓.

### 9.3 The synthesis sum becomes an integral (slides 42–43)

DTFS synthesis has $\frac1N$ in front. The dots are $\Delta\Omega=2\pi/N$ apart, so
$\frac1N=\frac{\Delta\Omega}{2\pi}$:
$$x_N[n]=\frac1N\sum_k X_M(\Omega_k)e^{j\Omega_kn}
=\frac{1}{2\pi}\sum_k X_M(\Omega_k)e^{j\Omega_kn}\cdot\Delta\Omega
\ \xrightarrow{\ M\to\infty,\ \Delta\Omega\to0\ }\ 
\frac{1}{2\pi}\int_0^{2\pi}X(\Omega)e^{j\Omega n}\,d\Omega.$$
The middle sum is rectangles of width $\Delta\Omega$ under a curve. As the rectangles get thin, the
sum becomes an integral, exactly as in calculus. That gives the DTFT pair:
$$\boxed{X(\Omega)=\sum_{n=-\infty}^{\infty}x[n]\,e^{-j\Omega n}}\qquad\qquad
\boxed{x[n]=\frac{1}{2\pi}\int_0^{2\pi}X(\Omega)\,e^{j\Omega n}\,d\Omega}$$

**Continuous-time twin:** this is Part 1's Fourier series → Fourier transform. There you let the
period $T\to\infty$, the harmonic spacing $2\pi/T$ shrank to zero, and the list of coefficients
became a continuous $X(\omega)$. Here $N\to\infty$, the spacing $2\pi/N$ shrinks, and the DTFS list
becomes $X(\Omega)$.

**Two things to remember about $X(\Omega)$:**
- **$\Omega$ can take any value, but $X(\Omega)$ repeats every $2\pi$**, because
  $e^{-j(\Omega+2\pi)n}=e^{-j\Omega n}$ (the invisible extra lap, box in 5.3). Only $[-\pi,\pi)$
  matters. $\Omega=\pi$, the pattern $+1,-1,+1,\dots$, is the fastest a discrete signal can wiggle.
  It corresponds to $f_s/2$ in Step 2.
- **The DTFT only exists if the sum settles.** 9.6 explains when that happens.

### 9.4 Worked example 1: a short signal, $x[-1]=1,\ x[0]=2,\ x[1]=1$

**Step 1: plug the samples in.** Only three samples are nonzero, so the infinite sum has only three
terms:
$$X(\Omega)=x[-1]e^{-j\Omega(-1)}+x[0]e^{0}+x[1]e^{-j\Omega(1)}=e^{+j\Omega}+2+e^{-j\Omega}$$

**Step 2: simplify with Euler.** Since $e^{j\Omega}+e^{-j\Omega}=2\cos\Omega$:
$$X(\Omega)=2+2\cos\Omega$$

**Step 3: evaluate it at some frequencies.**

| $\Omega$ | $-\pi$ | $-3\pi/4$ | $-\pi/2$ | $-\pi/4$ | 0 | $\pi/4$ | $\pi/2$ | $3\pi/4$ | $\pi$ |
|---|---|---|---|---|---|---|---|---|---|
| $X(\Omega)$ | 0 | 0.59 | 2 | 3.41 | **4** | 3.41 | 2 | 0.59 | **0** |
| shape | ▁ | ▂ | ▄ | ▆ | █ | ▆ | ▄ | ▂ | ▁ |

It's a hump centred on $\Omega=0$ that drops to 0 at $\pm\pi$, and then **repeats every $2\pi$**.

**Step 4: read the result.**
- **$X(0)=4$** is just the sum of the samples, $1+2+1$, because $e^0=1$. It's the signal's
  overall level.
- **$X(\pi)=0$** says there's no fast wiggle. Check by scoring against the fastest pattern
  $(-1)^n$: $1\cdot(-1)+2\cdot(1)+1\cdot(-1)=0$ ✓.
- The signal is a smooth bump, so its content is **low-frequency**.

**Step 5: go back with synthesis.** You need one fact, the continuous version of Step 6's
orthogonality:
$$\int_0^{2\pi}e^{jm\Omega}\,d\Omega=\begin{cases}2\pi&m=0\\0&m\ne0\end{cases}$$
because $e^{jm\Omega}$ goes round the circle a whole number of times and cancels out.

| $n$ | $X(\Omega)\,e^{j\Omega n}$ | Terms that survive ($m=0$) | $x[n]$ |
|---|---|---|---|
| 0 | $2+e^{j\Omega}+e^{-j\Omega}$ | $2$ | $\frac{1}{2\pi}\cdot2\cdot2\pi=$ **2** ✓ |
| 1 | $2e^{j\Omega}+e^{j2\Omega}+\mathbf{1}$ | $1$ | **1** ✓ |
| 2 | $2e^{j2\Omega}+e^{j3\Omega}+e^{j\Omega}$ | none | **0** ✓ |

**Shortcut (useful in tests):** when $X(\Omega)$ is written as a sum of $e^{-j\Omega n}$ terms,
**$x[n]$ is just the number in front of $e^{-j\Omega n}$**. That's an inverse DTFT by inspection.

**Link to the DFT:** a 4-point DFT would give only this curve's values at
$\Omega=0,\ \pi/2,\ \pi,\ 3\pi/2$, which are **4, 2, 0, 2**: the "gold dots".

### 9.5 Worked example 2: an infinite signal, $x[n]=(\tfrac12)^n u[n]$

**Step 1: plug in.** Now there are infinitely many terms:
$$X(\Omega)=1+\tfrac12e^{-j\Omega}+\tfrac14e^{-j2\Omega}+\tfrac18e^{-j3\Omega}+\dots=\sum_{n\ge0}\left(\tfrac12e^{-j\Omega}\right)^n$$

**Step 2: geometric series.** The ratio is $q=\tfrac12e^{-j\Omega}$. Its size is $\tfrac12<1$, so
the sum settles:
$$X(\Omega)=\frac{1}{1-\tfrac12e^{-j\Omega}}$$

**Step 3: evaluate it.** The values are complex now.

| $\Omega$ | 0 | $\pi/4$ | $\pi/2$ | $3\pi/4$ | $\pi$ |
|---|---|---|---|---|---|
| $X(\Omega)$ | 2 | $1.19-0.65j$ | $0.8-0.4j$ | $0.69-0.18j$ | 0.667 |
| $\lvert X(\Omega)\rvert$ | **2** | 1.36 | 0.89 | 0.72 | **0.667** |
| angle | 0° | −29° | −27° | −15° | 0° |

By hand at $\Omega=\pi/2$: $e^{-j\pi/2}=-j$, so $X=\dfrac{1}{1+\tfrac12j}$. Multiply top and
bottom by $1-\tfrac12j$: $\dfrac{1-\tfrac12j}{1+\tfrac14}=\dfrac{1-0.5j}{1.25}=0.8-0.4j$.

**Step 4: read the result.**
- **$\lvert X(0)\rvert=2$** is again the sum of the samples: $1+\tfrac12+\tfrac14+\dots=2$.
- The size is biggest at low $\Omega$ and smallest at $\pi$: also **low-frequency**, which fits a
  smooth decay.
- It's **complex** this time because the signal isn't symmetric about $n=0$. The angle carries
  the timing (phase). Example 1 was symmetric, so its values were real.

**Contrast:** flip every other sign, $(-\tfrac12)^n u[n]=1,-\tfrac12,\tfrac14,-\tfrac18,\dots$ The
sizes swap ends: **0.667 at $\Omega=0$ and 2 at $\Omega=\pi$**. A zig-zag signal is
**high-frequency**.

### 9.6 When does the DTFT exist? (absolute summability)

**Start with $\Omega=0$.** Every $e^{-j\cdot0\cdot n}=1$, so the formula becomes "add up all the
samples": $X(0)=\sum_n x[n]$. $X_M(0)$ is the same sum over the kept samples $-M\dots M$.

**The DTFT is a limit.** Slide 39 defines $X(\Omega)$ as **the value $X_M(\Omega)$ settles at as
$M\to\infty$**. If the partial sums never settle on one finite number, there is nothing to call
$X(\Omega)$, and the DTFT doesn't exist.

**Two signals side by side** (keep $n=-M\dots M$ and add up the samples):

| $M$ | Sum of $(\tfrac12)^{\lvert n\rvert}$ | Sum of $u[n]$ |
|---|---|---|
| 0 | 1 | 1 |
| 1 | $0.5+1+0.5=2$ | $0+1+1=2$ |
| 2 | 2.5 | 3 |
| 4 | 2.875 | 5 |
| 100 | ≈ 3 | 101 |
| → ∞ | **settles at 3** ✓ | **keeps climbing** ✗ |

For $u[n]$, the left half of the block ($n<0$) is all zeros and the right half ($n=0\dots M$) is
all ones: $M+1$ ones, so the sum is $M+1$.
- **$(\tfrac12)^{\lvert n\rvert}$:** each new pair of samples is smaller than the last
  ($0.5,\ 0.25,\ 0.125,\dots$). The additions shrink to nothing, so the total levels off.
- **$u[n]$:** each new sample is another full 1, so the total grows forever.

`lecture(2)` slide 4 says it in one line: *"For convergence, we need the magnitudes to go to 0."*

**It isn't only $\Omega=0$.** At other frequencies $e^{-j\Omega n}$ turns each sample without
shrinking it (it always has size 1). For $u[n]$ the partial sums go:

| $\Omega$ | Partial sums as $M$ grows | Settles? |
|---|---|---|
| 0 | $1,\ 2,\ 3,\ 4,\ 5,\dots$ | ✗ grows forever |
| $\pi$ | $1,\ 0,\ 1,\ 0,\ 1,\dots$ | ✗ flips forever |
| $\pi/2$ | $1,\ 1-j,\ -j,\ 0,\ 1,\ 1-j,\dots$ | ✗ goes round in a loop forever |

There's no $\Omega$ where it settles, so **$u[n]$ has no DTFT at all**. $\Omega=0$ is just the
clearest case, because every term points the same way and nothing cancels.

**The general rule.** Each term $x[n]e^{-j\Omega n}$ has size $\lvert x[n]\rvert$, because turning
doesn't change size. If those sizes add up to a finite total, the sum settles at every $\Omega$:
$$\boxed{\sum_n\lvert x[n]\rvert<\infty}\quad(\text{"absolutely summable"})\ \Rightarrow\ \text{the DTFT exists.}$$
- $u[n]$: $1+1+1+\dots=\infty$. Fails.
- $(\tfrac12)^{\lvert n\rvert}$: the sizes add to 3. Passes.
- **Any nonzero periodic signal** fails too, because its sizes repeat forever (T01 Q1(d)). That's
  why periodic signals use the DTFS instead.

*Side note:* some textbooks give $u[n]$ a DTFT with an impulse $\delta$ at $\Omega=0$. That's an
extended version. In this course the answer is "no DTFT, because $\sum\lvert u[n]\rvert=\infty$".

**Preview of the fix (Step 11).** First multiply by $r^{-n}$ to force the samples to shrink. With
$r=1.25$, $u[n]$ becomes $(0.8)^nu[n]$. Now the sizes go to 0, and the sum settles at
$\frac{1}{1-0.8}=5$. That's `lecture(2)` slides 4–5, and it's the whole idea of the Z-transform.

### 9.7 Test practice: T02 Q3(c), worked

$x[n]=a^{-n}u[n]$ with $a=2$, i.e. $(\tfrac12)^nu[n]$. Keep only $n=0\dots N$:
$X_N(\Omega)=\sum_{n=0}^{N}x[n]e^{-j\Omega n}$. How big must $N$ be so that
$\lvert X(\Omega)-X_N(\Omega)\rvert\le0.01$ for every $\Omega$? This is the "how big must $M$
be" question from 9.2.

The error is just the dropped tail. Each dropped term has size $(\tfrac12)^n$, so:
$$\lvert X-X_N\rvert=\Big\lvert\sum_{n=N+1}^{\infty}(\tfrac12)^ne^{-j\Omega n}\Big\rvert\le\sum_{n=N+1}^{\infty}(\tfrac12)^n=(\tfrac12)^N.$$
- $N=6$: $\frac{1}{64}\approx0.016>0.01$ ✗
- $N=7$: $\frac{1}{128}\approx0.008\le0.01$ ✓, so **$N=7$, which is 8 samples** ($n=0\dots7$).

As $a\to1$ from above, the samples shrink more slowly, so you need many more of them. In general the
tail is $\frac{a^{-N}}{a-1}$. For $a=1.1$ that needs $N=73$.

**Takeaway.** The DTFT is the DTFS of a block that has grown to infinity. The dots become the
continuous curve $X(\Omega)$, which repeats every $2\pi$. It exists only when the samples' sizes
add up to something finite.

---

## Step 10: Frequency response, where LTI systems just multiply

**The payoff from Step 4.** Convolution in time becomes multiplication in frequency:
$$y=x*h\quad\Longleftrightarrow\quad Y(\Omega)=H(\Omega)\,X(\Omega).$$
$H(\Omega)$, the DTFT of $h$, is called the **frequency response**.

**Why.** Feed a single walker $x[n]=e^{j\Omega n}$ into an LTI system:
$$y[n]=\sum_m h[m]e^{j\Omega(n-m)}=e^{j\Omega n}\underbrace{\sum_m h[m]e^{-j\Omega m}}_{H(\Omega)}.$$
The same walker comes out, multiplied by the number $H(\Omega)$. $\lvert H(\Omega)\rvert$ is the
**gain** at that frequency, and $\angle H(\Omega)$ is the **phase shift**. So an LTI system works
like this: split the input into frequencies, scale each one by $H$, and add them back up.

**Example.** The two-sample average, $h=[\tfrac12,\tfrac12]$:
$$H(\Omega)=\tfrac12+\tfrac12e^{-j\Omega}=e^{-j\Omega/2}\cos(\Omega/2),\qquad\lvert H\rvert=\lvert\cos(\Omega/2)\rvert.$$
- At $\Omega=0.2\pi$ the gain is $0.95$, so low frequencies pass.
- At $\Omega=0.8\pi$ the gain is $0.31$.
- At $\Omega=\pi$ the gain is $0$: the input $x=(-1)^n$ gives $y=\tfrac12(1-1)=0$.

So averaging is a **lowpass filter**. In Lab 3 Q4 you filtered by multiplying the DFT by a mask
of 0s and 1s. That is this step.

**Same shape as 9.4.** Read worked example 1's bump as a filter, $h=[1,2,1]$. Its frequency
response has size $\lvert H(\Omega)\rvert=2+2\cos\Omega$: gain 4 at $\Omega=0$, 2 at $\pi/2$, and
0 at $\pi$. It's another lowpass filter, a weighted average. Whether $h$ sits at $n=-1\dots1$ or
$n=0\dots2$, the size is the same; shifting only adds phase.

**The problem that drives Step 11:** as 9.6 showed, the DTFT needs $\sum\lvert x\rvert<\infty$.
The step $u[n]$, growing signals like $2^n u[n]$, and the impulse response of any unstable system
all fail that test, but we still want to analyse them. Step 11 uses the $r^{-n}$ trick previewed
at the end of 9.6.

---

## Step 11: Z-transform, squash first, then DTFT

**Problem.** The DTFT only works if the samples shrink, i.e. $\sum\lvert x[n]\rvert<\infty$ (Step 9.6).
The step $u[n]$, growing signals like $2^nu[n]$, and the impulse response of every unstable system
fail this test. Step 14's difference equations produce signals like these all the time, so we need
a transform that can handle them.

### 11.1 The fix: fade the signal out before taking the DTFT

**Idea.** Multiply the signal by a fading factor $r^{-n}$ first (Step 15 calls this "squashing"), so that it shrinks. Then take the
DTFT of the faded signal, which now exists.

Take $u[n]$ with $r=1.25$, so $r^{-n}=(1/1.25)^n=0.8^n$:

| $n$ | 0 | 1 | 2 | 3 | 4 | … | 20 |
|---|---|---|---|---|---|---|---|
| $u[n]$ | 1 | 1 | 1 | 1 | 1 | … | 1 |
| fading factor $r^{-n}=0.8^n$ | 1 | 0.8 | 0.64 | 0.51 | 0.41 | … | 0.012 |
| **faded signal** $u[n]\,r^{-n}$ | 1 | 0.8 | 0.64 | 0.51 | 0.41 | … | 0.012 |

The faded signal shrinks, so its DTFT exists. At $\Omega=0$ it's $1+0.8+0.64+\dots=\frac{1}{1-0.8}=5$.

- **Nothing is lost.** You can undo the fading by multiplying by $r^{n}$ (`lecture(2)` slide 14).
- **$r$ is a dial.** $r>1$ fades the future ($n>0$). $r<1$ does the opposite: it makes the future
  bigger and fades the past ($n<0$), because $r^{-n}$ with negative $n$ is $r^{\lvert n\rvert}$.
- The slides call this **re-weighting**.

### 11.2 Two steps in one: the number $z$

The DTFT of the faded signal is
$$\sum_n x[n]\,\underbrace{r^{-n}}_{\text{fade}}\,\underbrace{e^{-j\Omega n}}_{\text{DTFT}}.$$
Use the exponent rule $a^{-n}b^{-n}=(ab)^{-n}$: $\;r^{-n}e^{-j\Omega n}=(re^{j\Omega})^{-n}$. Give
the bracket a name, $z=re^{j\Omega}$:
$$\boxed{X(z)=\sum_{n=-\infty}^{\infty}x[n]\,z^{-n}},\qquad z=re^{j\Omega}.$$

**What $z$ is.** It's a complex number, so it's a point on the plane (Step 5.1), written in polar
form:
- its **distance from 0**, $r=\lvert z\rvert$, is **how hard you fade**;
- its **angle**, $\Omega$, is **the frequency**, exactly as in the DTFT.

```
                Im
                 │          • z = r·e^{jΩ}
                 │        ╱
                 │      ╱   distance r = |z|  → how hard you fade
                 │    ╱
                 │  ╱  angle Ω               → which frequency
   ──────────────┼────────────────────── Re
                 │
   The circle |z| = 1 (r = 1, no fading) is the "unit circle".
   X(z) on the unit circle is the ordinary DTFT.
```

### 11.3 Read $z^{-n}$ as a tag: "this sample sits at position $n$"

For a finite signal, $X(z)$ is just the list of samples, each tagged with its position:

| position $n$ | −2 | −1 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| tag $z^{-n}$ | $z^{2}$ | $z^{1}$ | $1$ | $z^{-1}$ | $z^{-2}$ | $z^{-3}$ |

**Positive powers of $z$ are the past ($n<0$). Negative powers are the future.**

**Example (T03 Q2, $x_1$).** $x_1[n]=\delta[n]-3\delta[n-1]+2\delta[n-2]$ is the list $[1,-3,2]$ at
$n=0,1,2$:
$$X_1(z)=1-3z^{-1}+2z^{-2}=\frac{z^2-3z+2}{z^2}=\frac{(z-1)(z-2)}{z^2}.$$
(Multiply top and bottom by $z^2$ to get the fraction form the solutions use.)

**Going backwards is just reading tags.** T03 Q3(d) gives
$V(z)=\dots+\tfrac18z^3+\tfrac14z^2+\tfrac12z+1+\tfrac13z^{-1}+\tfrac19z^{-2}+\dots$ So
$v[-2]=\tfrac14$ (the number on $z^{2}$), $v[-1]=\tfrac12$, $v[0]=1$, $v[1]=\tfrac13$,
$v[2]=\tfrac19$.

**A delay is a multiplication by $z^{-1}$.** Shifting every sample one step later turns each tag
$z^{-n}$ into $z^{-(n+1)}=z^{-1}\cdot z^{-n}$. So
$$x[n-1]\ \leftrightarrow\ z^{-1}X(z),\qquad x[n-k]\ \leftrightarrow\ z^{-k}X(z),\qquad \delta[n-k]\ \leftrightarrow\ z^{-k}.$$
This is the property that makes Step 14 work.

### 11.4 Infinite signals: the geometric series again

**$a^nu[n]$, step by step:**
$$X(z)=\sum_{n=0}^{\infty}a^nz^{-n}=\sum_{n=0}^{\infty}(az^{-1})^n
\overset{\text{geometric}}{=}\frac{1}{1-az^{-1}}
\overset{\times z/z}{=}\frac{z}{z-a}.$$
The geometric series only settles if the ratio has size less than 1:
$\lvert az^{-1}\rvert<1\iff\lvert z\rvert>\lvert a\rvert$. **Keep that condition.** It becomes the
ROC in Step 12.

**$u[n]$** is the case $a=1$: $\;\dfrac{1}{1-z^{-1}}=\dfrac{z}{z-1}$, valid for $\lvert z\rvert>1$.

The two ways of writing it, $\frac{1}{1-az^{-1}}$ and $\frac{z}{z-a}$, are the same thing (divide top
and bottom by $z$). The slides switch between them.

**Check against Step 9.** $(\tfrac12)^nu[n]$ gives $X(z)=\frac{z}{z-1/2}$. On the unit circle at
$\Omega=\pi/2$, $z=e^{j\pi/2}=j$:
$$\frac{j}{j-\tfrac12}=\frac{j(-\tfrac12-j)}{(-\tfrac12)^2+1^2}=\frac{1-\tfrac12j}{1.25}=0.8-0.4j,$$
which is exactly the DTFT value in Step 9's example 2. **The DTFT is the Z-transform evaluated on the
unit circle.**

**Takeaway.** $X(z)=\sum x[n]z^{-n}$ is the DTFT of the faded signal. $\lvert z\rvert$ is the fading
and $\angle z$ is the frequency. For finite signals you just write the samples with their tags; for
infinite ones you use the geometric series, which only works for some $z$. Step 12 is about *which*
$z$.

---

## Step 12: ROC, which amounts of fading work

### 12.1 The question the ROC answers

The **ROC (region of convergence)** is the set of $z$ for which $\sum x[n]z^{-n}$ settles to a finite
number. In other words, it's the fading amounts $r$ that make $r^{-n}x[n]$ absolutely summable. T03
Q1(c) asks exactly this.

**Only the distance $r=\lvert z\rvert$ matters, not the angle.** Each term has size
$\lvert x[n]\rvert\,\lvert z\rvert^{-n}=\lvert x[n]\rvert\,r^{-n}$, and the angle part $e^{-j\Omega n}$
always has size 1. So if one point at distance $r$ is in the ROC, the **whole circle** of radius $r$
is. ROCs are therefore always made of whole circles: the outside of a circle, the inside of one, or
a ring. That's why this guide draws them on a **ruler** from $\lvert z\rvert=0$ to $\infty$.

### 12.2 A right-sided signal: $0.6^nu[n]$

The faded signal is $0.6^n\,r^{-n}=(0.6/r)^n$, a geometric series with ratio $0.6/r$:

| $r=\lvert z\rvert$ | ratio $0.6/r$ | actual sum | formula $\frac{z}{z-0.6}$ | works? |
|---|---|---|---|---|
| 0.5 | 1.2 | $1+1.2+1.44+\dots=\infty$ | $-5$ (meaningless) | ❌ |
| 0.6 | 1 | $1+1+1+\dots=\infty$ | blows up | ❌ |
| 1 | 0.6 | 2.5 | 2.5 | ✅ |
| 2 | 0.3 | 1.43 | 1.43 | ✅ |

**ROC: $\lvert z\rvert>0.6$.** Outside the ROC the formula still produces a number, but the sum it
came from doesn't exist (Lab 4 Q1D).

**Why it's the *outside* of a circle:** all the samples are at $n\ge0$, and for $n>0$ a bigger $r$
makes $r^{-n}$ smaller, which fades harder. So if one $r$ works, every bigger $r$ works too, and the
ROC runs from the edge all the way out to $\infty$.
```
|z|:  0 ─────────── 0.6 ═══════════════════════════► ∞
                  (edge)       ROC: |z| > 0.6
```

### 12.3 A left-sided signal: $2^nu[-n-1]$ (T03 Q1(c), $x_L$)

This signal only lives at $n=-1,-2,-3,\dots$, with values $0.5,\,0.25,\,0.125,\dots$ For negative $n$
the fading factor is $r^{-n}=r^{\lvert n\rvert}$, so **a bigger $r$ makes these samples bigger**:

| $n$ | −1 | −2 | −3 | −4 | sum |
|---|---|---|---|---|---|
| $x[n]$ | 0.5 | 0.25 | 0.125 | 0.0625 | |
| faded, $r=1$ | 0.5 | 0.25 | 0.125 | 0.0625 | 1 ✅ |
| faded, $r=3$ | 1.5 | 2.25 | 3.38 | 5.06 | ∞ ❌ |

Each faded sample is $(r/2)^{\lvert n\rvert}$, so it needs $r<2$. **ROC: $\lvert z\rvert<2$, the inside
of a circle.**

The transform, step by step. Substitute $m=-n$, so $n=-1,-2,\dots$ becomes $m=1,2,\dots$:
$$X(z)=\sum_{n=-\infty}^{-1}2^nz^{-n}=\sum_{m=1}^{\infty}2^{-m}z^{m}=\sum_{m=1}^{\infty}\left(\tfrac z2\right)^m
=\frac{z/2}{1-z/2}=\frac{z}{2-z}=-\frac{z}{z-2},\qquad\left\lvert\tfrac z2\right\rvert<1\iff\lvert z\rvert<2.$$
(A geometric series that starts at $m=1$ is $\frac{\text{first term}}{1-\text{ratio}}$.)
```
|z|:  0 ═══════════ 2 ─────────────────────────────► ∞
      ROC: |z| < 2  (edge)
```

### 12.4 The same formula can come from two different signals

Negate the left-sided example: $-2^nu[-n-1]$ has transform $+\frac{z}{z-2}$. Now compare it with the
right-sided one:

| Signal | $X(z)$ | ROC | Runs |
|---|---|---|---|
| $2^nu[n]$ | $\frac{z}{z-2}$ | $\lvert z\rvert>2$ | forward (right-sided) |
| $-2^nu[-n-1]$ | $\frac{z}{z-2}$ | $\lvert z\rvert<2$ | backward (left-sided) |

**Same formula, different signals.** So "$X(z)=\frac{z}{z-2}$" on its own is an incomplete answer. A
Z-transform is always **formula + ROC**. In general:
$$a^nu[n]\leftrightarrow\frac{z}{z-a},\ \lvert z\rvert>\lvert a\rvert
\qquad\qquad
-a^nu[-n-1]\leftrightarrow\frac{z}{z-a},\ \lvert z\rvert<\lvert a\rvert$$

### 12.5 Two-sided signals: both conditions at once, giving a ring (or nothing)

Split the signal into a right part ($n\ge0$) and a left part ($n\le-1$). Each part has its own
condition, and the ROC is where **both** hold.

**Example (T03 Q2, $x_4$):** $(\tfrac12)^nu[n]-3^nu[-n-1]$.
- The right part needs $\lvert z\rvert>\tfrac12$. The left part needs $\lvert z\rvert<3$.
- So the **ROC is $\tfrac12<\lvert z\rvert<3$**, a ring, and $X_4(z)=\frac{z}{z-1/2}+\frac{z}{z-3}$.
```
|z|:  0 ──────── ½ ═══════════════════ 3 ──────────────► ∞
                     ROC: ½ < |z| < 3
```

**Example with no ROC at all (T03 Q1(d)):** $h[n]=2^{\lvert n\rvert}$, which is
$\dots,8,4,2,\underline{1},2,4,8,\dots$
- The right part $2^nu[n]$ needs $\lvert z\rvert>2$.
- The left part (values $2,4,8,\dots$ at $n=-1,-2,-3$) is $(\tfrac12)^nu[-n-1]$, which needs
  $\lvert z\rvert<\tfrac12$.
- No $r$ is both $>2$ and $<\tfrac12$, so the **ROC is empty and there's no Z-transform.**

The reason: fading only works in one direction at a time. $r>1$ shrinks the future but enlarges the
past, and $r<1$ does the opposite. A signal that grows in *both* directions can't be tamed. The same
happens to $g[n]=2^n$ for all $n$, where the right part needs $\lvert z\rvert>2$ and the left part
needs $\lvert z\rvert<2$.

### 12.6 Finite signals: everything works

A finite list has finitely many terms, so the sum is always finite. The ROC is the **whole plane**,
except $z=0$ if there are $z^{-1}$ terms (since $1/0$ blows up) and $z=\infty$ if there are positive
powers. For example, $X_1(z)=1-3z^{-1}+2z^{-2}$ has ROC "all $z\ne0$".

**ROC shapes in one table** (`lecture(2)` slide 26):

| Signal | ROC shape | Example |
|---|---|---|
| finite | everything (maybe not 0 or ∞) | $x_1$: $z\ne0$ |
| right-sided | **outside** a circle | $0.6^nu[n]$: $\lvert z\rvert>0.6$ |
| left-sided | **inside** a circle | $2^nu[-n-1]$: $\lvert z\rvert<2$ |
| two-sided | a **ring** (or empty) | $x_4$: $\tfrac12<\lvert z\rvert<3$ |

### 12.7 Poles and zeros: where the edges come from

Most Z-transforms in this course are fractions, $X(z)=\frac{B(z)}{A(z)}$. Cancel any common factors
first, then:
- **Poles** are the values of $z$ that make the **denominator** zero. $X$ blows up there. Mark them
  **×**.
- **Zeros** are the values of $z$ that make the **numerator** zero. $X=0$ there. Mark them **○**.

**Why poles are the ROC's edges.** For $a^nu[n]\leftrightarrow\frac{z}{z-a}$, the pole is $z=a$, and
the series stops working exactly when the ratio size $\lvert a/z\rvert$ reaches 1, i.e. at
$\lvert z\rvert=\lvert a\rvert$. So:
> **The ROC never contains a pole, and its edges sit at the poles' distances from 0.**

**Worked example (T03 Q4(a)).** $F(z)=\dfrac{2z^2+2z}{z^2+2z-8}$.
1. Factor the numerator: $2z^2+2z=2z(z+1)$, so the **zeros** are $0$ and $-1$.
2. Factor the denominator: two numbers that multiply to $-8$ and add to $+2$ are $4$ and $-2$, so
   $z^2+2z-8=(z-2)(z+4)$, and the **poles** are $2$ and $-4$.
3. Pole-zero plot (everything happens to be on the real axis here):
```
                        Im
                         │
   ──────×──────────○────○──────────×──────── Re
        −4         −1    0          2
```
4. On the ruler, use each pole's **distance from 0**: $\lvert2\rvert=2$ and $\lvert-4\rvert=4$. (The
   sign doesn't matter, because the ROC only cares about $\lvert z\rvert$.)
```
|z|:  0 ───────────── 2 ───────────── 4 ───────────────► ∞
      [  ROC A  ]     ×   [ ROC B ]   ×   [  ROC C  ]
      |z| < 2             2 < |z| < 4     |z| > 4
```
With $P$ poles at different distances there are $P+1$ possible ROCs; here 2 poles give 3. T03 Q4(e)
asks whether $\lvert z\rvert=4$ can be in an ROC. It can't: there's a pole on that circle.

### 12.8 A pole is an ingredient; the ROC decides which way it runs

Each piece $\frac{z}{z-p}$ is the transform of $p^n$ running in some direction, so **each pole $p$
means the signal contains the ingredient $p^n$**:
- if $\lvert p\rvert<1$, it shrinks as $n$ increases;
- if $\lvert p\rvert>1$, it grows;
- if $p$ is negative, it flips sign every step (like $(-4)^n$).

The poles tell you *which* ingredients are in the signal. The ROC tells you *which direction* each
one runs:
> **ROC outside a pole → that ingredient runs forward: $p^nu[n]$.
> ROC inside a pole → it runs backward: $-p^nu[-n-1]$.**

So for $F(z)$ above, which turns out to be $\frac{z}{z-2}+\frac{z}{z+4}$ (Step 13 shows how):

| ROC | pole 2 runs… | pole −4 runs… | $f[n]$ | Type |
|---|---|---|---|---|
| A: $\lvert z\rvert<2$ | backward | backward | $-\left(2^n+(-4)^n\right)u[-n-1]$ | left-sided |
| B: $2<\lvert z\rvert<4$ | forward | backward | $2^nu[n]-(-4)^nu[-n-1]$ | two-sided |
| C: $\lvert z\rvert>4$ | forward | forward | $\left(2^n+(-4)^n\right)u[n]$ | right-sided |

T03 Q4(b) asks for the ROC containing the circle $r=1$ (that's A), $r=3$ (B) and $r=5$ (C). T03
Q4(c), "$f[n]=0$ for $n<0$", is C. T03 Q4(d), "two-sided", is B.

### 12.9 Causal, stable, DTFT: read them off the ruler

- **Causal** means $h[n]=0$ for $n<0$, i.e. right-sided starting at 0. So the ROC is **outside the
  outermost pole** (all the way to ∞).
- **Stable (BIBO)** means $\sum\lvert h[n]\rvert<\infty$ (Step 4). That's the DTFT condition (Step 9),
  and the DTFT lives on the unit circle. So the ROC must **contain the unit circle,
  $\lvert z\rvert=1$**. Put simply: if no fading ($r=1$) is needed, the signal was already summable.
- **The DTFT exists** under exactly the same condition: the unit circle is in the ROC.
- **Causal and stable** ⇔ the ROC is outside the outermost pole *and* contains $\lvert z\rvert=1$ ⇔
  **every pole is strictly inside the unit circle.**

**Why stability works this way, without memorising:** stable means the signal dies out at both ends,
so each ingredient must shrink **in the direction it runs**.
- A forward ingredient $p^n$ (as $n\to+\infty$) shrinks only if $\lvert p\rvert<1$.
- A backward ingredient $p^n$ (as $n\to-\infty$) shrinks only if $\lvert p\rvert>1$. For example,
  $2^n$ at $n=-1,-2,-3$ is $0.5,0.25,0.125$.

Applied to $F(z)$:

| ROC | contains $\lvert z\rvert=1$? | Causal? | Stable / has a DTFT? |
|---|---|---|---|
| A: $\lvert z\rvert<2$ | ✅ (1 < 2) | ❌ | ✅ |
| B: $2<\lvert z\rvert<4$ | ❌ | ❌ | ❌ |
| C: $\lvert z\rvert>4$ | ❌ | ✅ | ❌ |

No ROC is both causal and stable, because the poles at 2 and −4 are outside the unit circle.

**Shortcuts:**

| ROC | Signal is… |
|---|---|
| outside the outermost pole | right-sided (causal if it starts at $n\ge0$) |
| inside the innermost pole | left-sided |
| a ring between two poles | two-sided |
| contains $\lvert z\rvert=1$ | stable, and the DTFT exists |

### 12.10 T03 Q2 answers in one table

| Signal | $X(z)$ | ROC | Other ROCs for the same formula | DTFT? |
|---|---|---|---|---|
| $x_1=\delta[n]-3\delta[n-1]+2\delta[n-2]$ | $\frac{(z-1)(z-2)}{z^2}$ | $z\ne0$ | none (the only pole is at 0) | ✅ |
| $x_2=n\,u[n]$ | $\frac{z}{(z-1)^2}$ | $\lvert z\rvert>1$ | $\lvert z\rvert<1$ | ❌ (edge at 1) |
| $x_3=(-2)^nu[-n-1]$ | $-\frac{z}{z+2}$ | $\lvert z\rvert<2$ | $\lvert z\rvert>2$ | ✅ |
| $x_4=(\tfrac12)^nu[n]-3^nu[-n-1]$ | $\frac{z}{z-1/2}+\frac{z}{z-3}$ | $\tfrac12<\lvert z\rvert<3$ | $\lvert z\rvert<\tfrac12$, $\lvert z\rvert>3$ | ✅ |

For $x_3$, follow the steps of 12.3 with $(-2)$ in place of $2$: $\sum_{m\ge1}(-z/2)^m=\frac{-z/2}{1+z/2}=-\frac{z}{z+2}$.

---

## Step 13: Inverting a Z-transform (getting $x[n]$ back)

You're given $X(z)$ **and** an ROC, or a hint such as "causal", "stable" or "the circle $\lvert z\rvert=3$
is in the ROC". There are three methods (`lecture(2)` Part 4):

| Method | When to use it |
|---|---|
| **Inspection**: match a known pair | $X(z)$ is already in the table |
| **Partial fractions**: split into table pieces | $X(z)$ is a fraction with several poles (the main method) |
| **Series expansion**: read the tags | you only need the first few samples, or it's an easy series |

### 13.1 The table (from the T03 sheet)

| $x[n]$ | $X(z)$ | ROC |
|---|---|---|
| $\delta[n-k]$ | $z^{-k}$ | all $z$ (except 0 or ∞) |
| $u[n]$ | $\frac{z}{z-1}$ | $\lvert z\rvert>1$ |
| $p^nu[n]$ | $\frac{z}{z-p}=\frac{1}{1-pz^{-1}}$ | $\lvert z\rvert>\lvert p\rvert$ |
| $-p^nu[-n-1]$ | $\frac{z}{z-p}$ | $\lvert z\rvert<\lvert p\rvert$ |
| $p^{n-1}u[n-1]$ | $\frac{1}{z-p}$ | $\lvert z\rvert>\lvert p\rvert$ |
| $-p^{n-1}u[-n]$ | $\frac{1}{z-p}$ | $\lvert z\rvert<\lvert p\rvert$ |
| $n\,p^nu[n]$ | $\frac{pz}{(z-p)^2}$ | $\lvert z\rvert>\lvert p\rvert$ |
| $\rho^n\cos(\Omega_0n)\,u[n]$ | $\frac{z(z-\rho\cos\Omega_0)}{z^2-2\rho\cos\Omega_0\,z+\rho^2}$ | $\lvert z\rvert>\rho$ |
| $\rho^n\sin(\Omega_0n)\,u[n]$ | $\frac{\rho\sin\Omega_0\,z}{z^2-2\rho\cos\Omega_0\,z+\rho^2}$ | $\lvert z\rvert>\rho$ |

**Where $\frac{1}{z-p}$ comes from:** $\frac{1}{z-p}=z^{-1}\cdot\frac{z}{z-p}$, and $z^{-1}$ means
"delay by one" (11.3). So it's $p^nu[n]$ delayed by one step, which is $p^{n-1}u[n-1]$.

**Properties:**

| Property | Time | $z$ | ROC |
|---|---|---|---|
| linearity | $ax[n]+bh[n]$ | $aX(z)+bH(z)$ | at least the overlap |
| shift | $x[n-k]$ | $z^{-k}X(z)$ | same (maybe ±0 or ∞) |
| convolution | $(x*h)[n]$ | $X(z)H(z)$ | at least the overlap |
| time reversal | $x[-n]$ | $X(1/z)$ | flipped: $r\to1/r$ |
| multiply by $a^n$ | $a^nx[n]$ | $X(z/a)$ | scaled by $\lvert a\rvert$ |

The last property is the fading idea again: $\sum a^nx[n]z^{-n}=\sum x[n](z/a)^{-n}=X(z/a)$.

### 13.2 Inspection, example 1: the cosine pair (T03 Q3(a))

$X(z)=\dfrac{z^2}{z^2+1/4}$, $\lvert z\rvert>\tfrac12$. Match it to the cosine pair term by term:
1. **Denominator:** $z^2-2\rho\cos\Omega_0\,z+\rho^2$ should equal $z^2+0\cdot z+\tfrac14$.
   - There's no $z$ term, so $\cos\Omega_0=0$, which gives $\Omega_0=\pi/2$.
   - $\rho^2=\tfrac14$, so $\rho=\tfrac12$.
2. **Check the numerator:** $z(z-\rho\cos\Omega_0)=z(z-0)=z^2$ ✓.
3. **Answer:** $x[n]=(\tfrac12)^n\cos(\tfrac{\pi}{2}n)\,u[n]=1,\ 0,\ -\tfrac14,\ 0,\ \tfrac1{16},\dots$

**Check by series:** $\frac{z^2}{z^2+1/4}=\frac{1}{1+\frac14z^{-2}}=1-\tfrac14z^{-2}+\tfrac1{16}z^{-4}-\dots$
Reading the tags gives $1,0,-\tfrac14,0,\tfrac1{16}$ ✓.

**What the poles mean here:** $z^2+\tfrac14=0$ gives $z=\pm\tfrac j2=\tfrac12e^{\pm j\pi/2}$. That's
a **pair of complex poles**: their distance $\tfrac12$ is the **decay** $\rho$, and their angle
$\pm\pi/2$ is the **frequency** $\Omega_0$. A complex pole $p=\rho e^{j\Omega_0}$ gives the ingredient
$p^n=\rho^ne^{j\Omega_0n}$, a spinning point (Step 5) that shrinks. The pair together makes a
decaying cosine.

### 13.3 Inspection, example 2: undoing the fading (T03 Q1(b))

You're told that $X(3e^{j\Omega})=\dfrac{1}{1-\frac j2e^{-j\Omega}}$, with $\lvert z\rvert=3$ in the ROC.
1. $X$ on the circle $r=3$ is the DTFT of the faded signal $w[n]=3^{-n}x[n]$ (11.2).
2. DTFT pair: $a^nu[n]\leftrightarrow\frac{1}{1-ae^{-j\Omega}}$ for $\lvert a\rvert<1$. Here
   $a=\tfrac j2$, so $w[n]=(\tfrac j2)^nu[n]$.
3. Undo the fading: $x[n]=3^n\,w[n]=(\tfrac{3j}{2})^nu[n]$.

### 13.4 Partial fractions, the main method

**Why it's needed:** $\frac{2z^2+2z}{z^2+2z-8}$ isn't in the table, but it's a **sum** of two
fractions that are. Partial fractions find that sum.

**Recipe**
1. **Factor the denominator** to get the poles.
2. **Choose the form:**
   - If the numerator has a factor $z$, **divide $X(z)$ by $z$ first**. The pieces then come out as
     $c\,\frac{z}{z-p}$, which match $p^n$ directly.
   - Otherwise, split $X(z)$ directly into $\frac{c}{z-p}$ pieces and use the delayed pair
     $p^{n-1}$.
3. **Find each $c$ by "cover-up":** multiply both sides by $(z-p)$, then set $z=p$. All the other
   pieces vanish.
4. **Draw the ruler** and pick the ROC (it's given, or follows from "causal", "stable" or "contains
   the circle $r$").
5. **Invert each piece:** if the ROC is outside $\lvert p\rvert$ it runs forward; if inside, backward
   (12.8).
6. **Sanity check:** compute $x[0]$ and $x[1]$ another way (13.5) and compare.

**Worked example A: T03 Q4 (the numerator has a factor $z$).**
$F(z)=\dfrac{2z(z+1)}{(z-2)(z+4)}$.
1. Poles: $2$ and $-4$.
2. Divide by $z$: $\dfrac{F(z)}{z}=\dfrac{2(z+1)}{(z-2)(z+4)}=\dfrac{C}{z-2}+\dfrac{D}{z+4}$.
3. Cover-up:
   - **For $C$:** multiply both sides by $(z-2)$, giving
     $\frac{2(z+1)}{z+4}=C+\frac{D(z-2)}{z+4}$. At $z=2$ the $D$ term is 0, so
     $C=\frac{2(3)}{6}=1$.
   - **For $D$:** multiply by $(z+4)$, giving $\frac{2(z+1)}{z-2}=\frac{C(z+4)}{z-2}+D$. At $z=-4$,
     $D=\frac{2(-3)}{-6}=1$.
   - Multiply back by $z$: $\;F(z)=\dfrac{z}{z-2}+\dfrac{z}{z+4}$. (Note that $z+4=z-(-4)$, so that
     pole is $p=-4$.)
4. & 5. The three ROCs give the three answers in the 12.8 table.
6. **Check (ROC C, causal):** the formula gives $f[0]=1+1=2$ and $f[1]=2+(-4)=-2$. Running the
   division $\frac{2z^2+2z}{z^2+2z-8}$ in powers of $z^{-1}$ gives $2-2z^{-1}+20z^{-2}-\dots$ ✓.

**Worked example B: T03 Q3(b) (no factor $z$ in the numerator).**
$A(z)=\dfrac{3z-7}{z^2-5z+6}$, $\lvert z\rvert>3$.
1. $z^2-5z+6=(z-2)(z-3)$, so the poles are 2 and 3.
2. Split directly: $A(z)=\dfrac{C}{z-2}+\dfrac{D}{z-3}$.
3. Cover-up:
   - $C$: multiply by $(z-2)$ and set $z=2$, giving $C=\frac{3(2)-7}{2-3}=\frac{-1}{-1}=1$.
   - $D$: multiply by $(z-3)$ and set $z=3$, giving $D=\frac{3(3)-7}{3-2}=2$.
   - So $A(z)=\dfrac{1}{z-2}+\dfrac{2}{z-3}$.
4. The ROC $\lvert z\rvert>3$ is outside both poles, so both pieces run forward.
5. Using $\frac{1}{z-p}\leftrightarrow p^{n-1}u[n-1]$:
   $\;a[n]=\left(2^{n-1}+2\cdot3^{n-1}\right)u[n-1]=0,\ 3,\ 8,\ 22,\dots$
6. **Check:** dividing $3z-7$ by $z^2-5z+6$ gives $3z^{-1}+8z^{-2}+\dots$, so $a[1]=3$ and $a[2]=8$ ✓.

**Worked example C: from `lecture(3)`.** Here $H(z)=\dfrac{z^2}{(z-\frac12)(z-2)}$, which comes from
$y[n]-\tfrac52y[n-1]+y[n-2]=x[n]$. Dividing by $z$ gives
$H(z)=-\tfrac13\frac{z}{z-1/2}+\tfrac43\frac{z}{z-2}$:

| ROC | $h[n]$ | Sided | Causal? | Stable? |
|---|---|---|---|---|
| $\lvert z\rvert>2$ | $\left(\tfrac43 2^n-\tfrac13(\tfrac12)^n\right)u[n]$ | right | ✅ | ❌ ($2^n$ blows up) |
| $\tfrac12<\lvert z\rvert<2$ | $-\tfrac13(\tfrac12)^n u[n]-\tfrac43 2^n u[-n-1]$ | two | ❌ | ✅ |
| $\lvert z\rvert<\tfrac12$ | $\left(\tfrac13(\tfrac12)^n-\tfrac43 2^n\right)u[-n-1]$ | left | ❌ | ❌ |

Running the recurrence directly gives $h=1,\ 2.5,\ 5.25,\ 10.625,\dots$, which matches the causal row.
**Lab 4 Q1** is the same exercise with poles at 0.6 and 1.2.

> **Step 14 does partial fractions in $z^{-1}$ form**, e.g. $\frac{2}{1-z^{-1}}-\frac{1}{1-\frac12z^{-1}}$.
> That's the same pieces written differently, since $\frac{1}{1-pz^{-1}}=\frac{z}{z-p}$.

### 13.5 Series expansion: read the tags

**Idea.** Write $X(z)$ as a power series, then read $x[n]$ as the number on $z^{-n}$ (11.3).

**The ROC tells you which way to expand:**
- **Outside** ($\lvert z\rvert>\dots$) means right-sided: expand in powers of $z^{-1}$.
- **Inside** ($\lvert z\rvert<\dots$) means left-sided: expand in powers of $z$.

**Worked example (T03 Q3(c)).** $Y(z)=\dfrac{2+z^{-1}}{1-\frac12z^{-1}}$, $\lvert z\rvert>\tfrac12$,
and you want $y[1],y[2],y[3]$.
1. The ROC is outside, so expand in $z^{-1}$. Inside the ROC $\lvert\tfrac12z^{-1}\rvert<1$, so the
   geometric series works:
   $\;\frac{1}{1-\frac12z^{-1}}=1+\tfrac12z^{-1}+\tfrac14z^{-2}+\tfrac18z^{-3}+\dots$
2. Multiply by $(2+z^{-1})$ and collect each power:

| power | from $2\times$ series | from $z^{-1}\times$ series | total $=y[n]$ |
|---|---|---|---|
| $z^{0}$ | 2 | — | **$y[0]=2$** |
| $z^{-1}$ | 1 | 1 | **$y[1]=2$** |
| $z^{-2}$ | $\tfrac12$ | $\tfrac12$ | **$y[2]=1$** |
| $z^{-3}$ | $\tfrac14$ | $\tfrac14$ | **$y[3]=\tfrac12$** |

The solutions get the same numbers by long division. The geometric-series route is easier whenever
the denominator looks like $1-az^{-1}$.

**Slide example of both directions** (`lecture(2)` slides 47–48): $\frac{z^2}{z-3}$ gives
$3^{n+1}u[n+1]$ for $\lvert z\rvert>3$, but $-3^{n+1}u[-n-2]$ for $\lvert z\rvert<3$. The same formula
expanded in different directions gives different signals, which is 12.4 again.

### 13.6 The whole Z-transform workflow

```
 signal x[n] ──(sum Σ x[n]z⁻ⁿ; geometric series)──► formula X(z) + ROC
                                                       │
 x[n] ◄──(invert each piece using the ROC)── ruler ◄──(factor; poles, zeros; partial fractions)
```
- **The ROC is never optional.** Without it you can't tell forward from backward.
- **Unit circle in the ROC** ⇔ stable ⇔ the DTFT exists.
- **Outside the outermost pole** ⇔ right-sided (causal).

---

## Step 14: Difference equations

### 14.1 A difference equation is a recipe a computer runs

$y[n]=\tfrac12y[n-1]+x[n]$, with $y[-1]=1$ and $x[n]=u[n]$:
$$y[0]=\tfrac12(1)+1=1.5,\quad y[1]=\tfrac12(1.5)+1=1.75,\quad y[2]=1.875,\ \dots\to 2$$
There's no calculus here. It's a loop, which is why real DSP chips use these. The Z-transform
gives you the **closed form** for $y[n]$, so you don't have to run the loop.

### 14.2 Delays become $z^{-1}$, and initial conditions need the unilateral transform

When there are **initial conditions**, use the **unilateral** transform
$Y_+(z)=\sum_{n\ge0}y[n]z^{-n}$. Its shift rule picks up the stored value:
$$\sum_{n\ge0}y[n-1]z^{-n}=\underbrace{y[-1]}_{n=0\text{ term}}+\sum_{n\ge1}y[n-1]z^{-n}=y[-1]+z^{-1}Y_+(z).$$
For a two-step delay: $y[n-2]\to z^{-2}Y_++z^{-1}y[-1]+y[-2]$.

### 14.3 Fully worked: $y[n]-\tfrac12y[n-1]=u[n]$, $y[-1]=1$ (lecture 3's running example)

1. **Transform both sides:** $Y_+-\tfrac12\left(z^{-1}Y_++1\right)=\dfrac{1}{1-z^{-1}}$
2. **Collect the $Y_+$ terms:** $Y_+\left(1-\tfrac12z^{-1}\right)=\tfrac12+\dfrac{1}{1-z^{-1}}$
3. **Split by cause:**
$$Y_+=\underbrace{\frac{1/2}{1-\tfrac12z^{-1}}}_{\text{from }y[-1]\text{: zero-input}}+\underbrace{\frac{1}{(1-\tfrac12z^{-1})(1-z^{-1})}}_{\text{from the input: zero-state}}$$
4. **Partial fractions:** $\dfrac{1}{(1-\tfrac12z^{-1})(1-z^{-1})}=\dfrac{2}{1-z^{-1}}-\dfrac{1}{1-\tfrac12z^{-1}}$
5. **Invert** (right-sided, $n\ge0$):
$$y_{zi}[n]=(\tfrac12)^{n+1},\qquad y_{zs}[n]=2-(\tfrac12)^n,\qquad y[n]=2-(\tfrac12)^{n+1}$$

This gives $1.5,\ 1.75,\ 1.875,\dots$, the same as the loop in 14.1.

### 14.4 Three ways to split the output (they're different splits)

| Split | Based on | In the example |
|---|---|---|
| zero-input + zero-state | **cause:** initial memory vs the input | $(\tfrac12)^{n+1}$ + $\left[2-(\tfrac12)^n\right]$ |
| transient + steady-state | **time:** dies out vs persists | $-(\tfrac12)^{n+1}$ + $2$ |
| homogeneous + particular | **maths:** solves the "$=0$" equation vs one particular solution | $C(\tfrac12)^n$ + $2$ |

- A system described by a difference equation is **LTI only if its initial conditions are zero**.
  Otherwise a zero input still gives a nonzero output (the zero-input response), which breaks
  linearity.
- **Initial value theorem:** $y[0]=\lim_{z\to\infty}Y_+(z)$. Here every $z^{-1}\to0$, giving
  $\tfrac12+1=\tfrac32$ ✓.
- **Final value theorem:** $y[\infty]=\lim_{z\to1}(1-z^{-1})Y_+(z)$. It's valid only if all poles
  are inside the unit circle, except at most one simple pole at $z=1$. Here it gives 2 ✓.

### 14.5 FIR vs IIR (Lab 4 Q3)

- **IIR (with feedback; $y$ appears on the right-hand side):** $y[n]=a\,y[n-1]+x[n]$ has
  $h[n]=a^n u[n]$, which never ends. The pole is at $a$, so it's stable only if $\lvert a\rvert<1$.
- **FIR (no feedback):** $y[n]=\sum_{k=0}^{M-1}h[k]\,x[n-k]$. The impulse response *is* the list
  of coefficients. $H(z)=\sum h[k]z^{-k}$ has every pole at $z=0$, so it's **always causal and
  stable**. The cost: you need many taps $M$ to get close to an ideal filter, and more taps means
  more memory, more computation and more delay.

**Recipe: solve a difference equation with initial conditions**
1. Take the unilateral Z-transform of both sides, using the shift rule from 14.2.
2. Solve for $Y_+$. Terms involving $y[-1],y[-2]$ form the zero-input response; terms involving
   $X_+$ form the zero-state response.
3. Do partial fractions, then invert with the right-sided pairs (all for $n\ge0$).
4. **Sanity check:** compute $y[0]$ and $y[1]$ by hand from the equation and compare.

---

## Step 15: Laplace and differential equations, Steps 11–14 again for continuous time

`lecture(4).pdf` and `lecture(5).pdf` have almost the same slide titles as `lecture(2)` and
`lecture(3)`. Every idea carries over:

| Discrete time (Z) | Continuous time (Laplace) |
|---|---|
| squash by $r^{-n}$ | squash by $e^{-\sigma t}$ |
| $z=re^{j\Omega}$ | $s=\sigma+j\omega$ |
| $X(z)=\sum x[n]z^{-n}$ | $X(s)=\int x(t)e^{-st}dt$ |
| ROC depends on $\lvert z\rvert$, so it's rings | ROC depends on $\mathrm{Re}\,s=\sigma$, so it's vertical strips |
| unit circle = DTFT | $j\omega$-axis = CTFT |
| right-sided: outside the outermost pole | right-sided: to the right of the rightmost pole |
| $a^n u[n]\leftrightarrow\frac{z}{z-a}$, $\lvert z\rvert>\lvert a\rvert$ | $e^{-at}u(t)\leftrightarrow\frac{1}{s+a}$, $\mathrm{Re}\,s>-a$ |
| causal + stable ⇔ poles inside the unit circle | causal + stable ⇔ poles in the left half-plane |
| delay $y[n-1]\leftrightarrow z^{-1}Y$ | derivative $y'(t)\leftrightarrow sY$ |
| unilateral: $y[n-1]\to z^{-1}Y_++y[-1]$ | unilateral: $y'\to sY-y(0^-)$ |
| difference equation | differential equation |

**The link between them:** $z=e^{sT_s}$ (the lecture uses $T_s=1$, so $z=e^s$). If $\sigma<0$
then $\lvert z\rvert=e^{\sigma T_s}<1$. So the left half-plane maps to the inside of the unit
circle, and sampling $e^{-at}$ gives $(e^{-aT_s})^n$, which is a power $p^n$.

**Twin examples:**

| | Discrete (lecture 3) | Continuous (lecture 5) |
|---|---|---|
| Equation | $y[n]-\tfrac12y[n-1]=u[n]$, $y[-1]=1$ | $y'+y=2u(t)$, $y(0^-)=1$ |
| Zero-input | $(\tfrac12)^{n+1}$ | $e^{-t}$ |
| Zero-state | $2-(\tfrac12)^n$ | $2-2e^{-t}$ |
| Total | $2-(\tfrac12)^{n+1}\to2$ | $2-e^{-t}\to2$ |

They have the same shape, with $e^{-t}$ replaced by $(\tfrac12)^n$.

---

## Self-check (answers hidden)

<details><summary>1. (Step 2) At f_s = 10 Hz, what frequency does a 12 Hz cosine look like?</summary>

2 Hz. The nearest multiple of 10 is 10, and $12-10=2$.
</details>

<details><summary>2. (Step 4) Is y[n] = x[n²] linear? Time-invariant?</summary>

It's linear: scaling or adding inputs scales or adds the outputs. It's not time-invariant: delaying
the input doesn't simply delay the output, because the system reads the input at index $n^2$. This
is from the lecture.
</details>

<details><summary>3. (Step 4) Is h[n] = 0.9ⁿ u[n] causal? Stable?</summary>

It's causal, because it's zero for $n<0$. It's stable, because $\sum0.9^n=\frac{1}{1-0.9}=10<\infty$.
</details>

<details><summary>4. (Step 6) What is the DFT of [1, 1, 1, 1]? What does it mean?</summary>

$[4,0,0,0]$. A constant signal is pure frequency 0. $X[0]$ is the sum of the samples.
</details>

<details><summary>5. (Step 7) With N = 8, which leaks: cos(πn/2) or cos(3πn/8)?</summary>

- $\cos(\pi n/2)$: $\Omega_0/2\pi=1/4$, so $N_0=4$. $8/4=2$ whole cycles, so it's **clean**:
  $\lvert X\rvert=[0,0,4,0,0,0,4,0]$, spikes at $k=2$ and $6$.
- $\cos(3\pi n/8)$: $\Omega_0/2\pi=3/16$, so $N_0=16$. 8 samples hold 1.5 cycles, so it **leaks**:
  $\lvert X\rvert\approx[1,\ 2.4,\ 2.8,\ 1.19,\ 1,\ 1.19,\ 2.8,\ 2.4]$, every bin nonzero.
</details>

<details><summary>6. (Step 7) A DTFS of x[n] = cos(πn/3) is computed with N = 9. Does synthesis recover x for every n? Which N would you use?</summary>

No. $\Omega_0/2\pi=1/6$, so $N_0=6$, and $9/6=1.5$ isn't whole. Synthesis repeats the block, so at
$n=9$ it gives $x[0]=1$, but the true $x[9]=\cos(3\pi)=-1$. Use $N=6$, or any multiple (12, 18, …).
</details>

<details><summary>7. (Step 8) Linear convolution of [1,1] with [1,1]? What do 2-point DFTs give instead?</summary>

The linear convolution is $[1,2,1]$. Multiplying 2-point DFTs gives the wrapped version,
$[1+1,\ 2]=[2,2]$. Pad both signals to length 3 to get $[1,2,1]$.
</details>

<details><summary>8. (Step 12) x[n] = 0.8ⁿ u[n] + 2ⁿ u[−n−1]. Find X(z) and its ROC. Is it stable?</summary>

$X(z)=\frac{z}{z-0.8}-\frac{z}{z-2}$. The second term is minus the left-sided pair. The ROC is
$0.8<\lvert z\rvert<2$, a ring, so the signal is two-sided. The ring contains $\lvert z\rvert=1$,
so it's **stable**, but it isn't causal.
</details>

<details><summary>9. (Step 12) The causal system y[n] = 1.1·y[n−1] + x[n]. Stable?</summary>

No. The pole is at $1.1$, outside the unit circle, and $h[n]=1.1^n u[n]$ grows forever.
</details>

<details><summary>10. (Step 12) The causal system y[n] = −0.5·y[n−1] + x[n]. What does h[n] look like?</summary>

$h[n]=(-0.5)^n u[n]=1,-0.5,0.25,-0.125,\dots$ The sign flips every sample and the size shrinks.
The pole is at $-0.5$, inside the unit circle, so it's stable.
</details>

<details><summary>11. (Step 11) Write X(z) for the list x = [3, 0, −1] at n = −1, 0, 1. What is its ROC?</summary>

Tag each sample with $z^{-n}$: $X(z)=3z^{1}+0\cdot1+(-1)z^{-1}=3z-z^{-1}$. It's finite, so the ROC is
everything except $z=0$ (because of $z^{-1}$) and $z=\infty$ (because of $z^{1}$).
</details>

<details><summary>12. (Step 12) X(z) = z/(z−0.5) + z/(z+3). List every possible ROC. Which one is causal? Which is stable?</summary>

The poles are $0.5$ and $-3$, at distances $0.5$ and $3$, which gives three ROCs:

| ROC | $x[n]$ | Causal? | Stable? |
|---|---|---|---|
| $\lvert zvert<0.5$ | $-\left(0.5^n+(-3)^night)u[-n-1]$ | ❌ | ❌ (1 isn't inside) |
| $0.5<\lvert zvert<3$ | $0.5^nu[n]-(-3)^nu[-n-1]$ | ❌ | ✅ (contains $\lvert zvert=1$) |
| $\lvert zvert>3$ | $\left(0.5^n+(-3)^night)u[n]$ | ✅ | ❌ ($(-3)^n$ blows up) |
</details>

<details><summary>13. (Step 13) Invert X(z) = z / ((z−1)(z−0.5)), |z| > 1.</summary>

There's a factor $z$ on top, so divide by $z$: $rac{X}{z}=rac{1}{(z-1)(z-0.5)}=rac{C}{z-1}+rac{D}{z-0.5}$.
Cover-up gives $C=rac{1}{1-0.5}=2$ and $D=rac{1}{0.5-1}=-2$, so $X=rac{2z}{z-1}-rac{2z}{z-0.5}$.
The ROC is outside both poles, so both run forward:
$x[n]=2\left(1-0.5^night)u[n]=0,\ 1,\ 1.5,\ 1.75,\dots$ **Check:** the first terms of the series
expansion are $0+z^{-1}+1.5z^{-2}+\dots$ ✓
</details>

<details><summary>14. (Step 14) y[n] = 0.9·y[n−1] + u[n], y[−1] = 0. Find the final value without solving.</summary>

$Y_+=\frac{1}{(1-0.9z^{-1})(1-z^{-1})}$, and $(1-z^{-1})Y_+$ at $z=1$ is $\frac{1}{0.1}=10$. In
general, a constant input $c$ settles at $\frac{c}{1-a}$, which you'll see in Lab 4 Q2A.
</details>
