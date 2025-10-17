import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Example data
x = np.array([1, 2, 3, 4, 5])
y = np.array([2.5, 1.8, 1.4, 1.1, 0.9])

# Define your hyperbolic model
def hyperbola(x, A, B):
    return A / (x + B)

# Fit the model to your data
params, cov = curve_fit(hyperbola, x, y, p0=[1, 1])  # initial guesses for A and B
A, B = params
print(f"A = {A:.4f}, B = {B:.4f}")

# Create fitted curve
x_fit = np.linspace(min(x), max(x), 100)
y_fit = hyperbola(x_fit, A, B)

# Plot
plt.scatter(x, y, color='red', label='Data points')
plt.plot(x_fit, y_fit, color='blue', label=f'Fit: y = {A:.2f}/(x + {B:.2f})')
plt.legend()
plt.show()
