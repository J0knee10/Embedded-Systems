import numpy as np
import matplotlib.pyplot as plt

# define gcd function
def gcd(x, y):
   """This function implements the Euclidian algorithm
   to find G.C.D. of two numbers"""

   while(y):
       x, y = y, x % y

   return x

# define lcm function
def lcm(x, y):
   """This function takes two
   integers and returns the L.C.M."""
   lcm = (x*y)//gcd(x,y)
   return lcm

# define the main function 
def main():
   A=0.5; F1=10; Phi = 0; Fs=60; sTime=0; eTime = 1;
   #2*pi*10/60 => w1= pi/3 => N =6
   t1 = np.arange(sTime,eTime,1.0/Fs)
   y1 = A*np.cos(2 * np.pi * F1 * t1 + Phi)
   B=0.3; F2=15;
   #2*pi*15/60 => w2=pi/2 => N = 4
   t2 = np.arange(sTime,eTime,1.0/Fs)
   y2 = B*np.cos(2 * np.pi * F2 * t2 + Phi)
   
   y3 = y1+y2

   #how many samples to store J cycles of y
   nSamplesPeriod1 = int(Fs/F1)
   nSamplesPeriod2 = int(Fs/F2)
   nSamplesPeriod_LCM = lcm( int(nSamplesPeriod1),int(nSamplesPeriod2))
   # When we have two signals, the Least common mutiplier is the period of the added waveform!

   s = 'Number of samples per cycle N1='+ repr(nSamplesPeriod1)+'  N2='+ repr(nSamplesPeriod2) + '  LCM = '+ repr(nSamplesPeriod_LCM)
   print(s)
   nSamplesPeriod_int = int(nSamplesPeriod_LCM)

   J = 3   # lets plot J cycles
   plt.figure(1)
   #plt.plot(t1[0:nSamplesPeriod_int*J], y1[0:nSamplesPeriod_int*J],'r--o')
   #plt.plot(t1[0:nSamplesPeriod_int*J], y2[0:nSamplesPeriod_int*J],'g--o')
   plt.plot( y1[0:nSamplesPeriod_int*J],'r--o',label='y1')
   plt.plot( y2[0:nSamplesPeriod_int*J],'g--o',label='y2')
   plt.xlabel('sample n'); plt.ylabel('y[n]')
   plt.legend()
   plt.grid()

   plt.figure(2)
   #plt.plot(t1[0:nSamplesPeriod_int*J], y3[0:nSamplesPeriod_int*J],'b--o')
   plt.plot( y3[0:nSamplesPeriod_int*J],'b--o',label='y3')
   plt.xlabel('sample n'); plt.ylabel('y[n]')
   plt.grid()
   plt.legend()
   plt.show()

if __name__ == '__main__':
    main()
