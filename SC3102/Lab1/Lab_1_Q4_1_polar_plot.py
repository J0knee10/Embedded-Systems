# plotting 3D complex plane
import numpy as np
import matplotlib.pyplot as plt


def main():
    #y[n] = Aexp( (j*w1*n+Phi)) = A( cos(w1*n+Phi) +j*sin(w1*n+Phi))

    # A=0.98; w1=2*np.pi/36; Phi = 0;  numSamples = 55
    A=0.98; w1=2*np.pi/18; Phi = np.pi/6;  numSamples = 55
    n = np.arange(0,numSamples,1)
    y1 = np.multiply(np.power(A,n), np.exp(1j*(w1*n+Phi)))

    #plotting in 2-d, both the real and imag values
    plt.figure(1)
    plt.plot(n, y1[0:numSamples].real,'r--o', label='Real')
    plt.plot(n, y1[0:numSamples].imag,'g--o', label='Imag')
    plt.xlabel('sample n'); plt.ylabel('y[n]')
    plt.grid(True)
    plt.legend()

    #plotting in polar
    plt.figure(2)
    axp = plt.subplot(111, projection='polar')
    for x in y1:
        axp.plot([0, np.angle(x)], [0, np.abs(x)], marker='o')

    # plotting 3D complex plane
    plt.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    reVal = y1.real
    imgVal = y1.imag
    ax.plot(n, reVal, imgVal, label='complex exponential phasor')
    ax.scatter(n, reVal, imgVal, c='r', marker='o')
    ax.set_xlabel('sample n')
    ax.set_ylabel('real')
    ax.set_zlabel('imag')
    ax.legend()

    plt.show()

if __name__ == '__main__':
    main()
