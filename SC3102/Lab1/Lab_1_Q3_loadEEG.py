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

# let's plot the signal
plt.figure(figsize=(15,3))
plt.plot(EEG)
# ALWAYS label your plot axes in this course (and ever)
plt.xlabel('Sample Number')
plt.ylabel('Voltage (uV)')

# now let's zoom in to see more detail
plt.figure(figsize=(15,3))
plt.plot(EEG) # '.' means plot the data points as individual dots without linking them
plt.xlim([0,1000]) # this limits the x-axis shown
plt.ylim([-15, 15]); # this limits the y-axis shown
plt.xlabel('Sample Number')
plt.ylabel('Voltage (uV)')
plt.show()