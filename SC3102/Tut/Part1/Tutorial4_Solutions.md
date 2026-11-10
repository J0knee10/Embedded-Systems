# SC3102 Tutorial 4: Fourier Series and CT Fourier Transforms — Worked Solutions

*Worked solutions written from the official NTULearn solutions as a reference (not a copy).*
The steps follow the official method and order; the explanations are my own wording.
Official source: "Tutorial 4: Solutions" (typed PDF, 8 pages). Questions: `Tutorial4(1).pdf`.
⚠ marks a real problem in the official solution. Every ⚠ is collected, together with practical shortcuts, in
[Disagreements.md](Disagreements.md).

**Conventions used in this course**
- **Complex Fourier series:** $x(t)=\sum_k C_ke^{jk\omega_0t}$, with $C_k=\frac1{T_0}\int_{T_0}x(t)e^{-jk\omega_0t}dt$ and $\omega_0=2\pi/T_0$.
- **Fourier transform in $f$ (Hz):** $X(f)=\int x(t)e^{-j2\pi ft}dt$.
- **Parseval for a periodic signal:** $P=\sum_k|C_k|^2$.

---

## Q1. Complex Fourier series

### (a) $x(t)=\cos(4t)+\sin(6t)$
1. **Find the fundamental.**
   - The two terms have periods $\pi/2$ and $\pi/3$; their common period is $T_0=\pi$.
   - So $\omega_0=2\pi/T_0=2$.
   - Target form: $x(t)=\sum_kC_ke^{jk\omega_0t}=\sum_kC_ke^{j2kt}$.
2. **Expand with Euler's formula:**
   $$x(t)=\tfrac12\left(e^{j4t}+e^{-j4t}\right)+\tfrac1{2j}\left(e^{j6t}-e^{-j6t}\right)
   =-\tfrac1{2j}e^{-j6t}+\tfrac12e^{-j4t}+\tfrac12e^{j4t}+\tfrac1{2j}e^{j6t}.$$
3. **Read off the coefficients.** $e^{j4t}$ is $k=2$ and $e^{j6t}$ is $k=3$ (because $\omega_0=2$).

**Answer: $C_{-3}=-\frac1{2j}$, $C_{-2}=\frac12$, $C_2=\frac12$, $C_3=\frac1{2j}$; all other $C_k=0$.**

### (b) $x(t)=\sum_n y(t-3n)$, with $y(t)=e^{-t}$ on $[0,3]$
1. **Fundamental.** The copies of $y$ are placed every 3 s, so $T_0=3$ and $\omega_0=2\pi/3$:
   $$x(t)=\sum_kC_ke^{jk\omega_0t}=\sum_kC_ke^{j\frac{2\pi k}{3}t}.$$
2. **Coefficient integral over one period.** On $[0,3]$, $x(t)=e^{-t}$, so
   $$C_k=\frac1{T_0}\int_0^{T_0}x(t)e^{-jk2\pi f_0t}dt=\frac13\int_0^3e^{-t}e^{-j\frac{2\pi k}{3}t}dt=\frac13\int_0^3e^{-\left(1+j\frac{2\pi k}{3}\right)t}dt.$$
   (Why the exponents combine: $e^{-t}e^{-jat}=e^{-(1+ja)t}$, which turns it into a single exponential.)
3. **Integrate:**
   $$C_k=-\frac{1}{3\left(1+j\frac{2\pi k}{3}\right)}e^{-\left(1+j\frac{2\pi k}{3}\right)t}\Big|_0^3=\frac{1}{3\left(1+j\frac{2\pi k}{3}\right)}\left(1-e^{-(3+j2\pi k)}\right)=\frac{1-e^{-3}}{3\left(1+j\frac{2\pi k}{3}\right)}.$$
   (Why the last step: $e^{-j2\pi k}=1$ for every integer $k$.)
4. **Assemble the series.**

**Answer:**
$$x(t)=\frac{1-e^{-3}}{3}\sum_{k=-\infty}^{\infty}\frac{e^{j\frac{2\pi k}{3}t}}{1+j\frac{2\pi k}{3}}.$$
(Checked numerically for $k=0,1,-2$.)

---

## Q2. Average power of $x(t)=e^{jt}+\cos(2t+1)-\sin(5t)$ using Parseval

1. **Euler form:**
   $$x(t)=e^{jt}+\tfrac12e^{j(2t+1)}+\tfrac12e^{-j(2t+1)}-\tfrac1{2j}e^{j5t}+\tfrac1{2j}e^{-j5t}.$$
2. **Identify the series.** It is periodic with $\omega_0=1$, so the coefficients are
   $$C_{-5}=\tfrac1{2j},\quad C_{-2}=\tfrac12e^{-j},\quad C_1=1,\quad C_2=\tfrac12e^{j},\quad C_5=-\tfrac1{2j},$$
   and all other $C_k=0$. (Why the constant phase factors appear: $e^{\pm j(2t+1)}=e^{\pm j}e^{\pm j2t}$.)
3. **Apply Parseval.** The phase factors have magnitude 1, so they don't change any $|C_k|$:
   $$P=\sum_k|C_k|^2=|C_{-5}|^2+|C_{-2}|^2+|C_1|^2+|C_2|^2+|C_5|^2=4\times\tfrac14+1.$$

**Answer: $P=2$.**

---

## Q3. Fourier transforms

### (a) $x(t)=\cos(2\pi f_0t)$
1. **Definition plus Euler:**
   $$X(f)=\int\cos(2\pi f_0t)e^{-j2\pi ft}dt=\tfrac12\int\left(e^{j2\pi f_0t}+e^{-j2\pi f_0t}\right)e^{-j2\pi ft}dt$$
   $$=\tfrac12\int e^{-j2\pi(f-f_0)t}dt+\tfrac12\int e^{-j2\pi(f+f_0)t}dt.$$
2. **Known pair:** $\mathcal F\{1\}=\int e^{-j2\pi ft}dt=\delta(f)$.
3. **Frequency-shifting property:** each integral above is that same delta, moved to $f=\pm f_0$:
   $$X(f)=\tfrac12\big(\delta(f-f_0)+\delta(f+f_0)\big).$$

**Answer: $X(f)=\frac12\big(\delta(f-f_0)+\delta(f+f_0)\big)$.** Sketch: two arrows of weight $\tfrac12$ at $\pm f_0$.

### (b) $x(t)=t\,e^{-\alpha t}u(t)$, $\alpha>0$
1. **Definition:**
   $$X(f)=\int_{-\infty}^{\infty}t\,e^{-\alpha t}u(t)e^{-j2\pi ft}dt=\int_0^{\infty}t\,e^{-(\alpha+j2\pi f)t}dt.$$
2. **Integration by parts**, $\int u\,dv=uv-\int v\,du$, with $u=t$:
   $$X(f)=\left[\frac{-t}{\alpha+j2\pi f}e^{-(\alpha+j2\pi f)t}-\frac{1}{(\alpha+j2\pi f)^2}e^{-(\alpha+j2\pi f)t}\right]_0^{\infty}=\frac{1}{(\alpha+j2\pi f)^2}.$$
   (Why only one term survives: at $\infty$ both terms vanish because $\alpha>0$; at 0 only the second term is non-zero.)

**Answer: $X(f)=\dfrac{1}{(\alpha+j2\pi f)^2}$.**

---

## Q4. Three rectangular pulses (height $A$, width $\tau$, centred at $-T_0$, $0$, $+T_0$)

1. **Name the pieces.**
   - $x_1(t)=A$ for $|t|\le\tau/2$: the centre pulse.
   - $x_2(t)=x_1(t+T_0)$: the left pulse.
   - $x_3(t)=x_1(t-T_0)$: the right pulse.
   - So $x(t)=x_1(t)+x_1(t+T_0)+x_1(t-T_0)$.
2. **Time-shifting property:** a shift by $\pm T_0$ multiplies the transform by $e^{\pm j2\pi fT_0}$:
   $$X(f)=X_1(f)+X_1(f)e^{j2\pi fT_0}+X_1(f)e^{-j2\pi fT_0}=X_1(f)\big[1+2\cos(2\pi fT_0)\big].$$
   (Why the cosine: $e^{j\theta}+e^{-j\theta}=2\cos\theta$.)
3. **Transform of one pulse:**
   $$X_1(f)=\int_{-\tau/2}^{\tau/2}Ae^{-j2\pi ft}dt=A\frac{e^{-j2\pi ft}}{-j2\pi f}\Bigg|_{-\tau/2}^{\tau/2}=\frac{A}{\pi f}\cdot\frac{e^{j\pi f\tau}-e^{-j\pi f\tau}}{2j}=\frac{A}{\pi f}\sin(\pi f\tau)=A\tau\frac{\sin(\pi f\tau)}{\pi f\tau}=A\tau\,\mathrm{sinc}(f\tau).$$
4. **Substitute** $X_1$ into step 2.

**Answer: $X(f)=A\tau\,\mathrm{sinc}(f\tau)\big(1+2\cos(2\pi fT_0)\big)$.**
(The figure labels the right pulse "$T$" and the left one "$-T_0$". Both the official solution and this one take them to be the same spacing $T_0$.)

---

## Q5. $x(t)=A+B\cos(2\pi f_0t)$ into $h(t)=2W\mathrm{sinc}(2Wt)$, with $f_0=100$ Hz and $W=1000$ Hz

1. **Output of an LTI system:** $y=x*h$. Picture it as $x(t)\to[h(t)]\to y(t)$.
2. **Convolution theorem:** $x*h\leftrightarrow X(f)H(f)$, so $Y(f)=X(f)H(f)$.
3. **Input spectrum:**
   $$X(f)=A\delta(f)+\tfrac B2\big[\delta(f-f_0)+\delta(f+f_0)\big].$$
4. **Filter response:** from the given pair $\mathrm{sinc}(2Wt)\leftrightarrow\frac1{2W}\Pi\!\left(\frac f{2W}\right)$,
   $$H(f)=\mathcal F[2W\mathrm{sinc}(2Wt)]=\Pi\!\left(\tfrac f{2W}\right).$$
   This is an ideal low-pass filter with gain 1 for $|f|<1000$ Hz.
5. **Multiply (graphical step).** The spikes at $0$ and $\pm100$ Hz all lie inside the pass band, so each is multiplied by 1:
   $$Y(f)=A\delta(f)+\tfrac B2\big[\delta(f-f_0)+\delta(f+f_0)\big].$$
6. **Back to time:** $y(t)=\mathcal F^{-1}[Y(f)]=x(t)$.

**Answer: $y(t)=A+B\cos(2\pi f_0t)$.** The signal passes through unchanged.

**Power spectral density of the output:**
$$S_y(f)=A^2\delta(f)+\tfrac{B^2}{4}\big[\delta(f-f_0)+\delta(f+f_0)\big],\qquad P=A^2+2\cdot\tfrac{B^2}{4}=A^2+\tfrac{B^2}{2}.$$
Sketch: an arrow of weight $A^2$ at 0 and arrows of weight $B^2/4$ at $\pm100$ Hz.
> Note: the official solution writes this as $|Y(f)|^2$. Strictly, you can't square a delta; for a periodic signal the PSD is $\sum|C_k|^2\delta(f-kf_0)$, which gives the same expression. See [Disagreements.md](Disagreements.md).

---

## Exercises

### Ex 1. Complex Fourier series of $x(t)=\sin^2(t)$
1. **Fundamental.** $\sin^2t=\frac12(1-\cos2t)$, so $T_0=\pi$ and $\omega_0=2$. Target form: $x=\sum C_ke^{j2kt}$.
2. **Euler form:**
   $$\sin^2t=\left(\frac{e^{jt}-e^{-jt}}{2j}\right)^2=-\tfrac14\left(e^{j2t}-2+e^{-j2t}\right)=-\tfrac14e^{-j2t}+\tfrac12-\tfrac14e^{j2t}.$$
   (Why the minus sign: $(2j)^2=-4$.)
3. **Read off the coefficients.** $e^{j2t}$ is $k=1$ because $\omega_0=2$.

**Answer: $C_{-1}=-\frac14$, $C_0=\frac12$, $C_1=-\frac14$; all other $C_k=0$.**

### Ex 2. Evaluate $\displaystyle\int_{-\infty}^{\infty}\frac{\sin(3\tau)}{\tau}\cdot\frac{\sin(t-\tau)}{t-\tau}\,d\tau$ with the convolution theorem
1. **Recognise a convolution.** The integral is $x*y$ with $x(t)=\frac{\sin t}{t}$ and $y(t)=\frac{\sin3t}{t}$. By the convolution theorem, $x*y\leftrightarrow X(f)Y(f)$.
2. **Find $X(f)$ by duality.** Start from the given pair, $A\Pi(t/\tau)\leftrightarrow A\tau\frac{\sin(\pi f\tau)}{\pi f\tau}$.
   - Choose $A=\pi$ and $\tau=1/\pi$: $\pi\Pi(\pi t)\leftrightarrow\frac{\sin f}{f}$.
   - Duality (if $x(t)\leftrightarrow X(f)$, then $X(t)\leftrightarrow x(-f)$) gives
   $$\frac{\sin t}{t}\leftrightarrow\pi\Pi(-\pi f)=\pi\Pi(\pi f)=X(f).$$
   (Why the sign can be dropped: the rectangle is even.)
3. **Find $Y(f)$ the same way.**
   - Write $\frac{\sin3t}{t}=\frac{3\sin3t}{3t}$.
   - Choose $A=\pi$ and $\tau=3/\pi$, then apply duality:
   $$\frac{\sin3t}{t}\leftrightarrow\pi\Pi\!\left(\tfrac{\pi f}{3}\right)=Y(f).$$
4. **Multiply.**
   - $X(f)$ is a box of height $\pi$ on $|f|\le\frac1{2\pi}$.
   - $Y(f)$ is a wider box of height $\pi$ on $|f|\le\frac3{2\pi}$.
   - Their product is the narrower box, at height $\pi^2$:
   $$X(f)Y(f)=\begin{cases}\pi^2&|f|\le\frac1{2\pi}\\0&\text{else}\end{cases}=\pi^2\Pi(\pi f).$$
5. **Invert.** Using the pair with duality, $A\tau\frac{\sin(\pi t\tau)}{\pi t\tau}\leftrightarrow A\Pi(f/\tau)$, take $A=\pi^2$ and $\tau=1/\pi$:
   $$\mathcal F^{-1}\big(X(f)Y(f)\big)=\pi\frac{\sin t}{t}.$$

**Answer: $\displaystyle\int_{-\infty}^{\infty}\frac{\sin3\tau}{\tau}\frac{\sin(t-\tau)}{t-\tau}d\tau=\pi\frac{\sin t}{t}$.** (Checked by numerical integration at $t=1.3$.)

### Ex 3. Inverse transform of the staircase $X(\omega)$: height 2 on $|\omega|<1$, height 1 on $1<|\omega|<2$, zero elsewhere
1. **Inverse transform in $\omega$:** $x(t)=\frac1{2\pi}\int X(\omega)e^{j\omega t}d\omega$. Split it at the corners of the staircase:
   $$x(t)=\frac1{2\pi}\left[\int_{-2}^{-1}e^{j\omega t}d\omega+\int_{-1}^{1}2e^{j\omega t}d\omega+\int_{1}^{2}e^{j\omega t}d\omega\right]$$
   $$=\frac1{2\pi}\left[\frac1{jt}e^{j\omega t}\Big|_{-2}^{-1}+\frac2{jt}e^{j\omega t}\Big|_{-1}^{1}+\frac1{jt}e^{j\omega t}\Big|_{1}^{2}\right].$$
2. **Collect into $\frac{e^{ja}-e^{-ja}}{2j}$ shapes:**
   $$x(t)=\frac1{\pi t}\left[\frac{e^{-jt}-e^{-j2t}}{2j}+\frac{2(e^{jt}-e^{-jt})}{2j}+\frac{e^{j2t}-e^{jt}}{2j}\right]=\frac1{\pi t}\left[\frac{e^{j2t}-e^{-j2t}}{2j}+\frac{e^{jt}-e^{-jt}}{2j}\right].$$
3. **Recognise the sines**, using $\frac{e^{ja}-e^{-ja}}{2j}=\sin a$.

**Answer: $x(t)=\dfrac{1}{\pi t}\big(\sin(2t)+\sin(t)\big)$.** (Checked numerically.)
