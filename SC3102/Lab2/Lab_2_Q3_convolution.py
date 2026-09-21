# Q3: Building convolution from the dot product
#   3.2 input signal (spike train)      3.3 boxcar kernel
#   3.4 dot product                     3.5 convolution as a matrix of shifted kernels

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)           # remove this line if you want a new random signal each run

# ---------------------------------------------------------------- 3.2 input signal
n_samples = 100
n_spikes = 5

signal = np.zeros(n_samples)                                  # zero vector
signal[np.random.randint(0, n_samples, n_spikes)] = 1         # 5 unit impulses at random places

plt.figure(figsize=(12, 3))
plt.plot(signal, linewidth=2)
plt.xlabel('Time'); plt.ylabel('Signal Intensity')
plt.title('Signal (%d impulses)' % n_spikes)

# ---------------------------------------------------------------- 3.3 boxcar kernel
kernel = np.zeros(10)       # 10 samples long
kernel[2:8] = 1             # boxcar of width 6

plt.figure(figsize=(12, 3))
plt.plot(kernel, linewidth=2, color='red')
plt.xlabel('Time'); plt.ylabel('Intensity')
plt.title('Kernel (boxcar, width 6)')

# ---------------------------------------------------------------- 3.4 dot product
a = np.random.randint(1, 10, 20)
b = np.random.randint(1, 10, 20)
print('a =', a)
print('b =', b)
print('Dot Product: %s' % np.dot(a, b))          # sum of element-wise products
print('Check by hand: %s' % np.sum(a * b))


# ------------------------------------------------- 3.5 convolution = dot with shifted kernels
def convolve_by_matrix(x, h):
    """Convolve x with h by building a matrix whose row i is h shifted to start at i.

    y[n] = sum_i x[i] * h[n - i]  ->  y = x . H, where H[i, i:i+M] = h
    Output length is N + M - 1 (the tail of the last shifted kernel).
    """
    N, M = len(x), len(h)
    shifted_kernel = np.zeros((N, N + M - 1))
    for i in range(N):
        shifted_kernel[i, i:i + M] = h
    return np.dot(x, shifted_kernel)


convolved_signal = convolve_by_matrix(signal, kernel)

plt.figure(figsize=(12, 3))
plt.plot(convolved_signal, linewidth=2)
plt.ylabel('Intensity'); plt.xlabel('Time')
plt.title('Signal convolved with boxcar kernel')

# Sanity check against NumPy
print('\nmax |ours - np.convolve| =', np.max(np.abs(convolved_signal - np.convolve(signal, kernel))))

# ---- Why the lab sheet's rev_kernel still works -------------------------------------------
# The sheet fills each row with kernel[::-1]. That actually convolves with the FLIPPED kernel,
# so it only agrees with np.convolve because this boxcar happens to be symmetric.
rev = np.zeros((n_samples, n_samples + len(kernel) - 1))
for i in range(n_samples):
    rev[i, i:i + len(kernel)] = kernel[::-1]
print('symmetric kernel, reversed vs not:',
      np.max(np.abs(np.dot(signal, rev) - convolved_signal)))

asym = np.array([1.0, 2.0, 3.0, 0.0, 0.0])          # an asymmetric kernel exposes the difference
print('asymmetric kernel, reversed  error:',
      np.max(np.abs(convolve_by_matrix(signal, asym[::-1]) - np.convolve(signal, asym))))
print('asymmetric kernel, un-reversed error:',
      np.max(np.abs(convolve_by_matrix(signal, asym) - np.convolve(signal, asym))))

# ---------------------------------------------------------------- redo with more spikes
n_spikes_many = 30
signal_many = np.zeros(n_samples)
signal_many[np.random.randint(0, n_samples, n_spikes_many)] = 1
convolved_many = convolve_by_matrix(signal_many, kernel)

fig, ax = plt.subplots(2, 1, figsize=(12, 5), sharex=True)
ax[0].plot(signal_many, linewidth=2)
ax[0].set_title('Signal with %d impulses' % n_spikes_many); ax[0].set_ylabel('Intensity')
ax[1].plot(convolved_many, linewidth=2)
ax[1].set_title('Convolved with boxcar kernel - the boxcars now overlap and add up')
ax[1].set_xlabel('Time'); ax[1].set_ylabel('Intensity')
plt.tight_layout()

plt.show()
