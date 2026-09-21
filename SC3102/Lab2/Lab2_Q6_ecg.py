# Q6: filtering a real ECG signal (optional section)
#   6.1 load and plot the raw ECG, spot the noise
#   6.2 remove the 50 Hz mains ("brum") noise with a Butterworth filter
#   6.3 compare the spectra before and after with an FFT
#
# A digital filter is just an LTI system: y[n] = x[n] * h[n]. Here the system is
# specified by its coefficients (b, a) instead of by h[n] directly.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import scipy.signal as signal

# ------------------------------------------------------------------ 6.1 load the signal
dataset = pd.read_csv("ECG.csv")
y = np.array([e for e in dataset.hart])

N = len(y)          # number of sample points
Fs = 1000           # sampling frequency, Hz
T = 1.0 / Fs        # sample spacing
x = np.linspace(0.0, N * T, N)              # time axis, seconds

yf = scipy.fftpack.fft(y)                                   # spectrum of the raw signal
xf = np.linspace(0, int(1 / (2 * T)), int(N / 2))           # frequency axis, 0 .. Fs/2

# ------------------------------------------------------------------ 6.2 Butterworth lowpass
# 4th order, cutoff 50 Hz. Wn is normalised to the Nyquist frequency Fs/2.
b, a = signal.butter(4, 50 / (Fs / 2), 'low')
y_filt = signal.filtfilt(b, a, y)           # filtfilt = forward + backward -> zero phase shift
yff = scipy.fftpack.fft(y_filt)

# ------------------------------------------------------------------ plots
mag_raw = 2.0 / N * np.abs(yf[:N // 2])
mag_filt = 2.0 / N * np.abs(yff[:N // 2])

fig_td = plt.figure(figsize=(11, 6))
fig_td.canvas.manager.set_window_title('Time domain signals')
ax1 = fig_td.add_subplot(211); ax1.set_title('Before filtering')
ax2 = fig_td.add_subplot(212); ax2.set_title('After filtering')
ax1.plot(x, y, color='r', linewidth=0.7)
ax2.plot(x, y_filt, color='g', linewidth=0.7)
for ax in (ax1, ax2):
    ax.set_xlabel('time (s)'); ax.set_ylabel('amplitude')
fig_td.tight_layout()

fig_fd = plt.figure(figsize=(11, 6))
fig_fd.canvas.manager.set_window_title('Frequency domain signals')
ax3 = fig_fd.add_subplot(211); ax3.set_title('Before filtering')
ax4 = fig_fd.add_subplot(212); ax4.set_title('After filtering')
ax3.plot(xf, mag_raw, color='r', linewidth=0.7, label='raw')
ax4.plot(xf, mag_filt, color='g', linewidth=0.7, label='filtered')
for ax in (ax3, ax4):
    ax.set_ylim([0, 0.2]); ax.axvline(50, color='b', ls=':', lw=1)
    ax.set_xlabel('frequency (Hz)'); ax.set_ylabel('|X(f)|'); ax.legend()
fig_fd.tight_layout()

# Zoom on ~1.5 s so the noise riding on the QRS complexes is visible
fig_zoom, axz = plt.subplots(figsize=(11, 4))
mask = x < 1.5
axz.plot(x[mask], y[mask], color='r', linewidth=0.8, label='raw')
axz.plot(x[mask], y_filt[mask], color='g', linewidth=1.2, label='filtered')
axz.set_xlabel('time (s)'); axz.set_ylabel('amplitude')
axz.set_title('Zoom: the 50 Hz ripple is gone, the QRS complexes survive')
axz.legend()
fig_zoom.tight_layout()

# ------------------------------------------------------------------ numbers to quote
i50 = int(np.argmin(np.abs(xf - 50)))
stop = xf > 50
print('N = %d samples, Fs = %d Hz, duration = %.2f s' % (N, Fs, N * T))
print('strongest components in the raw signal (Hz): %s'
      % np.round(xf[np.argsort(mag_raw)[-6:][::-1]], 1))
print('energy above 50 Hz: raw %.4f -> filtered %.4f  (%.1f%% removed)'
      % (np.sum(mag_raw[stop] ** 2), np.sum(mag_filt[stop] ** 2),
         100 * (1 - np.sum(mag_filt[stop] ** 2) / np.sum(mag_raw[stop] ** 2))))
print('magnitude at exactly 50 Hz: raw %.4f -> filtered %.4f  (only %.0f%% removed)'
      % (mag_raw[i50], mag_filt[i50], 100 * (1 - mag_filt[i50] / mag_raw[i50])))

# Two things worth noticing in those numbers:
#
# 1. 50 Hz is the CUTOFF, i.e. the -3 dB point, so the filter only halves the component
#    sitting exactly at 50 Hz. It is the content well ABOVE 50 Hz that gets crushed.
#    To really suppress a 50 Hz tone you need the cutoff below it, or a notch.
#
# 2. In this particular recording the interference is broadband high-frequency hash
#    rather than one clean 50 Hz line, which is why a lowpass is the right system here.
#    For genuine mains hum a narrow notch keeps the sharp QRS edges intact:
#       b_n, a_n = signal.iirnotch(50, Q=30, fs=Fs)

plt.show()
