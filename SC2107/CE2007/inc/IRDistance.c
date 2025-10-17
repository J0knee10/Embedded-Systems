// IRDistance.c
// Runs on MSP432
// Provide mid-level functions that convert raw ADC
// values from the GP2Y0A21YK0F infrared distance sensors to
// distances in mm.
// Jonathan Valvano
// May 25, 2017

/* This example accompanies the books
   "Embedded Systems: Introduction to the MSP432 Microcontroller",
       ISBN: 978-1512185676, Jonathan Valvano, copyright (c) 2017
   "Embedded Systems: Real-Time Interfacing to the MSP432 Microcontroller",
       ISBN: 978-1514676585, Jonathan Valvano, copyright (c) 2017
   "Embedded Systems: Real-Time Operating Systems for ARM Cortex-M Microcontrollers",
       ISBN: 978-1466468863, , Jonathan Valvano, copyright (c) 2017
 For more information about my classes, my research, and my books, see
 http://users.ece.utexas.edu/~valvano/

Simplified BSD License (FreeBSD License)
Copyright (c) 2017, Jonathan Valvano, All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are
those of the authors and should not be interpreted as representing official
policies, either expressed or implied, of the FreeBSD Project.
*/

// Pololu #3543 Vreg (5V regulator output) connected to all three Pololu #136 GP2Y0A21YK0F Vcc's (+5V) and MSP432 +5V (J3.21)
// Pololu #3543 Vreg (5V regulator output) connected to positive side of three 10 uF capacitors physically near the sensors
// Pololu ground connected to all three Pololu #136 GP2Y0A21YK0F grounds and MSP432 ground (J3.22)
// Pololu ground connected to negative side of all three 10 uF capacitors
// MSP432 P9.0 (J5) (analog input to MSP432) connected to right GP2Y0A21YK0F Vout
// MSP432 P4.1 (J1.5) (analog input to MSP432) connected to center GP2Y0A21YK0F Vout
// MSP432 P9.1 (J5) (analog input to MSP432) connected to left GP2Y0A21YK0F Vout

#include <stdint.h>
#include "../inc/ADC14.h"
#include "msp.h"
#include <math.h>


/*
 * Routine to convert Filtered Raw ADC values to distance data.
 * Either via curve fitting (hyperbolic, polynomial, log etc), or piece-wise linear method.
 */

// estimate the curve coefficients
// Estimate A and B for the model: y = A / (x + B)
void estimateHyperbolicCoefficients(float *A_out, float *B_out) {
    float y[] = {13755, 9000, 6300, 5200, 4800, 4300}; // independent
    float x[] = {50, 100, 150, 200, 250, 300};         // dependent
    // int x[11] = {50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150}; 
    // int y[11] = {14850, 13630, 12550, 11450, 10470, 9830, 9030, 8400, 7830, 7500, 7020};        // dependent
    int n = sizeof(x)/sizeof(x[0]);

    float A = 1000000.0f;   // initial guess
    float B = 100.0f;       // initial guess
    float learningRateA = 0.1f;
    float learningRateB = 0.1f;
    int iterations = 200000;
    int iter, i;
    for (iter = 0; iter < iterations; iter++) {
        float dA = 0.0f, dB = 0.0f;
        float loss = 0.0f;

        for (i = 0; i < n; i++) {
            float denom = y[i] + B;
            if (fabsf(denom) < 1e-6f) continue;

            float x_pred = A / denom;
            float error = x_pred - x[i];
            loss += error * error;

            // Partial derivatives
            dA += 2 * error / denom;
            dB += 2 * error * (-A) / (denom * denom);
        }

        // Update coefficients
        A -= learningRateA * dA;
        B -= learningRateB * dB;

        // Optional: stop early if loss is very small
        if (loss < 1e-6f) break;

        // Optional debug
        // if (iter % 20000 == 0) printf("Iter %d: A=%.3f, B=%.3f, Loss=%.3f\n", iter, A, B, loss);
    }

    *A_out = A;
    *B_out = B;
}


int32_t LeftConvert(int32_t nl){        // returns left distance in mm
  // write this for Lab 4
    uint32_t length=0;
    // nl = 1000.010/(length+0.8514);
    length = 1000000/(-669.68+nl);

    return length;
}

int32_t CenterConvert(int32_t nc){   // returns center distance in mm
  // write this for Lab 4
    uint32_t length=0;
    length = 1000000/(-626.018 + nc);

    return length;
}

int32_t RightConvert(int32_t nr){      // returns right distance in mm
  // write this for Lab 4
    uint32_t length=0;
    length = 1000000/(-669.68+nr);


    return length;
}
