# SC3102 Lab 3: Discrete Fourier Transforms — Complete Answers & Notes

**Environment:** the repo-wide venv at `D:\Jon\Uni\SYproject\embeddedSys\.venv`
(Python 3.11.9 · numpy 2.4.6 · scipy 1.17.1 · matplotlib 3.11.2). The lab's README pins
Python 3.8 / numpy 1.24, but nothing in `lab_tools.py` depends on that — it ran without errors.

The answers are also written directly into [Lab-03-DFT.ipynb](Lab-03-DFT.ipynb) as markdown
cells under each question, and the notebook has been executed so every plot and audio player is
already in it. All numbers below come from that run (timings in Q3 are machine-dependent).

---

## 0. The one idea this lab is built around

You already know the continuous-time story: a signal $x(t)$ can be written as a sum/integral of
complex exponentials $e^{j\omega t}$, and the Fourier transform tells you how much of each.
This lab is that same idea **after a computer gets involved**, which forces two compromises:

1. **Time becomes discrete** — we only keep samples $x[n] = x_c(nT_s)$. *(Q1: sampling, aliasing)*
2. **We only have a finite block of $N$ samples** — so we can only use $N$ frequencies,
   $\Omega_k = 2\pi k/N$. That is the **DFT**:

$$X[k]=\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N}
\qquad\Longleftrightarrow\qquad
x[n]=\frac{1}{N}\sum_{k=0}^{N-1}X[k]e^{+j2\pi kn/N}$$

Every weird DFT behaviour in this lab traces back to one of those two compromises:

| Compromise | Consequence you see in the lab |
|---|---|
| Sampling at $f_s$ | Frequencies $f$ and $f + mf_s$ look identical → **aliasing** (Q1B). Need $f_s > 2B$. |
| Discrete time | Frequency is now in **rad/sample**, only meaningful in $[-\pi, \pi)$ (Q2A) |
| Only $N$ basis frequencies | Signals "between bins" smear out → **spectral leakage** (Q2A) |
| Finite block | The DFT silently assumes the block **repeats forever** with period $N$ (Q2C) |

Then Q3 shows why we can afford to do this in practice (**FFT**), and Q4 shows what it buys you:
filtering is just **multiplying in the frequency domain** — $Y[k] = H[k]X[k]$ — which is the
"convolution in time = multiplication in frequency" property from Lab 2's world.

**Mapping from what you already know (CT) to this lab (DT):**

| Continuous time | Discrete time (this lab) |
|---|---|
| $\omega$ in rad/s, any value | $\Omega = \omega T_s = 2\pi f/f_s$ in rad/sample, $2\pi$-periodic |
| $\cos(\omega_0 t)$ is always periodic | $\cos(\Omega_0 n)$ periodic only if $\Omega_0/2\pi$ is rational |
| CTFT: integral over all $t$ | DFT: finite sum over $N$ samples, $N$ frequencies |
| Fourier series of a periodic signal | DFT = Fourier series of the **periodic extension** of the block (DTFS) |
| $x(t)\cos(\omega_c t) \leftrightarrow \tfrac12[X(\omega-\omega_c)+X(\omega+\omega_c)]$ | Same modulation property, used in Q4B |

---

## 1. Q1 — Sampling

### 1A. How are samples obtained? ($f_0 = 8$ Hz)

Observations in one second $= f_s$ exactly.

| $f_s$ | samples/s | samples per cycle | $x[n]$ |
|---|---|---|---|
| 32 | 32 | 4 | $1, 0, -1, 0, \dots$ — looks like a cosine |
| 16 | 16 | 2 | $1, -1, 1, -1, \dots$ — exactly at Nyquist ($2f_0$) |
| 8 | 8 | 1 | $1, 1, 1, \dots$ — **looks like a constant!** |

At $f_s = 8$ every sample hits a peak, so an 8 Hz cosine becomes indistinguishable from 0 Hz. That
is aliasing, previewed. Also note: $x[n]$ is *just a list of numbers indexed by integer $n$*; the
"seconds" only exist if you remember $f_s$.

### 1B. Aliasing (3 Hz vs 13 Hz)

- **At $f_s = 16$: indistinguishable.** Max sample difference $= 7.5\times10^{-15}$ (round-off).
  Proof: $\cos(2\pi\cdot13n/16) = \cos(2\pi n - 2\pi\cdot3n/16) = \cos(2\pi\cdot3n/16)$.
- **At $f_s = 32$: distinguishable** (max difference 1.96).
- **All aliases of 3 Hz at $f_s=16$:** $f = |\pm3 + 16m|$ → **3, 13, 19, 29, 35, 45, 51, …**
  (verified by brute force over 0–59 Hz).
- **Sampling rate to distinguish 3 Hz from every signal bandlimited to 13 Hz: $f_s > 26$ Hz**
  (Nyquist: $f_s > 2B$). *Strictly* greater — at exactly 26 Hz, $\sin(2\pi\cdot13t)$ samples to all
  zeros, so adding it to the 3 Hz cosine doesn't change the samples.

> **Rule:** sampling at $f_s$ cannot tell $f$ apart from $f + mf_s$ or $mf_s - f$. Frequencies
> "fold" around multiples of $f_s/2$.

### 1C. Is a sampled periodic signal periodic?

$x[n] = \cos(2\pi \tfrac{f_0}{f_s} n)$ is periodic with period $N$ iff $\tfrac{f_0}{f_s}N \in \mathbb{Z}$.
**Smallest period = denominator of $f_0/f_s$ in lowest terms.**

- $f_0 = 3$: $3/16$ → **period 16** (3 cycles fit in 16 samples). *Not* 16/3 — must be an integer.
- $f_0 = 4$: $4/16 = 1/4$ → **period 4**.
- **Not periodic:** $f_0/f_s$ irrational, e.g. $f_0 = \sqrt2$ Hz or $\pi$ Hz. The continuous
  cosine is periodic but the samples never exactly repeat.
  (Trap: $f_0 = 3.3$ *is* periodic: $33/160$ → period 160.)

This is the same thing your `notes/periodicity` plots show (`cos(n)` never repeats, because
$\Omega_0 = 1$ gives $\Omega_0/2\pi = 1/2\pi$, irrational).

---

## 2. Q2 — The DFT ($N = 64$, $x[n] = A\cos(2\pi cn/N + \phi)$)

### 2A. Magnitude

- **Default ($A=1, c=5, \phi=0$):** only two nonzero bins, $k = \pm5$
  → $\Omega = \pm 2\pi\cdot5/64 = \pm5\pi/32 \approx \pm0.49$ rad/sample, each with $|X[k]|/N = 0.5$.
  Why 0.5: Euler, $A\cos(\Omega n) = \tfrac A2 e^{j\Omega n} + \tfrac A2 e^{-j\Omega n}$.
- **Amplitude** → both peaks scale linearly ($A=2$ → 1.0). **Phase** → magnitude plot unchanged.
- **Non-integer cycles → spectral leakage.** With $c = 5.5$: peaks drop to 0.33 ($k=\pm6$) and
  0.30 ($k=\pm5$), and **all 64 bins** become nonzero. With $c = 5.25$: 0.46 at $k = \pm5$,
  0.15 at $\pm6$, 0.10 at $\pm4$, … The true frequency isn't one of the 64 available basis
  frequencies, so it has to be built out of many of them.

### 2B. Phase

| Setting | $\angle X[5]$ | $\angle X[-5]$ |
|---|---|---|
| $\phi = 0$ | 0 | 0 |
| $\phi = \pi/2$ | $+\pi/2$ | $-\pi/2$ |
| $\phi = 1$ | $+1$ | $-1$ |

- **Positive and negative frequency phases are negatives of each other** — in fact
  $X[-k] = X[k]^*$ (**conjugate symmetry**). This holds for *any real signal*, because the
  imaginary parts have to cancel. Magnitude is even, phase is odd.
- **The signal's phase $\phi$ shows up directly as the DFT phase:** $X[\pm5] = \tfrac{NA}{2}e^{\pm j\phi}$.
- Why phases are only plotted for big coefficients: the angle of $10^{-16} + 10^{-17}j$ is random
  round-off noise, not information.

### 2C. Inverse DFT and the periodic extension

- **Inside the block (0–63): perfect recovery**, error $\sim3\times10^{-16}$. The DFT is just a
  change of basis (an invertible $N\times N$ matrix) — no information lost.
- **Outside the block: the block repeats with period 64** ($e^{j2\pi k(n+N)/N} = e^{j2\pi kn/N}$).
  The DFT implicitly treats your data as one period of a periodic signal — this is the DTFS.
- **$c = 0.5$:** still perfect inside the block, but the extension is the half-cycle copied end to
  end, with a **jump** from $x[63] \approx -1$ to $x[64] = 1$. That artificial discontinuity is
  *why* leakage happens: the DFT is "seeing" a signal with a sharp edge every 64 samples, and sharp
  edges need lots of frequencies.

> **Big connection:** leakage (2A) and periodic extension (2C) are the same phenomenon. If the
> block holds a whole number of cycles, the extension is seamless and the spectrum is clean.
> (In practice you fix this with **windowing** — tapering the block ends — which you'll likely meet later.)

---

## 3. Q3 — Computational cost

`dense_dft` builds $W_{k,n} = e^{-j2\pi kn/N}$ and computes $X = Wx$. It matches `np.fft.fft` to
$\sim10^{-12}$ — **same answer, different algorithm.**

| $N$ | dense | FFT | ratio |
|---|---|---|---|
| 32 | 32 µs | 3.7 µs | 8.6× |
| 64 | 0.20 ms | 4.0 µs | 50× |
| 128 | 0.44 ms | 4.9 µs | 90× |
| 256 | 1.9 ms | 5.3 µs | 364× |
| 512 | 8.5 ms | 7.2 µs | 1 179× |
| 1024 | 32 ms | 12 µs | 2 712× |
| 2048 | 125 ms | 22 µs | 5 559× |

- Dense: ~**4×** per doubling of $N$ → $O(N^2)$. FFT: ~**2×** per doubling → $O(N\log_2 N)$.
  For small $N$ the FFT is flat (~4 µs) because Python call overhead dominates.
- **The gap grows** like $N/\log_2N$. Plus memory: $W$ for $N = 48\,000$ (1 s of audio) would be
  ~37 GB. Without the FFT, DSP on real signals would not be practical — which is why "FFT" and
  "DFT" get used interchangeably.
- Why the FFT is faster (Cooley–Tukey idea): an $N$-point DFT splits into two $N/2$-point DFTs
  (even and odd samples) plus $N$ "twiddle" multiplications; recurse $\log_2 N$ times.

---

## 4. Q4 — Filtering with the DFT

### 4A. Audio denoising

Clean $= (\sin 2\pi220t + 0.3\sin2\pi440t)/1.3$; noise $=$ whistles at 3600 and 4100 Hz; $f_s = 16$ kHz.
Filter: $H[k] = 1$ if $\text{low} \le |f_k| \le \text{high}$, else 0; output $=$ IDFT$(H \cdot X)$.

| Band | What survives | Result |
|---|---|---|
| 100–1000 Hz | 220 + 440 Hz | **= clean signal** (error $7\times10^{-13}$) |
| 100–300 Hz | 220 Hz only | lose the 440 Hz overtone → purer/thinner tone, error 0.23 |
| 3000–5000 Hz (or 3500–4500) | 3600 + 4100 Hz | **= the noise alone** (error $2\times10^{-12}$) |

- The mask uses $|f|$, so it keeps **both** $+f$ and $-f$. If you kept only $+f$, you'd break
  conjugate symmetry and get a complex output.
- It's *perfect* here only because every tone sits exactly on a DFT bin (2 s block, 0.5 Hz bin
  spacing). Real audio would leak, and an ideal brick-wall filter rings — but the principle holds.
- Connection to Lab 2: $Y[k] = H[k]X[k]$ is convolution with $h[n] = \text{IDFT}(H)$, done in
  the frequency domain (strictly *circular* convolution, since the DFT assumes periodicity — see
  the docstring of `lab.fft_filter`).

### 4B. Radio: Amplitude Modulation and frequency-division multiplexing

Two 5 s recordings (`message1.wav` music, `message2.wav` dialogue), resampled to $f_s = 60$ kHz and
lowpassed to $B = 4$ kHz.

1. **Original spectra:** both in 0–4 kHz → **completely overlapping**. Add them and they're gone for good.
2. **Multiply by carriers** (12 kHz, 24 kHz): modulation property shifts each spectrum to
   $f_c \pm B$ → **8–16 kHz** and **20–28 kHz**, at **half height**. **No overlap.**
3. **Sum:** two separate humps with a gap at 16–20 kHz. Sounds like hiss.
4. **Recover:** bandpass $f_c \pm 4$ kHz (isolate the channel) → multiply by $2\cos(2\pi f_ct)$
   (shift back to baseband; the 2 undoes the ½) → lowpass 4 kHz (remove the copy at $2f_c$).
   Result matches the originals: relative error $\sim2\times10^{-11}$, correlation 1.000000.

The math of step 4: $\cos^2\theta = \tfrac12 + \tfrac12\cos2\theta$, so
$2\,x(t)\cos^2(2\pi f_ct) = x(t) + x(t)\cos(2\pi\cdot2f_c t)$ — the lowpass keeps $x(t)$.

**Q4B answers:**
- **Carrier condition:** $|f_{c1} - f_{c2}| \ge 2B$ (each channel is $2B$ wide). Also $f_c \ge B$
  and $f_c + B < f_s/2$ (that's why $f_s = 60$ kHz: $24 + 4 = 28 < 30$).
  Verified by breaking it: carriers 12 & 16 kHz → recovered music has relative error 0.82
  (garbage); both at 12 kHz → a mush of both messages.
- **Wider bandwidth signals:** spread carriers further apart ($\ge 2B$ plus a guard band),
  widen the bandpass to $f_c \pm B$ and recovery lowpass to $B$, push carriers up as needed and
  raise $f_s$ to stay above Nyquist. Real world: AM radio stations (~5 kHz audio) sit 9–10 kHz apart;
  FM stations need ~200 kHz each. More bandwidth per channel = fewer channels.

---

## 5. Key takeaways

1. **Sampling only keeps $x_c(nT_s)$.** Frequencies $f$ and $f \pm mf_s$ produce identical samples
   (aliasing). To keep a signal bandlimited to $B$: **$f_s > 2B$**.
2. **DT frequency is $\Omega = 2\pi f/f_s$ rad/sample**, $2\pi$-periodic, so only $[-\pi,\pi)$ matters.
   $\Omega = \pi$ ↔ $f = f_s/2$ is the fastest possible oscillation ($+1,-1,+1,\dots$).
3. **A sampled sinusoid is periodic only if $f_0/f_s$ is rational**; the period is the reduced denominator.
4. **A real cosine → two DFT spikes at $\pm k$, each $NA/2$.** Read amplitude from $|X|$, phase from $\angle X$.
5. **Real signal ⇒ conjugate symmetry** $X[-k] = X[k]^*$: even magnitude, odd phase.
6. **The DFT assumes the block repeats with period $N$.** Non-integer cycles ⇒ jump at the edges ⇒
   **spectral leakage**.
7. **IDFT(DFT(x)) = x exactly** — the DFT is an invertible change of basis.
8. **DFT is $O(N^2)$; FFT is $O(N\log N)$**, same result. The speed-up grows with $N$.
9. **Filtering = multiply the spectrum by a mask** ($Y = HX$). Keep both $\pm f$ to stay real.
10. **Multiplying by $\cos(2\pi f_ct)$ shifts the spectrum to $\pm f_c$** (modulation). That's how
    many signals share one medium (FDM), provided carriers are $\ge 2B$ apart.

---

## 6. How to run

```powershell
D:\Jon\Uni\SYproject\embeddedSys\.venv\Scripts\Activate.ps1
cd D:\Jon\Uni\SYproject\embeddedSys\SC3102\Lab3
python -m pip install notebook        # the venv doesn't have Jupyter yet
python -m notebook Lab-03-DFT.ipynb
```

Or open `Lab-03-DFT.ipynb` in VS Code and pick the `.venv` kernel. The notebook is saved
with all outputs, so you can read it without running anything; to redo the experiments, change
the `# EXPERIMENT` values in the code cells (1A: `f_s`; 1B: `alias_sample_rate`; 1C: `f0`;
Q2: `amplitude`/`cycles`/`phase`; 3B: `benchmark_sizes`; 4A: `low`/`high`; 4B: `carrier_frequencies`)
and re-run. Every code cell is left at its **default** setting.
