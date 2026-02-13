#include "show.h"
static uint32_t secondsElapsed = 0;  // Tracks elapsed time since device start
void show_task(void *pvParameters)
{
   u32 lastWakeTime = getSysTickCnt();
   while(1)
    {	

			// vTaskDelayUntil(&lastWakeTime, F2T(RATE_50_HZ));
			vTaskDelayUntil(&lastWakeTime, F2T(1));
			secondsElapsed++;
			oled_show();    
    }
}

void oled_show(void)
{  
     //To DO
		char octalMM[3], octalSS[3]; // Two digits + null

    // Calculate minutes and seconds
    uint32_t minutes = secondsElapsed / 60;
    uint32_t seconds = secondsElapsed % 60;

    // Convert to octal strings
    snprintf(octalMM, sizeof(octalMM), "%02o", minutes);
    snprintf(octalSS, sizeof(octalSS), "%02o", seconds);

    // Display name
    OLED_ShowString(0, 0, (uint8_t*)"Octal clock");

    // Display octal clock below the name
    OLED_ShowString(0, 16, (uint8_t*)octalMM);
    OLED_ShowChar(16, 16, ':', 12, 1);
    OLED_ShowString(24, 16, (uint8_t*)octalSS);

    // Push the buffer to OLED
    OLED_Refresh_Gram();
	  		
	}

