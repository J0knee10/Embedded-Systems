#include "buz.h"

int buz_Count=2000;
extern EventGroupHandle_t ledEventGroup; // Tell buz.c that it exists globally
//buz initialization
void buz_Init(void)
{
	GPIO_InitTypeDef  GPIO_InitStructure;
	
  RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOB, ENABLE);    //Enable APB Clock
	
  GPIO_InitStructure.GPIO_Pin =  BUZ_PIN;                  //buz Pin
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT;            //Push pull output
  GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_100MHz;        //100MHz
  GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_UP;
  GPIO_Init(BUZ_PORT, &GPIO_InitStructure);                    //Initialize buz GPIO
	GPIO_SetBits(BUZ_PORT,BUZ_PIN);
	BUZ = 0;
}

void buz_task(void *pvParameters)
{
	int ledCycleCount = 0;
    while(1)
    {
				// Wait for one LED cycle (bit 0)
        xEventGroupWaitBits(ledEventGroup,
                            0x01,
                            pdTRUE,  // clear the bit after reading
                            pdFALSE, // wait for any bit (not all)
                            portMAX_DELAY);

        ledCycleCount++;

        // ON for 2 cycles, OFF for 1
        if (ledCycleCount <= 2)
        {
            // BUZ = 1; // ON, buzzer too noisy when i am working, so i comment it out
        }
        else
        {
            BUZ = 0; // OFF
            ledCycleCount = 0; // reset counter
        } 
    }
}  
