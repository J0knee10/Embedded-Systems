# SC3102 Tutorial 1: Signals 1 — Worked Solutions

*Worked solutions written from the official NTULearn solutions as a reference (not a copy).*
The steps follow the official method and order; the explanations are my own wording.
Official source: "Tutorial1: Solutions" (typed PDF, 7 pages). Questions: `Tutorial1(1).pdf`.
⚠ marks a real problem in the official solution. Every ⚠ is collected, together with practical shortcuts, in
[Disagreements.md](Disagreements.md).

---

## Q1. Prove or disprove periodicity using the definition

**Approach used for (a)–(c):** assume a period $T>0$ exists, write out $x(t+T)=x(t)$ for all $t$, and see whether that equation can hold.

### (a) $x(t)=e^{3.1t}$
1. Assume $T>0$ works. For every $t$:
   $$x(t+T)=e^{3.1(t+T)}=e^{3.1t}=x(t).$$
2. $e^{3.1t}$ is never zero, so divide both sides by it:
   $$e^{3.1T}=1.$$
3. A real exponential equals 1 only when its exponent is 0, so $T=0$. That contradicts the assumption $T>0$.

**Answer: not periodic.**

### (b) $x(t)=e^{j3.1t}$, $j=\sqrt{-1}$
1. Assume $T>0$ works: $x(t+T)=e^{j3.1(t+T)}=e^{j3.1t}=x(t)$ for all $t$.
2. Divide by $e^{j3.1t}$, which is non-zero: $e^{j3.1T}=1$.
3. This holds when $3.1T=2\pi n$ for an integer $n$. (Why: $e^{j\theta}=1$ whenever $\theta$ is a whole number of turns.)
4. So $T=\dfrac{2\pi n}{3.1}$ is a period for every $n>0$. The fundamental period is the smallest one, at $n=1$.

**Answer: periodic, $T_0=\dfrac{2\pi}{3.1}$.**

### (c) $x(t)=\sum_{n=-\infty}^{\infty}g(t-3n)$, $g$ arbitrary
1. Assume $T>0$ works:
   $$x(t+T)=\sum_n g(t+T-3n)\overset{?}{=}\sum_n g(t-3n)=x(t).$$
2. Try $T=3m$ for an integer $m$:
   $$x(t+3m)=\sum_n g(t+3m-3n)=\sum_n g\big(t-(3n-3m)\big).$$
3. Change the summation variable to $k=n-m$. (Why this is allowed: as $n$ runs over all integers, so does $k$.) This gives
   $$x(t+3m)=\sum_k g(t-3k)=x(t).$$
4. So $T=3m$ is a period for every positive integer $m$. The smallest is at $m=1$.

**Answer: periodic, $T_0=3$.**

---

## Q2. Periodic or not? (time in seconds)

### (a) $x(t)=\cos(20t+1)+\sin(30\pi t-4)$
1. Find each term's fundamental period:
   - $\cos(20t+1)$: $T_0=\dfrac{2\pi}{20}=\dfrac{\pi}{10}$.
   - $\sin(30\pi t-4)$: $T_1=\dfrac{2\pi}{30\pi}=\dfrac{1}{15}$.
2. Take the ratio of the periods:
   $$\frac{T_0}{T_1}=\frac{\pi}{10}\cdot\frac{15}{1}=\frac{3\pi}{2}.$$
3. The ratio is irrational, so the two periods have no common multiple. (Why: a sum is periodic only if some whole number of each period lines up, which needs a rational ratio.)

**Answer: not periodic.**

### (b) $x(t)=\cos^2(10t)$
1. Use the identity $\cos^2(\theta)=\dfrac{1+\cos(2\theta)}{2}$:
   $$x(t)=\tfrac12+\tfrac12\cos(20t).$$
2. A constant term repeats with any period, so it doesn't restrict the period. The period comes from the cosine term: $2\pi/20$.

**Answer: periodic, $T_0=\dfrac{\pi}{10}$ s.**

---

## Q3. Energy signal or power signal?

### (a) $x(t)=e^{j\pi t}$, $-\infty<t<\infty$
1. Magnitude: $|x(t)|=|e^{j\pi t}|=1$.
2. Energy: $E_x=\int_{-\infty}^{\infty}|x(t)|^2dt=\int_{-\infty}^{\infty}1\,dt=\infty$. The energy is infinite.
3. Power:
   $$P_x=\lim_{T\to\infty}\frac1T\int_{-T/2}^{T/2}|x(t)|^2dt=\lim_{T\to\infty}\frac1T\int_{-T/2}^{T/2}dt=\lim_{T\to\infty}\frac1T\Big[\tfrac T2+\tfrac T2\Big]=1.$$
4. The power is finite and non-zero.

**Answer: power signal.**

### (b) $x(t)=t\,u(t)$
1. Squared magnitude: $|x(t)|^2=t^2u(t)$.
2. Energy: $E_x=\int_{-\infty}^{\infty}t^2u(t)\,dt=\infty$.
3. Power:
   $$P_x=\lim_{T\to\infty}\frac1T\int_{-T/2}^{T/2}t^2u(t)\,dt=\lim_{T\to\infty}\frac1T\int_0^{T/2}t^2dt=\infty.$$
   (Why it diverges: the integral is $T^3/24$, so $P=T^2/24$, which still grows.)

**Answer: neither an energy signal nor a power signal.**

---

## Q4. Energy of $x(t)+y(t)$ and $x(t)-y(t)$ for orthogonal energy signals

1. Definitions: $E_x=\int_{-\infty}^{\infty}|x(t)|^2dt$ and $E_y=\int_{-\infty}^{\infty}|y(t)|^2dt$.
2. Energy of the sum. Expand the square:
   $$E_{x+y}=\int_{-\infty}^{\infty}|x(t)+y(t)|^2dt=\int|x(t)|^2dt+\int|y(t)|^2dt+2\int x(t)y(t)\,dt.$$
3. Orthogonality makes the last integral zero, so
   $$E_{x+y}=E_x+E_y.$$
4. Energy of the difference: the same expansion, but the cross term has a minus sign:
   $$E_{x-y}=\int|x|^2dt+\int|y|^2dt-2\int x(t)y(t)\,dt=E_x+E_y.$$
5. So $E_{x+y}=E_{x-y}$.
6. Power: $x\pm y$ has finite energy, so it is an energy signal and its average power is zero.

**Answer: $E_{x+y}=E_{x-y}=E_x+E_y$. Both signals are energy signals with zero power.**

---

## Q5. Which functions satisfy the properties of an autocorrelation function?

First, the three properties an autocorrelation $R_x(\tau)$ must have:
- **(i) Symmetric:** $R_x(\tau)=R_x(-\tau)$.
- **(ii) Largest at the origin:** $|R_x(\tau)|\le R_x(0)$.
- **(iii) Non-negative spectrum:** $R_x(\tau)$ and the power spectral density $S_x(f)$ form a Fourier transform pair, and $S_x(f)\ge0$.

### (a) $x(\tau)=\delta(\tau)+\sin(2\pi f_1\tau)$
$\sin$ is an odd function, so $x(\tau)\ne x(-\tau)$. Property (i) fails.

**Answer: not an autocorrelation function.**

### (b) $x(\tau)=1-|\tau|$ for $-1\le\tau\le1$, 0 elsewhere
1. Remove the absolute value: $|\tau|=-\tau$ when $\tau<0$, and $|\tau|=\tau$ when $\tau>0$. So
   $$x(\tau)=\begin{cases}1+\tau&-1\le\tau\le0\\1-\tau&0\le\tau\le1\\0&\text{elsewhere}\end{cases}$$
   This is a triangle with its peak (value 1) at $\tau=0$ and its base from $-1$ to $1$.
2. Check the three properties:
   - (i) $x(\tau)=x(-\tau)$ ✓
   - (ii) $x(0)\ge x(\tau)$ ✓
   - (iii) The Fourier transform is non-negative ✓. Using the given pair with $T=1$, $X(f)=\mathrm{sinc}^2(f)\ge0$.
3. All three hold.

**Answer: it can be an autocorrelation function.**

> **⚠ Check:** the official solution gives the transform in step (iii) as $2\,\mathrm{sinc}^2(2f)$. The pair stated in the question,
> $\mathcal F[\mathrm{tri}(t/T)]=T\,\mathrm{sinc}^2(fT)$, with $T=1$ gives $\mathrm{sinc}^2(f)$. A numerical check agrees, and so does the
> value at $f=0$, which must equal the triangle's area of 1. The conclusion doesn't change, because both are $\ge0$.

*(The official PDF also lists a part (c) here, the rectangle $x(\tau)=1$ on $[-1,1]$. It is solved as Exercise 3 below.)*

---

## Exercises

### Ex 1(a) $x(t)=\cos(20t+1)\sin(30t-4)$
The official solution shows two methods.

**First method (common period of the factors):**
1. A product of two periodic signals is periodic if the factors share a common period.
2. The periods are $\dfrac{2\pi}{20}=\dfrac{\pi}{10}$ and $\dfrac{2\pi}{30}=\dfrac{\pi}{15}$.
3. Their common period is $\dfrac{\pi}{5}$. (Why: $2\times\frac{\pi}{10}=3\times\frac{\pi}{15}=\frac{\pi}{5}$.)

So the fundamental period is $\pi/5$ s.

**Second method (product-to-sum):**
1. Use $\cos(x)\sin(y)=\tfrac12\big(\sin(x+y)-\sin(x-y)\big)$:
   $$x(t)=\tfrac12\big(\sin(50t-3)-\sin(-10t+5)\big).$$
2. The two periods are $T_0=\dfrac{2\pi}{50}=\dfrac{\pi}{25}$ s and $T_1=\dfrac{2\pi}{10}=\dfrac{\pi}{5}$ s.
3. Their ratio is $\dfrac{T_0}{T_1}=\dfrac{\pi}{25}\cdot\dfrac{5}{\pi}=\dfrac15$, which is rational, so $x(t)$ is periodic.
4. The fundamental period is $5T_0=T_1=\dfrac{\pi}{5}$ s.

**Answer: periodic, $T_0=\dfrac{\pi}{5}$ s.**

### Ex 1(b) $x(t)=g(2t)$, with $g$ periodic with period $T_0$
1. Assume $T>0$ works: $x(t+T)=g\big(2(t+T)\big)=g(2t+2T)=g(2t)=x(t)$.
2. Substitute $\tau=2t$: the condition becomes $g(\tau+2T)=g(\tau)$.
3. That holds when $2T$ equals the period of $g$: $2T=T_0$, so $T=T_0/2$.

**Answer: periodic, fundamental period $\dfrac{T_0}{2}$.**

### Ex 2. $x(t)=A\cos(2\pi f_0t)$ for $-\frac{T_0}{2}\le t\le\frac{T_0}{2}$, 0 elsewhere, with $T_0=\frac1{f_0}$
1. Energy:
   $$E_x=\int_{-\infty}^{\infty}|x(t)|^2dt=\int_{-T_0/2}^{T_0/2}A^2\cos^2(2\pi f_0t)\,dt=\int_{-T_0/2}^{T_0/2}\frac{A^2}{2}\big[1+\cos(4\pi f_0t)\big]dt=\frac{A^2T_0}{2}.$$
   (Why the cosine part vanishes: over this window, $\cos(4\pi f_0t)$ runs through exactly two whole cycles, so its integral is zero.)
2. The energy is finite.

**Answer: energy signal ($E_x=A^2T_0/2$).**

### Ex 3. Is $x(\tau)=1$ for $-1\le\tau\le1$ (0 elsewhere) an autocorrelation function?
1. It is a rectangle of height 1 and width 2.
2. Check the three properties from Q5:
   - (i) $x(\tau)=x(-\tau)$ ✓
   - (ii) $x(0)\ge x(\tau)$ ✓
   - (iii) $X(f)=\mathcal F[x(\tau)]=2\,\mathrm{sinc}(2f)$. (Why: $x=\Pi(\tau/2)$ and the given pair uses $T=2$.) A sinc swings **both positive and negative**, so (iii) fails.

**Answer: not an autocorrelation function.** Its spectrum takes negative values, but a power spectral density can't.
