import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

x = np.linspace(-12.5, 12.5, 101)

y1 = np.sin(x)    #Sine wave                    
y2 = np.cos(x)    # Cosine wave
y3 = signal.unit_impulse(101, 50)   #Unit Impulse wave
y4 =  x > 0   #Unit Step wave
y5 = (x > -3)*(x < 3)   #Unit square wave
y6 = signal.sawtooth(x, 0.5)    #Triangular wave
y7 = np.exp(x/10)   #Exponential wave
y8 = signal.sawtooth(x,0.9)   #Sawtooth wave
y9 = 1 * (x >= 0) - 1 * (x < 0)
y10 = np.sinc(x)   #Sinc wave

wave_name = ['Sine wave', 'Cosine wave', 'Unit Impulse wave', 'Unit step wave','Square wave','Triangular wave','Exponential wave','Sawtooth wave','Sign function','Sinc fucntion']
y = [y1,y2,y3,y4,y5,y6,y7,y8,y9,y10]

plt.figure(figsize=(10,8))
for i in range(10):
   plt.subplot(5,2,i+1)
   plt.plot(x, y[i])
   plt.title(wave_name[i])
   plt.ylabel('Amplitude')
   plt.xlabel('Time')

plt.tight_layout()
plt.show()
