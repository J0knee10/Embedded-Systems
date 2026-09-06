import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy import io # this submodule let's us load the signal we want

EEG_data = io.loadmat('EEG_exp.mat', squeeze_me = True)

# print all the variables that exist in the dictionary
print(EEG_data.keys())

# this contains the EEG data
EEG = EEG_data['EEG']
# this contains the sampling rate, in Hz (or samples/second)
fs = EEG_data['fs']

dt = 0.001  
T_exp = 720  
t_EEG = np.arange(0,720,0.001)  
d_rate = 10 #Downsampling rate

# Plotting the signal and its downsampled version
plt.figure(figsize=(15,3))

plt.plot(t_EEG, EEG, label='EEG')
plt.plot(t_EEG[1:1000:d_rate], EEG[1:1000:d_rate], '.-', label='Downsampled', alpha=0.8)
plt.xlim([0,1]); plt.ylim([-15, 15]);
plt.legend()
plt.xlabel("Time")
plt.ylabel("Voltage")
plt.show()
