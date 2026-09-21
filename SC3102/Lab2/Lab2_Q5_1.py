# Q5.1: impulse responses of h1, h2 and the cascade h3 = h1 * h2
#
# Feeding delta[n] into an LTI system reads its impulse response straight out:
# x[n] = delta[n]  =>  y[n] = h[n].
# h1 is a lowpass FIR (all-positive, coefficients sum to ~1 -> smoothing).
# h2 is its highpass complement (h1 subtracted from a delta).
# Cascading them in series multiplies transfer functions, i.e. convolves impulse
# responses: h3[n] = h1[n] * h2[n], giving a bandpass-like response.

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from lti_utils import my_convolve, delta

impulseH1 = [0.06523, 0.14936, 0.21529, 0.2402, 0.21529, 0.14936, 0.06523]
impulseH2 = [-0.06523, -0.14936, -0.21529, 0.7598, -0.21529, -0.14936, -0.06523]
impulseH3 = np.convolve(impulseH1, impulseH2)

print('sum h1 = %.4f   -> gain at DC, passes slow signals (lowpass)' % np.sum(impulseH1))
print('sum h2 = %.4f  -> almost zero at DC, blocks slow signals (highpass)' % np.sum(impulseH2))
print('h1 + h2 = %s   -> h2[n] = delta[n-3] - h1[n], a spectrally inverted h1'
      % np.round(np.array(impulseH1) + np.array(impulseH2), 4))
print('len h1 = %d, len h2 = %d, len h3 = %d (= 7 + 7 - 1)'
      % (len(impulseH1), len(impulseH2), len(impulseH3)))

x1 = delta(30)          # unit impulse at n = 0

for h, name in [(impulseH1, 'H1'), (impulseH2, 'H2'), (impulseH3, 'H3 = H1 * H2')]:
    y_conv = np.convolve(x1, h)             # full convolution, len(x) + len(h) - 1
    y_lfilter = signal.lfilter(h, [1], x1)  # FIR filtering, truncated to len(x)
    y_mine = my_convolve(x1, h)             # our own implementation

    plt.figure()
    plt.stem(y_conv, linefmt='r--')
    plt.plot(y_lfilter, 'g-+')
    plt.plot(y_mine, 'b.', markersize=4)
    plt.title('impulse response of ' + name)
    plt.xlabel('sample n'); plt.ylabel(name.split(' ')[0] + '[n]')
    plt.legend(['scipy lfilter', 'my_convolve', 'np.convolve'])

    print('%-12s max |my_convolve - np.convolve| = %.2e' % (name, np.max(np.abs(y_mine - y_conv))))

# Frequency response - confirms lowpass / highpass / bandpass by eye
plt.figure()
for h, name in [(impulseH1, 'H1 (lowpass)'), (impulseH2, 'H2 (highpass)'), (impulseH3, 'H3 (bandpass)')]:
    w, H = signal.freqz(h, 1, worN=512)
    plt.plot(w / np.pi, np.abs(H), label=name)
plt.xlabel('normalised frequency  (x pi rad/sample)'); plt.ylabel('|H(e^jw)|')
plt.title('Magnitude response of the three systems'); plt.legend(); plt.grid(alpha=0.3)

plt.show()
