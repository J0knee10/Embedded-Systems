// RSLK Self Test via UART

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

#include "msp.h"
#include <stdint.h>
#include <string.h>
#include "..\inc\UART0.h"
#include "..\inc\EUSCIA0.h"
#include "..\inc\FIFO0.h"
#include "..\inc\Clock.h"
//#include "..\inc\SysTick.h"
#include "..\inc\SysTickInts.h"
#include "..\inc\CortexM.h"
#include "..\inc\TimerA1.h"
//#include "..\inc\Bump.h"
#include "..\inc\BumpInt.h"
#include "..\inc\LaunchPad.h"
#include "..\inc\Motor.h"
#include "../inc/IRDistance.h"
#include "../inc/ADC14.h"
#include "../inc/LPF.h"
#include "..\inc\Reflectance.h"
#include "../inc/TA3InputCapture.h"
#include "../inc/Tachometer.h"

#define P2_4 (*((volatile uint8_t *)(0x42098070)))
#define P2_3 (*((volatile uint8_t *)(0x4209806C)))
#define P2_2 (*((volatile uint8_t *)(0x42098068)))
#define P2_1 (*((volatile uint8_t *)(0x42098064)))
#define P2_0 (*((volatile uint8_t *)(0x42098060)))


void RSLK_Reset(void){
    DisableInterrupts();

    LaunchPad_Init();
    //Initialise modules used e.g. Reflectance Sensor, Bump Switch, Motor, Tachometer etc
    // ... ...

    EnableInterrupts();
}

// RSLK Self-Test
// Sample program of how the text based menu can be designed.
// Only one entry (RSLK_Reset) is coded in the switch case. Fill up with other menu entries required for Lab5 assessment.
// Init function to various peripherals are commented off.  For reference only. Not the complete list.

int main(void) {
  uint32_t cmd=0xDEAD, menu=0;

  DisableInterrupts();
  Clock_Init48MHz();  // makes SMCLK=12 MHz
  //SysTick_Init(48000,2);  // set up SysTick for 1000 Hz interrupts
  //Motor_Init();
  //Motor_Stop();
  LaunchPad_Init();
  //Bump_Init();
  //Bumper_Init();
  //IRSensor_Init();
  //Tachometer_Init();
  Reflectance_Init(); // Initialize reflectance sensors
  ADC0_InitSWTriggerCh17_12_16(); // Initialize ADC for IR sensors
  EUSCIA0_Init();     // initialize UART
  EnableInterrupts();

  while(1){                     // Loop forever
      // write this as part of Lab 5
      EUSCIA0_OutChar(CR); EUSCIA0_OutChar(LF);
      EUSCIA0_OutString("RSLK Testing"); EUSCIA0_OutChar(CR); EUSCIA0_OutChar(LF);
      EUSCIA0_OutString("[0] RSLK Reset"); EUSCIA0_OutChar(CR); EUSCIA0_OutChar(LF);
      EUSCIA0_OutString("[1] Motor Test"); EUSCIA0_OutChar(CR); EUSCIA0_OutChar(LF);
      EUSCIA0_OutString("[2] IR Sensor Test"); EUSCIA0_OutChar(CR); EUSCIA0_OutChar(LF);
      EUSCIA0_OutString("[3] Bumper Test"); EUSCIA0_OutChar(CR); EUSCIA0_OutChar(LF);
      EUSCIA0_OutString("[4] Reflectance Sensor Test"); EUSCIA0_OutChar(CR); EUSCIA0_OutChar(LF);
      EUSCIA0_OutString("[5] Tachometer Test"); EUSCIA0_OutChar(CR); EUSCIA0_OutChar(LF);
      EUSCIA0_OutString("[6] Reflectance Sensor 1 LED Blink Test"); EUSCIA0_OutChar(CR); EUSCIA0_OutChar(LF);
      EUSCIA0_OutString("[7] Move and Turn Right on Black Line"); EUSCIA0_OutChar(CR); EUSCIA0_OutChar(LF);
      EUSCIA0_OutString("[8] Move and Turn Right on IR Object"); EUSCIA0_OutChar(CR); EUSCIA0_OutChar(LF);

      EUSCIA0_OutString("CMD: ");
      cmd=EUSCIA0_InUDec();
      EUSCIA0_OutChar(CR); EUSCIA0_OutChar(LF);

      switch(cmd){
          case 0:
              RSLK_Reset();
              menu =1;
              cmd=0xDEAD;
              break;

          case 6: // Reflectance Sensor 1 LED Blink Test
              EUSCIA0_OutString("Starting Reflectance Sensor 1 LED Blink Test. Press any key to exit.\r\n");
              while(EUSCIA0_InStatus() == 0) { // Loop until a character is received
                  uint8_t sensor_data = Reflectance_Read(1000);
                  if (sensor_data & 0x01) { // Check if sensor 1 (bit 0) detects black
                      LaunchPad_LED(1); // Turn RED LED on
                      Clock_Delay1ms(100); // Blink delay
                      LaunchPad_LED(0); // Turn RED LED off
                      Clock_Delay1ms(100); // Blink delay
                  } else {
                      LaunchPad_LED(0); // Ensure RED LED is off
                  }
                  Clock_Delay1ms(10); // Small delay to prevent busy-waiting too much
              }
              while(EUSCIA0_InStatus()) { EUSCIA0_InChar(); } // Clear UART buffer
              menu = 1;
              cmd = 0xDEAD;
              break;

          case 7: // Move and Turn Right on Black Line
              EUSCIA0_OutString("Starting Move and Turn Right on Black Line Test. Press any key to exit.\r\n");
              Motor_Forward(3000, 3000); // Start moving forward
              while(EUSCIA0_InStatus() == 0) { // Loop until a character is received
                  uint8_t sensor_data = Reflectance_Read(1000);
                  if (sensor_data & 0x01) { // Check if sensor 1 (bit 0) detects black
                      Motor_Stop(); // Stop moving forward
                      Clock_Delay1ms(100); // Small delay for stability
                      Motor_Right(3000, 3000); // Turn right (adjust speed and duration as needed)
                      Clock_Delay1ms(500); // Calibrated delay for 90-degree turn (needs adjustment)
                      Motor_Stop(); // Stop turning
                      EUSCIA0_OutString("Black line detected, turned right.\r\n");
                      break; // Exit after turning
                  }
                  Clock_Delay1ms(10); // Small delay to prevent busy-waiting too much
              }
              Motor_Stop(); // Ensure motors are stopped if loop exits
              while(EUSCIA0_InStatus()) { EUSCIA0_InChar(); } // Clear UART buffer
              menu = 1;
              cmd = 0xDEAD;
              break;

          case 8: // Move and Turn Right on IR Object
              EUSCIA0_OutString("Starting Move and Turn Right on IR Object Test. Press any key to exit.\r\n");
              Motor_Forward(3000, 3000); // Start moving forward
              while(EUSCIA0_InStatus() == 0) { // Loop until a character is received
                  uint32_t ch17, ch12, ch16;
                  ADC_In17_12_16(&ch17, &ch12, &ch16); // Read all three IR sensors
                  int32_t center_distance_mm = CenterConvert(ch12); // Convert center sensor ADC to distance

                  if (center_distance_mm <= 200 && center_distance_mm > 0) { // Check if object within 20 cm (200 mm) and valid reading
                      Motor_Stop(); // Stop moving forward
                      Clock_Delay1ms(100); // Small delay for stability
                      Motor_Right(3000, 3000); // Turn right (adjust speed and duration as needed)
                      Clock_Delay1ms(500); // Calibrated delay for 90-degree turn (needs adjustment)
                      Motor_Stop(); // Stop turning
                      EUSCIA0_OutString("Object detected within 20cm, turned right.\r\n");
                      break; // Exit after turning
                  }
                  Clock_Delay1ms(10); // Small delay to prevent busy-waiting too much
              }
              Motor_Stop(); // Ensure motors are stopped if loop exits
              while(EUSCIA0_InStatus()) { EUSCIA0_InChar(); } // Clear UART buffer
              menu = 1;
              cmd = 0xDEAD;
              break;

          default:
              menu=1;
              break;
      }

      if(!menu)Clock_Delay1ms(3000);
      else{
          menu=0;
      }

      // ....
      // ....
  }
}

#if 0
//Sample program for using the UART related functions.
int Program5_4(void){
//int main(void){
    // demonstrates features of the EUSCIA0 driver
  char ch;
  char string[20];
  uint32_t n;
  DisableInterrupts();
  Clock_Init48MHz();  // makes SMCLK=12 MHz
  EUSCIA0_Init();     // initialize UART
  EnableInterrupts();
  EUSCIA0_OutString("\nLab 5 Test program for EUSCIA0 driver\n\rEUSCIA0_OutChar examples\n");
  for(ch='A'; ch<='Z'; ch=ch+1){// print the uppercase alphabet
     EUSCIA0_OutChar(ch);
  }
  EUSCIA0_OutChar(LF);
  for(ch='a'; ch<='z'; ch=ch+1){// print the lowercase alphabet
    EUSCIA0_OutChar(ch);
  }
  while(1){
    EUSCIA0_OutString("\n\rInString: ");
    EUSCIA0_InString(string,19); // user enters a string
    EUSCIA0_OutString(" OutString="); EUSCIA0_OutString(string); EUSCIA0_OutChar(LF);

    EUSCIA0_OutString("InUDec: ");   n=EUSCIA0_InUDec();
    EUSCIA0_OutString(" OutUDec=");  EUSCIA0_OutUDec(n); EUSCIA0_OutChar(LF);
    EUSCIA0_OutString(" OutUFix1="); EUSCIA0_OutUFix1(n); EUSCIA0_OutChar(LF);
    EUSCIA0_OutString(" OutUFix2="); EUSCIA0_OutUFix2(n); EUSCIA0_OutChar(LF);

    EUSCIA0_OutString("InUHex: ");   n=EUSCIA0_InUHex();
    EUSCIA0_OutString(" OutUHex=");  EUSCIA0_OutUHex(n); EUSCIA0_OutChar(LF);
  }
}
#endif
