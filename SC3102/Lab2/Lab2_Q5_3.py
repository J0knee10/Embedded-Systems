# Q5.3: is  y[n] = h3[n] * x[n]  a linear system?
#
# Let x1[n] = delta[n], x2[n] = -2 delta[n-15], so x[n] = x1[n] + x2[n].
# Linearity (superposition) requires
#     h3 * (x1 + x2)  ==  (h3 * x1) + (h3 * x2)
# Convolution is distributive over addition, so it must hold - we show it numerically.

import numpy as np
import matplotlib.pyplot as plt
from lti_utils import my_convolve, delta

impulseH1 = [0.06523, 0.14936, 0.21529, 0.2402, 0.21529, 0.14936, 0.06523]
impulseH2 = [-0.06523, -0.14936, -0.21529, 0.7598, -0.21529, -0.14936, -0.06523]
impulseH3 = np.convolve(impulseH1, impulseH2)

x1 = delta(30, 0, 1.0)          # x1[n] =  delta[n]
x2 = delta(30, 15, -2.0)        # x2[n] = -2 delta[n-15]

# ---- route A: filter separately, then add (additivity) ----
y1 = my_convolve(x1, impulseH3)
y2 = my_convolve(x2, impulseH3)
y_sum = y1 + y2

plt.figure()
plt.stem(y_sum, linefmt='r--')
plt.plot(y_sum, 'g-+')
plt.title('y1[n] + y2[n]')
plt.xlabel('sample n'); plt.ylabel('y[n]')

# ---- route B: add first, then filter ----
y_combined = my_convolve(x1 + x2, impulseH3)

plt.figure()
plt.stem(y_combined, linefmt='r--')
plt.plot(y_combined, 'g-+')
plt.title('h3[n] * (x1[n] + x2[n])')
plt.xlabel('sample n'); plt.ylabel('y[n]')

# ---- the two routes overlaid, plus the error ----
fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
ax[0].plot(y_sum, 'g-+', label='y1[n] + y2[n]')
ax[0].plot(y_combined, 'r--', label='h3[n] * (x1[n] + x2[n])')
ax[0].legend(); ax[0].set_ylabel('y[n]'); ax[0].set_title('The two routes lie on top of each other')
ax[1].plot(y_sum - y_combined, 'k')
ax[1].set_xlabel('sample n'); ax[1].set_ylabel('difference')
ax[1].set_title('Difference (numerical noise only)')
plt.tight_layout()

print('max |y1+y2 - h3*(x1+x2)| = %.2e  -> additive' % np.max(np.abs(y_sum - y_combined)))

# ---- homogeneity (scaling): h3 * (a*x1) == a * (h3 * x1) ----
a = 3.7
print('max |h3*(a*x1) - a*(h3*x1)| = %.2e  -> homogeneous'
      % np.max(np.abs(my_convolve(a * x1, impulseH3) - a * y1)))
print('=> additive + homogeneous => the system is LINEAR')

plt.show()
