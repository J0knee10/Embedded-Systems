# SC3102 Part 2: Discrete Time, Step by Step

Written for: "I'm fine with the continuous-time half, but the discrete half confuses me."

The steps follow the Part 2 lectures in `../Slides/` in order. Each step starts with the problem
the previous step couldn't solve. Every worked example was checked numerically.

**How each step is laid out:** **Problem** (what the last tool couldn't do), then **Idea** (the fix
in one sentence), then **Formula** (with every symbol explained), then **Example** (with real
numbers), then **Takeaway**.

**Notation:** the slides write discrete-time frequency as ω. This guide writes **Ω** (rad/sample)
to keep it separate from continuous-time ω (rad/s).

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

**The four transforms are one idea, extended four times:**

| | Works on | Frequencies it uses | Formula | Part 1 twin |
|---|---|---|---|---|
| **DFT** (Step 6) | a list of $N$ numbers | $N$ of them, $\Omega_k=2\pi k/N$ | $X[k]=\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N}$ | — |
| **DTFS** (Step 7) | a periodic signal, period $N$ | the same $N$ | same formula, valid for every $n$ | Fourier series |
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

**Periodic** means $x[n+N]=x[n]$ for every $n$, for some positive **integer** $N$.

**Test for $\cos(\Omega_0 n+\phi)$ or $e^{j\Omega_0 n}$:**
1. Find $\Omega_0$, the number multiplying $n$.
2. Compute $\Omega_0/2\pi$.
3. If it's a fraction, the signal is periodic. Reduce it to $k/N$ in lowest terms; the period is the denominator $N$.
4. If it isn't a fraction (a leftover $\pi$ or $\sqrt{\ }$), the signal is **never** periodic.

**Why:** you need $\Omega_0N=2\pi k$, a whole number of turns, with $N$ a whole number. In
continuous time $T=2\pi/\omega$ always works because $T$ can be any real number. In discrete time
$N$ has to be an integer, and that's the whole difference.

| Signal | $\Omega_0/2\pi$ | Period |
|---|---|---|
| $\cos(\pi n/2)$ | $1/4$ | 4 |
| $\cos(0.4\pi n)$ | $1/5$ | 5 |
| $\cos(3\pi n/8)$ | $3/16$ | **16** (not $16/3$: 3 cycles fit in 16 samples) |
| $\cos(n)$, $\cos(0.4n)$ | $\frac{1}{2\pi}$, $\frac{1}{5\pi}$ | never periodic |

- **Sums:** the period is the lowest common multiple of the parts' periods. For example,
  $\cos(\pi n/2)+\sin(\pi n/3)$ has periods 4 and 6, so $N=12$. If any part is never periodic,
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

**Problem.** The DFT handles a finite list, but real signals go on forever. Start with the easy
infinite ones: periodic signals.

**Idea.** A signal with period $N$ is fully described by one period. So take the DFT of one
period, and use the same synthesis formula for **every** $n$.

**Why that works:**
- Which walkers $e^{j\Omega n}$ repeat every $N$ samples? We need $\Omega N=2\pi k$, so
  $\Omega=2\pi k/N$.
- $k$ and $k+N$ give the same walker, because angles wrap. So **only $N$ different frequencies
  exist** for period $N$, and they are exactly the DFT's.
- The synthesis formula is therefore periodic with period $N$. It matches $x$ on one period, and
  both repeat, so it matches $x$ everywhere.

**Formulas:** identical to the DFT.
$$X[k]=\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N},\qquad x[n]=\frac1N\sum_{k=0}^{N-1}X[k]e^{j2\pi kn/N}\quad\text{for every }n.$$

**DFT vs DTFS:** the same numbers, read differently. The DFT says "here are $N$ numbers"; the
DTFS says "here is an infinite periodic signal". **The catch:** the DFT always behaves like the
DTFS, so it quietly assumes your block repeats forever. That assumption is what causes spectral
leakage in Lab 3 Q2.

**Compared with Part 1:** the continuous-time Fourier series needs infinitely many harmonics. The
DTFS needs only $N$, because discrete harmonics wrap around.

---

## Step 8: The catch with multiplying DFTs (circular convolution)

**Question.** In continuous time, convolution corresponds to multiplying Fourier transforms.
Does multiplying DFTs give convolution too?

**Example from the lecture:** $x=[1,2,1]$ and $h=[1,1,2]$.
- Linear convolution (Step 4) gives $x*h=[1,3,5,5,2]$: 5 values.
- Multiplying their 3-point DFTs and inverting gives $[6,5,5]$: 3 values.

The 3-value answer is the 5-value answer **wrapped around** into 3 slots:
$[1+5,\ 3+2,\ 5]=[6,5,5]$. The DFT treats both signals as repeating (Step 7), so the tail of the
convolution spills into the next period and lands on top of the start. That is **circular
convolution**.

**Fix:** before taking the DFT, pad both signals with zeros to at least $L_x+L_h-1$ samples (5
here). Then the result has room and nothing wraps, so you get $[1,3,5,5,2]$. This is how fast
filtering with the FFT is done in practice.

---

## Step 9: DTFT, non-periodic signals

**Problem.** Most signals aren't periodic: a single clap, or $(\tfrac12)^n u[n]$.

**Idea.** Pretend the signal is periodic with a huge period, then let the period grow to infinity.
As $N$ grows:
1. the block contains more and more of the real signal, and
2. the frequencies $2\pi k/N$ get closer together, until they fill in every $\Omega$.

**Formulas.**
$$X(\Omega)=\sum_{n=-\infty}^{\infty}x[n]\,e^{-j\Omega n}\qquad\qquad x[n]=\frac{1}{2\pi}\int_0^{2\pi}X(\Omega)\,e^{j\Omega n}\,d\Omega$$
The sum over $k$ has turned into an integral over $\Omega$, just as the Fourier series turned into
the CTFT in Part 1.

**Two things to remember:**
- **$\Omega$ can take any value, but $X(\Omega)$ repeats every $2\pi$**, because
  $e^{-j(\Omega+2\pi)n}=e^{-j\Omega n}$. Only $[-\pi,\pi)$ matters. $\Omega=\pi$, the pattern
  $+1,-1,+1,\dots$, is the fastest a discrete signal can wiggle. It corresponds to $f_s/2$ in
  Step 2.
- **The DTFT only exists if $\sum_n\lvert x[n]\rvert<\infty$** ("absolutely summable").

**Example.** $x[n]=(\tfrac12)^n u[n]$:
$$X(\Omega)=\sum_{n=0}^{\infty}\left(\tfrac12e^{-j\Omega}\right)^n=\frac{1}{1-\tfrac12e^{-j\Omega}}
\quad\text{(geometric series; the ratio has size }\tfrac12<1\text{)}$$
$X(0)=2$, which is just the sum of all the samples. $X(\pi)=\frac{1}{1+1/2}=\frac23$. So the
signal has more low-frequency content than high, which fits a smooth decay.

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

**The problem that drives Step 11:** the DTFT needs $\sum\lvert x\rvert<\infty$. The step $u[n]$,
growing signals like $2^n u[n]$, and the impulse response of any unstable system all fail that
test, but we still want to analyse them.

---

## Step 11: Z-transform, squash then DTFT

**Problem.** The DTFT of $u[n]$ would be $1+1+1+\dots=\infty$.

**Idea (how `lecture(2).pdf` introduces it):** first **squash** the signal by multiplying by
$r^{-n}$, then take the DTFT.
$$X(z)=\sum_n x[n]\,\underbrace{r^{-n}}_{\text{squash}}\;\underbrace{e^{-j\Omega n}}_{\text{DTFT}}
=\sum_n x[n]\,z^{-n},\qquad z=re^{j\Omega}.$$

A point $z$ in the z-plane encodes two things:
- **its distance from the origin, $r=\lvert z\rvert$:** how hard you squash
- **its angle, $\Omega$:** the frequency, the same as in the DTFT

Each circle of radius $r$ in the z-plane holds the DTFT of a squashed copy of $x$. The **unit
circle** ($r=1$, no squashing) holds the ordinary DTFT, which is the frequency response from
Step 10.

**Example.** $u[n]$: $X(z)=\sum_{n\ge0}z^{-n}=\frac{1}{1-z^{-1}}=\frac{z}{z-1}$, which works for
$\lvert z\rvert>1$. Any squash factor $r>1$ makes the step summable.

**Delay becomes a power of $z$:** $x[n-k]\leftrightarrow z^{-k}X(z)$. Convolution still becomes
multiplication: $Y(z)=H(z)X(z)$. These two properties are what make Step 14 possible.

---

## Step 12: ROC, poles and "sides"

### 12.1 ROC: where the sum actually works

The **ROC (region of convergence)** is the set of $z$ where the infinite sum adds up to a finite
number. Whether it converges depends only on $\lvert z\rvert$ (the angle part always has size
1), so an ROC is always made of whole circles: a disc, the outside of a circle, or a ring.

**Example:** $x[n]=0.6^n u[n]$ gives $X(z)=\sum(0.6/z)^n=\frac{z}{z-0.6}$, which needs
$\lvert0.6/z\rvert<1$, so the **ROC is $\lvert z\rvert>0.6$**.

| $z$ | Ratio $0.6/z$ | Actual sum | Formula $\frac{z}{z-0.6}$ |
|---|---|---|---|
| 2 | 0.3 | $1+0.3+0.09+\dots=$ **1.43** | **1.43** ✅ |
| 0.5 | 1.2 | $1+1.2+1.44+\dots=$ **∞** | **−5** ❌ |

Outside the ROC, the formula still gives a number, but the sum doesn't converge. This is Lab 4 Q1D.

### 12.2 The same formula can come from two signals

**Right-sided** $x[n]=a^n u[n]$:
$$X(z)=\sum_{n=0}^{\infty}(az^{-1})^n=\frac{z}{z-a},\qquad\text{needs }\lvert a/z\rvert<1\;\Rightarrow\;\boxed{\lvert z\rvert>\lvert a\rvert}$$
**Left-sided** $x[n]=-a^n u[-n-1]$, which is nonzero only for $n\le-1$. Substitute $m=-n$:
$$X(z)=-\sum_{m=1}^{\infty}(z/a)^m=\frac{z}{z-a},\qquad\text{needs }\lvert z/a\rvert<1\;\Rightarrow\;\boxed{\lvert z\rvert<\lvert a\rvert}$$
**Same formula, opposite ROCs.** So a Z-transform is always "**formula + ROC**". The $-5$ at $z=0.5$
in the table above is in fact the correct transform of the left-sided signal, because $z=0.5$ is
inside *its* ROC.

### 12.3 "Sided" is about time: which direction the signal runs

| $n$ | … | −3 | −2 | −1 | **0** | 1 | 2 | 3 | … | Name |
|---|---|---|---|---|---|---|---|---|---|---|
| $0.5^n$ for $n\ge0$ | | 0 | 0 | 0 | **1** | 0.5 | 0.25 | 0.125 | → forever | **right-sided** |
| $-2^n$ for $n\le-1$ | forever ← | −0.125 | −0.25 | −0.5 | **0** | 0 | 0 | 0 | | **left-sided** |
| both added | forever ← | ≠0 | ≠0 | ≠0 | ≠0 | ≠0 | ≠0 | ≠0 | → forever | **two-sided** |

If the signal is an impulse response, "right-sided starting at $n=0$" means the system reacts only
*after* it's poked, which is **causal** (Step 4).

### 12.4 A pole is an ingredient of the signal

**Mechanically:** a pole is a value of $z$ that makes the denominator zero, so the formula blows
up there. For $\frac{z}{z-0.6}+\frac{z}{z-1.2}$, the poles are $0.6$ and $1.2$.

**What it means:** each term $\frac{z}{z-p}$ is the transform of $p^n$, so **each pole $p$ means
the signal contains the ingredient $p^n$**.
- $\lvert p\rvert<1$ shrinks as $n$ increases.
- $\lvert p\rvert>1$ grows.
- A negative $p$ flips sign every step.

The poles tell you **which** exponentials make up the signal. They don't tell you which
**direction** in time each one runs.

### 12.5 The ROC decides the direction

> **ROC outside a pole → that ingredient runs forward ($p^n u[n]$).
> ROC inside a pole → it runs backward ($-p^n u[-n-1]$).**

The ROC depends only on $\lvert z\rvert$, so draw it as a **ruler** from 0 to ∞. The poles are
walls on the ruler, and the ROC must sit in one gap between them. $P$ poles at different radii
give $P+1$ possible ROCs. With poles at 0.5 and 2:
```
|z|:  0 ──────────── 0.5 ─────────── 1 ─────────── 2 ──────────── ∞
      [   region A   ]  ×  [       region B        ]  ×  [  region C  ]
                       pole      (unit circle is here)  pole
```

| Region | Pole 0.5 runs… | Pole 2 runs… | Signal | Causal? | Stable? |
|---|---|---|---|---|---|
| A: $\lvert z\rvert<0.5$ | backward | backward | left-sided | ❌ | ❌ |
| B: $0.5<\lvert z\rvert<2$ | **forward** | backward | two-sided | ❌ | ✅ |
| C: $\lvert z\rvert>2$ | forward | forward | right-sided | ✅ | ❌ |

### 12.6 Stability, without memorising

Stable means the signal dies out at both ends, so each ingredient must shrink **in the direction
it runs**:
- A **forward** ingredient $p^n$ (as $n\to+\infty$) shrinks only if $\lvert p\rvert<1$.
- A **backward** ingredient $p^n$ (as $n\to-\infty$) shrinks only if $\lvert p\rvert>1$. For
  example, $2^n$ at $n=-1,-2,-3$ is $0.5,0.25,0.125$.

Region B runs the small pole forward and the big pole backward, so both pieces shrink and the
signal is stable. That is exactly the case where the unit circle (radius 1) falls inside the ROC.

### 12.7 The rules, as shortcuts

| ROC shape | Signal is… | Why |
|---|---|---|
| outside the outermost pole | right-sided | outside every pole, so every ingredient runs forward |
| inside the innermost pole | left-sided | inside every pole, so every ingredient runs backward |
| a ring between two poles | two-sided | some ingredients run forward, some backward |

- **Causal** ⇔ the ROC is **outside the outermost pole**.
- **BIBO stable** ⇔ the ROC **contains the unit circle**. (A stable signal has a DTFT, and the
  DTFT lives on the unit circle.)
- **Both** ⇔ **every pole is strictly inside the unit circle.**

---

## Step 13: Inverting a Z-transform

**Recipe: find $h[n]$ from $H(z)$, given causal, stable, or a stated ROC**
1. Factor the denominator to find the poles.
2. Do partial fractions on $H(z)/z$, then multiply back by $z$. This gives a sum of $c\,\frac{z}{z-p}$ terms.
3. Sketch the ruler and pick the ROC: causal means outermost; stable means it contains $\lvert z\rvert=1$.
4. For each term: if the ROC is outside $p$, write $c\,p^n u[n]$; if inside, write $-c\,p^n u[-n-1]$.

### Worked example from `lecture(3).pdf` (the full maths behind the ruler in 12.5)

$y[n]-\tfrac52 y[n-1]+y[n-2]=x[n]$. Delays become powers of $z^{-1}$:
$$H(z)=\frac{1}{1-\tfrac52z^{-1}+z^{-2}}=\frac{z^2}{(z-\tfrac12)(z-2)}\qquad\text{poles at }\tfrac12,\ 2.$$

**Trick:** divide by $z$ first, so the terms come out in $\frac{z}{z-a}$ form, which matches the
table:
$$\frac{H(z)}{z}=\frac{z}{(z-\tfrac12)(z-2)}=\frac{-1/3}{z-\tfrac12}+\frac{4/3}{z-2}
\;\Rightarrow\;
H(z)=-\tfrac13\frac{z}{z-\tfrac12}+\tfrac43\frac{z}{z-2}.$$

| ROC | $h[n]$ | Sided | Causal? | Stable? |
|---|---|---|---|---|
| $\lvert z\rvert>2$ | $\left(\tfrac43 2^n-\tfrac13(\tfrac12)^n\right)u[n]$ | right | ✅ | ❌ ($2^n$ blows up) |
| $\tfrac12<\lvert z\rvert<2$ | $-\tfrac13(\tfrac12)^n u[n]-\tfrac43 2^n u[-n-1]$ | two | ❌ | ✅ |
| $\lvert z\rvert<\tfrac12$ | $\left(\tfrac13(\tfrac12)^n-\tfrac43 2^n\right)u[-n-1]$ | left | ❌ | ❌ |

No ROC is both causal and stable, because the pole at 2 is outside the unit circle. Running the
recurrence directly gives $h=1,\ 2.5,\ 5.25,\ 10.625,\dots$, which matches the causal row exactly.

> **Lab 4 Q1 is the same exercise with poles at 0.6 and 1.2.** Fill in the three rows yourself
> before checking `../Lab4/Lab_4_Answers.md`.

**Pairs to memorise:**

| $x[n]$ | $X(z)$ | ROC |
|---|---|---|
| $\delta[n]$ | $1$ | all $z$ |
| $u[n]$ | $\frac{z}{z-1}$ | $\lvert z\rvert>1$ |
| $a^n u[n]$ | $\frac{z}{z-a}=\frac{1}{1-az^{-1}}$ | $\lvert z\rvert>\lvert a\rvert$ |
| $-a^n u[-n-1]$ | $\frac{z}{z-a}$ | $\lvert z\rvert<\lvert a\rvert$ |
| $n a^n u[n]$ | $\frac{az}{(z-a)^2}$ | $\lvert z\rvert>\lvert a\rvert$ |
| $x[n-k]$ | $z^{-k}X(z)$ | same |
| $(x*h)[n]$ | $X(z)H(z)$ | contains $R_X\cap R_H$ |

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

<details><summary>5. (Step 8) Linear convolution of [1,1] with [1,1]? What do 2-point DFTs give instead?</summary>

The linear convolution is $[1,2,1]$. Multiplying 2-point DFTs gives the wrapped version,
$[1+1,\ 2]=[2,2]$. Pad both signals to length 3 to get $[1,2,1]$.
</details>

<details><summary>6. (Step 12) x[n] = 0.8ⁿ u[n] + 2ⁿ u[−n−1]. Find X(z) and its ROC. Is it stable?</summary>

$X(z)=\frac{z}{z-0.8}-\frac{z}{z-2}$. The second term is minus the left-sided pair. The ROC is
$0.8<\lvert z\rvert<2$, a ring, so the signal is two-sided. The ring contains $\lvert z\rvert=1$,
so it's **stable**, but it isn't causal.
</details>

<details><summary>7. (Step 12) The causal system y[n] = 1.1·y[n−1] + x[n]. Stable?</summary>

No. The pole is at $1.1$, outside the unit circle, and $h[n]=1.1^n u[n]$ grows forever.
</details>

<details><summary>8. (Step 12) The causal system y[n] = −0.5·y[n−1] + x[n]. What does h[n] look like?</summary>

$h[n]=(-0.5)^n u[n]=1,-0.5,0.25,-0.125,\dots$ The sign flips every sample and the size shrinks.
The pole is at $-0.5$, inside the unit circle, so it's stable.
</details>

<details><summary>9. (Step 14) y[n] = 0.9·y[n−1] + u[n], y[−1] = 0. Find the final value without solving.</summary>

$Y_+=\frac{1}{(1-0.9z^{-1})(1-z^{-1})}$, and $(1-z^{-1})Y_+$ at $z=1$ is $\frac{1}{0.1}=10$. In
general, a constant input $c$ settles at $\frac{c}{1-a}$, which you'll see in Lab 4 Q2A.
</details>
