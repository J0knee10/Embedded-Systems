import numpy as np
import matplotlib.pyplot as plt

Fm=100
t1 = np.linspace(0,0.1,200)
y1 = np.sin(2 * np.pi * Fm * t1 + np.pi/6)  #Sine wave

fig, axs = plt.subplots(1, 2,figsize=(10, 4),constrained_layout=True)
axs[0].plot(t1,y1,'b',label = 'continuous')
axs[0].set_title("Sine wave")
axs[0].set_xlabel('time in sec')
axs[0].set_ylabel('y(t)')    

fs1=int(input("Enter the sampling frequency : ")) #sampling rate
n1 = np.arange(0,0.1*fs1)/fs1
x1=np.sin(2 * np.pi * Fm * n1 + np.pi/6); 
axs[1].plot(t1, y1, 'r--', alpha=0.5, label='continuous ref')
axs[1].stem(n1, x1, linefmt='b-', markerfmt='bo', basefmt='k-', label='samples')
axs[1].plot(n1, x1, 'b:', alpha=0.6)
axs[1].set_title("discrete time signal x(n) with fs = " + str(fs1))
axs[1].set_xlabel('time in sec')
axs[1].set_ylabel('y(t)')
axs[1].legend()

plt.show()