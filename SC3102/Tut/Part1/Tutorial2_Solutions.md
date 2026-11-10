# SC3102 Tutorial 2: Signals 2 — Worked Solutions

*Worked solutions written from the official NTULearn solutions as a reference (not a copy).*
The steps follow the official method and order; the explanations are my own wording.
Official source: "Tutorial 2: Solutions" (typed PDF, 8 pages). Questions: `Tutorial2.pdf`.
⚠ marks a real problem in the official solution. Every ⚠ is collected, together with practical shortcuts, in
[Disagreements.md](Disagreements.md).

**Rules used for the spectra**
- Write every term as a **cosine with a positive amplitude**: $A\cos(2\pi ft+\phi)$.
  - Turn a sine into a cosine with $\sin\theta=\cos(\theta-\pi/2)$.
  - Absorb a minus sign with $-\cos\theta=\cos(\theta+\pi)$.
- **Single-sided spectrum:** amplitude $A$ and phase $\phi$ at frequency $f\ge0$.
- **Double-sided spectrum:** use Euler, $A\cos(2\pi ft+\phi)=\frac A2e^{j(2\pi ft+\phi)}+\frac A2e^{-j(2\pi ft+\phi)}$.
  - The amplitude is $A/2$ at both $\pm f$ (even).
  - The phase is $+\phi$ at $+f$ and $-\phi$ at $-f$ (odd).

---

## Q1. Single- and double-sided amplitude and phase spectra

### (a) $x_1(t)=10\cos\!\left(4\pi t+\frac{\pi}{8}\right)+6\sin\!\left(8\pi t+\frac{3\pi}{4}\right)$
1. Convert the sine to a cosine by subtracting $\pi/2$ from its phase:
   $$x_1(t)=10\cos\!\left(4\pi t+\tfrac{\pi}{8}\right)+6\cos\!\left(8\pi t+\tfrac{3\pi}{4}-\tfrac{\pi}{2}\right)=10\cos\!\left(4\pi t+\tfrac{\pi}{8}\right)+6\cos\!\left(8\pi t+\tfrac{\pi}{4}\right).$$
2. Euler form:
   $$x_1(t)=5e^{j(4\pi t+\frac{\pi}{8})}+5e^{-j(4\pi t+\frac{\pi}{8})}+3e^{j(8\pi t+\frac{\pi}{4})}+3e^{-j(8\pi t+\frac{\pi}{4})}.$$
3. Frequencies: $\omega_1=2\pi f_1=4\pi$ gives $f_1=2$ Hz; $\omega_2=2\pi f_2=8\pi$ gives $f_2=4$ Hz.

**Spectra to sketch:**

| | Amplitude | Phase (rad) |
|---|---|---|
| Single-sided | 10 at 2 Hz, 6 at 4 Hz | $\pi/8$ at 2 Hz, $\pi/4$ at 4 Hz |
| Double-sided | 5 at $\pm2$ Hz, 3 at $\pm4$ Hz | $\pi/8$ at 2, $-\pi/8$ at $-2$, $\pi/4$ at 4, $-\pi/4$ at $-4$ |

### (b) $x_2(t)=8\sin(3\pi t)\cos(5\pi t)$
1. Tools: $\sin A\cos B=\tfrac12[\sin(A+B)+\sin(A-B)]$ and $-\cos\theta=\cos(\theta+\pi)$.
2. Product to sum:
   $$x_2(t)=4\sin(8\pi t)+4\sin(-2\pi t)=4\sin(8\pi t)-4\sin(2\pi t).$$
3. Sines to cosines:
   $$x_2(t)=4\cos\!\left(8\pi t-\tfrac{\pi}{2}\right)-4\cos\!\left(2\pi t-\tfrac{\pi}{2}\right).$$
4. Absorb the minus sign with $+\pi$:
   $$x_2(t)=4\cos\!\left(8\pi t-\tfrac{\pi}{2}\right)+4\cos\!\left(2\pi t-\tfrac{\pi}{2}+\pi\right)=4\cos\!\left(8\pi t-\tfrac{\pi}{2}\right)+4\cos\!\left(2\pi t+\tfrac{\pi}{2}\right).$$
5. Euler form:
   $$x_2(t)=2e^{j(8\pi t-\frac{\pi}{2})}+2e^{-j(8\pi t-\frac{\pi}{2})}+2e^{j(2\pi t+\frac{\pi}{2})}+2e^{-j(2\pi t+\frac{\pi}{2})}.$$
6. Frequencies: $\omega_1=8\pi$ gives $f_1=4$ Hz; $\omega_2=2\pi$ gives $f_2=1$ Hz.

**Spectra to sketch:**

| | Amplitude | Phase (rad) |
|---|---|---|
| Single-sided | 4 at 1 Hz, 4 at 4 Hz | $+\pi/2$ at 1 Hz, $-\pi/2$ at 4 Hz |
| Double-sided | 2 at $\pm1$ Hz and $\pm4$ Hz | $\pi/2$ at 1, $-\pi/2$ at $-1$, $-\pi/2$ at 4, $\pi/2$ at $-4$ |

(The answer sheet's form, $4\cos(8\pi t-\frac{\pi}{2})-4\cos(2\pi t-\frac{\pi}{2})$, is the same signal before the minus sign is absorbed.)

---

## Q2. Sketch the signals

### (a) $x_1(t)=r(t)-r(t-1)$
Use the ramp definition, $r(t)=t$ for $t\ge0$ and 0 otherwise, and split by the value of $t$:
1. $t<0$: both ramps are zero, so $x_1(t)=0$.
2. $0\le t<1$: $r(t)=t$ and $r(t-1)=0$, so $x_1(t)=t$.
3. $t\ge1$: $r(t)=t$ and $r(t-1)=t-1$, so $x_1(t)=t-(t-1)=1$.

**Sketch:** zero up to $t=0$, a straight line rising to 1 at $t=1$, then flat at 1 forever.

### (b) $x_2(t)=\sum_{n=-\infty}^{\infty}g(t-3n)$, with $g(t)=u(t)u(2-t)$
1. $g(t)=u(t)u(2-t)$ is a rectangle: 1 for $0\le t\le2$, 0 elsewhere. (Why: $u(t)$ switches on at 0, and $u(2-t)$ switches off after 2.)
2. $x_2$ repeats this rectangle every 3 s. This is a **pulse train** with period $T=3$ s.

**Sketch:** height-1 pulses on $[3n,\,3n+2]$, that is $\dots,[-3,-1],[0,2],[3,5],[6,8],\dots$, with gaps of length 1 between them.

---

## Q3. Express the signals using singularity functions

### (a) $x_1(t)$: $+1$ on $(-1,0)$, $-1$ on $(0,1)$
1. It is two rectangular pulses:
   $$x_1(t)=\Pi\!\left(t+\tfrac12\right)-\Pi\!\left(t-\tfrac12\right).$$
2. Rewrite each pulse as a difference of two steps. (Why: a pulse on $(a,b)$ is $u(t-a)-u(t-b)$.)
   $$x_1(t)=u(t+1)-u(t)-u(t)+u(t-1)=u(t+1)-2u(t)+u(t-1).$$

**Answer: $x_1(t)=u(t+1)-2u(t)+u(t-1)$.**

### (b) $x_3(t)$: the periodic sawtooth (rises from 0 to 2 over one second, then stays at 0 for one second)
1. The graph repeats a triangular piece every $T=2$ s, so it can be written as
   $$x_3(t)=\sum_{n=-\infty}^{\infty}g(t-2n),$$
   where $g$ is the shape over one period.
2. From the figure, $g$ is a ramp of slope 2 on $[0,1]$, cut off at $t=1$:
   $$g(t)=2r(t)\,u(1-t)=r(2t)\,u(1-t).$$
   (Why the two forms are equal: $r(2t)=2t=2r(t)$ for $t\ge0$.)

**Answer: $x_3(t)=\sum_n g(t-2n)$, with $g(t)=r(2t)u(1-t)$.**

---

## Q4. Evaluate the integrals

### (a) $\int_{-\infty}^{7}t^2\delta(t-3)\,dt$
By the shifting (sifting) property, the integral picks out $t^2$ at $t=3$. That point lies inside the range $(-\infty,7]$.

**Answer: $t^2\big|_{t=3}=9$.**

### (b) $\int_{-\infty}^{\infty}\cos(\pi t)\,\delta(2t-2)\,dt$
1. **Common trap:** plugging $t=1$ straight in gives $\cos(\pi)=-1$, which is **wrong**. The delta has a scale factor of 2 inside it.
2. Apply $\delta(at)=\dfrac{1}{|a|}\delta(t)$: $\delta(2t-2)=\delta\big(2(t-1)\big)=\tfrac12\delta(t-1)$.
3. Then
   $$\int_{-\infty}^{\infty}\cos(\pi t)\,\delta(2t-2)\,dt=\frac12\int_{-\infty}^{\infty}\cos(\pi t)\,\delta(t-1)\,dt=\frac12\cos(\pi t)\Big|_{t=1}=-\frac12.$$

(The official solution notes that a change of variables gives the same result.)

**Answer: $-\tfrac12$.**

---

## Q5. Sampling $y(t)=K\cos(6000\pi t)\cos(2000\pi t)$

**Find the highest frequency first.**
1. Use $\cos A\cos B=\tfrac12[\cos(A+B)+\cos(A-B)]$:
   $$y(t)=\frac K2\big(\cos(8000\pi t)+\cos(4000\pi t)\big).$$
2. $2\pi f_1t=8000\pi t$ gives $f_1=4000$ Hz; $2\pi f_2t=4000\pi t$ gives $f_2=2000$ Hz.
3. The maximum frequency is $f_m=f_1=4000$ Hz. (Why this step matters: the product contains 4000 Hz, even though neither factor does.)

### (a) Largest sampling interval
1. Shannon's sampling theorem requires $F_s\ge2f_m$.
2. The minimum rate is $F_s=2\times4000=8000$ Hz.
3. The interval is the reciprocal of the rate.

**Answer: $T_s=\dfrac1{F_s}=\dfrac{1}{8000}$ s $=125\ \mu$s.**

### (b) Samples needed for one minute at that rate
At 8000 samples per second, one minute needs $60\times8000$.

**Answer: 480 000 samples.**

> **⚠ Check (document issue, minor):** the official solution PDF adds a part (c), "let the new transmitted signal be …", but the signal it gives is identical to the original, and no answer for (c) follows. It looks like an unfinished edit. Parts (a) and (b) are unaffected.

---

## Exercises

### Ex 1. Spectra of $x_3(t)=4\sin(8\pi t)+2\sin\!\left(12\pi t-\frac{\pi}{4}\right)-10\cos\!\left(16\pi t+\frac{5\pi}{4}\right)$
1. Tools: $-\cos\theta=\cos(\theta+\pi)$ and $\cos\theta=\cos(\theta+2\pi)$.
2. Sines to cosines:
   $$x_3(t)=4\cos\!\left(8\pi t-\tfrac{\pi}{2}\right)+2\cos\!\left(12\pi t-\tfrac{\pi}{4}-\tfrac{\pi}{2}\right)-10\cos\!\left(16\pi t+\tfrac{5\pi}{4}\right)$$
   $$=4\cos\!\left(8\pi t-\tfrac{\pi}{2}\right)+2\cos\!\left(12\pi t-\tfrac{3\pi}{4}\right)-10\cos\!\left(16\pi t+\tfrac{5\pi}{4}\right).$$
3. Absorb the minus sign by adding $\pi$, then remove a full turn of $2\pi$. (Why: $\frac{9\pi}{4}-2\pi=\frac{\pi}{4}$.)
   $$x_3(t)=4\cos\!\left(8\pi t-\tfrac{\pi}{2}\right)+2\cos\!\left(12\pi t-\tfrac{3\pi}{4}\right)+10\cos\!\left(16\pi t+\tfrac{5\pi}{4}+\pi\right)$$
   $$=4\cos\!\left(8\pi t-\tfrac{\pi}{2}\right)+2\cos\!\left(12\pi t-\tfrac{3\pi}{4}\right)+10\cos\!\left(16\pi t+\tfrac{\pi}{4}\right).$$
4. Euler form:
   $$x_3(t)=2e^{j(8\pi t-\frac{\pi}{2})}+2e^{-j(8\pi t-\frac{\pi}{2})}+e^{j(12\pi t-\frac{3\pi}{4})}+e^{-j(12\pi t-\frac{3\pi}{4})}+5e^{j(16\pi t+\frac{\pi}{4})}+5e^{-j(16\pi t+\frac{\pi}{4})}.$$
5. Frequencies: $\omega_1=8\pi\to f_1=4$ Hz, $\omega_2=12\pi\to f_2=6$ Hz, $\omega_3=16\pi\to f_3=8$ Hz.

**Spectra to sketch:**

| | Amplitude | Phase (rad) |
|---|---|---|
| Single-sided | 4 at 4 Hz, 2 at 6 Hz, 10 at 8 Hz | $-\pi/2$, $-3\pi/4$, $\pi/4$ |
| Double-sided | 2 at $\pm4$, 1 at $\pm6$, 5 at $\pm8$ | $+f$: $-\pi/2,-3\pi/4,\pi/4$; $-f$: $\pi/2,3\pi/4,-\pi/4$ |

### Ex 2. $x_3(t)=\Pi\!\left(\frac{t-3}{6}\right)+\Pi\!\left(\frac{t-4}{2}\right)$: sketch it and write its derivative using impulses
1. The two rectangles:
   - $\Pi\!\left(\frac{t-3}{6}\right)$ has width 6 and centre 3, so it covers $[0,6]$.
   - $\Pi\!\left(\frac{t-4}{2}\right)$ has width 2 and centre 4, so it covers $[3,5]$.
2. **Sketch of the sum:** 1 on $[0,3)$, 2 on $[3,5)$, 1 on $[5,6)$, and 0 elsewhere.
3. **Derivative:** each jump becomes an impulse whose weight is the jump size. Up-steps of $+1$ occur at $t=0$ and $t=3$; down-steps of $-1$ occur at $t=5$ and $t=6$:
   $$\frac{d}{dt}x_3(t)=\delta(t)+\delta(t-3)-\delta(t-5)-\delta(t-6).$$

### Ex 3. $x_2(t)$ from the figure in singularity functions
From the figure: zero until $t=1$; then a line from $-1$ (at $t=1$) down to $-2$ (at $t=2$); then a jump up to $+2$; then a line falling to 0 at $t=4$; zero after that.

1. **Split the waveform into two pieces:**
   - $x_{21}$, the negative piece on $[1,2]$.
   - $x_{22}$, the falling triangle on $[2,4]$.
2. **First piece.** On $[1,2]$ it equals $-t$, so
   $$x_{21}(t)=-t\,\Pi\!\left(t-\tfrac32\right)=-t\big(u(t-1)-u(t-2)\big)=-t\,u(t-1)+t\,u(t-2).$$
3. Rewrite each $t$ around its own switch-on point so that ramps appear. (Why: write $t=(t-1)+1$ next to $u(t-1)$, and $t=(t-2)+2$ next to $u(t-2)$.)
   $$x_{21}(t)=\big(-(t-1)-1\big)u(t-1)+\big((t-2)+2\big)u(t-2)$$
   $$=-r(t-1)-u(t-1)+r(t-2)+2u(t-2).$$
4. **Second piece.** It starts at height 2 at $t=2$, falls with slope $-1$, and the slope stops at $t=4$:
   $$x_{22}(t)=2u(t-2)-r(t-2)+r(t-4).$$
5. **Add the pieces.** The $r(t-2)$ terms cancel:
   $$x_2(t)=-r(t-1)-u(t-1)+r(t-2)+2u(t-2)+2u(t-2)-r(t-2)+r(t-4).$$

**Answer: $x_2(t)=-u(t-1)+4u(t-2)-r(t-1)+r(t-4)$.**

### Ex 4. $\int_0^{\infty}\sqrt{t+3}\;\delta(t+2)\,dt$
By the shifting property, the integral would pick out the integrand at $t=-2$. But $t=-2$ lies outside the integration range $[0,+\infty)$, so the delta never fires.

**Answer: 0.**
