# Q4.1 - 4.3: fMRI hemodynamic model
#   4.1 neural input signal (three impulses)
#   4.2 the HRF - the impulse response h(t) of the hemodynamic "system"
#   4.3 build the BOLD output by shifting and scaling the HRF by hand

import numpy as np
import matplotlib.pyplot as plt

dt = 0.1                                   # 0.1 s sampling interval
times = np.arange(0, 40, dt)               # 40 s of experiment
n_time_points = len(times)


def index_of(t):
    """Index of time t in `times` (arange gives floats, so never test with ==)."""
    return int(np.argmin(np.abs(times - t)))


# ---------------------------------------------------------------- 4.1 neural input signal
i_time_4 = index_of(4)
i_time_10 = index_of(10)
i_time_20 = index_of(20)

neural_signal = np.zeros(n_time_points)
neural_signal[i_time_4] = 2       # impulse of amplitude 2 at t = 4 s
neural_signal[i_time_10] = 1      # impulse of amplitude 1 at t = 10 s
neural_signal[i_time_20] = 3      # impulse of amplitude 3 at t = 20 s

plt.figure()
plt.plot(times, neural_signal)
plt.xlabel('time (seconds)'); plt.ylabel('neural signal')
plt.ylim(0, 3.2)
plt.title('Neural model for three impulses')


# ---------------------------------------------------------------- 4.2 hemodynamic response
def hrf(t):
    "A hemodynamic response function"
    return t ** 8.6 * np.exp(-t / 0.547)


hrf_times = np.arange(0, 20, dt)           # the HRF lasts ~20 s
hrf_signal = hrf(hrf_times)
n_hrf_points = len(hrf_signal)

plt.figure()
plt.plot(hrf_times, hrf_signal)
plt.xlabel('time (seconds)'); plt.ylabel('BOLD signal')
plt.title('Estimated BOLD signal for event at time 0')


# ------------------------------------------------- 4.3 BOLD output: shift, scale, add
bold_signal = np.zeros(n_time_points)
bold_signal[i_time_4:i_time_4 + n_hrf_points] = hrf_signal * 2
bold_signal[i_time_10:i_time_10 + n_hrf_points] += hrf_signal * 1
bold_signal[i_time_20:i_time_20 + n_hrf_points] += hrf_signal * 3

plt.figure()
plt.plot(times, bold_signal)
plt.xlabel('time (seconds)'); plt.ylabel('bold signal')
plt.title('Output BOLD signal for three impulses')

# NOTE: this only fits because the last impulse (t = 20 s) plus the 20 s HRF ends exactly at 40 s.
# Move an impulse later and the response would be chopped off - that is the length problem
# solved in Lab_2_Q4_algorithm.py by extending the output to N + M - 1 points.

plt.show()
