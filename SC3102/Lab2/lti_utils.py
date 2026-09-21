"""Small helper module for Lab 2 Q5 - our own convolution, written from scratch."""

import numpy as np


def my_convolve(x, h):
    """Discrete convolution  y[n] = sum_k x[k] h[n-k],  no NumPy shortcuts.

    Same shift-scale-add algorithm as Q4.4: each input sample drops a scaled
    copy of the impulse response into the output, starting at that sample.
    Output length is len(x) + len(h) - 1.
    """
    x = np.asarray(x, dtype=float)
    h = np.asarray(h, dtype=float)
    N, M = len(x), len(h)

    y = np.zeros(N + M - 1)
    for n in range(N):
        for m in range(M):
            y[n + m] += x[n] * h[m]
    return y


def delta(length, k=0, amplitude=1.0):
    """amplitude * delta[n - k], as a vector of the given length."""
    d = np.zeros(length)
    d[k] = amplitude
    return d
