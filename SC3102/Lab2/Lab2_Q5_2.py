# Q5.2: response of H1, H2, H3 to  x[n] = delta[n] - 2*delta[n-15]
#
# The lab asks for our OWN convolution module - see lti_utils.my_convolve.
# np.convolve / scipy.signal.lfilter are plotted on top only as a check.

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from lti_utils import my_convolve, delta

impulseH1 = [0.06523, 0.14936, 0.21529, 0.2402, 0.21529, 0.14936, 0.06523]
impulseH2 = [-0.06523, -0.14936, -0.21529, 0.7598, -0.21529, -0.14936, -0.06523]
impulseH3 = np.convolve(impulseH1, impulseH2)

# x[n] = delta[n] - 2 delta[n-15]
x1 = delta(30, 0, 1.0) + delta(30, 15, -2.0)

plt.figure()
plt.stem(x1, linefmt='k-', basefmt=' ')
plt.title('input  x[n] = $\delta$[n] - 2$\delta$[n-15]')
plt.xlabel('sample n'); plt.ylabel('x[n]')

for h, name in [(impulseH1, 'H1'), (impulseH2, 'H2'), (impulseH3, 'H3')]:
    y_mine = my_convolve(x1, h)                 # our module
    y_np = np.convolve(x1, h)                   # reference
    y_lf = signal.lfilter(h, [1], x1)           # reference, truncated to len(x1)

    plt.figure()
    plt.stem(y_mine, linefmt='r--')
    plt.plot(y_lf, 'g-+')
    plt.title('x convolve with ' + name)
    plt.xlabel('sample n'); plt.ylabel('y[n]')
    plt.legend(['scipy lfilter', 'my_convolve'])

    print('%s: max |my_convolve - np.convolve| = %.2e   length %d'
          % (name, np.max(np.abs(y_mine - y_np)), len(y_mine)))

# Time invariance: the second term is just the first, delayed by 15 and scaled by -2.
y3 = my_convolve(x1, impulseH3)
h3_at_0 = my_convolve(delta(30, 0), impulseH3)
h3_at_15 = my_convolve(delta(30, 15), impulseH3)
print('\ntime invariance, max |y - (h3@0 - 2*h3@15)| = %.2e'
      % np.max(np.abs(y3 - (h3_at_0 - 2 * h3_at_15))))

plt.show()
