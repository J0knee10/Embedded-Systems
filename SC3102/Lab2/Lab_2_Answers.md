# SC3102 Lab 2: Linear Time-Invariant Systems — Complete Answers & Notes

**Environment:** the repo-wide venv at `D:\Jon\Uni\SYproject\embeddedSys\.venv`
(Python 3.11.9 · numpy 2.4.6 · scipy 1.17.1 · matplotlib 3.11.2 · pandas 3.0.6 · opencv 5.0.0)

Install it with `python -m pip install -r requirements.lock.txt` from the repo root.
All outputs quoted below were produced on this stack.

---

## 0. The one idea this lab is built around

A **system** turns an input signal into an output signal. If that system is **linear** and
**time-invariant (LTI)**, then it is *completely* described by one thing: its response to a
single unit impulse, $h[n]$ (or $h(t)$). Once you know $h$, the output for *any* input is

$$y(t) = x(t) * h(t) = \int_{-\infty}^{+\infty} x(\tau)h(t-\tau)\,d\tau
\qquad\qquad
y[n] = x[n] * h[n] = \sum_{k} x[k]\,h[n-k]$$

Every question in this lab is one of two things: **finding $h$**, or **convolving with $h$**.

**Why this is true** — and the intuition the lab is trying to build:
1. Any input can be written as a sum of scaled, shifted impulses: $x[n]=\sum_k x[k]\,\delta[n-k]$.
2. **Time-invariance** says the response to $\delta[n-k]$ is $h[n-k]$ — the same shape, just shifted.
3. **Linearity** says the responses to each piece simply add up, scaled by $x[k]$.

Put those three together and you get convolution. That is literally the "shift, scale, add"
algorithm you write by hand in Q3 and Q4.

---

## 1. Q2 — A system in action: edge detection

**File:** [Lab_2_Q2_EdgeDetection.py](file:///D:/Jon/Uni/SYproject/embeddedSys/SC3102/Lab2/Lab_2_Q2_EdgeDetection.py)
**Needs:** `pip install opencv-python` (already installed into the venv)

Nothing to derive here — the point is to *see* a system: image in $\to$ edge map out.

```python
edges = cv2.Canny(image, 100, 200)   # 100 = lower hysteresis threshold, 200 = upper
```

**What Canny actually does, and why it belongs in a convolution lab:**
1. Gaussian blur — a **2-D convolution** with a smoothing kernel (noise suppression).
2. Sobel gradients — **2-D convolution** with $[-1,0,1]$-style difference kernels.
3. Non-maximum suppression + hysteresis thresholding (these steps are *not* linear).

So steps 1–2 are exactly the operation studied in 1-D for the rest of the lab; the thresholding
at the end is what makes the *overall* edge detector a non-linear system.

The script runs the same system on both `edgeflower.jpg` and `testimage.jpg`, which is the
"try a different test image" instruction.

**Takeaway:** a *kernel* is just an impulse response wearing a different hat. Blurring,
sharpening, edge detection and audio filtering are all the same mathematical operation.

---

## 2. Q3 — Building convolution out of the dot product

**File:** [Lab_2_Q3_convolution.py](file:///D:/Jon/Uni/SYproject/embeddedSys/SC3102/Lab2/Lab_2_Q3_convolution.py)

### 3.2 Input signal — a spike train
```python
n_samples = 100
signal = np.zeros(n_samples)
signal[np.random.randint(0, n_samples, 5)] = 1
```
100 samples, 5 unit impulses at random positions. This is a train of $\delta$'s: exactly the
decomposition $x[n]=\sum_k x[k]\delta[n-k]$ made visible.

> `np.random.seed(0)` is set in the script so your plots are reproducible. Delete that line
> for a fresh random signal each run.

### 3.3 Kernel — a boxcar
```python
kernel = np.zeros(10)   # 10 samples long
kernel[2:8] = 1         # boxcar of width 6
```
A boxcar is a **moving-sum / averaging filter** — the simplest lowpass there is.

### 3.4 Dot product
$$\text{dotproduct}_{ab}=\sum_{i=1}^{n} a_i b_i$$
```python
np.dot(a, b)      # == np.sum(a * b)
```
Weighted sum of one vector by another; both must be the same length. In signal processing it
is a **similarity measure** — it is large when the two vectors have big values in the same
places. Convolution is nothing more than this dot product evaluated at every possible shift.

### 3.5 Convolution = dot product with a matrix of shifted kernels
```python
def convolve_by_matrix(x, h):
    N, M = len(x), len(h)
    shifted_kernel = np.zeros((N, N + M - 1))
    for i in range(N):
        shifted_kernel[i, i:i + M] = h
    return np.dot(x, shifted_kernel)
```
Row $i$ holds a copy of the kernel starting at position $i$; the dot product with the signal
scales each row by $x[i]$ and sums them. Result:

```
max |ours - np.convolve| = 0.0
```

**Output length is $N+M-1 = 100+10-1 = 109$**, not 100 — the last kernel copy hangs off the end.

### ⚠ The one real gotcha in this question

The lab sheet tells you to fill each row with `kernel[::-1]` (the reversed kernel). Work it
through: putting the reversed kernel in row $i$ gives

$$y[n]=\sum_i x[i]\,h[M-1-(n-i)]$$

which is convolution with the **flipped** kernel, not with $h$ itself. It agrees with
`np.convolve` here **only because this boxcar is symmetric** ($h=[0,0,1,1,1,1,1,1,0,0]$ reads
the same backwards). The script proves the point:

| kernel | rows filled with reversed $h$ | rows filled with $h$ |
|---|---|---|
| symmetric boxcar | error `0.0` | error `0.0` |
| asymmetric `[1,2,3,0,0]` | error **`2.0`** | error `0.0` |

The "flip and slide" reversal in the convolution *formula* is already accounted for by the
staircase structure of the matrix — you must not flip a second time. The correct row content
is the kernel as-is.

### Redo with more spikes
The script repeats with 30 spikes. With 5 spikes the boxcars sit apart and you just see 5
rectangles; with 30 they **overlap and add**, producing a stepped waveform. That superposition
is linearity in action, and it is exactly what the fMRI question exploits next.

---

## 3. Q4 — fMRI: predicting the BOLD signal

**Files:** [Lab_2_Q4_hrf.py](file:///D:/Jon/Uni/SYproject/embeddedSys/SC3102/Lab2/Lab_2_Q4_hrf.py) (4.1–4.3) ·
[Lab_2_Q4_algorithm.py](file:///D:/Jon/Uni/SYproject/embeddedSys/SC3102/Lab2/Lab_2_Q4_algorithm.py) (4.4–4.5)

**The physical story:** an event (a flashing checkerboard) causes neurons to fire; the firing
causes a slow local blood-flow change; the MRI scanner measures that blood flow (the BOLD
signal). The mapping *neural firing $\to$ blood flow* is modelled as an LTI system.

| Signal processing | fMRI |
|---|---|
| input $x[n]$ | neural firing model |
| impulse response $h[n]$ | **HRF** — haemodynamic response function |
| output $y[n]$ | predicted BOLD signal |

### 4.1 Neural input signal
40 s at $\Delta t = 0.1$ s $\Rightarrow$ 400 samples. Impulses of amplitude 2 at $t=4$,
1 at $t=10$, 3 at $t=20$.

```python
def index_of(t):
    return int(np.argmin(np.abs(times - t)))
```

> **Why not the sheet's `int(np.where(times == 4)[0])`?** Two reasons. `np.arange` with a
> 0.1 step produces binary floats, so an exact `==` comparison is fragile; and `int()` on an
> array is deprecated (it raises a `DeprecationWarning` on numpy ≥ 1.25 and will become an
> error). `np.argmin(np.abs(times - t))` is robust on every numpy version.

### 4.2 The HRF — the impulse response
$$h(t)=t^{8.6}\,e^{-t/0.547}$$
```python
hrf_times  = np.arange(0, 20, 0.1)
hrf_signal = hrf(hrf_times)          # 200 samples
```
Shape: ~0 at first, peaks around 4–5 s, decays back by ~20 s. It is slow and smooth — blood
flow cannot follow neuronal firing instantly. In practice you would estimate it by averaging
the measured BOLD response over many brief events.

### 4.3 Building the output by hand
```python
bold_signal = np.zeros(n_time_points)
bold_signal[i_time_4 :i_time_4  + n_hrf_points]  = hrf_signal * 2
bold_signal[i_time_10:i_time_10 + n_hrf_points] += hrf_signal * 1
bold_signal[i_time_20:i_time_20 + n_hrf_points] += hrf_signal * 3
```
**Shift** by the impulse position (time-invariance), **scale** by the amplitude (homogeneity),
**add** (additivity). The `+=` on lines 2 and 3 *is* superposition — that is why the responses
to $t=4$ and $t=10$ visibly merge into one broad hump.

This only fits inside 400 samples because $20\text{ s}+20\text{ s}=40\text{ s}$ exactly. Move
an impulse later and the tail would be silently chopped off — which is the problem 4.4 fixes.

### 4.4 The general algorithm
1. start with a zero output vector
2. for each index $i$ of the input, take a copy of the HRF starting at $i$
3. scale it by `input[i]`
4. add it into the output

**Length:** if the input is $N$ points and the HRF is $M$ points, the copy starting at
$i=N-1$ runs to $N-1+M-1$. The output must therefore be $\mathbf{N+M-1}$ points long —
$M-1$ more than the input.

```python
def shift_scale_add(input_signal, kernel):
    N, M = len(input_signal), len(kernel)
    output = np.zeros(N + M - 1)
    for i in range(N):
        output[i:i + M] += kernel * input_signal[i]
    return output
```
The time axis must be extended to match:
```python
extra_times    = np.arange(n_hrf_points - 1) * 0.1 + 40
times_and_tail = np.concatenate((times, extra_times))
```

### 4.5 …that algorithm *is* convolution
```python
bold_signal = np.convolve(neural_signal, hrf_signal)
```
Verified by the script:
```
lengths: ours 599, np.convolve 599, N + M - 1 = 599        # 400 + 200 - 1
max |ours - np.convolve| = 5.68e-14                        # floating-point noise only
```
$5.68\times10^{-14}$ on signals of order $10^{7}$ is exact agreement to machine precision.

### Redo with a different neural input
The script adds a 7-impulse version (amplitudes 1.5–3 spread from $t=2$ to $t=36$). Two things
to look for: the individual responses **overlap and sum**, and the response to the $t=36$
impulse **runs past 40 s into the tail** — the $M-1$ extra samples you would have lost without
extending the output vector.

---

## 4. Q5 — LTI systems, cascading, and proving linearity

**Files:** [lti_utils.py](file:///D:/Jon/Uni/SYproject/embeddedSys/SC3102/Lab2/lti_utils.py) (our own convolution module) ·
[Lab2_Q5_1.py](file:///D:/Jon/Uni/SYproject/embeddedSys/SC3102/Lab2/Lab2_Q5_1.py) ·
[Lab2_Q5_2.py](file:///D:/Jon/Uni/SYproject/embeddedSys/SC3102/Lab2/Lab2_Q5_2.py) ·
[Lab2_Q5_3.py](file:///D:/Jon/Uni/SYproject/embeddedSys/SC3102/Lab2/Lab2_Q5_3.py)

$$h_1[n]=[0.06523,\,0.14936,\,0.21529,\,0.2402,\,0.21529,\,0.14936,\,0.06523]$$
$$h_2[n]=[-0.06523,\,-0.14936,\,-0.21529,\,0.7598,\,-0.21529,\,-0.14936,\,-0.06523]$$

Both are **FIR** (finite impulse response) filters, 7 taps, and both are symmetric about the
centre tap $\Rightarrow$ **linear phase**.

### 5.1 Impulse responses, and the cascade $h_3 = h_1 * h_2$

Feeding $x[n]=\delta[n]$ into an LTI system reads its impulse response straight out:
$\delta[n]*h[n]=h[n]$. That is why "plot the impulse response" and "convolve with $\delta$"
are the same instruction.

Script output:
```
sum h1 =  1.1000   -> gain at DC, passes slow signals (lowpass)
sum h2 = -0.1000   -> almost zero at DC, blocks slow signals (highpass)
h1 + h2 = [0. 0. 0. 1. 0. 0. 0.]   -> h2[n] = delta[n-3] - h1[n]
len h1 = 7, len h2 = 7, len h3 = 13   (= 7 + 7 - 1)
```

Three things fall out of this:

- $\sum_n h[n]$ is the **DC gain** $H(e^{j0})$. $h_1$ has gain $\approx 1.1$ (passes DC $\Rightarrow$ **lowpass**);
  $h_2$ has gain $\approx -0.1 \approx 0$ (kills DC $\Rightarrow$ **highpass**).
- $h_1+h_2=\delta[n-3]$ exactly. So $h_2$ is built by **spectral inversion**:
  $h_2[n]=\delta[n-3]-h_1[n]$, i.e. "all-pass minus lowpass = highpass". The delay of 3 is the
  group delay of the 7-tap filter, $(7-1)/2$.
- **Cascading two LTI systems in series convolves their impulse responses.** Passing a signal
  through $h_1$ then $h_2$ is identical to passing it once through $h_3=h_1*h_2$.
  Lowpass $*$ highpass $\Rightarrow$ **bandpass** — the script's `freqz` plot shows this directly.

**`np.convolve` vs `scipy.signal.lfilter`:** both implement the same FIR filtering, but
`np.convolve(x, h)` returns the **full** $N+M-1$ result, while `lfilter(h, [1], x)` returns
only the first $N$ samples (the tail is truncated). They overlay perfectly on the region they
share. The `[1]` is the denominator $a$ — setting $a=[1]$ makes it a pure FIR filter.

### 5.2 Response to $x[n]=\delta[n]-2\delta[n-15]$

The lab asks for **your own** convolution module, so `lti_utils.my_convolve` implements the
double loop directly from the definition:

```python
def my_convolve(x, h):
    N, M = len(x), len(h)
    y = np.zeros(N + M - 1)
    for n in range(N):
        for m in range(M):
            y[n + m] += x[n] * h[m]
    return y
```

Verification against NumPy:
```
H1: max |my_convolve - np.convolve| = 0.00e+00   length 36    # 30 + 7 - 1
H2: max |my_convolve - np.convolve| = 0.00e+00   length 36
H3: max |my_convolve - np.convolve| = 0.00e+00   length 42    # 30 + 13 - 1
```
Bit-for-bit identical.

**Reading the plot:** the output is one copy of $h$ at $n=0$, plus an inverted, doubled copy
at $n=15$. Nothing else. That is time-invariance made visual — the system's response shape
never changes, it only shifts and scales. The script also checks this numerically:
```
time invariance, max |y - (h3@0 - 2*h3@15)| = 0.00e+00
```

### 5.3 Is $y[n]=h_3[n]*x[n]$ linear?

With $x_1[n]=\delta[n]$, $x_2[n]=-2\delta[n-15]$, so $x=x_1+x_2$, we must show

$$h_3 * (x_1+x_2) \;=\; (h_3 * x_1)+(h_3 * x_2) \;=\; y_1[n]+y_2[n]$$

The script computes both routes and overlays them, plus a difference trace:
```
max |y1+y2 - h3*(x1+x2)| = 0.00e+00     -> additive
max |h3*(a*x1) - a*(h3*x1)| = 0.00e+00  -> homogeneous     (a = 3.7)
=> additive + homogeneous => the system is LINEAR
```

The difference plot is a flat line at zero. **Why it must be so:** convolution is distributive
over addition and commutes with scalar multiplication —

$$\sum_k (x_1[k]+x_2[k])h[n-k]=\sum_k x_1[k]h[n-k]+\sum_k x_2[k]h[n-k]$$

so *any* system defined by a convolution is automatically linear. Note that full linearity
needs **both** properties: additivity **and** homogeneity (scaling), which is why the script
tests both. Together they give superposition:
$h*(a x_1 + b x_2) = a(h*x_1) + b(h*x_2)$.

---

## 5. Q6 — Filtering a real ECG signal (optional)

**File:** [Lab2_Q6_ecg.py](file:///D:/Jon/Uni/SYproject/embeddedSys/SC3102/Lab2/Lab2_Q6_ecg.py)

### 6.1 Load and inspect
```python
dataset = pd.read_csv("ECG.csv")
y  = np.array([e for e in dataset.hart])
N  = len(y)            # 3600 samples
Fs = 1000              # Hz  ->  3.60 s of recording
x  = np.linspace(0.0, N/Fs, N)
```
The raw trace shows the QRS complexes buried under a fast, fuzzy ripple.

### 6.2 Butterworth lowpass
```python
b, a   = signal.butter(4, 50/(Fs/2), 'low')   # 4th order, cutoff normalised to Nyquist
y_filt = signal.filtfilt(b, a, y)
```
- **`50/(Fs/2)`** — SciPy expects $W_n$ normalised so that 1.0 = the Nyquist frequency $F_s/2 = 500$ Hz. So $W_n = 0.1$.
- **Butterworth** is chosen for its maximally flat passband (no ripple distorting the ECG morphology).
- **`filtfilt`, not `lfilter`** — it runs the filter forwards then backwards, which cancels the
  phase delay. **Zero phase shift matters clinically**: a phase-distorted ECG would shift the
  QRS peaks and corrupt interval measurements.

### 6.3 FFT before and after
```python
yf  = scipy.fftpack.fft(y)
yff = scipy.fftpack.fft(y_filt)
xf  = np.linspace(0, Fs/2, N//2)                 # one-sided frequency axis
mag = 2.0/N * np.abs(yf[:N//2])                  # 2/N scales to true amplitude
```
Only the first $N/2$ bins are plotted: the FFT of a real signal is conjugate-symmetric, so the
upper half is a mirror image carrying no new information. The $2/N$ factor converts FFT bin
magnitudes to physical amplitudes (the 2 recovers the energy discarded with the mirrored half).

Script output:
```
strongest components in the raw signal (Hz): [0.0, 3.3, 16.7, 13.3, 0.3, 16.4]
energy above 50 Hz: raw 0.0133 -> filtered 0.0003    (97.6% removed)
magnitude at exactly 50 Hz: raw 0.0023 -> filtered 0.0011   (only 52% removed)
```

**Two results worth understanding:**

1. **The cutoff is the $-3$ dB point, not a wall.** At exactly 50 Hz the 4th-order response is
   $1/\sqrt{2}$ in amplitude, and `filtfilt` applies it twice $\Rightarrow$ $\approx 0.5$.
   Hence only ~52 % removed *at* 50 Hz, while content well above 50 Hz is crushed by 97.6 %.
   If you genuinely wanted to kill a 50 Hz tone you would put the cutoff below it, or use a notch.
2. **In this recording the interference is broadband HF hash, not a single 50 Hz line** — the
   real ECG energy sits at 0–35 Hz, so a lowpass is the right system here. For true mains hum
   a narrow notch preserves the sharp QRS edges better:
   `b_n, a_n = signal.iirnotch(50, Q=30, fs=Fs)`

**The LTI connection:** a digital filter *is* an LTI system. Here it is specified by its
coefficients $(b,a)$ rather than by $h[n]$ directly, but filtering is still convolution —
`lfilter(b, [1], x)` and `np.convolve(x, b)` are the same operation (Q5.1 proves it).

---

## 6. Key takeaways

1. **LTI $\Rightarrow$ fully characterised by $h[n]$.** One impulse test tells you the response
   to every possible input.
2. **Convolution is shift, scale, add.** Not a formula to memorise — an algorithm you wrote
   twice in this lab (Q3.5, Q4.4) before being told its name.
3. **Output length is $N+M-1$.** Forgetting the $M-1$ tail silently truncates your answer.
4. **$\delta[n]$ is the probe.** $x*\delta = x$; $\delta * h = h$.
5. **Series cascade $\Rightarrow$ convolve the impulse responses.** $h_3 = h_1 * h_2$.
   Lowpass $*$ highpass $=$ bandpass.
6. **$\sum_n h[n]$ = DC gain.** Sums to 1 $\to$ lowpass; sums to 0 $\to$ highpass. Fast sanity check.
7. **Linear = additive AND homogeneous.** Any system written as a convolution is linear for free.
8. **Kernel = impulse response = filter.** Image blurring, edge detection, ECG denoising and
   the fMRI haemodynamic model are all the same operation in different clothes.
9. **Watch the double flip.** The reversal in the convolution formula is already built into the
   shifted-kernel matrix; reversing again is a bug that a symmetric kernel will hide from you.
10. **Cutoff $\ne$ brick wall.** A filter's cutoff frequency is where it is 3 dB down, not where
    the signal disappears.

---

## 7. How to run

```powershell
D:\Jon\Uni\SYproject\embeddedSys\.venv\Scripts\Activate.ps1
cd D:\Jon\Uni\SYproject\embeddedSys\SC3102\Lab2

python Lab_2_Q2_EdgeDetection.py    # Q2  edge detection (needs opencv)
python Lab_2_Q3_convolution.py      # Q3  convolution from the dot product
python Lab_2_Q4_hrf.py              # Q4.1 - 4.3  HRF and the BOLD signal
python Lab_2_Q4_algorithm.py        # Q4.4 - 4.5  our algorithm == np.convolve
python Lab2_Q5_1.py                 # Q5.1 impulse responses, h3 = h1 * h2
python Lab2_Q5_2.py                 # Q5.2 own convolution module
python Lab2_Q5_3.py                 # Q5.3 linearity proof
python Lab2_Q6_ecg.py               # Q6   ECG filtering (optional)
```
