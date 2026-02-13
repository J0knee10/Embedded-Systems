#include "system.h"

#define START_TASK_PRIO 4
#define START_STK_SIZE 256
TaskHandle_t StartTask_Handler;
EventGroupHandle_t ledEventGroup;
void start_task(void *pvParameters);
void ledTimerCallback(TimerHandle_t xTimer);
TimerHandle_t xAutoTimer;   // must declare handler
uint32_t ledOnTime = 1;    // ON duration in seconds, updated from USART
uint8_t ledState = 1;      // 1 = OFF
char msg[10];
int main (void)
{
	systemInit();
	
	// Initialize the timer that controls blinking
	xAutoTimer = xTimerCreate(
			"SendUART1Sec", 			// name
			pdMS_TO_TICKS(1000),	// period
			pdTRUE,								// auto reload
			(void*) 0,						// timer ID
			ledTimerCallback							// callback
		);
		xTimerStart(xAutoTimer, pdMS_TO_TICKS(0));
	if (xAutoTimer == NULL) {
			// Handle error in timer creation if needed
	}
	
	xTaskCreate((TaskFunction_t)start_task,
							(const char*)"start_task",
							(uint16_t)START_STK_SIZE,
							(void*)NULL,
							(UBaseType_t)START_TASK_PRIO,
							(TaskHandle_t*)&StartTask_Handler);
	// xTaskCreate(show_task, "show_task", 256, NULL, 2, NULL); //Lab 1 task
	
							
	vTaskStartScheduler();
						
}

						
void start_task(void *pvParameters)
{
	taskENTER_CRITICAL();
	ledEventGroup = xEventGroupCreate();
	// xTaskCreate(led_task, "led_task", LED_STK_SIZE, NULL, LED_TASK_PRIO, NULL); // Lab 1 task
	// xTaskCreate(buz_task, "buz_task", BUZ_STK_SIZE, NULL, BUZ_TASK_PRIO, NULL); // Lab 1 task
	xTaskCreate(btn_task, "btn_task", USERB_STK_SIZE, NULL, USERB_TASK_PRIO, NULL);
	vTaskDelete(StartTask_Handler);
	taskEXIT_CRITICAL();
}

void ledTimerCallback(TimerHandle_t xTimer)
{
		int i;  // declare at top
    sprintf(msg, "I am blinking\n\r");
		if (LED == 1)  // LED is OFF, turn ON
    {
        LED = 0;
        ledState = 0;
				for (i = 0; msg[i] != '\0'; i++){
            usart3_send(msg[i]);
				}
        xTimerChangePeriod(xAutoTimer, pdMS_TO_TICKS(ledOnTime*1000), 0);
    }
    else  // LED is ON, turn OFF
    {
        LED = 1;
        ledState = 1;
        xTimerChangePeriod(xAutoTimer, pdMS_TO_TICKS(1000), 0); // OFF for 1s
    }
}
