# SC3102 Lab 1: Signals and its Representations - Complete Answers & Notes

---

## 1. Basic Representation of Signals
**File:** [Lab_1_Q1_example.py](file:///D:/Jonathan/Uni_stuff/Embedded-Systems/SC3102/Lab1/Lab_1_Q1_example.py)

### 10 Canonical Signals Implemented:
1. **Sine wave:** $y_1 = \sin(x)$
   - Implementation: `np.sin(x)`
2. **Cosine wave:** $y_2 = \cos(x)$
   - Implementation: `np.cos(x)`
3. **Unit impulse ($\delta[n]$):**
   $$\delta[n] = \begin{cases} 1, & n = 0 \\ 0, & n \neq 0 \end{cases}$$
   - Implementation: `scipy.signal.unit_impulse(101, 50)` (centered at index 50, where $x = 0$)
4. **Unit step wave ($u[n]$):**
   $$u[n] = \begin{cases} 1, & n \ge 0 \\ 0, & n < 0 \end{cases}$$
   - Implementation: `1.0 * (x >= 0)` or boolean condition `x >= 0`
5. **Square / Rectangular wave:**
   $$u[n] = \begin{cases} 1, & -k < n < k \\ 0, & \text{otherwise} \end{cases}$$
   - Implementation: `(x > -3) * (x < 3)`
6. **Triangular wave:**
   - Implementation: `scipy.signal.sawtooth(x, 0.5)` (symmetric triangle wave with 50% duty cycle)
7. **Exponential wave:** $e^{x}$
   - Implementation: `np.exp(x / 10)` (scaled by 10 to keep within reasonable plotting bounds over $[-12.5, 12.5]$)
8. **Sawtooth wave:** $x(n) = n - \lfloor n \rfloor$
   - Implementation: `scipy.signal.sawtooth(x, 0.9)`
9. **Signum function ($\text{sgn}(x)$):**
   $$\text{sgn}(x) = \begin{cases} -1, & x < 0 \\ 0, & x = 0 \\ 1, & x > 0 \end{cases}$$
   - Implementation: `np.sign(x)` or `1 * (x >= 0) - 1 * (x < 0)`
10. **Sinc wave:** $\mathrm{sinc}(x) = \frac{\sin(\pi x)}{\pi x}$ (normalized) or $\frac{\sin(x)}{x}$ (unnormalized)
    - Implementation: `np.sinc(x)`

---

## 2. Time Domain Analysis

### 2.1. Sampling Theorem (Nyquist-Shannon)
**File:** [Lab_1_Q2_sampling.py](file:///D:/Jonathan/Uni_stuff/Embedded-Systems/SC3102/Lab1/Lab_1_Q2_sampling.py)

**Signal Definition:**
$$y(t) = A \sin(2\pi \cdot 100t + \pi/6)$$

#### Questions & Answers:
1. **What is the maximum signal frequency?**
   - $F_m = 100\text{ Hz}$.

2. **What is the minimum sampling frequency required for actual reconstruction?**
   - By the **Nyquist-Shannon Sampling Theorem**, an analog continuous-time signal can be completely reconstructed if and only if the sampling frequency $f_s$ is at least twice the maximum frequency component:
     $$f_{s,\min} = 2 F_m = 2 \times 100\text{ Hz} = 200\text{ Hz}$$
   - This threshold ($200\text{ Hz}$) is called the **Nyquist rate**.

3. **What happens if we sample the signal below the minimum sampling frequency ($f_s < 200\text{ Hz}$)?**
   - **Aliasing** occurs. High frequency components fold back into the baseband $[0, f_s/2]$.
   - The sampled discrete points form a lower-frequency apparent sinusoidal curve (alias). Information is irretrievably lost and perfect reconstruction is impossible.
   - *Example tested:* At $f_s = 175\text{ Hz}$, the apparent aliased frequency is:
     $$f_{\text{alias}} = |F_m - f_s| = |100 - 175| = 75\text{ Hz}$$
   - *Example tested:* At $f_s = 400\text{ Hz}$ ($f_s > 2F_m$), samples track the original $100\text{ Hz}$ wave with full fidelity.

---

### 2.2. Addition of Two Discrete Time Signals
**File:** [Lab_1_Q2_addition.py](file:///D:/Jonathan/Uni_stuff/Embedded-Systems/SC3102/Lab1/Lab_1_Q2_addition.py)

**Signals Given:**
- $y_1(t) = A \cos(2\pi \cdot 10t)$, with $A = 0.5$, $F_1 = 10\text{ Hz}$
- $y_2(t) = B \cos(2\pi \cdot 15t)$, with $B = 0.3$, $F_2 = 15\text{ Hz}$
- $y_3(t) = y_1(t) + y_2(t)$
- Sampling frequency: $F_s = 60\text{ Hz}$, $t = \frac{n}{F_s}$

#### Questions & Answers:

**a. Find the discrete-time representation of $y_1[n]$, $y_2[n]$, and $y_3[n]$:**
Substitute $t = \frac{n}{F_s} = \frac{n}{60}$:
$$y_1[n] = 0.5 \cos\left(2\pi \cdot 10 \cdot \frac{n}{60}\right) = 0.5 \cos\left(\frac{2\pi}{6} n\right) = 0.5 \cos\left(\frac{\pi}{3} n\right)$$
$$y_2[n] = 0.3 \cos\left(2\pi \cdot 15 \cdot \frac{n}{60}\right) = 0.3 \cos\left(\frac{2\pi}{4} n\right) = 0.3 \cos\left(\frac{\pi}{2} n\right)$$
$$y_3[n] = 0.5 \cos\left(\frac{\pi}{3} n\right) + 0.3 \cos\left(\frac{\pi}{2} n\right)$$

**b. Find the period of $y_3[n]$:**
- Digital frequency of $y_1[n]$: $\omega_1 = \frac{\pi}{3} \implies \frac{\omega_1}{2\pi} = \frac{1}{6} = \frac{k_1}{N_1} \implies N_1 = 6\text{ samples/cycle}$.
- Digital frequency of $y_2[n]$: $\omega_2 = \frac{\pi}{2} \implies \frac{\omega_2}{2\pi} = \frac{1}{4} = \frac{k_2}{N_2} \implies N_2 = 4\text{ samples/cycle}$.
- Period of sum $y_3[n]$:
  $$N_3 = \text{LCM}(N_1, N_2) = \text{LCM}(6, 4) = 12\text{ samples}$$

**c. How are the periods of $y_3[n]$ related to $y_1[n]$ and $y_2[n]$?**
- The period $N_3$ of the sum of two periodic discrete-time sequences is the **Least Common Multiple (LCM)** of their individual fundamental periods $N_1$ and $N_2$:
  $$N_3 = \text{LCM}(N_1, N_2) = \frac{N_1 \times N_2}{\text{GCD}(N_1, N_2)} = \frac{6 \times 4}{2} = 12$$
- In continuous-time, two signals must have a common rational harmonic relationship ($T_1/T_2 \in \mathbb{Q}$). In discrete-time, both digital frequencies $\frac{\omega}{2\pi}$ must be rational for the signals to be individually periodic, and their sum has a period equal to the LCM of the two integer periods.

**d. Is $y_3[n]$ an energy or power signal? Find its (energy or power) and compare it against $y_1[n]$ and $y_2[n]$:**
- **Signal Classification:**
  - A discrete-time signal is an **energy signal** if $0 < E < \infty$ and $P = 0$.
  - A discrete-time signal is a **power signal** if $0 < P < \infty$ and $E = \infty$.
  - Because $y_1[n]$, $y_2[n]$, and $y_3[n]$ are periodic non-zero sinusoidal sequences extending over $-\infty < n < \infty$, their total energy summed over all time is infinite ($E = \infty$).
  - However, their average power over one period is finite and non-zero:
    $$\boxed{y_3[n] \text{ is a power signal.}}$$
- **Power Calculation:**
  For a periodic discrete-time sinusoid $x[n] = C \cos(\omega n + \theta)$, the average power is $P = \frac{C^2}{2}$.
  - Power of $y_1[n]$:
    $$P_1 = \frac{1}{N_1} \sum_{n=0}^{N_1-1} |y_1[n]|^2 = \frac{A^2}{2} = \frac{(0.5)^2}{2} = \frac{0.25}{2} = 0.125\text{ W}$$
  - Power of $y_2[n]$:
    $$P_2 = \frac{1}{N_2} \sum_{n=0}^{N_2-1} |y_2[n]|^2 = \frac{B^2}{2} = \frac{(0.3)^2}{2} = \frac{0.09}{2} = 0.045\text{ W}$$
  - Power of $y_3[n]$:
    Since $\omega_1 \neq \omega_2$ (orthogonal over their common period $N_3 = 12$), the cross-correlation term averages to 0:
    $$P_3 = \frac{1}{12} \sum_{n=0}^{11} (y_1[n] + y_2[n])^2 = P_1 + P_2 = 0.125 + 0.045 = 0.170\text{ W}$$
  - **Comparison:**
    $$P_3 = P_1 + P_2 = 0.170\text{ W}$$
    The total average power of the combined signal equals the sum of the average powers of the individual constituent signals.

---

## 3. Working on a Natural Signal (EEG)

### 3.1. Loading and Plotting EEG Signals
**File:** [Lab_1_Q3_loadEEG.py](file:///D:/Jonathan/Uni_stuff/Embedded-Systems/SC3102/Lab1/Lab_1_Q3_loadEEG.py)

- Loaded `EEG_exp.mat` using `scipy.io.loadmat('EEG_exp.mat', squeeze_me=True)`.
- Keys present in the dictionary: `['__header__', '__version__', '__globals__', 'EEG', 'fs', 'trial_info']`
- Raw data attributes:
  - `EEG.shape` = `(720000,)` (720,000 data points)
  - `fs` = `1000` Hz

---

### 3.2. Analog-to-Digital Conversion (Quantization)
**File:** [Lab_1_Q3_ADC.py](file:///D:/Jonathan/Uni_stuff/Embedded-Systems/SC3102/Lab1/Lab_1_Q3_ADC.py)

**Parameters:**
- Range: $[-32\,\mu\text{V}, +32\,\mu\text{V}]$, Full scale range: $V_{\text{range}} = 32 - (-32) = 64\,\mu\text{V}$.
- 4-bit ADC: $N = 4 \implies \text{number of quantization levels } L = 2^4 = 16$.

#### Questions & Answers:
1. **What is the voltage resolution $\Delta v$?**
   $$\Delta v = \frac{V_{\max} - V_{\min}}{2^B} = \frac{64\,\mu\text{V}}{16} = 4\,\mu\text{V}$$

2. **What are the number of possible voltage levels of the new digitized EEG signal? How is this related to $\Delta v$?**
   - For a $B$-bit uniform ADC, the number of discrete quantization levels is $L = 2^B$. For 4 bits: $L = 2^4 = 16\text{ levels}$.
   - The relationship is:
     $$L = \frac{V_{\max} - V_{\min}}{\Delta v} = \frac{64}{\Delta v}$$
   - Inversely proportional: Increasing $\Delta v$ reduces the number of distinct quantization levels $L$.

3. **What happens when $\Delta v$ is increased?**
   - Step height increases, creating coarse quantization steps.
   - **Quantization error / noise** ($e[n] = x[n] - x_q[n]$) increases (quantization noise power $\sigma_e^2 = \frac{\Delta v^2}{12}$).
   - The reconstructed waveform shows visible distortion (flat step plateaus), losing small amplitude fluctuations (e.g. brainwave micro-spikes).

4. **Find the minimum number of bits that can approximately represent the signal. Justify (open-ended question):**
   - The typical EEG voltage in the dataset spans from approximately $-15\,\mu\text{V}$ to $+20\,\mu\text{V}$.
   - With a 4-bit converter ($\Delta v = 4\,\mu\text{V}$), the step size is nearly 15–20% of the entire signal dynamic range, which creates severe quantization distortion.
   - With an **8-bit ADC** ($2^8 = 256$ levels):
     $$\Delta v_{8\text{-bit}} = \frac{64}{256} = 0.25\,\mu\text{V}$$
     A step size of $0.25\,\mu\text{V}$ is small enough to preserve physiological brain waveforms (alpha, beta, theta rhythms) while maintaining high Signal-to-Quantization-Noise Ratio ($\text{SQNR} \approx 6.02 B + 1.76 \approx 50\text{ dB}$).
   - Therefore, at least **8 to 10 bits** is the recommended minimum for practical EEG acquisition.

---

### 3.3. Down-Sampling in Time
**File:** [Lab_1_Q3_sampling.py](file:///D:/Jonathan/Uni_stuff/Embedded-Systems/SC3102/Lab1/Lab_1_Q3_sampling.py)

#### Questions & Answers:
1. **What is sampling period $dt$?**
   $$dt = \frac{1}{f_s} = \frac{1}{1000\text{ Hz}} = 0.001\text{ s} = 1\text{ ms}$$

2. **What is the total number of samples of the EEG signal?**
   $$N = 720,000\text{ samples}$$

3. **What is the total time duration ($T_{\text{exp}}$) of the given EEG signal?**
   $$T_{\text{exp}} = N \times dt = \frac{720,000}{1,000} = 720\text{ seconds} \quad (12\text{ minutes})$$

4. **Time Vector Construction:**
   - Vector in code: `t_EEG = np.arange(0, T_exp, dt)` (length 720,000).

5. **Effect of Downsampling by a factor $M = 10$:**
   - Effective sampling rate drops to $f_{s,\text{new}} = \frac{1000}{10} = 100\text{ Hz}$.
   - New Nyquist frequency drops to $f_{\text{nyq}} = 50\text{ Hz}$.
   - Slower brainwaves (< 50 Hz, like delta/theta/alpha) are retained, but higher-frequency components (> 50 Hz, such as gamma bands or sharp spike potentials) are smoothed out or aliased.

---

## 4. Polar Plot of Signals (Optional)

### 4.1. Complex Exponential Signal
**File:** [Lab_1_Q4_1_polar_plot.py](file:///D:/Jonathan/Uni_stuff/Embedded-Systems/SC3102/Lab1/Lab_1_Q4_1_polar_plot.py)

**Signal Definition:**
$$y[n] = A^n e^{j(\omega n + \phi)} = A^n \left(\cos(\omega n + \phi) + j\sin(\omega n + \phi)\right)$$

- For $A < 1$ (e.g., $A = 0.98$): The signal decays inward exponentially towards the origin as $n$ increases.
- In 2D: Displays decaying sinusoids with a phase offset between the real component (cosine) and imaginary component (sine).
- In Polar plot: Forms an inward spiral towards the center.
- In 3D: Forms a tapered helical corkscrew along the sample index axis $n$.

---

### 4.2. Discrete Fourier Twiddle Factors $W_N^k$
**File:** [Lab_1_Q4_2_3D_plot.py](file:///D:/Jonathan/Uni_stuff/Embedded-Systems/SC3102/Lab1/Lab_1_Q4_2_3D_plot.py)

**Definition:**
$$W^k = 1 \cdot e^{j\left(\frac{2\pi}{N} k n\right)}, \quad N = 16, \quad n = 0, \dots, N-1$$

#### Observations & Relationships:
1. **Angular Frequency:**
   $$\omega_k = \frac{2\pi}{N} k = \frac{2\pi}{16} k = \frac{\pi}{8} k\text{ rad/sample}$$
   The digital angular frequency increases linearly with the index $k$.
2. **Number of Complete Cycles over $N$ samples:**
   - Over the span of $N = 16$ samples, the phasor completes exactly **$k$ full cycles**:
     - For $k = 0$: Constant value $W^0 = 1$ ($0$ cycles, DC component).
     - For $k = 1$: Completes exactly $1$ full cycle around the unit circle.
     - For $k = 2$: Completes exactly $2$ full cycles.
     - For $k = 3$: Completes exactly $3$ full cycles.
3. **Discrete Fourier Basis:**
   These functions form the orthogonal basis functions for the 16-point Discrete Fourier Transform (DFT).
