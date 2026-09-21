# Q4.4 - 4.5: the general shift-scale-add algorithm IS convolution
#   4.4 write the algorithm ourselves, extending the output to N + M - 1 points
#   4.5 show np.convolve gives exactly the same answer

import numpy as np
import matplotlib.pyplot as plt

dt = 0.1
times = np.arange(0, 40, dt)
n_time_points = len(times)


def index_of(t):
    return int(np.argmin(np.abs(times - t)))


def hrf(t):
    "A hemodynamic response function"
    return t ** 8.6 * np.exp(-t / 0.547)


hrf_times = np.arange(0, 20, dt)
hrf_signal = hrf(hrf_times)
n_hrf_points = len(hrf_signal)

# same neural input as 4.1 so we can validate against 4.3
neural_signal = np.zeros(n_time_points)
neural_signal[index_of(4)] = 2
neural_signal[index_of(10)] = 1
neural_signal[index_of(20)] = 3


# ---------------------------------------------------------------- 4.4 our own algorithm
def shift_scale_add(input_signal, kernel):
    """1. start with a zero output vector of length N + M - 1
       2. for every index i of the input, take a copy of the kernel starting at i
       3. scale it by input[i]
       4. add it into the output"""
    N, M = len(input_signal), len(kernel)
    output = np.zeros(N + M - 1)                  # extended by M - 1 points for the tail
    for i in range(N):
        input_value = input_signal[i]
        output[i:i + M] += kernel * input_value
    return output


bold_signal = shift_scale_add(neural_signal, hrf_signal)

# 'times' must be extended too, because bold_signal is now N + M - 1 long
extra_times = np.arange(n_hrf_points - 1) * dt + 40
times_and_tail = np.concatenate((times, extra_times))

plt.figure()
plt.plot(times_and_tail, bold_signal)
plt.xlabel('time (seconds)'); plt.ylabel('bold signal')
plt.title('Output BOLD signal using our algorithm')

# ---------------------------------------------------------------- 4.5 it is convolution
bold_np = np.convolve(neural_signal, hrf_signal)

plt.figure()
plt.plot(times_and_tail, bold_np)
plt.xlabel('time (seconds)'); plt.ylabel('bold signal')
plt.title('Our algorithm is the same as convolution')

print('lengths: ours %d, np.convolve %d, N + M - 1 = %d'
      % (len(bold_signal), len(bold_np), n_time_points + n_hrf_points - 1))
print('max |ours - np.convolve| =', np.max(np.abs(bold_signal - bold_np)))

# ---------------------------------------------------------------- redo with more spikes
np.random.seed(1)
neural_many = np.zeros(n_time_points)
for t, amp in [(2, 1.5), (7, 3), (12, 2), (18, 1), (25, 2.5), (31, 2), (36, 3)]:
    neural_many[index_of(t)] = amp

bold_many = shift_scale_add(neural_many, hrf_signal)

fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
ax[0].stem(times, neural_many, basefmt=' ')
ax[0].set_ylabel('neural signal'); ax[0].set_title('Neural model, 7 impulses')
ax[1].plot(times_and_tail, bold_many)
ax[1].set_xlabel('time (seconds)'); ax[1].set_ylabel('bold signal')
ax[1].set_title('BOLD output - responses overlap and superpose (linearity)')
plt.tight_layout()

# Note the responses near t = 36 s spill past the 40 s experiment: that tail is exactly
# the M - 1 extra samples, and it would have been lost without extending the output vector.

plt.show()
