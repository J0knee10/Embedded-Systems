# SC3102 Tutorial 3: Systems — Worked Solutions

*Worked solutions written from the official NTULearn solutions as a reference (not a copy).*
The steps follow the official method and order; the explanations are my own wording.
Official source: "Tutorial 3: Solutions" (typed PDF, 14 pages). Questions: `Tutorial3(3).pdf`.
⚠ marks a real problem in the official solution or in the answer key printed on the question sheet. Every ⚠ is collected, together with practical shortcuts, in
[Disagreements.md](Disagreements.md).

**The standard property tests used throughout**
- **Memory:** does $y(t)$ use input values from times other than $t$?
- **Causal:** does $y(t_0)$ use only inputs at times $\le t_0$?
- **Time-invariant:** call the output for $x_1$ $y_1$. Feed in $x_2=x_1(t-t_0)$ to get $y_2$. Compare $y_2$ with $y_1(t-t_0)$; the system is time-invariant if they're equal.
- **Linear:** does $a_1x_1+a_2x_2\to a_1y_1+a_2y_2$ hold?

---

## Q1. Memory, causality, time-invariance, linearity

### (a) $y(t)=|x(t)|$
- **(i) Memory:** $y(t)$ uses only the present input, so the system is **memoryless**.
- **(ii) Causality:** the output at any $t_0$ depends only on inputs at $t\le t_0$ (in fact only at $t_0$), so it is **causal**.
- **(iii) Time-invariance:**
  1. Arbitrary input $x_1$ gives $y_1(t)=|x_1(t)|$.
  2. The shifted input $x_2(t)=x_1(t-t_0)$ gives $y_2(t)=|x_2(t)|=|x_1(t-t_0)|$.
  3. Shifting the original output gives $y_1(t-t_0)=|x_1(t-t_0)|$.
  4. $y_2(t)=y_1(t-t_0)$, so it is **time-invariant**.
- **(iv) Linearity:**
  1. $x_1$ and $x_2$ give $|x_1(t)|$ and $|x_2(t)|$.
  2. $x_1+x_2$ gives $|x_1(t)+x_2(t)|$.
  3. In general $|x_1+x_2|\ne|x_1|+|x_2|$. (Why: try $x_1=1$, $x_2=-1$; the left side is 0 and the right side is 2.)
  4. So it is **non-linear**.

**Answer: memoryless, causal, time-invariant, non-linear.**

### (b) $y(t)=x(t-1)$
- **(i) Memory:** it uses the input from 1 s earlier, so it **has memory**.
- **(ii) Causality:** it never uses future inputs, so it is **causal**.
- **(iii) Time-invariance:**
  1. $y_1(t)=x_1(t-1)$.
  2. $x_2(t)=x_1(t-t_0)$ gives $y_2(t)=x_2(t-1)=x_1(t-t_0-1)$.
  3. $y_1(t-t_0)=x_1(t-t_0-1)$.
  4. They are equal, so it is **time-invariant**.
- **(iv) Linearity:**
  1. $x_1$ and $x_2$ give $x_1(t-1)$ and $x_2(t-1)$.
  2. $x_1+x_2$ gives $x_1(t-1)+x_2(t-1)$.
  3. More generally, $a_1x_1+a_2x_2\to a_1y_1+a_2y_2$, so it is **linear**.

**Answer: with memory, causal, time-invariant, linear.**

---

## Q2. Ideal sampling $y(t)=x(t)\sum_n\delta(t-nT_s)$: linear? time-invariant? causal?

**Linearity**
1. Let $y_1=x_1\sum_n\delta(t-nT_s)$ and $y_2=x_2\sum_n\delta(t-nT_s)$.
2. The input $\alpha x_1+\beta x_2$ gives
   $$y_o(t)=(\alpha x_1+\beta x_2)\sum_n\delta(t-nT_s)=\alpha x_1\sum_n\delta(t-nT_s)+\beta x_2\sum_n\delta(t-nT_s)=\alpha y_1+\beta y_2.$$
3. So it is **linear**.

**Time-invariance**
1. Use the sampling property of the delta, $x(t)\delta(t-a)=x(a)\delta(t-a)$, to rewrite the output:
   $$y(t)=\sum_n x(nT_s)\,\delta(t-nT_s).$$
2. Feed in the shifted input $x(t-t_0)$:
   $$y_o(t)=x(t-t_0)\sum_n\delta(t-nT_s)=\sum_n x(nT_s-t_0)\,\delta(t-nT_s).$$
3. Compare with the shifted output:
   $$y(t-t_0)=\sum_n x(nT_s)\,\delta(t-t_0-nT_s).$$
4. These differ. (Why: in $y_o$ the impulses stay on the fixed grid $nT_s$; in $y(t-t_0)$ the grid itself moves by $t_0$.)
5. So it is **not time-invariant**.

**Causality:** the output never depends on future input values, so it is **causal**.

**Answer: linear, not time-invariant, causal.**

---

## Q3. Step response $g(t)=\Pi\!\left(\frac{t-1}{2}\right)$; find the output for $x(t)=\Pi(t)$, and decide whether the system is causal

1. **Caution:** $g$ is the response to $u(t)$, **not** the impulse response. The impulse response would need $x=\delta(t)$.
2. Write the new input as a difference of two steps:
   $$\Pi(t)=u\!\left(t+\tfrac12\right)-u\!\left(t-\tfrac12\right).$$
3. **Time invariance:** a shifted step gives a shifted step response:
   $$u\!\left(t+\tfrac12\right)\to g\!\left(t+\tfrac12\right),\qquad u\!\left(t-\tfrac12\right)\to g\!\left(t-\tfrac12\right).$$
4. **Linearity:** the difference of inputs gives the difference of outputs:
   $$y(t)=g\!\left(t+\tfrac12\right)-g\!\left(t-\tfrac12\right)=\Pi\!\left(\frac{t-\frac12}{2}\right)-\Pi\!\left(\frac{t-\frac32}{2}\right).$$
5. **Causal:** yes. The output doesn't depend on future input values. (Why: $g$ is zero before $t=0$, so the step response doesn't start before the step does.)

**Answer: $y(t)=\Pi\!\left(\frac{t-1/2}{2}\right)-\Pi\!\left(\frac{t-3/2}{2}\right)$; the system is causal.**
Equivalently, $y=+1$ on $[-\tfrac12,\tfrac12]$, $0$ on $(\tfrac12,\tfrac32)$, and $-1$ on $[\tfrac32,\tfrac52]$.

---

## Q4. Outputs of LTI systems, $y=x*h$

### (a) $h(t)=\delta(t-1)$, $x(t)=\sin\!\left(\frac{\pi t}{2}\right)$
1. By the shifting property of the delta:
   $$y(t)=\int_{-\infty}^{\infty}\sin\!\left(\tfrac{\pi\tau}{2}\right)\delta(t-\tau-1)\,d\tau=\sin\!\left(\tfrac{\pi(t-1)}{2}\right)=\sin\!\left(\tfrac{\pi t}{2}-\tfrac{\pi}{2}\right)=-\cos\!\left(\tfrac{\pi t}{2}\right).$$
2. **Take-away:** convolving with $\delta(t)$ returns the input unchanged. Convolving with $\delta(t-t_0)$ returns the input delayed by $t_0$.

**Answer: $y(t)=-\cos\!\left(\frac{\pi t}{2}\right)$.**

### (b) $h(t)=u(t)$, $x(t)=(t+1)u(t+1)$
1. Set up the integral:
   $$y(t)=\int_{-\infty}^{\infty}(\tau+1)\,u(\tau+1)\,u(t-\tau)\,d\tau=\int_{-1}^{t}(\tau+1)\,d\tau.$$
   (Why these limits: $u(\tau+1)$ needs $\tau\ge-1$, and $u(t-\tau)$ needs $\tau\le t$.)
2. Integrate:
   $$y(t)=\left(\tfrac12\tau^2+\tau\right)\Big|_{-1}^{t}=\left(\tfrac12t^2+t\right)-\left(\tfrac12-1\right)=\tfrac12t^2+t+\tfrac12.$$
3. The integral is empty when $t<-1$, so multiply by $u(t+1)$.

**Answer: $y(t)=\left(\frac12t^2+t+\frac12\right)u(t+1)$.**

### (c) $h(t)=u(t)-u(t-2)$, $x(t)=r(t)u(3-t)$: graphical convolution
1. **Choose which signal to fix.** Convolution is commutative, so either one can stay put. Fix the more complicated shape: $x$, a ramp from 0 to 3 on $[0,3]$. Flip and slide $h$, a unit box on $[0,2]$.
2. $h(t-\tau)$ is non-zero for $\tau\in[t-2,t]$, and $x(\tau)$ is non-zero for $\tau\in[0,3]$. So
   $$y(t)=\int_{\max(0,\,t-2)}^{\min(3,\,t)}h(t-\tau)\,x(\tau)\,d\tau=\int_{\max(0,\,t-2)}^{\min(3,\,t)}\tau\,d\tau.$$
3. Go through the cases one at a time:

| Case | Overlap $[\max(0,t-2),\,\min(3,t)]$ | Calculation | $y(t)$ |
|---|---|---|---|
| $t<0$ | none (the box is entirely left of the ramp) | — | $0$ |
| $0\le t<2$ | $[0,t]$ | $\int_0^t\tau\,d\tau=\frac{\tau^2}{2}\Big\vert_0^t$ | $\frac{t^2}{2}$ |
| $2\le t<3$ | $[t-2,t]$ | $\frac{t^2}{2}-\frac{(t-2)^2}{2}$ | $2t-2$ |
| $3\le t<5$ | $[t-2,3]$ | $\frac{9}{2}-\frac{(t-2)^2}{2}$ | $\frac{(5-t)(t+1)}{2}$ |
| $t\ge5$ | none (the box has slid past the ramp) | — | $0$ |

**Answer:** the piecewise $y(t)$ in the table. It is continuous: 2 at $t=2$, peak 4 at $t=3$, back to 0 at $t=5$.

---

## Q5. BIBO stability

"Stable" means every bounded input produces a bounded output.

### (a) $y[n]=\sum_{k=-\infty}^{n}x[k]$ (accumulator)
1. To show instability, one bounded input with an unbounded output is enough. Take $x[n]=u[n]$, which is bounded by 1.
2. Then
   $$y[n]=\sum_{k=-\infty}^{n}u[k]=\sum_{k=0}^{n}u[k]=\begin{cases}n+1&n\ge0\\0&n<0\end{cases}$$
3. As $n\to\infty$, $y[n]\to\infty$.

**Answer: unstable.**

### (b) $y[n]=\frac1M\sum_{k=0}^{M-1}x[n-k]$ (moving average)
1. Write out the sum: $y[n]=\frac1M\big(x[n]+x[n-1]+\dots+x[n-M+1]\big)$, the average of the last $M$ samples.
2. Suppose the input is bounded: $|x[n]|<B_x$.
3. Then the output is bounded too:
   $$|y[n]|\le\frac1M(M\cdot B_x)=B_x.$$

**Answer: stable.**

---

## Q6. $h(t)=e^{-t}u(t)$, $H(\omega)=\frac{1}{1+j\omega}$; output for $x(t)=\cos(t)+\sin(3t)$

1. **Why the frequency domain:** computing $y=h*x$ directly in time is messy. Complex exponentials are much easier, because an LTI system only scales each one:
   $$x=\sum_n C_ne^{j\omega_nt}\ \Rightarrow\ y=\sum_n C_nH(\omega_n)e^{j\omega_nt}.$$
2. **Euler form of the input:**
   $$x(t)=\tfrac12e^{jt}+\tfrac12e^{-jt}+\tfrac{1}{2j}e^{j3t}-\tfrac{1}{2j}e^{-j3t}.$$
3. **Scale each term by $H$ at its own frequency:**
   $$y(t)=\tfrac12H(1)e^{jt}+\tfrac12H(-1)e^{-jt}+\tfrac1{2j}H(3)e^{j3t}-\tfrac1{2j}H(-3)e^{-j3t}.$$
4. **Substitute $H$:**
   $$y(t)=\frac{1}{2(1+j)}e^{jt}+\frac{1}{2(1-j)}e^{-jt}+\frac{1}{2j(1+3j)}e^{j3t}-\frac{1}{2j(1-3j)}e^{-j3t}.$$

**Answer: as in step 4.**
(Real form, if you want it: $|H(1)|=\frac1{\sqrt2}$ with phase $-\frac{\pi}{4}$, and $|H(3)|=\frac1{\sqrt{10}}$ with phase $-\tan^{-1}3$, so
$y(t)=\frac{1}{\sqrt2}\cos\!\left(t-\frac{\pi}{4}\right)+\frac{1}{\sqrt{10}}\sin(3t-\tan^{-1}3)$. Checked numerically against step 4.)

---

## Exercises

### Ex 1. $\mathcal H[x(t)]=a$ (constant output). For which $a$ is it linear, and for which is it time-invariant?
- **Time-invariance:**
  1. The test needs $\mathcal H[x(t-t_0)]=y(t-t_0)$ for every $t_0$.
  2. Here both sides equal the constant $a$, whatever $a$ is.
  3. So it is time-invariant **for any $a$**.
- **Linearity:**
  1. Linearity needs $\mathcal H[\alpha x_1+\beta x_2]=\alpha y_1+\beta y_2$.
  2. The left side is $a$; the right side is $(\alpha+\beta)a$.
  3. For these to agree for every $\alpha$ and $\beta$, we need $a=0$.

**Answer: linear only when $a=0$; time-invariant for every $a$.**

### Ex 2. Linear? Time-invariant? Causal? Impulse response if possible
*Preliminary remark (from the official solution, reworded): if a system is time-varying, it has no single impulse response in the usual sense, because the response depends on when the impulse arrives.*

**(a) $\frac{d^2y}{dt^2}+3\frac{dy}{dt}-t\,y(t)=3x(t+2)$**
- **Linear:** the equation has no constant terms and no non-linear functions of $y$.
- **Time-variant:** the coefficient multiplying $y(t)$ is $t$, which changes with time.
- **Not causal:** the input enters as $x(t+2)$, which is 2 s in the future.

**Answer: linear, time-variant, not causal.**
> **⚠ Check:** the answer key at the bottom of the question sheet (`Tutorial3(3).pdf`) says "time-invariant" here. The official worked solution says **time-variant**, which is correct because of the $-t\,y(t)$ term. The answer key has a typo.

**(b) $y(t)-x(t)-x(t-4)=3$**
- **Non-linear:** the constant $+3$ means a zero input gives a non-zero output.
- **Time-invariant:** all coefficients are constants.
- **Causal:** only $x(t)$ and $x(t-4)$ appear, so no future inputs are used.
- **Impulse response:** set $x=\delta(t)$ to get $h(t)=\delta(t)+\delta(t-4)+3$.

**Answer: non-linear, time-invariant, causal; $h(t)=\delta(t)+\delta(t-4)+3$.**
> **⚠ Check (conceptual):** this $h$ is the response to $\delta(t)$, but it does **not** describe the system the way an LTI impulse response does. For example, $(x*h)(t)$ adds $3\int x$, not 3. Use it only as "the output when the input is $\delta$".

**(c) $y(t)=x(t)+3x(t-2)+\int_{t-10}^{t-3}x(\tau)\,d\tau$**
- **LTI:** integration is a linear operation, and a window that slides with $t$ is time-invariant. So the system is linear and time-invariant.
- **Impulse response:** set $x=\delta(t)$:
  $$h(t)=\delta(t)+3\delta(t-2)+\int_{t-10}^{t-3}\delta(\tau)\,d\tau=\delta(t)+3\delta(t-2)+u(t-3)-u(t-10).$$
  (Why: the integral is 1 exactly when $0$ lies in the window, i.e. when $3\le t\le10$.)
- **Causal:** $h(t)$ is non-zero only for $t\ge0$.

**Answer: linear, time-invariant, causal; $h(t)=\delta(t)+3\delta(t-2)+u(t-3)-u(t-10)$.**

**(d) $y(t)=\sin(2t)\,x(t)$**
- **Time-invariance:**
  1. $y_1(t)=\sin(2t)x_1(t)$.
  2. $x_2=x_1(t-t_0)$ gives $y_2(t)=\sin(2t)x_1(t-t_0)$.
  3. But $y_1(t-t_0)=\sin\big(2(t-t_0)\big)x_1(t-t_0)$.
  4. These are not equal, so the system is **not time-invariant**.
- **Linearity:**
  $$a_1x_1+a_2x_2\to\sin(2t)[a_1x_1+a_2x_2]=a_1\sin(2t)x_1+a_2\sin(2t)x_2=a_1y_1+a_2y_2,$$
  so it is **linear**.
- **Causal:** the output uses only the present input.

**Answer: linear, not time-invariant, causal.**

### Ex 3. $h(t)=u(t)$: output for each input, using the convolution integral
With $h=u$, the convolution reduces to a running integral: $y(t)=\int_{-\infty}^{t}x(\tau)\,d\tau$.

- **(a) $x=u(t-2)$:**
  $$y(t)=\int_{-\infty}^{\infty}u(\tau-2)u(t-\tau)\,d\tau=\int_2^t1\,d\tau=\begin{cases}0&t<2\\t-2&t\ge2\end{cases}$$
  **Answer: $y(t)=(t-2)u(t-2)$.**
- **(b) $x=e^{-2t}u(t)$:**
  $$y(t)=\int_{-\infty}^{\infty}e^{-2\tau}u(\tau)u(t-\tau)\,d\tau=\int_0^te^{-2\tau}d\tau$$
  **Answer: $y(t)=\tfrac12(1-e^{-2t})u(t)$.**
- **(c) $x=t\,u(t)$:**
  $$y(t)=\int_0^t\tau\,d\tau=\tfrac12\tau^2\Big|_0^t$$
  **Answer: $y(t)=\tfrac12t^2u(t)$.**
- **(d) $x=t^2u(t)$:**
  $$y(t)=\int_0^t\tau^2\,d\tau$$
  **Answer: $y(t)=\tfrac13t^3u(t)$.**
  > **⚠ Check:** the answer key on the question sheet prints $\tfrac12t^3u(t)$. The official worked solution gives $\tfrac13t^3u(t)$, which is correct: $\int_0^t\tau^2\,d\tau=t^3/3$. The answer key has a typo.
- **(e) $h(t)=\sum_{n=-\infty}^{\infty}\delta(t-2n)$, arbitrary $x(t)$:**
  1. Each impulse shifts the input: $x(t)*\delta(t-2n)=x(t-2n)$.
  2. By linearity, convolving with the whole train adds up all the shifted copies:
     $$y(t)=x(t)*\sum_n\delta(t-2n)=\sum_n x(t)*\delta(t-2n)=\sum_n x(t-2n).$$
  3. The result is the **periodic extension** of $x$, with the same period (2) as the impulse train.

  **Answer: $y(t)=\sum_{n=-\infty}^{\infty}x(t-2n)$.**

### Ex 3(f). $h(t)=4e^{-5t}\big(u(t-3)-u(t-6)\big)$, $x(t)=\Pi\!\left(\frac{t-3}{2}\right)$: graphical approach
The official solution uses the form $y(t)=\int h(\tau)\,x(t-\tau)\,d\tau$. It keeps $h$ fixed (a decaying exponential living on $[3,6]$), and flips and slides the box $x$. It then splits the result into five cases by how much the box overlaps $h$.

1. **Locate the flipped box.** $x$ is 1 on $[2,4]$. (Why: centre 3, width 2.) So $x(t-\tau)=1$ when $2\le t-\tau\le4$, which means
   $$\tau\in[t-4,\ t-2].$$
2. **Overlap with $h$:** $[\max(3,t-4),\ \min(6,t-2)]$.
3. **The five cases** follow from the same "no overlap / entering / fully inside / leaving / no overlap" structure as the official solution:

| Case | Overlap | $y(t)=\int4e^{-5\tau}d\tau$ over the overlap |
|---|---|---|
| $t<5$ | none | $0$ |
| $5\le t<7$ | $[3,\ t-2]$ | $-\tfrac45\big(e^{-5(t-2)}-e^{-15}\big)$ |
| $7\le t<8$ | $[t-4,\ t-2]$ | $-\tfrac45\big(e^{-5(t-2)}-e^{-5(t-4)}\big)$ |
| $8\le t<10$ | $[t-4,\ 6]$ | $-\tfrac45\big(e^{-30}-e^{-5(t-4)}\big)$ |
| $t\ge10$ | none | $0$ |

(Each integral uses $\int4e^{-5\tau}d\tau=-\tfrac45e^{-5\tau}$.)

**Answer: the table above. The output is non-zero only for $5\le t<10$.**

> **⚠ Check:** the official solution (and the answer key on the question sheet) puts the case boundaries at $t=3,5,6,8$. It gives
> - $-\frac45(e^{-5t}-e^{-15})$ on $[3,5)$,
> - $-\frac45(e^{-5t}-e^{-5(t-2)})$ on $[5,6)$,
> - $-\frac45(e^{-30}-e^{-5(t-2)})$ on $[6,8)$.
>
> Those limits correspond to the flipped box sitting on $[t-2,t]$, which is correct for an input on $[0,2]$, i.e. $\Pi\!\left(\frac{t-1}{2}\right)$.
> But the question's input $\Pi\!\left(\frac{t-3}{2}\right)$ sits on $[2,4]$. The official sketch of $x$ even shows it on $[2,4]$. So every boundary should move 2 s later.
> A numerical convolution confirms the shifted table above. The official expressions do match a direct numerical convolution with the input on $[0,2]$.

> **⚠ Check (document issue):** in the official solution PDF, the restated question list shows a *different* part (f): "$h(t)=u(t-3)$, $x(t)=e^{2t}u(-t)$", but the worked answer then solves the $4e^{-5t}$ version above. In case you are given that version:
> $$y(t)=\int_{-\infty}^{\min(0,\,t-3)}e^{2\tau}d\tau=\begin{cases}\tfrac12e^{2(t-3)}&t<3\\\tfrac12&t\ge3\end{cases}$$
> (This is my own solution; the PDF doesn't solve it.)

### Ex 4. $h[n]=\left(\frac47\right)2^{n-1}u[-n]+\frac{11}{7}\left(\frac14\right)^{n-1}u[n-1]$

**(a) Causal?**
1. A causal LTI system needs $h[n]=0$ for every $n<0$.
2. The $u[-n]$ term is non-zero for $n\le0$, so $h$ has values at negative $n$.

**Answer: non-causal.**

**(b) BIBO stable?**
1. For an LTI system, test whether $\sum|h[n]|<\infty$. Both pieces are positive, so the absolute values can be dropped:
   $$\sum_{n=-\infty}^{\infty}h[n]=\sum_{n=-\infty}^{0}\left(\tfrac47\right)2^{n-1}+\sum_{n=1}^{\infty}\tfrac{11}{7}\left(\tfrac14\right)^{n-1}.$$
2. **Left-sided piece.** Flip the index ($n\to-n$) so it becomes a sum over $n\ge0$:
   $$\sum_{n=-\infty}^{0}\left(\tfrac47\right)2^{n-1}=\left(\tfrac47\right)\sum_{n=0}^{\infty}\left(\tfrac12\right)^{n+1}=\left(\tfrac47\right)\left(\tfrac12\right)\sum_{n=0}^{\infty}\left(\tfrac12\right)^{n}=\left(\tfrac27\right)\frac{1}{1-\frac12}=\frac47.$$
3. **Right-sided piece.** Let $m=n-1$:
   $$\sum_{n=1}^{\infty}\tfrac{11}{7}\left(\tfrac14\right)^{n-1}=\tfrac{11}{7}\sum_{m=0}^{\infty}\left(\tfrac14\right)^m=\tfrac{11}{7}\cdot\frac{1}{1-\frac14}=\frac{44}{21}.$$
4. **Total:** $\sum h[n]=\frac47+\frac{44}{21}=\frac{8}{3}<\infty$. (The official solution stops at the unsimplified sum; $\frac83$ is the simplified value, checked numerically.)

**Answer: BIBO stable** (the impulse response is absolutely summable).
