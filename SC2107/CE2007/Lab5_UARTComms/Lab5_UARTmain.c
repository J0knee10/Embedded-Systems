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
#include "..\inc\Clock.h"
#include "..\inc\SysTick.h"
//#include "..\inc\SysTickInts.h"
#include "..\inc\CortexM.h"
#include "..\inc\TimerA1.h"
#include "..\inc\TimerA2.h"
#include "..\inc\Bump.h"
//#include "..\inc\BumpInt.h"
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
volatile uint8_t reflectance_data = 0;
volatile uint8_t bump_data = 0x3F;
volatile uint8_t rfCentre = 0;


void RSLK_Reset(void){
    DisableInterrupts();

    LaunchPad_Init();
    //Initialise modules used e.g. Reflectance Sensor, Bump Switch, Motor, Tachometer etc
    // ... ...

    EnableInterrupts();
}
void MyBumpHandler(uint8_t data){
    // data = bump state (0-63)
    bump_data = data;
}

void PollBumpSwitches(void){
  bump_data = Bump_Read(); // Periodically poll the bump switches
}

void PollReflectance(void){
  reflectance_data = Reflectance_Center(1000); // Periodically poll the reflectance sensor
}

void SysTick_Handler(void){
    // empty handler to prevent crash
}
void TimedPause(uint32_t time){
  Clock_Delay1ms(time);         // run for a while and stop
  Motor_Stop();
  while(LaunchPad_Input()==0);  // wait for touch
  while(LaunchPad_Input());     // wait for release
}

// void SysTick_Handler(void){
//     // empty handler to prevent crash
// }


// RSLK Self-Test
// Sample program of how the text based menu can be designed.
// Only one entry (RSLK_Reset) is coded in the switch case. Fill up with other menu entries required for Lab5 assessment.
// Init function to various peripherals are commented off.  For reference only. Not the complete list.

int main(void) {
  uint32_t cmd=0xDEAD, menu=0;

  DisableInterrupts();
  Clock_Init48MHz();  // makes SMCLK=12 MHz
  SysTick_Init();  // set up SysTick for 1000 Hz interrupts
  Motor_Init();
  Motor_Stop();
  LaunchPad_Init();
  Bump_Init(&MyBumpHandler);
  //Bumper_Init();
  //IRSensor_Init();
  //Tachometer_Init();
  Reflectance_Init(); // Initialize reflectance sensors
  ADC0_InitSWTriggerCh17_12_16(); // Initialize ADC for IR sensors
  UART0_Init();     // initialize UART
  TimerA1_Init(&PollReflectance, 50000); 
  //TimerA1_Init(&PollBumpSwitches, 5000); // 10ms polling for bump switches
  EnableInterrupts();

  while(1){                     // Loop forever
      // write this as part of Lab 5
      UART0_OutChar(CR); UART0_OutChar(LF);
      UART0_OutString("RSLK Testing"); UART0_OutChar(CR); UART0_OutChar(LF);
      UART0_OutString("[0] RSLK Reset"); UART0_OutChar(CR); UART0_OutChar(LF);
      UART0_OutString("[1] Motor Test"); UART0_OutChar(CR); UART0_OutChar(LF);
      UART0_OutString("[2] IR Sensor Test"); UART0_OutChar(CR); UART0_OutChar(LF);
      UART0_OutString("[3] Bumper Test"); UART0_OutChar(CR); UART0_OutChar(LF);
      UART0_OutString("[4] Reflectance Sensor Test"); UART0_OutChar(CR); UART0_OutChar(LF);
      UART0_OutString("[5] Tachometer Test"); UART0_OutChar(CR); UART0_OutChar(LF);
      UART0_OutString("[6] L Task 1 (Blink LED IR sensor)"); UART0_OutChar(CR); UART0_OutChar(LF);
      UART0_OutString("[7] L Task 2 (Blink LED bump switch) SKIPPED"); UART0_OutChar(CR); UART0_OutChar(LF);
      UART0_OutString("[8] M Task (Reflectance and motor)"); UART0_OutChar(CR); UART0_OutChar(LF);
      UART0_OutString("[10] H Task (Maze use reflectance)"); UART0_OutChar(CR); UART0_OutChar(LF);

      UART0_OutString("CMD: ");
      cmd=UART0_InUDec();
      UART0_OutChar(CR); UART0_OutChar(LF);

      switch(cmd){
          case 0:
              RSLK_Reset();
              menu =1;
              cmd=0xDEAD;
              break;

          case 6: // L Task 1
                // UART0_OutString("Starting Reflectance Sensor 1 LED Blink Test. Press any key to exit.\r\n");
                // while(UART0_InStatus() == 0) { // Loop until a character is received
                //     uint8_t sensor_data = Reflectance_Read(1000);
                //     if (sensor_data & 0x01) { // Check if sensor 1 (bit 0) detects black
                //         LaunchPad_LED(1); // Turn RED LED on
                //         Clock_Delay1ms(100); // Blink delay
                //         LaunchPad_LED(0); // Turn RED LED off
                //         Clock_Delay1ms(100); // Blink delay
                //     } else {
                //         LaunchPad_LED(0); // Ensure RED LED is off
                //     }
                //     Clock_Delay1ms(10); // Small delay to prevent busy-waiting too much
                // }
                UART0_OutString("L Task 1 (Blink LED IR sensor).\r\n");
                while(UART0_InStatus() == 0) { // Loop until a character is received
                  uint32_t ch17, ch12, ch16;
                  ADC_In17_12_16(&ch17, &ch12, &ch16); // Read all three IR sensors
                  int32_t center_distance_mm = CenterConvert(ch12); // Convert center sensor ADC to distance

                  if (center_distance_mm <= 250 && center_distance_mm > 150) { // Check if object within 20 cm (200 mm) and valid reading
                        LaunchPad_LED(1); // Turn RED LED on
                        Clock_Delay1ms(100); // Blink delay
                        LaunchPad_LED(0); // Turn RED LED off
                        Clock_Delay1ms(100); // Blink delay
                        UART0_OutString("Object detected within 20cm, blink LED.\r\n");
                        // break; // Exit after turning
                  }
                  Clock_Delay1ms(10); // Small delay to prevent busy-waiting too much
              }

              while(UART0_InStatus()) { UART0_InChar(); } // Clear UART buffer
              menu = 1;
              cmd = 0xDEAD;
              break;
            case 7: // Move and Turn Right on IR Object
                UART0_OutString("Starting Move and Turn Right on IR Object Test. Press any key to exit.\r\n");
                Motor_Forward(3000, 3000); // Start moving forward
                while(UART0_InStatus() == 0) { // Loop until a character is received
                    uint32_t ch17, ch12, ch16;
                    ADC_In17_12_16(&ch17, &ch12, &ch16); // Read all three IR sensors
                    int32_t center_distance_mm = CenterConvert(ch12); // Convert center sensor ADC to distance

                    if (center_distance_mm <= 200 && center_distance_mm > 0) { // Check if object within 20 cm (200 mm) and valid reading
                        Motor_Stop(); // Stop moving forward
                        Clock_Delay1ms(100); // Small delay for stability
                        Motor_Right(3000, 3000); // Turn right (adjust speed and duration as needed)
                        Clock_Delay1ms(500); // Calibrated delay for 90-degree turn (needs adjustment)
                        Motor_Stop(); // Stop turning
                        UART0_OutString("Object detected within 20cm, turned right.\r\n");
                        break; // Exit after turning
                    }
                    Clock_Delay1ms(10); // Small delay to prevent busy-waiting too much
                }
                Motor_Stop(); // Ensure motors are stopped if loop exits
                while(UART0_InStatus()) { UART0_InChar(); } // Clear UART buffer
                menu = 1;
                cmd = 0xDEAD;
                break;
              

          case 8: // Move and Turn Right on Black Line
                UART0_OutString("M task, press SW1/2 to start.\r\n");
                TimedPause(500);
                while (reflectance_data != 0x03) {
                    Motor_Right(700, 700);
                }
                Motor_Stop();
                Motor_Forward(1000,1000);
                Clock_Delay1ms(2000);
                while(reflectance_data!=0x03){};
                Motor_Stop();
            //   Motor_Forward(3000, 3000); // Start moving forward
            //   while(UART0_InStatus() == 0) { // Loop until a character is received
            //       uint8_t sensor_data = Reflectance_Read(1000);
            //       if (~sensor_data & 0x01) { // Check if sensor 1 (bit 0) detects black
            //           Motor_Stop(); // Stop moving forward
            //           Clock_Delay1ms(100); // Small delay for stability
            //           Motor_Right(3000, 3000); // Turn right (adjust speed and duration as needed)
            //           Clock_Delay1ms(500); // Calibrated delay for 90-degree turn (needs adjustment)
            //           Motor_Stop(); // Stop turning
            //           UART0_OutString("Black line detected, turned right.\r\n");
            //           break; // Exit after turning
            //       }
            //       Clock_Delay1ms(10); // Small delay to prevent busy-waiting too much
            //   }
            //   Motor_Stop(); // Ensure motors are stopped if loop exits
              while(UART0_InStatus()) { UART0_InChar(); } // Clear UART buffer
              Motor_Stop(); // Ensure motors are stopped if loop exits
              menu = 1;
              cmd = 0xDEAD;
              break;

          case 9: // Bump Switch Test - Turn Right
              UART0_OutString("Starting Bump Switch Test (Turn Right on Bump). Press any key to exit.\r\n");
              Motor_Forward(3000, 3000); // Start moving forward
              while(UART0_InStatus() == 0) { // Loop until a character is received (to exit test)
                  if (bump_data != 0x3F) { // Check if any bump switch is pressed (value updated by TimerA1 ISR)
                      Motor_Stop();
                      Clock_Delay1ms(100);
                      Motor_Right(3000, 3000);
                      Clock_Delay1ms(500); // Calibrated delay for turn (adjust as needed)
                      Motor_Stop();
                      UART0_OutString("Bump detected, turned right.\r\n");
                      // Wait until switches are released. The TimerA1 ISR will update bump_data.
                      UART0_OutString("Please release bump switches to continue...\r\n");
                      while(bump_data != 0x3F) {
                          Clock_Delay1ms(50);
                      }
                      break; // Exit the inner while loop after turning
                  }
                  Clock_Delay1ms(10); // Small delay to prevent busy-waiting too much
              }
              Motor_Stop(); // Ensure motors are stopped if loop exits
              while(UART0_InStatus()) { UART0_InChar(); } // Clear UART buffer
              menu = 1;
              cmd = 0xDEAD;
              break;

             case 10: // Move and Turn Right on Black Line
                UART0_OutString("H task, press SW1/2 to start.\r\n");
                TimedPause(500);

                //Forward
                Motor_Forward(1000, 1000);
                while (reflectance_data != 0x03) {};
                Motor_Stop();

                //Right
                Motor_Right(1000, 1000);
                Clock_Delay1ms(1300); //**** 1400ms TO TURN ****
                Motor_Stop();

                //Forward
                Motor_Forward(1000, 1000);
                Clock_Delay1ms(2500);
                Motor_Stop();

                //Left
                Motor_Left(1000, 1000);
                Clock_Delay1ms(1400); //**** 1400ms TO TURN ****
                Motor_Stop();

                //Forward
                Motor_Forward(1000, 1000);
                while (reflectance_data != 0x03) {};
                Motor_Stop();

                                //Left
                Motor_Left(1000, 1000);
                Clock_Delay1ms(1400); //**** 1400ms TO TURN ****
                Motor_Stop();

                       //Forward
                Motor_Forward(1000, 1000);
                Clock_Delay1ms(2000);
                Motor_Stop();


                                                //Left
                Motor_Left(1000, 1000);
                Clock_Delay1ms(1400); //**** 1400ms TO TURN ****
                Motor_Stop();

                       //Forward
                Motor_Forward(1000, 1000);
                Clock_Delay1ms(2500);
                Motor_Stop();

                                //Right
                Motor_Right(1000, 1000);
                Clock_Delay1ms(1300); //**** 1400ms TO TURN ****
                Motor_Stop();

                
                //Forward
                Motor_Forward(1000, 1000);
                Clock_Delay1ms(1500);
                while (reflectance_data != 0x03) {};
                Motor_Stop();

                // Motor_Forward(1000,1000);
                // Clock_Delay1ms(2000);
                // while(reflectance_data!=0x03){};
                // Motor_Stop();
                // while(UART0_InStatus()) { UART0_InChar(); } // Clear UART buffer
                Motor_Stop(); // Ensure motors are stopped if loop exits
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
  UART0_Init();     // initialize UART
  EnableInterrupts();
  UART0_OutString("\nLab 5 Test program for EUSCIA0 driver\n\rUART0_OutChar examples\n");
  for(ch='A'; ch<='Z'; ch=ch+1){// print the uppercase alphabet
     UART0_OutChar(ch);
  }
  UART0_OutChar(LF);
  for(ch='a'; ch<='z'; ch=ch+1){// print the lowercase alphabet
    UART0_OutChar(ch);
  }
  while(1){
    UART0_OutString("\n\rInString: ");
    UART0_InString(string,19); // user enters a string
    UART0_OutString(" OutString="); UART0_OutString(string); UART0_OutChar(LF);

    UART0_OutString("InUDec: ");   n=UART0_InUDec();
    UART0_OutString(" OutUDec=");  UART0_OutUDec(n); UART0_OutChar(LF);
    UART0_OutString(" OutUFix1="); UART0_OutUFix1(n); UART0_OutChar(LF);
    UART0_OutString(" OutUFix2="); UART0_OutUFix2(n); UART0_OutChar(LF);

    UART0_OutString("InUHex: ");   n=UART0_InUHex();
    UART0_OutString(" OutUHex=");  UART0_OutUHex(n); UART0_OutChar(LF);
  }
}
#endif
